# YuktiAi - Karnataka Cultural Festivals Data Pipeline

A data engineering asset and dataset generator for **YuktiAi**, capturing cultural heritage festivals across Karnataka with authentic metadata, geographic validation, historical provenance, gastronomic highlights, and AI semantic tags.

---

## 📁 Repository Contents

- [`seed_data.py`](file:///Users/macbookpro/.gemini/antigravity-ide/scratch/yuktiai/seed_data.py): Production-ready Python ETL pipeline with geographic bounding-box validation, schema verification, and export capabilities.
- [`festivals_karnataka.json`](file:///Users/macbookpro/.gemini/antigravity-ide/scratch/yuktiai/festivals_karnataka.json): Curated JSON array of distinct Karnataka festivals.
- [`festivals_karnataka.csv`](file:///Users/macbookpro/.gemini/antigravity-ide/scratch/yuktiai/festivals_karnataka.csv): Tabular dataset formatted for data warehousing and analytics.

---

## 📋 Schema Specification

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `id` | `string` | Unique kebab-case identifier | `"mysuru-dasara"` |
| `name` | `string` | Official English name | `"Mysuru Dasara (Nada Habba)"` |
| `local_name` | `string` | Authentic Kannada script name | `"ಮೈಸೂರು ದಸರಾ (ನಾಡಹಬ್ಬ)"` |
| `district` | `string` | Karnataka administrative district | `"Mysuru"` |
| `city` | `string` | Town, city, or sacred site | `"Mysuru"` |
| `lat` | `float` | Exact latitude (bounded: 11.5°N - 18.6°N) | `12.3051` |
| `lng` | `float` | Exact longitude (bounded: 74.0°E - 78.7°E) | `76.6551` |
| `start_date` | `string` | ISO 8601 date string | `"2026-10-11"` |
| `end_date` | `string` | ISO 8601 date string | `"2026-10-20"` |
| `duration_days` | `integer` | Duration in days | `10` |
| `season` | `string` | Traditional / seasonal timeframe | `"Sharad (Autumn / Navaratri)"` |
| `category` | `string` | Cultural / thematic classification | `"State Festival & Royal Heritage"` |
| `description` | `string` | In-depth contextual narrative | *Full description of rituals and festivities* |
| `cultural_significance` | `string` | Spiritual, mythos, and social role | *Heritage and community impact* |
| `history` | `string` | Historical provenance and royal patronage | *Chronology (Vijayanagara, Wodeyar, Kadamba, etc.)* |
| `attractions` | `array<string>` | Highlights, rituals & performances | `["Jamboo Savari", "Palace 100k Illumination"]` |
| `local_food` | `array<string>` | Authentic regional cuisine & GI delicacies | `["Mysore Pak", "Maddur Vada", "Rasabale"]` |
| `footfall` | `integer` | Estimated total visitors/pilgrims | `1800000` |
| `footfall_formatted` | `string` | Formatted human-readable footfall | `"1.8 Million+"` |
| `images` | `array<object>` | High-resolution image assets & captions | `[{"url": "...", "caption": "...", "is_primary": true}]` |
| `tags` | `array<string>` | Semantic indexing & recommendation tags | `["heritage", "royal", "nada-habba", "mysuru-palace"]` |

---

## 🚀 Execution Instructions

Run the data pipeline to regenerate or validate datasets:

```bash
cd yuktiai

# Generate both JSON and CSV with summary metrics:
python3 seed_data.py --summary

# Custom output paths:
python3 seed_data.py --json-output custom_festivals.json --csv-output custom_festivals.csv
```
