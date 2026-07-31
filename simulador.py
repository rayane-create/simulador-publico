import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página corporativa da Fast Tennis
st.set_page_config(page_title="Fast Tennis - Plataforma Estratégica de Precificação", layout="wide")

# ==========================================
# APLICAÇÃO DA IDENTIDADE VISUAL FAST TENNIS (GUIDELINE 2025)
# Paleta Oficial: Blue FT (#053CD8), Navy FT (#022D8A), Green FT (#0DF205), Green FT Escuro (#00A807)
# ==========================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,700;0,800;1,800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Bw Nista Geometric', 'Montserrat', sans-serif !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #022D8A !important;
            font-weight: 800 !important;
        }

        /* ESTILIZAÇÃO DA SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #022D8A !important;
        }
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #FFFFFF !important;
        }

        /* Selectbox da Sidebar */
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border-radius: 8px !important;
            border: 1px solid #CBD5E0 !important;
            color: #022D8A !important;
            font-weight: 700 !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="select"] * {
            color: #022D8A !important;
        }
        
        /* Botões Padrão Green FT */
        div.stButton > button {
            background-color: #0DF205 !important;
            color: #022D8A !important;
            font-weight: 800 !important;
            border-radius: 20px !important;
            border: none !important;
            padding: 8px 24px !important;
        }
        div.stButton > button:hover {
            background-color: #053CD8 !important;
            color: #FFFFFF !important;
        }

        /* TABELA SUGERIDA - VERDE MAIS FORTE PORÉM TRANSLÚCIDO */
        .tabela-sugerida-box {
            background-color: rgba(13, 242, 5, 0.12);
            padding: 22px 28px;
            border-radius: 12px;
            border-left: 12px solid #00A807;
            margin: 15px 0;
            border-top: 1px solid rgba(0, 168, 7, 0.25);
            border-right: 1px solid rgba(0, 168, 7, 0.25);
            border-bottom: 1px solid rgba(0, 168, 7, 0.25);
            box-shadow: 0 4px 15px rgba(0, 168, 7, 0.15);
        }
        .tabela-sugerida-box h2 {
            margin: 6px 0;
            color: #022D8A !important;
            font-size: 36px !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        /* TABELA SUGERIDA REDUZIDA (QUANDO EXCEÇÃO ATIVADA) */
        .tabela-sugerida-reduzida {
            background-color: #F8F9FA;
            padding: 12px 20px;
            border-radius: 8px;
            border-left: 6px solid #CBD5E0;
            margin: 12px 0;
            border: 1px solid #E2E8F0;
        }
        .tabela-sugerida-reduzida h2 {
            margin: 2px 0;
            color: #6C757D !important;
            font-size: 20px !important;
            font-weight: 700 !important;
        }

        /* TABELA EXCEÇÃO - DESTAQUE GIGANTE */
        .tabela-excecao-box {
            background-color: rgba(13, 242, 5, 0.12);
            padding: 22px 28px;
            border-radius: 12px;
            border-left: 12px solid #00A807;
            margin: 15px 0;
            border-top: 1px solid rgba(0, 168, 7, 0.25);
            border-right: 1px solid rgba(0, 168, 7, 0.25);
            border-bottom: 1px solid rgba(0, 168, 7, 0.25);
            box-shadow: 0 4px 15px rgba(0, 168, 7, 0.18);
        }
        .tabela-excecao-box h2 {
            margin: 6px 0;
            color: #00A807 !important;
            font-size: 36px !important;
            font-weight: 800 !important;
        }

        .card-destaque {
            background-color: #F8F9FA;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 10px 14px;
            margin-top: 4px;
        }

        .card-resumo-unidade {
            background-color: #F0F4FF;
            border: 1px solid #C3D3FC;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 15px;
        }

        .alerta-fino-executivo {
            background-color: #F8F9FA;
            color: #7F1D1D;
            border: 1px solid #FECACA;
            border-left: 4px solid #991B1B;
            padding: 8px 14px;
            font-size: 12.5px;
            font-weight: 600;
            border-radius: 4px;
            margin: 10px 0;
        }

        .box-relatorio-equilibrado {
            background-color: #F8F9FA;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            padding: 12px 16px;
            min-height: 85px !important;
            box-sizing: border-box !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        /* GRÁFICO EXECUTIVO COM PERCENTUAIS EM TODAS AS CLASSES */
        .grafico-executivo-container {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 20px 15px 12px 15px;
            margin-top: 15px;
        }
        .linha-grafico-flex {
            display: flex;
            justify-content: center;
            gap: 30px;
            align-items: flex-end;
            padding-bottom: 0px;
            border-bottom: 2px solid #CBD5E0;
        }
        .barra-coluna-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 85px;
        }
        .barra-empilhada-box {
            width: 52px;
            height: 180px;
            background-color: transparent;
            display: flex;
            flex-direction: column-reverse;
            overflow: hidden;
            border-radius: 4px 4px 0 0;
            border: 1px solid #CBD5E0;
        }
        .segmento-classe {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9px;
            font-weight: 800;
            color: #FFFFFF;
            overflow: hidden;
            text-shadow: 0px 1px 2px rgba(0,0,0,0.6);
        }
        .rotulos-container-fixed {
            display: flex;
            justify-content: center;
            gap: 30px;
            padding-top: 10px;
        }
        .rotulo-unidade-box {
            width: 85px;
            text-align: center;
            font-size: 11px;
            font-weight: 700;
            color: #022D8A;
            line-height: 1.25;
            min-height: 38px;
            display: flex;
            align-items: flex-start;
            justify-content: center;
            padding: 0 2px;
        }
        .tag-similaridade {
            background-color: #022D8A;
            color: #0DF205;
            font-size: 10.5px;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 10px;
            margin-bottom: 6px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# CONTROLE DE AMBIENTE SEGURO (AUTENTICAÇÃO)
# ==========================================

USUARIOS_PERMITIDOS = {"rayane@fasttennis.com.br": "Simulador8734"}

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

def realizar_login():
    email_input = st.session_state["login_email"].strip()
    senha_input = st.session_state["login_senha"]
    if email_input in USUARIOS_PERMITIDOS and USUARIOS_PERMITIDOS[email_input] == senha_input:
        st.session_state["autenticado"] = True
        st.session_state["usuario_logado"] = email_input
        st.rerun()
    else:
        st.error("Credenciais corporativas inválidas.")

if not st.session_state["autenticado"]:
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color:#F8F9FA; padding:30px; border-radius:12px; border-top:6px solid #022D8A; box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
                <h3 style="color:#022D8A; margin-top:0; margin-bottom:5px; font-weight:800;">Acesso Restrito Fast Tennis</h3>
                <p style="color:#6C757D; font-size:13px; margin-bottom:25px;">Insira suas credenciais corporativas autorizadas.</p>
            </div>
        """, unsafe_allow_html=True)
        st.text_input("E-mail Corporativo:", key="login_email")
        st.text_input("Senha de Acesso:", type="password", key="login_senha")
        st.button("Entrar no Sistema", on_click=realizar_login, use_container_width=True)
    st.stop()

# ==========================================
# BANCO DE DADOS REVISADO LINHA A LINHA
# ==========================================
df_existentes = [
    {"Status": "Operando", "Unidade": "Fast Tennis Aguas Claras - Brasília", "Cidade": "Brasília", "Estado": "DF", "Endereço": "Trecho 3 Q 5 - Sul, Brasília - DF, 71936-500", "Quadras": 3, "Renda Média": 20740, "População": 80388, "REGIC": "Metrópole Nacional", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 4", "A++": 0.15, "A+": 0.27, "B1": 0.29},
    {"Status": "Pausada", "Unidade": "Fast Tennis Alphaville - São Paulo", "Cidade": "Barueri", "Estado": "SP", "Endereço": "R. Vicente de Carvalho, 205 - Melville Empresarial II, Barueri - SP, 06485-360", "Quadras": 1, "Renda Média": 27400, "População": 44300, "REGIC": "Grande Metrópole", "Perfil Praça": "Comercial", "Tabela Praticada": "Tabela 5", "A++": 0.27, "A+": 0.23, "B1": 0.21},
    {"Status": "Operando", "Unidade": "Fast Tennis Alto da Boa Vista - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Av. Adolfo Pinheiro, 810 – Santo Amaro, São Paulo/SP", "Quadras": 1, "Renda Média": 23654, "População": 85519, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.20, "A+": 0.24, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Alto de Pinheiros - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Avenida São Gualter, 1023 – Alto de Pinheiros São Paulo/SP", "Quadras": 2, "Renda Média": 23900, "População": 82500, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.22, "A+": 0.23, "B1": 0.15},
    {"Status": "Operando", "Unidade": "Fast Tennis Alto do Ipiranga - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua Engenheiro Américo de Carvalho Ramos, nº 97, Vila Gumercindo, São Paulo/SP", "Quadras": 1, "Renda Média": 19775, "População": 177000, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.16, "A+": 0.20, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Anhanguera - Jundiaí", "Cidade": "Jundiaí", "Estado": "SP", "Endereço": "Rua Aurora Germano de Lemos, 228 – Vila Guarani, Jundiaí/SP", "Quadras": 1, "Renda Média": 11650, "População": 67900, "REGIC": "Capital Regional C", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.06, "A+": 0.10, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Bebedouro - Bebedouro", "Cidade": "Bebedouro", "Estado": "SP", "Endereço": "Av. Osvaldo Perrone 376 - Jardim Progresso, Bebedouro/SP", "Quadras": 2, "Renda Média": 5900, "População": 44900, "REGIC": "Centro Sub-Regional B", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 1", "A++": 0.02, "A+": 0.02, "B1": 0.08},
    {"Status": "Operando", "Unidade": "Fast Tennis Belvedere - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Rua Professor Sylvio Barbosa, 416, bairro Belvedere, Belo Horizonte - MG", "Quadras": 5, "Renda Média": 23100, "População": 63400, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.22, "A+": 0.26, "B1": 0.17},
    {"Status": "Operando", "Unidade": "Fast Tennis Boa Viagem - Recife", "Cidade": "Recife", "Estado": "PE", "Endereço": "Rua Copacabana, 279 - Boa Viagem, Recife/PE", "Quadras": 2, "Renda Média": 12214, "População": 102900, "REGIC": "Capital Regional A", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.08, "A+": 0.14, "B1": 0.16},
    {"Status": "Operando", "Unidade": "Fast Tennis Botafogo - Campinas", "Cidade": "Campinas", "Estado": "SP", "Endereço": "Rua Culto à Ciência, 229, - Boatafogo, Campinas/SP", "Quadras": 1, "Renda Média": 12300, "População": 96574, "REGIC": "Capital Regional A", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.07, "A+": 0.13, "B1": 0.20},
    {"Status": "Operando", "Unidade": "Fast Tennis Brooklin - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua California, 470 - Brooklin - São Paulo/SP", "Quadras": 1, "Renda Média": 29400, "População": 162400, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.30, "A+": 0.27, "B1": 0.15},
    {"Status": "Operando", "Unidade": "Fast Tennis Buritis I - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Av. Engenheiro Carlos Goulart, 971 - Buritis - BH/MG", "Quadras": 3, "Renda Média": 16700, "População": 80900, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.10, "A+": 0.24, "B1": 0.24},
    {"Status": "Operando", "Unidade": "Fast Tennis Calafate - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Rua Pimentel Barbosa, nº 40, Bairro Clafate, Belo Horizonte/MG", "Quadras": 1, "Renda Média": 13100, "População": 121200, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 1", "A++": 0.05, "A+": 0.20, "B1": 0.23},
    {"Status": "Em Implantação", "Unidade": "Fast Tennis Campestre - São Paulo", "Cidade": "Santo André", "Estado": "SP", "Endereço": "Rua Suíça, nº 337 e nº 345, Bairro Parque das Nações, Santo André/SP, CEP: 09210-000", "Quadras": 2, "Renda Média": 10583, "População": 128586, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Não Decidida", "A++": 0.05, "A+": 0.09, "B1": 0.17},
    {"Status": "Operando", "Unidade": "Fast Tennis Campo Belo - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua João Álvares Soares, nº 709, Bairro Campo Belo, São Paulo/SP", "Quadras": 2, "Renda Média": 27328, "População": 117500, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.27, "A+": 0.25, "B1": 0.16},
    {"Status": "Operando", "Unidade": "Fast Tennis Cantareira - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Av. Nova Cantareira 4687 - Tucuruvi, São Paulo/SP - CEP:02341-002", "Quadras": 1, "Renda Média": 11500, "População": 95500, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.06, "A+": 0.12, "B1": 0.14},
    {"Status": "Operando", "Unidade": "Fast Tennis Capim Macio - Natal", "Cidade": "Natal", "Estado": "RN", "Endereço": "R. Valter Fernandes, 1971 - Capim Macio, Natal - RN, 59082-090", "Quadras": 2, "Renda Média": 14700, "População": 64400, "REGIC": "Capital Regional A", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 2", "A++": 0.04, "A+": 0.28, "B1": 0.22},
    {"Status": "Operando", "Unidade": "Fast Tennis Castelo - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Rua Castelo de Alenquer, 40 – Castelo, Belo Horizonte/MG", "Quadras": 1, "Renda Média": 10500, "População": 111575, "REGIC": "Metrópole", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 2", "A++": 0.03, "A+": 0.13, "B1": 0.20},
    {"Status": "Operando", "Unidade": "Fast Tennis Centro São Bernardo - São Bernardo do Campo", "Cidade": "São Bernardo do Campo", "Estado": "SP", "Endereço": "Rua João Pessoa 535 - Centro, São Bernardo do Campo/SP", "Quadras": 1, "Renda Média": 10800, "População": 164300, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.05, "A+": 0.09, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Chácara Inglesa - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "R. Juréia, 1024 - Chácara Inglesa, São Paulo - SP, 04140-110", "Quadras": 1, "Renda Média": 21400, "População": 178712, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.18, "A+": 0.22, "B1": 0.19},
    {"Status": "Operando", "Unidade": "Fast Tennis Chácara Santo Antônio - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "R. Antônio das Chagas, 1263 - Chácara Santo Antônio, São Paulo - SP, 04714-002", "Quadras": 2, "Renda Média": 25795, "População": 78250, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.24, "A+": 0.26, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Cidade Nova - Cidade Nova", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "R. Artur de Sá, 389 - União, Belo Horizonte - MG, 31170-710", "Quadras": 2, "Renda Média": 10969, "População": 123470, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.03, "A+": 0.15, "B1": 0.19},
    {"Status": "Operando", "Unidade": "Fast Tennis Contagem - Contagem", "Cidade": "Contagem", "Estado": "MG", "Endereço": "R. Joaquim Rocha, 71 - Betania, Contagem - MG, 32017-270", "Quadras": 1, "Renda Média": 7860, "População": 73600, "REGIC": "Capital Regional B", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 1", "A++": 0.03, "A+": 0.06, "B1": 0.13},
    {"Status": "Operando", "Unidade": "Fast Tennis Estoril - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Rua Geraldo Vasconcellos - 83 - Estoril, Belo Horizonte/MG", "Quadras": 1, "Renda Média": 12612, "População": 85000, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.06, "A+": 0.17, "B1": 0.20},
    {"Status": "Operando", "Unidade": "Fast Tennis Estrela Sul - Juiz de Fora", "Cidade": "Juiz de Fora", "Estado": "MG", "Endereço": "Rua Luz Interior, 402 – Estrela Sul, Juiz de Fora/MG", "Quadras": 2, "Renda Média": 10480, "População": 113000, "REGIC": "Capital Regional B", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 1", "A++": 0.04, "A+": 0.12, "B1": 0.14},
    {"Status": "Operando", "Unidade": "Fast Tennis Eusébio - Eusébio", "Cidade": "Eusébio", "Estado": "CE", "Endereço": "Av. Eusébio de Queiroz, 2552 - Centro, Eusébio - CE, 61760-000", "Quadras": 2, "Renda Média": 8515, "População": 49972, "REGIC": "Metrópole", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 2", "A++": 0.04, "A+": 0.08, "B1": 0.11},
    {"Status": "Em Implantação", "Unidade": "Fast Tennis Formosa - Formosa", "Cidade": "Formosa", "Estado": "GO", "Endereço": "Rua Antônio P. Dutra, 490 - Quadra 105 - Centro, Formosa - GO, 73801-200", "Quadras": 1, "Renda Média": 7266, "População": 51392, "REGIC": "Centro Sub-Regional", "Perfil Praça": "Residencial", "Tabela Praticada": "Não Decidida", "A++": 0.03, "A+": 0.05, "B1": 0.10},
    {"Status": "Operando", "Unidade": "Fast Tennis General Lecor", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "R. Gen. Lecor, 641 - Ipiranga, São Paulo - SP, 04213-020", "Quadras": 1, "Renda Média": 12568, "População": 143312, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.08, "A+": 0.13, "B1": 0.13},
    {"Status": "Operando", "Unidade": "Fast Tennis Guararapes - Fortaleza", "Cidade": "Fortaleza", "Estado": "CE", "Endereço": "Rua Jornalista César Magalhães, 560 – Guararapes Fortaleza/CE", "Quadras": 3, "Renda Média": 12450, "População": 54706, "REGIC": "Capital Regional A", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 2", "A++": 0.08, "A+": 0.16, "B1": 0.13},
    {"Status": "Operando", "Unidade": "Fast Tennis Indaiatuba - São Paulo", "Cidade": "Indaiatuba", "Estado": "SP", "Endereço": "R. Voluntário João dos Santos, 1140 - Jardim Adriana, Indaiatuba - SP, 13330-230", "Quadras": 1, "Renda Média": 11187, "População": 53898, "REGIC": "Centro Sub-Regional", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 2", "A++": 0.05, "A+": 0.10, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Interlagos - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Av. Atlântica, 4987 - Interlagos, São Paulo - SP, 04772-005", "Quadras": 1, "Renda Média": 10475, "População": 45892, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 4", "A++": 0.06, "A+": 0.09, "B1": 0.14},
    {"Status": "Operando", "Unidade": "Fast Tennis Jardim - São Paulo", "Cidade": "Santo André", "Estado": "SP", "Endereço": "Av. Dom Pedro II, 835 - Jardim, Santo André - SP, 09120-410", "Quadras": 1, "Renda Média": 14195, "População": 128600, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 4", "A++": 0.09, "A+": 0.13, "B1": 0.20},
    {"Status": "Operando", "Unidade": "Fast Tennis Jardim Portal da Colina - Sorocaba", "Cidade": "Sorocaba", "Estado": "SP", "Endereço": "R. Paulo Antônio do Nascimento, 46 - Jardim Portal da Colina, Sorocaba - SP, 18047-400", "Quadras": 2, "Renda Média": 11900, "População": 52624, "REGIC": "Capital Regional B", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 3", "A++": 0.06, "A+": 0.11, "B1": 0.20},
    {"Status": "Operando", "Unidade": "Fast Tennis Jardim Social - Curitiba", "Cidade": "Curitiba", "Estado": "PR", "Endereço": "Av. N. Sra. da Luz, 1359 - Jardim Social, Curitiba - PR, 82520-060", "Quadras": 2, "Renda Média": 18300, "População": 56768, "REGIC": "Metrópole", "Perfil Praça": "Mista Qualificada", "Tabela Praticada": "Tabela 3", "A++": 0.10, "A+": 0.31, "B1": 0.21},
    {"Status": "Operando", "Unidade": "Fast Tennis Lapa - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Avenida José Maria de Faria, 324 – Lapa de Baixo São Paulo/SP", "Quadras": 4, "Renda Média": 14200, "População": 107250, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 4", "A++": 0.08, "A+": 0.15, "B1": 0.19},
    {"Status": "Operando", "Unidade": "Fast Tennis Moema - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Alameda dos Guaramomis, 1251 - Planalto Paulista, São Paulo - SP, 04076-012", "Quadras": 1, "Renda Média": 28900, "População": 143796, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.30, "A+": 0.25, "B1": 0.16},
    {"Status": "Operando", "Unidade": "Fast Tennis Monte Pascal - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua Monte Pascal, 32 – City Lapa, São Paulo/SP", "Quadras": 1, "Renda Média": 21446, "População": 90476, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.18, "A+": 0.23, "B1": 0.17},
    {"Status": "Operando", "Unidade": "Fast Tennis Mooca - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua Siqueira Bueno, 1000 – Belenzinho, São Paulo/SP", "Quadras": 1, "Renda Média": 13400, "População": 147000, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 4", "A++": 0.07, "A+": 0.15, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Morada da Colina - Uberlândia", "Cidade": "Uberlândia", "Estado": "MG", "Endereço": "Avenida Liberdade - 1176 - Uberlândia -MG", "Quadras": 1, "Renda Média": 14528, "População": 54900, "REGIC": "Capital Regional B", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 2", "A++": 0.07, "A+": 0.18, "B1": 0.19},
    {"Status": "Operando", "Unidade": "Fast Tennis Morumbi - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Av. Giovanni Gronchi, 2735 - Jardim Leonor, São Paulo - SP, 05658-070", "Quadras": 1, "Renda Média": 14200, "População": 165700, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.12, "A+": 0.12, "B1": 0.09},
    {"Status": "Operando", "Unidade": "Fast Tennis Nova Aliança Sul - Ribeirão Preto", "Cidade": "Ribeirão Preto", "Estado": "SP", "Endereço": "Uberaba, 165 - Jardim Nova Alianca Sul, Ribeirão Preto - SP, Brasil", "Quadras": 2, "Renda Média": 12900, "População": 90800, "REGIC": "Capital Regional A", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 3", "A++": 0.09, "A+": 0.12, "B1": 0.19},
    {"Status": "Operando", "Unidade": "Fast Tennis Orla da Pampulha - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Av. Otacílio Negrão de Lima 7000 - Bandeirantes, Belo Horizonte/MG - CEP: 31365-450", "Quadras": 4, "Renda Média": 9940, "População": 42149, "REGIC": "Metrópole", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 2", "A++": 0.03, "A+": 0.13, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Pampulha - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Rua José Moura Peçanha 77 - Ouro Preto, Belo Horizonte/MG - CEP: 31330-540", "Quadras": 1, "Renda Média": 11675, "População": 75076, "REGIC": "Metrópole", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 2", "A++": 0.04, "A+": 0.16, "B1": 0.22},
    {"Status": "Operando", "Unidade": "Fast Tennis Parque Piqueri - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua José Tavares Siqueira, 519 - Parque São Jorge, São Paulo - SP, 03085-030", "Quadras": 1, "Renda Média": 12800, "População": 138700, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 4", "A++": 0.08, "A+": 0.14, "B1": 0.14},
    {"Status": "Operando", "Unidade": "Fast Tennis Ponte JK - Brasília", "Cidade": "Brasília", "Estado": "DF", "Endereço": "SCES Trecho 2 Beira Lago - Setor de Clubes Esportivos Sul Trecho 2 - Plano Piloto, Brasília - DF", "Quadras": 3, "Renda Média": 25400, "População": 95617, "REGIC": "Metrópole Nacional", "Perfil Praça": "Comercial", "Tabela Praticada": "Tabela 4", "A++": 0.24, "A+": 0.30, "B1": 0.22},
    {"Status": "Operando", "Unidade": "Fast Tennis Praia do Canto - Vitória", "Cidade": "Vitória", "Estado": "ES", "Endereço": "R. José Teixeira, 191 - Praia do Canto, Vitória - ES, 29055-310", "Quadras": 1, "Renda Média": 16840, "População": 83239, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.16, "A+": 0.16, "B1": 0.17},
    {"Status": "Operando", "Unidade": "Fast Tennis Praia Grande - Praia Grande", "Cidade": "Praia Grande", "Estado": "SP", "Endereço": "Av. Brasil 400 - Boqueirão, Praia Grande/SP - CEP:11701-090", "Quadras": 2, "Renda Média": 8900, "População": 84400, "REGIC": "Capital Regional B", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.03, "A+": 0.06, "B1": 0.15},
    {"Status": "Operando", "Unidade": "FastTennis Radial Leste - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua Pedro Bellegarde, 127 - Tatuapé, São Paulo - SP, 03317-080", "Quadras": 1, "Renda Média": 15700, "População": 146400, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 4", "A++": 0.11, "A+": 0.16, "B1": 0.16},
    {"Status": "Operando", "Unidade": "Fast Tennis Recreio - Rio de Janeiro", "Cidade": "Rio de Janeiro", "Estado": "RJ", "Endereço": "Praça Mozart Firmeza 35 - Recreio dos Bandeirantes, Rio de Janeiro/ RJ - CEP: 22795-365", "Quadras": 1, "Renda Média": 22000, "População": 74360, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.22, "A+": 0.19, "B1": 0.19},
    {"Status": "Operando", "Unidade": "Fast Tennis Rio Claro - São Paulo", "Cidade": "Rio Claro", "Estado": "SP", "Endereço": "Avenida 55 - Jardim Kennedy, Rio Claro - SP, Brasil", "Quadras": 2, "Renda Média": 7400, "População": 72800, "REGIC": "Centro Sub-Regional", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 1", "A++": 0.03, "A+": 0.05, "B1": 0.11},
    {"Status": "Operando", "Unidade": "Fast Tennis Salgado Filho - Curitiba", "Cidade": "Curitiba", "Estado": "PR", "Endereço": "Av. Senador Salgado Filho 5067 - Uberaba, Curitiba/PR", "Quadras": 1, "Renda Média": 8900, "População": 64000, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.03, "A+": 0.10, "B1": 0.12},
    {"Status": "Operando", "Unidade": "Fast Tennis Salto - São Paulo", "Cidade": "Salto", "Estado": "SP", "Endereço": "R. Floriano Peixoto, 2059 - Jardim Sontag, Salto - SP, 13322-150", "Quadras": 1, "Renda Média": 6560, "População": 54900, "REGIC": "Centro Sub-Regional A", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.01, "A+": 0.04, "B1": 0.10},
    {"Status": "Operando", "Unidade": "Fast Tennis Santa Lúcia - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Rua Halley 1105 - Santa Lúcia, Belo Horizonte/MG - CEP: 30360-330", "Quadras": 2, "Renda Média": 19400, "População": 88597, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.16, "A+": 0.24, "B1": 0.20},
    {"Status": "Operando", "Unidade": "Fast Tennis Santana - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua Dr. José Augusto César, 35 - Santana, São Paulo - SP, 02403-080", "Quadras": 2, "Renda Média": 17700, "População": 153100, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.13, "A+": 0.18, "B1": 0.19},
    {"Status": "Operando", "Unidade": "Fast Tennis Santa Rosa - Niterói", "Cidade": "Niterói", "Estado": "RJ", "Endereço": "Rua Ver. Duque Estrada 100 - Santa Rosa, Niterói/RJ - CEP: 24240-210", "Quadras": 1, "Renda Média": 17400, "População": 178510, "REGIC": "Capital Regional A", "Perfil Praça": "Mista Qualificada", "Tabela Praticada": "Tabela 2", "A++": 0.15, "A+": 0.17, "B1": 0.26},
    {"Status": "Operando", "Unidade": "Fast Tennis Santo Amaro", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua João Alfredo 320 - Santo Amaro, São Paulo/SP CEP: 04747-000", "Quadras": 1, "Renda Média": 21100, "População": 82400, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 4", "A++": 0.17, "A+": 0.22, "B1": 0.19},
    {"Status": "Operando", "Unidade": "Fast Tennis São Bento - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Rua Cel. Antônio García de Paiva 46 - São Bento, Belo Horizonte/MG - CEP: 30360-010", "Quadras": 2, "Renda Média": 16700, "População": 127317, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.11, "A+": 0.22, "B1": 0.19},
    {"Status": "Operando", "Unidade": "Fast Tennis São Caetano - São Caetano do Sul", "Cidade": "São Caetano do Sul", "Estado": "SP", "Endereço": "Av. Guido Aliberti 3975 - Mauá, São Caetano do Sul/ SP - CEP: 09521-040", "Quadras": 2, "Renda Média": 10200, "População": 122900, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.04, "A+": 0.08, "B1": 0.17},
    {"Status": "Operando", "Unidade": "Fast Tennis Saúde - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Avenida Miguel Estefno nº 731, Saúde, São Paulo/SP", "Quadras": 1, "Renda Média": 17700, "População": 186000, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.13, "A+": 0.19, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Saul Macedo - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Rua Professor Saul Macedo,77, Belvedere, MG - 30.320-490", "Quadras": 1, "Renda Média": 23100, "População": 63400, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.22, "A+": 0.26, "B1": 0.17},
    {"Status": "Operando", "Unidade": "Fast Tennis Savassi - Belo Horizonte", "Cidade": "Belo Horizonte", "Estado": "MG", "Endereço": "Av. do Contorno, 6539 - Savassi, Belo Horizonte - MG, 30110-043", "Quadras": 1, "Renda Média": 19685, "População": 192365, "REGIC": "Metrópole", "Perfil Praça": "Mista Qualificada", "Tabela Praticada": "Tabela 4", "A++": 0.15, "A+": 0.27, "B1": 0.22},
    {"Status": "Operando", "Unidade": "Fast Tennis Sete Lagoas - Sete Lagoas", "Cidade": "Sete Lagoas", "Estado": "MG", "Endereço": "Rua Paulo Frontin 459 - Centro, Sete Lagoas/MG - CEP: 35700-049", "Quadras": 2, "Renda Média": 12514, "População": 50760, "REGIC": "Capital Regional C", "Perfil Praça": "Mista", "Tabela Praticada": "Tabela 1", "A++": 0.09, "A+": 0.14, "B1": 0.12},
    {"Status": "Operando", "Unidade": "Fast Tennis Setor Bueno - Goiânia", "Cidade": "Goiânia", "Estado": "GO", "Endereço": "R. T-48, 671 - St. Bueno, Goiânia - GO, 74210-190", "Quadras": 1, "Renda Média": 17800, "População": 94500, "REGIC": "Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.09, "A+": 0.28, "B1": 0.22},
    {"Status": "Em Implantação", "Unidade": "Fast Tennis Sinop - Sinop", "Cidade": "Sinop", "Estado": "MT", "Endereço": "Avenida Lino Pavesi, Av. Jardim de Monet, 141, Sinop - MT, 78550-178", "Quadras": 2, "Renda Média": 10243, "População": 44084, "REGIC": "Capital Regional C", "Perfil Praça": "Residencial", "Tabela Praticada": "Não Decidida", "A++": 0.05, "A+": 0.05, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Taquaral - Campinas", "Cidade": "Campinas", "Estado": "SP", "Endereço": "R. Fernão Lopes, 1110 - Taquaral, Campinas - SP, 13087-051", "Quadras": 1, "Renda Média": 12738, "População": 40203, "REGIC": "Capital Regional A", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 3", "A++": 0.08, "A+": 0.14, "B1": 0.20},
    {"Status": "Operando", "Unidade": "Fast Tennis Tirol- Natal", "Cidade": "Natal", "Estado": "RN", "Endereço": "Av. Afonso Pena 863 - Tirol, Natal/RN - CEP: 59020-100", "Quadras": 1, "Renda Média": 15400, "População": 72800, "REGIC": "Capital Regional A", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 2", "A++": 0.08, "A+": 0.23, "B1": 0.17},
    {"Status": "Operando", "Unidade": "Fast Tennis Três Poderes - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "R. Hugo Cacuri, 175 - Instituto de Previdencia, São Paulo - SP, 05578-030", "Quadras": 1, "Renda Média": 18100, "População": 587000, "REGIC": "Grande Metrópole", "Perfil Praça": "Comercial", "Tabela Praticada": "Tabela 4", "A++": 0.19, "A+": 0.18, "B1": 0.17},
    {"Status": "Operando", "Unidade": "Fast Tennis Verbo Divino - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "R. Verbo Divino, 797 - Granja Julieta, São Paulo - SP, 04719-001", "Quadras": 1, "Renda Média": 24800, "População": 77600, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.22, "A+": 0.16, "B1": 0.18},
    {"Status": "Operando", "Unidade": "Fast Tennis Vila Olímpia - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Av. Santo Amaro, 1860 - Vila Olímpia, São Paulo - SP, 04506-002", "Quadras": 1, "Renda Média": 30900, "População": 160900, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.33, "A+": 0.27, "B1": 0.15},
    {"Status": "Operando", "Unidade": "Fast Tennis Vila Sônia", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "R. Domingos Olímpio, 227 - Vila Sonia, São Paulo - SP, 05625-060", "Quadras": 1, "Renda Média": 17315, "População": 115968, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.14, "A+": 0.17, "B1": 0.16},
    {"Status": "Operando", "Unidade": "Fast Tennis Vilhena - Rondônia", "Cidade": "Vilhena", "Estado": "RO", "Endereço": "Av. Rio de Janeiro, 1023 - Novo Tempo, Vilhena - RO, Brasil", "Quadras": 1, "Renda Média": 6100, "População": 42800, "REGIC": "Centro Sub-Regional", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 1", "A++": 0.03, "A+": 0.03, "B1": 0.08},
    {"Status": "Operando", "Unidade": "Fast Tennis Ypiranga - São Paulo", "Cidade": "São Paulo", "Estado": "SP", "Endereço": "Rua Azira Assad Jafet, 22 - Ipiranga, São Paulo - SP, Brasil", "Quadras": 1, "Renda Média": 19000, "População": 120000, "REGIC": "Grande Metrópole", "Perfil Praça": "Residencial", "Tabela Praticada": "Tabela 5", "A++": 0.10, "A+": 0.17, "B1": 0.16}
]

df_base_unidades = pd.DataFrame(df_existentes)
LISTA_NOMES_UNIDADES = ["Selecione..."] + sorted(df_base_unidades["Unidade"].tolist())

TABELAS_OFICIAIS = {
    1: {"tkm": 338, "plus": 329},
    2: {"tkm": 411, "plus": 399},
    3: {"tkm": 470, "plus": 499},
    4: {"tkm": 570, "plus": 599},
    5: {"tkm": 690, "plus": 710}
}

def limpar_nome_unidade(nome):
    """Remove o prefixo 'Fast Tennis ' para exibição limpa nos gráficos."""
    return str(nome).replace("Fast Tennis ", "").strip()

# ==========================================
# SIDEBAR - MENU DROPDOWN NOMES LIMPOS
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding: 10px 0 20px 0;">
            <a href="#" style="background-color:#0DF205; color:#022D8A; padding:10px 24px; border-radius:20px; font-weight:800; text-decoration:none; display:inline-block;">Sair do Sistema</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color:#FFFFFF; font-weight:800; font-size:16px; margin-bottom:5px;'>Filtros de Navegação</p>", unsafe_allow_html=True)
    
    modulo_selecionado = st.selectbox(
        "Selecione o Módulo:",
        [
            "Simulador Precificação Inicial",
            "Simulador Pontos Pré-Definidos",
            "Reavaliação Estratégica"
        ],
        key="modulo_navegacao"
    )
    
    st.markdown("---")
    st.markdown(f"<small style='color:#FFFFFF;'>Sessão Ativa: <b>{st.session_state['usuario_logado']}</b></small>", unsafe_allow_html=True)

# ==============================================================================
# MÓDULO 1: SIMULADOR PRECIFICAÇÃO INICIAL (LAYOUT REORGANIZADO E SIMÉTRICO)
# ==============================================================================
if modulo_selecionado == "Simulador Precificação Inicial":
    
    def limpar_campos_m1():
        st.session_state["val_estado"] = "Selecione..."
        st.session_state["val_cidade"] = ""
        st.session_state["val_populacao"] = 0
        st.session_state["val_classe_a_mais_mais"] = 0.0
        st.session_state["val_classe_a_mais"] = 0.0
        st.session_state["val_classe_b1"] = 0.0
        st.session_state["val_renda_media"] = 0.0
        st.session_state["val_tempo_proxima"] = 0
        st.session_state["val_sem_unidade_proxima"] = False
        st.session_state["val_sem_concorrente"] = False
        st.session_state["val_media_mercado"] = 0.0
        st.session_state["val_viabilidade_bp"] = "Aguardando simulação..."
        st.session_state["val_m1_consideracoes"] = ""

    if "val_estado" not in st.session_state:
        limpar_campos_m1()

    st.title("Simulador Estratégico de Precificação Inicial")
    st.markdown("Diagnóstico e recomendação para novos pontos comerciais não cadastrados na base.")
    st.markdown("---")
    
    st.subheader("1. Dados da Área de Estudo e Mercado")
    st.markdown("<p style='font-size:13.5px; color:#5A6578; margin-bottom:15px;'>Insira os dados geográficos e mercadológicos extraídos da ferramenta oficial.</p>", unsafe_allow_html=True)

    with st.container(border=True):
        c1, c2 = st.columns([1.15, 1])
        with c1:
            # ADICIONADA BORDALATERAL DISCRETA ENTRE AS COLUNAS
            st.markdown("""
                <div style="border-right: 1px solid #E2E8F0; padding-right: 22px;">
                    <p style="color:#022D8A; font-weight:800; font-size:15px; margin-bottom:12px;">Localização & Indicadores de População</p>
                </div>
            """, unsafe_allow_html=True)
            
            sub_c1, sub_c2 = st.columns(2)
            with sub_c1:
                lista_estados = ["Selecione...", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
                estado = st.selectbox("Estado (UF):", lista_estados, key="val_estado")
                populacao = st.number_input("População Total (Área):", min_value=0, step=1, key="val_populacao")
            with sub_c2:
                cidade = st.text_input("Cidade:", placeholder="Digite a cidade...", key="val_cidade")
                renda_media = st.number_input("Renda Média (R$):", min_value=0.0, step=100.0, key="val_renda_media")

            st.write("")
            st.markdown("<p style='color:#022D8A; font-weight:800; font-size:14px; margin-bottom:8px;'>Proporção de Classes de Renda</p>", unsafe_allow_html=True)
            sub_cl1, sub_cl2, sub_cl3 = st.columns(3)
            with sub_cl1:
                classe_a_mais_mais = st.number_input("% Classe A++:", min_value=0.0, max_value=1.0, step=0.01, key="val_classe_a_mais_mais")
            with sub_cl2:
                classe_a_mais = st.number_input("% Classe A+:", min_value=0.0, max_value=1.0, step=0.01, key="val_classe_a_mais")
            with sub_cl3:
                classe_b1 = st.number_input("% Classe B1:", min_value=0.0, max_value=1.0, step=0.01, key="val_classe_b1")

            soma_percentuais = classe_b1 + classe_a_mais + classe_a_mais_mais
            calculo_alvo = int(soma_percentuais * populacao)
            
            st.markdown(f"""
                <div class="card-destaque" style="margin-top:10px;">
                    <span style="color:#6C757D; font-size:11px; font-weight:700; text-transform:uppercase;">🎯 Público Alvo Calculado (B1 + A+ + A++)</span> &nbsp;|&nbsp; 
                    <b style="font-size:16px; color:#022D8A;">{calculo_alvo:,} hab.</b> 
                    <small style="color:#6C757D;">({soma_percentuais*100:.1f}% da área)</small>
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("<p style='color:#022D8A; font-weight:800; font-size:15px; margin-bottom:12px;'>Mercado & Concorrência Local</p>", unsafe_allow_html=True)
            tempo_proxima = st.number_input("Tempo até unidade próxima (min):", min_value=0, step=1, key="val_tempo_proxima")
            sem_unidade_proxima = st.checkbox("Não possui unidades Fast próximas no raio", key="val_sem_unidade_proxima")
            
            st.write("")
            media_mercado = st.number_input("Preço Médio Concorrentes (Plus 1x):", min_value=0.0, step=10.0, key="val_media_mercado")
            sem_concorrente = st.checkbox("Não possui concorrentes na área de estudo", key="val_sem_concorrente")

        st.write("")
        col_btn1, col_btn2 = st.columns([5, 1.2])
        with col_btn2:
            st.button("Limpar Avaliação", on_click=limpar_campos_m1, use_container_width=True)

    dados_preenchidos = (
        estado != "Selecione..." and cidade.strip() != "" and renda_media > 0 and (sem_concorrente or media_mercado > 0)
    )

    if not dados_preenchidos:
        st.info("Aguardando dados. Por favor, preencha as informações para gerar o diagnóstico.")
    else:
        # Lógica das tabelas
        if estado == "SP":
            if renda_media <= 8500.00: tab_min, tab_max = 1, 2
            elif renda_media <= 11500.00: tab_min, tab_max = 2, 3
            elif renda_media <= 16000.00: tab_min, tab_max = 3, 4
            elif renda_media <= 22000.00: tab_min, tab_max = 4, 5
            else: tab_min, tab_max = 5, 5
        else:
            if renda_media <= 9500.00: tab_min, tab_max = 1, 2
            elif renda_media <= 13500.00: tab_min, tab_max = 2, 3
            elif renda_media <= 18000.00: tab_min, tab_max = 3, 4
            elif renda_media <= 25000.00: tab_min, tab_max = 4, 5
            else: tab_min, tab_max = 5, 5

        if populacao < 40000:
            tabela_sugerida = tab_min
        else:
            if calculo_alvo >= 25000: tabela_sugerida = tab_max
            else:
                if soma_percentuais >= 0.40: tabela_sugerida = tab_max
                elif soma_percentuais >= 0.30: tabela_sugerida = int(np.round((tab_min + tab_max) / 2))
                else: tabela_sugerida = tab_min

        precos = {1: 329, 2: 399, 3: 499, 4: 599, 5: 710}
        tkms = {1: 338, 2: 411, 3: 470, 4: 580, 5: 690}

        preco_sugerido = precos[tabela_sugerida]
        tkm_sugerido = tkms[tabela_sugerida]

        aplicar_excecao = st.checkbox("Ativar exceção técnica (Sobrescrever tabela baseada no comportamento de mercado)", key="chk_excecao")

        st.write("")
        if not aplicar_excecao:
            # TABELA SUGERIDA EM PROTAGONISMO GIGANTE
            st.markdown(f"""
                <div class="tabela-sugerida-box">
                    <p style="margin:0; font-size:12px; color:#6C757D; font-weight:bold; text-transform:uppercase; letter-spacing:0.5px;">TABELA SUGERIDA PELO ALGORITMO (PERFIL ECONÔMICO)</p>
                    <h2>Tabela {tabela_sugerida}</h2>
                    <p style="margin:0; font-size:15px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {preco_sugerido},00</b> &nbsp;|&nbsp; TKM: <b>R$ {tkm_sugerido},00</b></p>
                </div>
            """, unsafe_allow_html=True)
            tabela_final = tabela_sugerida
            justificativa_excecao = ""
        else:
            # TABELA SUGERIDA EM ESTILO SECUNDÁRIO/REDUZIDO
            st.markdown(f"""
                <div class="tabela-sugerida-reduzida">
                    <p style="margin:0; font-size:11px; color:#6C757D; font-weight:bold; text-transform:uppercase;">Tabela Sugerida pelo Algoritmo (Referência):</p>
                    <h2>Tabela {tabela_sugerida} <span style="font-size:13px; font-weight:normal; color:#4A5568;">(R$ {preco_sugerido},00 | TKM: R$ {tkm_sugerido},00)</span></h2>
                </div>
            """, unsafe_allow_html=True)

            col_exc1, col_exc2 = st.columns([1, 2])
            with col_exc1:
                tabela_escolhida = st.selectbox("Selecione a Tabela Definitiva:", [1, 2, 3, 4, 5], index=tabela_sugerida - 1, key="val_tabela_excecao")
            with col_exc2:
                justificativa_excecao = st.text_input("Justificativa Estratégica (Obrigatório):", placeholder="Ex: Concorrência com forte posicionamento premium...", key="val_justificativa_excecao")

            tabela_final = tabela_escolhida
            # TABELA EXCEÇÃO EM DESTAQUE GIGANTE
            st.markdown(f"""
                <div class="tabela-excecao-box">
                    <p style="margin:0; font-size:12px; color:#00A807; font-weight:bold; text-transform:uppercase; letter-spacing:0.5px;">TABELA ESCOLHIDA POR DECISÃO TÉCNICA (EXCEÇÃO DEFINITIVA)</p>
                    <h2>Tabela {tabela_final}</h2>
                    <p style="margin:0; font-size:15px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {precos[tabela_final]},00</b> &nbsp;|&nbsp; TKM: <b>R$ {tkms[tabela_final]},00</b></p>
                    {f'<p style="margin:8px 0 0 0; font-size:13px; color:#00A807;"><b>Justificativa:</b> {justificativa_excecao}</p>' if justificativa_excecao else ''}
                </div>
            """, unsafe_allow_html=True)

        preco_ref = precos[tabela_final]
        tkm_ref = tkms[tabela_final]

        if not sem_unidade_proxima and tempo_proxima <= 15 and tempo_proxima > 0:
            st.markdown('<div class="alerta-fino-executivo">Proteção de Rede: Existe unidade próxima em raio inferior a 15 min. Verificar canibalização.</div>', unsafe_allow_html=True)

        st.markdown(f"<small style='color:#6C757D;'>Intervalo de tabelas calculadas (Algoritmo):</small> <b>Tab {tab_min} a {tab_max}</b>", unsafe_allow_html=True)
        
        if sem_concorrente or media_mercado == 0:
            diag, status, rec = "Mercado Exclusivo", "Sem Concorrência Direta", "Oportunidade de captura total da demanda sem pressão concorrencial direta."
            txt_dif = "Sem Concorrente Directo"
        else:
            dif_mercado = (preco_ref - media_mercado) / media_mercado
            txt_dif = f"{dif_mercado*100:+.1f}%"
            if dif_mercado < -0.10: diag, status, rec = "Abaixo da Média Regional", "Preço Abaixo do Mercado", "Avaliar margem para reposicionamento."
            elif dif_mercado <= 0.20: diag, status, rec = "Compatível com o Cenário", "Preço Aderente", "Posicionamento adequado ao mercado."
            else: diag, status, rec = "Muito Acima da Concorrência", "Descolamento de Preço", "Revisão mandatória em Comitê."

        st.write("")
        st.markdown("##### Relatório de Viabilidade de Mercado")
        cv1, cv2, cv3 = st.columns([1.2, 1.2, 1])
        with cv1: 
            st.markdown(f"""
                <div class="box-relatorio-equilibrado">
                    <span style="color:#6C757D; font-size:10px; font-weight:700; text-transform:uppercase;">DIRETRIZ E STATUS</span>
                    <span style="font-size:12px; color:#022D8A; margin-top:3px;"><b>Diretriz:</b> {diag}</span>
                    <span style="font-size:12px; color:#022D8A; margin-top:1px;"><b>Status:</b> {status}</span>
                </div>
            """, unsafe_allow_html=True)
        with cv2: 
            st.markdown(f"""
                <div class="box-relatorio-equilibrado" style="background-color: #FFFDF5; border-left: 3px solid #D69E2E;">
                    <span style="color:#975A16; font-size:10px; font-weight:700; text-transform:uppercase;">RECOMENDAÇÃO</span>
                    <span style="font-size:12px; color:#2D3748; margin-top:3px; line-height:1.3;">{rec}</span>
                </div>
            """, unsafe_allow_html=True)
        with cv3:
            st.markdown(f"""
                <div class="box-relatorio-equilibrado">
                    <span style="color:#6C757D; font-size:10px; font-weight:700; text-transform:uppercase;">DIFERENÇA MERCADO X FAST</span>
                    <span style="font-size:20px; font-weight:800; color:#022D8A; margin-top:2px;">{txt_dif}</span>
                </div>
            """, unsafe_allow_html=True)

        st.write("")
        with st.container(border=True):
            st.markdown("##### Viabilidade de Rentabilidade do Business Plan (BP)")
            cbp1, cb2 = st.columns(2)
            with cbp1:
                st.metric(label="TKM para o BP:", value=f"R$ {tkm_ref},00")
            with cb2:
                viabilidade_bp = st.selectbox(
                    "Status de rentabilidade projetada:", 
                    ["Aguardando simulação...", "Viável (Alinhado às Diretrizes do BP)", "Inviável (Payback projetado superior a 60 meses)", "Margem Líquida abaixo de R$ 10.000,00", "Margem Líquida entre R$ 10.000,00 e R$ 15.000,00", "Margem Líquida entre R$ 15.000,00 e R$ 20.000,00", "Margem Líquida acima de R$ 20.000,00"],
                    key="val_viabilidade_bp"
                )

        # CÁLCULO DE UNIDADES SIMILARES
        st.write("")
        st.markdown("##### Unidades da Rede com Perfil Similar")
        
        linhas_similares_pdf = ""
        barras_html_pdf = ""
        if not df_base_unidades.empty:
            alvo_sp = (estado == "SP")
            df_filtrado = df_base_unidades[df_base_unidades['Estado'].apply(lambda x: x == "SP") == alvo_sp].copy()
            
            if not df_filtrado.empty:
                r_ref = renda_media if renda_media > 0 else 1
                p_ref = populacao if populacao > 0 else 1
                a2_ref = classe_a_mais_mais if classe_a_mais_mais > 0 else 1
                a1_ref = classe_a_mais if classe_a_mais > 0 else 1
                b1_ref = classe_b1 if classe_b1 > 0 else 1
                
                df_filtrado['Distancia'] = np.sqrt(
                    ((df_filtrado['Renda Média'] - renda_media) / r_ref)**2 + 
                    ((df_filtrado['População'] - populacao) / p_ref)**2 +
                    ((df_filtrado['A++'] - classe_a_mais_mais) / a2_ref)**2 +
                    ((df_filtrado['A+'] - classe_a_mais) / a1_ref)**2 +
                    ((df_filtrado['B1'] - classe_b1) / b1_ref)**2
                )
                
                df_filtrado['% Similaridade'] = df_filtrado['Distancia'].apply(
                    lambda d: f"{max(0.0, min(100.0, (1 - d/(d+1.5)) * 100)):.1f}%"
                )
                
                df_ranking = df_filtrado.sort_values(by='Distancia').head(3)
                
                st.dataframe(
                    df_ranking[["Unidade", "Cidade", "Renda Média", "População", "Tabela Praticada", "% Similaridade"]], 
                    use_container_width=True, 
                    hide_index=True
                )

                for _, r in df_ranking.iterrows():
                    linhas_similares_pdf += f"<tr><td style='padding:6px; border:1px solid #ddd;'><b>{r['Unidade']}</b></td><td style='padding:6px; border:1px solid #ddd;'>{r['Tabela Praticada']}</td><td style='padding:6px; border:1px solid #ddd;'>{r['% Similaridade']}</td></tr>"

                # OPÇÃO 1: BARRAS COM PERCENTUAIS EM TODAS AS CLASSES (B1, A+, A++)
                st.write("")
                st.markdown("**Perfil da Renda e Distribuição Social (Soma de 100% da População)**")
                
                colunas_grafico = [
                    {"nome": "Ponto Simulado", "b1": classe_b1 * 100, "ap": classe_a_mais * 100, "app": classe_a_mais_mais * 100, "sim": "Alvo"}
                ]
                for _, r_u in df_ranking.iterrows():
                    colunas_grafico.append({
                        "nome": limpar_nome_unidade(r_u["Unidade"]),
                        "b1": float(r_u["B1"]) * 100,
                        "ap": float(r_u["A+"]) * 100,
                        "app": float(r_u["A++"]) * 100,
                        "sim": r_u["% Similaridade"]
                    })

                barras_html_tela = ""
                rotulos_html_tela = ""

                for item in colunas_grafico:
                    v_b1, v_ap, v_app = item["b1"], item["ap"], item["app"]
                    v_outras = max(0.0, 100.0 - (v_b1 + v_ap + v_app))

                    h_outras = int((v_outras / 100.0) * 180)
                    h_b1 = int((v_b1 / 100.0) * 180)
                    h_ap = int((v_ap / 100.0) * 180)
                    h_app = int((v_app / 100.0) * 180)

                    # Rótulos para TODAS as classes (B1, A+, A++)
                    txt_b1 = f"{v_b1:.0f}%" if v_b1 >= 3 else ""
                    txt_ap = f"{v_ap:.0f}%" if v_ap >= 3 else ""
                    txt_app = f"{v_app:.0f}%" if v_app >= 3 else ""

                    barras_html_tela += f"""<div class="barra-coluna-wrapper"><span class="tag-similaridade">{item['sim']}</span><div class="barra-empilhada-box"><div class="segmento-classe" style="height:{h_outras}px; background-color:#CBD5E0;" title="Outras (C/D/E): {v_outras:.1f}%"></div><div class="segmento-classe" style="height:{h_b1}px; background-color:#053CD8;" title="Classe B1: {v_b1:.1f}%">{txt_b1}</div><div class="segmento-classe" style="height:{h_ap}px; background-color:#0DF205; color:#022D8A;" title="Classe A+: {v_ap:.1f}%">{txt_ap}</div><div class="segmento-classe" style="height:{h_app}px; background-color:#15803D;" title="Classe A++: {v_app:.1f}%">{txt_app}</div></div></div>"""
                    rotulos_html_tela += f"""<div class="rotulo-unidade-box">{item['nome']}</div>"""
                    
                    barras_html_pdf += f"""<div style="flex:1; text-align:center;"><span style="font-size:10px; background:#022D8A; color:#0DF205; font-weight:bold; padding:2px 6px; border-radius:8px; display:inline-block; margin-bottom:4px;">{item['sim']}</span><div style="height:140px; display:flex; flex-direction:column-reverse; justify-content:flex-start; align-items:center; background:#F1F5F9; border-radius:4px; padding:4px;"><div style="height:{h_outras*0.7}px; width:22px; background:#CBD5E0; border-radius:2px; margin-bottom:2px;"></div><div style="height:{h_b1*0.7}px; width:22px; background:#053CD8; border-radius:2px; margin-bottom:2px;"></div><div style="height:{h_ap*0.7}px; width:22px; background:#0DF205; border-radius:2px; margin-bottom:2px;"></div><div style="height:{h_app*0.7}px; width:22px; background:#15803D; border-radius:2px;"></div></div><span style="font-size:10px; color:#2D3748; font-weight:bold; display:block; margin-top:6px;">{item['nome']}</span></div>"""

                st.markdown(f"""<div class="grafico-executivo-container"><p style="margin:0 0 15px 0; font-size:13px; font-weight:800; color:#022D8A; text-transform:uppercase;">Perfil da Renda e Distribuição Social (Soma de 100% da População)</p><div class="linha-grafico-flex">{barras_html_tela}</div><div class="rotulos-container-fixed">{rotulos_html_tela}</div><div style="text-align:center; font-size:11px; color:#6C757D; margin-top:15px;"><span style="color:#CBD5E0; font-weight:bold;">■ Outras Classes (C/D/E)</span> &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#053CD8; font-weight:bold;">■ Classe B1 (Base)</span> &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#0DF205; font-weight:bold;">■ Classe A+ (Elevada)</span> &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#15803D; font-weight:bold;">■ Classe A++ (Mais Elevada)</span></div></div>""", unsafe_allow_html=True)

        # CAMPO DE CONSIDERAÇÕES FINAIS DO COMITÊ
        st.write("")
        st.markdown("##### Considerações Finais do Comitê")
        consideracoes_m1 = st.text_area("Insira observações ou parecer técnico para o PDF:", placeholder="Digite aqui comentários sobre o ponto comercial, concorrência ou viabilidade...", height=80, key="val_m1_consideracoes")

        # RELATÓRIO PDF EXECUTIVO COMPLETO
        st.write("")
        st.markdown("---")
        with st.expander("📄 Exportar Relatório Executivo Oficial (PDF)", expanded=False):
            modo_definicao = f"Exceção Técnica ({justificativa_excecao})" if aplicar_excecao else "Análise de Dados do Algoritmo"
            
            html_relatorio = f"""
            <div style="font-family: Arial, sans-serif; background: #ffffff; padding: 25px; border: 1px solid #CBD5E0; border-radius: 8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; background-color:#022D8A; padding:15px 20px; border-radius:6px; color:#ffffff;">
                    <div>
                        <h2 style="color:#ffffff; margin:0; font-size:20px; text-transform:uppercase;">Relatório de Precificação Estratégica</h2>
                        <small style="color:#0DF205; font-weight:bold;">Fast Tennis - Comitê de Precificação</small>
                    </div>
                    <span style="font-size:12px; color:#E2E8F0;">Precificação Inicial</span>
                </div>
                <hr style="border: 0; border-top: 1px solid #cbd5e0; margin: 15px 0;">
                
                <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 20px;">
                    <tr style="background-color:#F8F9FA;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>Praça / Cidade:</b> {cidade} - {estado}</td>
                        <td style="padding:8px; border:1px solid #ddd;"><b>População Total:</b> {populacao:,} hab.</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Renda Média Região:</b> R$ {renda_media:,.2f}</td>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Público Alvo (B1+A+ A++):</b> {calculo_alvo:,} hab. ({soma_percentuais*100:.1f}%)</td>
                    </tr>
                </table>

                <div style="background-color:#F0FDF4; border-left:6px solid #00A807; padding:15px; border-radius:4px; margin-bottom:20px; border:1px solid #BBF7D0;">
                    <h3 style="margin:0; color:#022D8A; font-size:18px;">TABELA SELECIONADA: TABELA {tabela_final}</h3>
                    <p style="margin:4px 0 0 0; font-size:13px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {preco_ref},00</b> | TKM: <b>R$ {tkm_ref},00</b></p>
                    <p style="margin:4px 0 0 0; font-size:11px; color:#6C757D;">Modo de Definição: <b>{modo_definicao}</b></p>
                </div>

                <div style="font-size:12px; line-height:1.5; margin-bottom:20px; background-color:#FFFFFF; padding:12px; border:1px solid #E2E8F0; border-radius:4px;">
                    <p style="margin:0 0 4px 0;"><b>Diretriz Regional:</b> {diag}</p>
                    <p style="margin:0 0 4px 0;"><b>Status de Mercado:</b> {status} (Diferença: {txt_dif})</p>
                    <p style="margin:0 0 4px 0;"><b>Recomendação:</b> {rec}</p>
                    <p style="margin:0 0 0 0;"><b>Status de Rentabilidade Projetada (BP):</b> {viabilidade_bp}</p>
                </div>

                <h4 style="color:#022D8A; margin:15px 0 8px 0; font-size:12px; text-transform:uppercase;">Unidades da Rede com Perfil Similar:</h4>
                <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-bottom: 20px;">
                    <thead>
                        <tr style="background-color:#F8F9FA; text-align:left; color:#022D8A;">
                            <th style="padding:6px; border:1px solid #ddd;">Unidade</th>
                            <th style="padding:6px; border:1px solid #ddd;">Tabela Praticada</th>
                            <th style="padding:6px; border:1px solid #ddd;">% Similaridade</th>
                        </tr>
                    </thead>
                    <tbody>
                        {linhas_similares_pdf}
                    </tbody>
                </table>

                <h4 style="color:#022D8A; margin:15px 0 8px 0; font-size:12px; text-transform:uppercase;">Distribuição Social de Renda (%) e Similaridade:</h4>
                <div style="display:flex; justify-content:space-around; align-items:flex-end; background:#F8F9FA; padding:15px; border-radius:6px; border:1px solid #E2E8F0; margin-bottom:12px;">
                    {barras_html_pdf}
                </div>
                <div style="text-align:center; font-size:10px; color:#6C757D; margin-bottom:20px;">
                    <span style="color:#CBD5E0; font-weight:bold;">■ Outras Classes (C/D/E)</span> &nbsp;&nbsp;
                    <span style="color:#053CD8; font-weight:bold;">■ Classe B1 (Base)</span> &nbsp;&nbsp; 
                    <span style="color:#0DF205; font-weight:bold;">■ Classe A+ (Elevada)</span> &nbsp;&nbsp; 
                    <span style="color:#15803D; font-weight:bold;">■ Classe A++ (Mais Elevada)</span>
                </div>

                {f'''
                <div style="background-color:#FFFDF5; border-left:4px solid #D69E2E; padding:12px; border-radius:4px; margin-bottom:20px;">
                    <h4 style="margin:0 0 4px 0; color:#975A16; font-size:11px; text-transform:uppercase;">Considerações Finais do Comitê:</h4>
                    <p style="margin:0; font-size:12px; color:#2D3748; line-height:1.4;">{consideracoes_m1}</p>
                </div>
                ''' if consideracoes_m1 else ''}

                <button onclick="window.print()" style="background-color: #0DF205; color: #022D8A; border: none; padding: 10px 24px; font-weight: bold; border-radius: 20px; cursor: pointer; font-size:13px;">Imprimir / Salvar PDF Executivo</button>
            </div>
            """
            st.components.v1.html(html_relatorio, height=680, scrolling=True)

# ==============================================================================
# MÓDULO 2: SIMULADOR PONTOS PRÉ-DEFINIDOS
# ==============================================================================
elif modulo_selecionado == "Simulador Pontos Pré-Definidos":
    st.title("Simulador Estratégico para Pontos Pré-Definidos")
    st.markdown("Simulação e definição de tabela para unidades mapeadas com dados demográficos e endereço cadastrados.")
    st.markdown("---")

    def limpar_campos_m1_pre():
        st.session_state["val_pre_unidade"] = "Selecione..."
        st.session_state["val_pre_tempo_proxima"] = 0
        st.session_state["val_pre_sem_unidade_proxima"] = False
        st.session_state["val_pre_sem_concorrente"] = False
        st.session_state["val_pre_media_mercado"] = 0.0
        st.session_state["val_pre_viabilidade_bp"] = "Aguardando simulação..."
        st.session_state["val_m2_consideracoes"] = ""

    if "val_pre_unidade" not in st.session_state:
        limpar_campos_m1_pre()

    st.subheader("1. Seleção da Unidade Mapeada")
    nome_u_pre = st.selectbox("Selecione a Unidade Mapeada:", LISTA_NOMES_UNIDADES, key="val_pre_unidade")

    if nome_u_pre != "Selecione...":
        dados_u_pre = df_base_unidades[df_base_unidades["Unidade"] == nome_u_pre].iloc[0]
        
        estado = dados_u_pre["Estado"]
        cidade = dados_u_pre["Cidade"]
        endereco_pre = dados_u_pre["Endereço"]
        num_quadras_pre = int(dados_u_pre["Quadras"])
        populacao = int(dados_u_pre["População"])
        renda_media = float(dados_u_pre["Renda Média"])
        regic = dados_u_pre["REGIC"]
        tipo_praca = dados_u_pre["Perfil Praça"]
        status_u = dados_u_pre["Status"]

        classe_a_mais_mais = float(dados_u_pre["A++"])
        classe_a_mais = float(dados_u_pre["A+"])
        classe_b1 = float(dados_u_pre["B1"])
        
        soma_percentuais = classe_b1 + classe_a_mais + classe_a_mais_mais
        calculo_alvo = int(soma_percentuais * populacao)

        # RESUMO AUTOMÁTICO DA UNIDADE FORMATADO
        html_card_unidade = f"""
            <div class="card-resumo-unidade">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <h3 style="margin:0; color:#022D8A;">{dados_u_pre['Unidade']} ({cidade} - {estado})</h3>
                    <span style="background-color:#022D8A; color:#0DF205; padding:4px 12px; border-radius:15px; font-weight:800; font-size:12px;">Status: {status_u} | Quadras: {num_quadras_pre}</span>
                </div>
                <p style="margin:0 0 8px 0; font-size:13px; color:#022D8A;"><b>Endereço Cadastrado:</b> {endereco_pre}</p>
                <div style="display:flex; justify-content:space-between; font-size:13px; color:#2D3748; flex-wrap:wrap; gap:10px;">
                    <div><b>População Área:</b> {populacao:,} hab.</div>
                    <div><b>Renda Média:</b> R$ {renda_media:,.2f}</div>
                    <div><b>🎯 Público Alvo (B1+A+ A++):</b> {calculo_alvo:,} hab. ({soma_percentuais*100:.1f}%)</div>
                </div>
            </div>
        """
        st.markdown(html_card_unidade, unsafe_allow_html=True)

        st.subheader("2. Concorrência & Entorno Local")
        with st.container(border=True):
            col_pre1, col_pre2 = st.columns(2)
            with col_pre1:
                tempo_proxima = st.number_input("Tempo até unidade próxima (min):", min_value=0, step=1, key="val_pre_tempo_proxima")
                sem_unidade_proxima = st.checkbox("Não possui unidades Fast próximas no raio", key="val_pre_sem_unidade_proxima")
            with col_pre2:
                media_mercado = st.number_input("Preço Médio Concorrentes (Plus 1x):", min_value=0.0, step=10.0, key="val_pre_media_mercado")
                sem_concorrente = st.checkbox("Não possui concorrentes na área de estudo", key="val_pre_sem_concorrente")

            st.write("")
            col_btn_p1, col_btn_p2 = st.columns([5, 1.2])
            with col_btn_p2:
                st.button("Limpar Avaliação", on_click=limpar_campos_m1_pre, use_container_width=True)

        if sem_concorrente or media_mercado > 0:
            # Lógica das tabelas
            if estado == "SP":
                if renda_media <= 8500.00: tab_min, tab_max = 1, 2
                elif renda_media <= 11500.00: tab_min, tab_max = 2, 3
                elif renda_media <= 16000.00: tab_min, tab_max = 3, 4
                elif renda_media <= 22000.00: tab_min, tab_max = 4, 5
                else: tab_min, tab_max = 5, 5
            else:
                if renda_media <= 9500.00: tab_min, tab_max = 1, 2
                elif renda_media <= 13500.00: tab_min, tab_max = 2, 3
                elif renda_media <= 18000.00: tab_min, tab_max = 3, 4
                elif renda_media <= 25000.00: tab_min, tab_max = 4, 5
                else: tab_min, tab_max = 5, 5

            if populacao < 40000:
                tabela_sugerida = tab_min
            else:
                if calculo_alvo >= 25000: tabela_sugerida = tab_max
                else:
                    if soma_percentuais >= 0.40: tabela_sugerida = tab_max
                    elif soma_percentuais >= 0.30: tabela_sugerida = int(np.round((tab_min + tab_max) / 2))
                    else: tabela_sugerida = tab_min

            precos = {1: 329, 2: 399, 3: 499, 4: 599, 5: 710}
            tkms = {1: 338, 2: 411, 3: 470, 4: 580, 5: 690}

            preco_sugerido = precos[tabela_sugerida]
            tkm_sugerido = tkms[tabela_sugerida]

            aplicar_excecao = st.checkbox("Ativar exceção técnica (Sobrescrever tabela baseada no comportamento de mercado)", key="chk_excecao_pre")

            st.write("")
            if not aplicar_excecao:
                # TABELA SUGERIDA EM PROTAGONISMO GIGANTE
                st.markdown(f"""
                    <div class="tabela-sugerida-box">
                        <p style="margin:0; font-size:12px; color:#6C757D; font-weight:bold; text-transform:uppercase; letter-spacing:0.5px;">TABELA SUGERIDA PELO ALGORITMO (PERFIL ECONÔMICO)</p>
                        <h2>Tabela {tabela_sugerida}</h2>
                        <p style="margin:0; font-size:15px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {preco_sugerido},00</b> &nbsp;|&nbsp; TKM: <b>R$ {tkm_sugerido},00</b></p>
                    </div>
                """, unsafe_allow_html=True)
                tabela_final = tabela_sugerida
                justificativa_excecao = ""
            else:
                # TABELA SUGERIDA REDUZIDA
                st.markdown(f"""
                    <div class="tabela-sugerida-reduzida">
                        <p style="margin:0; font-size:11px; color:#6C757D; font-weight:bold; text-transform:uppercase;">Tabela Sugerida pelo Algoritmo (Referência):</p>
                        <h2>Tabela {tabela_sugerida} <span style="font-size:13px; font-weight:normal; color:#4A5568;">(R$ {preco_sugerido},00 | TKM: R$ {tkm_sugerido},00)</span></h2>
                    </div>
                """, unsafe_allow_html=True)

                col_exc1, col_exc2 = st.columns([1, 2])
                with col_exc1:
                    tabela_escolhida = st.selectbox("Selecione a Tabela Definitiva:", [1, 2, 3, 4, 5], index=tabela_sugerida - 1, key="val_tabela_excecao_pre")
                with col_exc2:
                    justificativa_excecao = st.text_input("Justificativa Estratégica (Obrigatório):", placeholder="Ex: Concorrência com forte posicionamento premium...", key="val_justificativa_excecao_pre")

                tabela_final = tabela_escolhida
                # TABELA EXCEÇÃO EM DESTAQUE GIGANTE
                st.markdown(f"""
                    <div class="tabela-excecao-box">
                        <p style="margin:0; font-size:12px; color:#00A807; font-weight:bold; text-transform:uppercase; letter-spacing:0.5px;">TABELA ESCOLHIDA POR DECISÃO TÉCNICA (EXCEÇÃO DEFINITIVA)</p>
                        <h2>Tabela {tabela_final}</h2>
                        <p style="margin:0; font-size:15px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {precos[tabela_final]},00</b> &nbsp;|&nbsp; TKM: <b>R$ {tkms[tabela_final]},00</b></p>
                        {f'<p style="margin:8px 0 0 0; font-size:13px; color:#00A807;"><b>Justificativa:</b> {justificativa_excecao}</p>' if justificativa_excecao else ''}
                    </div>
                """, unsafe_allow_html=True)

            preco_ref = precos[tabela_final]
            tkm_ref = tkms[tabela_final]

            if not sem_unidade_proxima and tempo_proxima <= 15 and tempo_proxima > 0:
                st.markdown('<div class="alerta-fino-executivo">Proteção de Rede: Existe unidade próxima em raio inferior a 15 min. Verificar canibalização.</div>', unsafe_allow_html=True)

            st.markdown(f"<small style='color:#6C757D;'>Intervalo de tabelas calculadas (Algoritmo):</small> <b>Tab {tab_min} a {tab_max}</b>", unsafe_allow_html=True)
            
            if sem_concorrente or media_mercado == 0:
                diag, status, rec = "Mercado Exclusivo", "Sem Concorrência Direta", "Oportunidade de captura total da demanda sem pressão concorrencial direta."
                txt_dif = "Sem Concorrente Directo"
            else:
                dif_mercado = (preco_ref - media_mercado) / media_mercado
                txt_dif = f"{dif_mercado*100:+.1f}%"
                if dif_mercado < -0.10: diag, status, rec = "Abaixo da Média Regional", "Preço Abaixo do Mercado", "Avaliar margem para reposicionamento."
                elif dif_mercado <= 0.20: diag, status, rec = "Compatível com o Cenário", "Preço Aderente", "Posicionamento adequado ao mercado."
                else: diag, status, rec = "Muito Acima da Concorrência", "Descolamento de Preço", "Revisão mandatória em Comitê."

            st.write("")
            st.markdown("##### Relatório de Viabilidade de Mercado")
            cv1, cv2, cv3 = st.columns([1.2, 1.2, 1])
            with cv1: 
                st.markdown(f"""
                    <div class="box-relatorio-equilibrado">
                        <span style="color:#6C757D; font-size:10px; font-weight:700; text-transform:uppercase;">DIRETRIZ E STATUS</span>
                        <span style="font-size:12px; color:#022D8A; margin-top:3px;"><b>Diretriz:</b> {diag}</span>
                        <span style="font-size:12px; color:#022D8A; margin-top:1px;"><b>Status:</b> {status}</span>
                    </div>
                """, unsafe_allow_html=True)
            with cv2: 
                st.markdown(f"""
                    <div class="box-relatorio-equilibrado" style="background-color: #FFFDF5; border-left: 3px solid #D69E2E;">
                        <span style="color:#975A16; font-size:10px; font-weight:700; text-transform:uppercase;">RECOMENDAÇÃO</span>
                        <span style="font-size:12px; color:#2D3748; margin-top:3px; line-height:1.3;">{rec}</span>
                    </div>
                """, unsafe_allow_html=True)
            with cv3:
                st.markdown(f"""
                    <div class="box-relatorio-equilibrado">
                        <span style="color:#6C757D; font-size:10px; font-weight:700; text-transform:uppercase;">DIFERENÇA MERCADO X FAST</span>
                        <span style="font-size:20px; font-weight:800; color:#022D8A; margin-top:2px;">{txt_dif}</span>
                    </div>
                """, unsafe_allow_html=True)

            st.write("")
            with st.container(border=True):
                st.markdown("##### Viabilidade de Rentabilidade do Business Plan (BP)")
                cbp1, cb2 = st.columns(2)
                with cbp1:
                    st.metric(label="TKM para o BP:", value=f"R$ {tkm_ref},00")
                with cb2:
                    viabilidade_bp = st.selectbox(
                        "Status de rentabilidade projetada:", 
                        ["Aguardando simulação...", "Viável (Alinhado às Diretrizes do BP)", "Inviável (Payback projetado superior a 60 meses)", "Margem Líquida abaixo de R$ 10.000,00", "Margem Líquida entre R$ 10.000,00 e R$ 15.000,00", "Margem Líquida entre R$ 15.000,00 e R$ 20.000,00", "Margem Líquida acima de R$ 20.000,00"],
                        key="val_pre_viabilidade_bp"
                    )

            # CÁLCULO DE UNIDADES SIMILARES
            st.write("")
            st.markdown("##### Unidades da Rede com Perfil Similar")
            
            linhas_similares_pdf_pre = ""
            barras_html_pdf_pre = ""
            if not df_base_unidades.empty:
                alvo_sp = (estado == "SP")
                df_filtrado = df_base_unidades[(df_base_unidades['Estado'].apply(lambda x: x == "SP") == alvo_sp) & (df_base_unidades['Unidade'] != nome_u_pre)].copy()
                
                if not df_filtrado.empty:
                    r_ref = renda_media if renda_media > 0 else 1
                    p_ref = populacao if populacao > 0 else 1
                    a2_ref = classe_a_mais_mais if classe_a_mais_mais > 0 else 1
                    a1_ref = classe_a_mais if classe_a_mais > 0 else 1
                    b1_ref = classe_b1 if classe_b1 > 0 else 1
                    
                    df_filtrado['Distancia'] = np.sqrt(
                        ((df_filtrado['Renda Média'] - renda_media) / r_ref)**2 + 
                        ((df_filtrado['População'] - populacao) / p_ref)**2 +
                        ((df_filtrado['A++'] - classe_a_mais_mais) / a2_ref)**2 +
                        ((df_filtrado['A+'] - classe_a_mais) / a1_ref)**2 +
                        ((df_filtrado['B1'] - classe_b1) / b1_ref)**2
                    )
                    
                    df_filtrado['% Similaridade'] = df_filtrado['Distancia'].apply(
                        lambda d: f"{max(0.0, min(100.0, (1 - d/(d+1.5)) * 100)):.1f}%"
                    )
                    
                    df_ranking = df_filtrado.sort_values(by='Distancia').head(3)
                    
                    st.dataframe(
                        df_ranking[["Unidade", "Cidade", "Renda Média", "População", "Tabela Praticada", "% Similaridade"]], 
                        use_container_width=True, 
                        hide_index=True
                    )

                    for _, r in df_ranking.iterrows():
                        linhas_similares_pdf_pre += f"<tr><td style='padding:6px; border:1px solid #ddd;'><b>{r['Unidade']}</b></td><td style='padding:6px; border:1px solid #ddd;'>{r['Tabela Praticada']}</td><td style='padding:6px; border:1px solid #ddd;'>{r['% Similaridade']}</td></tr>"

                    # OPÇÃO 1 NO MÓDULO 2 (SOMA 100% POPULAÇÃO DIVIDIDA EM 4 CLASSES)
                    st.write("")
                    st.markdown("**Perfil da Renda e Distribuição Social (Soma de 100% da População)**")
                    
                    colunas_grafico_pre = [
                        {"nome": limpar_nome_unidade(dados_u_pre['Unidade']), "b1": classe_b1 * 100, "ap": classe_a_mais * 100, "app": classe_a_mais_mais * 100, "sim": "Alvo"}
                    ]
                    for _, r_u in df_ranking.iterrows():
                        colunas_grafico_pre.append({
                            "nome": limpar_nome_unidade(r_u["Unidade"]),
                            "b1": float(r_u["B1"]) * 100,
                            "ap": float(r_u["A+"]) * 100,
                            "app": float(r_u["A++"]) * 100,
                            "sim": r_u["% Similaridade"]
                        })

                    barras_html_tela_pre = ""
                    rotulos_html_tela_pre = ""

                    for item in colunas_grafico_pre:
                        v_b1, v_ap, v_app = item["b1"], item["ap"], item["app"]
                        v_outras = max(0.0, 100.0 - (v_b1 + v_ap + v_app))

                        h_outras = int((v_outras / 100.0) * 180)
                        h_b1 = int((v_b1 / 100.0) * 180)
                        h_ap = int((v_ap / 100.0) * 180)
                        h_app = int((v_app / 100.0) * 180)

                        txt_b1 = f"{v_b1:.0f}%" if v_b1 >= 3 else ""
                        txt_ap = f"{v_ap:.0f}%" if v_ap >= 3 else ""
                        txt_app = f"{v_app:.0f}%" if v_app >= 3 else ""

                        barras_html_tela_pre += f"""<div class="barra-coluna-wrapper"><span class="tag-similaridade">{item['sim']}</span><div class="barra-empilhada-box"><div class="segmento-classe" style="height:{h_outras}px; background-color:#CBD5E0;" title="Outras (C/D/E): {v_outras:.1f}%"></div><div class="segmento-classe" style="height:{h_b1}px; background-color:#053CD8;" title="Classe B1: {v_b1:.1f}%">{txt_b1}</div><div class="segmento-classe" style="height:{h_ap}px; background-color:#0DF205; color:#022D8A;" title="Classe A+: {v_ap:.1f}%">{txt_ap}</div><div class="segmento-classe" style="height:{h_app}px; background-color:#15803D;" title="Classe A++: {v_app:.1f}%">{txt_app}</div></div></div>"""
                        rotulos_html_tela_pre += f"""<div class="rotulo-unidade-box">{item['nome']}</div>"""
                        
                        barras_html_pdf_pre += f"""<div style="flex:1; text-align:center;"><span style="font-size:10px; background:#022D8A; color:#0DF205; font-weight:bold; padding:2px 6px; border-radius:8px; display:inline-block; margin-bottom:4px;">{item['sim']}</span><div style="height:140px; display:flex; flex-direction:column-reverse; justify-content:flex-start; align-items:center; background:#F1F5F9; border-radius:4px; padding:4px;"><div style="height:{h_outras*0.7}px; width:22px; background:#CBD5E0; border-radius:2px; margin-bottom:2px;"></div><div style="height:{h_b1*0.7}px; width:22px; background:#053CD8; border-radius:2px; margin-bottom:2px;"></div><div style="height:{h_ap*0.7}px; width:22px; background:#0DF205; border-radius:2px; margin-bottom:2px;"></div><div style="height:{h_app*0.7}px; width:22px; background:#15803D; border-radius:2px;"></div></div><span style="font-size:10px; color:#2D3748; font-weight:bold; display:block; margin-top:6px;">{item['nome']}</span></div>"""

                    st.markdown(f"""<div class="grafico-executivo-container"><p style="margin:0 0 15px 0; font-size:13px; font-weight:800; color:#022D8A; text-transform:uppercase;">Perfil da Renda e Distribuição Social (Soma de 100% da População)</p><div class="linha-grafico-flex">{barras_html_tela_pre}</div><div class="rotulos-container-fixed">{rotulos_html_tela_pre}</div><div style="text-align:center; font-size:11px; color:#6C757D; margin-top:15px;"><span style="color:#CBD5E0; font-weight:bold;">■ Outras Classes (C/D/E)</span> &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#053CD8; font-weight:bold;">■ Classe B1 (Base)</span> &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#0DF205; font-weight:bold;">■ Classe A+ (Elevada)</span> &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:#15803D; font-weight:bold;">■ Classe A++ (Mais Elevada)</span></div></div>""", unsafe_allow_html=True)

            # CAMPO DE CONSIDERAÇÕES FINAIS
            st.write("")
            st.markdown("##### Considerações Finais do Comitê")
            consideracoes_m2 = st.text_area("Insira observações ou parecer técnico para o PDF:", placeholder="Digite aqui comentários sobre o ponto pré-definido...", height=80, key="val_m2_consideracoes")

            # RELATÓRIO PDF EXECUTIVO COMPLETO
            st.write("")
            st.markdown("---")
            with st.expander("📄 Exportar Relatório Oficial (PDF)", expanded=False):
                modo_definicao = f"Exceção Técnica ({justificativa_excecao})" if aplicar_excecao else "Análise de Dados do Algoritmo"
                html_relatorio = f"""
                <div style="font-family: Arial, sans-serif; background: #ffffff; padding: 25px; border: 1px solid #CBD5E0; border-radius: 8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; background-color:#022D8A; padding:15px 20px; border-radius:6px; color:#ffffff;">
                        <div>
                            <h2 style="color:#ffffff; margin:0; font-size:20px; text-transform:uppercase;">Relatório de Precificação Estratégica</h2>
                            <small style="color:#0DF205; font-weight:bold;">Fast Tennis - Comitê de Precificação</small>
                        </div>
                        <span style="font-size:12px; color:#E2E8F0;">Pontos Pré-Definidos</span>
                    </div>
                    <hr style="border: 0; border-top: 1px solid #cbd5e0; margin: 15px 0;">
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 20px;">
                        <tr style="background-color:#F8F9FA;">
                            <td style="padding:8px; border:1px solid #ddd;"><b>Unidade:</b> {dados_u_pre['Unidade']} (Quadras: {num_quadras_pre})</td>
                            <td style="padding:8px; border:1px solid #ddd;"><b>População Total:</b> {populacao:,} hab.</td>
                        </tr>
                        <tr>
                            <td style="padding:8px; border:1px solid #ddd;"><b>Endereço Cadastrado:</b> {endereco_pre}</td>
                            <td style="padding:8px; border:1px solid #ddd;"><b>Público Alvo:</b> {calculo_alvo:,} hab. ({soma_percentuais*100:.1f}%)</td>
                        </tr>
                    </table>

                    <div style="background-color:#F0FDF4; border-left:6px solid #00A807; padding:15px; border-radius:4px; margin-bottom:20px; border:1px solid #BBF7D0;">
                        <h3 style="margin:0; color:#022D8A; font-size:18px;">TABELA SELECIONADA: TABELA {tabela_final}</h3>
                        <p style="margin:4px 0 0 0; font-size:13px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {preco_ref},00</b> | TKM: <b>R$ {tkm_ref},00</b></p>
                        <p style="margin:4px 0 0 0; font-size:11px; color:#6C757D;">Modo de Definição: <b>{modo_definicao}</b></p>
                    </div>

                    <div style="font-size:12px; line-height:1.5; margin-bottom:20px; background-color:#FFFFFF; padding:12px; border:1px solid #E2E8F0; border-radius:4px;">
                        <p style="margin:0 0 4px 0;"><b>Diretriz Regional:</b> {diag}</p>
                        <p style="margin:0 0 4px 0;"><b>Status de Mercado:</b> {status} (Diferença: {txt_dif})</p>
                        <p style="margin:0 0 4px 0;"><b>Recomendação:</b> {rec}</p>
                        <p style="margin:0 0 0 0;"><b>Status de Rentabilidade Projetada (BP):</b> {viabilidade_bp}</p>
                    </div>

                    <h4 style="color:#022D8A; margin:15px 0 8px 0; font-size:12px; text-transform:uppercase;">Unidades da Rede com Perfil Similar:</h4>
                    <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-bottom: 20px;">
                        <thead>
                            <tr style="background-color:#F8F9FA; text-align:left; color:#022D8A;">
                                <th style="padding:6px; border:1px solid #ddd;">Unidade</th>
                                <th style="padding:6px; border:1px solid #ddd;">Tabela Praticada</th>
                                <th style="padding:6px; border:1px solid #ddd;">% Similaridade</th>
                            </tr>
                        </thead>
                        <tbody>
                            {linhas_similares_pdf_pre}
                        </tbody>
                    </table>

                    <h4 style="color:#022D8A; margin:15px 0 8px 0; font-size:12px; text-transform:uppercase;">Distribuição Social de Renda (%) e Similaridade:</h4>
                    <div style="display:flex; justify-content:space-around; align-items:flex-end; background:#F8F9FA; padding:15px; border-radius:6px; border:1px solid #E2E8F0; margin-bottom:12px;">
                        {barras_html_pdf_pre}
                    </div>
                    <div style="text-align:center; font-size:10px; color:#6C757D; margin-bottom:20px;">
                        <span style="color:#CBD5E0; font-weight:bold;">■ Outras Classes (C/D/E)</span> &nbsp;&nbsp;
                        <span style="color:#053CD8; font-weight:bold;">■ Classe B1 (Base)</span> &nbsp;&nbsp; 
                        <span style="color:#0DF205; font-weight:bold;">■ Classe A+ (Elevada)</span> &nbsp;&nbsp; 
                        <span style="color:#15803D; font-weight:bold;">■ Classe A++ (Mais Elevada)</span>
                    </div>

                    {f'''
                    <div style="background-color:#FFFDF5; border-left:4px solid #D69E2E; padding:12px; border-radius:4px; margin-bottom:20px;">
                        <h4 style="margin:0 0 4px 0; color:#975A16; font-size:11px; text-transform:uppercase;">Considerações Finais do Comitê:</h4>
                        <p style="margin:0; font-size:12px; color:#2D3748; line-height:1.4;">{consideracoes_m2}</p>
                    </div>
                    ''' if consideracoes_m2 else ''}

                    <button onclick="window.print()" style="background-color: #0DF205; color: #022D8A; border: none; padding: 10px 24px; font-weight: bold; border-radius: 20px; cursor: pointer; font-size:13px;">Imprimir / Salvar PDF Executivo</button>
                </div>
                """
                st.components.v1.html(html_relatorio, height=680, scrolling=True)

# ==============================================================================
# MÓDULO 3: REAVALIAÇÃO E REPRECIFICAÇÃO DE UNIDADES ATIVAS
# ==============================================================================
else:
    st.title("Reavaliação Estratégica de Unidades Ativas")
    st.markdown("Matriz de diagnóstico com carregamento automático dos dados demográficos e de mercado da unidade.")
    st.markdown("---")

    def limpar_campos_m2():
        st.session_state["m2_nome_u"] = "Selecione..."
        st.session_state["val_m3_consideracoes"] = ""
        for key in ["m2_mix", "m2_cres_base", "m2_vendedor"]:
            st.session_state[key] = "Selecione..."
        for key in ["m2_tkm_real", "m2_ll", "m2_fat", "m2_objecoes", "m2_conv_u", "m2_lead_u", "m2_churn_u", "m2_conc_p"]:
            st.session_state[key] = 0.0

    if "m2_nome_u" not in st.session_state:
        st.session_state["m2_med_conv"] = 0.0
        st.session_state["m2_med_lead"] = 0.0
        st.session_state["m2_med_churn"] = 0.0
        limpar_campos_m2()

    # 1. MÉDIAS GLOBAIS DA REDE
    st.subheader("1. Parâmetros Médios Atuais da Rede")
    with st.container(border=True):
        mr1, mr2, mr3 = st.columns(3)
        with mr1:
            media_rede_conversao = st.number_input("% Conversão Médio Rede:", min_value=0.0, step=0.5, key="m2_med_conv")
        with mr2:
            media_rede_lead_conect = st.number_input("% Lead Conectado Médio Rede:", min_value=0.0, step=0.5, key="m2_med_lead")
        with mr3:
            media_rede_churn = st.number_input("% Churn Médio Rede:", min_value=0.0, step=0.1, key="m2_med_churn")

    st.write("")
    
    # SELEÇÃO DA UNIDADE
    st.subheader("2. Seleção de Unidade & Diagnóstico Operacional")
    nome_unidade_sel = st.selectbox("Selecione a Unidade para Reavaliação:", LISTA_NOMES_UNIDADES, key="m2_nome_u")

    if nome_unidade_sel != "Selecione...":
        dados_u = df_base_unidades[df_base_unidades["Unidade"] == nome_unidade_sel].iloc[0]
        
        tab_praticada_str = str(dados_u["Tabela Praticada"])
        tab_praticada_u = int(tab_praticada_str.replace("Tabela", "").strip()) if "Tabela" in tab_praticada_str else 3
        
        populacao_u = int(dados_u["População"])
        renda_u = float(dados_u["Renda Média"])
        num_quadras_re = int(dados_u["Quadras"])
        endereco_re = dados_u["Endereço"]
        pct_alvo_u = float(dados_u["A++"] + dados_u["A+"] + dados_u["B1"])
        num_alvo_u = int(pct_alvo_u * populacao_u)
        
        tkm_esperado_rede = TABELAS_OFICIAIS[tab_praticada_u]["tkm"]
        preco_plus_esperado = TABELAS_OFICIAIS[tab_praticada_u]["plus"]

        # RESUMO AUTOMÁTICO DA UNIDADE FORMATADO
        html_card_reav = f"""
            <div class="card-resumo-unidade">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h3 style="margin:0; color:#022D8A;">{dados_u['Unidade']} ({dados_u['Cidade']})</h3>
                    <span style="background-color:#022D8A; color:#0DF205; padding:4px 12px; border-radius:15px; font-weight:800; font-size:13px;">Tabela Praticada: Tabela {tab_praticada_u} | Quadras: {num_quadras_re}</span>
                </div>
                <p style="margin:0 0 8px 0; font-size:13px; color:#022D8A;"><b>Endereço Cadastrado:</b> {endereco_re}</p>
                <div style="display:flex; justify-content:space-between; font-size:13px; color:#2D3748; flex-wrap:wrap; gap:10px;">
                    <div><b>População Residente:</b> {populacao_u:,} hab.</div>
                    <div><b>🎯 Público Alvo (B1+A+ A++):</b> {num_alvo_u:,} hab. ({pct_alvo_u*100:.1f}%)</div>
                    <div><b>Renda Média:</b> R$ {renda_u:,.2f}</div>
                    <div><b>TKM Esperado:</b> R$ {tkm_esperado_rede},00 | <b>Plano Plus 1x:</b> R$ {preco_plus_esperado},00</div>
                </div>
            </div>
        """
        st.markdown(html_card_reav, unsafe_allow_html=True)

        # CAMPOS OPERACIONAIS REQUISITADOS
        with st.container(border=True):
            st.markdown("<p style='color:#022D8A; font-weight:800; font-size:15px; margin-bottom:12px;'>Preenchimento do Desempenho Operacional da Unidade</p>", unsafe_allow_html=True)
            u1, u2, u3 = st.columns(3)
            
            with u1:
                st.markdown("**Desempenho Financeiro**")
                tkm_real_unidade = st.number_input("TKM Real Praticado (R$):", min_value=0.0, step=5.0, key="m2_tkm_real")
                atingimento_ll = st.number_input("% Atingimento Meta Lucro Líquido:", min_value=0.0, step=1.0, key="m2_ll")
                atingimento_fat = st.number_input("% Atingimento Meta Faturamento:", min_value=0.0, step=1.0, key="m2_fat")

            with u2:
                st.markdown("**Conversão e Vendas**")
                perfil_vendedor = st.selectbox("Perfil da Equipe/Vendedor:", ["Selecione...", "Vendedor de alta performance", "Necessidade de desenvolvimento", "Vendedor desalinhado"], key="m2_vendedor")
                mix_produtos = st.selectbox("Distribuição do Mix:", ["Selecione...", "Consumo Plus saudável", "Smart acima do Plus (8% a 15%)", "Smart acima do Plus (> 15%)"], key="m2_mix")
                objecoes_preco = st.number_input("% Objeções por Preço:", min_value=0.0, step=1.0, key="m2_objecoes")
                conversao_unidade = st.number_input("% Conversão de Vendas:", min_value=0.0, step=0.5, key="m2_conv_u")

            with u3:
                st.markdown("**Engajamento & Concorrência**")
                lead_conect_unidade = st.number_input("% Lead Conectado:", min_value=0.0, step=0.5, key="m2_lead_u")
                churn_unidade = st.number_input("% Churn Local:", min_value=0.0, step=0.1, key="m2_churn_u")
                crescimento_base = st.selectbox("Evolução da Base:", ["Selecione...", "Crescimento saudável e consistente", "Oscilação de alunos", "Crescimento estagnado"], key="m2_cres_base")
                preco_concorrentes = st.number_input("Preço Médio Concorrentes (Plus 1x):", min_value=0.0, step=10.0, key="m2_conc_p")

            st.write("")
            col_btn_m2_1, col_btn_m2_2 = st.columns([5, 1.2])
            with col_btn_m2_2:
                st.button("Limpar Avaliação", on_click=limpar_campos_m2, use_container_width=True)

        pronto_m2 = (
            mix_produtos != "Selecione..." and
            crescimento_base != "Selecione..." and
            perfil_vendedor != "Selecione..." and
            media_rede_conversao > 0
        )

        if not pronto_m2:
            st.info("Aguardando preenchimento dos indicadores operacionais da unidade acima para compilação da Matriz Estratégica.")
        else:
            st.write("")
            st.markdown('<div class="faixa-resultados">Matriz de Orientação e Diagnóstico</div>', unsafe_allow_html=True)
            
            matriz_sinais = []

            # 1. Lucro Líquido
            s_ll = "Positivo" if atingimento_ll >= 90 else "Atenção" if atingimento_ll >= 80 else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "Lucro Líquido", "Referência / Alvo": "≥ 90.0%", "Desempenho Unidade": f"{atingimento_ll:.1f}%", "Sinal": s_ll})

            # 2. Faturamento
            s_fat = "Positivo" if atingimento_fat >= 90 else "Atenção" if atingimento_fat >= 80 else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "Faturamento", "Referência / Alvo": "≥ 90.0%", "Desempenho Unidade": f"{atingimento_fat:.1f}%", "Sinal": s_fat})

            # 3. Mix
            s_mix = "Positivo" if "saudável" in mix_produtos else "Atenção" if "8%" in mix_produtos else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "Mix de Produtos", "Referência / Alvo": "Consumo Saudável", "Desempenho Unidade": mix_produtos, "Sinal": s_mix})

            # 4. Objeções
            s_obj = "Positivo" if objecoes_preco <= 10 else "Atenção" if objecoes_preco <= 25 else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "Objeções por Preço", "Referência / Alvo": "≤ 10.0%", "Desempenho Unidade": f"{objecoes_preco:.1f}%", "Sinal": s_obj})

            # 5. Conversão
            s_conv = "Positivo" if conversao_unidade >= media_rede_conversao else "Atenção" if conversao_unidade >= (media_rede_conversao * 0.90) else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "Conversão", "Referência / Alvo": f"Média Rede ({media_rede_conversao:.1f}%)", "Desempenho Unidade": f"{conversao_unidade:.1f}%", "Sinal": s_conv})

            # 6. Lead Conectado
            s_lead = "Positivo" if lead_conect_unidade >= media_rede_lead_conect else "Atenção" if lead_conect_unidade >= (media_rede_lead_conect * 0.90) else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "% Lead Conectado", "Referência / Alvo": f"Média Rede ({media_rede_lead_conect:.1f}%)", "Desempenho Unidade": f"{lead_conect_unidade:.1f}%", "Sinal": s_lead})

            # 7. TKM
            s_tkm = "Positivo" if tkm_real_unidade >= tkm_esperado_rede else "Atenção" if tkm_real_unidade >= (tkm_esperado_rede * 0.90) else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "TKM Praticado", "Referência / Alvo": f"Esp. Tab {tab_praticada_u} (R$ {tkm_esperado_rede})", "Desempenho Unidade": f"R$ {tkm_real_unidade:.0f}", "Sinal": s_tkm})

            # 8. Crescimento Base
            s_base = "Positivo" if "saudável" in crescimento_base else "Atenção" if "Oscilação" in crescimento_base else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "Crescimento Base", "Referência / Alvo": "Crescimento Saudável", "Desempenho Unidade": "Oscilação/Queda" if s_base != "Positivo" else "Saudável", "Sinal": s_base})

            # 9. Churn
            s_churn = "Positivo" if churn_unidade <= media_rede_churn else "Atenção" if churn_unidade <= (media_rede_churn * 1.15) else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "% Churn", "Referência / Alvo": f"Média Rede ({media_rede_churn:.1f}%)", "Desempenho Unidade": f"{churn_unidade:.1f}%", "Sinal": s_churn})

            # 10. Perfil Vendedor
            s_vend = "Positivo" if "alta performance" in perfil_vendedor else "Atenção" if "desenvolvimento" in perfil_vendedor else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "Perfil Vendedor", "Referência / Alvo": "Alta Performance", "Desempenho Unidade": "Desenvolvimento/Desalinhado" if s_vend != "Positivo" else "Alta Perform.", "Sinal": s_vend})

            # 11. Pesquisa Mercado
            dif_conc = (preco_plus_esperado - preco_concorrentes) / preco_concorrentes if preco_concorrentes > 0 else 0
            s_merc = "Positivo" if abs(dif_conc) <= 0.10 else "Atenção" if abs(dif_conc) <= 0.20 else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "Pesquisa de Mercado", "Referência / Alvo": "Aderente (Até 10% dif)", "Desempenho Unidade": f"{dif_conc*100:+.1f}% vs Conc.", "Sinal": s_merc})

            # 12. Potencial Região
            s_pot = "Positivo" if renda_u >= 15000 and pct_alvo_u >= 0.35 else "Atenção" if renda_u >= 11000 and pct_alvo_u >= 0.25 else "Crítico"
            matriz_sinais.append({"Critério Avaliado": "Potencial Econômico", "Referência / Alvo": "≥ R$ 15k e ≥ 35% Alvo", "Desempenho Unidade": f"R$ {renda_u:,.0f} | {pct_alvo_u*100:.0f}%", "Sinal": s_pot})

            # Compilação
            df_sinais = pd.DataFrame(matriz_sinais)
            qtd_positivos = sum(1 for x in matriz_sinais if x["Sinal"] == "Positivo")
            qtd_atencao = sum(1 for x in matriz_sinais if x["Sinal"] == "Atenção")
            qtd_criticos = sum(1 for x in matriz_sinais if x["Sinal"] == "Crítico")
            pct_positivos = (qtd_positivos / len(matriz_sinais)) * 100

            def estilizar_sinais(val):
                if val == "Positivo": return 'background-color: #DCFCE7; color: #15803D; font-weight: bold;'
                if val == "Atenção": return 'background-color: #FEF9C3; color: #A16207; font-weight: bold;'
                if val == "Crítico": return 'background-color: #FEE2E2; color: #B91C1C; font-weight: bold;'
                return ''
                
            st.dataframe(df_sinais.style.map(estilizar_sinais, subset=['Sinal']), use_container_width=True, hide_index=True)

            st.markdown(f"""
                <div style="background-color:#F8F9FA; border:1px solid #E2E8F0; padding:12px 20px; border-radius:4px; margin-top:8px; display:flex; justify-content:space-around;">
                    <span style="font-size:14px; color:#2D3748;">Resumo da Avaliação ➔</span>
                    <span style="font-size:14px;">Positivos: <b style="color:#15803D;">{qtd_positivos} ({pct_positivos:.0f}%)</b></span>
                    <span style="font-size:14px;">Atenção: <b style="color:#A16207;">{qtd_atencao}</b></span>
                    <span style="font-size:14px;">Críticos: <b style="color:#B91C1C;">{qtd_criticos}</b></span>
                </div>
            """, unsafe_allow_html=True)

            st.write("")
            st.subheader("3. Relatório Estratégico de Posicionamento")

            indicio_desalinhamento = (s_obj == "Crítico" and s_conv == "Crítico" and "mais de 15%" in mix_produtos)

            if pct_positivos >= 70.0:
                rec_pop = "<b>Elegível a Aumento ou Manutenção Premium</b>: Desempenho altamente saudável. Tabela aderente ao mercado e perfil do público. Unidade qualificada para elevação em Comitê."
                cor_pop = "#166534"
                bg_pop = "#F0FDF4"
            elif qtd_criticos >= 3:
                rec_pop = "<b>Reavaliação de Posicionamento / Redução de Tabela</b>: Alta concentração de indicadores críticos na unidade. Necessária intervenção imediata para ajuste de margem ou estratégia promocional agressiva."
                cor_pop = "#991B1B"
                bg_pop = "#FEF2F2"
            else:
                rec_pop = "<b>Ajuste Operacional (Sem Alteração de Preço Imediata)</b>: Cenário neutro ou em transição. O foco mandatório deve estar na correção dos processos comerciais internos e capacitação da equipe antes de testar sensibilidade de preço."
                cor_pop = "#975A16"
                bg_pop = "#FFFDF5"

            st.markdown(f"""
                <div style="background-color:{bg_pop}; border-left:6px solid {cor_pop}; padding:18px; border-radius:8px; margin-bottom:15px;">
                    <p style="margin:0; font-size:11px; color:{cor_pop}; font-weight:bold; text-transform:uppercase;">Diretriz Estratégica</p>
                    <p style="margin:6px 0 0 0; font-size:15px; color:#2D3748; line-height:1.5;">{rec_pop}</p>
                    {f'<p style="margin:8px 0 0 0; font-size:13px; color:#B91C1C;"><b>⚠️ Alerta Crítico Adicional:</b> Identificado forte indício de desalinhamento de tabela (Combinação de alta sensibilidade a preço, baixa conversão e fuga extrema para o plano Smart).</p>' if indicio_desalinhamento else ''}
                </div>
            """, unsafe_allow_html=True)

            # CAMPO DE CONSIDERAÇÕES FINAIS (MÓDULO 3)
            st.write("")
            st.markdown("##### Considerações Finais do Comitê")
            consideracoes_m3 = st.text_area("Insira observações ou parecer técnico para o PDF:", placeholder="Digite aqui comentários operacionais ou justificativas técnicas...", height=80, key="val_m3_consideracoes")

            # RELATÓRIO PDF EXECUTIVO PARA O MÓDULO 3
            st.write("")
            st.markdown("---")
            with st.expander("📄 Exportar Relatório de Reavaliação (PDF)", expanded=False):
                linhas_tabela_pdf = ""
                for x in matriz_sinais:
                    cor_fundo = "#DCFCE7" if x['Sinal'] == "Positivo" else "#FEF9C3" if x['Sinal'] == "Atenção" else "#FEE2E2"
                    cor_texto = "#15803D" if x['Sinal'] == "Positivo" else "#A16207" if x['Sinal'] == "Atenção" else "#B91C1C"
                    linhas_tabela_pdf += f"""<tr>
                        <td style="padding:6px; border:1px solid #ddd;">{x['Critério Avaliado']}</td>
                        <td style="padding:6px; border:1px solid #ddd;">{x['Referência / Alvo']}</td>
                        <td style="padding:6px; border:1px solid #ddd;">{x['Desempenho Unidade']}</td>
                        <td style="padding:6px; border:1px solid #ddd; background-color:{cor_fundo}; color:{cor_texto}; font-weight:bold; text-align:center;">{x['Sinal']}</td>
                    </tr>"""

                html_pdf_m3 = f"""
                <div style="font-family: Arial, sans-serif; background: #ffffff; padding: 25px; border: 1px solid #CBD5E0; border-radius: 8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; background-color:#022D8A; padding:15px 20px; border-radius:6px; color:#ffffff;">
                        <div>
                            <h2 style="color:#ffffff; margin:0; font-size:20px; text-transform:uppercase;">Relatório de Reavaliação Estratégica</h2>
                            <small style="color:#0DF205; font-weight:bold;">Fast Tennis - Comitê de Precificação</small>
                        </div>
                        <span style="font-size:12px; color:#E2E8F0;">Unidade Ativa</span>
                    </div>
                    <hr style="border: 0; border-top: 1px solid #cbd5e0; margin: 15px 0;">
                    
                    <h4 style="margin:0 0 5px 0; color:#022D8A;">Unidade: {dados_u['Unidade']} ({dados_u['Cidade']})</h4>
                    <p style="margin:0 0 15px 0; font-size:12px; color:#2D3748;">Endereço: <b>{endereco_re}</b> | Quadras: <b>{num_quadras_re}</b> | Tabela Atual: <b>Tabela {tab_praticada_u}</b></p>
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-bottom: 20px;">
                        <thead>
                            <tr style="background-color:#F8F9FA; text-align:left; color:#022D8A;">
                                <th style="padding:6px; border:1px solid #ddd;">Critério Avaliado</th>
                                <th style="padding:6px; border:1px solid #ddd;">Referência / Alvo da Rede</th>
                                <th style="padding:6px; border:1px solid #ddd;">Desempenho Unidade</th>
                                <th style="padding:6px; border:1px solid #ddd; text-align:center;">Classificação</th>
                            </tr>
                        </thead>
                        <tbody>
                            {linhas_tabela_pdf}
                        </tbody>
                    </table>

                    <div style="background-color:#F8F9FA; border:1px solid #E2E8F0; padding:10px; border-radius:4px; margin-bottom:15px; text-align:center; font-size:12px;">
                        <b>Resumo da Matriz:</b> <span style="color:#15803D;">Positivos: {qtd_positivos} ({pct_positivos:.0f}%)</span> | 
                        <span style="color:#A16207;">Atenção: {qtd_atencao}</span> | 
                        <span style="color:#B91C1C;">Críticos: {qtd_criticos}</span>
                    </div>

                    <div style="background-color:{bg_pop}; border-left:6px solid {cor_pop}; padding:15px; border-radius:6px; margin-bottom:20px;">
                        <h3 style="margin:0 0 5px 0; font-size:13px; color:{cor_pop}; text-transform:uppercase;">Diretriz Estratégica (Comitê)</h3>
                        <p style="margin:0; font-size:13px; color:#2D3748; line-height:1.4;">{rec_pop}</p>
                    </div>

                    {f'''
                    <div style="background-color:#FFFDF5; border-left:4px solid #D69E2E; padding:12px; border-radius:4px; margin-bottom:20px;">
                        <h4 style="margin:0 0 4px 0; color:#975A16; font-size:11px; text-transform:uppercase;">Considerações Finais do Comitê:</h4>
                        <p style="margin:0; font-size:12px; color:#2D3748; line-height:1.4;">{consideracoes_m3}</p>
                    </div>
                    ''' if consideracoes_m3 else ''}
                    
                    <button onclick="window.print()" style="background-color: #0DF205; color: #022D8A; border: none; padding: 10px 24px; font-weight: bold; border-radius: 20px; cursor: pointer; font-size:13px;">Imprimir / Salvar PDF Executivo</button>
                </div>
                """
                st.components.v1.html(html_pdf_m3, height=680, scrolling=True)
