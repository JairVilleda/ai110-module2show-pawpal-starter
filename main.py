from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Alex", available_time=90)

buddy = Pet(name="Buddy", species="Dog", age=4)
mochi = Pet(name="Mochi", species="Cat", age=2)

# Tasks for Buddy
buddy.add_task(Task(title="Morning Walk",    duration=30, priority=3, pet_name="Buddy", preferred_time="morning"))
buddy.add_task(Task(title="Feeding",         duration=10, priority=3, pet_name="Buddy", preferred_time="morning"))
buddy.add_task(Task(title="Grooming",        duration=40, priority=1, pet_name="Buddy"))

# Tasks for Mochi
mochi.add_task(Task(title="Playtime",        duration=20, priority=2, pet_name="Mochi", preferred_time="morning"))
mochi.add_task(Task(title="Litter Cleaning", duration=15, priority=2, pet_name="Mochi"))

owner.add_pet(buddy)
owner.add_pet(mochi)

# --- Schedule ---
scheduler = Scheduler(owner=owner)
scheduler.generate_plan(current_time_block="morning")

# --- Output ---
print("=" * 40)
print("        Today's Schedule")
print("=" * 40)

for task in scheduler.get_plan():
    print(f"  {task}")

print()
print("--- Scheduler Decisions ---")
for note in scheduler.explain_plan():
    print(f"  {note}")

print()
print("--- Conflict Warnings ---")
warnings = scheduler.detect_conflicts()
if warnings:
    for w in warnings:
        print(f"  WARNING: {w}")
else:
    print("  No conflicts detected.")

print("=" * 40)
