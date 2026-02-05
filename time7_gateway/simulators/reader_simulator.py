import argparse
import sys
import select
import httpx


def parse_ids(s: str) -> list[str]:
    parts = s.replace(",", " ").split()
    return [p.strip() for p in parts if p.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()

    endpoint = f"{args.base_url.rstrip('/')}/reader/events"
    print("POSTING TO:", endpoint)
    active_ids: list[str] = []

    print('Type IDs and press Enter. Empty line clears. Type "q" to quit.')

    with httpx.Client(timeout=5.0) as client:
        while True:
            ready, _, _ = select.select([sys.stdin], [], [], args.interval)

            if ready:
                line = sys.stdin.readline()
                if not line:
                    break
                line = line.strip()

                if line.lower() in ("q", "quit", "exit"):
                    break

                if line == "":
                    active_ids = []
                    continue

                active_ids = parse_ids(line)
                continue

            if not active_ids:
                continue

            payload = {"tagIds": active_ids}
            r = client.post(endpoint, json=payload)
            if r.status_code >= 400:
                print("ERROR", r.status_code, r.text)


if __name__ == "__main__":
    main()