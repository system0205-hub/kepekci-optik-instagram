"""
Kepekci Optik — Instagram Otomatik Paylasim Scripti
Kullanim:
  python scripts/instagram-publish.py carousel exports/yuz-sekline-gore-gozluk-secimi
  python scripts/instagram-publish.py post exports/cam-markalari-yetkili-satici
  python scripts/instagram-publish.py carousel exports/gozluk-temizlik-7-hata --schedule "2026-03-31 12:00"
"""

import os
import sys
import json
import time
import base64
import glob
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib import request, parse, error

# Windows console UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── .env dosyasini oku ──────────────────────────────────────────────────────
def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        print("HATA: .env dosyasi bulunamadi!")
        sys.exit(1)
    env = {}
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                env[key.strip()] = val.strip()
    return env

ENV = load_env()
ACCESS_TOKEN = ENV.get("META_ACCESS_TOKEN", "")
IG_ACCOUNT_ID = ENV.get("INSTAGRAM_BUSINESS_ID", "")
CLOUD_NAME = ENV.get("CLOUDINARY_CLOUD", "")
CLOUD_KEY = ENV.get("CLOUDINARY_KEY", "")
CLOUD_SECRET = ENV.get("CLOUDINARY_SECRET", "")
GRAPH_API = "https://graph.facebook.com/v21.0"


# ── Cloudinary'ye gorsel yukle (SDK) ────────────────────────────────────────
def upload_to_cloudinary(image_path):
    import cloudinary
    import cloudinary.uploader

    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=CLOUD_KEY,
        api_secret=CLOUD_SECRET,
        secure=True
    )

    # Video mu gorsel mi?
    ext = Path(image_path).suffix.lower()
    res_type = "video" if ext in [".mp4", ".mov", ".avi", ".webm"] else "image"

    try:
        result = cloudinary.uploader.upload(
            image_path,
            folder="kepekci-optik",
            public_id=Path(image_path).stem,
            overwrite=True,
            resource_type=res_type
        )
        url = result.get("secure_url", "")
        if url:
            print(f"  ✓ Yuklendi: {Path(image_path).name} → {url}")
            return url
        else:
            print(f"  ✗ Yukleme basarisiz: {result}")
            return None
    except Exception as e:
        print(f"  ✗ Hata: {e}")
        return None


# ── Meta API cagri yardimcisi ───────────────────────────────────────────────
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
        print(f"  ✗ API Hata: {body}")
        return None


# ── Container durumunu kontrol et ───────────────────────────────────────────
def wait_for_container(container_id, max_wait=60):
    for i in range(max_wait // 5):
        url = f"{GRAPH_API}/{container_id}?fields=status_code&access_token={ACCESS_TOKEN}"
        req = request.Request(url)
        try:
            with request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode())
                status = result.get("status_code")
                if status == "FINISHED":
                    return True
                if status == "ERROR":
                    print(f"  ✗ Container hatasi: {result}")
                    return False
        except Exception:
            pass
        time.sleep(5)
    print("  ✗ Container zaman asimi")
    return False


# ── Reels video paylas ──────────────────────────────────────────────────────
def publish_reels(video_url, caption, cover_url=None):
    print("\n🎬 Reels video paylasiliyor...")
    params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
    }
    if cover_url:
        params["cover_url"] = cover_url

    result = graph_api_call(f"{IG_ACCOUNT_ID}/media", params)
    if not result or "id" not in result:
        print("  ✗ Container olusturulamadi")
        return False

    container_id = result["id"]
    print(f"  ✓ Container: {container_id}")
    print("  ⏳ Video isleniyor (bu biraz zaman alabilir)...")

    # Video isleme daha uzun surebilir
    if not wait_for_container(container_id, max_wait=300):
        return False

    pub = graph_api_call(f"{IG_ACCOUNT_ID}/media_publish", {"creation_id": container_id})
    if pub and "id" in pub:
        print(f"  ✅ REELS YAYINLANDI! Media ID: {pub['id']}")
        return True
    return False


# ── Tek gorsel post paylas ──────────────────────────────────────────────────
def publish_single_post(image_url, caption, schedule_time=None):
    print("\n📸 Tek gorsel post paylasiliyor...")
    params = {
        "image_url": image_url,
        "caption": caption,
    }
    if schedule_time:
        params["published"] = "false"
        params["publish_time"] = str(schedule_time)

    result = graph_api_call(f"{IG_ACCOUNT_ID}/media", params)
    if not result or "id" not in result:
        print("  ✗ Container olusturulamadi")
        return False

    container_id = result["id"]
    print(f"  ✓ Container: {container_id}")

    if not wait_for_container(container_id):
        return False

    if schedule_time:
        print(f"  ✓ ZAMANLI paylasim ayarlandi! Container ID: {container_id}")
        return True

    pub = graph_api_call(f"{IG_ACCOUNT_ID}/media_publish", {"creation_id": container_id})
    if pub and "id" in pub:
        print(f"  ✓ Paylasim basarili! Media ID: {pub['id']}")
        return True
    return False


# ── Carousel paylas ─────────────────────────────────────────────────────────
def publish_carousel(image_urls, caption, schedule_time=None):
    print(f"\n📚 Carousel paylasiliyor ({len(image_urls)} gorsel)...")

    # 1. Her gorsel icin child container olustur
    child_ids = []
    for i, url in enumerate(image_urls):
        print(f"  [{i+1}/{len(image_urls)}] Child container olusturuluyor...")
        result = graph_api_call(f"{IG_ACCOUNT_ID}/media", {
            "image_url": url,
            "is_carousel_item": "true",
        })
        if result and "id" in result:
            child_ids.append(result["id"])
            print(f"  ✓ Child {i+1}: {result['id']}")
        else:
            print(f"  ✗ Child {i+1} basarisiz!")
            return False
        time.sleep(2)

    # Child container'larin hazir olmasini bekle
    print("  ⏳ Container'lar hazirlaniyor...")
    time.sleep(10)

    # 2. Parent carousel container
    params = {
        "media_type": "CAROUSEL",
        "caption": caption,
        "children": ",".join(child_ids),
    }
    if schedule_time:
        params["published"] = "false"
        params["publish_time"] = str(schedule_time)

    result = graph_api_call(f"{IG_ACCOUNT_ID}/media", params)
    if not result or "id" not in result:
        print("  ✗ Carousel container olusturulamadi")
        return False

    carousel_id = result["id"]
    print(f"  ✓ Carousel container: {carousel_id}")

    if not wait_for_container(carousel_id):
        return False

    # 3. Zamanli ise yayinlama, otomatik yayinlanacak
    if schedule_time:
        print(f"\n  ✅ ZAMANLI CAROUSEL AYARLANDI! Container ID: {carousel_id}")
        return True

    # 3b. Hemen yayinla
    pub = graph_api_call(f"{IG_ACCOUNT_ID}/media_publish", {"creation_id": carousel_id})
    if pub and "id" in pub:
        print(f"\n  ✅ CAROUSEL PAYLASILDI! Media ID: {pub['id']}")
        return True
    return False


# ── Caption oku (once .txt, sonra ACIKLAMA.md) ─────────────────────────────
def read_caption_from_folder(folder_path):
    folder = Path(folder_path)

    # 1. Oncelik: instagram-aciklama.txt
    txt_file = folder / "instagram-aciklama.txt"
    if txt_file.exists():
        caption = txt_file.read_text(encoding="utf-8").strip()
        if caption:
            print(f"  ✓ Caption: instagram-aciklama.txt ({len(caption)} karakter)")
            return caption

    # 2. ACIKLAMA.md icinden "Instagram Aciklama Metni" bolumu
    aciklama = folder / "ACIKLAMA.md"
    if aciklama.exists():
        content = aciklama.read_text(encoding="utf-8")
        caption = ""
        in_caption = False
        for line in content.split("\n"):
            if "Instagram Açıklama Metni" in line or "Instagram Aciklama Metni" in line:
                in_caption = True
                continue
            if in_caption:
                if line.startswith("## ") and "Hashtag" not in line:
                    break
                if line.startswith("## Hashtag"):
                    break
                caption += line + "\n"
        caption = caption.strip()
        if caption:
            print(f"  ✓ Caption: ACIKLAMA.md ({len(caption)} karakter)")
            return caption

    print("  ✗ HATA: Caption bulunamadi! Paylasim iptal.")
    sys.exit(1)


# ── Klasorden gorselleri bul (sirali) ───────────────────────────────────────
def find_images(folder_path):
    folder = Path(folder_path)
    images = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.mp4", "*.mov"]:
        images.extend(folder.glob(ext))

    # ACIKLAMA.md ve diger dosyalari filtrele
    images = [img for img in images if img.suffix.lower() in [".png", ".jpg", ".jpeg", ".mp4", ".mov"]]

    # Sirala (01-xxx, 02-xxx seklinde)
    images.sort(key=lambda x: x.name)
    return images


# ── Ana fonksiyon ───────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 3:
        print("""
Kullanim:
  python scripts/instagram-publish.py carousel <klasor>
  python scripts/instagram-publish.py post <klasor>
  python scripts/instagram-publish.py carousel <klasor> --schedule "2026-03-31 12:00"
  python scripts/instagram-publish.py carousel <klasor> --dry-run

Ornekler:
  python scripts/instagram-publish.py carousel exports/yuz-sekline-gore-gozluk-secimi
  python scripts/instagram-publish.py post exports/cam-markalari-yetkili-satici
  python scripts/instagram-publish.py carousel exports/gozluk-temizlik-7-hata --schedule "2026-03-31 12:00"
        """)
        sys.exit(1)

    post_type = sys.argv[1]  # carousel veya post
    folder = sys.argv[2]
    schedule_str = None
    dry_run = False

    if "--schedule" in sys.argv:
        idx = sys.argv.index("--schedule")
        schedule_str = sys.argv[idx + 1]
    if "--dry-run" in sys.argv:
        dry_run = True

    # Kontroller
    if not ACCESS_TOKEN:
        print("HATA: META_ACCESS_TOKEN .env'de bulunamadi!")
        sys.exit(1)
    if not CLOUD_NAME or not CLOUD_KEY or not CLOUD_SECRET:
        print("HATA: Cloudinary bilgileri .env'de bulunamadi!")
        sys.exit(1)

    # Schedule parametresi varsa uyar (Windows Zamanlayici kullan)
    if schedule_str and not dry_run:
        print("⚠ NOT: --schedule Instagram API'de calismaz.")
        print("  Windows Gorev Zamanlayici kullan: schedule-post.py")
        print("  Bu script simdi HEMEN yayinlayacak.")
        print("")

    # Gorselleri bul
    images = find_images(folder)
    if not images:
        print(f"HATA: {folder} klasorunde gorsel bulunamadi!")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"  Kepekci Optik — Instagram Paylasim")
    print(f"{'='*50}")
    print(f"  Tip: {post_type}")
    print(f"  Klasor: {folder}")
    print(f"  Gorsel sayisi: {len(images)}")
    for img in images:
        print(f"    - {img.name}")

    # Caption oku
    caption = read_caption_from_folder(folder)
    print(f"  Caption: {len(caption)} karakter")

    # Zamanlama
    schedule_ts = None
    if schedule_str:
        turkey_offset = timedelta(hours=3)
        turkey_tz = timezone(turkey_offset)
        dt = datetime.strptime(schedule_str, "%Y-%m-%d %H:%M")
        dt = dt.replace(tzinfo=turkey_tz)
        schedule_ts = int(dt.timestamp())
        print(f"  Zamanli: {schedule_str} (TR saati)")

    if dry_run:
        print(f"\n  🔍 DRY RUN — paylasim yapilmayacak")
        print(f"  Caption onizleme:\n{caption[:200]}...")
        return

    print(f"\n{'='*50}")

    # Gorselleri imgbb'ye yukle
    print("\n📤 Gorseller Cloudinary'ye yukleniyor...")
    image_urls = []
    for img in images:
        url = upload_to_cloudinary(str(img))
        if url:
            image_urls.append(url)
        else:
            print(f"HATA: {img.name} yuklenemedi, iptal!")
            sys.exit(1)
        time.sleep(2)

    print(f"\n  ✓ {len(image_urls)} gorsel yuklendi")

    # Paylas
    if post_type == "carousel":
        if len(image_urls) < 2:
            print("HATA: Carousel icin en az 2 gorsel gerekli!")
            sys.exit(1)
        success = publish_carousel(image_urls, caption, schedule_ts)
    elif post_type == "post":
        success = publish_single_post(image_urls[0], caption, schedule_ts)
    elif post_type == "reels":
        # Video URL'sini bul
        video_urls = [u for u in image_urls if any(u.endswith(e) for e in [".mp4", ".mov", ".avi", ".webm"])]
        cover_urls = [u for u in image_urls if not any(u.endswith(e) for e in [".mp4", ".mov", ".avi", ".webm"])]
        if not video_urls:
            print("HATA: Reels icin MP4 video dosyasi gerekli!")
            sys.exit(1)
        cover = cover_urls[0] if cover_urls else None
        success = publish_reels(video_urls[0], caption, cover)
    else:
        print(f"HATA: Bilinmeyen tip: {post_type}")
        sys.exit(1)

    if success:
        print(f"\n{'='*50}")
        print(f"  ✅ BASARILI!")
        print(f"{'='*50}")
    else:
        print(f"\n  ❌ BASARISIZ — loglari kontrol et")


if __name__ == "__main__":
    main()
