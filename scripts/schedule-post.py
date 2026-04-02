"""
Kepekci Optik — Windows Gorev Zamanlayici ile Instagram Paylasim
Kullanim:
  python scripts/schedule-post.py add carousel exports/yuz-sekline-gore-gozluk-secimi "2026-04-02 12:00"
  python scripts/schedule-post.py add post exports/cam-markalari-yetkili-satici "2026-04-03 19:00"
  python scripts/schedule-post.py list
  python scripts/schedule-post.py remove <task-adi>
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_DIR = Path(__file__).parent.parent
SCRIPT_PATH = PROJECT_DIR / "scripts" / "instagram-publish.py"
SCHEDULE_FILE = PROJECT_DIR / "content" / "scheduled-posts.json"


def load_schedule():
    if SCHEDULE_FILE.exists():
        return json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
    return []


def save_schedule(data):
    SCHEDULE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def add_task(post_type, folder, schedule_str):
    dt = datetime.strptime(schedule_str, "%Y-%m-%d %H:%M")
    date_str = dt.strftime("%d/%m/%Y")
    time_str = dt.strftime("%H:%M")

    folder_name = Path(folder).name
    task_name = f"KepekciOptik_{folder_name}_{dt.strftime('%Y%m%d_%H%M')}"

    python_path = sys.executable
    publish_script = str(SCRIPT_PATH)
    folder_full = str(PROJECT_DIR / folder)

    # Publish scripti icin batch dosyasi olustur (Windows Task Scheduler icin)
    batch_dir = PROJECT_DIR / "scripts" / "tasks"
    batch_dir.mkdir(exist_ok=True)
    batch_file = batch_dir / f"{task_name}.bat"

    batch_content = f'''@echo off
cd /d "{PROJECT_DIR}"
"{python_path}" "{publish_script}" {post_type} "{folder_full}"
echo Paylasim tamamlandi: {folder_name}
echo %date% %time% >> "{PROJECT_DIR}\\content\\publish-log.txt"
echo {folder_name} - YAYINLANDI >> "{PROJECT_DIR}\\content\\publish-log.txt"
'''
    batch_file.write_text(batch_content, encoding="utf-8")

    # Windows Gorev Zamanlayici'ya ekle
    cmd = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", str(batch_file),
        "/sc", "once",
        "/sd", date_str,
        "/st", time_str,
        "/f"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0:
            print(f"  ✅ Gorev eklendi: {task_name}")
            print(f"     Tarih: {schedule_str}")
            print(f"     Icerik: {folder_name} ({post_type})")

            # Schedule dosyasina kaydet
            schedule = load_schedule()
            schedule.append({
                "task_name": task_name,
                "post_type": post_type,
                "folder": folder,
                "datetime": schedule_str,
                "status": "scheduled",
                "batch_file": str(batch_file)
            })
            save_schedule(schedule)
            return True
        else:
            print(f"  ❌ HATA: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ HATA: {e}")
        return False


def list_tasks():
    schedule = load_schedule()
    if not schedule:
        print("  Zamanlanmis paylasim yok.")
        return

    print(f"\n{'='*60}")
    print(f"  Zamanlanmis Paylasimlar ({len(schedule)} adet)")
    print(f"{'='*60}")
    for i, task in enumerate(schedule, 1):
        status = task.get("status", "?")
        icon = "⏰" if status == "scheduled" else "✅" if status == "published" else "❌"
        print(f"  {i}. {icon} {task['datetime']} — {Path(task['folder']).name} ({task['post_type']})")
        print(f"     Gorev: {task['task_name']}")
    print(f"{'='*60}")


def remove_task(task_name):
    # Windows'tan sil
    cmd = ["schtasks", "/delete", "/tn", task_name, "/f"]
    subprocess.run(cmd, capture_output=True, text=True)

    # Schedule dosyasindan sil
    schedule = load_schedule()
    schedule = [t for t in schedule if t["task_name"] != task_name]
    save_schedule(schedule)
    print(f"  ✅ Gorev silindi: {task_name}")


def main():
    if len(sys.argv) < 2:
        print("""
Kullanim:
  python scripts/schedule-post.py add <tip> <klasor> "<tarih saat>"
  python scripts/schedule-post.py list
  python scripts/schedule-post.py remove <gorev-adi>

Ornekler:
  python scripts/schedule-post.py add carousel exports/yuz-sekline-gore-gozluk-secimi "2026-04-02 12:00"
  python scripts/schedule-post.py add post exports/cam-markalari-yetkili-satici "2026-04-03 19:00"
  python scripts/schedule-post.py list
        """)
        sys.exit(1)

    action = sys.argv[1]

    if action == "add":
        if len(sys.argv) < 5:
            print("HATA: add <tip> <klasor> \"<tarih saat>\" gerekli!")
            sys.exit(1)
        post_type = sys.argv[2]
        folder = sys.argv[3]
        schedule_str = sys.argv[4]

        print(f"\n{'='*60}")
        print(f"  Kepekci Optik — Zamanli Paylasim")
        print(f"{'='*60}")
        add_task(post_type, folder, schedule_str)

    elif action == "list":
        list_tasks()

    elif action == "remove":
        if len(sys.argv) < 3:
            print("HATA: remove <gorev-adi> gerekli!")
            sys.exit(1)
        remove_task(sys.argv[2])

    else:
        print(f"Bilinmeyen aksiyon: {action}")


if __name__ == "__main__":
    main()
