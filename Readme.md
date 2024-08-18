# Web Trafik Loglarına Dayalı Yapay Zeka Destekli Soru-Cevap Sistemi

Özetçe:
Proje, web trafik loglarına dayalı olarak geliştirilen bir yapay zeka destekli soru-cevap sistemi geliştirme süreçlerini içermektedir.
Sistem, kullanıcılardan gelen doğal dildeki soruları analiz ederek, log verileri analiz ederek yanıt üretmeyi hedeflemektedir. 
Log verileri veri önişleme adımları ile temizlenmiş, TF-IDF yöntemiyle vektörize edilerek FAISS vektör veri tabanında depolanmıştır. Kullanıcı sorularına en uygun log kayıtlarını bulmak için Retrieval-Augmented Generation (RAG) modeli ile GPT-2 dil modeli kullanılmıştır. Geliştirilen sistem, yapılan testler sonucunda, kullanıcı sorularına  yanıtlar üretebilmiştir.
Geliştirilen proje, web sitelerinin trafik verilerini daha etkili bir şekilde analiz etmeye ve performanslarını iyileştirmeye yönelik olup bu alanda potansiyel olarak iyileştirme süreçlerine yardımcı olabilecek niteliğe sahiptir.

Giriş:

Web siteleri, kullanıcı davranışlarını izleyebilmektedir. Bu davranışları trafik logları olarak kaydederek geliştiriciler için sistem performansını değerlendirmeye olanak sağlamaktadır..
Bu loglar, manuel olarak analiz edilmesi zor, karmaşık ve zaman alıcı olan yüksek miktarda verilerdir. 
Log verilerinden anlamlı bilgiler çıkarmak kullanıcı deneyimini iyileştirmek için kritik öneme sahiptir.

Geliştirilen proje, web trafik loglarını verilerini analiz eden ve kullanıcıların doğal dildeki sorularına yanıt üreten yapay zeka destekli bir sistemdir. 
Retrieval-Augmented Generation (RAG) modeli ile geliştirilen bu sistem, üretilen verilerden anlamlı bilgiler çıkararak, trafik analiz süreçlerini hızlandırmaktadır. 
Bu proje, web sitelerinin performansını artırma ve güvenlik tehditlerini daha hızlı tespit etme konusunda önemli katkı sunma potansiyeline sahiptir.3










#%%
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Veri Yükleme
data = pd.read_csv('data/apache/data.csv')

# Veri çerçevesindeki sütun adlarını kontrol et
print("Sütun Adları:", data.columns)

# Tarih sütununu datetime formatına dönüştürme
data['Date'] = pd.to_datetime(data['Date'].str.strip('[]'), format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')

# Eksik Verilerin Kontrolü
missing_values = data.isnull().sum()
print("Eksik Veriler:", missing_values)

# Gereksiz Sütunları Kaldırma (eğer veri çerçevesinde varsa)
data = data.drop(columns=['Referrer', 'User Agent'], errors='ignore')

# Yeni Özellikler Ekleme: Yıl, Ay, Gün, Saat, Dakika
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day
data['Hour'] = data['Date'].dt.hour
data['Minute'] = data['Date'].dt.minute

# 'Status Code' sütununu sayısal değerlere dönüştürme (eğer gerekliyse)
data['Status Code'] = pd.to_numeric(data['Status Code'], errors='coerce')

# Boş veya Hatalı Verileri Temizleme
data = data.dropna(subset=['Request', 'Endpoint', 'Status Code'])
data = data[data['Request'].str.strip() != '']
data = data[data['Endpoint'].str.strip() != '']
data = data[data['Status Code'].notna()]  # Sayısal sütunları kontrol et

# Birleştirilen metin verisini oluştur
data['Combined'] = data['Request'] + ' ' + data['Endpoint'] + ' ' + data['Status Code'].astype(str)

# Boş verileri kontrol et
print(data['Combined'].head())
print(data['Combined'].isnull().sum())

# TF-IDF Vektörizasyonu
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Combined']).toarray()

# FAISS İndeksi Oluşturma ve Vektörlerin Eklenmesi
index = faiss.IndexFlatL2(X.shape[1])
index.add(X.astype('float32'))

# Kullanıcı Sorgusunu Vektörleştirme ve En Yakın Komşuları Bulma
def find_relevant_logs(query):
    query_vector = vectorizer.transform([query]).toarray().astype('float32')
    D, I = index.search(query_vector, 5)
    return data.iloc[I[0]]

# GPT-2 Modeli ile Yanıt Oluşturma
def generate_response(logs):
    input_text = " ".join(
        logs.apply(lambda row: f"{row['Date']} {row['Request']} {row['Endpoint']} {row['Status Code']}",
                   axis=1).tolist())
    input_text = input_text[:1000]  # Giriş metnini 1000 karakterle sınırlama

    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

    output = model.generate(input_ids, attention_mask=attention_mask, max_length=150, num_return_sequences=1,
                            pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Sorgu Yanıt Sistemi
def answer_question(query):
    relevant_logs = find_relevant_logs(query)
    response = generate_response(relevant_logs)
    return response

# Model ve Tokenizer Yükleme
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
#%%
# Test Sorguları Listesi
queries = [
    "Son 24 saatte hangi URL'ler 500 hatası aldı?",
    "Son bir ayda hangi IP adresleri en fazla 403 hatası aldı?",
    "Son bir yıl içinde en sık kullanılan POST isteklerinin listesi nedir?",
    "Son 30 gün içinde hangi tarayıcılar en fazla 404 hatası aldı?",
    "Son haftada hangi endpoint'ler en yüksek Response Size'a sahipti?",
    "En son 10 istekte hangi User Agent'lar kullanıldı?",
    "En yüksek zaman alımı (Time Taken) olan 5 istek nedir?",
    "Son 6 ayda hangi Referrer en çok ziyaret edildi?",
    "Son 24 saatte hangi Endpoint'lerde 502 hatası alındı?",
    "Hangi IP adresleri en uzun süre GET isteği yaptı?",
    "Which IP adress has Longest GET time ?",
]
#%%
# Her bir sorguyu test etme
for query in queries:
    print("-" * 80)
    print("\n")
    
    response = answer_question(query)
    print(f"Sorgu: {query}")
    print(f"Modelin Yanıtı: {response}")
    print("\n")
