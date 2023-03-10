from Command_Macro import Command


macro = Command()

df_schedule_updates, week, weekdate = macro.get_schedule_updates()
print(df_schedule_updates)
print(week)
print(weekdate)

'''
schedule_updates = [['3522', '6', [[False, ''], [False, ''], [False, ''], [False, ''], [True, '50'], [False, ''], [False, '']]], ['2520', '6', [[True, '16'], [False, ''], [True, '35'], [False, ''], [True, '50'], [False, ''], [False, '']]]]
macro.open_TRESS()
macro.select_attendance()
'''

# macro.update_schedules(df_schedule_updates)