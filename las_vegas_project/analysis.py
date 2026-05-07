"""
analysis.py
-----------
Algoritmayı 100 kez çalıştırır ve şunları ölçer:
  - Ortalama adım sayısı (deneysel E[X])
  - Ortalama çalışma süresi
  - Standart sapma (rastgeleliğin etkisi)
  - Teorik değerle karşılaştırma
"""

import time
import math
import statistics
from data_generator import generate_data, dataset_info, STUDENT_ID
from las_vegas import las_vegas_search

RUNS = 100   # Kaç kez çalıştırılacak


def run_experiment(data: list[int], runs: int = RUNS) -> dict:
    """
    Las Vegas algoritmasını `runs` kez çalıştırır.
    Her çalıştırma farklı seed kullanır (STUDENT_ID + i).

    Döndürür:
        Tüm istatistikleri içeren sözlük
    """
    steps_list = []
    times_list = []

    for i in range(runs):
        seed = STUDENT_ID + i          # Her çalıştırma için farklı ama tekrarlanabilir seed

        start = time.perf_counter()
        result = las_vegas_search(data, seed=seed)
        end = time.perf_counter()

        steps_list.append(result["steps"])
        times_list.append((end - start) * 1_000)   # ms cinsinden

    # İstatistikler
    mean_steps   = statistics.mean(steps_list)
    stdev_steps  = statistics.stdev(steps_list)
    mean_time_ms = statistics.mean(times_list)
    stdev_time   = statistics.stdev(times_list)
    min_steps    = min(steps_list)
    max_steps    = max(steps_list)

    return {
        "runs"         : runs,
        "steps_list"   : steps_list,
        "times_list"   : times_list,
        "mean_steps"   : mean_steps,
        "stdev_steps"  : stdev_steps,
        "mean_time_ms" : mean_time_ms,
        "stdev_time_ms": stdev_time,
        "min_steps"    : min_steps,
        "max_steps"    : max_steps,
    }


def theoretical_expected_steps(p: float) -> float:
    """
    Geometrik dağılım beklentisi: E[X] = 1/p
    p = koşulu sağlayan elemanların oranı ≈ 1/7
    """
    return 1.0 / p


def theoretical_stdev(p: float) -> float:
    """
    Geometrik dağılım standart sapması: σ = sqrt((1-p) / p²)
    """
    return math.sqrt((1 - p) / (p ** 2))


def print_report(exp: dict, info: dict) -> None:
    """
    Sonuçları güzel biçimde yazdırır.
    """
    p = info["special_ratio"]
    e_theory = theoretical_expected_steps(p)
    s_theory  = theoretical_stdev(p)

    print()
    print("=" * 60)
    print("  LAS VEGAS ANALİZ RAPORU")
    print("=" * 60)
    print(f"  Çalıştırma sayısı          : {exp['runs']}")
    print(f"  Veri boyutu (n)            : {info['n']:,}")
    print(f"  Özel eleman oranı (p)      : {p:.6f}  (~1/7 = {1/7:.6f})")
    print()
    print("  ── ADIM SAYISI ──────────────────────────────────")
    print(f"  Deneysel ortalama E[X]     : {exp['mean_steps']:.4f}")
    print(f"  Teorik    E[X] = 1/p       : {e_theory:.4f}")
    print(f"  Fark                       : {abs(exp['mean_steps'] - e_theory):.4f}")
    print()
    print(f"  Deneysel std sapma         : {exp['stdev_steps']:.4f}")
    print(f"  Teorik   std sapma         : {s_theory:.4f}")
    print(f"  Minimum adım               : {exp['min_steps']}")
    print(f"  Maksimum adım              : {exp['max_steps']}")
    print()
    print("  ── ÇALIŞMA SÜRESİ ───────────────────────────────")
    print(f"  Ortalama süre              : {exp['mean_time_ms']:.4f} ms")
    print(f"  Std sapma (süre)           : {exp['stdev_time_ms']:.4f} ms")
    print()
    print("  ── YORUM ────────────────────────────────────────")

    ratio = exp['mean_steps'] / e_theory
    if 0.85 <= ratio <= 1.15:
        print("  [OK] Deneysel ortalama teorik değere yakın (±%15 içinde).")
    else:
        print(f"  [!]  Deneysel/Teorik oran: {ratio:.3f}  — beklenmedik sapma!")

    cv = exp['stdev_steps'] / exp['mean_steps']
    print(f"  Varyasyon katsayısı (CV)   : {cv:.4f}  ({cv*100:.1f}%)")
    print("  Yüksek CV → rastgelelik çalışma süresini etkiliyor.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    print("Veri seti oluşturuluyor...")
    data = generate_data()
    info = dataset_info(data)

    print(f"Algoritma {RUNS} kez çalıştırılıyor...")
    exp = run_experiment(data, runs=RUNS)

    print_report(exp, info)
