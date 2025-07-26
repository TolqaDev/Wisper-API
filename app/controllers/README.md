# Controllers Klasörü

Bu klasör API endpoint'lerini yöneten controller sınıflarını içerir. Her controller belirli bir domain'e odaklanır.

## Dosyalar

### health_controller.py
Sistem sağlık durumu ve monitoring endpoint'lerini yönetir.

**Endpoint:**
- \`GET /api/v1/health\`: Sistem durumu, kuyruk istatistikleri ve veritabanı durumu

**Algoritma:**
1. Greenstalk kuyruk istatistiklerini al
2. Veritabanından işlem durumu sayılarını hesapla
3. Sistem sağlık durumunu değerlendir
4. Kapsamlı durum raporu döner

**Özellikler:**
- Kuyruk ve veritabanı senkronizasyon kontrolü
- Detaylı istatistikler
- Sistem uyarı durumları

### transcription_controller.py
Ses dönüştürme işlemlerinin API endpoint'lerini yönetir.

**Endpoint'ler:**
- \`POST /api/v1/transcribe\`: Yeni dönüştürme işi oluştur
- \`GET /api/v1/transcribe/{id}\`: İşlem durumu sorgula
- \`DELETE /api/v1/transcribe/{id}/cancel\`: İşlemi iptal et

**Algoritma (POST /transcribe):**
1. **İstek Başlangıç Zamanını Kaydet**: İşlemin ne kadar sürdüğünü ölçmek için.
2. **İstemci IP Adresini Al**: İsteği atan istemcinin IP adresini loglamak ve yanıtta döndürmek için.
3. Form verilerini doğrula (talent_id, acc_id, mp3_file)
4. Dosya formatı ve boyutu kontrolü
5. Benzersiz UUID oluştur
6. Geçici dosya kaydet
7. Veritabanına kayıt ekle
8. Kuyruğa iş ekle
9. **İşlem Süresini Hesapla**: İşlemin tamamlanma süresini milisaniye cinsinden hesapla.
10. **Gelişmiş JSON Yanıtı Dön**: İşlem kimliği, durum bilgisi, istemci IP'si, işlem süresi ve dinamik zaman damgası içeren detaylı bir yanıt döner.

**Güvenlik Kontrolleri:**
- Zorunlu alan doğrulaması
- Dosya boyutu limiti (25MB)
- Desteklenen format kontrolü
- MIME type doğrulaması

**Hata Yönetimi:**
- HTTP status kodları
- Detaylı hata mesajları
- Transaction rollback
- Kapsamlı loglama
- **Hata durumunda da detaylı yanıt**: Hata durumunda bile istemci IP'si, işlem süresi ve zaman damgası gibi bilgileri içeren bir yanıt döner.
