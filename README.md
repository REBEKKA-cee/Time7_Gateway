Time7 Authentication Gateway (Mock Impinj IAS Stack

This project implements a lightweight RFID authentication system, simulating the full Impinj Reader → Gateway → IAS verification flow using local mock services.

It allows local end-to-end development without requiring any physical Impinj Reader or IAS backend.

End-to-End Architecture

Mock Reader → Time7 Gateway → Mock IAS → Time7 Gateway → Client

Mock Reader
	•	Simulates Impinj Reader JSON payloads
	•	Sends EPC scan events to Gateway /api/verify

Time7 Gateway
	•	Accepts scan events
	•	Calls Mock IAS
	•	Returns mapped authentication results
	
Mock IAS
	•	Behaves like Impinj Authentication Service (IAS)
	•	Returns: authentic / tampered / mismatch / unknown
 1. Project Structure

Time7_Gateway/
│
├── mock_reader.py          # Mock Impinj Reader (sends ReaderEvent JSON)
├── mock_ias.py             # Mock IAS service
│
├── time7_gateway/
│   ├── api/
│   │   └── verify.py       # Main API routing
│   ├── clients/
│   │   └── ias_client.py   # HTTP client for calling IAS
│   ├── services/
│   │   └── auth_service.py # Business logic behind verification
│   ├── models/
│   └── ...
│
└── README.md               # You are reading this file

2. Mock Reader
Mock Reader simulates Impinj Reader Event JSON:
POST /data/stream

{
 POST /data/stream

{
  "reader_id": "reader-001",
  "tags": [
  
    {
      "epc": "303400000000000000000001",
      "antenna": 1,
      "rssi": -55.5,
      "timestamp": "2025-02-03T10:00:00Z"
    }
  ]
}

Mock Reader forwards each tag to the Gateway:

POST http://127.0.0.1:8000/api/verify

 3. Gateway Verification Flow
Gateway receives a tag and executes:
	1.	Validate request
	2.	Call IASClient.verify_epc()
	3.	Map IAS result into internal model
	4.	Return unified response
Example response:
{
  "epc": "303400000000000000000001",
  "result": "authentic",
  "message": "OK",
  "reader_id": "reader-001",
  "timestamp": "2025-02-03T10:00:00Z",
  "impinj_raw": {
    "result": "authentic",
    "details": {
      "epc": "303400000000000000000001",
      "reader_id": "reader-001",
      "verified_at": "2026-02-03T10:03:11.773253"
    }
  }
}

4. Mock IAS
Mock IAS locally simulates authentication logic:
	•	EPC prefix “3034” → authentic
	•	EPC prefix “9999” → mismatch
	•	Otherwise → tampered

Sample request:
POST http://127.0.0.1:8200/verify

 5. How to Run
Start Gateway (port 8000)
uvicorn time7_gateway.main:app --reload --port 8000
Start Mock IAS (port 8200)
uvicorn mock_ias:app --reload --port 8200
Start Mock Reader (port 8100)
uvicorn mock_reader:app --reload --port 8100

6. Test the Full Flow
curl -X POST http://127.0.0.1:8100/data/stream \
-H "Content-Type: application/json" \
-d '{
  "reader_id": "reader-001",
  "tags": [

    {
      "epc": "303400000000000000000001",
      "antenna": 1,
      "rssi": -55.5,
      "timestamp": "2025-02-03T10:00:00Z"
    }
  ]
}

Expected output:
{
  "sent": 1,
  "results": [
  
    {
      "epc": "303400000000000000000001",
      "result": "authentic",
      "message": "OK",
      ...
    }
  ]
}
This confirms the entire stack is working end-to-end.

7. Future Improvements (Design Notes)
The mock version intentionally simplifies many production features.
Real system should include:

Idempotency
	•	Add composite key: (partner_id, idempotency_key)
	•	Avoid duplicate events

Permission Checks
	•	Validate API client scopes (verify:write, etc.)
Error Handling
	•	Retry with backoff
	•	Circuit breaker for IAS timeout
	•	Return proper 5xx on IAS failure

Partner-Specific Logic
	•	Routing engine
	•	Custom flows per brand

These are left as future iteration tasks.

Summary

This project provides a clean, local, end-to-end mock of Impinj IAS authentication, allowing development and debugging without hardware.

It includes:
	•	Mock Reader
	•	Mock IAS
	•	Gateway
	•	Full verification pipeline
	•	Clean modular structure


