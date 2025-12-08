import requests
import json

LOGIN_URL = "https://app.blasttv.ph/api/v2/login"
LIVE_URL  = "https://app.blasttv.ph/api/v2/event/live?rpp=10"

EMAIL = "candadofrances@gmail.com"
PASSWORD = "Lmatt0603!"


def get_token():
    payload = {
        "id": EMAIL,
        "secret": PASSWORD
    }

    headers = {
        "content-type": "application/json",
        "origin": "https://app.blasttv.ph",
        "referer": "https://app.blasttv.ph/"
    }

    res = requests.post(LOGIN_URL, json=payload, headers=headers)

    print("LOGIN RESPONSE:", res.text)  # Debug

    if res.status_code != 200:
        print("Login failed:", res.text)
        return None

    data = res.json()
    return data.get("access_token") or data.get("data", {}).get("access_token")


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

    print("\nTOKEN ACQUIRED:", token, "\n")

    events_json = fetch_live_streams(token)
    print(json.dumps(events_json, indent=4))

    # Try extract stream url
    for event in events_json.get("data", []):
        print("\nEvent:", event.get("title"))
        if "url" in event:
            print("Stream URL:", event["url"])
        elif "stream_url" in event:
            print("Stream URL:", event["stream_url"])
        else:
            print("No stream URL found yet")


if __name__ == "__main__":
    main()
