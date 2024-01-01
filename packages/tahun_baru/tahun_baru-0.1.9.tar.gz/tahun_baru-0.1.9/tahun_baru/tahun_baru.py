import click
# from playsound import playsound
import platform
import shutil
import os
from datetime import datetime, timedelta
from typing import Text


def format_waktu(selisih: timedelta) -> Text:
    # Ubah selisih waktu ke dalam hari, jam, menit, dan detik
    hari = selisih.days
    jam, detik = divmod(selisih.seconds, 3600)
    menit, detik = divmod(detik, 60)
    data = str(hari).zfill(2), str(jam).zfill(2), str(menit).zfill(2), str(detik).zfill(2)
    return tengah_layar("➡️ ➡️ ➡️ ➡️ ➡️ : 🕛 {} hari, {} jam, {} menit, {} detik".format(data[0], data[1], data[2], data[3]))
     
def tanggal_tahun_baru(tanggal_target):
    return datetime.strptime(f'{tanggal_target} 00:00:00', '%Y-%m-%d %H:%M:%S')

def penghitung_mundur(target_waktu):
    ucapan = tengah_layar("🎉 🎉 🎉 Selamat 🎉 🎉 🎉 Tahun Baru! 🥳 🥳 🥳 🥳 🥳")
    selisih = target_waktu - datetime.now()
    while selisih > timedelta(seconds=0):
        data = format_waktu(selisih)
        click.echo("\r" +  click.style(data, fg=(0, 225, 60)), nl=False)
        selisih = target_waktu - datetime.now()
    click.clear()
    click.echo("\r" + click.style(tengah_layar("🎉 🎉 🎉 Selamat 🎉 🎉 🎉 Tahun Baru! 🥳 🥳 🥳 🥳 🥳"), fg=(6, 250, 202)))
    # playsound('path_to_your_sound_file.mp3')

# memberiskan layar
def bersihkan_layar():
    # Mendeteksi sistem operasi dan membersihkan layar konsol
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# string tepat ditengah
def tengah_layar(text: Text) -> Text:
    terminal_width = shutil.get_terminal_size().columns
    spaces = (terminal_width - len(text)) // 2
    return ' ' * spaces + text

@click.command()
@click.option('-f', help='Format tahun, bulan, dan tanggal. Contoh 2024-01-01')
@click.help_option(help='Menampilkan pesan bantuan dan keluar.')
@click.version_option(version='0.1.9', message="v0.1.9", help="Menampilkan versi saat ini")
def hitung_mundur(f):
    bersihkan_layar()
    buatan = ("Dibuat oleh : Yuhari")
    akun = ("Instagram : @gro_hari")
    for i in range(10):
        click.echo("")
    click.echo(buatan)
    click.echo(akun)
    click.echo("")
    click.echo("")
    click.echo(click.style(tengah_layar("❤️ ❤️ ❤️ ❤️ ❤️  Hitungan mundur tahun baru dimulai... ❤️ ❤️ ❤️ ❤️ ❤️"), fg=(123, 239, 204)))
    # Waktu tujuan berdasarkan input
    penghitung_mundur(tanggal_tahun_baru(f))

if __name__ == '__main__':
    try:
        hitung_mundur()
    except KeyboardInterrupt:
        click.echo("\nHitungan mundur dihentikan.")
