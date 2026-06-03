import io 
import os
import joblib
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
from tkinter import * 
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt 
from databases import ava_get_data
from data_processing import Arad , Mism
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# * Import the Model 
"""
! Google Gemini was used to assist in importing the model.
"""
model_path = os.path.join(BASE_DIR,"astreoid_impact_classification_models","model.pkl")
load_model = None

try:
    if os.path.exists(model_path):
        load_model = joblib.load(model_path) 
    else:
        raise FileNotFoundError
except FileNotFoundError: 
    messagebox.showerror(title="Sistem Hatası",message="Astreoid Risk Hesaplama Tahmin Modeli Bulunamadı!") 

# * Main Window Configures
window = Tk() 
window.geometry("1000x600") 
window.title("My Space App") 
window_icon = PhotoImage(file=os.path.join(BASE_DIR,"icon.png")) 
window.iconphoto(True,window_icon)

# * Menubar Options
options = Frame(window,bg="#c7c3c3") 
options.pack() 
options.pack_propagate(False) 
options.configure(width=1000,height=30) 

# * Switch Function
def switch(page): 
    for fm in main_frame.winfo_children(): 
        fm.destroy() 
        window.update() 

    page()

# * Button Command Functions 
# * Welcome Menu Function
def welcome(): 
    welcome_frame = Frame(main_frame,bg="#0B132B")

    welcome_sub_frame = Frame(welcome_frame,width=850,height=600,bg="#0B132B") 
    welcome_sub_frame.pack(padx=50,pady=20) 

    main_title = Label(welcome_sub_frame,text="Hoşgeldiniz",justify=CENTER,bg="#0B132B",font=("Open Sans",18),fg="white") 
    main_title.pack()

    first_sub_title = Label(welcome_sub_frame,text="Projenin Temel Amacı",justify=LEFT,bg="#0B132B",font=("Open Sans",12),fg="white")
    first_sub_title.pack(pady=5,anchor=W)

    first_text = Label(
        welcome_sub_frame,
        text = """
        Bu projenin temel amacı; NASA API ile kapsamlı bir Uzay Yönetim ve Analiz Paneli (Space Management & Analysis Dashboard) geliştirmektir. 
        Uygulama, uzay bilimleri verilerinin yerel bir veritabanında optimize edilmiş şekilde depolanmasını, tarihsel değişimlerin istatistiksel 
        grafiklerle görselleştirilmesini ve makine öğrenmesi algoritmalarıyla risk tahmini yapılmasını hedefleyen multi-disipliner bir yazılım çalışmasıdır.
        Projenin kapsamı ve arayüz menüleri şu üç ana modülden oluşmaktadır.
        """,
        wraplength=825,
        bg="#0B132B",
        fg="white",
        justify=LEFT
    ) 

    first_text.pack()
    
    second_text = Label(
        welcome_sub_frame,
        text = """
        Astronomi Görsel Arşivi (AVA): NASA APOD (Astronomy Picture of the Day) API'si kullanılarak geliştirilen bu modül, 
        29.05.2025 – 30.05.2026 tarihleri arasındaki (son bir yıllık) astronomi görsel materyallerini ve bilimsel açıklamalarını yerel SQLite veritabanında saklar 
        ve listeler. Kullanıcılar, arayüzde yer alan dinamik Listbox bileşeni üzerinden diledikleri tarihi seçerek, o güne ait yüksek çözünürlüklü görsel içeriğe, 
        başlık, telif hakkı ve detaylı literatür açıklamalarına gecikmesiz olarak erişebilmektedir.
        """,
        wraplength=825,
        bg="#0B132B",
        fg="white",
        justify=LEFT
    ) 

    second_text.pack()

    third_text = Label(
        welcome_sub_frame,
        text = """
        Asteroit Risk Analiz Paneli (ARAD): NASA NeoWS (Near Earth Object Web Service) API verilerini temel alan bu panel, dünyanın yakınından geçen 
        asteroitlerin son bir yıllık fiziksel ve yörüngesel verilerini istatistiksel grafiklerle analiz eder. Panel bünyesinde yer alan "Risk Hesaplama 
        Penceresi" (Toplevel),arka planda çalışan bir Makine Öğrenmesi Sınıflandırma Modeli (Random Forest) ile entegre edilmiştir. Kullanıcı tarafından 
        arayüze girilen asteroit parametreleri (maksimum/minimum çap, mutlak parlaklık, hız, minimum uzaklık ve sentry durumu) doğrultusunda model, 
        ilgili gök cisminin potansiyel tehlike durumunu (Pozitif/Negatif) sınıflandırır ve çarpma olasılığını yüzde bazında hesaplar.
        """,
        wraplength=825,
        bg="#0B132B",
        fg="white",
        justify=LEFT
    ) 

    third_text.pack()

    third_text = Label(
        welcome_sub_frame,
        text = """
        Mars InSight Sol Monitörü: NASA InSight Mars uzay aracının Sol 675 ile Sol 681 günleri arasında kızıl gezegenden topladığı anlık atmosferik verileri işler. 
        Bu modül; Mars yüzeyindeki sıcaklık (°C), rüzgar hızı (m/s) ve açık hava basıncı (Pa) değerlerinin haftalık ve günlük bazdaki değişimlerini, 
        Matplotlib ve Seaborn kütüphaneleri aracılığıyla gelişmiş sekmeli grafik panelleri halinde kullanıcıya sunar.
        """,
        wraplength=825,
        bg="#0B132B",
        fg="white",
        justify=LEFT
    ) 

    third_text.pack()

    signature = Label(welcome_sub_frame,text="2026 Made By Ayberk Aktan",justify=CENTER,bg="#0B132B",fg="white") 
    signature.pack(side=BOTTOM,anchor=S,pady=5)

    welcome_frame.pack(fill=BOTH,expand=True) 

# * Astronomy Picture of the Day / Astronomy Visual Archive Frame
"""
! This function utilizes Google Gemini for displaying images from the database.
"""
def apod_frame(): 
    apod_frames = Frame(main_frame,bg="#4D96FF") 

    connect_ava_db = sqlite3.connect(os.path.join(BASE_DIR,"astronomy_vis_arch.db")) 
    cursor_ava_db = connect_ava_db.cursor() 

    ava_date_data = cursor_ava_db.execute("SELECT date FROM visuals") 
    date_data =[row[0] for row in ava_date_data.fetchall()[::-1]]

    list_box = Listbox(apod_frames,height=85,width=20) 
    list_box.pack(side=LEFT,padx=20,pady=60) 

    for i in range(len(date_data)): 
        list_box.insert(i,date_data[i])
    
    image_frame = Frame(apod_frames,width=400,height=300) 
    image_frame.pack(side=LEFT,anchor=NW,padx=20,pady=60)

    info_frame = Frame(apod_frames,width=400,height=375,bg="white") 
    info_frame.pack(side=TOP,anchor=NE,padx=10,pady=60) 
    info_frame.pack_propagate(False)

    firstly_label = Label(
        info_frame,
        text="Astronomi Görsel Arşive Hoşgeldiniz!\n\nLütfen yan taraftan tarih seçip o tarih ile ilgili görsel materyal ve bilgilerini keşfediniz !",
        width=400,
        wraplength=375,
        justify=CENTER,
        bg="white",
        font=("Trebuchet MS",18)
    ) 
    firstly_label.pack(side=TOP,pady=75)

    title_label = Label(info_frame,text="",bg="white",font=("Georgia",10)) 
    title_label.pack(padx=10,pady=5,anchor=W) 

    copyrights_label = Label(info_frame,text="",bg="white") 
    copyrights_label.pack(padx=10,anchor=W)

    explains_label = Label(info_frame,text="",width=400,wraplength=350,justify=LEFT,bg="white") 
    explains_label.pack(padx=10,anchor=W)

    image_frame.pack_propagate(False) 

    image_label = Label(image_frame,bg="#4D96FF") 
    image_label.pack(side=TOP,fill=BOTH,expand=True) 

    # * Select Date Button Command Function
    def select_date(): 
        if not list_box.curselection(): 
            messagebox.showwarning(title="Tarih Seçimi Uyarısı",message="Lütfen Tarih Seçmeden Gönder Butonuna Basmayınız!")
        else:
            firstly_label.destroy() 

            for i in list_box.curselection():
                get_date = list_box.get(i)
                
                mini_connect = sqlite3.connect(os.path.join(BASE_DIR,"astronomy_vis_arch.db")) 
                mini_cursor = mini_connect.cursor() 

                target_data = mini_cursor.execute("SELECT * FROM visuals WHERE date = ?",(get_date,))
                target_data_row = target_data.fetchone()

                if target_data_row:
                    try:
                        image_col = target_data_row[4] 
                        
                        image_data = io.BytesIO(image_col) 
                        img = Image.open(image_data) 
                        img = img.resize((400,300),Image.Resampling.LANCZOS) 
                        tk_img = ImageTk.PhotoImage(img) 

                        image_label.config(image=tk_img) 
                        image_label.image = tk_img
                    except Exception as e: 
                        messagebox.showwarning(title="Uyarı !",message="Üzgünüm Bu tarihteki görsel materyal gösterilememektir!")
                    
                    titles = target_data_row[3] 
                    types = target_data_row[2]
                    copyrights = target_data_row[5]
                    explains = target_data_row[1] 

                    title_label.config(text=titles)
                
                    if copyrights: 
                        copyrights_label.config(text=f"{copyrights}") 
                    else:
                        copyrights_label.config(text="Anonim") 

                    explains_label.config(text=explains)

                mini_connect.close()
        
    select_button = Button(apod_frames,text="Gönder",width=15,height=1,command=select_date,font=("Open Sans",10),cursor="hand1") 
    select_button.pack(side=RIGHT,anchor=SE,padx=10,pady=10)
      
    apod_frames.pack(fill=BOTH,expand=True)

    connect_ava_db.close()

# * Astreoid Neows / Astreoid Risk Analysis Dashboard (ARAD) 
def astreoid_nws_frame(): 
    astreoid_nws_frames = Frame(main_frame,bg="#1A1F36") 
    
    title_frame = Frame(astreoid_nws_frames,width=1000,bg="#1A1F36") 
    title_frame.grid(row=0,column=0)

    main_label = Label(title_frame,text="Astreoid Risk Analiz Paneli",justify=LEFT,font=("Trebuchet MS",18),bg="#1A1F36",fg="white") 
    main_label.grid(row=0,column=0,padx=60)

    plot_tabs = ttk.Notebook(astreoid_nws_frames) 

    plot_1 = Frame(plot_tabs,width=1000,height=485,bg="#1A1F36") 
    plot_2 = Frame(plot_tabs,width=1000,height=485,bg="#1A1F36") 
    plot_3 = Frame(plot_tabs,width=1000,height=485,bg="#1A1F36") 
    plot_4 = Frame(plot_tabs,width=1000,height=485,bg="#1A1F36") 
    plot_5 = Frame(plot_tabs,width=1000,height=485,bg="#1A1F36")

    plot_tabs.add(plot_1,text="Astreoid Çap Analizi") 
    plot_tabs.add(plot_2,text="Astreoid Parlaklığı") 
    plot_tabs.add(plot_3,text="Astreoid Tehlike Dağlımı") 
    plot_tabs.add(plot_4,text="Ortalama Çap ve Hız İlişki Dağılımı")
    plot_tabs.add(plot_5,text="Astreoid Parlaklık ve Hız Dağılımı") 

    (fig1,ax1) = plt.subplots(figsize=(10,4.85),dpi=100) 

    canvas_1 = FigureCanvasTkAgg(fig1,master=plot_1) 
    canvas_1.get_tk_widget().pack() 
    
    (fig2,ax2) = plt.subplots(figsize=(10,4.85),dpi=100) 

    canvas_2 = FigureCanvasTkAgg(fig2,master=plot_2) 
    canvas_2.get_tk_widget().pack() 

    (fig3,ax3) = plt.subplots(figsize=(10,4.85),dpi=100) 

    canvas_3 = FigureCanvasTkAgg(fig3,master=plot_3) 
    canvas_3.get_tk_widget().pack() 

    (fig4,ax4) = plt.subplots(figsize=(10,4.85),dpi=100)
    
    canvas_4 = FigureCanvasTkAgg(fig4,master=plot_4) 
    canvas_4.get_tk_widget().pack() 

    (fig5,ax5) = plt.subplots(figsize=(10,4.85),dpi=100)
    
    canvas_5 = FigureCanvasTkAgg(fig5,master=plot_5) 
    canvas_5.get_tk_widget().pack() 
    
    def plot(): 
        arad_data = Arad() 
        arad_data.get_data() 
        arad_data.get_all_data()

        ax1.barh(arad_data.astreoid_names,arad_data.max_diameters) 
        ax1.barh(arad_data.astreoid_names,arad_data.min_diameters)
        ax1.set_ylabel("Astreoid Adları") 
        ax1.tick_params(axis="y",rotation=45,labelsize=6)
        ax1.set_xlabel("Çap (km)") 
        ax1.set_title("Astreoidlerin Çap Karşılaştırması (Son 10 Gün)")
        ax1.legend(["Maksimum Çap","Minimum Çap"],loc=1)
        canvas_1.draw() 

        ax2.barh(arad_data.astreoid_names,arad_data.absoulte_magn,color="green") 
        ax2.set_ylabel("Astreoid Adları") 
        ax2.set_xlabel("Astreoid Parlaklığı") 
        ax2.set_title("Astreoidlerin Parlaklık Şiddeti Karşılaştırması (Son 10 Gün)")
        ax2.tick_params(axis="y",rotation=45,labelsize=6)
        ax2.legend(["Astreoid Parlaklıkları"])
        canvas_2.draw()

        sns.histplot(arad_data.potential_hazrd,bins=2,ax=ax3)
        ax3.set_ylabel("Astreoid Sayısı") 
        ax3.set_xlabel("Astreoid Tehlike Durumu") 
        ax3.set_title("Astreoidlerin Tehlike Dağlımı (Bütün Astreoidler)") 
        canvas_3.draw()
        
        average_diameter = (np.array(arad_data.all_max_diameters) + np.array(arad_data.all_min_diameters)) / 2
        ax4.scatter(arad_data.all_speed,average_diameter) 
        ax4.set_title("Ortalama Çap ve Hız Dağlımı (Bütün Astreoidler)") 
        ax4.set_xlabel("Hız (kmh)")
        ax4.set_ylabel("Ortalam Çap (km)") 
        canvas_4.draw()

        ax5.scatter(arad_data.all_magnitude,arad_data.all_speed,color="#98d169") 
        ax5.set_title("Astreoid Parlaklık ve Hız Dağlımı (Bütün Astreoidler)") 
        ax5.set_xlabel("Asteoid Parlaklığı (h)") 
        ax5.set_ylabel("Astreoid Hızı (kmh)") 
        canvas_5.draw()
    
    plot()
    
    plot_tabs.grid(row=1,column=0)
    
    # * Predict Risk Window Function
    def predict_window():
        new_window = Toplevel() 
        new_window.title("Risk Hesaplama (My Space App)")
        new_window.geometry("400x400")
        new_window.config(background="#1A1F36")

        input_frame = Frame(new_window,bg="#1A1F36") 
        input_frame.grid(row=0,column=0,padx=45,pady=15) 

        max_diameter_label = Label(input_frame,text="Maksimum Çap (km)",bg="#1A1F36",fg="white") 
        max_diameter_label.grid(row=0,column=0,pady=10) 

        max_diameter_input = Entry(input_frame,width=30) 
        max_diameter_input.grid(row=0,column=1,pady=10) 

        min_diameter_label = Label(input_frame,text="Minimum Çap (km)",bg="#1A1F36",fg="white") 
        min_diameter_label.grid(row=1,column=0,pady=10) 

        min_diameter_input = Entry(input_frame,width=30) 
        min_diameter_input.grid(row=1,column=1,pady=10) 

        abs_magnitude_label = Label(input_frame,text="Mutlak Parlaklık (h)",bg="#1A1F36",fg="white") 
        abs_magnitude_label.grid(row=2,column=0,pady=10) 

        abs_magnitude_input = Entry(input_frame,width=30) 
        abs_magnitude_input.grid(row=2,column=1,pady=10)

        min_distance_label = Label(input_frame,text="Minimum Uzaklık (AU)",bg="#1A1F36",fg="white") 
        min_distance_label.grid(row=3,column=0,pady=10) 

        min_distance_input = Entry(input_frame,width=30) 
        min_distance_input.grid(row=3,column=1,pady=10) 

        speed_label = Label(input_frame,text="Astreoid Hızı (km/h)",bg="#1A1F36",fg="white") 
        speed_label.grid(row=4,column=0,pady=10) 

        speed_input = Entry(input_frame,width=30) 
        speed_input.grid(row=4,column=1,pady=10)

        var = IntVar() 
        is_sentry_variable = None 

        def attach_variable():
            is_sentry_variable = var.get()
        
        """
        ! Google Gemini was used to assist in using the imported model.
        """
        def calculate_risk():
            try:
                max_diameter = float(max_diameter_input.get().strip())
                min_diameter = float(min_diameter_input.get().strip())
                abs_magnitude = float(abs_magnitude_input.get().strip())
                min_distance = float(min_distance_input.get().strip())
                speed = float(speed_input.get().strip())

                df = pd.DataFrame(
                    [[max_diameter,min_diameter,abs_magnitude,min_distance,speed,is_sentry_variable]],
                    columns=["max_diameter","min_diameter","absoulte_magnitude","min_distance_au","speed_kmh","sentry_object"]
                ) 

                prediction = load_model.predict(df)[0] 
                prediction_proballity = load_model.predict_proba(df)[0][1]
            except Exception as e: 
                messagebox.showerror(title="Tahmin Hesaplama Hatası!",message="Lütfen Alanları Boş Bırakmayınız ve Girdileri Doğru Giriniz!") 
                print(e)
            else:
                output_frame = Frame(new_window,bg="#1A1F36",width=400,height=100)
                output_frame.grid(row=1,column=0)

                prediction_title_label = Label(output_frame,text="Tehlike Durumu : ",bg="#1A1F36",fg="white",font=("Segoe UI Mono",15)) 
                prediction_title_label.grid(row=0,column=0)

                prediction_main_label = Label(output_frame,text="",bg="#1A1F36",fg="white",font=("Segoe UI Mono",15))
                prediction_main_label.grid(row=0,column=1) 

                proballity_title_label = Label(output_frame,text="Tehlike Olasılığı : ",bg="#1A1F36",fg="white",font=("Segoe UI Mono",15)) 
                proballity_title_label.grid(row=1,column=0) 

                proballity_main_label = Label(output_frame,text=f"%{(prediction_proballity * 100):.2f}",bg="#1A1F36",fg="white",font=("Segoe UI Mono",15)) 
                proballity_main_label.grid(row=1,column=1)

                if prediction == 0: 
                    prediction_main_label.config(text="Negatif") 
                
                if prediction == 1:
                    prediction_main_label.config(text="Pozitif") 
                
                proballity_main_label.config(text=f"%{(prediction_proballity * 100):.2f}")

        is_sentry_label = Label(input_frame,text="Takibe Alınma Durumu",bg="#1A1F36",fg="white")
        is_sentry_label.grid(row=5,column=0,pady=10) 

        is_sentry_check = Checkbutton(input_frame,variable=var,command=attach_variable,bg="#1A1F36",activebackground="#1A1F36")  
        is_sentry_check.grid(row=5,column=1,pady=10)

        submit_btn = Button(input_frame,text="Gönder",command=calculate_risk,cursor="hand1") 
        submit_btn.grid(row=7,column=1,pady=10) 

        attach_variable() 

    impact_prediction_btn = Button(title_frame,text="Risk Hesapla",width=15,height=1,font=("Open Sans",15),command=predict_window,cursor="hand1")  

    impact_prediction_btn.grid(row=0,column=1,pady=10,padx=40) 

    astreoid_nws_frames.pack(fill=BOTH,expand=True)

# * Insight Mars Function
def insight_mars(): 
    insight_mars_frames = Frame(main_frame,bg="#CD853F") 
    
    main_title = Label(insight_mars_frames,text="Mars InSight Sol Monitör",justify=CENTER,bg="#CD853F",fg="white",font=("Trebuchet MS",18)) 
    main_title.grid(row=0,column=0,padx=375) 

    plot_tabs = ttk.Notebook(insight_mars_frames) 

    plot_1 = Frame(plot_tabs,width=1000,height=545,bg="#CD853F") 
    plot_2 = Frame(plot_tabs,width=1000,height=545,bg="#CD853F") 
    plot_3 = Frame(plot_tabs,width=1000,height=545,bg="#CD853F") 
   
    plot_tabs.add(plot_1,text="Sıcaklık Analizi") 
    plot_tabs.add(plot_2,text="Rüzgar Analizi") 
    plot_tabs.add(plot_3,text="Basınç Analizi") 
   
    (fig1,ax1) = plt.subplots(figsize=(10,4.85),dpi=100) 

    canvas_1 = FigureCanvasTkAgg(fig1,master=plot_1) 
    canvas_1.get_tk_widget().pack() 
    
    (fig2,ax2) = plt.subplots(figsize=(10,4.85),dpi=100) 

    canvas_2 = FigureCanvasTkAgg(fig2,master=plot_2) 
    canvas_2.get_tk_widget().pack() 

    (fig3,ax3) = plt.subplots(figsize=(10,4.85),dpi=100) 

    canvas_3 = FigureCanvasTkAgg(fig3,master=plot_3) 
    canvas_3.get_tk_widget().pack() 

    plot_tabs.grid(row=1,column=0) 

    def plots(): 
        misim_data = Mism() 
        misim_data.mism_get_all_data() 

        plt.close("all")
        
        ax1.plot(misim_data.sol_days,misim_data.max_temp) 
        ax1.plot(misim_data.sol_days,misim_data.av_temp)
        ax1.plot(misim_data.sol_days,misim_data.min_temp) 
        ax1.set_title("Haftalık Sıcaklık Değişimi (Sol Ölçeği)")
        ax1.set_xlabel("Sol Günleri") 
        ax1.set_ylabel("Sıcaklık (°C)")
        ax1.legend(["Maksimum Sıcaklık","Ortalama Sıcaklık","Minimum Sıcaklık"],loc=0)
        canvas_1.draw()  

        ax2.plot(misim_data.sol_days,misim_data.max_wind_speed) 
        ax2.plot(misim_data.sol_days,misim_data.av_wind_speed) 
        ax2.plot(misim_data.sol_days,misim_data.min_wind_speed) 
        ax2.set_title("Haftalık Rüzgar Hızı Değişimi (Sol Ölçeği)") 
        ax2.set_xlabel("Sol Günleri") 
        ax2.set_ylabel("Rüzgar Hızı (m/s)") 
        ax2.legend(["Maksimum Hız","Ortalama Hız","Minimum Hız"]) 
        canvas_2.draw()

        ax3.plot(misim_data.sol_days,misim_data.max_pre) 
        ax3.plot(misim_data.sol_days,misim_data.av_pre) 
        ax3.plot(misim_data.sol_days,misim_data.min_pre) 
        ax3.set_title("Haftalık Basınç Değişimleri (Sol Ölçeği)") 
        ax3.set_xlabel("Sol Günleri") 
        ax3.set_ylabel("Basınç (Pa)") 
        ax3.legend(["Maksimum Basınç","Ortalama Basınç","Minimum Basınç"]) 
        canvas_3.draw()
    
    plots()

    insight_mars_frames.pack(fill=BOTH,expand=True)


# * Menubar Buttons
welcome_btn = Button(
    options, 
    text="Hoşgeldiniz",
    font=("Segoe UI",10),
    bd = 0,
    cursor="hand1",
    command=(lambda : switch(welcome))
)
welcome_btn.place(x=0,y=0,width=200,height=27)

apod_btn = Button(
    options, 
    text="Astronomi Görsel Arşivi",
    font=("Segoe UI",10),
    bd = 0,
    cursor="hand1",
    command=(lambda : switch(apod_frame))
)
apod_btn.place(x=200,y=0,width=200,height=27)

astreoid_neows_btn = Button(
    options, 
    text="Asteroid Risk Paneli",
    font=("Segoe UI",10),
    bd = 0,
    cursor="hand1",
    command=(lambda : switch(astreoid_nws_frame))
)
astreoid_neows_btn.place(x=400,y=0,width=200,height=27)

insight_mars_data_btn = Button(
    options, 
    text="Mars InSight Sol Monitör",
    font=("Segoe UI",10),
    bd = 0,
    cursor="hand1",
    command=(lambda : switch(insight_mars))
)
insight_mars_data_btn.place(x=600,y=0,width=200,height=27)

# * Main Frame 
main_frame = Frame(window) 
main_frame.pack(fill=BOTH,expand=True)

welcome()
window.mainloop()
