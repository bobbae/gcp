package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", hello)
	mux.HandleFunc("/podinfo", podInfo)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Server listening on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, mux))
}

func hello(w http.ResponseWriter, r *http.Request) {
	log.Printf("Serving request: %s", r.URL.Path)
	host, _ := os.Hostname()
	fmt.Fprintf(w, "Hello, world!\n")
	fmt.Fprintf(w, "Version: 1.0.0\n")
	fmt.Fprintf(w, "Hostname: %s\n", host)
}

func podInfo(w http.ResponseWriter, r *http.Request) {

	log.Printf("podInfo")

	config, err := rest.InClusterConfig()
	if err != nil {
		fmt.Fprintf(w, "Error: %s", err.Error())
	}
	// creates the clientset
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		fmt.Fprintf(w, "Error: %s", err.Error())
	}

	// get pods in all the namespaces by omitting namespace
	// Or specify namespace to get pods in particular namespace
	pods, err := clientset.CoreV1().Pods("").List(context.TODO(), metav1.ListOptions{})
	if err != nil {
		fmt.Fprintf(w, "Error: %s", err.Error())
	}
	fmt.Fprintf(w, "There are %d pods in the cluster\n", len(pods.Items))

	// Examples for error handling:
	// - Use helper functions e.g. errors.IsNotFound()
	// - And/or cast to StatusError and use its properties like e.g. ErrStatus.Message
	_, err = clientset.CoreV1().Pods("default").Get(context.TODO(), "hello-app-XXXX", metav1.GetOptions{})
	if errors.IsNotFound(err) {
		fmt.Fprintf(w, "Pod example-xxxxx not found in default namespace\n")
	} else if statusError, isStatus := err.(*errors.StatusError); isStatus {
		fmt.Fprintf(w, "Error getting pod %v\n", statusError.ErrStatus.Message)
	} else if err != nil {
		panic(err.Error())
	} else {
		fmt.Fprintf(w, "Found example-xxxxx pod in default namespace\n")
	}

	fmt.Fprintf(w, "Hello, world!\n")
	fmt.Fprintf(w, "Version: 1.0.0\n")

	//time.Sleep(10 * time.Second)
}
