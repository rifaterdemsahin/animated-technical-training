# syntax=docker/dockerfile:1
FROM golang:1-alpine AS build
WORKDIR /src
COPY tools/carousel/server/go.mod tools/carousel/server/go.sum ./
RUN go mod download
COPY tools/carousel/server/ ./
RUN CGO_ENABLED=0 go build -o /out/carousel-server .

FROM alpine:3.20
RUN adduser -D -u 10001 app
WORKDIR /app
COPY --from=build /out/carousel-server ./carousel-server
COPY tools/carousel/server/static ./static
COPY sprites ./sprites
COPY scripts ./scripts

ENV STATIC_DIR=/app/static
ENV SPRITES_DIR=/app/sprites
ENV SCRIPTS_DIR=/app/scripts
ENV PORT=8080

USER app
EXPOSE 8080
ENTRYPOINT ["./carousel-server"]
CMD ["serve"]
