from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome() # Chrome uygulamasını kullanma

df = pd.read_csv("linkler.csv", delimiter=",", encoding="utf-16")

yorumlar = []
for kategori in df.columns[:2]:
    for link in df[kategori].values:
        link += "/yorumlar" # Trendyol'un ürün yorumları sayfasına gitmek için bir eklenti
        driver.get(link) # İstenen bağlantının webdriver üzerinde açılması
        html = driver.page_source # İstenen sayfadaki HTML içeriğin elde edilmesi

        soup = BeautifulSoup(html, "html.parser") # Elde edilen içeriğin parçalanması
        for data in soup.findAll("div", {"class", "rnr-com-w"}): # İlgili linkteki ürüne ait yorum sınıfı üzerinde döngü
            yorum = data.find(class_ = "rnr-com-tx") # Yorum içeriğinin elde edilebilmesi için üst sınıfı elde etme
            yildiz_sayisi = data.findAll(class_ = "full", attrs={'style':'width: 100%; max-width: 100%;'}) # Yıldız sayısının elde edilmesi
            if yorum != None and yildiz_sayisi != None:
                yorumlar.append([kategori, len(yildiz_sayisi), yorum.find("p").text.strip()])

df = pd.DataFrame(yorumlar, columns=["Kategori", "Yıldız", "Yorum"])
df.to_csv('yorumlar.csv', index = False, encoding = 'utf-16')
