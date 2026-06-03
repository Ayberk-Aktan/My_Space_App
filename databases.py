import io
import os 
import sqlite3 
import requests
import datetime
from PIL import Image

API_KEY = "YOUR_API_KEY"

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# * Astronomy Visual Archive (AVA) İnitial Databases and get API Data Function
"""
! In this section, some functions were performed with the help of Google Gemini.
! Using for io and Pillow library.
"""
def ava_get_data():
    ava_db_connect = sqlite3.connect(os.path.join(BASE_DIR,"astronomy_vis_arch.db")) 
    ava_db_cursor = ava_db_connect.cursor() 
    ava_db_cursor.execute("CREATE TABLE IF NOT EXISTS visuals (date text PRIMARY KEY DESC, explanation text , media_type text , title text , media blob , copyright text )") 
    
    try:
        now_date = datetime.datetime.now().strftime("%Y-%m-%d") 
        old_date = "2026-05-29"
        ava_requests = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&start_date={old_date}&end_date={now_date}")
        ava_requests.raise_for_status() 
        ava_json = ava_requests.json()  
    except Exception as e: 
        print("API İsteği Başarısız Oldu.",e) 
        ava_db_connect.close()
        return 
    
    visual_dates = [i["date"] for i in ava_json]
    visual_explanation = [j["explanation"] for j in ava_json] 
    visual_media_type = [k["media_type"] for k in ava_json] 
    visual_title = [l["title"] for l in ava_json] 
    visual_copyright = [m.get("copyright") for m in ava_json] 
    visual_image_urls = [n["url"] for n in ava_json]
    visual_image = [] 

    for i in range(len(visual_image_urls)): 
        if visual_media_type[i] == "video": 
            visual_image.append(None)
            continue
        else:
            try:
                image_respone = requests.get(visual_image_urls[i]) 
                image_respone.raise_for_status() 

                image_bytes = io.BytesIO(image_respone.content) 
                image = Image.open(image_bytes) 

                output = io.BytesIO() 
                image_format = image.format.upper() if image.format in ["JPG", "PNG", "GIF"] else "JPEG" 
                image.save(output,format=image_format)

                blob_data = output.getvalue() 

                visual_image.append(blob_data) 
            except Exception as e: 
                visual_image.append(None) 

    for i in range(len(visual_dates)): 
        values = ( 
            visual_dates[i],
            visual_explanation[i],
            visual_media_type[i],
            visual_title[i], 
            visual_image[i],
            visual_copyright[i]
        )

        ava_db_cursor.execute("INSERT OR REPLACE INTO visuals VALUES (?,?,?,?,?,?)",values)
    
    ava_db_connect.commit() 
    ava_db_connect.close() 

# * Astreoid Risk Analysis Data (ARAD) İnitial Databases and get API Function 
def arad_get_data(): 
    arad_db_connect = sqlite3.connect(os.path.join(BASE_DIR,"astreoid_risk_anaylzed.db"))
    arad_db_cursor = arad_db_connect.cursor() 

    arad_db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS 
    astreoids (
              close_date text type UNIQUE,
              astreoid_name text,
              max_diameter real, 
              min_diameter real, 
              absoulte_magnitude real, 
              min_distance_km real,
              min_distance_au real,
              speed_kmh real, 
              potentially_hazardous INTEGER CHECK (potentially_hazardous IN (0,1)),
              sentry_object INTEGER CHECK (sentry_object IN (0,1)) 
    )
    """)

    try: 
        start_date = "2026-05-18" 
        end_date = "2026-05-25"

        arad_requests = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={API_KEY}") 
        arad_requests.raise_for_status() 
        arad_json = arad_requests.json() 
    except Exception as e: 
        print("API Çekme İşlemi Başarısız",e) 
        arad_db_connect.close() 
        return 
    
    date_list = [i for i in arad_json["near_earth_objects"]]
    astreoid_names = [arad_json["near_earth_objects"][j][0]["name"] for j in date_list]
    astreoid_min_diamtr_km = [arad_json["near_earth_objects"][k][0]["estimated_diameter"]["kilometers"]["estimated_diameter_min"] for k in date_list] 
    astreoid_max_diamtr_km = [arad_json["near_earth_objects"][l][0]["estimated_diameter"]["kilometers"]["estimated_diameter_max"] for l in date_list] 
    astreoid_magnitude_h = [arad_json["near_earth_objects"][m][0]["absolute_magnitude_h"] for m in date_list] 
    astreoid_close_km = [arad_json["near_earth_objects"][n][0]["close_approach_data"][0]["miss_distance"]["kilometers"] for n in date_list]
    astreoid_close_au = [arad_json["near_earth_objects"][i][0]["close_approach_data"][0]["miss_distance"]["astronomical"] for i in date_list]
    astreoid_velo_kmh = [arad_json["near_earth_objects"][i][0]["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"] for i in date_list]
    astreoid_pot_hazard = [arad_json["near_earth_objects"][i][0]["is_potentially_hazardous_asteroid"] for i in date_list] 
    astreoid_sentries = [arad_json["near_earth_objects"][i][0]["is_sentry_object"] for i in date_list] 

    for i in range(len(date_list)): 
        values = (
            date_list[i],
            astreoid_names[i], 
            astreoid_max_diamtr_km[i],
            astreoid_min_diamtr_km[i],
            astreoid_magnitude_h[i],
            astreoid_close_km[i],
            astreoid_close_au[i],
            astreoid_velo_kmh[i],
            astreoid_pot_hazard[i],
            astreoid_sentries[i]
        )

        arad_db_cursor.execute("INSERT INTO astreoids VALUES (?,?,?,?,?,?,?,?,?,?)",values)
    
    arad_db_connect.commit() 
    arad_db_connect.close() 

# * Mars InSight Sol Monitor (MISM) İnitial Databases and get API Function 
def misim_get_data(): 
    misim_db_connect = sqlite3.connect(os.path.join(BASE_DIR,"mars_insight_sol_data.db"))
    misim_db_cursor = misim_db_connect.cursor() 
    misim_db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS mars_solars (
    solar_day text UNIQUE, 
    average_temp real, 
    minimum_temp real,
    maximum_temp real, 
    average_wind_speed real, 
    minimum_wind_speed real, 
    maximum_wind_speed real, 
    average_pressure real, 
    minimum_pressure real, 
    maximum_pressure real 
    )
    """)

    try: 
        misim_response = requests.get(f"https://api.nasa.gov/insight_weather/?api_key={API_KEY}&feedtype=json&ver=1.0")
        misim_response.raise_for_status() 
        misim_json = misim_response.json() 
    except Exception as e: 
        print("API Çekme İşlemi Başarısız",e) 
        misim_db_connect.close() 
        return 

    sol_days = [i for i in misim_json][:-2]
    average_temp = [misim_json[f"{i}"]["AT"]["av"] for i in sol_days]
    minimum_temp = [misim_json[f"{i}"]["AT"]["mn"] for i in sol_days] 
    maximum_temp = [misim_json[f"{i}"]["AT"]["mx"] for i in sol_days] 
    average_wind_speed = [misim_json[f"{i}"]["HWS"]["av"] for i in sol_days] 
    minimum_wind_speed = [misim_json[f"{i}"]["HWS"]["mn"] for i in sol_days]
    maximum_wind_speed = [misim_json[f"{i}"]["HWS"]["mx"] for i in sol_days] 
    average_pressure = [misim_json[f"{i}"]["PRE"]["av"] for i in sol_days] 
    minimum_pressure = [misim_json[f"{i}"]["PRE"]["mn"] for i in sol_days]
    maximum_pressure = [misim_json[f"{i}"]["PRE"]["mx"] for i in sol_days]
    
    for i in range(len(sol_days)): 
        values = (
            sol_days[i],
            average_temp[i],
            minimum_temp[i],
            maximum_temp[i],
            average_wind_speed[i],
            minimum_wind_speed[i],
            maximum_wind_speed[i],
            average_pressure[i],
            minimum_pressure[i],
            maximum_pressure[i]
        )    

        misim_db_cursor.execute("INSERT OR REPLACE INTO mars_solars VALUES (?,?,?,?,?,?,?,?,?,?)",values)

    misim_db_connect.commit() 
    misim_db_connect.close() 

   







    



