#!/usr/bin/env python3
import hashlib
import itertools
import os
import sys
import threading
import time
import datetime

# Renkleri tamamen kapat - ANSI kodları çıktıda görünmez
class _Bos:
    def __getattr__(self, _):
        return ""
Fore = Style = _Bos()
WHITE = DIM = RESET = ""

banner = r"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⠀⢰⡆⢘⣆⠀⠀⡆⠀⢸⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⣆⣧⡤⠾⢷⡚⠛⢻⣏⢹⡏⠉⣹⠟⡟⣾⠳⣼⢦⣀⣰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠰⣄⡬⢷⣝⢯⣷⢤⣘⣿⣦⣼⣿⣾⣷⣼⣽⣽⣿⣯⡾⢃⣠⣞⠟⠓⢦⣀⠆⠀⠀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠲⣄⣤⣞⡉⠛⢶⣾⡷⠟⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⡿⢿⡛⠻⠿⣥⣤⣶⠞⠉⢓⣤⡴⢁⠄⠀⠀⠀⠀⠀
⠀⠀⠀⣄⣠⠞⠉⢛⣻⡿⠛⠁⠀⣸⠯⠈⠀⠁⣴⣿⣿⣿⡶⠤⠽⣇⠈⣿⠀⠀⠈⠙⠻⢶⣾⣻⣭⠿⢫⣀⣴⡶⠃⠀⠀
⠀⢤⣀⣜⣉⣩⣽⠿⠋⠀⠀⠀⠀⣿⠈⠀⠀⢸⣿⣿⣿⣿⣀⠀⠀⠸⠇⢸⡇⠀⠀⠀⠀⠀⠘⠛⢶⣶⣾⣻⡯⠄⠀⣠⠄
⠀⠤⠬⢭⣿⣿⠋⠀⠀⠀⠀⠀⠀⢻⡀⠀⠀⠀⢿⣿⣿⣿⡿⠋⠁⠀⠀⣼⠁⠀⠀⠀⠀⠀⢀⣴⣫⣏⣙⠛⠒⠚⠋⠁⠀
⡔⢀⡵⠋⢧⢹⡀⠀⠀⠀⠀⠀⠀⠈⢷⡀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⠀⣠⣾⣿⡛⠛⠛⠓⠦⠀⠀⠀⠀
⣇⠘⠳⠦⠼⠧⠷⣄⣀⠀⠀⠀⠀⠀⠀⠳⢤⣀⠀⠀⠀⠀⠀⢀⣠⠾⠃⠀⠀⠀⣀⣴⣻⣟⡋⠉⠉⢻⠶⠀⠀⠀⠀⠀⠀
⠈⠑⠒⠒⠀⠀⢄⣀⡴⣯⣵⣖⣦⠤⣀⣀⣀⠉⠙⠒⠒⠒⠚⠉⢁⣀⣠⢤⣖⣿⣷⢯⡉⠉⠙⣲⠞⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠙⠣⢤⡞⠉⢉⡿⠒⢻⢿⡿⠭⣭⡭⠿⣿⡿⠒⠻⣯⡷⡄⠉⠳⣬⠷⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠺⠤⣄⣠⡏⠀⠀⡿⠀⠀⠘⡾⠀⢀⣈⡧⠴⠒⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠒⠓⠒⠒⠚⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
BEKLENEN_UZUNLUKLAR = {
    32: "md5",
    40: "sha1",
    64: "sha256",
    128: "sha512",
}
HASH_FUNCS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}
UZUNLUK_FOR_TUR = {v: k for k, v in BEKLENEN_UZUNLUKLAR.items()}

WORDLISTS = ["vastrel_wordlist.txt"]
LOG_FILE = "hash_crack_logs.txt"


class AnimasyonluArayuz:
    def __init__(self):
        self.spinner_karakterleri = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def animasyonlu_yaz(self, metin, hiz=0.02, renk=Fore.WHITE):
        for harf in metin:
            sys.stdout.write(f"{renk}{harf}")
            sys.stdout.flush()
            time.sleep(hiz)
        print(RESET)

    def animasyonlu_input(self, soru, hiz=0.015, renk=Fore.CYAN, prompt_simge="»", prompt_rengi=Fore.YELLOW):
        for harf in soru:
            sys.stdout.write(f"{renk}{harf}")
            sys.stdout.flush()
            time.sleep(hiz)
        return input(f"{RESET} {prompt_rengi}{prompt_simge} {RESET}")

    def progres_bar(self, yuzde, genislik=40, onek=""):
        yuzde = max(0.0, min(100.0, yuzde))
        dolu = int(genislik * yuzde / 100)
        renk = Fore.GREEN if yuzde > 66 else Fore.YELLOW if yuzde > 33 else Fore.RED
        cubuk = f"{renk}{'█' * dolu}{DIM}{'░' * (genislik - dolu)}{RESET}"
        sys.stdout.write(f"\r{onek}{cubuk} %{yuzde:5.1f}")
        sys.stdout.flush()

    def calisirken(self, fonksiyon, *args, mesaj="İşlem yapılıyor", **kwargs):
        sonuc = {}
        hata = {}

        def sarmalayici():
            try:
                sonuc["deger"] = fonksiyon(*args, **kwargs)
            except Exception as exc:
                hata["exc"] = exc

        t = threading.Thread(target=sarmalayici, daemon=True)
        t.start()
        spin = itertools.cycle(self.spinner_karakterleri)
        while t.is_alive():
            sys.stdout.write(f"\r{Fore.CYAN}{next(spin)} {mesaj}... {RESET}")
            sys.stdout.flush()
            time.sleep(0.08)
        t.join()
        if "exc" in hata:
            sys.stdout.write(f"\r{Fore.RED}✗ {mesaj} başarısız.{' ' * 20}\n")
            raise hata["exc"]
        sys.stdout.write(f"\r{Fore.GREEN}✓ {mesaj} tamamlandı.{' ' * 20}\n")
        sys.stdout.flush()
        return sonuc.get("deger")


def hazirla(dosya_yolu):
    if not os.path.isfile(dosya_yolu):
        return None
    return os.path.getsize(dosya_yolu)


def main():
    arayuz = AnimasyonluArayuz()

    arayuz.clear()
    print(WHITE + banner + RESET)
    print(WHITE + "-" * 64 + RESET)
    print(Fore.CYAN + "  Developer : 404invisiblepeople")
    print(Fore.CYAN + "  Group     : Vastrel")
    print(Fore.CYAN + "  Algorithms: MD5 / SHA1 / SHA256 / SHA512")
    print(WHITE + "-" * 64 + RESET)

    hash_value = arayuz.animasyonlu_input(Fore.YELLOW + "\ntarget hash: " + RESET).strip().lower()
    if not hash_value:
        print(Fore.RED + "Hash değeri boş olamaz.")
        raise SystemExit(1)

    tahmin_edilen_tur = BEKLENEN_UZUNLUKLAR.get(len(hash_value))
    if tahmin_edilen_tur:
        hash_type = tahmin_edilen_tur
        print(Fore.CYAN + f"Hash türü tahmini: {hash_type}")
    else:
        print(Fore.YELLOW + "Hash türü otomatik belirlenemedi.")
        hash_type = arayuz.animasyonlu_input(
            Fore.YELLOW + "Hash türü (md5, sha1, sha256, sha512): " + RESET
        ).strip().lower()

    hash_func = HASH_FUNCS.get(hash_type)
    if hash_func is None:
        print(Fore.RED + "Desteklenmeyen hash türü. Geçerli türler: " + ", ".join(HASH_FUNCS))
        raise SystemExit(1)

    beklenen_uzunluk = UZUNLUK_FOR_TUR[hash_type]
    if len(hash_value) != beklenen_uzunluk or any(c not in "0123456789abcdef" for c in hash_value):
        print(
            Fore.YELLOW
            + f"Uyarı: Değer {hash_type.upper()} biçiminde görünmüyor (beklenen uzunluk: {beklenen_uzunluk} karakter)."
        )
        if arayuz.animasyonlu_input(Fore.YELLOW + "Yine de devam edilsin mi? (e/h): " + RESET).strip().lower() != "e":
            raise SystemExit(0)

    print("\n" + WHITE + "-" * 64 + RESET)
    print(Fore.CYAN + f"  Hash türü : {hash_type.upper()}")
    print(Fore.CYAN + f"  Hedef     : {hash_value}")
    print(Fore.CYAN + f"  Wordlist  : {', '.join(WORDLISTS)}")
    print(WHITE + "-" * 64 + RESET)

    # ====================================================================== tarama
    start_time = time.time()
    total_attempts = 0
    found = None
    used_wordlist = None

    for wordlist in WORDLISTS:
        toplam_bayt = arayuz.calisirken(hazirla, wordlist, mesaj=f"{wordlist} yükleniyor")
        if toplam_bayt is None:
            print(Fore.YELLOW + f"Wordlist bulunamadı, atlandı: {wordlist}")
            continue
        if toplam_bayt == 0:
            print(Fore.YELLOW + f"Wordlist boş: {wordlist}")
            continue

        print(Fore.CYAN + f"\nDosya: {wordlist} ({toplam_bayt:,} bayt)")

        islenen_bayt = 0
        son_guncelleme = 0.0

        try:
            with open(wordlist, "rb", buffering=1024 * 1024) as handle:
                for ham_satir in handle:
                    islenen_bayt += len(ham_satir)
                    # NOT: Hashleme orijinal baytlar üzerinden yapılır; decode/encode
                    # turuna sokulmaz. Aksi halde UTF-8 olmayan satırlarda hash
                    # eşleşmeleri kaçırılabilir.
                    candidate_bytes = ham_satir.rstrip(b"\r\n")
                    if not candidate_bytes:
                        continue

                    total_attempts += 1
                    digest = hash_func(candidate_bytes).hexdigest()

                    if digest == hash_value:
                        found = candidate_bytes.decode("utf-8", errors="replace")
                        used_wordlist = wordlist
                        break

                    simdi = time.time()
                    if simdi - son_guncelleme >= 0.05:
                        son_guncelleme = simdi
                        arayuz.progres_bar(islenen_bayt / toplam_bayt * 100, onek="  ")

            arayuz.progres_bar(100.0, onek="  ")
            print()

            if found is not None:
                break

        except OSError as exc:
            print(Fore.RED + f"Dosya okunamadı ({wordlist}): {exc}")

    elapsed = time.time() - start_time

    print("\n" + WHITE + "-" * 64 + RESET)

    if found is not None:
        print(Fore.GREEN + "SONUÇ: Eşleşme bulundu")
        print(Fore.CYAN + f"Hash türü : {hash_type.upper()}")
        print(Fore.CYAN + f"Hash      : {hash_value}")
        print(Fore.CYAN + f"Aday      : {found}")
        print(Fore.CYAN + f"Wordlist  : {used_wordlist}")
    else:
        print(Fore.RED + "SONUÇ: Eşleşme wordlist dosyalarında bulunamadı")

    print(Fore.CYAN + f"Deneme    : {total_attempts:,}")
    print(Fore.CYAN + f"Süre      : {elapsed:.3f} saniye")
    if elapsed > 0:
        print(Fore.CYAN + f"Hız       : {total_attempts / elapsed:,.0f} aday/sn")

    print(WHITE + "-" * 64 + RESET)

    try:
        status = "Bulundu" if found is not None else "Bulunamadı"
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(
                f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] "
                f"{hash_type.upper()} | {hash_value} | {status} | "
                f"Deneme: {total_attempts} | Süre: {elapsed:.3f}s\n"
            )
    except OSError as exc:
        print(Fore.RED + f"Log dosyasına yazılamadı: {exc}")

    input(DIM + "\nÇıkmak için Enter tuşuna basın..." + RESET)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + Fore.YELLOW + "İşlem kullanıcı tarafından durduruldu.")
        raise SystemExit(130)
