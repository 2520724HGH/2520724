
from flask import Flask, request, redirect, url_for, render_template_string
from datetime import datetime

app = Flask(__name__)

# In-memory storage (resets when server restarts)
notes = []  # each: {"id": int, "text": str, "author": str|None, "time": datetime}

BASE = '''
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title or "WritePad" }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-neutral-50 text-neutral-900">
    <header class="sticky top-0 bg-white/80 backdrop-blur border-b border-neutral-200">
      <div class="max-w-2xl mx-auto px-4 py-3 flex items-center gap-3">
        <a href="{{ url_for('index') }}" class="font-black">WritePad</a>
        <a href="{{ url_for('reset') }}" class="ml-auto text-sm underline">모두 지우기</a>
      </div>
    </header>
    <main class="max-w-2xl mx-auto px-4 py-6">{{ body|safe }}</main>
  </body>
</html>
'''

def page(title, body):
    return render_template_string(BASE, title=title, body=body)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = (request.form.get("text") or "").strip()
        author = (request.form.get("author") or "").strip() or None
        if text:
            notes.append({
                "id": len(notes) + 1,
                "text": text,
                "author": author,
                "time": datetime.now(),
            })
        return redirect(url_for("index"))

    body = '''
    <form method="post" class="space-y-3 mb-6">
      <textarea name="text" rows="5" class="w-full px-3 py-2 rounded-xl border border-neutral-300" placeholder="무엇이든 적어보세요" required></textarea>
      <div class="flex gap-2">
        <input name="author" class="flex-1 px-3 py-2 rounded-xl border border-neutral-300" placeholder="작성자(선택)">
        <button class="px-4 py-2 rounded-xl bg-black text-white">올리기</button>
      </div>
    </form>
    '''
    if not notes:
        body += '<div class="p-6 rounded-2xl bg-neutral-100 text-neutral-600">아직 아무 글도 없어요.</div>'
    else:
        body += '<div class="space-y-4">'
        for n in sorted(notes, key=lambda x: x["time"], reverse=True):
            who = n["author"] or "익명"
            t = n["time"].strftime("%Y-%m-%d %H:%M")
            body += f'''
            <article class="p-4 rounded-2xl bg-white border border-neutral-200">
              <div class="text-sm text-neutral-500">{t} · {who}</div>
              <p class="mt-2 whitespace-pre-wrap">{n["text"]}</p>
            </article>
            '''
        body += '</div>'
    return page("WritePad", body)

@app.route("/reset")
def reset():
    notes.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # debug=False → Ctrl+C 한 번으로 종료, 프로덕션에서도 안전
    app.run(host="0.0.0.0", port=5000, debug=False)
