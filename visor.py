import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="WhatsApp Redmi Viewer", layout="wide")
st.title("📱 Mis Mensajes de WhatsApp")

db_file = 'msgstore.db'

def load_data():
    conn = sqlite3.connect(db_file)
    # Usamos los nombres exactos confirmados en tu diagnóstico
    query = """
    SELECT 
        datetime(timestamp/1000, 'unixepoch', 'localtime') as Fecha,
        chat_row_id as Contacto,
        text_data as Mensaje
    FROM message 
    WHERE text_data IS NOT NULL AND text_data != ''
    ORDER BY timestamp DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

try:
    data = load_data()
    
    # Sidebar para elegir el chat
    contactos = sorted(data['Contacto'].unique())
    contacto_sel = st.sidebar.selectbox("Seleccionar ID de Chat", contactos)
    
    # Filtrar mensajes
    filtro = data[data['Contacto'] == contacto_sel]
    
    st.subheader(f"Chat con ID: {contacto_sel}")
    
    # Mostrar como un chat real
    for _, row in filtro[::-1].iterrows(): # Le damos la vuelta para que el más nuevo esté abajo
        with st.chat_message("user"):
            st.write(row['Mensaje'])
            st.caption(f"📅 {row['Fecha']}")

except Exception as e:
    st.error(f"Algo salió mal: {e}")