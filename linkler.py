import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

kategori_linkleri = dict() # Kategori isimlerinin ve linklerinin tutulacağı sözlük veri yapısı 

url = "https://www.trendyol.com" # Kullanılacak internet sayfası
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.content, "html.parser")
a = soup.find("ul", {"class": "main-nav"}).find_all("a", href=True) # Belirlenen class'lardaki bağlantı etiketlerinin bulunması

for i in a:
    kategori_linkleri[i.text.strip()] = url + i["href"] + "?pi=" # Her bir kategori ismi için link ataması: URL + Kategori İsmi + Page Index (pi) kodu

link_listesi = dict() # Alt kategorilerde bulunan ürünlerin kategori adına göre listeler halinde atanması
for kategori in kategori_linkleri.items():
    urun_linkleri = list() # Her sayfa içinde bulunan ürünlerin toplanması için geçici liste değişkeni
    index = 1 # Başlangıç sayfasının indisi

    while True:
        link = kategori[1] + str(index) # Sayfa linki + sayfa indisi
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        sayfa = soup.find_all(class_ = "p-card-wrppr") # Seçili sınıfa ait div etiketlerinin elde edilmesi
        
        urun_linkleri += [url + urun.find("a")["href"] for urun in sayfa] # Her bir ürün adresinin alınması ve geçici listeye aktarılması
        
        index += 1 # Sayfa sayısının artırılması
        time.sleep(1) # Çok sık istekte bulunmamak için 1 saniye bekle
        
        if a == [] or index == 3: # Bir sonraki sayfanın kontrolü (sayfada veri yoksa döngüden çık) ya da her kategori için 10 sayfalık ürün sınırlandırması. Sayfa 15'te dur.
            link_listesi[kategori[0]] = urun_linkleri # Elde edilen linkleri ilgili kategoriye liste halinde atama
            break

    print("looping...")

df = pd.DataFrame.from_dict(link_listesi, orient = 'index').transpose()
df.to_csv('linkler.csv', index = False, encoding = 'utf-16')
