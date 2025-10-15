#  Intelligent Claims QA Service

A **Python FastAPI microservice** for extracting and analyzing medical claim sheets from images or PDFs using **Google Gemini Vision API** and LLMs.
It supports **structured JSON extraction** and enables asking questions about uploaded documents.

---

## Features

* Upload **PDF or image** of a medical claim sheet.
* Extract **structured data** including:
  * Patient details
  * Diagnoses
  * Medications
  * Procedures
  * Admission information
  * Total claim amount
* Ask **questions about a specific document** and get concise answers.
* Health check endpoint to verify service status.
* **Memory-Based** storage for extracted documents.

---

## API Endpoints

### 1. **POST /extract**

Upload a PDF or image to extract medical claim data.

**Request** (multipart/form-data):

| Field | Type | Description                              |
| ----- | ---- | ---------------------------------------- |
| file  | file | PDF or image file of medical claim sheet |

**Response** (JSON):

```json
{
  "document_id": "doc_1690000000_0",
  "extracted_data": {
    "patient": { "name": "Miriam Njeri", "age": null },
    "diagnoses": ["Hypertension", "Type 2 Diabetes Mellitus", "Acute Bronchitis"],
    "medications": [
      { "name": "Medication", "dosage": null, "quantity": null }
    ],
    "procedures": ["MRI Scan", "Consultation", "Nursing Care"],
    "admission": { 
      "was_admitted": false, 
      "admission_date": null, 
      "discharge_date": null 
    },
    "total_amount": "22,800.00"
  }
}
```

---

### 2. **POST /ask**

Ask a question about a previously extracted document.

**Request** (JSON):

```json
{
  "document_id": "doc_1690000000_0",
  "question": "How many tablets of paracetamol were prescribed?"
}
```

**Response** (JSON):

```json
{
  "answer": "10 tablets"
}
```

---

### 3. **GET /health**

Check service health.

**Response** (JSON):

```json
{
  "status": "healthy",
  "timestamp": "2025-10-15T12:00:00",
  "documents_stored": 1
}
```

---

### 4. **GET /documents**

List all stored documents (metadata only).

**Response** (JSON):

```json
{
  "count": 1,
  "documents": [
    {
      "document_id": "doc_1690000000_0",
      "filename": "claim.pdf",
      "timestamp": "2025-10-15T12:00:00"
    }
  ]
}
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key (get free key at [ai.google.dev](https://ai.google.dev))

### Setup Steps

1. **Clone the repository**:

```bash
git clone https://github.com/chukjosh/curacel_intelligent_claims_qa_service.git
cd curacel_intelligent_claims_qa_service
```

2. **Create a virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your-google-gemini-api-key
```

---

## Running the Service

Start the FastAPI server:

```bash
python run.py
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

* Service runs on [http://localhost:8000](http://localhost:8000)
* Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
* Alternative docs: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Testing

### Using Swagger UI (Recommended)

1. Navigate to [http://localhost:8000/docs](http://localhost:8000/docs)
2. Click on any endpoint to expand
3. Click "Try it out"
4. Fill in parameters and execute

### Using cURL

**Extract a document:**

```bash
curl -X POST "http://127.0.0.1:8000/extract" \
  -F "file=@claim.pdf"
```

**Ask a question:**

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc_1690000000_0",
    "question": "What is the patient name?"
  }'
```

**Check health:**

```bash
curl http://127.0.0.1:8000/health
```

**List documents:**

```bash
curl http://127.0.0.1:8000/documents
```

### Using Python

```python
import requests

# Extract document
with open("claim.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/extract",
        files={"file": f}
    )
    doc_id = response.json()["document_id"]
    print(f"Document ID: {doc_id}")

# Ask question
response = requests.post(
    "http://localhost:8000/ask",
    json={
        "document_id": doc_id,
        "question": "What medications were prescribed?"
    }
)
print(response.json()["answer"])
```

---

## Requirements

### System Requirements

* Python 3.10+
* Internet connection (for Gemini API)

### Python Dependencies

See `requirements.txt`:

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
python-dotenv==1.0.0
google-generativeai==0.3.2
PyPDF2==3.0.1
Pillow==10.2.0
python-multipart==0.0.6
```

---

## Architecture

### Directory Structure

```
curacel_Intelligent_claims_qa_service/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app initialization
│   ├── config.py                # Configuration and environment variables
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic data models
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py    # Gemini API integration
│   │   ├── document_processor.py     # PDF text extraction
│   │   └── storage_service.py   # Document storage logic
│   │
│   └── api/
│       ├── __init__.py
│       └── routes.py            # API endpoints
│
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore file
└── readme.md                    # Documentation
```

### Technology Stack

- **Framework**: FastAPI (modern, fast, async-capable)
- **OCR/LLM**: Google Gemini Vision API
- **PDF Processing**: PyPDF2
- **Image Processing**: Pillow (PIL)
- **Data Validation**: Pydantic
- **Storage**: File-based JSON (persistent across restarts)

### Design Principles

1. **Modular Architecture**: Separated concerns (utilities, models, endpoints)
2. **Type Safety**: Pydantic models for all data structures
3. **Error Handling**: Comprehensive HTTP exception handling
4. **Persistence**: Auto-save/load documents across restarts
5. **Scalability**: Stateless design, easily extensible to databases

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key for document processing |

### Supported File Types

- **Images**: JPEG (.jpg, .jpeg), PNG (.png), WebP (.webp)
- **Documents**: PDF (.pdf)

### Model Selection

The service automatically tries multiple Gemini models with fallback:

1. `gemini-2.5-pro` (primary)
2. `gemini-2.5-flash` (fallback)

---

## Advanced Usage

### Custom Prompts

To modify extraction behavior, edit the prompts in `answer_question` under the `GeminiService` class:

```python
prompt = """
Analyze this medical claim sheet and extract:
- Custom field 1
- Custom field 2
...
"""
```

### Scaling Considerations

**For Production:**

1. **Replace file storage** with Redis or PostgreSQL:
```python
# Replace memory storage with Redis
import redis
r = redis.Redis(host='localhost', port=6379)
```

2. **Add authentication**:
```python
from fastapi.security import HTTPBearer
security = HTTPBearer()
```

3. **Implement rate limiting**:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

4. **Use async processing** for large documents:
```python
from fastapi import BackgroundTasks
```

---

## Troubleshooting

### Common Issues

**1. "Document with ID not found"**
- **Cause**: Document ID doesn't exist (server was restarted without persistence)
- **Fix**: Check available documents:
```bash
curl http://localhost:8000/documents
```

**2. "Invalid file type"**
- **Cause**: Unsupported file format
- **Fix**: Use JPEG, PNG, WebP, or PDF only

**3. "Failed to parse extracted JSON"**
- **Cause**: Gemini returned malformed JSON
- **Fix**: Check document quality, try a clearer scan

### Getting Help

1. Check server logs for detailed error messages
2. Verify API key: `echo $GEMINI_API_KEY`
3. Test with Swagger UI first before CLI tools

---

## Performance Considerations

### Response Times

- **Extract endpoint**: 3-10 seconds (depends on document complexity)
- **Ask endpoint**: 2-5 seconds (includes built-in 2-second delay)
- **Health/Documents**: <100ms

### API Limits (Gemini Free Tier)

- 60 requests per minute
- 1,500 requests per day
- Consider upgrading for production use

---

## Notes & Recommendations

* Current storage is **memory-based**; for production, migrate to a database (PostgreSQL, MongoDB, or Redis).
* Ensure Gemini API keys are valid and have sufficient quota.
* Prompts for LLM are **strictly JSON-oriented** to ensure structured output.
* Can extend to fallback OCR (Tesseract) if needed for images that LLM fails to parse.
* Handles both PDFs and JPEG/PNG/WebP images.
* Built-in 2-second delay on `/ask` endpoint as per specifications.

---

## License

This project is provided as-is as a Curacel Take-Home Task for educational use.

---

## Contact & Support

For issues, improvements, or questions:
- Open an issue on GitHub
- Check the comprehensive error messages provided by API endpoints
- Review Swagger UI documentation at `/docs`

---

## Sample Medical Claims

Sample medical claim documents for testing can be found at: `/test_files`

---

**Thank You**
