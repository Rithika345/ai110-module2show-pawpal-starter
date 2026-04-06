# 🐾 PawPal+

A smart pet care management system that helps owners keep their furry friends happy and healthy. Track feedings, walks, medications, and appointments with intelligent scheduling.

## Features

- **Pet Management** — Add and manage multiple pets with species and age info
- **Task Scheduling** — Create one-time, daily, or weekly recurring tasks
- **Sorting by Time** — Today's schedule is always displayed in chronological order
- **Conflict Detection** — Warnings when two tasks overlap at the same time
- **Recurring Tasks** — Completing a daily/weekly task auto-generates the next occurrence
- **Filtering** — View tasks by pet or by completion status
- **Streamlit UI** — Clean, interactive web interface with session persistence

## Smarter Scheduling

The `Scheduler` class acts as the system's brain. It pulls tasks from all pets via the `Owner`, then applies:

1. **Time-based sorting** using Python's `sorted()` with a lambda key on `HH:MM` strings
2. **Conflict detection** via pairwise comparison of task times and dates, returning warning strings instead of crashing
3. **Recurrence handling** using `timedelta` to calculate the next occurrence date when a recurring task is marked complete

## Getting Started

```bash
# Install dependencies
pip install streamlit pytest

# Run the CLI demo
python main.py

# Launch the web app
streamlit run app.py
```

## Testing PawPal+

```bash
python -m pytest tests/ -v
```

The test suite covers 9 cases: task completion, task count, chronological sorting, daily recurrence, weekly recurrence, conflict detection, pet filtering, status filtering, and one-time task behavior.

**Confidence Level:** ⭐⭐⭐⭐⭐ (9/9 tests passing)

## Tech Stack

- Python 3.12 with dataclasses
- Streamlit for the UI
- pytest for testing

## 📸 Demo

Run `streamlit run app.py` to see the app in action.
