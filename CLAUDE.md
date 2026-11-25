# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A RAG (retrieval-augmented generation) AI chatbot that answers academic-affairs questions (학사 안내) for Hanyang University ERICA, built on a cloud architecture. User-facing content and documentation are mainly in Korean.

## Current state

The repository is only a scaffold so far. It has no source code, dependency manifests, build tooling, tests or CI yet. The `.gitignore` is the standard GitHub Python template, so the backend is expected to be in Python. Don't make up build, lint or test commands. Once tooling is added (e.g. `pyproject.toml`, `package.json`), update this file with the real commands.

## Intended layout

- `backend/ingest/`: the ingestion pipeline. It loads academic-affairs source documents, then chunks and embeds them and writes them to the retrieval store.
- `backend/query/`: the query path. It retrieves relevant chunks for a user question and generates the answer with an LLM.
- `frontend/`: the chat UI.
- `docs/`: project and architecture documentation.

Ingest and query are separate because they run as separate services or jobs. They share only the retrieval store and its schema (chunk format, metadata, embedding model). A change to that schema on one side must also be made on the other.

## Conventions

- Commit messages follow Conventional Commits (e.g. `chore: ...`, `feat: ...`).
