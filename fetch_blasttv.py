import requests
import json
from datetime import datetime

BASE_API_LIST = "https://app.blasttv.ph/api/v2/event/live?p=1&rpp=25"
EVENT_API = "https://app.blasttv.ph/api/v4/event/{}?includePlaybackDetails=URL&displayGeoblocked=HIDE"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def fetch_event_ids():
    try:
        r = requests.get(BASE_API_LIST, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        event_ids = [item["id"] for item in data.get("data", [])]
        return event_ids
    except Exception as e:
        print("Error fetching event IDs:", e)
        return []

def fetch_m3u8(event_id):
    try:
        r = requests.get(EVENT_API.format(event_id), headers=HEADERS)
        r.raise_for_status()
        data = r.json()

        playback = data.get("playbackDetails", {})
        url = playback.get("url") or playback.get("streamUrl")

        return url
    except Exception as e:
        print(f"Error fetching m3u8 for event {event_id}:", e)
        return None

def generate_playlist():
    event_ids = fetch_event_ids()

    lines = ["#EXTM3U", f"# Generated: {datetime.now()}"]

    for eid in event_ids:
        m3u8 = fetch_m3u8(eid)
        if m3u8:
            lines.append(f"#EXTINF:-1 tvg-id=\"{eid}\", BLASTTV Event {eid}")
            lines.append(m3u8)

    with open("playlist.m3u8", "w") as f:
        f.write("\n".join(lines))

    print("playlist.m3u8 updated!")

if __name__ == "__main__":
    generate_playlist()
  
