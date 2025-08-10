from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import pyodbc
from streamlit_autorefresh import st_autorefresh
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Esta deve ser a primeira linha de comando Streamlit no script
st.set_page_config(page_title="Dinatec", layout="wide", page_icon=":truck:")

# Data padrão (será substituída pela data selecionada pelo usuário)
data_atual = datetime.today().strftime('%Y-%m-%d')

# Inicializar a variável de controle de envio de e-mails
if 'ultima_execucao_email' not in st.session_state:
    st.session_state['ultima_execucao_email'] = datetime.now() - timedelta(minutes=5)

# Função para limpar a tela e atualizar o estado
def limpar_tela():
    st.session_state.captura_concluida = True
    st.session_state.recarregar = True

# Rodapé e botão flutuante
footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
    }
    .main > div {
        padding-bottom: 150px;
    }
    .whatsapp-button {
        position: fixed;
        bottom: 80px;
        right: 20px;
        background-color: #25D366;
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        transition: transform 0.3s;
        text-decoration: none !important;
        border: none;
    }
    .whatsapp-button:hover {
        transform: scale(1.1);
    }
    .whatsapp-icon {
        font-size: 36px;
        color: white;
    }
</style>

<div class="footer">
    Desenvolvido por 🛡️ <a href="https://www.dinatec.com.br" target="_blank">Dinatec</a> | 📩 <a href="mailto:thiago.panuto@dinatec.com.br">Suporte</a>
</div>
<a href="https://wa.me/5516993253920" target="_blank" class="whatsapp-button">
    <i class="fab fa-whatsapp whatsapp-icon"></i>
</a>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
"""
# Configurar o autorefresh para atualizar a página a cada 1 minuto (60000 ms)
st_autorefresh(interval=60000, key='main_refresh')

st.title("Dinatec - Entrega de Mercadorias")

# Campo para seleção de data
col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
with col1:
    data_selecionada = st.date_input(
        "📅 Selecione a data:",
        value=datetime.today(),
        format='DD/MM/YYYY',
        min_value=datetime(2025, 7, 30),
        help="Selecione a data para consultar as entregas"
    )
# Converter a data selecionada para string no formato correto
data_pesquisa = data_selecionada.strftime('%Y-%m-%d')
st.divider()

with col2:
    data_viagem = st.date_input(
        "🚌 Data da Viagem:",
        value=datetime.today(),
        format='DD/MM/YYYY',
        help="Selecione a data da viagem"
    )
with col3:
    tipo_veiculo = st.selectbox(
        "🚚 Tipo de Veículo:",
        options=["Caminhão", "Carro", "Caminhonete", "Moto", "Outro"],
        help="Selecione o tipo de veículo para a entrega"
    )
with col4:
    motorista_veiculo = st.text_input(
        "🚚 Motorista:",
        value="",
        help="Informe o motorista do veículo"
    )
with col5:
    placa_veiculo = st.text_input(
        "🚚 Placa do Veículo:",
        value="",
        help="Informe a placa do veículo"
    )

st.markdown(footer, unsafe_allow_html=True)
st.cache_data.clear()

 