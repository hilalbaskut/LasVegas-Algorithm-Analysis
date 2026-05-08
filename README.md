# Las Vegas Algorithm — Randomized Search Analysis

> **Algoritma Analizi Dersi** | Rastgeleleştirilmiş Algoritmalar Projesi  
> Öğrenci No Son 2 Hane: **03** → Las Vegas Yaklaşımı | n = 10⁵

---

## 📋 Proje Özeti

Bu proje, 100.000 elemanlı rastgele bir dizide `x mod 7 == 0` koşulunu sağlayan ilk elemanı bulmak için **Las Vegas algoritması** uygular. Rastgeleliğin zaman karmaşıklığı üzerindeki etkisi, **Geometrik Dağılım** temelli teorik model ile 100 deneysel çalıştırmanın karşılaştırılmasıyla analiz edilmiştir.

### Algoritma Seçim Mantığı

| Parametre | Kural | Bu Proje |
|---|---|---|
| Algoritma Tipi | Son iki hane **tek** → Las Vegas | `03` → **Las Vegas** |
| Veri Boyutu | Son rakam `< 5` → n = 10⁵ | `3 < 5` → **n = 100.000** |

---

## 🗂️ Proje Yapısı

```
.
├── data_generator.py   # Seed'li rastgele veri seti üretici
├── las_vegas.py        # Las Vegas arama algoritması
├── analysis.py         # 100 çalıştırma + istatistiksel analiz
├── main.py             # Ana program (giriş noktası)
└── README.md
```

---

## ⚙️ Kurulum ve Çalıştırma

**Gereksinimler:** Python 3.10+, standart kütüphane yeterli (ek paket gerekmez).

```bash
# Repoyu klonla
git clone https://github.com/<kullanici-adin>/<repo-adin>.git
cd <repo-adin>

# Öğrenci numarasını ayarla (data_generator.py içinde)
# STUDENT_ID = <öğrenci_numaranız>

# Çalıştır
python main.py
```

---

## 🔢 Parametreler

| Sabit | Değer | Açıklama |
|---|---|---|
| `STUDENT_ID` | `1240505903` | Rastgele sayı üretici seed'i |
| `N` | `100_000` | Veri seti boyutu |
| `CONDITION` | `x % 7 == 0` | Aranacak özel eleman koşulu |
| `RUNS` | `100` | Deneysel analiz için çalıştırma sayısı |

---

## 📁 Dosya Açıklamaları

### `data_generator.py`
Öğrenci numarasıyla seed'lenmiş `random.Random` örneği kullanarak `n` elemanlı rastgele tam sayı dizisi üretir. Seed zorunluluğu yönerge gereğidir; tekrarlanabilir sonuçlar sağlar.

```python
STUDENT_ID = 1240505903
CONDITION  = lambda x: x % 7 == 0

def generate_data(n=N, seed=STUDENT_ID) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(1, 10 * n) for _ in range(n)]
```

### `las_vegas.py`
Las Vegas yaklaşımıyla arama yapar: koşulu sağlayan eleman bulunana kadar rastgele indeks seçer. Sonuç **her zaman %100 doğrudur**; yalnızca kaç adım süreceği rastgeledir.

```python
def las_vegas_search(data, seed=None) -> dict:
    rng = random.Random(seed)
    steps = 0
    while True:
        steps += 1
        idx = rng.randint(0, len(data) - 1)
        if CONDITION(data[idx]):
            return {"found_index": idx, "found_value": data[idx],
                    "steps": steps, "success": True}
```

### `analysis.py`
Algoritmayı `RUNS=100` kez farklı seed'lerle çalıştırır; adım sayısı ve süre üzerinden ortalama, standart sapma ve varyasyon katsayısı hesaplar. Sonuçları Geometrik Dağılım'ın teorik değerleriyle karşılaştırır.

### `main.py`
Dört aşamalı ana akışı yürütür: veri üretimi → tek çalıştırma örneği → teorik hesaplar → 100 çalıştırma analizi ve özet rapor.

---

## 📊 Sonuçlar

### Veri Seti

| Metrik | Değer |
|---|---|
| Toplam eleman | 100.000 |
| Koşulu sağlayan eleman (`x % 7 == 0`) | 14.290 |
| Gerçek oran (p) | 0.14290 |
| Teorik oran (1/7) | 0.14286 |

### Teorik vs Deneysel (100 Çalıştırma)

| Metrik | Teorik | Deneysel |
|---|---|---|
| E[X] — Beklenen adım sayısı | 6.9979 | 6.3800 |
| σ — Standart sapma | 6.4786 | 4.5986 |
| Hata oranı | 0.000 | **0.000** |
| CV (Varyasyon Katsayısı) | — | %72.1 |
| Minimum adım | — | 1 |
| Maksimum adım | — | 20 |
| Ortalama çalışma süresi | — | 0.0134 ms |

### Örnek Çıktı

```
╔══════════════════════════════════════════════════════╗
║         LAS VEGAS ALGORİTMASI - ANA PROGRAM         ║
╠══════════════════════════════════════════════════════╣
║  Öğrenci No Son 2 Hane : 03 (tek → Las Vegas)       ║
║  Veri Boyutu           : n = 100,000                ║
║  Seed                  : 1240505903                  ║
║  Arama Koşulu          : x mod 7 == 0               ║
╚══════════════════════════════════════════════════════╝

[3/4] Teorik hesaplar...
      Beklenen adım sayısı  E[X] = 1/p = 1/0.14290 = 6.9979
      Standart sapma        σ    = √((1-p)/p²)    = 6.4786

ÖZET KARŞILAŞTIRMA TABLOSU
-------------------------------------------
Metrik                       Teorik  Deneysel
-------------------------------------------
E[X] (beklenen adım)         6.9979    6.3800
σ (standart sapma)           6.4786    4.5986
-------------------------------------------
Las Vegas garantisi: Her çalıştırma %100 doğru sonuç verir.
Rastgelelik yalnızca SÜRE üzerinde etkilidir, doğrulukta değil.
```

---

## 🧮 Matematiksel Temel

Las Vegas algoritmasında bir elemanı bulmak için gereken adım sayısı **X**, `p` parametreli **Geometrik Dağılım**'a uyar.

$$P(X = k) = (1 - p)^{k-1} \cdot p$$

| Formül | İfade | Bu Proje |
|---|---|---|
| Beklenen adım sayısı | $E[X] = \dfrac{1}{p}$ | $\dfrac{1}{0.14290} \approx 6.9979$ |
| Standart sapma | $\sigma = \sqrt{\dfrac{1-p}{p^2}}$ | $\approx 6.4786$ |
| Büyük adım olasılığı | $P(X > k) = (1-p)^k$ | Üstel hızda → 0 |

### Zaman Karmaşıklığı

| Durum | Karmaşıklık |
|---|---|
| **Beklenen** | O(1/p) · O(T) = **O(1)** |
| **En kötü (teorik)** | O(∞) — ancak P(X > k) üstel azalır |
| **Bellek** | O(n) veri seti, O(1) algoritma |

---

## 🔍 Bulgular ve Yorum

- **Doğruluk garantisi:** 100/100 çalıştırmada `found_value % 7 == 0` doğrulandı.
- **E[X] yakınsaması:** Deneysel ortalama (6.38), teorik değerin (6.9979) ±%15 bandında — Las Vegas'ın beklenen davranışıyla uyumlu.
- **Yüksek CV (%72.1):** Rastgelelik çalışma süresi üzerinde belirleyici etkiye sahip; her çalıştırma birbirinden farklı sürebilir. Bu Las Vegas'ın doğasıdır.
- **σ farkı:** Deneysel σ (4.60) < Teorik σ (6.48) — 100 örneklem, Geometrik dağılımın asimetrik sağ kuyruğunu tam yakalayamıyor. Örneklem büyüdükçe teorik değere yakınsama beklenir.

---

## 📄 Lisans

Bu proje akademik amaçlıdır. Ders ödevi kapsamında hazırlanmıştır.
