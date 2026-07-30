import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página corporativa da Fast Tennis
st.set_page_config(page_title="Fast Tennis - Plataforma Estratégica", layout="wide")

# ==========================================
# APLICAÇÃO DA IDENTIDADE VISUAL FAST TENNIS (GUIDELINE 2025)
# Paleta Oficial: Blue FT (#053CD8), Navy FT (#022D8A), Green FT (#0DF205)
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
        
        /* Faixa de Destaque */
        .faixa-resultados {
            background-color: #022D8A;
            color: #FFFFFF;
            padding: 14px 20px;
            margin: 25px -4rem 15px -4rem; 
            font-size: 18px; 
            font-weight: 800;
            border-left: 6px solid #0DF205;
        }

        .tabela-sugerida-box {
            background-color: #F8F9FA;
            padding: 18px;
            border-radius: 8px;
            border-left: 6px solid #022D8A;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }
        .tabela-sugerida-box h2 {
            margin: 4px 0;
            color: #022D8A !important;
            font-size: 26px;
            font-weight: 800;
        }

        .tabela-excecao-box {
            background-color: #F0FDF4;
            padding: 18px;
            border-radius: 8px;
            border-left: 6px solid #0DF205;
            margin-bottom: 15px;
            border: 1px solid #DCFCE7;
        }
        .tabela-excecao-box h2 {
            margin: 4px 0;
            color: #166534 !important;
            font-size: 26px;
            font-weight: 800;
        }

        .card-destaque {
            background-color: #F8F9FA;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 12px 15px;
            margin-top: 6px;
        }

        .card-resumo-unidade {
            background-color: #F0F4FF;
            border: 1px solid #C3D3FC;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .alerta-fino {
            background-color: #FEF2F2;
            color: #991B1B;
            border-left: 4px solid #EF4444;
            padding: 8px 14px;
            font-size: 13px;
            font-weight: 600;
            border-radius: 4px;
            margin-bottom: 12px;
        }

        .box-relatorio-equilibrado {
            background-color: #F8F9FA;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            padding: 14px 18px;
            height: 110px !important;
            box-sizing: border-box !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
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
# BANCO DE DADOS DE UNIDADES REAIS FAST TENNIS
# ==========================================
df_existentes = [
    {"Unidade": "FT AGUAS CLARAS - DF", "Cidade": "Brasília", "IsSP": False, "Renda Média": 20740, "População": 80388, "REGIC": "Metrópole Nacional", "Tabela Praticada": 4, "A++": 0.23, "A+": 0.27, "B1": 0.21},
    {"Unidade": "FT ALPHAVILLE - SP", "Cidade": "Barueri", "IsSP": True, "Renda Média": 27400, "População": 44300, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.15, "A+": 0.23, "B1": 0.21},
    {"Unidade": "FT ALTO DA BOA VISTA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 23654, "População": 85519, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.17, "A+": 0.20, "B1": 0.18},
    {"Unidade": "FT ALTO DOS PINHEIROS - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 23900, "População": 82500, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.22, "A+": 0.20, "B1": 0.18},
    {"Unidade": "FT ALTO DO IPIRANGA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 19775, "População": 177000, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.14, "A+": 0.16, "B1": 0.15},
    {"Unidade": "FT ANHANGUERA - SP", "Cidade": "Jundiaí", "IsSP": True, "Renda Média": 11650, "População": 67900, "REGIC": "Capital Regional C", "Tabela Praticada": 3, "A++": 0.00, "A+": 0.10, "B1": 0.18},
    {"Unidade": "FT BEBEDOURO - SP", "Cidade": "Bebedouro", "IsSP": True, "Renda Média": 5900, "População": 44900, "REGIC": "Centro Sub-Regional B", "Tabela Praticada": 1, "A++": 0.02, "A+": 0.09, "B1": 0.15},
    {"Unidade": "FT BELVEDERE - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 23100, "População": 63400, "REGIC": "Metrópole", "Tabela Praticada": 3, "A++": 0.22, "A+": 0.26, "B1": 0.17},
    {"Unidade": "FT BOA VIAGEM - PE", "Cidade": "Recife", "IsSP": False, "Renda Média": 12214, "População": 102000, "REGIC": "Capital Regional A", "Tabela Praticada": 2, "A++": 0.08, "A+": 0.14, "B1": 0.16},
    {"Unidade": "FT BOTAFOGO - SP", "Cidade": "Campinas", "IsSP": True, "Renda Média": 12300, "População": 96574, "REGIC": "Capital Regional A", "Tabela Praticada": 3, "A++": 0.07, "A+": 0.13, "B1": 0.20},
    {"Unidade": "FT BROOKLIN - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 29400, "População": 162400, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.30, "A+": 0.27, "B1": 0.15},
    {"Unidade": "FT BURITIS - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 16700, "População": 80900, "REGIC": "Metrópole", "Tabela Praticada": 2, "A++": 0.10, "A+": 0.24, "B1": 0.24},
    {"Unidade": "FT CALAFATE - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 13100, "População": 121200, "REGIC": "Metrópole", "Tabela Praticada": 1, "A++": 0.09, "A+": 0.17, "B1": 0.20},
    {"Unidade": "FT CAMPO BELO - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 27328, "População": 117500, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.27, "A+": 0.25, "B1": 0.15},
    {"Unidade": "FT CANTAREIRA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 11500, "População": 95500, "REGIC": "Grande Metrópole", "Tabela Praticada": 3, "A++": 0.09, "A+": 0.18, "B1": 0.23},
    {"Unidade": "FT CAPIM MACIO - RN", "Cidade": "Natal", "IsSP": False, "Renda Média": 14700, "População": 64400, "REGIC": "Capital Regional A", "Tabela Praticada": 2, "A++": 0.10, "A+": 0.18, "B1": 0.22},
    {"Unidade": "FT CASTELO - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 10500, "População": 111575, "REGIC": "Metrópole", "Tabela Praticada": 2, "A++": 0.05, "A+": 0.13, "B1": 0.20},
    {"Unidade": "FT CENTRO SÃO BERNARDO - SP", "Cidade": "São Bernardo do Campo", "IsSP": True, "Renda Média": 10800, "População": 164300, "REGIC": "Grande Metrópole", "Tabela Praticada": 3, "A++": 0.05, "A+": 0.12, "B1": 0.18},
    {"Unidade": "FT CHÁCARA INGLESA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 21400, "População": 178712, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.18, "A+": 0.22, "B1": 0.15},
    {"Unidade": "FT CHÁCARA SANTO ANTÔNIO - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 25795, "População": 78250, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.24, "A+": 0.25, "B1": 0.14},
    {"Unidade": "FT CIDADE NOVA - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 10969, "População": 123470, "REGIC": "Metrópole", "Tabela Praticada": 2, "A++": 0.03, "A+": 0.15, "B1": 0.19},
    {"Unidade": "FT CONTAGEM - MG", "Cidade": "Contagem", "IsSP": False, "Renda Média": 7860, "População": 73600, "REGIC": "Capital Regional B", "Tabela Praticada": 1, "A++": 0.00, "A+": 0.08, "B1": 0.15},
    {"Unidade": "FT ESTORIL - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 12612, "População": 85000, "REGIC": "Metrópole", "Tabela Praticada": 2, "A++": 0.05, "A+": 0.17, "B1": 0.22},
    {"Unidade": "FT ESTRELA SUL - JF", "Cidade": "Juiz de Fora", "IsSP": False, "Renda Média": 10480, "População": 113000, "REGIC": "Capital Regional B", "Tabela Praticada": 1, "A++": 0.04, "A+": 0.12, "B1": 0.18},
    {"Unidade": "FT GUARARAPES - CE", "Cidade": "Fortaleza", "IsSP": False, "Renda Média": 12450, "População": 54706, "REGIC": "Capital Regional A", "Tabela Praticada": 2, "A++": 0.08, "A+": 0.14, "B1": 0.21},
    {"Unidade": "FT INDAIATUBA - SP", "Cidade": "Indaiatuba", "IsSP": True, "Renda Média": 11187, "População": 53898, "REGIC": "Centro Sub-Regional", "Tabela Praticada": 2, "A++": 0.02, "A+": 0.10, "B1": 0.14},
    {"Unidade": "FT JARDIM - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 14195, "População": 128600, "REGIC": "Grande Metrópole", "Tabela Praticada": 4, "A++": 0.07, "A+": 0.18, "B1": 0.23},
    {"Unidade": "FT JARDIM PORTAL DA COLINA - SP", "Cidade": "Sorocaba", "IsSP": True, "Renda Média": 11900, "População": 52624, "REGIC": "Capital Regional B", "Tabela Praticada": 3, "A++": 0.02, "A+": 0.10, "B1": 0.14},
    {"Unidade": "FT JARDIM SOCIAL - PR", "Cidade": "Curitiba", "IsSP": False, "Renda Média": 31000, "População": 56708, "REGIC": "Metrópole", "Tabela Praticada": 5, "A++": 0.10, "A+": 0.31, "B1": 0.21},
    {"Unidade": "FT LAPA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 14200, "População": 107250, "REGIC": "Grande Metrópole", "Tabela Praticada": 4, "A++": 0.08, "A+": 0.18, "B1": 0.22},
    {"Unidade": "FT MOEMA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 28900, "População": 143796, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.30, "A+": 0.26, "B1": 0.13},
    {"Unidade": "FT MOOCA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 13400, "População": 147000, "REGIC": "Grande Metrópole", "Tabela Praticada": 4, "A++": 0.07, "A+": 0.18, "B1": 0.23},
    {"Unidade": "FT MORADA DA COLINA - MG", "Cidade": "Uberlândia", "IsSP": False, "Renda Média": 14528, "População": 54900, "REGIC": "Capital Regional B", "Tabela Praticada": 2, "A++": 0.07, "A+": 0.16, "B1": 0.18},
    {"Unidade": "FT MORUMBI - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 14200, "População": 165700, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.12, "A+": 0.21, "B1": 0.20},
    {"Unidade": "FT NOVA ALIANÇA SUL - SP", "Cidade": "Ribeirão Preto", "IsSP": True, "Renda Média": 12900, "População": 90800, "REGIC": "Capital Regional A", "Tabela Praticada": 3, "A++": 0.08, "A+": 0.15, "B1": 0.18},
    {"Unidade": "FT ORLA PAMPULHA - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 9940, "População": 42149, "REGIC": "Metrópole", "Tabela Praticada": 2, "A++": 0.01, "A+": 0.11, "B1": 0.17},
    {"Unidade": "FT PAMPULHA - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 11675, "População": 75076, "REGIC": "Metrópole", "Tabela Praticada": 2, "A++": 0.04, "A+": 0.12, "B1": 0.18},
    {"Unidade": "FT PARQUE PIQUERI - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 12800, "População": 138700, "REGIC": "Grande Metrópole", "Tabela Praticada": 4, "A++": 0.08, "A+": 0.14, "B1": 0.17},
    {"Unidade": "FT PONTE JK - DF", "Cidade": "Brasília", "IsSP": False, "Renda Média": 25400, "População": 95617, "REGIC": "Metrópole Nacional", "Tabela Praticada": 4, "A++": 0.24, "A+": 0.30, "B1": 0.14},
    {"Unidade": "FT PRAIA DO CANTO - ES", "Cidade": "Vitória", "IsSP": False, "Renda Média": 16840, "População": 83239, "REGIC": "Metrópole", "Tabela Praticada": 3, "A++": 0.11, "A+": 0.18, "B1": 0.22},
    {"Unidade": "FT PRAIA GRANDE - SP", "Cidade": "Praia Grande", "IsSP": True, "Renda Média": 8900, "População": 84400, "REGIC": "Capital Regional B", "Tabela Praticada": 3, "A++": 0.02, "A+": 0.11, "B1": 0.18},
    {"Unidade": "FT RADIAL LESTE TATUAPÉ - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 15700, "População": 146400, "REGIC": "Grande Metrópole", "Tabela Praticada": 4, "A++": 0.11, "A+": 0.19, "B1": 0.21},
    {"Unidade": "FT RECREIO - RJ", "Cidade": "Rio de Janeiro", "IsSP": False, "Renda Média": 22000, "População": 74360, "REGIC": "Metrópole", "Tabela Praticada": 2, "A++": 0.16, "A+": 0.25, "B1": 0.24},
    {"Unidade": "FT RIO CLARO - SP", "Cidade": "Rio Claro", "IsSP": True, "Renda Média": 7400, "População": 72800, "REGIC": "Centro Sub-Regional I", "Tabela Praticada": 1, "A++": 0.01, "A+": 0.04, "B1": 0.12},
    {"Unidade": "FT SALGADO FILHO - PR", "Cidade": "Curitiba", "IsSP": False, "Renda Média": 8900, "População": 64000, "REGIC": "Metrópole", "Tabela Praticada": 2, "A++": 0.02, "A+": 0.08, "B1": 0.14},
    {"Unidade": "FT SALTO - SP", "Cidade": "Salto", "IsSP": True, "Renda Média": 6560, "População": 54900, "REGIC": "Centro Sub-Regional A", "Tabela Praticada": 2, "A++": 0.01, "A+": 0.04, "B1": 0.10},
    {"Unidade": "FT SANTA LÚCIA - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 19400, "População": 88597, "REGIC": "Metrópole", "Tabela Praticada": 3, "A++": 0.16, "A+": 0.24, "B1": 0.24},
    {"Unidade": "FT SANTA ROSA - RJ", "Cidade": "Niterói", "IsSP": False, "Renda Média": 17400, "População": 178510, "REGIC": "Capital Regional A", "Tabela Praticada": 2, "A++": 0.11, "A+": 0.18, "B1": 0.24},
    {"Unidade": "FT SANTANA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 17700, "População": 153100, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.15, "A+": 0.22, "B1": 0.18},
    {"Unidade": "FT SANTO AMARO - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 21100, "População": 82400, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.17, "A+": 0.21, "B1": 0.22},
    {"Unidade": "FT SÃO BENTO - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 16700, "População": 127317, "REGIC": "Metrópole", "Tabela Praticada": 2, "A++": 0.11, "A+": 0.22, "B1": 0.24},
    {"Unidade": "FT SÃO CAETANO - SP", "Cidade": "São Caetano do Sul", "IsSP": True, "Renda Média": 10200, "População": 122900, "REGIC": "Grande Metrópole", "Tabela Praticada": 3, "A++": 0.04, "A+": 0.06, "B1": 0.19},
    {"Unidade": "FT SAÚDE - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 17700, "População": 186000, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.13, "A+": 0.19, "B1": 0.21},
    {"Unidade": "FT SAUL MACEDO - MG", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 23100, "População": 63400, "REGIC": "Metrópole", "Tabela Praticada": 3, "A++": 0.22, "A+": 0.26, "B1": 0.17},
    {"Unidade": "FT SAVASSI - MG", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 19885, "População": 192365, "REGIC": "Metrópole", "Tabela Praticada": 3, "A++": 0.15, "A+": 0.27, "B1": 0.22},
    {"Unidade": "FT SETE LAGOAS - MG", "Cidade": "Sete Lagoas", "IsSP": False, "Renda Média": 12514, "População": 50760, "REGIC": "Capital Regional C", "Tabela Praticada": 1, "A++": 0.09, "A+": 0.14, "B1": 0.16},
    {"Unidade": "FT SETOR BUENO - GO", "Cidade": "Goiânia", "IsSP": False, "Renda Média": 17800, "População": 94500, "REGIC": "Metrópole", "Tabela Praticada": 3, "A++": 0.15, "A+": 0.24, "B1": 0.22},
    {"Unidade": "FT TAQUARAL - SP", "Cidade": "Campinas", "IsSP": True, "Renda Média": 12738, "População": 40203, "REGIC": "Capital Regional A", "Tabela Praticada": 3, "A++": 0.08, "A+": 0.14, "B1": 0.23},
    {"Unidade": "FT TIROL - RN", "Cidade": "Natal", "IsSP": False, "Renda Média": 15400, "População": 72800, "REGIC": "Capital Regional A", "Tabela Praticada": 2, "A++": 0.11, "A+": 0.18, "B1": 0.24},
    {"Unidade": "FT TRÊS PODERES - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 18100, "População": 587000, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.19, "A+": 0.18, "B1": 0.22},
    {"Unidade": "FT VERBO DIVINO - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 24800, "População": 77600, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.22, "A+": 0.23, "B1": 0.18},
    {"Unidade": "FT VILA OLIMPIA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 30900, "População": 160900, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.33, "A+": 0.26, "B1": 0.12},
    {"Unidade": "FT VILHENA - RO", "Cidade": "Vilhena", "IsSP": False, "Renda Média": 6100, "População": 42800, "REGIC": "Centro Sub-Regional", "Tabela Praticada": 1, "A++": 0.03, "A+": 0.10, "B1": 0.17},
    {"Unidade": "FT YPIRANGA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 19000, "População": 120000, "REGIC": "Grande Metrópole", "Tabela Praticada": 5, "A++": 0.10, "A+": 0.17, "B1": 0.20}
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

# ==========================================
# SIDEBAR - SELEÇÃO DE MÓDULO DO DASHBOARD
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='color:#FFFFFF; font-weight:800;'>Fast Tennis</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='color:#FFFFFF; font-weight:700; font-size:14px;'>Navegação da Plataforma</p>", unsafe_allow_html=True)
    
    modulo_selecionado = st.radio(
        "Selecione o Módulo Operacional:",
        ["1. Simulador de Precificação Inicial", "2. Reavaliação Estratégica (Unidades Ativas)"],
        key="modulo_navegacao",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(f"<small style='color:#FFFFFF;'>Sessão Ativa: <b>{st.session_state['usuario_logado']}</b></small>", unsafe_allow_html=True)
    if st.button("Sair do Sistema", use_container_width=True):
        st.session_state["autenticado"] = False
        st.rerun()

# ==============================================================================
# MÓDULO 1: SIMULADOR DE PRECIFICAÇÃO INICIAL
# ==============================================================================
if modulo_selecionado == "1. Simulador de Precificação Inicial":
    
    def limpar_campos_m1():
        st.session_state["val_estado"] = "Selecione..."
        st.session_state["val_cidade"] = ""
        st.session_state["val_populacao"] = 0
        st.session_state["val_classe_a_mais_mais"] = 0.0
        st.session_state["val_classe_a_mais"] = 0.0
        st.session_state["val_classe_b1"] = 0.0
        st.session_state["val_regic"] = "Selecione..."
        st.session_state["val_tipo_praca"] = "Selecione..."
        st.session_state["val_renda_media"] = 0.0
        st.session_state["val_tempo_proxima"] = 0
        st.session_state["val_media_mercado"] = 0.0
        st.session_state["val_viabilidade_bp"] = "Aguardando simulação..."

    if "val_estado" not in st.session_state:
        limpar_campos_m1()

    st.title("Simulador Estratégico de Precificação Inicial")
    st.markdown("---")
    
    st.subheader("1. Dados da Área de Estudo e Mercado")
    st.markdown("<p style='font-size:13.5px; color:#5A6578; margin-bottom:15px;'>Insira os dados geográficos e mercadológicos extraídos da ferramenta oficial.</p>", unsafe_allow_html=True)

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Localização e Demografia**")
            lista_estados = ["Selecione...", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
            estado = st.selectbox("Estado (UF):", lista_estados, key="val_estado")
            cidade = st.text_input("Cidade:", placeholder="Digite a cidade...", key="val_cidade")
            regic = st.selectbox("REGIC:", ["Selecione...", "Centro Sub-Regional", "Capital Regional C", "Capital Regional B", "Capital Regional A", "Metrópole", "Grande Metrópole", "Metrópole Nacional"], key="val_regic")
            populacao = st.number_input("População Total (Área):", min_value=0, step=1, key="val_populacao")

        with c2:
            st.markdown("**Percentuais de Classes**")
            classe_a_mais_mais = st.number_input("% Classe A++ (Ex: 0.15):", min_value=0.0, max_value=1.0, step=0.01, key="val_classe_a_mais_mais")
            classe_a_mais = st.number_input("% Classe A+ (Ex: 0.23):", min_value=0.0, max_value=1.0, step=0.01, key="val_classe_a_mais")
            classe_b1 = st.number_input("% Classe B1 (Ex: 0.21):", min_value=0.0, max_value=1.0, step=0.01, key="val_classe_b1")
            
            soma_percentuais = classe_b1 + classe_a_mais + classe_a_mais_mais
            calculo_alvo = int(soma_percentuais * populacao)
            
            st.markdown(f"""
                <div class="card-destaque">
                    <span style="color:#6C757D; font-size:11px; font-weight:700; text-transform:uppercase;">Público Alvo Calculado (B1 + A+ + A++)</span><br>
                    <span style="font-size:22px; font-weight:800; color:#022D8A;">{calculo_alvo:,} hab.</span><br>
                    <small style="color:#6C757D;">Soma das classes: <b>{soma_percentuais*100:.1f}%</b> da população.</small>
                </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown("**Mercado e Vocação**")
            tipo_praca = st.selectbox("Perfil da Praça:", ["Selecione...", "Comercial", "Mista", "Residencial", "Mista Qualificada"], key="val_tipo_praca")
            renda_media = st.number_input("Renda Média (R$):", min_value=0.0, step=100.0, key="val_renda_media")
            tempo_proxima = st.number_input("Tempo até unidade próxima (min):", min_value=0, step=1, key="val_tempo_proxima")
            media_mercado = st.number_input("Preço Médio Concorrentes (Plus 1x):", min_value=0.0, step=10.0, key="val_media_mercado")

        st.write("")
        col_btn1, col_btn2 = st.columns([5, 1.2])
        with col_btn2:
            st.button("Limpar Avaliação", on_click=limpar_campos_m1, use_container_width=True)

    dados_preenchidos = (
        estado != "Selecione..." and regic != "Selecione..." and tipo_praca != "Selecione..." and 
        cidade.strip() != "" and renda_media > 0 and media_mercado > 0
    )

    if not dados_preenchidos:
        st.info("Aguardando dados. Por favor, preencha as informações para gerar o diagnóstico.")
    else:
        # Lógica de Tabelas
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
        
        st.markdown('<div class="faixa-resultados">Análise Estratégica e Recomendações</div>', unsafe_allow_html=True)

        preco_sugerido = precos[tabela_sugerida]
        tkm_sugerido = tkms[tabela_sugerida]

        st.markdown(f"""
            <div class="tabela-sugerida-box">
                <p style="margin:0; font-size:11px; color:#6C757D; font-weight:bold; text-transform:uppercase;">Tabela Sugerida pelo Algoritmo (Perfil Econômico)</p>
                <h2>Tabela {tabela_sugerida}</h2>
                <p style="margin:0; font-size:14px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {preco_sugerido},00</b> | TKM Técnico: <b>R$ {tkm_sugerido},00</b></p>
            </div>
        """, unsafe_allow_html=True)

        aplicar_excecao = st.checkbox("Ativar exceção técnica (Sobrescrever tabela baseada no comportamento de mercado)", key="chk_excecao")

        justificativa_excecao = ""
        if aplicar_excecao:
            col_exc1, col_exc2 = st.columns([1, 2])
            with col_exc1:
                tabela_escolhida = st.selectbox("Selecione a Tabela Definitiva:", [1, 2, 3, 4, 5], index=tabela_sugerida - 1, key="val_tabela_excecao")
            with col_exc2:
                justificativa_excecao = st.text_input("Justificativa Estratégica (Obrigatório):", placeholder="Ex: Concorrência com forte posicionamento premium...", key="val_justificativa_excecao")

            tabela_final = tabela_escolhida
            st.markdown(f"""
                <div class="tabela-excecao-box">
                    <p style="margin:0; font-size:11px; color:#166534; font-weight:bold; text-transform:uppercase;">Tabela Escolhida por Decisão Técnica</p>
                    <h2>Tabela {tabela_final}</h2>
                    <p style="margin:0; font-size:14px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {precos[tabela_final]},00</b> | TKM Técnico: <b>R$ {tkms[tabela_final]},00</b></p>
                    {f'<p style="margin:6px 0 0 0; font-size:12px; color:#166534;"><b>Justificativa:</b> {justificativa_excecao}</p>' if justificativa_excecao else ''}
                </div>
            """, unsafe_allow_html=True)
        else:
            tabela_final = tabela_sugerida

        preco_ref = precos[tabela_final]
        tkm_ref = tkms[tabela_final]

        if tempo_proxima <= 15 and tempo_proxima > 0:
            st.markdown('<div class="alerta-fino">Proteção de Rede: Existe unidade próxima em raio inferior a 15 min. Verificar canibalização.</div>', unsafe_allow_html=True)

        st.markdown(f"<small style='color:#6C757D;'>Intervalo de tabelas calculadas (Algoritmo):</small> <b>Tab {tab_min} a {tab_max}</b>", unsafe_allow_html=True)
        
        dif_mercado = (preco_ref - media_mercado) / media_mercado if media_mercado > 0 else 0

        if dif_mercado < -0.10: diag, status, rec = "Abaixo da Média Regional", "Preço Abaixo do Mercado", "Avaliar margem para reposicionamento."
        elif dif_mercado <= 0.20: diag, status, rec = "Compatível com o Cenário", "Preço Aderente", "Posicionamento adequado ao mercado."
        else: diag, status, rec = "Muito Acima da Concorrência", "Descolamento de Preço", "Revisão mandatória em Comitê."

        st.write("")
        st.markdown("##### Relatório de Viabilidade de Mercado")
        cv1, cv2, cv3 = st.columns([1.2, 1.2, 1])
        with cv1: 
            st.markdown(f"""
                <div class="box-relatorio-equilibrado">
                    <span style="color:#6C757D; font-size:11px; font-weight:700; text-transform:uppercase;">DIRETRIZ E STATUS</span>
                    <span style="font-size:13px; color:#022D8A; margin-top:4px;"><b>Diretriz:</b> {diag}</span>
                    <span style="font-size:13px; color:#022D8A; margin-top:2px;"><b>Status:</b> {status}</span>
                </div>
            """, unsafe_allow_html=True)
        with cv2: 
            st.markdown(f"""
                <div class="box-relatorio-equilibrado" style="background-color: #FFFDF5; border-left: 4px solid #D69E2E;">
                    <span style="color:#975A16; font-size:11px; font-weight:700; text-transform:uppercase;">RECOMENDAÇÃO</span>
                    <span style="font-size:13px; color:#2D3748; margin-top:4px; line-height:1.3;">{rec}</span>
                </div>
            """, unsafe_allow_html=True)
        with cv3:
            st.markdown(f"""
                <div class="box-relatorio-equilibrado">
                    <span style="color:#6C757D; font-size:11px; font-weight:700; text-transform:uppercase;">DIFERENÇA MERCADO X FAST</span>
                    <span style="font-size:24px; font-weight:800; color:{'#D32F2F' if dif_mercado > 0.20 else '#2E7D32'}; margin-top:2px;">{dif_mercado*100:+.1f}%</span>
                </div>
            """, unsafe_allow_html=True)

        st.write("")
        with st.container(border=True):
            st.markdown("##### Viabilidade de Rentabilidade do Business Plan (BP)")
            cbp1, cb2 = st.columns(2)
            with cbp1:
                st.metric(label="TKM Técnico para o BP:", value=f"R$ {tkm_ref},00")
            with cb2:
                viabilidade_bp = st.selectbox(
                    "Status de rentabilidade projetada:", 
                    ["Aguardando simulação...", "Viável (Alinhado às Diretrizes do BP)", "Inviável (Payback projetado superior a 60 meses)", "Margem Líquida abaixo de R$ 10.000,00", "Margem Líquida entre R$ 10.000,00 e R$ 15.000,00", "Margem Líquida entre R$ 15.000,00 e R$ 20.000,00", "Margem Líquida acima de R$ 20.000,00"],
                    key="val_viabilidade_bp"
                )

        # RELATÓRIO OFICIAL EM IMPRESSÃO PDF
        st.write("")
        st.markdown("---")
        with st.expander("📄 Exportar Relatório Oficial (PDF)", expanded=False):
            st.info("Utilize a impressão nativa ou salve em PDF o documento formatado abaixo.")
            
            modo_definicao = f"Exceção Técnica ({justificativa_excecao})" if aplicar_excecao else "Análise de Dados do Algoritmo"
            info_tabela_economica = f'<p style="margin:4px 0 0 0; font-size:12px; color:#E2E8F0;">Tabela Sugerida Inicial: <b>Tabela {tabela_sugerida}</b> (Ref: R$ {preco_sugerido},00)</p>' if aplicar_excecao else ""

            html_relatorio = f"""
            <div style="font-family: Arial, sans-serif; background: #ffffff; padding: 25px; border: 2px solid #022D8A; border-radius: 8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="color:#022D8A; margin:0;">Relatório de Precificação Estratégica</h2>
                    <span style="font-size:12px; color:#6C757D;">Fast Tennis - Comitê de Expansão</span>
                </div>
                <hr style="border: 0; border-top: 1px solid #cbd5e0; margin: 15px 0;">
                
                <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 20px;">
                    <tr style="background-color:#F8F9FA;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>Praça / Cidade:</b> {cidade} - {estado}</td>
                        <td style="padding:8px; border:1px solid #ddd;"><b>População:</b> {populacao:,} hab.</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Renda Média:</b> R$ {renda_media:,.2f}</td>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Público Alvo (B1+A+ A++):</b> {calculo_alvo:,} hab. ({soma_percentuais*100:.1f}%)</td>
                    </tr>
                    <tr style="background-color:#F8F9FA;">
                        <td style="padding:8px; border:1px solid #ddd;"><b>REGIC / Perfil:</b> {regic} / {tipo_praca}</td>
                        <td style="padding:8px; border:1px solid #ddd;"><b>Preço Média Concorrentes:</b> R$ {media_mercado:,.2f}</td>
                    </tr>
                </table>

                <div style="background-color:#022D8A; color:#ffffff; padding:15px; border-radius:6px; margin-bottom:20px;">
                    <h3 style="margin:0; color:#0DF205;">TABELA SELECIONADA: TABELA {tabela_final}</h3>
                    <p style="margin:5px 0 0 0; font-size:14px;">Preço Ref. Plano Plus 1x: <b>R$ {preco_ref},00</b> | TKM Técnico: <b>R$ {tkm_ref},00</b></p>
                    <p style="margin:5px 0 0 0; font-size:12px; color:#E2E8F0;">Modo de Definição: <b>{modo_definicao}</b></p>
                    {info_tabela_economica}
                </div>

                <div style="font-size:13px; line-height:1.5; margin-bottom:20px;">
                    <p style="margin:0 0 5px 0;"><b>Diretriz Regional:</b> {diag}</p>
                    <p style="margin:0 0 5px 0;"><b>Status de Mercado:</b> {status} (Variação vs Concorrência: {dif_mercado*100:+.1f}%)</p>
                    <p style="margin:0 0 5px 0;"><b>Recomendação:</b> {rec}</p>
                    <p style="margin:0 0 5px 0;"><b>Status de Rentabilidade Projetada (BP):</b> {viabilidade_bp}</p>
                </div>
                <button onclick="window.print()" style="background-color: #0DF205; color: #022D8A; border: none; padding: 10px 20px; font-weight: bold; border-radius: 20px; cursor: pointer;">Imprimir / Salvar PDF</button>
            </div>
            """
            st.components.v1.html(html_relatorio, height=520, scrolling=True)


# ==============================================================================
# MÓDULO 2: REAVALIAÇÃO E REPRECIFICAÇÃO DE UNIDADES ATIVAS (AUTOMATIZADO)
# ==============================================================================
else:
    st.title("Reavaliação Estratégica de Unidades Ativas")
    st.markdown("Matriz de diagnóstico com carregamento automático dos dados demográficos e de mercado da unidade.")
    st.markdown("---")

    def limpar_campos_m2():
        st.session_state["m2_nome_u"] = "Selecione..."
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
        # EXTRAÇÃO AUTOMÁTICA DOS DADOS DO BANCO
        dados_u = df_base_unidades[df_base_unidades["Unidade"] == nome_unidade_sel].iloc[0]
        
        tab_praticada_u = int(dados_u["Tabela Praticada"])
        populacao_u = int(dados_u["População"])
        renda_u = float(dados_u["Renda Média"])
        pct_alvo_u = float(dados_u["A++"] + dados_u["A+"] + dados_u["B1"])
        num_alvo_u = int(pct_alvo_u * populacao_u)
        
        tkm_esperado_rede = TABELAS_OFICIAIS[tab_praticada_u]["tkm"]
        preco_plus_esperado = TABELAS_OFICIAIS[tab_praticada_u]["plus"]

        # 🟡 RESUMO AUTOMÁTICO DA UNIDADE
        st.markdown(f"""
            <div class="card-resumo-unidade">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h3 style="margin:0; color:#022D8A;">{dados_u['Unidade']} ({dados_u['Cidade']})</h3>
                    <span style="background-color:#022D8A; color:#0DF205; padding:4px 12px; border-radius:15px; font-weight:800; font-size:13px;">Tabela Praticada: Tabela {tab_praticada_u}</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:13px; color:#2D3748; flex-wrap:wrap; gap:10px;">
                    <div><b>População Residente:</b> {populacao_u:,} hab.</div>
                    <div><b>Público Alvo (B1+A+ A++):</b> {num_alvo_u:,} hab. ({pct_alvo_u*100:.1f}%)</div>
                    <div><b>Renda Média:</b> R$ {renda_u:,.2f}</div>
                    <div><b>TKM Esperado:</b> R$ {tkm_esperado_rede},00 | <b>Plano Plus 1x:</b> R$ {preco_plus_esperado},00</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

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

            # RELATÓRIO PDF PARA O MÓDULO 2
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

                html_pdf_m2 = f"""
                <div style="font-family: Arial, sans-serif; background: #ffffff; padding: 25px; border: 2px solid #022D8A; border-radius: 8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h2 style="color:#022D8A; margin:0;">Relatório de Reavaliação Estratégica</h2>
                        <span style="font-size:12px; color:#6C757D;">Fast Tennis - Diretoria Executiva</span>
                    </div>
                    <hr style="border: 0; border-top: 1px solid #cbd5e0; margin: 15px 0;">
                    
                    <h4 style="margin:0 0 10px 0; color:#022D8A;">Unidade: {dados_u['Unidade']} ({dados_u['Cidade']})</h4>
                    <p style="margin:0 0 15px 0; font-size:13px;">Tabela Praticada: <b>Tabela {tab_praticada_u}</b> | População: <b>{populacao_u:,} hab.</b> | Público Alvo: <b>{num_alvo_u:,} hab. ({pct_alvo_u*100:.1f}%)</b></p>
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 20px;">
                        <thead>
                            <tr style="background-color:#F8F9FA; text-align:left; color:#2D3748;">
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

                    <div style="background-color:#F8F9FA; border:1px solid #E2E8F0; padding:10px; border-radius:4px; margin-bottom:15px; text-align:center; font-size:13px;">
                        <b>Resumo:</b> <span style="color:#15803D;">Positivos: {qtd_positivos} ({pct_positivos:.0f}%)</span> | 
                        <span style="color:#A16207;">Atenção: {qtd_atencao}</span> | 
                        <span style="color:#B91C1C;">Críticos: {qtd_criticos}</span>
                    </div>

                    <div style="background-color:{bg_pop}; border-left:6px solid {cor_pop}; padding:15px; border-radius:6px; margin-bottom:20px;">
                        <h3 style="margin:0 0 5px 0; font-size:14px; color:{cor_pop};">Diretriz Estratégica (Comitê)</h3>
                        <p style="margin:0; font-size:14px; color:#2D3748; line-height:1.5;">{rec_pop}</p>
                    </div>
                    
                    <button onclick="window.print()" style="background-color: #0DF205; color: #022D8A; border: none; padding: 10px 20px; font-weight: bold; border-radius: 20px; cursor: pointer;">Imprimir / Salvar PDF</button>
                </div>
                """
                st.components.v1.html(html_pdf_m2, height=650, scrolling=True)
    else:
        st.info("Aguardando a seleção da unidade para carregar os dados demográficos do banco e iniciar a avaliação.")
