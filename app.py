import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Foodie AI Assistant",
    page_icon="🍕",
    layout="wide"
)

st.title("🍕 Foodie AI Assistant")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("🍽️ Menu")
    st.write("🍛 Pav Bhaji")
    st.write("🥘 Chole Bhature")
    st.write("🍕 Pizza")
    st.write("🥭 Mango Lassi")
    st.write("🥞 Masala Dosa")
    st.write("🍚 Biryani")
    st.write("🌭 Vada Pav")
    st.write("🥞 Rava Dosa")
    st.write("🥟 Samosa")

with col2:
    components.html(
        """
        <iframe
        allow="microphone;"
        width="70%"
        height="450"
        src="https://console.dialogflow.com/api-client/demo/embedded/a1ffdf21-85d8-4bdf-9834-ab894a357d80">
        </iframe>
        """,
        height=700
    )