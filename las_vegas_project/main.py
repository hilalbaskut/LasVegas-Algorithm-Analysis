"""
main.py
-------
Las Vegas Algoritması - Ana Program
Öğrenci No: ...03  |  Algoritma: Las Vegas  |  n = 10^5

Çalıştırmak için:
    python main.py
"""

from data_generator import generate_data, dataset_info, STUDENT_ID, N
from las_vegas import las_vegas_search
from analysis import run_experiment, print_report, theoretical_expected_steps, theoretical_stdev, RUNS


def main():
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║         LAS VEGAS ALGORİTMASI - ANA PROGRAM         ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  Öğrenci No Son 2 Hane : 03 (tek → Las Vegas)       ║")
    print(f"║  Veri Boyutu           : n = {N:,}              ║")
    print(f"║  Seed                  : {STUDENT_ID}                           ║")
    print(f"║  Arama Koşulu          : x mod 7 == 0               ║")
    print("╚══════════════════════════════════════════════════════╝")

    # ── 1. Veri seti ────────────────────────────────────────────
    print("\n[1/4] Veri seti oluşturuluyor...")
    data = generate_data()
    info = dataset_info(data)
    print(f"      {info['n']:,} eleman üretildi.")
    print(f"      Koşulu sağlayan eleman sayısı : {info['special_count']:,}  (oran: {info['special_ratio']:.5f})")

    # ── 2. Tek çalıştırma örneği ─────────────────────────────────
    print("\n[2/4] Tek çalıştırma örneği...")
    result = las_vegas_search(data, seed=STUDENT_ID)
    print(f"      Bulunan değer   : {result['found_value']:,}  (indeks: {result['found_index']:,})")
    print(f"      Adım sayısı     : {result['steps']}")
    print(f"      Doğrulama       : {result['found_value']} % 7 = {result['found_value'] % 7}  ✓")

    # ── 3. Teorik değerler ───────────────────────────────────────
    p = info["special_ratio"]
    e_theory = theoretical_expected_steps(p)
    s_theory  = theoretical_stdev(p)
    print(f"\n[3/4] Teorik hesaplar...")
    print(f"      Beklenen adım sayısı  E[X] = 1/p = 1/{p:.5f} = {e_theory:.4f}")
    print(f"      Standart sapma        σ    = √((1-p)/p²)    = {s_theory:.4f}")

    # ── 4. 100 kez çalıştır ve analiz ───────────────────────────
    print(f"\n[4/4] Algoritma {RUNS} kez çalıştırılıyor (farklı seed'lerle)...")
    exp = run_experiment(data, runs=RUNS)

    # ── Rapor ───────────────────────────────────────────────────
    print_report(exp, info)

    # ── Özet tablo ──────────────────────────────────────────────
    print("ÖZET KARŞILAŞTIRMA TABLOSU")
    print("-" * 45)
    print(f"{'Metrik':<28} {'Teorik':>7}  {'Deneysel':>8}")
    print("-" * 45)
    print(f"{'E[X] (beklenen adım)':<28} {e_theory:>7.4f}  {exp['mean_steps']:>8.4f}")
    print(f"{'σ (standart sapma)':<28} {s_theory:>7.4f}  {exp['stdev_steps']:>8.4f}")
    print("-" * 45)
    print()
    print("Las Vegas garantisi: Her çalıştırma %100 doğru sonuç verir.")
    print("Rastgelelik yalnızca SÜRE üzerinde etkilidir, doğrulukta değil.")
    print()


if __name__ == "__main__":
    main()
