import streamlit as st
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mooi Laboratory ERP", page_icon="🧪", layout="wide")

# --- BULUT BAĞLANTISI ---
SHEET_ID = "1gRSbiYEBftt19clNs6KoJYVlr6wSl70_J9sX7B_w07s"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# Veriyi Google Sheets'ten Çek
@st.cache_data(ttl=10) # 10 saniyede bir günceller
def verileri_yukle():
    try:
        return pd.read_csv(CSV_URL)
    except:
        return pd.DataFrame(columns=["Formul_Adi", "Icerik"])

df_bulut = verileri_yukle()

# --- YAN MENÜ ---
st.sidebar.title("Mooi Lab Panel")
sayfa = st.sidebar.radio("Menü:", ["Formül Görüntüle", "Yeni Formül Ekle"])

# --- ANA SAYFA: FORMÜL GÖRÜNTÜLE ---
if sayfa == "Formül Görüntüle":
    st.header("🧪 Kayıtlı Formüller")
    if not df_bulut.empty:
        secilen_ad = st.selectbox("Formül Seçin", df_bulut["Formul_Adi"].tolist())
        detay = df_bulut[df_bulut["Formul_Adi"] == secilen_ad]["Icerik"].values[0]
        
        st.subheader(f"Reçete: {secilen_ad}")
        st.info(detay)
    else:
        st.warning("Bulutta henüz formül bulunamadı.")

# --- YENİ FORMÜL EKLE ---
elif sayfa == "Yeni Formül Ekle":
    st.header("➕ Yeni Reçete Oluştur")
    st.write("Şefim, verilerinizin güvenliği için yeni formülleri doğrudan Google Sheets'e ekliyoruz.")
    
    tablo_linki = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
    st.link_button("🚀 Google Sheets'i Aç ve Veri Gir", tablo_linki)
    
    st.markdown("""
    **Nasıl Yapılır?**
    1. Yukarıdaki butona tıkla.
    2. Açılan tabloda en alt satıra Formül Adı ve İçeriği yaz.
    3. Buraya dönüp sayfayı yenile, formülün listeye gelecektir!
    """)
