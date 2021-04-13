package main

import (
	"context"
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"math/rand"
	"net/http"
	"os"
	"time"

	"github.com/nishanths/go-xkcd"
)

type Xkcd struct {
	Title string `json:"title"`
	URL   string `json:"url"`
}

func main() {
	log.Print("starting server...")
	http.HandleFunc("/", handler)

	// Determine port for HTTP service.
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
		log.Printf("defaulting to port %s", port)
	}

	http.HandleFunc("/xkcd", xkcdHandler)
	http.HandleFunc("/json", jsonHandler)
	// Start HTTP server.
	log.Printf("listening on port %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}

func handler(w http.ResponseWriter, r *http.Request) {
	name := os.Getenv("NAME")
	if name == "" {
		name = "World"
	}
	fmt.Fprintf(w, "Hello %s!\n", name)
}

func getXkcd() Xkcd {
	client := xkcd.NewClient()
	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)
	comic, err := client.Get(context.Background(), r1.Intn(2421)+1)
	if err != nil {
		log.Fatal(err)
	}
	xkcd := Xkcd{
		Title: comic.Title,
		URL:   comic.ImageURL,
	}
	return xkcd
}

func jsonHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	json.NewEncoder(w).Encode(getXkcd())
}

func xkcdHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	t, err := template.New("foo").Parse(`{{define "FOO"}}
<html><head>
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Patrick+Hand+SC&display=swap" rel="stylesheet">
<style>body { font-family: 'Patrick Hand SC', cursive; font-size: 48px; }
</style></head><body class="text-center">
<div id="container" class="jumbotron">
	<div class="d-grid gap-3">
		<div class="p-2 bg-light border">
			<img src="{{.URL}}" alt="{{.Title}}" />
		</div>
		<div class="p-2 bg-light border">
			{{.Title}}
		</div>
	</div>
</div>
</body></html>{{end}}
`,
	)

	if err != nil {
		log.Fatal(err)
	}
	err = t.ExecuteTemplate(w, "FOO", getXkcd())
}
