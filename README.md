Time7 Gateway – Authentication API

Phase 1: Mock Verification Flow

This project provides a lightweight gateway API for verifying RFID EPC tags.
Phase 1 implements a mock verification logic (no real Impinj reader connection yet).

The purpose of Phase 1 is to allow frontend/mobile clients to start integration and testing early.

Features (Phase 1)

FastAPI-based lightweight gateway server
	•	/api/verify endpoint that accepts EPC scanning events
	•	Mock verification logic:
	•	EPC starting with “3034” → authentic
	•	All others → mismatch
	•	Standardized response format
	•	Includes schemas, enums, services and client modules
	•	Ready for extension to real Impinj Reader & Octane SDK in Phase 2


  time7_gateway/
│
├── api/
│   ├── verify.py        # /api/verify verification endpoint
│   └── admin.py         # admin utilities (health check etc.)
│
├── models/
│   ├── schemas.py       # Request & response models
│   ├── enums.py         # AuthResult enum
│   └── __init__.py
│
├── services/
│   ├── auth_service.py  # Core mock verification logic
│   └── __init__.py
│
├── clients/
│   ├── impinj_mock.py   # Mock client for Impinj verification
│   └── __init__.py
│
├── storage/
│   └── __init__.py      # Future logging/storage modules
│
└── main.py              # FastAPI application entrypoint

API Endpoints

Request (JSON)
{
  "epc": "303400000000000000000001",
  "token": "optional-string",
  "reader_id": "reader-001",
  "timestamp": "2025-01-29T08:00:00Z"
}

Response (example)
{
  "epc": "303400000000000000000001",
  "result": "authentic",
  "message": "OK",
  "reader_id": "reader-001",
  "timestamp": "2025-01-29T08:00:00Z",
  "impinj_raw": null
}

Mock Verification Logic (Phase 1)

if epc.startswith("3034"):
    return AuthResult.AUTHENTIC
else:
    return AuthResult.MISMATCH
  This lets frontend/mobile apps test the workflow without connecting to real Impinj readers.

  


    


