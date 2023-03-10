from Command_Macro import Command


macro = Command()

updates = macro.get_schedule_updates()
# print(updates[0])
# print(updates[1])
# print(updates[2])

# schedule_updates = [['3522', '6', [[False, ''], [False, ''], [False, ''], [False, ''], [True, '50'], [False, ''], [False, '']]], ['2520', '6', [[True, '16'], [False, ''], [True, '35'], [False, ''], [True, '50'], [False, ''], [False, '']]]]
macro.open_TRESS()
macro.select_attendance()

macro.update_schedules(updates)