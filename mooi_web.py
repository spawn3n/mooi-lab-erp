import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Sayfa Ayarları
st.set_page_config(page_title="Mooi Lab Cloud", page_icon="🧪")

st.title("🧪 Mooi Laboratory Cloud")

# Google Sheets Bağlantısı
conn = st.connection("gsheets", type=GSheetsConnection)

# Verileri Google'dan Çek
url = "BURAYA_KOPYALADIGIN_GOOGLE_SHEETS_LINKINI_YAPISTIR"
data = conn.read(spreadsheet=url, worksheet="Formuller")

# --- MENÜ ---
menu = ["Formülleri Gör", "Yeni Formül Ekle"]
secim = st.sidebar.selectbox("İşlem Seçin", menu)

if secim == "Formülleri Gör":
    st.subheader("📚 Kayıtlı Reçeteler")
    st.dataframe(data)

elif secim == "Yeni Formül Ekle":
    st.subheader("➕ Yeni Kayıt")
    with st.form("kayit_formu"):
        yeni_ad = st.text_input("Formül Adı")
        yeni_icerik = st.text_area("İçerik (Hammadde: Miktar)")
        submit = st.form_submit_button("Buluta Gönder")

        if submit:
            if yeni_ad and yeni_icerik:
                # Mevcut veriye ekle
                yeni_satir = pd.DataFrame([{"Formul_Adi": yeni_ad, "Icerik": yeni_icerik}])
                updated_df = pd.concat([data, yeni_satir], ignore_index=True)
                
                # Google Sheets'e Yaz
                conn.update(spreadsheet=url, worksheet="Formuller", data=updated_df)
                st.success("Veri Google Sheets'e işlendi! Sayfayı yenileyebilirsiniz.")
                st.balloons()
