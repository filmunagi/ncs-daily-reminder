import os
import sys
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
APP_URL = os.environ.get("APP_URL", "https://artleebk.netlify.app")

MESSAGES = [
    "오늘도 NCS 문제 풀 시간! 스트릭 끊기지 않게 한 문제만 풀고 시작해요.",
    "출근 전 5분, NCS 한 문제. 오늘도 스트릭 이어가요!",
    "잠깐 시간 내서 NCS 문제 풀고 하루 시작하기 어때요?",
]


def main():
    if not BOT_TOKEN or not CHAT_ID:
        print("TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID가 설정되지 않았습니다.", file=sys.stderr)
        sys.exit(1)

    import random
    text = f"{random.choice(MESSAGES)}\n\n{APP_URL}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    resp.raise_for_status()
    print("알림 전송 완료:", resp.json().get("ok"))


if __name__ == "__main__":
    main()
