# Utils Klasörü

Bu klasör yardımcı fonksiyonlar ve araçları içerir.

## Dosyalar

### webhook_client.py
Webhook istekleri gönderen istemci sınıfı.

**Ana İşlevler:**

**send_completion_webhook():**
- Dönüştürme tamamlandığında webhook gönderir
- Asenkron HTTP istek gönderimi
- Yeniden deneme mekanizması
- Exponential backoff algoritması

**Webhook Payload Formatı:**
\`\`\`json
{
  "uuid": "işlem-kimliği",
  "talent_id": "yetenek-kimliği", 
  "acc_id": "hesap-kimliği",
  "text": "dönüştürülen-metin",
  "status": "completed",
  "timestamp": "2024-01-01T00:00:00Z"
}
\`\`\`

**Yeniden Deneme Algoritması:**
1. Maksimum 3 deneme
2. Her denemede exponential backoff (2^attempt saniye)
3. HTTP 200 response'da başarılı sayılır
4. Timeout: 30 saniye
5. Tüm denemeler başarısızsa error log

**Hata Yönetimi:**
- Network timeout'ları
- HTTP error status kodları
- JSON serialization hataları
- Connection errors
- SSL/TLS hataları

**Güvenlik Özellikleri:**
- HTTPS desteği
- Request timeout
- Content-Type header kontrolü
- Safe JSON serialization

**Monitoring:**
- Detaylı loglama
- Başarı/başarısızlık metrikleri
- Response time tracking
- Error categorization

**Konfigürasyon:**
- Webhook URL çevre değişkeninden alınır
- Timeout ve retry sayıları ayarlanabilir
- Header customization desteği
- Environment-based configuration

### auth.py (Yeni)
API kimlik doğrulama mekanizmasını yöneten yardımcı fonksiyonlar.

**Ana İşlevler:**

**oauth2_scheme:**
- FastAPI'nin \`HTTPBearer\` şemasını kullanarak \`Authorization: Bearer <TOKEN>\` başlığını bekler.

**get_current_user(credentials):**
- Gelen Bearer token'ı doğrular.
- \`settings.API_SECRET_TOKEN\` ile karşılaştırır.
- Token geçerliyse basit bir kullanıcı kimliği döndürür.
- Geçersizse \`HTTPException(401)\` fırlatır.

**Güvenlik:**
- Basit token karşılaştırması (geliştirme ortamı için uygun)
- Gerçek uygulamalarda JWT veya daha karmaşık doğrulama yöntemleri kullanılmalıdır.
- Hata durumunda \`WWW-Authenticate\` başlığı ile istemciye bilgi verir.
