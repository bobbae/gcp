package server

import (
	"context"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"cloud.google.com/go/storage"
	"google.golang.org/api/iterator"
)

const DEFAULT_DIRLIST_PAGE_SIZE = 100

type OBJECT_TYPE uint

const (
	OBJECT_TYPE_NOTFOUND OBJECT_TYPE = 0
	OBJECT_TYPE_FILE     OBJECT_TYPE = 1
	OBJECT_TYPE_DIR      OBJECT_TYPE = 2
)

func (o OBJECT_TYPE) String() string {
	names := [...]string{
		"NOTFOUND",
		"FILE",
		"DIR",
	}
	if o < 0 || o > OBJECT_TYPE_DIR {
		return "UNKNOWN"
	}
	return names[o]
}

func gcsClient(ctx context.Context, w http.ResponseWriter) *storage.Client {
	gcsClient, err := storage.NewClient(ctx)
	if err != nil || gcsClient == nil {
		msg := fmt.Sprintf("Could not initialize GCS client: %v", err)
		log.Print(msg)
		http.Error(w, msg, http.StatusInternalServerError)
		return nil
	}
	return gcsClient
}

func gcsBucketHandle(ctx context.Context, w http.ResponseWriter, gcsClient *storage.Client) *storage.BucketHandle {
	bucketName := os.Getenv("BUCKET")
	if bucketName == "" {
		msg := fmt.Sprintf("Bucket name must be specified in environment variable BUCKET. Got BUCKET=%s", bucketName)
		log.Print(msg)
		http.Error(w, msg, http.StatusInternalServerError)
		return nil
	}
	bucketHandle := gcsClient.Bucket(bucketName)
	return bucketHandle
}

type Server struct {
	DirListPageSize int
}

type ObjAttrsWithErr struct {
	Attrs *storage.ObjectAttrs
	Error error
}

func fileOrDirExists(ctx context.Context, bucketHandle *storage.BucketHandle, gcsPath string, objAttrsWithErr *ObjAttrsWithErr) (bool, OBJECT_TYPE) {
	if objAttrsWithErr.Error == nil {
		// it's a file
		return true, OBJECT_TYPE_FILE
	}

	//
	// check to see if it's a dir
	//

	// GCS faux directory structure is complicated:
	// bucketHandle.Object() cannot locate directories; however, bucketHandle.Objects() can.
	q := storage.Query{
		Delimiter: "/",
		Prefix:    gcsPath,
		Versions:  false,
	}
	// storage.ObjectIterator doesn't have a peek() method; if it did, we could do bucketHandle.Objects()
	// once for the whole request rather than once here and again in dirList()
	objectIterator := bucketHandle.Objects(ctx, &q)
	next, err := objectIterator.Next()

	if next != nil && err != iterator.Done {
		return true, OBJECT_TYPE_DIR
	}

	return false, OBJECT_TYPE_NOTFOUND
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if s.DirListPageSize == 0 {
		s.DirListPageSize = DEFAULT_DIRLIST_PAGE_SIZE
	}
	ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
	defer cancel()
	gcsClient := gcsClient(ctx, w)
	bucketHandle := gcsBucketHandle(ctx, w, gcsClient)

	gcsPath := getGCSPath(r)
	w.Header().Add("X-GCS-PATH", gcsPath)
	w.Header().Add("X-GCS-BUCKET", os.Getenv("BUCKET"))
	w.Header().Add("Access-Control-Allow-Origin", "*")
	// special case: root dir
	if gcsPath == "" {
		s.dirList(ctx, w, r, bucketHandle)
		return
	}

	objHandle := bucketHandle.Object(gcsPath)
	attrs, err := objHandle.Attrs(ctx)
	objAttrsWithErr := ObjAttrsWithErr{
		Attrs: attrs,
		Error: err,
	}
	found, fileOrDir := fileOrDirExists(ctx, bucketHandle, gcsPath, &objAttrsWithErr)
	if !found {
		msg := fmt.Sprintf("HTTP 404: \"%s\" not found", gcsPath)
		http.Error(w, msg, http.StatusNotFound)
		return
	}
	if fileOrDir == OBJECT_TYPE_DIR {
		s.dirList(ctx, w, r, bucketHandle)
		return
	}

	// serve object contents back to user
	objReader, err := objHandle.NewReader(ctx)
	if err != nil {
		msg := fmt.Sprintf("Could not create objReader: %v", err)
		log.Print(msg)
		http.Error(w, msg, http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", attrs.ContentType)
	w.WriteHeader(http.StatusOK)
	io.Copy(w, objReader)
}

func getGCSPath(r *http.Request) string {
	return r.URL.Path[1:] // strip leading "/"
}

// do not call this function unless you know the gcsPath is a directory
func (s *Server) dirList(ctx context.Context, w http.ResponseWriter, r *http.Request, bucketHandle *storage.BucketHandle) {
	tmpl, err := template.New("").Funcs(template.FuncMap{
		"hasSuffix": func(s, suffix string) bool {
			return strings.HasSuffix(s, suffix)
		},
	}).Parse(PAGE_TEMPLATE)
	if err != nil {
		msg := fmt.Sprintf("Could not parse template: %v", err)
		log.Print(msg)
		http.Error(w, msg, http.StatusInternalServerError)
		return
	}
	gcsPath := getGCSPath(r)
	if gcsPath != "" && !strings.HasSuffix(gcsPath, "/") {
		gcsPath = gcsPath + "/"
	}
	q := storage.Query{
		Delimiter: "/",
		Prefix:    gcsPath,
		Versions:  false,
	}
	objectIterator := bucketHandle.Objects(ctx, &q)
	var dirEntries []*storage.ObjectAttrs
	pageToken := r.URL.Query().Get("pageToken")
	nextPageToken, err := iterator.NewPager(objectIterator, s.DirListPageSize, pageToken).NextPage(&dirEntries)
	if err != nil {
		msg := fmt.Sprintf("Could not get next page of dir entries: %v", err)
		log.Print(msg)
		http.Error(w, msg, http.StatusInternalServerError)
		return
	}
	type TemplateStruct struct {
		DirName       string
		NextPageToken string
		DirEntries    []*storage.ObjectAttrs
	}
	dirName := getGCSPath(r)
	if dirName == "" {
		dirName = "/"
	}
	templateVars := TemplateStruct{
		DirName:       dirName,
		NextPageToken: nextPageToken,
		DirEntries:    dirEntries,
	}
	err = tmpl.Execute(w, templateVars)
	if err != nil {
		msg := fmt.Sprintf("Could not execute template: %v", err)
		log.Print(msg)
		http.Error(w, msg, http.StatusInternalServerError)
		return
	}
}

var PAGE_TEMPLATE = `
<html>
  <head>
    <title>Index of {{ .DirName }}</title>
    <style>
      table, th, td {
      border: 0px;
      padding: 2px;
      padding-right: 15px;
      }
    </style>
  </head>
  <body>
    <h1>Index of {{ .DirName }}</h1>
    <hr>
    <table>
      <tr><th align="left">Name</th><th>&nbsp;</th><th align="left">Content-Type</th><th>Created</th><th>Updated</th></tr>
        <tr>
          <td><pre><a href="..">../</a></pre></td>
          <td><pre>dir</pre></td>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
        </tr>
      {{- /* Iterate over directories first, they will have dir name in $key.Prefix. $key.Name will be "" */ -}}
      {{- range $key, $value := .DirEntries -}}
        {{- if ne $value.Prefix "" -}}
        <tr>
          <td><pre><a href="/{{ $value.Prefix }}">{{ $value.Prefix }}</a></pre></td>
          <td><pre>dir</pre></td>
          <td><pre>{{ $value.ContentType }}</pre></td>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
        </tr>
        {{- end -}}
      {{- end -}}
      {{- /* Iterate over file next, they will have file name in $key.Name. $key.Prefix will be "" */ -}}
      {{- range $key, $value := .DirEntries -}}
        {{- if ne $value.Name "" -}}
          {{- /* exclude faux directory entries that come in as files. For example,
                 if you have /folder1/test.txt, you'll end up with: $value.Name="folder1/",
                 $value.Name="folder1/test.txt" */ -}}
          {{- if not (hasSuffix $value.Name "/") -}}
            <tr>
              <td><pre><a href="/{{ $value.Name }}">{{ $value.Name }}</a></pre></td>
              <td><pre>file</pre></td>
              <td><pre>{{ $value.ContentType }}</pre></td>
              <td><pre>{{ $value.Created }}</pre></td>
              <td><pre>{{ $value.Updated }}</pre></td>
            </tr>
          {{- end -}}
        {{- end -}}
      {{- end -}}
    </table>
    <hr>
    {{ if .NextPageToken }}<a href="{{ .DirName }}?pageToken={{ .NextPageToken }}">Next page</a>{{ end }}
  </body>
</html>
`
