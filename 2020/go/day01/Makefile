.DEFAULT_GOAL := build

fmt:
	goimports -l -w .
.PHONY:fmt

lint: fmt
	golint ./...
.PHONY:lint

vet: fmt
	go vet ./...
	shadow ./...
.PHONY:vet

build: vet
	go build
.PHONY:build
