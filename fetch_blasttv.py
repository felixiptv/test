import requests
import json

LOGIN_URL = "https://app.blasttv.ph/api/v2/auth/login"
LIVE_URL  = "https://app.blasttv.ph/api/v2/event/live?p=1&rpp=25"

EMAIL = "candadofrances@gmail.com"
PASSWORD = "Lmatt0603!"


def get_token():
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }

    headers = {
        "content-type": "application/json",
        "origin": "https://app.blasttv.ph",
        "referer": "https://app.blasttv.ph/"
    }

    res = requests.post(LOGIN_URL, json=payload, headers=headers)

    if res.status_code != 200:
        print("Login failed:", res.text)
        return None

    data = res.json()
    return data.get("data", {}).get("access_token")


def fetch_live_streams(token):
    headers = {
        "authorization": f"Bearer {token}",
        "origin": "https://app.blasttv.ph",
        "referer": "https://app.blasttv.ph/"
    }

    res = requests.get(LIVE_URL, headers=headers)

    if res.status_code != 200:
        print("Error fetching streams:", res.text)
        return None

    return res.json()


def main():
    token = get_token()
    if not token:
        return

    print("Token acquired!\n")

    events_json = fetch_live_streams(token)
    print(json.dumps(events_json, indent=4))

    # Example: extract stream URL (depends on structure)
    for event in events_json.get("data", []):
        print("\nEvent:", event.get("title"))
        if "stream_url" in event:
            print("Stream:", event["stream_url"])
        elif "url" in event:
            print("URL:", event["url"])
        else:
            print("No stream URL found yet")


if __name__ == "__main__":
    main()
