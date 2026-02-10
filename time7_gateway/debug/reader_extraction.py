import os
import time
import requests

from time7_gateway.debug.config import BASE_URL, REFRESH_SECONDS

URL = f"{BASE_URL}/debug/active-tags"
REFRESH_SECONDS = 0.25


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    while True:
        try:
            r = requests.get(URL, timeout=2)
            r.raise_for_status()
            data = r.json()

            clear_screen()
            items = data.get("items", [])

            print("ActiveTags (PRE-IAS) — debug monitor (refreshes in-place)")
            print(f"Endpoint: {URL}")
            print(f"Count: {data.get('count', len(items))}\n")

            for t in items:
                print(f"- {t.get('id')} | first={t.get('first_seen')} | last={t.get('last_seen')}")

            print("\nCTRL+C to stop.")
            time.sleep(REFRESH_SECONDS)

        except KeyboardInterrupt:
            break
        except Exception as e:
            clear_screen()
            print("ActiveTags (PRE-IAS)")
            print(f"Endpoint: {URL}\n")
            print("Cannot fetch debug endpoint yet.")
            print(f"Error: {e}")
            time.sleep(1.0)


if __name__ == "__main__":
    main()