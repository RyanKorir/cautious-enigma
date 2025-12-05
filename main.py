# main.py
from gpt4all import GPT4All
import time
import threading
from datetime import datetime
import json
import os
import webbrowser
import database

# ---------------- Memory System ----------------
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"conversations": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def remember(user_input, lexy_response):
    mem = load_memory()
    mem["conversations"].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_input,
        "lexy": lexy_response
    })
    # Keep last 200 turns to maintain context but prevent unbounded growth
    mem["conversations"] = mem["conversations"][-200:]
    save_memory(mem)

def recall_summary(limit=5):
    mem = load_memory()
    convos = mem["conversations"][-limit:]
    if not convos:
        return "Sir, I don’t have any past conversations saved."
    # Produce short, clean bullets summarizing pairs (user -> lex)
    bullets = []
    for c in convos:
        u = c['user'].strip().replace('\n',' ')[:200]
        l = c['lexy'].strip().replace('\n',' ')[:200]
        bullets.append(f"- You: {u} → Lexy: {l}")
    return "Here’s what I recall from recent chats, sir:\n" + "\n".join(bullets)

# ---------------- Initialize DB ----------------
database.init_db()

# ---------------- Model ----------------
model_path = r"C:\Users\Ryan\AppData\Local\nomic.ai\GPT4All\Llama-3.2-3B-Instruct-Q4_0.gguf"
# Force CPU mode to avoid CUDA errors and ensure compatibility
model = GPT4All(model_path, device="cpu")

# ---------------- Reminders Checker ----------------
def reminder_checker():
    while True:
        reminders = database.get_reminders()
        now = datetime.now()
        for r in reminders:
            try:
                reminder_time = datetime.fromisoformat(r[2])
            except Exception:
                # If stored format differs, skip gracefully
                continue
            if reminder_time <= now:
                notice = f"Reminder, sir: {r[1]}"
                print("\n🔔", notice)
                # Optionally notify via desktop (plyer) - keep console fallback
                try:
                    from plyer import notification
                    notification.notify(title="Lexy Reminder", message=r[1], timeout=8)
                except Exception:
                    pass
                database.delete_reminder(r[0])
                remember(f"(system) reminder triggered: {r[1]}", notice)
        time.sleep(30)

threading.Thread(target=reminder_checker, daemon=True).start()

# ---------------- Utility functions / Intent routing ----------------
def open_youtube_search(query: str):
    q = webbrowser.quote(query)
    url = f"https://www.youtube.com/results?search_query={q}"
    webbrowser.open(url)
    return f"Opened YouTube search for '{query}', sir."

def safe_send_email_prep(to_email: str, subject: str, body: str):
    # Prepare mailto link (won't send automatically)
    mailto = f"mailto:{to_email}?subject={webbrowser.quote(subject)}&body={webbrowser.quote(body)}"
    webbrowser.open(mailto)
    return f"I prepared the email to {to_email} and opened your mail client, sir. Please review and send."

def parse_time_string_to_iso(timestr: str):
    # Use dateparser if available; otherwise return input
    try:
        import dateparser
        dt = dateparser.parse(timestr)
        if dt:
            return dt.isoformat()
    except Exception:
        pass
    return None

# ---------- Short-response enforcement ----------
def enforce_short(response_text: str, max_sentences: int = 3):
    # trim to max_sentences
    parts = [s.strip() for s in response_text.split('.') if s.strip()]
    if len(parts) <= max_sentences:
        return response_text.strip()
    return '. '.join(parts[:max_sentences]).strip() + '.'

# ---------------- Main Loop (command handling + chat) ----------------
print("Lexy: Hello sir 👋, I’m ready to assist you.")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue

    low = user_input.lower()

    if low in ["exit", "quit"]:
        print("Lexy: Goodbye sir. I’ll remember everything for next time.")
        break

    # ---- Recall memory ----
    if low in ["recall recent", "what do you remember", "recall"]:
        response = recall_summary(limit=5)
        print("Lexy:", response)
        remember(user_input, response)
        continue

    # ---- Notes ----
    if low.startswith("note:"):
        content = user_input[len("note:"):].strip()
        database.add_note(content)
        response = "Got it, sir — note saved."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if low == "show notes":
        notes = database.get_notes()
        if notes:
            response = "Your notes, sir:\n" + "\n".join([f"{n[0]}. {n[1]}" for n in notes])
        else:
            response = "No notes yet, sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if low == "delete all notes":
        database.delete_all_notes()
        response = "All notes cleared, sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if low.startswith("delete note"):
        try:
            note_id = int(low.split()[-1])
            database.delete_note(note_id)
            response = f"Note {note_id} deleted, sir."
        except:
            response = "Use → delete note [id], sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    # ---- Schedule ----
    if low.startswith("schedule:"):
        try:
            parts = user_input.replace("schedule:", "", 1).strip().split(" at ")
            event, timestr = parts[0].strip(), parts[1].strip()
            iso = parse_time_string_to_iso(timestr) or timestr
            database.add_schedule(event, iso)
            response = f"Scheduled '{event}' at {iso}, sir."
        except Exception:
            response = "Use → schedule: meeting at YYYY-MM-DD HH:MM, sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if low == "show schedule":
        events = database.get_schedule()
        if events:
            response = "Upcoming schedule, sir:\n" + "\n".join([f"{e[0]}. {e[1]} at {e[2]}" for e in events])
        else:
            response = "Nothing scheduled, sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if low == "delete all schedule":
        database.delete_all_schedule()
        response = "Schedule cleared, sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if low.startswith("delete schedule"):
        try:
            sched_id = int(low.split()[-1])
            database.delete_schedule(sched_id)
            response = f"Schedule {sched_id} deleted, sir."
        except:
            response = "Use → delete schedule [id], sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    # ---- Reminders ----
    if low.startswith("remind me:"):
        try:
            parts = user_input.replace("remind me:", "", 1).strip().split(" at ")
            content, timestr = parts[0].strip(), parts[1].strip()
            iso = parse_time_string_to_iso(timestr) or timestr
            database.add_reminder(content, iso)
            response = f"Reminder set → '{content}' at {iso}, sir."
        except:
            response = "Use → remind me: buy milk at YYYY-MM-DD HH:MM, sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if low == "show reminders":
        reminders = database.get_reminders()
        if reminders:
            response = "Your reminders, sir:\n" + "\n".join([f"{r[0]}. {r[1]} at {r[2]}" for r in reminders])
        else:
            response = "No reminders set, sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if low == "delete all reminders":
        database.delete_all_reminders()
        response = "All reminders cleared, sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if low.startswith("delete reminder"):
        try:
            rem_id = int(low.split()[-1])
            database.delete_reminder(rem_id)
            response = f"Reminder {rem_id} deleted, sir."
        except:
            response = "Use → delete reminder [id], sir."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    # ---- Play / YouTube quick intent ----
    if low.startswith("play "):
        # Example: "play chronixx song" or "play song chronixx"
        query = user_input[len("play "):].strip()
        response = open_youtube_search(query)
        print("Lexy:", response)
        remember(user_input, response)
        continue

    if "youtube" in low and ("play" in low or "on youtube" in low or low.startswith("youtube")):
        # user asked to use YouTube as platform - if previous intent was play, open
        # For safety, simply open YouTube search for last song request in memory if present
        # find last 'play' request
        mem = load_memory()["conversations"]
        last_play = next((c['user'] for c in reversed(mem) if c['user'].lower().startswith("play ")), None)
        if last_play:
            query = last_play[len("play "):].strip()
            response = open_youtube_search(query)
        else:
            response = "What should I search for on YouTube, sir?"
        print("Lexy:", response)
        remember(user_input, response)
        continue

    # ---- Email intent (prepare only) ----
    if low.startswith("send email to ") or low.startswith("email "):
        # parse "send email to X subject Y body Z" — keep simple and safe: prepare mailto
        parts = user_input.split()
        # find the first token that contains '@' as email
        email = next((t for t in parts if "@" in t and "." in t), None)
        if email:
            subject = "Message from Lexy"
            body = ""
            response = safe_send_email_prep(email, subject, body)
        else:
            response = "Provide an email address, sir (e.g., send email to me@example.com)."
        print("Lexy:", response)
        remember(user_input, response)
        continue

    # ---- Default: GPT4All Chat with context ----
    # Build short memory context (user and lexy pair summaries)
    past = load_memory()["conversations"][-10:]
    memory_context = "\n".join([f"You: {c['user']}\nLexy: {c['lexy']}" for c in past])

    personality_prefix = (
        "You are Lexy, a witty, polite AI assistant addressing the user as 'sir'. "
        "Keep replies SHORT (max 3 sentences). Avoid over-explaining, long lists, or repeating instructions. "
        "Stay concise, logical, and conversational. Use past context if directly relevant. "
        "If the user asks to perform an action you cannot do, offer a safe, transparent alternative."
    )

    prompt = f"{personality_prefix}\nPrevious:\n{memory_context}\nYou: {user_input}\nLexy:"
    with model.chat_session():
        response = model.generate(prompt, max_tokens=100, temp=0.6).strip()

    # post-process enforce brevity and remove any accidental system-like output
    if "You are Lexy" in response or "system" in response.lower():
        # trim potentially leaked policy text
        response = response.split("\n")[-1].strip()
    response = enforce_short(response, max_sentences=3)

    print("Lexy:", response)
    remember(user_input, response)
