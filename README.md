# ContextForge

ContextForge is a Retrieval-Augmented Generation (RAG) knowledge assistant.

Users can upload documents, ask questions, and receive answers grounded in relevant document content. When no relevant document is found, the system clearly returns a general answer instead of pretending it came from the knowledge base.

## Live Demo

- Frontend: https://context-forge-frontend.vercel.app
- Backend API: https://contextforge-6byw.onrender.com
- API documentation: https://contextforge-6byw.onrender.com/docs

## Architecture

```text
React frontend on Vercel
          |
          | HTTP API
          v
FastAPI backend on Render
          |
          +--> Supabase PostgreSQL
          |       |
          |       +--> document metadata
          |       +--> document chunks
          |       +--> pgvector embeddings
          |
          +--> Embedding model
          |
          +--> Gemini/OpenAI language model