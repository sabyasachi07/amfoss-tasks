package main

import (
	"context"
	"fmt"
	"log"

	"github.com/vartanbeno/go-reddit/v2/reddit"
)

var ctx = context.Background()

func main() {
	if err := run(); err != nil {
		log.Fatal(err)
	}
}

func run() (err error) {
	// Let's get the top 200 posts of r/golang.
	// Reddit returns a maximum of 100 posts at a time,
	// so we'll need to separate this into 2 requests.
	posts, _, err := reddit.DefaultClient().Subreddit.NewPosts(ctx, "memes", &reddit.ListPostOptions{
		ListOptions: reddit.ListOptions{
			Limit: 2,
		},
		Time: "all",
	})
	if err != nil {
		return
	}

	for _, post := range posts {
		fmt.Println(post.FullID)
	}

	// The After option sets the id of an item that Reddit
	// will use as an anchor point for the returned listing

	return
}
