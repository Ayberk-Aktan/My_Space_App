<h3>🛰️ My Space App </h3>
<hr> 
<h5>❓ Proje Hakkında</h5> 
<p> 
 Bu projenin temel amacı; NASA API ile kapsamlı bir Uzay Yönetim ve Analiz Paneli (Space Management & Analysis Dashboard) geliştirmektir. Ayrıca Trakya   Üniversitesi Bilgisayar Mühendisliği Programlama Dillerine Giriş dersi dönem sonu ödevi için geliştirilen uygulama, uzay bilimleri verilerinin yerel bir veritabanında optimize edilmiş şekilde depolanmasını, tarihsel değişimlerin istatistiksel grafiklerle görselleştirilmesini ve makine öğrenmesi algoritmalarıyla risk tahmini yapılmasını hedefleyen multi-disipliner bir yazılım çalışmasıdır. Projenin kapsamı ve arayüz menüleri şu üç ana modülden oluşmaktadır.
</p>
<hr>
<h5>🎨 Projenin Özellikleri</h5>
<p> 
<ul> 
  <li> 
      <b>🔭 Astronomi Görsel Arşivi (AVA):</b> NASA APOD (Astronomy Picture of the Day) API'si kullanılarak geliştirilen bu modül, 
      29.05.2025 – 30.05.2026 tarihleri arasındaki (son bir yıllık) astronomi görsel materyallerini ve bilimsel açıklamalarını yerel SQLite veritabanında saklar 
      ve listeler. Kullanıcılar, arayüzde yer alan dinamik Listbox bileşeni üzerinden diledikleri tarihi seçerek, o güne ait yüksek çözünürlüklü görsel içeriğe, 
      başlık, telif hakkı ve detaylı literatür açıklamalarına gecikmesiz olarak erişebilmektedir.
  </li>
  <br>
  <li> 
       <b>☄️ Asteroit Risk Analiz Paneli (ARAD):</b> NASA NeoWS (Near Earth Object Web Service) API verilerini temel alan bu panel, dünyanın yakınından geçen 
       asteroitlerin son bir yıllık fiziksel ve yörüngesel verilerini istatistiksel grafiklerle analiz eder. Panel bünyesinde yer alan "Risk Hesaplama 
       Penceresi",arka planda çalışan bir Makine Öğrenmesi Sınıflandırma Modeli (Random Forest) ile entegre edilmiştir. Kullanıcı tarafından 
       arayüze girilen asteroit parametreleri (maksimum/minimum çap, mutlak parlaklık, hız, minimum uzaklık ve sentry durumu) doğrultusunda model, 
       ilgili gök cisminin potansiyel tehlike durumunu (Pozitif/Negatif) sınıflandırır ve çarpma olasılığını yüzde bazında hesaplar.
  </li>
  <br>
  <li> 
       🔴 <b>Mars InSight Sol Monitörü:</b> NASA InSight Mars uzay aracının Sol 675 ile Sol 681 günleri arasında kızıl gezegenden topladığı anlık atmosferik verileri  işler. Bu modül; Mars yüzeyindeki sıcaklık (°C), rüzgar hızı (m/s) ve açık hava basıncı (Pa) değerlerinin haftalık ve günlük bazdaki değişimlerini, 
       Matplotlib ve Seaborn kütüphaneleri aracılığıyla gelişmiş sekmeli grafik panelleri halinde kullanıcıya sunar.
  </li>
</ul>
</p>
<hr> 
<h5>🧱 Projenin Mimarisi</h5>
<img width="1356" height="467" alt="image" src="https://github.com/user-attachments/assets/38cf55b4-cf0b-485c-b8dd-48ef71d8aced" />
<p> 
<i>Resim : Projenin Mimarisi</i>
</p>
<hr>
<h5>🛠️ Teknolojik Altyapı</h5>
<p>
    <li>🐍 <b>Dil</b> : Python 3.10.11</li>
    <li>💾 <b>Dosya İşlemleri</b> : os </li>
    <li>🖼️ <b>Görsel İşleme </b> : io ve Pillow </li>
    <li>📅 <b>Tarih ve Zaman İşlemleri</b> : datetime </li>
    <li>💻 <b>Kullanıcı Arayüzü (GUI)</b> : tkinter </li>
    <li>📊 <b>Veri Analizi ve Matematiksel İşlemler </b>: Pandas ve Numpy</li>
    <li>📈 <b>Veri Görselleştirme</b>: Matplotlib ve Seaborn</li>
    <li>🗄️ <b>Veritabanı</b> : SQLite</li>
    <li>🌐 <b>API Kaynağı ve İşlemleri</b> : NASA API ve requests</li>
    <li>🤖 <b>Makine Öğrenimi ve Model İşlemleri</b> : scikit-learn ve joblib</li>
</p>
<hr> 
<h5>🤖 Proje’de Kullanılan Makine Öğrenimi Modellerinin Analizi ve Karşılaştırılması</h5>
<p> 
Projedeki Astreoid Risk Analiz Paneli (ARAD) için yapılan astreoidlerin tehlike durumu ve bu tehlikelerin olasılıklarının hesaplanması için makine öğrenimi modelleri kullanılmıştır. Bu modeller sırasıyla : Lojistik Regresyon , Destek Vektör Sınıflandırma (SVC) , Karar Ağaçları (Decision Tree) ve son olarak Rassal Ağaçlar (Random Forrest) kullanılmıştır. Bu modeller teker teker eğitilerek hata metrikleri hesaplanmış ve en iyi model seçilerek ana projeye (.pkl) formatında aktarılmıştır.

Aşağıdaki tabloda modellerin doğruluk oranları, hata metrikleri ve eğitim-test skor oranları verilmiştir.

| 🤖 Model Adı | 📈 Eğitim Verisi Skoru | 📉 Test Verisi Skoru | 🎯 Precision (Kesinlik) | 🔬 Recall (Duyarlılık) | ⚖️ F1-Skor Değerleri | 🏆 Doğruluk Oranları |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Lojistik Regresyon** | 0.80 | 0.79 | 0.90 | 0.85 | 0.87 | 0.79 |
| **Destek Vektör Sınıflandırma (SVC)** | 0.83 | 0.78 | 0.91 | 0.83 | 0.87 | 0.78 |
| **Karar Ağaçları (Decision Tree)** | 0.83 | 0.72 | 1.00 | 0.67 | 0.80 | 0.72 |
| **Rassal Ormanlar (Random Forest)** | 0.88 | 0.79 | 1.00 | 0.76 | 0.86 | 0.79 |
<p>
  <i>Tablo : Projenin Tahmin Modellerinin Karşılaştırma Tablosu</i>
  <p>Bu tablodaki sonuçlara göre en iyi modelin Rassal Ormanlar (Random Forrest) olduğu görülmüş ve projede kullanılması için (.pkl) dosya formatında dışarıya aktarılmıştır. </p>
</p>
</p>
<hr>
<h5>🚀Kurulum ve Çalıştırma</h5>
<p>
Uygulamayı yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla takip edebilirsiniz:
</p>
 <li>
        <b>Depoyu Klonlayın:</b>
        <pre><code>git clone https://github.com/Ayberk-Aktan/My_Space_App.git</code></pre>
    </li>
    <li>
        <b>Proje Dizinine Gidin:</b>
        <pre><code>cd My_Space_App</code></pre>
    </li>
    <li>
        <b>Gerekli Kütüphaneleri Yükleyin:</b>
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>
        <b>Uygulamayı Başlatın:</b>
        <pre><code>python main.py</code></pre>
    </li>
   <p>
    ⚠️ ÖNEMLİ NOT: Uygulamayı ilk kez çalıştırmadan önce, API işlemleri ve yerel SQLite veritabanını başlatmak için (databases.py) ve yapay zeka modelini oluşturmak için (.pkl) risk_model_random_forrest.ipynb notebook'unu bir defaya mahsus çalıştırmanız gerekmektedir.
   </p>
<hr>
<h5>⚖️ Lisans</h5> 
<p>
  Bu proje <strong>Apache License 2.0</strong> ile lisanslanmıştır. Detaylı bilgi için <a href="LICENSE">LICENSE</a> dosyasına göz atabilirsiniz.
</p>
<hr>
<h5>🔗 İletişim</h5>
<p>
  Proje ile ilgili sorularınız veya geri bildirimleriniz için benimle iletişime geçebilirsiniz:
  <ul>
    <li>LinkedIn: <a href="https://www.linkedin.com/in/ayberk-aktan-3553a524a/">Ayberk Aktan</a></li>
    <li>GitHub: <a href="https://github.com/Ayberk-Aktan">Ayberk-Aktan</a></li>
  </ul>
</p>

