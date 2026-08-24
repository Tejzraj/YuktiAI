# YuktiAi Core Festival APIs (Tezraj - Database & Core APIs)

Base URL: `http://localhost:8000`

### Endpoints Reference

1. **Get All Festivals (With Multi-Param Filters)**
   - **Method:** `GET`
   - **Path:** `/festivals`
   - **Query Params:** 
     - `district` (optional, string) - e.g. `Mysuru`, `Vijayanagara`
     - `category` (optional, string) - e.g. `Folk Sports & Agrarian Heritage`
     - `date` (optional, string) - `YYYY-MM-DD` (e.g. `2026-10-15`)
   - **Response:** `{"count": int, "data": [...]}`

2. **Get Single Festival Detail**
   - **Method:** `GET`
   - **Path:** `/festivals/{festival_id}`
   - **Example:** `/festivals/1`
   - **Response:** Full festival record including embedded `images`, `hotels`, and `travel_options`.

---
*For full team matrix and consumption guides for Monika, Janvi, Tanishi, Nandish, and Simran, see [`TEAM_ROLES.md`](TEAM_ROLES.md).*