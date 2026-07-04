# ncs-daily-reminder

매일 아침 텔레그램으로 NCS 문제풀이 앱(artleebk.netlify.app) 링크를 보내는 GitHub Actions 저장소.

## 설정 방법

1. GitHub에서 새 저장소 생성 (예: `ncs-daily-reminder`), 이 폴더 내용 push.
2. 저장소 **Settings → Secrets and variables → Actions**에서 secret 2개 등록:
   - `TELEGRAM_BOT_TOKEN` — 기존 mirae_art_bot 토큰을 재사용하거나 새 봇 생성 (@BotFather)
   - `TELEGRAM_CHAT_ID` — 알림 받을 chat id (기존 봇에서 쓰던 값 그대로 사용 가능)
3. **Actions** 탭에서 워크플로우가 보이는지 확인하고, `workflow_dispatch`로 한 번 수동 실행해 테스트.
4. 문제 없으면 매일 KST 08:00에 자동 발송됩니다.

## 알림 시간 변경

`.github/workflows/daily-reminder.yml`의 cron 값을 수정하세요.
cron은 UTC 기준이라 KST = UTC+9 입니다. 예: KST 07:30 알림 → `30 22 * * *`.

## 메시지 문구 변경

`send_reminder.py`의 `MESSAGES` 리스트를 수정하면 됩니다.
