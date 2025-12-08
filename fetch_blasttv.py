import requests
import json

# Guest login endpoint
GUEST_LOGIN_URL = "https://app.blasttv.ph/api/v2/login/guest/checkin"
# Live events endpoint
LIVE_URL = "https://app.blasttv.ph/api/v2/event/live?rpp=25"

def get_guest_token():
    """Login as guest and return access token"""
    try:
        res = requests.post(GUEST_LOGIN_URL)
        res.raise_for_status()
    except requests.RequestException as e:
        print("Guest login failed:", e)
        return None

    data = res.json()
    token = data.get("access_token") or data.get("data", {}).get("access_token")
    if not token:
        print("No token found in response:", data)
        return None
    return token

def fetch_live_events(token):
    """Fetch live events using guest token"""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        res = requests.get(LIVE_URL, headers=headers)
        res.raise_for_status()
    except requests.RequestException as e:
        print("Fetching live events failed:", e)
        return None

    return res.json()

def save_playlist(events, filename="playlist.m3u8"):
    """Extract .m3u8 URLs and save to playlist file"""
    lines = ["#EXTM3U"]
    for event in events.get("data", []):
        title = event.get("title", "Unknown")
        stream_url = event.get("url") or event.get("stream_url")
        if stream_url and stream_url.endswith(".m3u8"):
            lines.append(f"#EXTINF:-1,{title}")
            lines.append(stream_url)
    if len(lines) > 1:
        with open(filename, "w") as f:
            f.write("\n".join(lines))
        print(f"Playlist saved to {filename}")
    else:
        print("No .m3u8 streams found to save.")

def main():
    token = get_guest_token()
    if not token:
        return

    print("Guest token acquired:", token)
    events = fetch_live_events(token)
    if not events:
        return

    print(json.dumps(events, indent=4))
    save_playlist(events)

if __name__ == "__main__":
    main()
