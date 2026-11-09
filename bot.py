#!/usr/bin/env python3
import os, json, time, urllib.request, urllib.parse, sys, datetime

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        return json.load(open(DATA_FILE))
    except Exception:
        return {}

def save_data(d):
    json.dump(d, open(DATA_FILE, "w"), ensure_ascii=False, indent=2)

def send(token, chat_id, text):
    if not token: return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": str(chat_id), "text": text}).encode()
    urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=10)

def get_updates(token, offset=None):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {"timeout": "30"}
    if offset: params["offset"] = offset
    url += "?" + urllib.parse.urlencode(params)
    return json.loads(urllib.request.urlopen(url, timeout=35).read())

def parse_command(text):
    if not text or not text.startswith("/"): return None, []
    parts = text.strip().split()
    cmd = parts[0].lstrip("/").split("@")[0]
    return cmd, parts[1:]


def handle(token, chat_id, text, data):
    cmd, args = parse_command(text)
    user = data.setdefault(str(chat_id), [])
    if cmd == "start":
        send(token, chat_id, "Бот учёта трат.\n/add 120 Продукты молоко\n/stats\n/list")
    elif cmd == "add" and len(args) >= 2:
        try: amt = float(args[0])
        except: send(token, chat_id, "Сумма — число"); return
        rec = {"amt": amt, "cat": args[1], "desc": " ".join(args[2:]), "date": datetime.date.today().isoformat()}
        user.append(rec); save_data(data)
        send(token, chat_id, f"Добавлено {amt} {rec['cat']}")
    elif cmd == "stats":
        total = sum(r["amt"] for r in user if (not args or r["cat"] == args[0]))
        send(token, chat_id, f"Итого: {total}")
    elif cmd == "list":
        if not user: send(token, chat_id, "Пусто")
        else: send(token, chat_id, "\n".join(str(i+1)+". "+str(r["amt"])+" "+r["cat"]+" "+r["desc"] for i,r in enumerate(user[-10:])))
    elif cmd == "clear":
        user.clear(); save_data(data); send(token, chat_id, "Очищено")
    else:
        send(token, chat_id, "Неизвестная команда. /add /stats /list")
# test parse
def test_parse():
    cmd, args = parse_command("/add 100 Продукты молоко")
    assert cmd == "add" and args[0] == "100"

def main():
    global TOKEN
    if not TOKEN:
        print("Set TELEGRAM_BOT_TOKEN in .env or env var", file=sys.stderr); return
    offset = None
    print("Bot started")
    while True:
        try:
            updates = get_updates(TOKEN, offset)
            for u in updates.get("result", []):
                offset = u["update_id"] + 1
                msg = u.get("message", {})
                chat = msg.get("chat", {}).get("id")
                txt = msg.get("text", "")
                if chat and txt: handle(TOKEN, chat, txt, load_data())
        except Exception as e:
            print("err", e, file=sys.stderr); time.sleep(2)

if __name__ == "__main__":
    main()
