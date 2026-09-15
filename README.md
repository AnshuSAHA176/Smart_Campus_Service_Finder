# 🎓 Smart Campus Service Finder

> AI-powered semantic campus search and intelligent walking navigation platform built with Django, Django REST Framework, PostgreSQL, PostGIS, pgvector, BGE-M3, Redis, and Django Channels.

Smart Campus Service Finder helps students and visitors discover campus facilities using natural-language queries and navigate to selected destinations using graph-based shortest-path routing.

Instead of searching with exact keywords such as `library` or `canteen`, users can ask:

> "Where can I find a quiet place to study for my exams?"

The system understands the query, classifies its intent, generates a semantic embedding, searches the campus database using vector similarity, considers geographical proximity, and returns relevant locations.

After selecting a destination, the navigation system finds the user's nearest graph node and uses **A*** to calculate a shortest walking route. During navigation, **WebSockets** receive live GPS positions and monitor whether the user remains on the planned route.

---

# ✨ Features

## 🔎 Natural Language Search

- Search campus facilities using normal human language.
- No requirement to know the exact name of a location.
- Supports intent-based queries.

Examples:

```text
"Where can I study?"
"Where can I print documents?"
"Where can I get administrative help?"
"Find a place to eat."
```

## 🧠 Semantic Search

- Uses **BGE-M3** for semantic embeddings.
- Uses **pgvector** for vector similarity search.
- Finds relevant locations based on meaning rather than exact keywords.

```text
User Query
     ↓
BGE-M3
     ↓
Embedding Vector
     ↓
pgvector
     ↓
Relevant Campus Places
```

## 🤖 AI Intent Classification

An LLM classifies the user's natural-language query into a campus-service category.

Supported categories include:

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

Example:

```text
"Where can I print my assignment?"
             ↓
       Intent Classification
             ↓
      Student Services /
          Technology
             ↓
        Search Places
```

## 📍 Location-Aware Search

- Accepts the user's latitude and longitude.
- Uses **PostGIS** for spatial operations.
- Calculates geographical proximity.
- Allows search results to consider the user's location.

## ⚡ Hybrid Ranking

Search results combine multiple signals:

```text
Semantic Relevance
        +
Geographical Proximity
        ↓
   Final Ranking
```

This allows the system to return places that are both **semantically relevant and geographically useful**.

---

# 🗺️ Intelligent Campus Navigation

The platform represents the campus walking network as a graph.

```text
GraphNode
   ↓
Campus navigation point / intersection

GraphEdge
   ↓
Walkable connection between nodes

Edge Weight
   ↓
Walking distance
```

The navigation engine uses **A*** to find a shortest walking path.

### Navigation Flow

```text
Select Destination
        ↓
Get Current GPS Location
        ↓
Find Nearest Graph Node
        ↓
Find Destination Node
        ↓
A* Pathfinding
        ↓
Shortest Walking Path
        ↓
Route Geometry
        ↓
Redis Navigation Session
        ↓
Live WebSocket Navigation
```

---

# 🧮 Algorithms & Intelligent Processing

## 🔍 Semantic Similarity Search

BGE-M3 converts user queries and campus-place information into vector embeddings.

```text
Query
 ↓
BGE-M3
 ↓
Vector
 ↓
pgvector Similarity Search
 ↓
Relevant Places
```

## 🤖 Intent Classification

An LLM determines the user's search intent and category.

```text
Natural Language Query
        ↓
       LLM
        ↓
Intent / Category
        ↓
Semantic Search
```

## 📍 Geospatial Distance

PostGIS is used for geographic calculations between users, places, and navigation routes.

```text
User GPS Point
      ↓
    PostGIS
      ↓
Distance Calculation
      ↓
Nearest / Relevant Location
```

## 🧭 A* Shortest Path

A* is used to calculate efficient walking routes through the campus graph.

The algorithm uses:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` = actual cost from the starting node to node `n`
- `h(n)` = estimated cost from node `n` to the destination
- `f(n)` = estimated total cost

Navigation:

```text
Current Location
       ↓
Nearest Graph Node
       ↓
       A*
       ↓
Destination Node
       ↓
Shortest Path
```

## 🗺️ Route Geometry

The A* path is converted into geographic coordinates and represented as a `LineString`.

Example:

```text
Node A
   │
   │
Node B ───── Node C
               │
               │
             Node D
```

The resulting LineString represents the planned walking route.

## 🚶 Point-to-Route Distance

During navigation:

```text
User GPS
   ↓
Point
   ↓
Distance to Route LineString
   ↓
Distance in meters
```

This allows the backend to determine whether the user is following the planned walking route.

## 🚨 Off-Route Detection

The navigation system monitors consecutive GPS updates rather than immediately declaring a user off-route.

Current logic:

```text
≤ 10m
   ↓
ON ROUTE

10m – 20m
   ↓
UNCERTAIN

> 20m
   ↓
MONITOR

Repeated deviation
   ↓
OFF ROUTE
```

The monitoring counter helps reduce false detections caused by temporary GPS inaccuracies.

## 🔄 Automatic Rerouting

Automatic rerouting is the next major navigation stage.

```text
User goes OFF ROUTE
        ↓
Find nearest Graph Node
        ↓
Keep destination
        ↓
Run A*
        ↓
Generate new route
        ↓
Create new LineString
        ↓
Update Redis
        ↓
Send new route through WebSocket
```

---

# 📡 Real-Time Navigation

The system uses **Django Channels and WebSockets** to receive live GPS updates.

```text
Frontend GPS
      │
      │ WebSocket
      ▼
Django Channels
      │
      ▼
Navigation Consumer
      │
      ├── GPS Position
      ├── Active Route
      ├── Route Geometry
      └── Navigation Status
```

Example GPS message:

```json
{
    "latitude": 25.6056847,
    "longitude": 88.1288192
}
```

Example navigation response:

```json
{
    "type": "navigation_status",
    "status": "on_route",
    "message": "You are following the planned route."
}
```

---

# 🔐 WebSocket Authentication

Live navigation connections are protected using JWT authentication.

Example:

```text
/ws/live/?token=<access_token>
```

The custom JWT middleware extracts the token and identifies the authenticated user.

Unauthenticated users are rejected from the live navigation connection.

---

# 💾 Redis Navigation Sessions

Redis stores temporary navigation state.

Example:

```text
navigation_route:<user_id>
```

The session can contain:

- Current route
- Route geometry
- Path nodes
- Destination
- Navigation state
- Off-route monitoring counter

Redis is used for temporary real-time state rather than repeatedly storing live GPS updates in PostgreSQL.

---

# 🗄️ Database Architecture

## PostgreSQL

Primary relational database for:

- Campus locations
- Graph nodes
- Graph edges
- Users
- Application data

## PostGIS

Used for:

- Geographic points
- Spatial queries
- Distance calculations
- Route geometry
- Geographic operations

## pgvector

Used for:

- Semantic embeddings
- Vector similarity search
- AI-powered campus search

## Redis

Used for:

- Navigation sessions
- Temporary navigation state
- Real-time state
- Django Channels infrastructure

---

# 🧩 Technology Stack

### Backend

- Python
- Django
- Django REST Framework

### AI & Search

- BGE-M3
- Sentence Transformers
- LLM Intent Classification
- Semantic Search
- Vector Embeddings
- pgvector

### Geospatial

- PostgreSQL
- PostGIS
- GeoDjango
- Point
- LineString
- Spatial Distance Queries

### Navigation

- Graph Data Structures
- A* Pathfinding
- Shortest Path Algorithms
- Route Geometry
- Off-Route Detection

### Real-Time

- Django Channels
- WebSockets
- Redis

### API Documentation

- drf-spectacular
- OpenAPI
- Swagger

### Infrastructure

- Docker
- PostgreSQL
- Redis
- Git
- GitHub

---

# 🏗️ System Architecture

```text
                         USER
                           │
                           │ Natural Language Query
                           ▼
                  ┌──────────────────┐
                  │    Search API    │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Intent Classifier│
                  │      (LLM)       │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │      BGE-M3      │
                  │    Embedding     │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │     pgvector     │
                  │ Semantic Search  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │     PostGIS      │
                  │ Geographic Rank  │
                  └────────┬─────────┘
                           │
                           ▼
                    SEARCH RESULTS
                           │
                           │ Select Destination
                           ▼
                  ┌──────────────────┐
                  │  Navigation API  │
                  └────────┬─────────┘
                           │
                      Current GPS
                           │
                           ▼
                  ┌──────────────────┐
                  │  Nearest Graph   │
                  │      Node        │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │        A*        │
                  │   Pathfinding    │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Route LineString │
                  └────────┬─────────┘
                           │
                           ▼
                    REDIS SESSION
                           │
                           ▼
                  ┌──────────────────┐
                  │ Django Channels  │
                  │    WebSocket     │
                  └────────┬─────────┘
                           │
                           ▼
                    LIVE NAVIGATION
                           │
                           ▼
                ┌─────────────────────┐
                │  Route Monitoring   │
                └──────────┬──────────┘
                           │
                     Off Route?
                      /                             NO           YES
                    │             │
                    ▼             ▼
                Continue       Reroute
                Navigation        │
                                  ▼
                                  A*
                                  │
                                  ▼
                              New Route
```

---

# 📡 API Overview

## Semantic Search

```http
GET /api/locations/search/
```

Searches campus locations using natural language.

## Location Details

```http
GET /api/locations/<id>/
```

Returns details for a specific campus location.

## Navigation

```http
POST /api/navigation/route/
```

Calculates a walking route between the user's current location and destination.

Example request:

```json
{
    "latitude": 25.6048959,
    "longitude": 88.1283591,
    "destination_latitude": 25.6055989,
    "destination_longitude": 88.129012
}
```

Example response:

```json
{
    "distance": 120.678,
    "path": [
        {
            "node": 90,
            "latitude": 25.6048959,
            "longitude": 88.1283591
        },
        {
            "node": 89,
            "latitude": 25.6049775,
            "longitude": 88.1284009
        }
    ],
    "route_geometry": [
        [88.1283591, 25.6048959],
        [88.1284009, 25.6049775]
    ]
}
```

## Live Navigation

```text
WS /ws/live/
```

Receives live GPS coordinates and returns navigation status.

Example:

```json
{
    "latitude": 25.6056847,
    "longitude": 88.1288192
}
```

---

# 🔄 Navigation Data Flow

```text
POST /navigation/route/
          ↓
      Find Nodes
          ↓
         A*
          ↓
    Route Generated
          ↓
    Route Geometry
          ↓
       Redis
          ↓
      WebSocket
          ↓
      GPS Updates
          ↓
  Point → LineString
          ↓
   Distance Check
          ↓
   Navigation Status
          ↓
      Off Route?
       /           NO        YES
     │          │
     │          ▼
     │       Rerouting
     │          │
     │          ▼
     │          A*
     │          │
     └──────────┘
```

---

# 🚀 Project Status

## Search System

- [x] Natural language search
- [x] AI intent classification
- [x] BGE-M3 embeddings
- [x] pgvector semantic search
- [x] PostGIS location queries
- [x] Hybrid search ranking
- [x] Admin place management
- [x] REST API

## Navigation System

- [x] Campus graph
- [x] Graph nodes
- [x] Graph edges
- [x] A* shortest-path routing
- [x] Current-location input
- [x] Destination input
- [x] Route generation
- [x] Route geometry
- [x] LineString generation
- [x] Redis navigation session
- [x] WebSocket live GPS
- [x] JWT WebSocket authentication
- [x] Basic on-route detection
- [x] Off-route monitoring
- [ ] Production-grade meter-based LineString distance validation
- [ ] Automatic route recalculation
- [ ] Arrival detection
- [ ] Route progress tracking
- [ ] Turn-by-turn navigation instructions

---

# 🛠️ Roadmap

## Navigation

- [ ] Accurate Point-to-LineString distance in meters
- [ ] Automatic route recalculation
- [ ] Arrival detection
- [ ] Route progress percentage
- [ ] Remaining distance
- [ ] Estimated walking time
- [ ] Turn-by-turn walking instructions
- [ ] Alternative routes
- [ ] Accessibility-aware routing
- [ ] Blocked-path support

## Search

- [ ] Search autocomplete
- [ ] Improved ranking
- [ ] Personalized recommendations
- [ ] Nearby service discovery
- [ ] Search history
- [ ] Query suggestions

## Geospatial

- [ ] Campus geofencing
- [ ] Building-level navigation
- [ ] Improved route geometry
- [ ] Spatial index optimization

## Reliability

- [ ] Automated API tests
- [ ] WebSocket tests
- [ ] Navigation simulation tests
- [ ] Rate limiting
- [ ] Production monitoring
- [ ] Structured logging
- [ ] CI/CD

---

# 🎯 Project Goal

The long-term goal is to create an intelligent campus platform combining:

```text
AI
+
Semantic Search
+
Vector Search
+
Geospatial Intelligence
+
Graph Algorithms
+
Real-Time Location
+
Intelligent Navigation
```

into a single system that helps users **discover campus services and navigate to them efficiently**.

---

# 👨‍💻 Developer

**Anshu Saha**

Backend Developer | Python | Django | AI

GitHub:

https://github.com/AnshuSAHA176
