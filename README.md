# 🎓 Smart Campus Service Finder

> AI-powered semantic search and location-aware campus service discovery platform built with Django, Django REST Framework, PostgreSQL, PostGIS, pgvector, and BGE-M3.

Smart Campus Service Finder helps students and visitors find relevant places and facilities across a university campus using **natural-language queries**.

Instead of searching with exact keywords such as `library` or `canteen`, users can ask questions like:

> "Where can I find a quiet place to study for my exams?"

The system understands the intent of the query, generates a semantic embedding, searches the campus database using vector similarity, considers the user's geographical location, and returns the most relevant places.

---

## ✨ Features

- 🔎 **Natural Language Search**
  - Search campus facilities using normal human language.
  - No need to know the exact name of a place.

- 🧠 **Semantic Search**
  - Uses **BGE-M3** embeddings to understand the meaning of queries.
  - Powered by **pgvector** for vector similarity search.

- 📍 **Location-Aware Search**
  - Uses the user's latitude and longitude.
  - Calculates geographical distance using **PostGIS**.

- 🤖 **AI Search Intent Classification**
  - Uses an LLM to identify the category of a user's query.
  - Categories include:
    - Academic
    - Administration
    - Culture
    - Environment
    - Food
    - Health
    - Hostel
    - Laboratory
    - Library
    - Parking
    - Research
    - Security
    - Sports
    - Student Services
    - Technology
    - Utilities

- ⚡ **Hybrid Ranking**
  - Combines semantic relevance and geographical proximity.
  - Produces a final ranking for search results.

- 🗺️ **PostGIS Spatial Queries**
  - Stores campus locations as geographic points.
  - Supports distance-based searches.

- 🔐 **Admin-only Place Management**
  - Authorized administrators can add, update, and delete campus places.

- 🧩 **RESTful API**
  - Built using Django REST Framework.

---

# 🏗️ System Architecture

```text
                    User
                      │
                      │ Natural Language Query
                      ▼
              ┌─────────────────┐
              │   Search API    │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ Intent Classifier│
              │      (LLM)      │
              └────────┬────────┘
                       │
                 Search Category
                       │
                       ▼
              ┌─────────────────┐
              │  BGE-M3 Model   │
              │   Embeddings    │
              └────────┬────────┘
                       │
                 Query Vector
                       │
                       ▼
              ┌─────────────────┐
              │    pgvector     │
              │ Semantic Search │
              └────────┬────────┘
                       │
                 Top Candidates
                       │
                       ▼
              ┌─────────────────┐
              │     PostGIS     │
              │ Distance Search │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Hybrid Ranking  │
              │ Semantic + Geo  │
              └────────┬────────┘
                       │
                       ▼
                  Top Results