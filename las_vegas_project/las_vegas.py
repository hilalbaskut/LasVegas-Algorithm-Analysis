"""
las_vegas.py
------------
Las Vegas Algoritması: Rastgele bir indeks seçer.
Eleman koşulu (mod 7 = 0) sağlanana kadar tekrar eder.
- Sonuç her zaman %100 DOĞRUDUR.
- Kaç adım süreceği rastgeledir.
"""

import random
from data_generator import CONDITION, STUDENT_ID


def las_vegas_search(data: list[int], seed: int = None) -> dict:
    """
    Veri içinde koşulu sağlayan bir elemanı Las Vegas yöntemiyle bulur.

    Parametreler:
        data  : Arama yapılacak liste
        seed  : Rastgele sayı üretici seed'i (tekrarlanabilirlik için)

    Döndürür:
        {
          "found_index"  : bulunan elemanın indeksi,
          "found_value"  : bulunan elemanın değeri,
          "steps"        : kaç denemede bulundu,
          "success"      : True (Las Vegas her zaman doğru bulur)
        }
    """
    rng = random.Random(seed)
    n = len(data)
    steps = 0

    while True:
        steps += 1
        idx = rng.randint(0, n - 1)      # Rastgele indeks seç
        if CONDITION(data[idx]):          # Koşul sağlanıyor mu?
            return {
                "found_index": idx,
                "found_value": data[idx],
                "steps": steps,
                "success": True,
            }


def las_vegas_count_all(data: list[int], seed: int = None) -> dict:
    """
    Alternatif versiyon: Tüm koşullu elemanları sayar (deterministik).
    Bu versiyon Las Vegas'ın deterministik kardeşidir — karşılaştırma için.
    """
    rng = random.Random(seed)
    n = len(data)
    indices = list(range(n))
    rng.shuffle(indices)          # Rastgele sırayla gez

    found = []
    steps = 0
    for idx in indices:
        steps += 1
        if CONDITION(data[idx]):
            found.append((idx, data[idx]))
            break                 # İlk buluşta dur (search versiyonu ile aynı mantık)

    return {
        "found_index": found[0][0] if found else -1,
        "found_value": found[0][1] if found else None,
        "steps": steps,
        "success": bool(found),
    }


if __name__ == "__main__":
    from data_generator import generate_data

    data = generate_data()

    print("=" * 50)
    print("LAS VEGAS ALGORİTMASI - TEK ÇALIŞTIRMA")
    print("=" * 50)

    result = las_vegas_search(data, seed=STUDENT_ID)

    print(f"Bulunan indeks  : {result['found_index']:,}")
    print(f"Bulunan değer   : {result['found_value']:,}")
    print(f"Adım sayısı     : {result['steps']}")
    print(f"Doğru mu?       : {result['success']}")
    print(f"Doğrulama       : {result['found_value']} mod 7 = {result['found_value'] % 7}")
    print("=" * 50)
