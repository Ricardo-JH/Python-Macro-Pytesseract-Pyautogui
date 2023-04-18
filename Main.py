from Command_Macro import Command


macro = Command()

updates = macro.get_schedule_updates(week_offset=1)
print(updates[0])

macro.open_TRESS()
macro.select_attendance()
macro.update_schedules(updates)

print('\nFinished') 