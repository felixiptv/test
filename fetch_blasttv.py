import asyncio
from playwright.async_api import async_playwright
import json

LIVE_URL = "https://app.blasttv.ph/api/v2/event/live?rpp=25"
PLAYLIST_FILE = "playlist.m3u8"

async def main():
    async with async_playwright() as p:
        # Launch headless Chromium
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Visit home page to generate guest token automatically
        await page.goto("https://app.blasttv.ph/home", timeout=60000)

        # Wait for network requests to load
        await page.wait_for_timeout(5000)  # 5 seconds for API requests to finish

        # Intercept /event/live request to get response
        async def handle_response(response):
            if LIVE_URL in response.url:
                try:
                    data = await response.json()
                    await save_playlist(data)
                except Exception as e:
                    print("Failed to get JSON:", e)

        page.on("response", handle_response)

        # Reload page to trigger /event/live
        await page.reload()
        await page.wait_for_timeout(5000)

        await browser.close()

async def save_playlist(events):
    """Extract .m3u8 URLs and save to playlist.m3u8"""
    lines = ["#EXTM3U"]
    for event in events.get("data", []):
        title = event.get("title", "Unknown")
        stream_url = event.get("url") or event.get("stream_url")
        if stream_url and ".m3u8" in stream_url:
            lines.append(f"#EXTINF:-1,{title}")
            lines.append(stream_url)
    if len(lines) > 1:
        with open(PLAYLIST_FILE, "w") as f:
            f.write("\n".join(lines))
        print(f"Playlist saved to {PLAYLIST_FILE}")
    else:
        print("No .m3u8 streams found")

if __name__ == "__main__":
    asyncio.run(main())
