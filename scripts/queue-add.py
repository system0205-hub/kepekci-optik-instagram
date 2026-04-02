"""
Queue'ya icerik ekle. Gorselleri Cloudinary'ye yukler, URL'leri queue.json'a yazar.

Kullanim:
  python scripts/queue-add.py carousel exports/yuz-sekline-gore-gozluk-secimi "2026-04-03 20:00"
  python scripts/queue-add.py post exports/cam-markalari-yetkili-satici "2026-04-04 12:00"
  python scripts/queue-add.py reels exports/mavi-isik-ekran-suresi-reels "2026-04-05 20:00"
  python scripts/queue-add.py list
"""

import os
import sys
import json
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_DIR = Path(__file__).parent.parent
QUEUE_FILE = PROJECT_DIR / "content" / "queue.json"


def load_env():
    env_path = PROJECT_DIR / ".env"
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


def upload_to_cloudinary(image_path, env):
    import cloudinary
    import cloudinary.uploader

    cloudinary.config(
        cloud_name=env.get("CLOUDINARY_CLOUD", ""),
        api_key=env.get("CLOUDINARY_KEY", ""),
        api_secret=env.get("CLOUDINARY_SECRET", ""),
        secure=True
    )

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
            print(f"  Yuklendi: {Path(image_path).name} -> {url}")
            return url
        print(f"  Yukleme basarisiz: {result}")
        return None
    except Exception as e:
        print(f"  Hata: {e}")
        return None


def find_media(folder_path):
    folder = Path(folder_path)
    files = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.mp4", "*.mov"]:
        files.extend(folder.glob(ext))
    files.sort(key=lambda x: x.name)
    return files


def read_caption(folder_path):
    folder = Path(folder_path)

    txt_file = folder / "instagram-aciklama.txt"
    if txt_file.exists():
        caption = txt_file.read_text(encoding="utf-8").strip()
        if caption:
            return caption

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
            return caption

    print("HATA: Caption bulunamadi!")
    sys.exit(1)


def load_queue():
    if QUEUE_FILE.exists():
        return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    return []


def save_queue(data):
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def add_to_queue(post_type, folder, schedule_str):
    env = load_env()
    folder_path = PROJECT_DIR / folder if not Path(folder).is_absolute() else Path(folder)

    print(f"\n{'='*50}")
    print(f"  Kuyruğa Ekleniyor")
    print(f"{'='*50}")
    print(f"  Tip: {post_type}")
    print(f"  Klasor: {folder}")
    print(f"  Zaman: {schedule_str}")

    # Gorselleri bul
    media_files = find_media(folder_path)
    if not media_files:
        print(f"HATA: {folder_path} klasorunde gorsel bulunamadi!")
        sys.exit(1)
    print(f"  Gorsel: {len(media_files)} adet")

    # Caption oku
    caption = read_caption(folder_path)
    print(f"  Caption: {len(caption)} karakter")

    # Cloudinary'ye yukle
    print(f"\n  Cloudinary'ye yukleniyor...")
    urls = []
    for f in media_files:
        url = upload_to_cloudinary(str(f), env)
        if url:
            urls.append(url)
        else:
            print(f"HATA: {f.name} yuklenemedi!")
            sys.exit(1)
        time.sleep(1)

    # Queue'ya ekle
    queue = load_queue()
    entry = {
        "name": Path(folder).name,
        "type": post_type,
        "datetime": schedule_str,
        "caption": caption,
        "urls": urls,
        "status": "pending",
        "added_at": time.strftime("%Y-%m-%d %H:%M")
    }
    queue.append(entry)
    save_queue(queue)

    print(f"\n  KUYRUGA EKLENDI!")
    print(f"  {schedule_str} saatinde otomatik yayinlanacak.")
    print(f"{'='*50}")


def list_queue():
    queue = load_queue()
    if not queue:
        print("  Kuyruk bos.")
        return

    print(f"\n{'='*60}")
    print(f"  Yayin Kuyrugu ({len(queue)} icerik)")
    print(f"{'='*60}")
    for i, entry in enumerate(queue, 1):
        status = entry.get("status", "?")
        icon = {"pending": "⏰", "published": "✅", "failed": "❌"}.get(status, "?")
        print(f"  {i}. {icon} {entry['datetime']} — {entry['name']} ({entry['type']})")
        if status == "published":
            print(f"     Media ID: {entry.get('media_id', '?')}")
    print(f"{'='*60}")


def main():
    if len(sys.argv) < 2:
        print("""
Kullanim:
  python scripts/queue-add.py carousel <klasor> "YYYY-MM-DD HH:MM"
  python scripts/queue-add.py post <klasor> "YYYY-MM-DD HH:MM"
  python scripts/queue-add.py reels <klasor> "YYYY-MM-DD HH:MM"
  python scripts/queue-add.py list
        """)
        sys.exit(1)

    action = sys.argv[1]

    if action == "list":
        list_queue()
    elif action in ["carousel", "post", "reels"]:
        if len(sys.argv) < 4:
            print("HATA: <klasor> ve <tarih saat> gerekli!")
            sys.exit(1)
        add_to_queue(action, sys.argv[2], sys.argv[3])
    else:
        print(f"Bilinmeyen: {action}")


if __name__ == "__main__":
    main()
