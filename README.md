# Risk Processor Service

A FastAPI-based backend for ingesting risk indicators, applying domain-specific transformation logic, and exposing results via JSON or CSV endpoints.

---

## 1. Setup Instructions

### Prerequisites
- Docker over linux
- Git

# Review project repo & packages 
repo code (public) - https://github.com/sergkonsta/risk-processor

service docker container (public) - `ghcr.io/sergkonsta/risk-processor:latest`


# Run container
docker run -p 8000:80 ghcr.io/sergkonsta/risk-processor:latest

Open in browser: http://localhost:8000/docs


# 2. API Documentation

### POST /process

Accepts a JSON payload for a single city, returns components + aggregated risk score.

json input example:
```
{
  "city": "Metropolis",
  "crime_index": 5.0,
  "accident_rate": 3.2,
  "socioeconomic_level": 7,
  "weather_condition": "rain"
}
```
Response (200 OK) example:
```
{
  "city": "Metropolis",
  "components": {
    "crime_index": 50.0,
    "accident_rate": 32.0,
    "socioeconomic_level": 66.67,
    "weather_condition": 50.0
  },
  "risk_score": 198.67
}
```
### POST /process-csv
Accepts a CSV upload with columns:

```city,crime_index,accident_rate,socioeconomic_level,weather_condition```

Returns a downloadable CSV with one row per input, enriched by either a risk_score (and original components) or an error.

### Example cURL
curl -X POST http://localhost:8000/process-csv \
  -F "file=@tests/mocks/mock_input.csv;type=text/csv" \
  --output results.csv


# 3. Transformation Logic & Assumptions
### Normalization

Numeric inputs (crime_index, accident_rate on 0–10; socioeconomic_level on 1–10) are linearly mapped to 0–100.

### Weather mapping

Categorical weather_condition (e.g. “sunny”, “rain”, “snow”) has a numeric severity defined and configurable in config/config.yaml and pipelined to risk_processor class constructor ; that severity is normalized to 0–100.

### Conditional logic

If normalized crime > 80 and socioeconomic < 30 → apply a 10% penalty on the crime component.

### Cross-feature logic

If normalized weather > 70 → amplify accident component by 20%.

### Weights & Noise

All component weights and a global noise_level (to simulate real-world variation) live in config/config.yaml.

Noise is applied last as a uniform random offset ±noise_level.

### Validation & Error Handling

All inputs (JSON & CSV) are validated via Pydantic for required fields, types, and ranges.

CSV row errors are returned inline (row-specific error column) without failing the full batch.

# 4. CI/CD
I’ve included a GitHub Actions workflow at .github/workflows/ci.yml:

### build-and-test

Checks out code, installs deps, runs pytest.

### build-and-push-image

Builds Docker image and pushes to ghcr.io/${{ github.repository_owner }}/risk-processor:latest.

# 5. Docker & Local Run
Build: docker build -t risk-processor:latest .

Run: docker run -p 8000:80 risk-processor:latest

Open Swagger UI at http://localhost:8000/docs.