# Middleware Klasörü

Bu klasör HTTP isteklerini işleyen middleware sınıflarını içerir.

## Dosyalar

### logging_middleware.py
Tüm API isteklerini kapsamlı olarak loglayan middleware sınıfı.

**Ana İşlevler:**

**dispatch(request, call_next):**
- Her HTTP isteği için çalışır
- Benzersiz istek kimliği oluşturur
- İstek ve yanıt bilgilerini loglar
- İşlem süresini ölçer
- Yanıt header'ına istek kimliği ekler

**İstek Loglama Algoritması:**
1. Benzersiz istek kimliği oluştur (UUID'nin ilk 8 karakteri)
2. İstemci IP adresini al
3. User-Agent bilgisini çıkar
4. HTTP method ve URL'yi kaydet
5. Header'ları ve query parametrelerini logla
6. POST istekleri için body'yi işle

**Body İşleme Stratejisi:**
- \`multipart/form-data\`: "dosya yükleme" olarak işaretle
- \`application/json\`: JSON parse et ve logla
- Diğer türler: "binary/other content" olarak işaretle
- Parse hatalarında güvenli fallback

**Yanıt Loglama:**
- HTTP status code
- İşlem süresi (milisaniye)
- Yanıt header'ları
- Log seviyesi belirleme (status code'a göre)

**Log Seviyeleri:**
- 500+: ERROR
- 400-499: WARNING  
- 200-399: INFO

**Güvenlik Özellikleri:**
- Hassas bilgilerin maskelenmesi
- JSON serialization hata yönetimi
- Memory-safe dosya işleme
- Exception handling

**Performans Optimizasyonu:**
- Lazy evaluation
- Minimal memory footprint
- Asenkron işlem desteği
- Efficient string operations
