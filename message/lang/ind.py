from json import loads
from src.utils import Dict2Obj
from colorama import Fore

config = Dict2Obj(loads(open("config.json", "r").read()))


MENU = Dict2Obj({
    "not_available": "Menu tidak tersedia!",
    "menu": (
        f"♯ _{config.prefix}help_ | _{config.prefix}menu_ - Menampilkan menu bot\n"
        f"♯ _{config.prefix}ping_ - Menampilkan ping bot\n"
        f"♯ _{config.prefix}runtime_ - Menampilkan total waktu bot berjalan\n"
        f"♯ _{config.prefix}usage_ - Menampilkan penggunaan perintah bot\n"
        f"♯ _{config.prefix}info_ - Menampilkan informasi bot\n"
        f"♯ _{config.prefix}menu downloader_ - Untuk menampilkan menu downloader\n"
        f"♯ _{config.prefix}menu sticker_ - Untuk menampilkan menu sticker\n"
        f"♯ _{config.prefix}menu image_ - Untuk menampilkan menu image\n"
        f"♯ _{config.prefix}menu group_ - Untuk menampilkan menu group\n"
    ),
    "downloader": (
        f"♯ {config.prefix}tiktok - Mendownload video tiktok\n"
    ),
    "sticker": (
        f"♯ {config.prefix}take - Mengambil stiker\n"
        f"♯ {config.prefix}stiker | {config.prefix}s - Mengubah gambar menjadi stiker\n"
        f"♯ {config.prefix}stikergif | {config.prefix}sgif - Mengubah gif/video menjadi stiker\n"
        f"♯ {config.prefix}achievement | {config.prefix}ach - Membuat achievement genshin dan menjadikannya stiker\n"
    ),
    "image": (
        f"♯ {config.prefix}toanime - Mengubah gambar menjadi anime\n"
        f"♯ {config.prefix}dalle - Mengubah teks menjadi gambar\n"
    ),
    "group": (
        f"♯ {config.prefix}add - Menambahkan seseorang ke dalam grup\n"
        f"♯ {config.prefix}kick - Mengeluarkan seseorang dari grup\n"
        f"♯ {config.prefix}promote - Menjadikan seseorang sebagai admin grup\n"
        f"♯ {config.prefix}demote - Menghapus admin seseorang dari grup\n"
        f"♯ {config.prefix}mentionall - Mention semua member grup\n"
        f"♯ {config.prefix}linkgroup - Mendapatkan link grup\n"
    )
})

USAGE = Dict2Obj({
    "help": f"{config.prefix}help | {config.prefix}menu",
    "ping": f"{config.prefix}ping",
    "usage": (
        f"Perintah: {config.prefix}usage - {config.prefix}penggunaan\n"
        f"Contoh: {config.prefix}usage downloader\n"
    ),
    "not_available": "Perintah yang kamu masukkan tidak ada di dalam daftar perintah yang tersedia",
    "take": (
        f"Balas stiker dengan perintah dibawah\n"
        f"Perintah: {config.prefix}take <author stiker> <pack stiker>\n\n"
        f"Contoh: {config.prefix}take Hitori-Bot @mhankbarbar"
    ),
    "sticker": (
        f"Kirim gambar dengan caption atau balas gambar dengan perintah dibawah\n"
        f"Perintah: {config.prefix}stiker - {config.prefix}s - {config.prefix}sticker"
    ),
    "stickergif": (
        f"Kirim gif/video dengan caption atau balas gif/video dengan perintah dibawah\n"
        f"Perintah: {config.prefix}stikergif - {config.prefix}sgif - {config.prefix}stickergif\n\n"
        f"Catatan: Jika video lebih dari 5 detik, maka akan diambil 5 detik pertama saja"
    ),
    "achievement": (
        f"Perintah: {config.prefix}achievement - {config.prefix}ach - {config.prefix}giachievement\n"
        f"Contoh: {config.prefix}achievement Hitori-Bot adalah bot terbaik yang pernah ada"
    ),
    "toanime": (
        f"Kirim gambar dengan caption atau balas gambar dengan perintah dibawah\n"
        f"Perintah: {config.prefix}jadianime - {config.prefix}toanime"
    ),
    "dalle": (
        f"Perintah: {config.prefix}dalle\n"
        f"Contoh: {config.prefix}dalle Beautiful flowers"
    ),
    "tiktok": (
        f"Perintah: {config.prefix}tiktok - {config.prefix}tt\n"
        f"Contoh: {config.prefix}tiktok https://vt.tiktok.com/xxxxxxxx/"
    ),
    "add": (
        f"Perintah: {config.prefix}add - {config.prefix}tambah\n"
        f"Contoh: {config.prefix}add 628xxxxxxxxxx"
    ),
    "kick": (
        f"Perintah: {config.prefix}kick - {config.prefix}tendang\n"
        f"Contoh: {config.prefix}kick @member-a @member-b"
    ),
    "promote": (
        f"Perintah: {config.prefix}promote\n"
        f"Contoh: {config.prefix}promote @member-a @member-b"
    ),
    "demote": (
        f"Perintah: {config.prefix}demote\n"
        f"Contoh: {config.prefix}demote @admin-a @admin-b"
    ),
    "mentionall": (
        f"Perintah: {config.prefix}mentionall - {config.prefix}everyone - {config.prefix}all\n"
        f"Contoh: {config.prefix}mentionall Halo semua, selamat pagi"
    ),
    "linkgroup": (
        f"Perintah: {config.prefix}linkgroup - {config.prefix}linkgrup - {config.prefix}grouplink\n"
        f"Contoh: {config.prefix}linkgroup"
    ),
    "setgroupicon": (
        f"Kirim gambar dengan caption atau balas gambar dengan perintah dibawah\n"
        f"Perintah: {config.prefix}setgroupicon"
    ),
    "setprefix": (
        f"Perintah: {config.prefix}setprefix\n"
        f"Contoh: {config.prefix}setprefix ?"
    ),
})

PROCESSING = "Sedang diproses..."

ERR = Dict2Obj({
    "bot_not_admin": "Maaf, bot tidak memiliki akses admin",
    "not_admin": "Maaf, kamu bukan admin",
    "not_contact": "Maaf, nomor tidak terdaftar di whatsapp",
    "not_group": "Maaf, perintah ini hanya bisa digunakan di dalam grup",
    "add": "Gagal menambahkan %s ke dalam grup",
    "kick": "Gagal mengeluarkan %s dari grup",
    "not_owner": "Maaf, kamu bukan owner bot"
})

SUCCESS = Dict2Obj({
    "add_member": "Berhasil menambahkan %s ke dalam grup",
    "set_group_icon": "Berhasil mengubah icon grup",
    "set_prefix": "Berhasil mengubah prefix menjadi %s"
})

WELCOME = "Halo @%s, selamat datang di grup %s"
GOODBYE = "Selamat tinggal @%s, xixixi"

CAPTION = Dict2Obj({
    "tiktok": (
        f"👤 *Author*: %s\n"
        f"✦ *Title*: %s\n"
        f"✦ *View(s)*: %s\n"
        f"✦ *Like(s)*: %s\n"
        f"✦ *Comment(s)*: %s\n"
        f"✦ *Share*: %s\n"
        f"✦ *Duration*: %s\n"
        f"♬ *Music Title*: %s\n"
    )
})

INFO = (
    f"Bot ini dibuat menggunakan Python.\n\n"
    f"Owner Bot: {config.owner.split('@')[0]}\n"
    f"Source Code: https://github.com/MhankBarBar/hitori-bot\n\n"
    f"© 2023 by *MhankBarBar* made with ❤️"
)

BANNER = (
    f"{Fore.CYAN}╦ ╦{Fore.WHITE}┬┌┬┐┌─┐┬─┐┬  {Fore.CYAN}╦ ╦{Fore.WHITE}┬ ┬┌─┐┌┬┐┌─┐{Fore.CYAN}╔═╗{Fore.WHITE}┌─┐┌─┐  {Fore.CYAN}╔╗ {Fore.WHITE}┌─┐┌┬┐\n"
    f"{Fore.CYAN}╠═╣{Fore.WHITE}│ │ │ │├┬┘│  {Fore.CYAN}║║║{Fore.WHITE}├─┤├─┤ │ └─┐{Fore.CYAN}╠═╣{Fore.WHITE}├─┘├─┘  {Fore.CYAN}╠╩╗{Fore.WHITE}│ │ │\n"
    f"{Fore.CYAN}╩ ╩{Fore.WHITE}┴ ┴ └─┘┴└─┴  {Fore.CYAN}╚╩╝{Fore.WHITE}┴ ┴┴ ┴ ┴ └─┘{Fore.CYAN}╩ ╩{Fore.WHITE}┴  ┴    {Fore.CYAN}╚═╝{Fore.WHITE}└─┘ ┴"
)
