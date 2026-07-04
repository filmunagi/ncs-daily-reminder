import os
import sys
import random
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
APP_URL = os.environ.get("APP_URL", "https://artleebk.netlify.app")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
SYNC_CODE = os.environ.get("SYNC_CODE")

MESSAGES = [
    "오늘 NCS 아직 안 풀었어요! 한 문제만 풀고 스트릭 이어가요.",
    "점심시간 짬 내서 NCS 한 문제 풀고 갈까요?",
    "오늘 몫 아직 안 끝났어요. 지금 5분만 투자해봐요.",
    "스트릭 끊기기 전에 얼른 한 문제!",
]


def already_solved_today() -> bool:
    """Supabase에서 오늘 날짜가 attendance_dates에 있는지 확인."""
    if not (SUPABASE_URL and SUPABASE_ANON_KEY and SYNC_CODE):
        # 설정이 안 되어 있으면 안전하게 "아직 안 풀었다"고 간주하고 알림을 보냄
        return False

    today = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d")
    url = f"{SUPABASE_URL}/rest/v1/ncs_progress"
    params = {"select": "attendance_dates", "sync_code": f"eq.{SYNC_CODE}"}
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    }
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    rows = resp.json()
    if not rows:
        return False
    attendance_dates = rows[0].get("attendance_dates") or []
    return today in attendance_dates


def send_telegram_message():
    text = f"{random.choice(MESSAGES)}\n\n{APP_URL}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    resp.raise_for_status()
    print("알림 전송 완료:", resp.json().get("ok"))


def main():
    if not BOT_TOKEN or not CHAT_ID:
        print("TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID가 설정되지 않았습니다.", file=sys.stderr)
        sys.exit(1)

    if already_solved_today():
        print("오늘 이미 풀었음 — 알림 생략")
        return

    send_telegram_message()


if __name__ == "__main__":
    main()
