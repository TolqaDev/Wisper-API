# App Klasörü

Bu klasör uygulamanın ana kodlarını içerir ve MVC (Model-View-Controller) mimarisine göre organize edilmiştir.

## Klasör Yapısı

### config/
Uygulama konfigürasyonları ve ayarları

- \`database.py\`: Veritabanı bağlantı ayarları ve session yönetimi
- \`settings.py\`: Çevre değişkenleri ve uygulama ayarları

### controllers/
API endpoint'lerini yöneten controller sınıfları

- \`health_controller.py\`: Sistem sağlık durumu endpoint'leri
- \`transcription_controller.py\`: Ses dönüştürme işlemleri endpoint'leri

### models/
Veritabanı modellerini tanımlayan sınıflar

- \`transcription.py\`: ConvertedSound modeli ve veritabanı şeması

### services/
İş mantığını içeren servis sınıfları

- \`queue_service.py\`: Greenstalk kuyruk işlemleri
- \`transcription_service.py\`: Ses dönüştürme iş mantığı

### middleware/
HTTP isteklerini işleyen middleware sınıfları

- \`logging_middleware.py\`: API isteklerini loglayan middleware

### utils/
Yardımcı fonksiyonlar ve araçlar

- \`webhook_client.py\`: Webhook istekleri gönderen istemci

## Mimari Prensipler

1. **Separation of Concerns**: Her sınıf tek bir sorumluluğa sahip
2. **Dependency Injection**: Bağımlılıklar constructor'da enjekte edilir
3. **Error Handling**: Kapsamlı hata yönetimi ve loglama
4. **Async/Await**: Asenkron programlama modeli
5. **Type Hints**: Python type annotations kullanımı
