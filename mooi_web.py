import streamlit as st
import json
import os
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mooi Laboratory ERP", page_icon="🧪", layout="wide")

# --- VERİ TABANI FONKSİYONLARI ---
def veri_yukle(dosya_adi, varsayilan):
    if os.path.exists(dosya_adi):
        with open(dosya_adi, "r", encoding="utf-8") as f:
            return json.load(f)
    return varsayilan

def veri_kaydet(dosya_adi, veri):
    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

# Verileri çek
formuller = veri_yukle("mooi_veritabani.json", {})
stok = veri_yukle("mooi_stok.json", {})

# --- YAN MENÜ (SIDEBAR) ---
st.sidebar.image("logo.png", width=150)
st.sidebar.title("Mooi Lab Panel")
sayfa = st.sidebar.radio("Gitmek istediğiniz bölüm:", ["Formül Görüntüle", "Yeni Formül Ekle", "Stok Yönetimi"])

# --- ANA SAYFA: FORMÜL GÖRÜNTÜLE ---
if sayfa == "Formül Görüntüle":
    st.header("🧪 Kayıtlı Formüller")
    secilen_formul = st.selectbox("Formül Seçin", list(formuller.keys()) if formuller else ["Kayıt yok"])
    
    if secilen_formul != "Kayıt yok":
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"İçerik: {secilen_formul}")
            # Tablo olarak göster
            df = pd.DataFrame(list(formuller[secilen_formul].items()), columns=["Hammadde", "Miktar (%)"])
            st.table(df)
        with col2:
            st.info("Bu formülü PDF olarak dışa aktarabilir veya üretim hesaplaması yapabilirsiniz.")

# --- YENİ FORMÜL EKLE ---
elif sayfa == "Yeni Formül Ekle":
    st.header("➕ Yeni Reçete Oluştur")
    yeni_ad = st.text_input("Formül Adı")
    icerik = st.text_area("İçerikleri yazın (Örn: Su: 70, Gliserin: 5)")
    
    if st.button("Kaydet"):
        if yeni_ad and icerik:
            # Basit bir ayrıştırma mantığı
            parcalar = {}
            for satir in icerik.split(","):
                if ":" in satir:
                    k, v = satir.split(":")
                    parcalar[k.strip()] = v.strip()
            formuller[yeni_ad] = parcalar
            veri_kaydet("mooi_veritabani.json", formuller)
            st.success(f"{yeni_ad} başarıyla buluta kaydedildi!")

# --- STOK YÖNETİMİ ---
elif sayfa == "Stok Yönetimi":
    st.header("📦 Hammadde Stok Durumu")
    # Stok listesini gösteren tablo
    if stok:
        st.write(pd.DataFrame(list(stok.items()), columns=["Hammadde", "Miktar (kg/lt)"]))
    else:
        st.warning("Stokta ürün bulunmuyor.")