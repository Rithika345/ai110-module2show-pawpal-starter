"""Automated test suite for PawPal+ system."""

import pytest
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


@pytest.fixture
def setup():
    owner = Owner(name="Test Owner")
    dog = Pet(name="Rex", species="Dog", age=2)
    cat = Pet(name="Luna", species="Cat", age=4)
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat, Scheduler(owner)


def test_task_completion():
    task = Task(description="Walk", time="08:00")
    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_add_task_increases_count(setup):
    _, dog, _, _ = setup
    initial = len(dog.tasks)
    dog.add_task(Task(description="Feed", time="09:00"))
    assert len(dog.tasks) == initial + 1


def test_sort_by_time(setup):
    owner, dog, _, scheduler = setup
    dog.add_task(Task(description="Evening walk", time="18:00"))
    dog.add_task(Task(description="Morning feed", time="07:00"))
    dog.add_task(Task(description="Noon meds", time="12:00"))
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_daily_recurrence():
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    task = Task(description="Feed", time="08:00", frequency="daily", date=today)
    new_task = task.mark_complete()
    assert new_task is not None
    assert new_task.date == tomorrow
    assert not new_task.completed


def test_weekly_recurrence():
    today = datetime.now().strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
    task = Task(description="Grooming", time="10:00", frequency="weekly", date=today)
    new_task = task.mark_complete()
    assert new_task is not None
    assert new_task.date == next_week


def test_conflict_detection(setup):
    _, dog, cat, scheduler = setup
    dog.add_task(Task(description="Walk", time="09:00"))
    cat.add_task(Task(description="Feed", time="09:00"))
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) >= 1
    assert "Conflict" in conflicts[0]


def test_filter_by_pet(setup):
    _, dog, cat, scheduler = setup
    dog.add_task(Task(description="Walk", time="08:00"))
    cat.add_task(Task(description="Feed", time="09:00"))
    dog_tasks = scheduler.filter_by_pet("Rex")
    assert all(t.pet_name == "Rex" for t in dog_tasks)


def test_filter_by_status(setup):
    _, dog, _, scheduler = setup
    t1 = Task(description="Walk", time="08:00")
    t2 = Task(description="Feed", time="09:00")
    dog.add_task(t1)
    dog.add_task(t2)
    t1.mark_complete()
    pending = scheduler.filter_by_status(completed=False)
    completed = scheduler.filter_by_status(completed=True)
    assert t2 in pending
    assert t1 in completed


def test_no_recurrence_for_once_task():
    task = Task(description="Vet visit", time="14:00", frequency="once")
    result = task.mark_complete()
    assert result is None
    assert task.completed
