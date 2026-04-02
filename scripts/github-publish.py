"""
GitHub Actions'da calisan Instagram publish scripti.
Queue.json'dan zamani gelen icerikleri yayinlar.

Cloudinary'ye ONCEDEN yuklenenmis URL'leri kullanir.
Secrets: META_ACCESS_TOKEN, INSTAGRAM_BUSINESS_ID
"""

import os
import sys
import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib import request, parse, error

# ── Config ────────────────────────────────────────────────────────────────────
ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN", "")
IG_ACCOUNT_ID = os.environ.get("INSTAGRAM_BUSINESS_ID", "")
GRAPH_API = "https://graph.facebook.com/v21.0"
QUEUE_FILE = Path(__file__).parent.parent / "content" / "queue.json"
TURKEY_TZ = timezone(timedelta(hours=3))


def graph_api_call(endpoint, params):
    params["access_token"] = ACCESS_TOKEN
    data = parse.urlencode(params).encode()
    url = f"{GRAPH_API}/{endpoint}"
    req = request.Request(url, data=data, method="POST")
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except error.URLError as e:
        body = e.read().decode() if hasattr(e, "read") else str(e)
        print(f"  API Hata: {body}")
        return None


def wait_for_container(container_id, max_wait=120):
    for _ in range(max_wait // 5):
        url = f"{GRAPH_API}/{container_id}?fields=status_code&access_token={ACCESS_TOKEN}"
        try:
            with request.urlopen(request.Request(url), timeout=10) as resp:
                result = json.loads(resp.read().decode())
                status = result.get("status_code")
                if status == "FINISHED":
                    return True
                if status == "ERROR":
                    print(f"  Container hatasi: {result}")
                    return False
        except Exception:
            pass
        time.sleep(5)
    print("  Container zaman asimi")
    return False


def publish_single(image_url, caption):
    print(f"  Post yayinlaniyor...")
    result = graph_api_call(f"{IG_ACCOUNT_ID}/media", {
        "image_url": image_url,
        "caption": caption,
    })
    if not result or "id" not in result:
        return None
    container_id = result["id"]
    if not wait_for_container(container_id):
        return None
    pub = graph_api_call(f"{IG_ACCOUNT_ID}/media_publish", {"creation_id": container_id})
    if pub and "id" in pub:
        return pub["id"]
    return None


def publish_carousel(image_urls, caption):
    print(f"  Carousel yayinlaniyor ({len(image_urls)} gorsel)...")
    child_ids = []
    for i, url in enumerate(image_urls):
        result = graph_api_call(f"{IG_ACCOUNT_ID}/media", {
            "image_url": url,
            "is_carousel_item": "true",
        })
        if result and "id" in result:
            child_ids.append(result["id"])
            print(f"    Child {i+1}: OK")
        else:
            print(f"    Child {i+1}: FAIL")
            return None
        time.sleep(2)

    time.sleep(10)

    result = graph_api_call(f"{IG_ACCOUNT_ID}/media", {
        "media_type": "CAROUSEL",
        "caption": caption,
        "children": ",".join(child_ids),
    })
    if not result or "id" not in result:
        return None

    carousel_id = result["id"]
    if not wait_for_container(carousel_id):
        return None

    pub = graph_api_call(f"{IG_ACCOUNT_ID}/media_publish", {"creation_id": carousel_id})
    if pub and "id" in pub:
        return pub["id"]
    return None


def publish_reels(video_url, caption, cover_url=None):
    print(f"  Reels yayinlaniyor...")
    params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
    }
    if cover_url:
        params["cover_url"] = cover_url

    result = graph_api_call(f"{IG_ACCOUNT_ID}/media", params)
    if not result or "id" not in result:
        return None

    container_id = result["id"]
    if not wait_for_container(container_id, max_wait=300):
        return None

    pub = graph_api_call(f"{IG_ACCOUNT_ID}/media_publish", {"creation_id": container_id})
    if pub and "id" in pub:
        return pub["id"]
    return None


def main():
    if not ACCESS_TOKEN or not IG_ACCOUNT_ID:
        print("HATA: META_ACCESS_TOKEN veya INSTAGRAM_BUSINESS_ID eksik!")
        sys.exit(1)

    if not QUEUE_FILE.exists():
        print("Queue dosyasi yok, cikiliyor.")
        return

    queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    now_turkey = datetime.now(TURKEY_TZ)
    print(f"Turkiye saati: {now_turkey.strftime('%Y-%m-%d %H:%M')}")

    changed = False
    for entry in queue:
        if entry.get("status") != "pending":
            continue

        scheduled = datetime.strptime(entry["datetime"], "%Y-%m-%d %H:%M")
        scheduled = scheduled.replace(tzinfo=TURKEY_TZ)

        if now_turkey < scheduled:
            print(f"  Henuz zamani gelmedi: {entry['name']} ({entry['datetime']})")
            continue

        print(f"\n{'='*50}")
        print(f"  YAYINLANIYOR: {entry['name']}")
        print(f"  Tip: {entry['type']}, Zamanlanmis: {entry['datetime']}")
        print(f"{'='*50}")

        media_id = None
        post_type = entry["type"]
        caption = entry["caption"]
        urls = entry["urls"]

        if post_type == "carousel":
            media_id = publish_carousel(urls, caption)
        elif post_type == "post":
            media_id = publish_single(urls[0], caption)
        elif post_type == "reels":
            video_urls = [u for u in urls if any(u.endswith(e) for e in [".mp4", ".mov"])]
            cover_urls = [u for u in urls if not any(u.endswith(e) for e in [".mp4", ".mov"])]
            if video_urls:
                media_id = publish_reels(video_urls[0], caption, cover_urls[0] if cover_urls else None)

        if media_id:
            entry["status"] = "published"
            entry["media_id"] = media_id
            entry["published_at"] = now_turkey.strftime("%Y-%m-%d %H:%M")
            print(f"  BASARILI! Media ID: {media_id}")
            changed = True
        else:
            entry["status"] = "failed"
            entry["failed_at"] = now_turkey.strftime("%Y-%m-%d %H:%M")
            print(f"  BASARISIZ!")
            changed = True

    if changed:
        QUEUE_FILE.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")
        print("\nQueue guncellendi.")
    else:
        print("\nYayinlanacak icerik yok.")


if __name__ == "__main__":
    main()
