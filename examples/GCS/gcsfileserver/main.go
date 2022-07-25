package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"gcsfileserver/server"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	s := server.Server{
		DirListPageSize: 100,
	}
	http.Handle("/", &s)

	fmt.Println("server running at port ", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
