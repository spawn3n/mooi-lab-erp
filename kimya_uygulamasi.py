import customtkinter as ctk
import os
import json
import re
from tkinter import messagebox, filedialog, Menu
from PIL import Image # Görsel işleme için gerekli kütüphane

# Dosya yolları
PROJE_DIZINI = os.path.dirname(os.path.abspath(__file__))
VERITABANI_DOSYASI = os.path.join(PROJE_DIZINI, "mooi_veritabani.json")
STOK_DOSYASI = os.path.join(PROJE_DIZINI, "mooi_stok.json")
NOTLAR_DOSYASI = os.path.join(PROJE_DIZINI, "mooi_notlar.json")
LOGO_YOLU = os.path.join(PROJE_DIZINI, "logo.png") # Logonun yolu

class MooiLabUygulamasi(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.title("Mooi Laboratory ERP v11.0 - GÖRSEL ARAÜZ")
        self.geometry("1400x950")
        self.configure(fg_color="#000000")

        # --- 🛡️ 15 FORMÜL LİSTESİ (SABİT VE TAM) ---
        self.varsayilan_liste = {
            "Antioksidan Defense (Gece Serumu)": {"kat": "Kozmetik", "icerik": "■ Çamfıstığı Yağı: 20 g\n■ Jojoba Yağı: 42 g\n■ Nar Çekirdeği Yağı: 5 g\n■ Squalane: 31.5 g\n■ Vitamin E: 1 g\n■ Akgünlük Uçucu Yağı: 0.2 g"},
            "Avokadolu Nemlendirici Krem": {"kat": "Kozmetik", "icerik": "■ Saf Su: 69.5 g\n■ Gliserin: 3 g\n■ Avokado Yağı: 10 g\n■ Jojoba Yağı: 5 g\n■ Gliseril Stearat PEG-100: 5 g\n■ Setil Alkol: 2.5 g\n■ Stearik Alkol: 2.5 g\n■ Stearik Asit: 2.5 g"},
            "Akne Kremi": {"kat": "Kozmetik", "icerik": "■ Saf Su: 34 g\n■ Hyaluronic Acid: 0.5 g\n■ Salisilik Asit: 1 g\n■ Allantoin: 1 g\n■ Akgünlük Yağı: 1 g\n■ Üzüm Çekirdeği Yağı: 1 g\n■ Setil Alkol: 2 g\n■ Çay Ağacı Yağı: 2.5 g"},
            "Bronzlaştırıcı Yağ Sprey": {"kat": "Kozmetik", "icerik": "■ Kakao Yağı: 5 g\n■ Hindistan Cevizi Yağı: 7 g\n■ Havuç Yağı: 10 g\n■ Zeytinyağı: 5 g\n■ Üzüm Çekirdeği Yağı: 25 g\n■ Squalene: 17 g\n■ Jojoba Yağı: 10 g"},
            "Cilt Sebum Dengeleyici Tonik": {"kat": "Kozmetik", "icerik": "■ Saf Su: 63 g\n■ Hyaluronic Acid: 0.3 g\n■ Gliserin: 7 g\n■ Aloe Vera Ekstresi: 20 g\n■ Niacidamide: 3 g\n■ Panthenol: 3 g\n■ Betain: 4 g"},
            "Çocuklara Özel Saç Bakım Yağı": {"kat": "Kozmetik", "icerik": "■ Jojoba Yağı: 25 g\n■ Squalane: 20 g\n■ Coco Caprylate: 35 g\n■ Kayısı Çekirdeği Yağı: 3 g\n■ E Vitamini: 0.5 g"},
            "Kaş ve Kirpik Bakım Yağı": {"kat": "Kozmetik", "icerik": "■ Hint Yağı: 2.5 g\n■ Argan Yağı: 25 g\n■ Nar Çekirdeği Yağı: 3.5 g\n■ Sedir Ağacı Yağı: 0.5 g\n■ Biberiye Yağı: 0.2 g"},
            "Leke Kremi (Ölmez Çiçek)": {"kat": "Kozmetik", "icerik": "■ Ölmez Çiçek Hidrosolü: 15 g\n■ Itır Hidrosolü: 1.5 g\n■ Pirinç Kepeği Yağı: 4.5 g\n■ Kuşburnu Yağı: 2.5 g\n■ Portakal Yağı: 1 g\n■ Arbutin: 0.5 g"},
            "Leke Serumu (Advanced)": {"kat": "Kozmetik", "icerik": "■ Gül Suyu: 70 g\n■ Cadı Fındığı Ekstresi: 20 g\n■ Niacinamide: 3 g\n■ Arbutin: 1 g\n■ Panthenol: 5 g\n■ Hyaluronic Acid: 0.5 g\n■ Gliserin: 1.5 g"},
            "Makyaj Temizleme Köpüğü": {"kat": "Kozmetik", "icerik": "■ Saf Su: 76 g\n■ Gliserin: 3 g\n■ Aloe Vera Ekstresi: 5 g\n■ Desil Glikozit: 5 g\n■ Betain: 3 g"},
            "Siyah Nokta ve Akne Serumu": {"kat": "Kozmetik", "icerik": "■ Saf Su: 72.5 g\n■ Desil Glikozit: 4 g\n■ Betain: 3 g\n■ Niacinamide: 2 g\n■ Panthenol: 0.7 g\n■ Aloe Vera Ekstresi: 10 g\n■ Salisilik Asit: 0.5 g"},
            "Torpido Sütü Parlatıcı Sprey": {"kat": "Oto Bakım", "icerik": "■ Saf Su: 248.70 kg\n■ Karbomer: 0.33 kg\n■ Ayçiçek Yağı: 44.20 kg\n■ Komperland KD: 3.32 kg\n■ Gliserin: 3.32 kg\n■ TEA: 0.13 kg"},
            "Araç İçi Temizleme (APC)": {"kat": "Oto Bakım", "icerik": "■ Saf Su: 917.5 kg\n■ LABSA: 20 kg\n■ SLES: 15 kg\n■ Kostik: 12 kg\n■ EDTA: 30 kg\n■ Etil Alkol: 4 kg"},
            "Jant Temizleyici (Konsantre)": {"kat": "Oto Bakım", "icerik": "■ Saf Su: 816 kg\n■ SLES: 24 kg\n■ HEDP: 65 kg\n■ Kostik: 60 kg\n■ Tuz: 35 kg"},
            "Lastik Parlatıcı (Parlak Bitiş)": {"kat": "Oto Bakım", "icerik": "■ Saf Su: 815.27 kg\n■ Glikoz Şurubu: 83.33 kg\n■ Gliserin: 100.00 kg"}
        }

        self.veritabani = self.veri_yukle(VERITABANI_DOSYASI, self.varsayilan_liste)
        self.stok = self.veri_yukle(STOK_DOSYASI, {})
        self.notlar = self.veri_yukle(NOTLAR_DOSYASI, {})
        self.su_anki_urun = None

        self.arayuz_kur()
        self.liste_guncelle()

    def veri_yukle(self, dosya, varsayilan):
        if os.path.exists(dosya):
            with open(dosya, "r", encoding="utf-8") as f:
                try: 
                    data = json.load(f)
                    for k, v in varsayilan.items():
                        if k not in data or len(data[k].get("icerik", "")) < 5:
                            data[k] = v
                    return data
                except: return varsayilan
        return varsayilan

    def arayuz_kur(self):
        # SOL PANEL (MENÜ)
        self.sol_panel = ctk.CTkFrame(self, width=320, fg_color="#0A0A0A", corner_radius=0)
        self.sol_panel.pack(side="left", fill="y")
        
        # --- LOGO ALANI ---
        try:
            raw_img = Image.open(LOGO_YOLU)
            logo_img = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(180, 180))
            self.logo_label = ctk.CTkLabel(self.sol_panel, image=logo_img, text="")
            self.logo_label.pack(pady=20)
        except:
            ctk.CTkLabel(self.sol_panel, text="MOOI", font=("Verdana", 40, "bold"), text_color="#E74C3C").pack(pady=20)

        ctk.CTkLabel(self.sol_panel, text="LABORATORY ERP", font=("Verdana", 14, "bold"), text_color="#5D6D7E").pack(pady=(0, 20))

        # ARAMA VE BUTONLAR
        self.arama_entry = ctk.CTkEntry(self.sol_panel, placeholder_text="🔍 Formül Ara...", fg_color="#1A1A1A", border_color="#E74C3C")
        self.arama_entry.pack(pady=10, padx=20, fill="x")
        self.arama_entry.bind("<KeyRelease>", lambda e: self.liste_guncelle())

        ctk.CTkButton(self.sol_panel, text="+ YENİ FORMÜL / SEGMENT", fg_color="#D4AC0D", hover_color="#B7950B", text_color="#000000", font=("Verdana", 12, "bold"), command=self.yeni_formul_penceresi).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(self.sol_panel, text="📦 STOK & MALİYET", fg_color="#2E86C1", font=("Verdana", 12, "bold"), command=self.stok_paneli).pack(pady=5, padx=20, fill="x")

        self.liste_kutusu = ctk.CTkScrollableFrame(self.sol_panel, width=280, fg_color="transparent")
        self.liste_kutusu.pack(expand=True, fill="both", padx=10, pady=10)

        # SAĞ PANEL (İÇERİK)
        self.sag_panel = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.sag_panel.pack(side="right", expand=True, fill="both")

        # ÜST BİLGİ ALANI
        self.baslik_label = ctk.CTkLabel(self.sag_panel, text="LÜTFEN BİR FORMÜL SEÇİN", font=("Verdana", 20, "bold"), text_color="#E74C3C")
        self.baslik_label.pack(pady=20)

        self.detay_frame = ctk.CTkFrame(self.sag_panel, fg_color="transparent")
        self.detay_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.sonuc_metni = ctk.CTkTextbox(self.detay_frame, font=("Verdana", 17), fg_color="#050505", border_color="#333333", border_width=1, corner_radius=10)
        self.sonuc_metni.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # MALİYET KARTU
        self.aksiyon_frame = ctk.CTkFrame(self.detay_frame, width=240, fg_color="#0F0F0F", corner_radius=15)
        self.aksiyon_frame.pack(side="right", fill="y")
        
        ctk.CTkLabel(self.aksiyon_frame, text="ANALİZ", font=("Verdana", 14, "bold"), text_color="#5D6D7E").pack(pady=15)
        self.maliyet_label = ctk.CTkLabel(self.aksiyon_frame, text="0.00 ₺", font=("Verdana", 28, "bold"), text_color="#2ECC71")
        self.maliyet_label.pack(pady=10)
        ctk.CTkLabel(self.aksiyon_frame, text="Birim Maliyet / g-kg", font=("Verdana", 10)).pack()
        
        ctk.CTkButton(self.aksiyon_frame, text="📄 PDF ÇIKTI AL", fg_color="#C0392B", hover_color="#922B21", command=self.pdf_disa_aktar).pack(pady=30, padx=15, fill="x")

        # NOTLAR ALANI
        ctk.CTkLabel(self.sag_panel, text="Laboratuvar Notları:", font=("Verdana", 12), text_color="#F1C40F").pack(anchor="w", padx=25)
        self.not_kutusu = ctk.CTkTextbox(self.sag_panel, height=120, font=("Consolas", 14), fg_color="#050505", border_color="#E74C3C", border_width=1, text_color="#F1C40F")
        self.not_kutusu.pack(fill="x", padx=20, pady=(5, 10))
        ctk.CTkButton(self.sag_panel, text="NOTU GÜNCELLE", fg_color="#1E8449", command=self.notlari_kaydet).pack(pady=(0, 20))

        # SAĞ TIK MENÜSÜ
        self.sag_tik_menu = Menu(self, tearoff=0, bg="#1A1A1A", fg="white", font=("Verdana", 10))
        self.sag_tik_menu.add_command(label="Düzenle", command=self.seciliyi_duzenle)
        self.sag_tik_menu.add_command(label="Sistemden Sil", command=self.seciliyi_sil)

    def liste_guncelle(self):
        for w in self.liste_kutusu.winfo_children(): w.destroy()
        arama = self.arama_entry.get().lower()
        kategoriler = sorted(list(set(v.get("kat", "Diğer") for v in self.veritabani.values())))
        for kat in kategoriler:
            match_found = any(isim for isim in self.veritabani if self.veritabani[isim].get("kat") == kat and arama in isim.lower())
            if match_found:
                ctk.CTkLabel(self.liste_kutusu, text=f"── {kat.upper()} ──", text_color="#E74C3C", font=("Verdana", 11, "bold")).pack(pady=10)
                for isim in sorted(self.veritabani.keys()):
                    if self.veritabani[isim].get("kat") == kat and arama in isim.lower():
                        btn = ctk.CTkButton(self.liste_kutusu, text=isim, fg_color="transparent", anchor="w", hover_color="#1A1A1A", command=lambda x=isim: self.formul_getir(x))
                        btn.pack(fill="x", padx=5)
                        btn.bind("<Button-3>", lambda e, x=isim: self.menu_goster(e, x))

    def formul_getir(self, isim):
        self.su_anki_urun = isim
        self.baslik_label.configure(text=isim.upper())
        veri = self.veritabani[isim]
        self.sonuc_metni.delete("1.0", "end")
        self.sonuc_metni.insert("1.0", veri['icerik'])
        self.not_kutusu.delete("1.0", "end")
        self.not_kutusu.insert("1.0", self.notlar.get(isim, ""))
        # Maliyet
        m = 0.0
        for s in veri['icerik'].split('\n'):
            if ":" in s:
                try:
                    h = s.split(":")[0].replace("■", "").strip()
                    mik_bul = re.findall(r"[-+]?\d*\.\d+|\d+", s.split(":")[1])
                    if mik_bul and h in self.stok:
                        m += (float(self.stok[h]["fiyat"]) / 1000) * float(mik_bul[0])
                except: continue
        self.maliyet_label.configure(text=f"{m:.2f} ₺")

    def menu_goster(self, event, isim):
        self.sag_tik_hedef = isim
        self.sag_tik_menu.post(event.x_root, event.y_root)

    def seciliyi_duzenle(self):
        isim = self.sag_tik_hedef
        p = ctk.CTkToplevel(self); p.title("Formül Düzenleyici"); p.geometry("600x700"); p.attributes("-topmost", True)
        txt = ctk.CTkTextbox(p, width=550, height=500, font=("Verdana", 14)); txt.pack(pady=20)
        txt.insert("1.0", self.veritabani[isim]["icerik"])
        def kay():
            self.veritabani[isim]["icerik"] = txt.get("1.0", "end-1c")
            with open(VERITABANI_DOSYASI, "w", encoding="utf-8") as f: json.dump(self.veritabani, f, indent=4)
            self.formul_getir(isim); p.destroy()
        ctk.CTkButton(p, text="GÜNCELLEMEYİ KAYDET", fg_color="#1E8449", command=kay).pack()

    def seciliyi_sil(self):
        if messagebox.askyesno("Dikkat", f"{self.sag_tik_hedef} formülü silinecek. Onaylıyor musun?"):
            del self.veritabani[self.sag_tik_hedef]
            with open(VERITABANI_DOSYASI, "w", encoding="utf-8") as f: json.dump(self.veritabani, f, indent=4)
            self.liste_guncelle()

    def stok_paneli(self):
        p = ctk.CTkToplevel(self); p.title("Stok Kayıt Merkezi"); p.geometry("600x700"); p.attributes("-topmost", True)
        fr = ctk.CTkFrame(p); fr.pack(pady=20, fill="x", padx=20)
        e1 = ctk.CTkEntry(fr, placeholder_text="Hammadde Adı", width=200); e1.pack(side="left", padx=5)
        e2 = ctk.CTkEntry(fr, placeholder_text="KG Fiyatı (₺)", width=150); e2.pack(side="left", padx=5)
        def ekle():
            if e1.get():
                self.stok[e1.get()] = {"fiyat": e2.get().replace(",", ".")}
                with open(STOK_DOSYASI, "w") as f: json.dump(self.stok, f)
                p.destroy(); self.stok_paneli()
        ctk.CTkButton(fr, text="EKLE", width=80, fg_color="#2E86C1", command=ekle).pack(side="left", padx=5)

    def yeni_formul_penceresi(self):
        p = ctk.CTkToplevel(self); p.title("Yeni Kayıt"); p.geometry("650x850"); p.attributes("-topmost", True)
        ctk.CTkLabel(p, text="Ürün İsmi:").pack(pady=(15,0))
        en = ctk.CTkEntry(p, width=450); en.pack(pady=5)
        ctk.CTkLabel(p, text="Segment (Yeni segment yazabilirsin):").pack(pady=(10,0))
        katlar = sorted(list(set(v.get("kat", "Kozmetik") for v in self.veritabani.values())))
        ek = ctk.CTkComboBox(p, values=katlar, width=450); ek.pack(pady=5)
        ctk.CTkLabel(p, text="İçerik Listesi:").pack(pady=(10,0))
        ti = ctk.CTkTextbox(p, width=550, height=450); ti.pack(pady=5)
        def kay():
            if en.get() and ek.get():
                self.veritabani[en.get()] = {"kat": ek.get(), "icerik": ti.get("1.0", "end-1c")}
                with open(VERITABANI_DOSYASI, "w", encoding="utf-8") as f: json.dump(self.veritabani, f, indent=4)
                self.liste_guncelle(); p.destroy()
        ctk.CTkButton(p, text="SİSTEME İŞLE", fg_color="#1E8449", height=40, command=kay).pack(pady=20)

    def notlari_kaydet(self):
        if self.su_anki_urun:
            self.notlar[self.su_anki_urun] = self.not_kutusu.get("1.0", "end-1c")
            with open(NOTLAR_DOSYASI, "w") as f: json.dump(self.notlar, f)
            messagebox.showinfo("Mooi Lab", "Not başarıyla güncellendi.")

    def pdf_disa_aktar(self):
        if self.su_anki_urun:
            f = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"{self.su_anki_urun}_Formul")
            if f:
                with open(f, "w", encoding="utf-8") as file: 
                    file.write(f"MOOI LABORATORY - FORMÜL RAPORU\n{'='*30}\nÜrün: {self.su_anki_urun}\n\nİçerik:\n{self.sonuc_metni.get('1.0', 'end')}")

if __name__ == "__main__":
    app = MooiLabUygulamasi()
    app.mainloop()