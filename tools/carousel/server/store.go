package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

// TopicDoc mirrors the scripts/<topic>.json shape exactly: {"topic": ..., "scenes": [...]}.
// Scenes are kept as untyped maps so the store never has to know the full scene
// schema (see MASTER_SPEC.md section 4.1) — it round-trips whatever JSON it's given.
type TopicDoc struct {
	Topic  string                   `bson:"_id" json:"topic"`
	Scenes []map[string]interface{} `bson:"scenes" json:"scenes"`
}

type Store struct {
	client *mongo.Client
	coll   *mongo.Collection
}

func NewStore(ctx context.Context, uri, dbName string) (*Store, error) {
	client, err := mongo.Connect(options.Client().ApplyURI(uri))
	if err != nil {
		return nil, fmt.Errorf("connect: %w", err)
	}
	if err := client.Ping(ctx, nil); err != nil {
		return nil, fmt.Errorf("ping: %w", err)
	}
	coll := client.Database(dbName).Collection("topics")
	return &Store{client: client, coll: coll}, nil
}

func (s *Store) Close(ctx context.Context) error {
	return s.client.Disconnect(ctx)
}

func (s *Store) ListTopics(ctx context.Context) ([]string, error) {
	cursor, err := s.coll.Find(ctx, bson.M{}, options.Find().SetProjection(bson.M{"_id": 1}))
	if err != nil {
		return nil, err
	}
	defer cursor.Close(ctx)

	var topics []string
	for cursor.Next(ctx) {
		var doc struct {
			ID string `bson:"_id"`
		}
		if err := cursor.Decode(&doc); err != nil {
			return nil, err
		}
		topics = append(topics, doc.ID)
	}
	return topics, cursor.Err()
}

func (s *Store) GetTopic(ctx context.Context, topic string) (*TopicDoc, error) {
	var doc TopicDoc
	err := s.coll.FindOne(ctx, bson.M{"_id": topic}).Decode(&doc)
	if err == mongo.ErrNoDocuments {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &doc, nil
}

func (s *Store) PutTopic(ctx context.Context, doc TopicDoc) error {
	_, err := s.coll.ReplaceOne(ctx, bson.M{"_id": doc.Topic}, doc, options.Replace().SetUpsert(true))
	return err
}

// SeedFromDir loads scripts/*.json into Mongo, skipping any topic that already
// has a document so it never clobbers edits made through the app.
func SeedFromDir(ctx context.Context, s *Store, scriptsDir string) error {
	entries, err := filepath.Glob(filepath.Join(scriptsDir, "*.json"))
	if err != nil {
		return err
	}
	for _, path := range entries {
		raw, err := os.ReadFile(path)
		if err != nil {
			return fmt.Errorf("read %s: %w", path, err)
		}
		var doc TopicDoc
		if err := json.Unmarshal(raw, &doc); err != nil {
			return fmt.Errorf("parse %s: %w", path, err)
		}
		if doc.Topic == "" {
			doc.Topic = filepath.Base(path[:len(path)-len(filepath.Ext(path))])
		}

		existing, err := s.GetTopic(ctx, doc.Topic)
		if err != nil {
			return fmt.Errorf("check existing %s: %w", doc.Topic, err)
		}
		if existing != nil {
			fmt.Printf("skip %s: already present in Mongo (%d scenes)\n", doc.Topic, len(existing.Scenes))
			continue
		}

		if err := s.PutTopic(ctx, doc); err != nil {
			return fmt.Errorf("seed %s: %w", doc.Topic, err)
		}
		fmt.Printf("seeded %s (%d scenes)\n", doc.Topic, len(doc.Scenes))
	}
	return nil
}
