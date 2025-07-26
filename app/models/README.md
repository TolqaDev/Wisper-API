# Models Klasörü

Bu klasör veritabanı modellerini ve şemalarını tanımlayan sınıfları içerir.

## Dosyalar

### transcription.py
Ses dönüştürme işlemlerinin veritabanı modelini tanımlar.

**ConvertedSound Modeli:**

**Alanlar:**
- \`uuid\`: Benzersiz işlem kimliği (Primary Key, UUID)
- \`talent_id\`: Yetenek kimliği (String, 50 karakter, zorunlu, indeksli)
- \`acc_id\`: Hesap kimliği (String, 50 karakter, zorunlu, indeksli)
- \`text\`: Dönüştürülen metin (Text, opsiyonel)
- \`encoded_text\`: MD5 ile şifrelenmiş metin (Text, opsiyonel)
- \`status\`: İşlem durumu (String, 20 karakter, zorunlu, indeksli)
- \`error_message\`: Hata mesajı (Text, opsiyonel)
- \`created_at\`: Oluşturulma tarihi (DateTime, otomatik)
- \`updated_at\`: Güncellenme tarihi (DateTime, otomatik güncelleme)

**Status Değerleri:**
- \`pending\`: Beklemede
- \`processing\`: İşlemde
- \`success\`: Başarılı
- \`error\`: Hatalı
- \`cancelled\`: İptal edildi

**İndeksler:**
- \`talent_id\`: Hızlı sorgulama için
- \`acc_id\`: Hesap bazlı filtreleme için
- \`status\`: Durum bazlı sorgular için

**Metodlar:**
- \`to_dict()\`: Model nesnesini sözlük formatına dönüştürür
- UUID'ler string formatında döner
- Tarihler ISO format'ta döner

**Veritabanı Özellikleri:**
- PostgreSQL UUID desteği
- Otomatik timestamp güncelleme
- Foreign key ilişkileri için hazır yapı
- Performans optimizasyonu için indeksler
