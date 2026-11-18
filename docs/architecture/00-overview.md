# C2P Architecture Overview

_Stub — will be fleshed out as modules are built._

## High-level pipeline

```
Upload drawing (PDF/image)
        │
        ▼
   Extract data (AI)          ← Module 1
        │
        ▼
Human verifies / edits        ← Module 2
  (AI bot assists)
        │
        ▼
  Select CNC tools             ← Module 3
        │
        ▼
Generate process plan          ← Module 4
  (AI + bot edits)
        │
        ▼
Save versioned plan            ← Module 5
  with source drawing
```

## Services

| Service | Role |
|---|---|
| FastAPI (Python) | REST API + business logic |
| PostgreSQL | Relational data (drawings, plans, users) |
| MongoDB / GridFS | Binary file storage (drawing files, PDFs) |
| Qdrant | Vector store for embedding-based search |
| Gemini API | AI inference (extraction, generation) |
| Next.js | Frontend |
