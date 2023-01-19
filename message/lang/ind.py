class Menu:

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def help(self) -> str:
        pesan = (f"{self.prefix}help | {self.prefix}menu - Menampilkan menu bot\n"
                 f"{self.prefix}ping - Menampilkan ping bot\n"
                 f"{self.prefix}take - Mengambil stiker\n"
                 f"{self.prefix}stiker | {self.prefix}s - Mengubah gambar menjadi stiker\n"
                 f"{self.prefix}stikergif | {self.prefix}sgif - Mengubah gif menjadi stiker\n"
                 f"{self.prefix}achievement | {self.prefix}ach - Membuat achievement genshin dan menjadikannya stiker\n"
                 f"{self.prefix}jadianime | {self.prefix}toanime - Mengubah gambar menjadi anime\n"
                 )
        return pesan
