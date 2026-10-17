from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task("Morning walk", "exercise", 30, "high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Robert", species="dog", age=3)
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feeding", "food", 10, "high"))
    assert len(pet.tasks) == 1

    pet.add_task(Task("Playtime", "enrichment", 20, "medium"))
    assert len(pet.tasks) == 2


def _scheduler_with(*tasks, pet_name="Robert"):
    owner = Owner(name="Sally", available_minutes_per_day=120)
    pet = Pet(name=pet_name, species="dog", age=3)
    owner.add_pet(pet)
    for t in tasks:
        pet.add_task(t)
    return Scheduler(owner), pet


def test_sort_by_time_puts_untimed_last():
    s, _ = _scheduler_with(
        Task("C", "x", 5, "low"),
        Task("B", "x", 5, "low", start_time="09:00"),
        Task("A", "x", 5, "low", start_time="07:30"),
    )
    assert [t.title for t in s.sort_by_time()] == ["A", "B", "C"]


def test_filter_by_pet_and_status():
    s, robert = _scheduler_with(Task("Walk", "x", 5, "low"), Task("Feed", "x", 5, "low"))
    mochi = Pet(name="Mochi", species="cat", age=5)
    s.owner.add_pet(mochi)
    mochi.add_task(Task("Play", "x", 5, "low"))
    robert.tasks[0].mark_complete()

    assert [t.title for t in s.filter_tasks(pet_name="Mochi")] == ["Play"]
    assert [t.title for t in s.filter_tasks(completed=True)] == ["Walk"]
    assert len(s.filter_tasks(pet_name="Robert", completed=False)) == 1


def test_daily_task_recurs_tomorrow():
    task = Task("Walk", "x", 5, "low", frequency="daily")
    _, pet = _scheduler_with(task)

    nxt = pet.complete_task(task)

    assert task.completed and not nxt.completed
    assert nxt.due_date == date.today() + timedelta(days=1)
    assert nxt in pet.tasks and nxt.pet_name == "Robert"


def test_weekly_task_recurs_in_seven_days():
    task = Task("Groom", "x", 5, "low", frequency="weekly")
    _, pet = _scheduler_with(task)

    assert pet.complete_task(task).due_date == date.today() + timedelta(days=7)


def test_once_task_does_not_recur():
    task = Task("Vet", "x", 5, "low", frequency="once")
    _, pet = _scheduler_with(task)

    assert pet.complete_task(task) is None
    assert len(pet.tasks) == 1


def test_detects_overlapping_tasks():
    s, _ = _scheduler_with(
        Task("Walk", "x", 30, "high", start_time="08:00"),
        Task("Feed", "x", 10, "high", start_time="08:15"),
    )
    assert len(s.detect_conflicts()) == 1


def test_same_start_time_is_a_conflict_across_pets():
    s, _ = _scheduler_with(Task("Walk", "x", 30, "high", start_time="08:00"))
    mochi = Pet(name="Mochi", species="cat", age=5)
    s.owner.add_pet(mochi)
    mochi.add_task(Task("Feed", "x", 10, "high", start_time="08:00"))

    warnings = s.detect_conflicts()

    assert len(warnings) == 1 and "different pets" in warnings[0]


def test_back_to_back_tasks_do_not_conflict():
    s, _ = _scheduler_with(
        Task("Walk", "x", 30, "high", start_time="08:00"),
        Task("Feed", "x", 10, "high", start_time="08:30"),
    )
    assert s.detect_conflicts() == []
