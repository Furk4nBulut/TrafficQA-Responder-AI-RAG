# Web Trafik Loglarına Dayalı Yapay Zeka Destekli Soru-Cevap Sistemi

## Proje Tanımı

Bu proje, web trafik loglarına dayalı olarak geliştirilen bir yapay zeka destekli soru-cevap sistemi geliştirme sürecini içermektedir. Sistem, kullanıcıların doğal dilde sorduğu soruları analiz ederek, web trafik loglarından anlamlı yanıtlar üretmeyi amaçlar. Bu proje, özellikle web sitelerinin trafik verilerini daha etkili bir şekilde analiz etmeye ve performanslarını iyileştirmeye yönelik önemli katkılar sunma potansiyeline sahiptir.

## [Proje Raporu](https://github.com/Furk4nBulut/WebTrafficQA-Responder-AI-RAG/blob/master/FurkanBulutReport.pdf) , [Proje Kodları](https://github.com/Furk4nBulut/WebTrafficQA-Responder-AI-RAG/blob/master/product.ipynb)
## Proje Videosu

Aşağıdaki önizleme resmine tıklayarak projenin çalıştırılma videosunu izleyebilirsiniz:

[![Proje Videosu](https://img.youtube.com/vi/Kzss2Vug7PE/maxresdefault.jpg)](https://www.youtube.com/watch?v=Kzss2Vug7PE)


## İçindekiler

- [Giriş](#giriş)
- [Proje Dosya Yapısı](#proje-dosya-yapısı)
- [Metodoloji](#metodoloji)
  - [Veri Hazırlığı ve Ön İşleme](#veri-hazırlığı-ve-ön-i̇şleme)
  - [RAG Modelinin Oluşturulması](#rag-modelinin-oluşturulması)
  - [Sistem Entegrasyonu ve Test](#sistem-entegrasyonu-ve-test)
  - [Performans Değerlendirmesi](#performans-değerlendirmesi)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Lisans](#lisans)

## Giriş

Web siteleri, kullanıcı davranışlarını izleyebilmekte ve bu davranışları trafik logları olarak kaydedebilmektedir. Ancak, bu logların manuel olarak analiz edilmesi zor, karmaşık ve zaman alıcıdır. Bu proje, web trafik loglarını analiz ederek kullanıcıların doğal dildeki sorularına yanıt üreten bir yapay zeka destekli sistem geliştirmeyi amaçlar. Sistem, Retrieval-Augmented Generation (RAG) modeli ile güçlendirilmiş olup, trafik analiz süreçlerini hızlandırarak web sitelerinin performansını artırmayı ve güvenlik tehditlerini daha hızlı tespit etmeyi hedefler.

## Proje Dosya Yapısı

- **Product.ipynb**: Projenin çalışır durumda olan Jupyter notebook dosyası. Projeyi bu dosya ile incelemeniz tavsiye edilir.
- **Data/**:
  - **Apache/**: `DataGenerator.py` dosyası kullanılarak oluşturulan `logfiles.log` ve `data.csv` dosyaları burada bulunur.
  - **WebTraffic/**: İnternet üzerinde bulunan hazır veri setlerine ait 5 farklı CSV dosyası içerir.
- **Data_generator/**: Veri üretme ve CSV formatında kaydetme işlemleri için kullanılan Python dosyaları.
- **Maintenance/**: Proje geliştirme sürecinde oluşturulan dosyalar.

## Metodoloji

### Veri Hazırlığı ve Ön İşleme

Bu aşama, modelin başarısı için kritik öneme sahiptir. Aşağıda veri hazırlığı ve ön işleme adımları yer almaktadır:

1. **Veri Oluşturma ve Yükleme**: Web trafik logları, Apache sunucusu simüle edilerek oluşturuldu ve `data.csv` dosyasına kaydedildi.
2. **Veri Temizliği**:
   - Eksik veriler kontrol edildi ve temizlendi.
   - Gereksiz sütunlar kaldırıldı.
3. **Tarih ve Zaman Bilgilerinin İşlenmesi**: `Date` sütunu datetime formatına dönüştürüldü ve yıl, ay, gün, saat gibi yeni özellikler çıkarıldı.
4. **Yeni Özelliklerin Eklenmesi**: Durum kodlarının sayısal değerlere dönüştürülmesi ve `Request`, `Endpoint`, `Status Code` sütunlarının birleştirilmesi ile `Combined` sütunu oluşturuldu.

### RAG Modelinin Oluşturulması

RAG modeli, bilgi alma (Retrieval) ve jeneratif model bileşenlerini (Generation) birleştirerek kullanıcı sorgularına anlamlı yanıtlar üreten bir yaklaşımdır. Bu aşamada:

1. **Bilgi Alma Bileşeni**:
   - FAISS ile vektör veri tabanı oluşturuldu ve sorgular için TF-IDF yöntemiyle vektörler hesaplandı.
   - Kullanıcı sorgularına en uygun log kayıtları FAISS kullanılarak belirlendi.
2. **Jeneratif Model Bileşeni**:
   - GPT-2 modeli Hugging Face Transformers kütüphanesi kullanılarak yüklendi ve log kayıtları kullanılarak yanıtlar üretildi.

### Sistem Entegrasyonu ve Test

Bilgi alma ve jeneratif model bileşenleri entegre edilerek bütünleşik bir sistem oluşturuldu. Bu aşama şu adımları içerir:

1. **Sistem Entegrasyonu**: FAISS ile yapılan bilgi alma işlemleri, GPT-2 modeliyle entegre edilerek yanıt üretildi.
2. **Test Senaryoları**: Çeşitli test sorguları oluşturularak sistemin performansı değerlendirildi.
3. **Sistem Performansının Değerlendirilmesi**: Yanıt kalitesi, doğruluk ve yanıt süreleri ölçülerek sistem performansı analiz edildi.

### Performans Değerlendirmesi

Geliştirilen RAG tabanlı soru-cevap sisteminin etkinliği ve verimliliği analiz edilmiştir. Doğruluk, yanıt kalitesi ve yanıt süreleri gibi performans kriterleri değerlendirilmiştir.

## Kurulum

1. Bu projeyi klonlayın:

   ```bash
   git clone https://github.com/Furk4nBulut/WebTrafficQA-Responder-AI-RAG.git
   cd WebTrafficQA-Responder-AI-RAG
   ```
2. Jupyter Notebook kullanarak `Product.ipynb` dosyasını çalıştırın.

## Kullanım

1. `DataGenerator.py` dosyasını çalıştırarak veriyi oluşturun.
2. Jupyter Notebook üzerinden projeyi çalıştırarak sistemi test edebilir ve geliştirilen modeli kullanarak sorularınıza yanıt alabilirsiniz.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atabilirsiniz.