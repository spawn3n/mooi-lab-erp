import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Sayfa Ayarları
st.set_page_config(page_title="Mooi Lab Cloud", page_icon="🧪")

# Senin Google Sheet Linkin (Sadeleştirilmiş hali)
URL = "https://docs.google.com/spreadsheets/d/1gRSbiYEBftt19clNs6KoJYVlr6wSl70_J9sX7B_w07s/edit"

# Başlık
st.title("🧪 Mooi Laboratory Cloud")

# Bağlantı Kurma
conn = st.connection("gsheets", type=GSheetsConnection)

# Veriyi Oku
try:
    # Doğrudan URL ve sekme ismini veriyoruz
    df = conn.read(spreadsheet=URL, worksheet="Formuller", ttl=0)
except Exception as e:
    st.error("⚠️ Bağlantı kurulamadı!")
    st.info(f"Hata Detayı: {e}")
    df = pd.DataFrame(columns=["Formul_Adi", "Icerik"])

# Menü Yapısı
menu = st.sidebar.selectbox("İşlem Seçin", ["Formülleri Listele", "Yeni Formül Ekle"])

if menu == "Formülleri Listele":
    st.subheader("📚 Kayıtlı Reçeteler")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Henüz kayıtlı formül bulunamadı. Lütfen yeni bir tane ekleyin.")

elif menu == "Yeni Formül Ekle":
    st.subheader("➕ Yeni Kayıt")
    with st.form("yeni_formul_formu"):
        ad = st.text_input("Formül Adı")
        icerik = st.text_area("İçerik (Hammadde ve Miktarlar)")
        submit = st.form_submit_button("Buluta Kaydet")
        
        if submit:
            if ad and icerik:
                # Mevcut veriye yeni satırı ekle
                yeni_satir = pd.DataFrame([{"Formul_Adi": ad, "Icerik": icerik}])
                guncel_df = pd.concat([df, yeni_satir], ignore_index=True)
                
                # Google Sheets'e Yaz (Güncelle)
                conn.update(spreadsheet=URL, worksheet="Formuller", data=guncel_df)
                st.success(f"'{ad}' başarıyla kaydedildi!")
                st.balloons()
            else:
                st.warning("Lütfen tüm alanları doldurun.")
