"""Tests for PawPal+ scheduling behavior."""

from pawpal_system import (
    DailyPlan,
    Owner,
    Pet,
    Priority,
    ScheduledTask,
    Scheduler,
    Task,
    TaskType,
)


def make_task(title, minutes, priority, category=TaskType.OTHER):
    return Task(
        title=title,
        category=category,
        duration_minutes=minutes,
        priority=priority,
    )


def test_sort_orders_high_priority_first():
    scheduler = Scheduler(Owner(name="Jordan"))
    tasks = [
        make_task("low", 10, Priority.LOW),
        make_task("high", 10, Priority.HIGH),
        make_task("medium", 10, Priority.MEDIUM),
    ]
    ordered = [t.title for t in scheduler.sort_tasks(tasks)]
    assert ordered == ["high", "medium", "low"]


def test_sort_breaks_ties_by_shorter_duration():
    scheduler = Scheduler(Owner(name="Jordan"))
    tasks = [
        make_task("long", 30, Priority.HIGH),
        make_task("short", 5, Priority.HIGH),
    ]
    ordered = [t.title for t in scheduler.sort_tasks(tasks)]
    assert ordered == ["short", "long"]


def test_fits_respects_remaining_minutes():
    scheduler = Scheduler(Owner(name="Jordan"))
    task = make_task("walk", 30, Priority.HIGH)
    assert scheduler.fits(task, 30) is True
    assert scheduler.fits(task, 29) is False


def test_build_plan_skips_tasks_that_exceed_time_budget():
    owner = Owner(name="Jordan", available_minutes=40)
    scheduler = Scheduler(owner)
    tasks = [
        make_task("walk", 30, Priority.HIGH),
        make_task("grooming", 45, Priority.LOW),  # never fits
        make_task("feeding", 10, Priority.HIGH),
    ]
    plan = scheduler.build_plan(Pet(name="Mochi", species="dog"), tasks)

    scheduled = [e.task.title for e in plan.entries]
    assert scheduled == ["feeding", "walk"]  # both high; shorter first
    assert plan.total_minutes == 40
    assert [t.title for t in plan.skipped] == ["grooming"]


def test_build_plan_assigns_sequential_start_times():
    owner = Owner(name="Jordan", available_minutes=60)
    scheduler = Scheduler(owner)
    tasks = [
        make_task("feeding", 10, Priority.HIGH),
        make_task("walk", 30, Priority.HIGH),
    ]
    plan = scheduler.build_plan(Pet(name="Mochi", species="dog"), tasks)

    # day_start defaults to 08:00; shorter high-priority task goes first
    assert plan.entries[0].start_time.strftime("%H:%M") == "08:00"
    assert plan.entries[0].end_time.strftime("%H:%M") == "08:10"
    assert plan.entries[1].start_time.strftime("%H:%M") == "08:10"
    assert plan.entries[1].end_time.strftime("%H:%M") == "08:40"


def test_build_plan_with_no_tasks_is_empty():
    scheduler = Scheduler(Owner(name="Jordan"))
    plan = scheduler.build_plan(Pet(name="Mochi", species="dog"), [])
    assert plan.entries == []
    assert plan.skipped == []
    assert plan.total_minutes == 0


def test_daily_plan_add_entry_updates_total():
    plan = DailyPlan(plan_date=None)
    task = make_task("walk", 25, Priority.HIGH)
    entry = ScheduledTask(task=task, start_time=None, end_time=None)
    plan.add_entry(entry)
    assert plan.total_minutes == 25
    assert plan.entries == [entry]


def test_explanation_mentions_scheduled_and_skipped():
    owner = Owner(name="Jordan", available_minutes=20)
    scheduler = Scheduler(owner)
    tasks = [
        make_task("walk", 15, Priority.HIGH),
        make_task("grooming", 45, Priority.LOW),
    ]
    plan = scheduler.build_plan(Pet(name="Mochi", species="dog"), tasks)
    text = scheduler.explain(plan)
    assert "walk" in text
    assert "Skipped" in text
    assert "grooming" in text
