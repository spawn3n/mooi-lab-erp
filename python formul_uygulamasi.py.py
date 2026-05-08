import customtkinter as ctk
from PIL import Image
import os

# --- VERİ BÖLÜMÜ (İleride burayı dolduracaksın) ---
# Buradaki yapıyı "Formül Adı": {"icerik": "...", "gorsel": "..."} şeklinde çoğaltabilirsin.
FORMUL_KUTUPHANESI = {
    "Örnek Formül 1": {
        "icerik": "- Madde A (%50)\n- Madde B (%50)",
        "gorsel": "resim1.png" # Bu isimde bir resim dosyası klasörde olmalı
    },
    "Örnek Formül 2": {
        "icerik": "- Bileşen X (%10)\n- Su (%90)",
        "gorsel": "resim2.png"
    }
}

class Uygulama(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("Mooi Kimya Formül Rehberi")
        self.geometry("600x650")

        # 1. Başlık ve Giriş Alanı
        self.label_baslik = ctk.CTkLabel(self, text="Formül İsmi Giriniz", font=("Arial", 18, "bold"))
        self.label_baslik.pack(pady=20)

        self.entry_arama = ctk.CTkEntry(self, width=350, placeholder_text="Aramak istediğiniz formül...")
        self.entry_arama.pack(pady=10)

        # 2. Ara Butonu
        self.btn_ara = ctk.CTkButton(self, text="Formülü Getir", command=self.ara_ve_goster)
        self.btn_ara.pack(pady=10)

        # 3. Sonuç Metin Alanı (İçerik burada görünecek)
        self.text_sonuc = ctk.CTkTextbox(self, width=450, height=150, font=("Arial", 14))
        self.text_sonuc.pack(pady=20)
        self.text_sonuc.insert("0.0", "Sonuçlar burada listelenecek...")

        # 4. Görsel Alanı (Resim burada görünecek)
        self.label_gorsel = ctk.CTkLabel(self, text="[ Görsel Alanı ]", width=300, height=200)
        self.label_gorsel.pack(pady=10)

    def ara_ve_goster(self):
        """Kullanıcının yazdığı ismi kütüphanede arar ve sonuçları ekrana basar."""
        aranan_isim = self.entry_arama.get()

        if aranan_isim in FORMUL_KUTUPHANESI:
            veri = FORMUL_KUTUPHANESI[aranan_isim]
            
            # Metni güncelle
            self.text_sonuc.delete("0.0", "end")
            self.text_sonuc.insert("0.0", f"FORMÜL İÇERİĞİ:\n\n{veri['icerik']}")
            
            # Görseli güncelle
            resim_yolu = veri['gorsel']
            if os.path.exists(resim_yolu):
                img = Image.open(resim_yolu)
                # Resmi ekrana sığacak şekilde boyutlandırıyoruz
                ctk_img = ctk.CTkImage(light_image=img, size=(300, 200))
                self.label_gorsel.configure(image=ctk_img, text="")
            else:
                self.label_gorsel.configure(image=None, text="Resim dosyası bulunamadı!")
        else:
            self.text_sonuc.delete("0.0", "end")
            self.text_sonuc.insert("0.0", "HATA: Formül kütüphanede bulunamadı.")
            self.label_gorsel.configure(image=None, text="[ Görsel Yok ]")

# Programı Başlat
if __name__ == "__main__":
    app = Uygulama()
    app.mainloop()