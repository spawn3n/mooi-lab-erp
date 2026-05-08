import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Mooi Lab Cloud", page_icon="🧪", layout="wide")

st.title("🧪 Mooi Laboratory Cloud")
st.write("Verileriniz Google Sheets üzerinden anlık senkronize ediliyor.")

# Google Sheets Bağlantısı
conn = st.connection("gsheets", type=GSheetsConnection)

# Verileri Google Sheets'ten Çek
# (Secrets içindeki linki kullanır)
try:
    df = conn.read(worksheet="Formuller")
except Exception as e:
    st.error("Veri okuma hatası! Lütfen Secrets içindeki linki ve sayfa adını kontrol edin.")
    df = pd.DataFrame(columns=["Formul_Adi", "Icerik"])

# --- YAN MENÜ ---
menu = st.sidebar.radio("İşlem Seçin", ["Formülleri Listele", "Yeni Formül Ekle"])

if menu == "Formülleri Listele":
    st.header("📚 Kayıtlı Reçeteler")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Henüz kayıtlı formül bulunmuyor.")

elif menu == "Yeni Formül Ekle":
    st.header("➕ Yeni Kayıt Oluştur")
    with st.form("yeni_kayit"):
        ad = st.text_input("Formül/Ürün Adı")
        icerik = st.text_area("İçerik Detayları (Örn: Su %70, Yağ %30)")
        submit = st.form_submit_button("Buluta Kaydet")
        
        if submit:
            if ad and icerik:
                # Yeni veriyi hazırla
                yeni_satir = pd.DataFrame([{"Formul_Adi": ad, "Icerik": icerik}])
                # Mevcut verinin altına ekle
                updated_df = pd.concat([df, yeni_satir], ignore_index=True)
                # Google Sheets'i Güncelle
                conn.update(worksheet="Formuller", data=updated_df)
                st.success(f"'{ad}' başarıyla Google Sheets'e kaydedildi!")
                st.balloons()
            else:
                st.warning("Lütfen tüm alanları doldurun.")
