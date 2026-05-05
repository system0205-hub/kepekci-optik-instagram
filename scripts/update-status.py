"""
STATUS.md uretici — Claude'un session basinda hizlica durumu anlamasi icin.

queue.json'u okur, son yayinlanan + sira bekleyen + hatali girisleri ozetler,
projenin koklerinde STATUS.md dosyasini olusturur.

Cron her saat calistirinca cagrilir (yayin olsa da olmasa da).
"""

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).parent.parent
QUEUE_FILE = ROOT / "content" / "queue.json"
STATUS_FILE = ROOT / "STATUS.md"
TURKEY_TZ = ZoneInfo("Europe/Istanbul")


def main():
    if not QUEUE_FILE.exists():
        print("queue.json bulunamadi.")
        return

    queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    now = datetime.now(TURKEY_TZ)

    published = [e for e in queue if e.get("status") == "published"]
    pending = [e for e in queue if e.get("status") == "pending"]
    failed = [e for e in queue if e.get("status") == "failed"]

    published.sort(key=lambda e: e.get("published_at", ""), reverse=True)
    pending.sort(key=lambda e: e.get("datetime", ""))

    lines = []
    lines.append("# Kepekci Optik — Yayin Durumu")
    lines.append("")
    lines.append(f"**Son guncelleme:** {now.strftime('%Y-%m-%d %H:%M')} (Turkiye saati)")
    lines.append("")
    lines.append(
        f"Toplam: {len(queue)} | Yayinlandi: {len(published)} | "
        f"Bekleyen: {len(pending)} | Hatali: {len(failed)}"
    )
    lines.append("")

    if pending:
        lines.append("## Sira bekleyen (sonraki 5)")
        lines.append("")
        for e in pending[:5]:
            lines.append(
                f"- **{e.get('name', '?')}** ({e.get('type', '?')}) — "
                f"{e.get('datetime', '?')}"
            )
        lines.append("")
    else:
        lines.append("## Sira bekleyen")
        lines.append("")
        lines.append("_(Kuyrukta hicbir sey yok — yeni icerik eklemek lazim)_")
        lines.append("")

    if failed:
        lines.append("## DIKKAT — Hatali yayinlar")
        lines.append("")
        for e in failed:
            lines.append(
                f"- **{e.get('name', '?')}** ({e.get('type', '?')}) — "
                f"planlanan: {e.get('datetime', '?')}, "
                f"hata zamani: {e.get('failed_at', '?')}"
            )
        lines.append("")

    if published:
        lines.append("## Son yayinlananlar (son 5)")
        lines.append("")
        for e in published[:5]:
            media_id = e.get("media_id", "")
            link = (
                f" — https://www.instagram.com/p/{media_id}/" if media_id else ""
            )
            lines.append(
                f"- **{e.get('name', '?')}** ({e.get('type', '?')}) — "
                f"{e.get('published_at', '?')}{link}"
            )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "_Bu dosya `scripts/update-status.py` tarafindan otomatik uretilir. "
        "Elle duzenleme — sonraki cron uzerine yazar._"
    )
    lines.append("")

    STATUS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"STATUS.md guncellendi: {STATUS_FILE}")


if __name__ == "__main__":
    main()
