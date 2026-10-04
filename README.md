# Vastrel Hash Cracker

Wordlist (sözlük) tabanlı MD5 / SHA1 / SHA256 / SHA512 hash kırma aracı. Terminalde çalışır, girilen hash değerinin uzunluğuna bakarak algoritmayı otomatik tahmin eder ve belirtilen wordlist dosyasındaki satırları tek tek hash'leyerek eşleşme arar.

- **Geliştirici:** 404invisiblepeople
- **Grup:** Vastrel

## Özellikler

- MD5, SHA1, SHA256, SHA512 desteği
- Hash uzunluğuna göre otomatik algoritma tahmini
- Canlı ilerleme çubuğu ve anlık hız (aday/sn) gösterimi
- Sonuçların `hash_crack_logs.txt` dosyasına otomatik kaydı
- Harici bağımlılık yok, yalnızca Python standart kütüphanesi kullanılır

## Gereksinimler

- Python 3.8 veya üzeri

Üçüncü taraf bir paket gerekmez.

## Kurulum

```bash
git clone https://github.com/<kullanici-adi>/<repo-adi>.git
cd <repo-adi>
```

## Kullanım

1. Aynı klasöre bir wordlist dosyası koyun ve adını `vastrel_wordlist.txt` yapın (her satırda bir aday kelime/şifre olacak şekilde).
2. Scripti çalıştırın:

```bash
python3 hash_cracker.py
```

3. İstendiğinde kırmak istediğiniz hash değerini girin. Script, hash uzunluğuna göre türü otomatik tahmin etmeye çalışır; tahmin edemezse türü (md5, sha1, sha256, sha512) elle girmenizi ister.
4. Tarama bitince eşleşme bulunduysa aday kelime, kullanılan wordlist, toplam deneme sayısı ve geçen süre ekrana yazdırılır; sonuç ayrıca `hash_crack_logs.txt` dosyasına eklenir.

### Farklı bir wordlist kullanmak

Varsayılan olarak script `vastrel_wordlist.txt` dosyasını arar. Başka bir dosya kullanmak isterseniz `hash_cracker.py` içindeki `WORDLISTS` listesini düzenleyin:

```python
WORDLISTS = ["benim_listem.txt"]
```

Listeye birden fazla dosya eklerseniz script, eşleşme bulunana kadar sırayla hepsini tarar.

## Nasıl çalışır?

Script wordlist dosyasını satır satır okur, her satırı (orijinal bayt dizisi üzerinden, kodlama hatalarına karşı dayanıklı şekilde) seçilen algoritmayla hash'ler ve hedef hash ile karşılaştırır. Eşleşme bulunursa tarama durur ve sonuç raporlanır.

## Sınırlamalar

- Yalnızca sözlük (wordlist) saldırısı yapar; brute-force/mask saldırısı veya tuzlanmış (salted) hash desteği yoktur.
- Performans tamamen wordlist boyutuna ve donanıma bağlıdır; çok büyük listelerde GPU tabanlı araçlar (örn. hashcat) çok daha hızlıdır.

## Yasal Uyarı

Bu araç yalnızca kendi sahip olduğunuz veya test etme izniniz bulunan hash değerleri üzerinde (parola denetimi, eğitim, yetkili güvenlik testi vb. amaçlarla) kullanılmak üzere paylaşılmıştır. Başkasına ait sistemlere veya verilere izinsiz erişim sağlamak amacıyla kullanılması kanunlara aykırıdır ve bu sorumluluk tamamen kullanıcıya aittir.

## Lisans

Bu depoya uygun gördüğünüz bir lisans (ör. MIT) eklemenizi öneririz.
