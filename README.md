# cautious-enigma
LexAI Butler – Your Personal Desktop AI Assistant (GPT4All, Python, SQLite)

LexAI Butler is a lightweight, fully offline, AI-powered personal assistant designed to help manage your day-to-day tasks — including reminders, notes, schedules, and intelligent conversation — all running locally on your machine.
It uses GPT4All (Llama-3.2-3B-Instruct) for natural language understanding, SQLite for long-term memory, and Python for automation logic.

Lexy speaks politely, responds intelligently, remembers information you give her, and operates completely offline.

🚀 Project Features
🧠 1. Local LLM Chat Assistant

Powered by GPT4All + Llama-3.2-3B-Instruct-Q4_0.gguf

Runs fully offline

CPU-friendly (CUDA optional)

Uses short, polished responses with a distinct personality (“sir” style but adjustable)

📝 2. Intelligent Note System

Lexy can:

Create notes

Show saved notes

Delete individual notes

Delete all notes

Examples

note: Buy milk
show notes
delete note 3
delete all notes

📅 3. Personal Schedule Manager

Save events with dates:

schedule: meeting at 2025-09-02 10:00
show schedule
delete schedule 2
delete all schedule

⏰ 4. Automatic Reminder System

Reminders run in a background thread and notify you at the exact time.

remind me: submit assignment at 2025-11-10 14:00
show reminders
delete reminder 1


Lexy prints a 🔔 notification when the time arrives.

🧩 5. Long-Term Memory

A JSON-based conversation memory stores the last 50 messages so Lexy remains context-aware without hallucinating.

recall
recall recent

🗂️ 6. SQLite Database Backend

A local lexy.db file stores:

Notes

Reminders

Schedules

No external database or internet required.

⚙️ 7. Robust Error-Free Model Loading

Includes:

CPU fallback

Graceful handling of missing CUDA DLLs

Safe model initialization

🎤 8. Voice Mode Integration (Optional)

Supports integration with:

Eleven Labs (text-to-speech)

pyttsx3 (offline TTS)

Vosk / Whisper (speech-to-text)

Voice features can be enabled at any time.

🛠️ Technology Stack
Component	Tool
Programming Language	Python 3.x
AI Model	GPT4All – Llama-3.2-3B-Instruct Q4_0 gguf
Local Database	SQLite3
Memory Storage	JSON
Threading	Python threading
Environment	Windows 10/11 (CLI)
Dependency Manager	venv + pip
📁 Project Structure
LexAI_Butler/
│── main.py
│── database.py
│── memory.json
│── lexy.db
│── venv/
│── models/
│     └── Llama-3.2-3B-Instruct-Q4_0.gguf

▶️ How to Run LexAI Butler
Step 1 — Activate Virtual Environment
cd C:\Users\Ryan\Desktop\LexAI_Butler
venv\Scripts\activate

Step 2 — Run the Assistant
python main.py

💬 Example Interaction
Lexy: Hello sir 👋, I’m ready to assist you.
You: note: remember to read chapter 3
Lexy: Saved your note, sir.
You: remind me: call John at 2025-11-05 12:00
Lexy: Reminder set, sir.
You: show schedule
You: recall recent

🎯 Project Goals

Build a fully offline personal assistant

Provide a portable AI you can customize

Enable future expansion:

Voice control

System automation

Smart file search

Web APIs

Home automation

🤝 Contributing

This project is beginner-friendly and modular. Feel free to:

Add new assistant skills

Improve memory context

Integrate voice

Add a GUI (Tkinter, PyQt, Web UI)

Pull requests are welcome.
