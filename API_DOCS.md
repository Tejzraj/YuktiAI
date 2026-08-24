# SanskritiPulse Core Festival APIs (Member 1)

Base URL: `http://localhost:8000`

### Endpoints

1. **Get All Festivals (With Filters)**
   - **Method:** `GET`
   - **Path:** `/festivals`
   - **Params:** 
     - `district` (optional, string) - e.g. `Mysuru`
     - `category` (optional, string) - e.g. `Folk Sports`
     - `date` (optional, string) - `YYYY-MM-DD`
   - **Response:** `{"count": int, "data": [...]}`

2. **Get Single Festival Detail**
   - **Method:** `GET`
   - **Path:** `/festivals/{festival_id}`
   - **Example:** `/festivals/mysuru-dasara`
   - **Response:** Full festival object including image URLs and nearby hotel data.