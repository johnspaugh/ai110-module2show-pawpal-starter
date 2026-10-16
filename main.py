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
    robert.add_task(Task("Morning walk", "exercise", 30, "high"))
    robert.add_task(Task("Grooming", "care", 45, "low", frequency="weekly"))
    mochi.add_task(Task("Feeding", "food", 10, "high"))
    mochi.add_task(Task("Playtime", "enrichment", 20, "medium"))
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


if __name__ == "__main__":
    main()
