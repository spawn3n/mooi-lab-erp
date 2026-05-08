import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Mooi Lab Cloud", page_icon="🧪")

# Bağlantıyı kur (Secrets'tan çeker)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🧪 Mooi Laboratory Cloud")

try:
    # Veriyi çekmeye çalış
    url = "https://docs.google.com/spreadsheets/d/1gRSbiYEBftt19clNs6KoJYVlr6wSl70_J9sX7B_w07s/edit"
    df = conn.read(spreadsheet=url, worksheet="Formuller")
    
    # Menü tasarımı
    menu = st.sidebar.selectbox("İşlem", ["Listele", "Yeni Ekle"])

    if menu == "Listele":
        st.subheader("📚 Kayıtlı Formüller")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Tablo şu an boş, ilk formülü eklemeye ne dersin?")

    elif menu == "Yeni Ekle":
        st.subheader("➕ Yeni Reçete")
        with st.form("ekle"):
            ad = st.text_input("Formül Adı")
            detay = st.text_area("İçerik")
            gonder = st.form_submit_button("Buluta Gönder")
            
            if gonder and ad:
                yeni = pd.DataFrame([{"Formul_Adi": ad, "Icerik": detay}])
                df = pd.concat([df, yeni], ignore_index=True)
                conn.update(worksheet="Formuller", data=df)
                st.success("Kaydedildi! Sayfayı yenileyebilirsiniz.")

except Exception as e:
    st.error("⚠️ Bağlantı Hatası Detayı:")
    st.code(str(e))
    st.info("İpucu: Google Sheets sekme isminin 'Formuller' olduğundan ve Paylaşım ayarının 'Düzenleyici' olduğundan emin olun.")
