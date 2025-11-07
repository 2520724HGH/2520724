
# WritePad (Flask)

초간단 '무엇이든 쓰기' 앱 — 배포용 패키지

## 로컬 실행
```bash
pip install -r requirements.txt
python writepad.py
# http://127.0.0.1:5000
```

## Render/Railway/Heroku류 배포
1) 이 폴더를 GitHub에 새 레포로 올림
2) Render(또는 Railway)에서 New Web Service 선택
3) Build/Start 명령은 자동으로 인식됨
   - Start command: `gunicorn writepad:app`
4) 배포 후 제공된 URL 접속

※ 이 앱은 메모리 저장이라 서버가 재시작되면 글이 지워집니다.
   (실서비스는 SQLite/PG 등 DB 연동 권장)
