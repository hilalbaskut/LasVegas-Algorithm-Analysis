"""
data_generator.py
-----------------
Öğrenci numarasıyla seed'lenmiş rastgele veri seti üretir.
Öğrenci no son iki hane: 03 → n = 10^5
"""

import random

STUDENT_ID = 1240505903          # Öğrenci numarasının tamamını buraya yaz (örn: 20210003)
N = 100_000             # Veri boyutu: son rakam 3 < 5 → 10^5
CONDITION = lambda x: x % 7 == 0   # "Özel" eleman koşulu: mod 7 = 0


def generate_data(n: int = N, seed: int = STUDENT_ID) -> list[int]:
    """
    Seed'li rastgele sayı üreticisiyle n elemanlı bir liste döndürür.
    Elemanlar 1 ile 10*n arasında rastgele tam sayılardır.
    """
    rng = random.Random(seed)
    data = [rng.randint(1, 10 * n) for _ in range(n)]
    return data


def get_special_indices(data: list[int]) -> list[int]:
    """
    Koşulu sağlayan (mod 7 = 0) elemanların indekslerini döndürür.
    """
    return [i for i, x in enumerate(data) if CONDITION(x)]


def dataset_info(data: list[int]) -> dict:
    """
    Veri seti hakkında temel istatistikleri döndürür.
    """
    special = get_special_indices(data)
    return {
        "n": len(data),
        "special_count": len(special),
        "special_ratio": len(special) / len(data),
        "theoretical_ratio": 1 / 7,
        "seed": STUDENT_ID,
    }


if __name__ == "__main__":
    data = generate_data()
    info = dataset_info(data)

    print("=" * 50)
    print("VERİ SETİ BİLGİLERİ")
    print("=" * 50)
    print(f"Toplam eleman sayısı     : {info['n']:,}")
    print(f"Özel eleman sayısı       : {info['special_count']:,}")
    print(f"Gerçek oran (mod7=0)     : {info['special_ratio']:.6f}")
    print(f"Teorik oran  (1/7)       : {info['theoretical_ratio']:.6f}")
    print(f"Seed (öğrenci no)        : {info['seed']}")
    print("=" * 50)
