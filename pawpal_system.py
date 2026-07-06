"""PawPal+ domain model — class stubs generated from diagrams/uml.mmd.

No scheduling logic yet. Implement the method bodies in small increments
(step 4 of the README workflow) and add tests as you go.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class TaskType(Enum):
    WALK = "walk"
    FEEDING = "feeding"
    MEDS = "meds"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"
    OTHER = "other"


@dataclass
class Owner:
    name: str
    preferences: list[str] = field(default_factory=list)
    day_start: time = time(8, 0)
    day_end: time = time(20, 0)
    available_minutes: int = 120


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age: int = 0
    tasks: list["Task"] = field(default_factory=list)


@dataclass
class Task:
    title: str
    category: TaskType
    duration_minutes: int
    priority: Priority
    preferred_time: time | None = None
    completed: bool = False

    def priority_score(self) -> int:
        """Return a sortable score for this task (higher = more important)."""
        return self.priority.value


@dataclass
class ScheduledTask:
    task: Task
    start_time: time
    end_time: time
    reason: str = ""


@dataclass
class DailyPlan:
    plan_date: date
    entries: list[ScheduledTask] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    total_minutes: int = 0

    def add_entry(self, entry: ScheduledTask) -> None:
        """Append a scheduled task and update total_minutes."""
        self.entries.append(entry)
        self.total_minutes += entry.task.duration_minutes

    def explanation(self) -> str:
        """Return a human-readable summary of why the plan looks the way it does."""
        lines = [f"Daily plan for {self.plan_date} — {self.total_minutes} min scheduled:"]
        for e in self.entries:
            lines.append(
                f"  {e.start_time:%H:%M} — {e.task.title} "
                f"({e.task.duration_minutes} min) [priority: {e.task.priority.name.lower()}] "
                f"— {e.reason}"
            )
        if self.skipped:
            names = ", ".join(t.title for t in self.skipped)
            lines.append(f"Skipped (not enough time): {names}")
        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (high first), then shorter tasks first."""
        return sorted(
            tasks,
            key=lambda t: (-t.priority_score(), t.duration_minutes),
        )

    def fits(self, task: Task, remaining: int) -> bool:
        """True if the task fits in the remaining available minutes."""
        return task.duration_minutes <= remaining

    def build_plan(self, pet: Pet, tasks: list[Task]) -> DailyPlan:
        """Choose and order tasks under the owner's constraints; return a DailyPlan."""
        plan = DailyPlan(plan_date=date.today())
        remaining = self.owner.available_minutes
        cursor = datetime.combine(plan.plan_date, self.owner.day_start)

        for task in self.sort_tasks(tasks):
            if self.fits(task, remaining):
                end = cursor + timedelta(minutes=task.duration_minutes)
                reason = (
                    f"chosen because priority is {task.priority.name.lower()} "
                    f"and it fits the remaining {remaining} min"
                )
                plan.add_entry(
                    ScheduledTask(
                        task=task,
                        start_time=cursor.time(),
                        end_time=end.time(),
                        reason=reason,
                    )
                )
                remaining -= task.duration_minutes
                cursor = end
            else:
                plan.skipped.append(task)

        return plan

    def explain(self, plan: DailyPlan) -> str:
        """Produce the reasoning for the given plan."""
        return plan.explanation()
