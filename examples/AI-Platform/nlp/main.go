// Sample language-quickstart uses the Google Cloud Natural API to analyze the
// sentiment of "Hello, world!".
package main

import (
	"context"
	"flag"
	"fmt"
	"log"

	language "cloud.google.com/go/language/apiv1"
	languagepb "google.golang.org/genproto/googleapis/cloud/language/v1"
)

func main() {
	textPtr := flag.String("text", "Hello world", "a sentence")
	flag.Parse()

	ctx := context.Background()

	// Creates a client.
	client, err := language.NewClient(ctx)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}
	defer client.Close()

	// Sets the text to analyze.
	text := *textPtr
	fmt.Println("text: ", text)

	// Detects the sentiment of the text.
	sentiment, err := client.AnalyzeSentiment(ctx, &languagepb.AnalyzeSentimentRequest{
		Document: &languagepb.Document{
			Source: &languagepb.Document_Content{
				Content: text,
			},
			Type: languagepb.Document_PLAIN_TEXT,
		},
		EncodingType: languagepb.EncodingType_UTF8,
	})
	if err != nil {
		log.Fatalf("Failed to analyze text: %v", err)
	}

	fmt.Printf("Text: %v Score: %v\n", text, sentiment.DocumentSentiment.Score)
	if sentiment.DocumentSentiment.Score >= 0 {
		fmt.Println("Sentiment: positive")
	} else {
		fmt.Println("Sentiment: negative")
	}
}
