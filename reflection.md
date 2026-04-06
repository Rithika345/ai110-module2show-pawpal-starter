# PawPal+ Reflection

## System Design

### Core Actions
Three core actions a user should be able to perform:
1. **Add a pet** — Register a new pet with its name, species, and age so it can be tracked in the system.
2. **Schedule a task** — Create a care activity (feeding, walk, vet visit) with a specific time and recurrence frequency for a given pet.
3. **View today's schedule** — See all pending tasks for the day sorted chronologically, with conflict warnings if two tasks overlap.

### 1a. Initial Design
I designed four classes with clear responsibilities:
- **Task** (dataclass): Holds a description, time, frequency, completion status, and date. Knows how to mark itself complete and generate a recurrence if needed.
- **Pet** (dataclass): Stores pet info (name, species, age) and owns a list of Tasks. Can add tasks and filter for pending ones.
- **Owner** (dataclass): Manages a list of Pets. Provides lookup by name and aggregates all tasks across pets.
- **Scheduler**: The orchestration layer. Takes an Owner reference and implements sorting, filtering, conflict detection, and recurrence handling. It never stores tasks directly — it always queries through the Owner, keeping a single source of truth.

### 1b. Design Changes
After reviewing the skeleton, I made a few adjustments:
- Added a `date` field to Task so that recurring tasks could generate future-dated instances instead of overwriting the original.
- Moved recurrence logic into `Task.mark_complete()` so the Task itself is responsible for knowing its next occurrence, while the Scheduler calls it and attaches the new task to the correct Pet.
- Added `pet_name` as a Task attribute so tasks remain identifiable when aggregated across multiple pets in the Scheduler.

## Algorithmic Layer

### 2a. Algorithms Implemented
- **Sorting**: `sorted()` with a `lambda t: t.time` key. Since times are stored as `"HH:MM"` strings, lexicographic sorting produces correct chronological order.
- **Filtering**: Simple list comprehensions matching on `pet_name` or `completed` status.
- **Conflict detection**: Nested loop comparing all task pairs for matching `(time, date)` tuples. Returns human-readable warning strings.
- **Recurrence**: `timedelta(days=1)` for daily, `timedelta(weeks=1)` for weekly. New task is a fresh instance with `completed=False`.

### 2b. Tradeoffs
The conflict detection only checks for exact time matches, not overlapping durations. A 30-minute vet appointment at 2:00 PM and a grooming session at 2:15 PM wouldn't be flagged. I chose this because tasks don't currently have a duration field, and adding one would increase complexity without clear benefit for the typical use case of short pet care activities. If duration tracking became important, I'd add a `duration_minutes` field and check for interval overlap instead.

The pairwise comparison is O(n²), which is fine for a household pet scheduler (maybe 10-20 tasks) but wouldn't scale to thousands of tasks. A production system might bucket tasks by `(date, time)` in a dictionary for O(n) detection.

## AI Strategy

### Most effective Copilot features
Agent Mode was most useful for fleshing out the full class implementations from skeletons. It understood the relationships between classes and generated consistent method signatures. Inline Chat was great for targeted improvements, like asking for a cleaner print format or a lambda-based sort.

### AI suggestion I rejected
Copilot initially suggested the Scheduler should maintain its own internal copy of all tasks. I rejected this because it would create a synchronization problem — if a task was added to a Pet directly, the Scheduler's copy would be stale. Instead, I kept the Scheduler stateless: it always queries the Owner's pets for fresh data. This is simpler and avoids bugs from duplicated state.

### Separate chat sessions
Using separate chat sessions for design vs. algorithms vs. testing kept context focused. The algorithm session didn't get cluttered with UI questions, and the testing session could focus purely on edge cases without revisiting implementation details.

### What I learned
Being the "lead architect" means AI is a powerful drafting tool, but I need to own the design decisions. The AI doesn't know my constraints (like wanting a single source of truth for tasks) unless I tell it. The best workflow was: I decide the architecture, AI drafts the code, I review for alignment with my design intent, and I course-correct when the AI optimizes for the wrong thing.
