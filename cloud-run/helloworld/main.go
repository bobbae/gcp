package main

import (
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"time"
	"context"
	"encoding/json"
	"html/template"

	"github.com/nishanths/go-xkcd"
)

type Xkcd struct {
	Title string `json:"title"`
	URL string `json:"url"`
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

func getXkcd() (Xkcd) {
	client := xkcd.NewClient()
	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)
	comic, err := client.Get(context.Background(), r1.Intn(2421)+1)
	if err != nil {
		log.Fatal(err)
	}
	xkcd := Xkcd {
		Title: comic.Title,
		URL: comic.ImageURL,
	}
	return xkcd
}

func jsonHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type","application/json")
	
	json.NewEncoder(w).Encode(getXkcd())
}

func xkcdHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
	t, err:= template.New("foo").Parse(`{{define "FOO"}}
		<html><head></head><center>
		<body><div id="comic"><img src="{{.URL}}" alt="{{.Title}}" />
		<br><center>{{.Title}}</center></div></body>
		</center>
		</html>
		{{end}}
		`,
	)

	if err != nil {
		log.Fatal(err)
	}
	err = t.ExecuteTemplate(w, "FOO", getXkcd())
}
