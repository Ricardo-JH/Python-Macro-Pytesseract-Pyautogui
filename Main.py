from Command_Macro import Command

macro = Command()

macro.open_TRESS()
macro.select_attendance()

emp_list = [['3522', '6', [[False, ''], [False, ''], [False, ''], [False, ''], [True, '50'], [False, ''], [False, '']]], ['2520', '6', [[True, '16'], [False, ''], [True, '35'], [False, ''], [True, '50'], [False, ''], [False, '']]]]
macro.update_schedules(emp_list)
