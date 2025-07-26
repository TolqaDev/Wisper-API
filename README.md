# Whisper Transcription API

OpenAI Whisper kullanarak ses dosyalarını metne dönüştüren profesyonel RESTful API sistemi.

## Özellikler

- **RESTful API**: FastAPI ile geliştirilmiş modern API
- **Kuyruk Sistemi**: Greenstalk ile asenkron işlem yönetimi
- **Worker Sistemi**: Arka planda çalışan ses dönüştürme işlemcisi
- **Veritabanı**: PostgreSQL ile veri saklama
- **Webhook**: İşlem tamamlandığında otomatik bildirim
- **Kapsamlı Loglama**: Tüm API istekleri ve işlemler loglanır
- **Docker Desteği**: Kolay kurulum ve dağıtım

## API Endpoints

### 1. Sistem Sağlığı
\`\`\`
GET /api/v1/health
\`\`\`
Sistem durumu ve kuyruk istatistiklerini döner.

### 2. Dönüştürme İşi Oluşturma
\`\`\`
POST /api/v1/transcribe
\`\`\`
Yeni ses dönüştürme işi oluşturur.

**Parametreler:**
- \`talent_id\` (zorunlu): Yetenek kimliği
- \`acc_id\` (zorunlu): Hesap kimliği
- \`mp3_file\` (zorunlu): Ses dosyası

### 3. İşlem Durumu Sorgulama
\`\`\`
GET /api/v1/transcribe/{id}
\`\`\`
Belirtilen işlem kimliği için durum bilgisi döner.

### 4. İşlem İptal Etme
\`\`\`
GET /api/v1/transcribe/{id}/cancel
\`\`\`
Beklemedeki işlemi iptal eder.

## Kurulum

### Docker ile Kurulum (Önerilen)

1. Projeyi klonlayın:
\`\`\`bash
git clone <repository-url>
cd whisper-transcription-api
\`\`\`

2. Çevre değişkenlerini ayarlayın:
\`\`\`bash
cp .env.example .env
# .env dosyasını düzenleyin
\`\`\`

3. Servisleri başlatın:
\`\`\`bash
docker-compose up -d
\`\`\`

### Manuel Kurulum

1. Python bağımlılıklarını yükleyin:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. PostgreSQL ve Beanstalk servislerini başlatın

3. Veritabanı migrasyonlarını çalıştırın:
\`\`\`bash
alembic upgrade head
\`\`\`

4. API'yi başlatın:
\`\`\`bash
uvicorn main:app --host 0.0.0.0 --port 8000
\`\`\`

5. Worker'ı başlatın:
\`\`\`bash
python worker/transcription_worker.py
\`\`\`

## Kullanım Örneği

\`\`\`python
import requests

# Ses dosyası yükleme
with open('audio.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/transcribe',
        data={
            'talent_id': '12345',
            'acc_id': '67890'
        },
        files={'mp3_file': f}
    )

job_id = response.json()['job_id']

# İşlem durumu kontrol etme
status_response = requests.get(
    f'http://localhost:8000/api/v1/transcribe/{job_id}'
)
print(status_response.json())
\`\`\`

## Mimari

Sistem 3 ana bileşenden oluşur:

1. **API Servisi**: FastAPI ile geliştirilmiş RESTful API
2. **Worker Servisi**: Greenstalk kuyruğunu dinleyen arka plan işlemcisi
3. **Veritabanı**: PostgreSQL ile veri saklama

## Güvenlik

- Dosya boyutu limiti (25MB)
- Desteklenen dosya formatları kontrolü
- MIME type doğrulaması
- Kapsamlı hata yönetimi

## Monitoring

- Tüm API istekleri loglanır
- İşlem durumları takip edilir
- Sistem sağlık durumu endpoint'i
- Kuyruk istatistikleri

## Lisans

MIT License
