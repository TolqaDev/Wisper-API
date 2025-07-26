# Worker Klasörü

Bu klasör arka planda çalışan worker servislerini içerir.

## Dosyalar

### transcription_worker.py
Greenstalk kuyruğunu dinleyen ve ses dönüştürme işlemlerini yapan ana worker sınıfı.

**Ana İşlevler:**

**load_whisper_model():**
- OpenAI Whisper modelini yükler
- "base" model kullanır (hız/kalite dengesi)
- Model yükleme hatalarını yönetir
- Memory-efficient loading

**process_job(job_data):**
- Tek bir işi işleyen ana algoritma
- Veritabanı durumu güncelleme
- Whisper ile ses dönüştürme
- MD5 şifreleme
- Webhook gönderimi
- Geçici dosya temizliği

**İş İşleme Algoritması:**
1. İş verilerini parse et (uuid, talent_id, acc_id, file_path)
2. Veritabanında durumu 'processing' yap
3. Ses dosyası varlığını kontrol et
4. Whisper ile transcription yap
5. Boş metin kontrolü
6. MD5 hash oluştur
7. Veritabanını 'success' olarak güncelle
8. Webhook gönder
9. Geçici dosyayı sil

**run():**
- Ana worker döngüsü
- Whisper model yükleme
- Kuyruk dinleme
- İş alma ve işleme
- Hata yönetimi ve recovery

**Kuyruk Dinleme Algoritması:**
1. Greenstalk client oluştur
2. Tube'u watch et
3. 30 saniye timeout ile job reserve et
4. JSON parse et
5. İşi process_job()'a gönder
6. Başarılıysa delete, hatalıysa release
7. Timeout'ta devam et, hata durumunda bekle

**Hata Yönetimi:**
- İş işleme hataları veritabanına kaydedilir
- Worker crash'lerinde recovery
- Poison message handling
- Graceful degradation

**Performans Optimizasyonu:**
- Model tek seferlik yükleme
- Connection pooling
- Memory management
- Efficient file handling

**Monitoring:**
- Detaylı işlem logları
- Performance metrikleri
- Error tracking
- Health check desteği

**Güvenlik:**
- Dosya path validation
- Safe file operations
- Error message sanitization
- Resource cleanup
