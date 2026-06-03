import os
import sqlite3 
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# * Astreoid Risk Analysis Dashboard (ARAD) Object and Data Processing Classes
"""
! For information on using the SQL between command, I consulted W3CSchools, and for some errors, I consulted Google Gemini.
"""
class Arad: 
    def __init__(self):
        self.astreoid_names = []
        self.max_diameters = []
        self.min_diameters = []
        self.absoulte_magn = []
        self.speed = []
        self.potential_hazrd = []

        self.all_speed = [] 
        self.all_max_diameters = [] 
        self.all_min_diameters = []
        self.all_magnitude = []

    def get_data(self): 
        arad_db_connect = sqlite3.connect(os.path.join(BASE_DIR,"astreoid_risk_anaylzed.db"))
        arad_db_cursor = arad_db_connect.cursor() 
    
        last_10_days_data = arad_db_cursor.execute("SELECT * FROM astreoids WHERE close_date BETWEEN '2026-05-14' AND '2026-05-24'")  
    
        all_data = last_10_days_data.fetchall()
      
        self.astreoid_names = [i[1] for i in all_data] 
        self.max_diameters = [i[2] for i in all_data] 
        self.min_diameters = [i[3] for i in all_data] 
        self.absoulte_magn = [i[4] for i in all_data] 
        self.min_distance = [i[5] for i in all_data] 
        self.speed = [i[7] for i in all_data] 

        arad_db_connect.close() 
    
    def get_all_data(self): 
        arad_db_connect2 = sqlite3.connect(os.path.join(BASE_DIR,"astreoid_risk_anaylzed.db")) 
        arad_db_cursor2 = arad_db_connect2.cursor() 

        all_data = arad_db_cursor2.execute("SELECT * FROM astreoids WHERE close_date") 

        all_data_fetchs = all_data.fetchall() 
        
        self.all_speed = [i[7] for i in all_data_fetchs] 
        self.all_max_diameters = [i[2] for i in all_data_fetchs] 
        self.all_min_diameters = [i[3] for i in all_data_fetchs] 
        self.all_magnitude = [i[4] for i in all_data_fetchs]
        self.potential_hazrd = [i[8] for i in all_data_fetchs]

        arad_db_connect2.close()

# * Mars InSight Sol Monitor (MISM) Object and Data Processing Classes 
class Mism: 
    def __init__(self): 
        self.sol_days = [] 
        self.av_temp = [] 
        self.min_temp = [] 
        self.max_temp = [] 
        self.av_wind_speed = [] 
        self.min_wind_speed = [] 
        self.max_wind_speed = [] 
        self.av_pre = [] 
        self.min_pre = [] 
        self.max_pre = [] 

    def mism_get_all_data(self): 
        mism_connect_db = sqlite3.connect(os.path.join(BASE_DIR,"mars_insight_sol_data.db"))
        mism_cursor = mism_connect_db.cursor() 

        all_mism_data = mism_cursor.execute("SELECT * FROM mars_solars WHERE solar_day") 
        all_misim_data_fetchs = all_mism_data.fetchall() 

        self.sol_days = [i[0] for i in all_misim_data_fetchs] 
        self.av_temp = [i[1] for i in all_misim_data_fetchs] 
        self.min_temp = [i[2] for i in all_misim_data_fetchs] 
        self.max_temp = [i[3] for i in all_misim_data_fetchs] 
        self.av_wind_speed = [i[4] for i in all_misim_data_fetchs] 
        self.min_wind_speed = [i[5] for i in all_misim_data_fetchs] 
        self.max_wind_speed = [i[6] for i in all_misim_data_fetchs] 
        self.av_pre = [i[7] for i in all_misim_data_fetchs] 
        self.min_pre = [i[8] for i in all_misim_data_fetchs] 
        self.max_pre = [i[9] for i in all_misim_data_fetchs] 

        mism_connect_db.close() 


   
   


