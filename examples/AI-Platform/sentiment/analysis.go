package sentiment

import (
	"context"
	"fmt"

	language "cloud.google.com/go/language/apiv1"
	languagepb "google.golang.org/genproto/googleapis/cloud/language/v1"
)

// RedditPost is the struct of a reddit post pulled from this repos' scraped post
type RedditPost struct {
	Title        string   `json:"title"`
	Score        int      `json:"score"`
	ID           string   `json:"id"`
	URL          string   `json:"url"`
	CommentCount int      `json:"comms_num"`
	CreatedAt    float32  `json:"created"`
	Body         string   `json:"body"`
	Timestamp    float32  `json:"timestamp"` // same as CreatedAt
	Comments     []string `json:"comments"`
	Analysis     Analysis `json:"analysis"`
}

// Analysis hold the results from the sentiment analysis from Google's API
type Analysis struct {
	Score           float32 `json:"score"`
	ParsedSentiment string  `json:"parsedSentiment"`
}

// Posts a wrapper struct around the Hot and Top posts that help parse the scraped Reddit posts in this repo
type Posts struct {
	HotPosts []RedditPost `json:"hot_posts"`
	TopPosts []RedditPost `json:"top_posts"`
}

// PrintAnalysis prints the results of the posts from the Sentiment Analysis api
func PrintAnalysis(posts []RedditPost) {
	for i := 0; i < len(posts); i++ {
		post := posts[i]

		fmt.Printf("post id: \"%s\"\n\ttitle: \"%s\"\n\tbody: \"%s\"\n\tsentiment for post: %s\n\tsentiment score: %f\n",
			post.ID,
			post.Title,
			post.Body,
			post.Analysis.ParsedSentiment,
			post.Analysis.Score,
		)
	}
}

func parseSentiment(score float32) string {
	if score == 0.0 {
		return "mixed"
	} else if score == 0.1 {
		return "neutral"
	} else if score > 0.1 {
		return "positive"
	} else if score < 0.1 && score > 0.0 {
		return "mixed"
	} else if score < 0.0 {
		return "negative"
	} else {
		return "unknown"
	}
}

// PrintSentimentChart prints the sentiment analysis chart
func PrintSentimentChart() {
	fmt.Printf("To interpret the scores:\n\tpositive: > 0.1\n\tnegative: < 0.0\n\tneutral: 0.1\n\tmixed: 0.0 - 0.1\n")
}

// pruneEmptyPosts remove reddit posts where the submitter did not write text in the post
func pruneEmptyPosts(posts []RedditPost) []RedditPost {
	postsWithBodyText := make([]RedditPost, 0)

	for i := 0; i < len(posts); i++ {
		post := posts[i]

		if post.Body == "" {
			continue
		}

		postsWithBodyText = append(postsWithBodyText, post)
	}

	return postsWithBodyText
}

func analyzeSentiment(ctx context.Context, client *language.Client, text string) (*languagepb.AnalyzeSentimentResponse, error) {
	return client.AnalyzeSentiment(ctx, &languagepb.AnalyzeSentimentRequest{
		Document: &languagepb.Document{
			Source: &languagepb.Document_Content{
				Content: text,
			},
			Type: languagepb.Document_PLAIN_TEXT,
		},
	})
}

// analyzePosts send each reddit post's body to Google's api for sentiment analysis
// mutates each post's Analyze.Score property and return the posts and no error
// if an error is present then empty posts and nil
func AnalyzePosts(ctx context.Context, client *language.Client, posts []RedditPost) ([]RedditPost, error) {
	postsWithBodyText := pruneEmptyPosts(posts)

	// Google's limits: 600 requests per minute, 800k per day
	// TODO: limmit the requests to 10 request per second to abide to Google's limit
	for i := 0; i < len(postsWithBodyText); i++ {
		post := postsWithBodyText[i]

		analysis, err := analyzeSentiment(ctx, client, post.Body)

		if err != nil {
			return []RedditPost{}, err
		}

		score := analysis.DocumentSentiment.Score

		// Keep a running total of the sentiment
		posts[i].Analysis.Score += score
		posts[i].Analysis.ParsedSentiment = parseSentiment(post.Analysis.Score)
	}

	return posts, nil
}
