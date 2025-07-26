# Alembic Klasörü

Bu klasör veritabanı migration'larını yöneten Alembic konfigürasyonlarını içerir.

## Dosyalar

### env.py
Alembic migration environment konfigürasyonu.

**Ana İşlevler:**

**get_url():**
- Veritabanı URL'ini çevre değişkeninden alır
- Fallback default değer sağlar
- Environment-based configuration

**run_migrations_offline():**
- Offline migration modu
- SQL script generation
- Database connection olmadan çalışır
- CI/CD pipeline'lar için ideal

**run_migrations_online():**
- Online migration modu
- Canlı veritabanı bağlantısı
- Real-time schema changes
- Production deployment için

**Konfigürasyon:**
- Model metadata import
- Connection pooling ayarları
- Logging konfigürasyonu
- Environment detection

### versions/001_create_converted_sounds_table.py
İlk migration dosyası - converted_sounds tablosunu oluşturur.

**upgrade() Fonksiyonu:**
1. converted_sounds tablosunu oluştur
2. Tüm sütunları tanımla (uuid, talent_id, acc_id, vb.)
3. Primary key constraint ekle
4. Performance indeksleri oluştur

**downgrade() Fonksiyonu:**
1. İndeksleri sil
2. Tabloyu sil
3. Rollback işlemi

**İndeks Stratejisi:**
- talent_id: Yetenek bazlı sorgular için
- acc_id: Hesap bazlı filtreleme için  
- status: Durum bazlı sorgular için

**Veri Tipleri:**
- UUID: PostgreSQL native UUID type
- String: Varchar with length limits
- Text: Unlimited text storage
- DateTime: Timezone-aware timestamps

### alembic.ini
Alembic konfigürasyon dosyası.

**Ana Ayarlar:**
- Script location: migration dosyalarının yeri
- Database URL: connection string
- Logging configuration
- Version path separator

**Logging Konfigürasyonu:**
- Root logger: WARN level
- SQLAlchemy logger: Engine queries
- Alembic logger: Migration operations
- Console handler: stderr output

**Migration Ayarları:**
- Version table name
- Script template location
- File naming convention
- Timezone handling

**Güvenlik:**
- Database credential management
- Environment variable usage
- Safe default values
- Connection timeout settings
\`\`\`

Bu kapsamlı sistem, OpenAI Whisper API kullanarak profesyonel bir ses-metin dönüştürme servisi sağlar. Sistem MVC mimarisi ile geliştirilmiş, kuyruk sistemi ile ölçeklenebilir, kapsamlı loglama ile izlenebilir ve Docker ile kolay deploy edilebilir bir yapıya sahiptir.
