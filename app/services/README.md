# Services Klasörü

Bu klasör iş mantığını içeren servis sınıflarını barındırır. Her servis belirli bir domain'e odaklanır.

## Dosyalar

### queue_service.py
Greenstalk kuyruk sistemini yöneten servis sınıfı.

**Ana İşlevler:**

**add_job(job_data, priority):**
- Kuyruğa yeni iş ekler
- JSON formatında veri serileştirme
- Öncelik bazlı sıralama (düşük sayı = yüksek öncelik)
- Bağlantı yönetimi ve hata kontrolü

**get_queue_stats():**
- Kuyruk istatistiklerini getirir
- Toplam, bekleyen, işlemde olan iş sayıları
- Buried (gömülü) iş sayısı
- Hata durumunda varsayılan değerler

**cancel_job_by_uuid(target_uuid):**
- UUID'ye göre işi kuyruktan iptal eder
- Kuyruktaki tüm işleri tarar
- Hedef işi bulup siler
- Diğer işleri geri bırakır

**Algoritma (İş İptali):**
1. Kuyruğu dinle
2. İşleri sırayla reserve et
3. JSON parse et ve UUID kontrol et
4. Eşleşme varsa delete, yoksa release
5. Timeout'a kadar devam et

### transcription_service.py
Ses dönüştürme işlemlerinin iş mantığını yönetir.

**Ana İşlevler:**

**create_transcription_job():**
- Yeni dönüştürme işi oluşturur
- Dosya doğrulaması yapar
- Geçici dosya kaydeder
- Veritabanına kayıt ekler
- Kuyruğa iş ekler

**Dosya Doğrulama Algoritması:**
1. Boyut kontrolü (25MB limit)
2. Dosya uzantısı kontrolü (mp3, wav, m4a, flac)
3. MIME type doğrulaması
4. İçerik türü kontrolü

**get_transcription_status():**
- İşlem durumunu sorgular
- UUID bazlı arama
- Model nesnesini dict'e dönüştürür

**cancel_transcription_job():**
- İşlemi iptal eder
- Sadece 'pending' durumundaki işler iptal edilebilir
- Kuyruk ve veritabanı senkronizasyonu

**Geçici Dosya Yönetimi:**
- /tmp/whisper_uploads klasörü
- UUID bazlı dosya isimlendirme
- Otomatik klasör oluşturma
- Hata durumunda temizlik

**MD5 Şifreleme:**
- Dönüştürülen metnin hash'ini oluşturur
- UTF-8 encoding desteği
- Güvenlik ve doğrulama amaçlı
