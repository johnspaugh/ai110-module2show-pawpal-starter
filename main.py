from pawpal_system import Task, Pet, Owner, Scheduler


def main() -> None:
    # Owner with 90 minutes available today
    owner = Owner(name="Sally", available_minutes_per_day=90)

    # Two pets
    robert = Pet(name="Robert", species="dog", age=3)
    mochi = Pet(name="Mochi", species="cat", age=5)
    owner.add_pet(robert)
    owner.add_pet(mochi)

    # Tasks with different durations and priorities
    robert.add_task(Task("Morning walk", "exercise", 30, "high", start_time="08:00"))
    robert.add_task(
        Task("Grooming", "care", 45, "low", frequency="weekly", start_time="17:00")
    )
    mochi.add_task(Task("Feeding", "food", 10, "high", start_time="08:15"))
    # Same start time as Morning walk (different pet) and as each other (same pet)
    mochi.add_task(Task("Brushing", "care", 5, "low", start_time="08:15"))
    robert.add_task(Task("Heartworm pill", "health", 5, "high", start_time="08:00"))
    mochi.add_task(Task("Playtime", "enrichment", 20, "medium", start_time="07:30"))
    mochi.add_task(Task("Flea medication", "health", 5, "high", frequency="monthly"))

    scheduler = Scheduler(owner)
    scheduler.generate_daily_plan()

    used = sum(t.duration_minutes for t in scheduler.plan)

    print("=" * 52)
    print(f"  Today's Schedule for {owner.name}")
    print(f"  Pets: {', '.join(p.name for p in owner.pets)}")
    print(f"  Time used: {used} of {owner.available_minutes_per_day} min")
    print("=" * 52)

    print(f"{'#':<3}{'Pet':<9}{'Task':<18}{'Min':>4}  {'Priority':<9}{'Repeats'}")
    print("-" * 52)
    for n, t in enumerate(scheduler.plan, start=1):
        print(
            f"{n:<3}{t.pet_name:<9}{t.title:<18}{t.duration_minutes:>4}  "
            f"{t.priority:<9}{t.frequency}"
        )

    if scheduler.skipped:
        print("-" * 52)
        print("Skipped (not enough time):")
        for t in scheduler.skipped:
            print(f"  - {t.pet_name}: {t.title} ({t.duration_minutes} min, {t.priority})")

    print()
    print(scheduler.explain_plan())

    print("\nSorted by time:")
    for t in scheduler.sort_by_time():
        print(f"  {t.start_time or '--:--'}  {t.pet_name}: {t.title}")

    print("\nMochi's tasks only:")
    for t in scheduler.filter_tasks(pet_name="Mochi"):
        print(f"  {t.title}")

    grooming = robert.tasks[1]
    nxt = robert.complete_task(grooming)
    print(f"\nCompleted '{grooming.title}'; next one due {nxt.due_date}")
    print("Pending after completion:", len(scheduler.filter_tasks(completed=False)))

    print("\nConflict check:")
    conflicts = scheduler.detect_conflicts()
    print("\n".join(f"  {c}" for c in conflicts) or "  none")


if __name__ == "__main__":
    main()
