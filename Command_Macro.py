from datetime import datetime, timedelta
from OCR_Detect import OCR
from credentials import *
import pandas as pd
import pyperclip
import pyautogui
import warnings
import pyodbc
import time


warnings.filterwarnings('ignore')


class Command:
    def __init__(self):
        pass
    
    def get_schedule_updates(self, week=None):
        start_time = time.time()

        Database = 'TRESS'
        Driver = 'ODBC Driver 17 for SQL Server'
        Server = 'SQLSERVER\GGAMASTEDDB'
        User = 'GGASOLUTIONS\ricardo.jaramillo'
        Connection_String = f'DRIVER={Driver};SERVER={Server};DATABASE={Database};UID={User};Trusted_Connection=yes;'

        connection = pyodbc.connect(Connection_String)
        
        if week == None:
            weekdate = datetime.date(datetime.now()) - timedelta(days=datetime.now().weekday())
            week = weekdate.isocalendar()[1]
        else:
            weekdate = datetime.strptime('2023-W' + str(week) + '-1', '%G-W%V-%u').strftime('%Y-%m-%d')
        
        query = f"Select * from V_schedules_daily_comparative where schedule_weekdate_TRESS = '{weekdate}'"

        data = pd.DataFrame(pd.read_sql(query, connection)).fillna('')
        data = data[['Emp', 'schedule_referenceDate_TRESS', 'schedule_daily_Genesys']]
        # data['schedule_daily_Genesys'] = data['schedule_daily_Genesys'].astype(int)
        
        elapsedTime = time.time() - start_time
        print(f'Time get data: {elapsedTime} sec') 

        connection.close()
        return data, week, weekdate


    def type(self, string, wait_time=0):
        pyperclip.copy(string)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(wait_time)
    

    def press(self, string, wait_time=0, times=1):
        for i in range(times):
            pyautogui.press(string)
            time.sleep(wait_time)
    

    def left_click(self, search, thresh=0, wait_time=0, offset_x=0, offset_y=0, psm=11):
        Detect = OCR(psm, thresh)

        img, words = Detect.get_boxes_words(pattern=search, thresh=thresh)
        
        if search in ['.', 'S?emana?']:
            Detect.show_img(img)
        
        x, y = words[0][1] + offset_x, words[0][2] + offset_y

        pyautogui.leftClick(x, y)
        time.sleep(wait_time)


    def open_TRESS(self):
        
        self.press('win', 1)
        self.type('Supervisores', 0.2)
        self.press('enter', 1.5)

        self.left_click('U?suario?:?', thresh=-100, offset_x=50) # U?suario?:?
        
        self.type(credentials['user'], 0.2)
        self.press('tab', 0.2)
        self.type(credentials['pass'], 0.2)
        self.press('enter', 3)
    

    def select_attendance(self):
        
        self.left_click('A?sistencia?', thresh=-10, wait_time=0.25)
        self.left_click('C?o?nsulta?r', thresh=-10, wait_time=0.25)


    def update_schedule(self, updates):
        
        # set start position
        self.left_click('H?abil?', thresh=-10, wait_time=0.25)
        self.press('up', times=6)
        self.press('left', times=2)

        # enter Schedule
        for update in updates:
            if update[0]:
                pyautogui.typewrite(update[1], 0.05)
                time.sleep(0.2)
            self.press('down')
        self.left_click('OK', thresh=-100, wait_time=1, psm=6)


    def update_schedules(self, df_schedule_updates):
        for emp, week, updates in emp_list:
            # enter Emp
            self.left_click('N?umero?', thresh=0, offset_x=30)
            self.type(emp, 0.2)
            self.press('enter', 1)

            # enter week number
            self.left_click('.S?emanal?', thresh=0, offset_y=25)
            pyautogui.typewrite(week, 0.05)
            time.sleep(0.2)
            self.press('enter', 1)

            self.left_click('F?echa?:?', thresh=-10, wait_time=1, offset_x=200)

            # need a list of updates for the specific Emp
            self.update_schedule(updates)
        
        pyautogui.alert('Schedules update Finish.')

            