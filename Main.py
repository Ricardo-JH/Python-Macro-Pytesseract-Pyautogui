from Command_Macro import Command


macro = Command()

updates = macro.get_schedule_updates()

macro.open_TRESS()
macro.select_attendance()

macro.update_schedules(updates)