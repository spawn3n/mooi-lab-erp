import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Mooi Lab Cloud", page_icon="🧪", layout="centered")

# --- BAĞLANTI AYARLARI ---
# Senin Excel tablo kimliğin (Linkinden aldım)
SHEET_ID = "1gRSbiYEBftt19clNs6KoJYVlr6wSl70_J9sX7B_w07s"
# Doğrudan CSV formatında okuma linki (En sorunsuz yöntem budur)
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

st.title("🧪 Mooi Laboratory Cloud")
st.markdown("---")

# Veriyi Çekme Fonksiyonu
def verileri_getir():
    try:
        # Cache (önbellek) sorunlarını önlemek için linkin sonuna rastgele sayı ekliyoruz
        url = f"{CSV_URL}&cache={pd.Timestamp.now().timestamp()}"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return pd.DataFrame(columns=["Formul_Adi", "Icerik"])

# Verileri çek
data = verileri_getir()

# --- YAN MENÜ ---
menu = st.sidebar.radio("İşlem Seçin", ["📚 Reçeteleri Gör", "➕ Yeni Formül Ekle"])

if menu == "📚 Reçeteleri Gör":
    st.subheader("Kayıtlı Formüller")
    if not data.empty:
        # Tabloyu daha şık gösterelim
        for index, row in data.iterrows():
            with st.expander(f"🔹 {row['Formul_Adi']}"):
                st.write(f"**İçerik:** {row['Icerik']}")
    else:
        st.info("Henüz kayıtlı formül bulunamadı.")

elif menu == "➕ Yeni Formül Ekle":
    st.subheader("Yeni Formül Kaydı")
    st.info("Şefim, güvenliğiniz için yazma işlemini doğrudan Google Sheets üzerinden yapıyoruz.")
    
    # Doğrudan Google Sheets'e yönlendiren şık bir buton
    tablo_linki = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
    st.link_button("🚀 Google Sheets'i Aç ve Formül Ekle", tablo_linki)
    
    st.write("")
    st.write("---")
    st.caption("Not: Google Sheets'e eklediğiniz formüller, sayfayı yenilediğinizde burada görünecektir.")

# Sayfa Alt Bilgisi
st.sidebar.markdown("---")
st.sidebar.caption("Mooi Laboratory v1.5")
