import random

def tebak_angka():
    angka_rahasia = random.randint(1, 10)
    tebakan = 0
    batas_tebakan = 3

    while tebakan < batas_tebakan:
        user = int(input("Masukkan angka :"))
        if user == angka_rahasia:
            print("Selamat, tebakan anda benar")
            break
        else:
            print("Salah!")
            tebakan += 1
    else:
        print(f"Anda gagal, angka rahasia adalah {angka_rahasia}")