from __future__ import annotations

import os
import sys

from dotenv import load_dotenv


from time7_gateway.clients.reader_client import ImpinjReaderClient


def must_get(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v


def main() -> int:
    load_dotenv() 

    reader_base_url = must_get("READER_BASE_URL")
    reader_user = os.getenv("READER_USER", "admin")
    reader_password = must_get("READER_PASSWORD")

    gateway_webhook_url = must_get("GATEWAY_WEBHOOK_URL")

    batch_limit = int(os.getenv("READER_BATCH_LIMIT", "50"))
    linger_ms = int(os.getenv("READER_BATCH_LINGER_MS", "200"))

    client = ImpinjReaderClient(
        base_url=reader_base_url,
        username=reader_user,
        password=reader_password,
    )

    try:
        result = client.set_event_webhook(
            target_url=gateway_webhook_url,
            enabled=True,
            event_batch_limit=batch_limit,
            event_batch_linger_ms=linger_ms,
        )
        print("Webhook configured:")
        print(result)

        try:
            current = client.get_event_webhook()
            print("\nReader webhook config:")
            print(current)
        except Exception as e:
            print(f"\n(Info) Could not fetch current webhook config: {e}")

        return 0
    finally:
        client.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"Failed: {e}")
        sys.exit(1)