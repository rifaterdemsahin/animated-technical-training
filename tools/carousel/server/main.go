// Command server is the DeliveryPilot carousel review app backend
// (MASTER_SPEC.md section 5): a small HTTP API in front of MongoDB that the
// static frontend in ./static talks to. Scene data round-trips as
// {"topic": ..., "scenes": [...]} exactly matching scripts/<topic>.json.
package main

import (
	"context"
	"crypto/subtle"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

func env(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func main() {
	cmd := "serve"
	if len(os.Args) > 1 {
		cmd = os.Args[1]
	}

	mongoURI := os.Getenv("MONGODB_URI")
	if mongoURI == "" {
		log.Fatal("MONGODB_URI is required")
	}
	dbName := env("MONGODB_DB", "animated_technical_training")

	ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
	defer cancel()
	store, err := NewStore(ctx, mongoURI, dbName)
	if err != nil {
		log.Fatalf("mongo connect failed: %v", err)
	}
	defer store.Close(context.Background())

	switch cmd {
	case "seed":
		scriptsDir := env("SCRIPTS_DIR", "../../../scripts")
		if err := SeedFromDir(ctx, store, scriptsDir); err != nil {
			log.Fatalf("seed failed: %v", err)
		}
	case "serve":
		serve(store)
	default:
		log.Fatalf("unknown command %q (expected 'serve' or 'seed')", cmd)
	}
}

func serve(store *Store) {
	staticDir := env("STATIC_DIR", "static")
	spritesDir := env("SPRITES_DIR", "../../../sprites")
	appPassword := os.Getenv("APP_PASSWORD")
	port := env("PORT", "8080")

	mux := http.NewServeMux()

	mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		http.ServeFile(w, r, filepath.Join(staticDir, "index.html"))
	})
	mux.HandleFunc("GET /app.js", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, filepath.Join(staticDir, "app.js"))
	})
	mux.HandleFunc("GET /styles.css", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, filepath.Join(staticDir, "styles.css"))
	})

	mux.HandleFunc("GET /api/topics", func(w http.ResponseWriter, r *http.Request) {
		topics, err := store.ListTopics(r.Context())
		if err != nil {
			writeJSONError(w, http.StatusInternalServerError, err)
			return
		}
		if topics == nil {
			topics = []string{}
		}
		writeJSON(w, http.StatusOK, topics)
	})

	mux.HandleFunc("GET /api/manifest", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, filepath.Join(spritesDir, "manifest.json"))
	})

	mux.HandleFunc("GET /api/topics/{topic}", func(w http.ResponseWriter, r *http.Request) {
		topic := r.PathValue("topic")
		doc, err := store.GetTopic(r.Context(), topic)
		if err != nil {
			writeJSONError(w, http.StatusInternalServerError, err)
			return
		}
		if doc == nil {
			writeJSONError(w, http.StatusNotFound, fmt.Errorf("unknown topic %q", topic))
			return
		}
		writeJSON(w, http.StatusOK, doc)
	})

	mux.HandleFunc("POST /api/topics/{topic}", func(w http.ResponseWriter, r *http.Request) {
		topic := r.PathValue("topic")
		var doc TopicDoc
		if err := json.NewDecoder(r.Body).Decode(&doc); err != nil {
			writeJSONError(w, http.StatusBadRequest, fmt.Errorf("invalid JSON: %w", err))
			return
		}
		if doc.Scenes == nil {
			writeJSONError(w, http.StatusBadRequest, errors.New("body must be {topic, scenes: [...]}"))
			return
		}
		doc.Topic = topic
		if err := store.PutTopic(r.Context(), doc); err != nil {
			writeJSONError(w, http.StatusInternalServerError, err)
			return
		}
		writeJSON(w, http.StatusOK, map[string]any{
			"status": "saved", "topic": topic, "scene_count": len(doc.Scenes),
		})
	})

	spritesFS := http.StripPrefix("/sprites/", http.FileServer(http.Dir(spritesDir)))
	mux.Handle("GET /sprites/", spritesFS)

	var handler http.Handler = mux
	if appPassword != "" {
		handler = basicAuth(handler, appPassword)
		log.Printf("basic auth enabled (APP_PASSWORD set)")
	} else {
		log.Printf("WARNING: APP_PASSWORD not set — server has no auth")
	}

	addr := ":" + port
	log.Printf("carousel server listening on %s (db=%s, static=%s, sprites=%s)",
		addr, env("MONGODB_DB", "animated_technical_training"), staticDir, spritesDir)
	log.Fatal(http.ListenAndServe(addr, handler))
}

func basicAuth(next http.Handler, password string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, pass, ok := r.BasicAuth()
		if !ok || subtle.ConstantTimeCompare([]byte(pass), []byte(password)) != 1 {
			w.Header().Set("WWW-Authenticate", `Basic realm="carousel"`)
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func writeJSONError(w http.ResponseWriter, status int, err error) {
	writeJSON(w, status, map[string]string{"error": err.Error()})
}
