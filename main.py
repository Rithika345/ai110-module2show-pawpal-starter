"""PawPal+ Demo Script - Verifies backend logic via CLI."""

from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner and pets
owner = Owner(name="Rithika")

buddy = Pet(name="Buddy", species="Dog", age=3)
whiskers = Pet(name="Whiskers", species="Cat", age=5)

owner.add_pet(buddy)
owner.add_pet(whiskers)

# Add tasks (intentionally out of order to test sorting)
buddy.add_task(Task(description="Evening walk", time="18:00", frequency="daily"))
buddy.add_task(Task(description="Morning feeding", time="07:30", frequency="daily"))
buddy.add_task(Task(description="Vet appointment", time="14:00"))
whiskers.add_task(Task(description="Morning feeding", time="07:30", frequency="daily"))
whiskers.add_task(Task(description="Medication", time="09:00", frequency="daily"))
whiskers.add_task(Task(description="Grooming", time="14:00", frequency="weekly"))

scheduler = Scheduler(owner)

# --- Today's Schedule (sorted) ---
print("=" * 50)
print("📅 TODAY'S SCHEDULE (Sorted by Time)")
print("=" * 50)
for task in scheduler.get_todays_schedule():
    print(f"  {task}")

# --- Conflict Detection ---
print("\n🔍 CONFLICT CHECK")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for c in conflicts:
        print(f"  {c}")
else:
    print("  No conflicts found.")

# --- Filter by Pet ---
print(f"\n🐶 Buddy's Tasks:")
for task in scheduler.filter_by_pet("Buddy"):
    print(f"  {task}")

# --- Mark Complete + Recurrence ---
print("\n✅ Marking Buddy's morning feeding as complete...")
buddy_feeding = buddy.tasks[1]  # Morning feeding
new_task = scheduler.mark_task_complete(buddy_feeding, buddy)
if new_task:
    print(f"  Recurring task created: {new_task}")

# --- Pending Tasks ---
print(f"\n📋 Pending tasks: {len(scheduler.filter_by_status(completed=False))}")
print(f"✅ Completed tasks: {len(scheduler.filter_by_status(completed=True))}")
