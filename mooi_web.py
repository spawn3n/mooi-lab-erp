import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Mooi Lab Cloud", page_icon="🧪")

# Bağlantı
conn = st.connection("gsheets", type=GSheetsConnection)

# Veriyi oku
try:
    # ttl=0 yaparak her seferinde en güncel veriyi çekmesini sağlıyoruz
    df = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], worksheet="Formuller", ttl=0)
except Exception as e:
    st.error(f"Bağlantı Kurulamadı! Lütfen E-Tablo sekme isminin 'Formuller' olduğundan emin olun.")
    df = pd.DataFrame(columns=["Formul_Adi", "Icerik"])

st.title("🧪 Mooi Laboratory Cloud")

# Menü
menu = st.sidebar.selectbox("Menü", ["Formülleri Gör", "Yeni Ekle"])

if menu == "Formülleri Gör":
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Tablo şu an boş. Lütfen yeni bir formül ekleyin.")

elif menu == "Yeni Ekle":
    with st.form("ekle_form"):
        ad = st.text_input("Formül Adı")
        icerik = st.text_area("İçerik")
        gonder = st.form_submit_button("Buluta Yaz")
        
        if gonder and ad and icerik:
            yeni_veri = pd.DataFrame([{"Formul_Adi": ad, "Icerik": icerik}])
            guncel_df = pd.concat([df, yeni_veri], ignore_index=True)
            conn.update(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], worksheet="Formuller", data=guncel_df)
            st.success("Başarıyla kaydedildi! 'Formülleri Gör' sekmesine bakabilirsiniz.")
