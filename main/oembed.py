import requests

TIKTOK_OEMBED_URL = "https://www.tiktok.com/oembed"


def fetch_tiktok_thumbnail(post_url, timeout=5):
    """Return the thumbnail URL for a TikTok post, or None if unavailable."""
    if not post_url:
        return None
    try:
        response = requests.get(
            TIKTOK_OEMBED_URL, params={"url": post_url}, timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None
    return data.get("thumbnail_url") or None
