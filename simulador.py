import json
import re
import io
import unicodedata
from datetime import datetime
import pandas as pd
import streamlit as st
import altair as alt
from github import Auth, Github, GithubException

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA & IDENTIDADE VISUAL EXECUTIVA (FAST TENNIS)
# ==============================================================================
st.set_page_config(
    page_title="Reajuste Rede 2026",
    page_icon=None,
    layout="wide",
)

HEX_BLUE = "#053CD8"
HEX_NAVY = "#022D8A"
HEX_GREEN = "#16A34A"
HEX_RED = "#DC2626"
HEX_BG = "#F8FAFC"
HEX_CARD_BORDER = "#E2E8F0"

PERCENTUAL_IPCA = 0.0444        # 4,44% de Reajuste IPCA 2026
DESCONTO_MEDIO_REDE = 0.0130    # 1,30% de Impacto Médio de Descontos na Rede

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {HEX_BG}; }}
    h1, h2, h3, h4 {{ color: {HEX_NAVY} !important; font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 700; }}
    .stButton>button {{ background-color: {HEX_BLUE}; color: #FFFFFF; border-radius: 6px; font-weight: 600; border: none; padding: 0.6rem 1.8rem; }}
    .stButton>button:hover {{ background-color: {HEX_NAVY}; color: #FFFFFF; }}
    
    .sticky-unit-header {{ 
        position: -webkit-sticky; 
        position: sticky; 
        top: 0px; 
        z-index: 999; 
        background-color: #FFFFFF; 
        border-bottom: 3px solid {HEX_NAVY}; 
        padding: 10px 16px; 
        margin-bottom: 1rem; 
        border-radius: 8px; 
        box-shadow: 0 4px 12px rgba(2, 45, 138, 0.08); 
        min-height: 52px;
        display: flex;
        align-items: center;
    }}
    
    .stMultiSelect [data-baseweb="tag"], div[data-baseweb="select"] [data-baseweb="tag"], span[data-baseweb="tag"] {{ background-color: rgba(13, 242, 5, 0.04) !important; border: 1px solid rgba(13, 242, 5, 0.25) !important; border-radius: 4px !important; }}
    .stMultiSelect [data-baseweb="tag"] *, div[data-baseweb="select"] [data-baseweb="tag"] *, span[data-baseweb="tag"] * {{ color: {HEX_NAVY} !important; fill: {HEX_NAVY} !important; font-weight: 600 !important; }}
    
    .header-box {{ background-color: {HEX_NAVY}; padding: 1.1rem 1.8rem; border-radius: 8px; margin-bottom: 1.2rem; box-shadow: 0 2px 8px rgba(2, 45, 138, 0.12); display: flex; align-items: center; justify-content: space-between; }}
    .header-title {{ color: #FFFFFF !important; margin: 0; font-size: 1.35rem; font-weight: 800; letter-spacing: -0.3px; line-height: 1.2; }}
    .header-subtitle {{ color: #93C5FD; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin: 0; }}

    .kpi-card {{ background-color: #FFFFFF; border: 1px solid {HEX_CARD_BORDER}; border-radius: 8px; padding: 1rem 1.2rem; height: 110px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); display: flex; flex-direction: column; justify-content: space-between; position: relative; overflow: hidden; }}
    .kpi-card-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 3.5px; }}
    .kpi-title {{ font-size: 0.74rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }}
    .kpi-value {{ font-size: 1.65rem; font-weight: 800; color: {HEX_NAVY}; margin: 2px 0 0 0; line-height: 1; }}
    .kpi-sub {{ font-size: 0.72rem; font-weight: 600; color: #94A3B8; }}
    
    .executive-card-half {{ background-color: #FFFFFF; border: 1px solid {HEX_CARD_BORDER}; border-radius: 8px; padding: 1.2rem; height: 195px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); display: flex; flex-direction: column; justify-content: space-between; }}
    .executive-card-title {{ font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }}
    
    .table-highlight-card-full {{ background-color: rgba(5, 60, 216, 0.04); border: 1.5px solid rgba(5, 60, 216, 0.22); border-top: 4px solid {HEX_BLUE}; border-radius: 8px; padding: 1.2rem 1.8rem; margin-top: 1rem; margin-bottom: 0.8rem; box-shadow: 0 2px 5px rgba(5, 60, 216, 0.03); }}
    
    .state-unit-item {{ padding: 7px 10px; border-radius: 5px; margin-bottom: 3px; font-size: 0.83rem; display: flex; align-items: center; justify-content: space-between; }}
    .state-unit-selected {{ background-color: rgba(5, 60, 216, 0.08); border-left: 3px solid {HEX_BLUE}; font-weight: 700; color: {HEX_NAVY}; }}
    .state-unit-default {{ background-color: #F8FAFC; color: #334155; }}
    .mix-bar-container {{ margin-bottom: 8px; }}
    .mix-label {{ font-size: 0.82rem; font-weight: 600; color: #334155; display: flex; justify-content: space-between; margin-bottom: 2px; }}
    .mix-bar-bg {{ background-color: #F1F5F9; border-radius: 4px; height: 8px; width: 100%; overflow: hidden; }}
    .mix-bar-fill {{ background-color: {HEX_BLUE}; height: 100%; border-radius: 4px; }}
    
    .sim-card {{ background-color: #FFFFFF; border: 1px solid {HEX_CARD_BORDER}; border-radius: 8px; padding: 1rem 1.2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02); text-align: center; }}
    .sim-card-inline {{ text-align: center; padding: 6px 0 2px 0; }}
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. AUTENTICAÇÃO RESTREITA
# ==============================================================================
USER_OFICIAL = "operacoes@fasttennis.com.br"
SENHA_OFICIAL = "Reajuste8734"

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown(
        f"<h2 style='text-align: center; color: {HEX_NAVY}; margin-top: 3rem;'>Fast Tennis - Comite Executivo</h2>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("form_login"):
            st.subheader("Acesso Restrito")
            usuario_input = st.text_input("E-mail corporativo")
            senha_input = st.text_input("Senha", type="password")
            btn_login = st.form_submit_button("Acessar Painel")

            if btn_login:
                if usuario_input == USER_OFICIAL and senha_input == SENHA_OFICIAL:
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Credenciais invalidas.")
    st.stop()

# ==============================================================================
# 3. BASE DE DADOS COMPLEMENTAR & TABELA DE PREÇOS (2026)
# ==============================================================================
TKM_REDE_REFERENCIA = {1: 330, 2: 410, 3: 470, 4: 570, 5: 680}

TABELA_PRECOS_FALLBACK = {
    "Aulas em Grupo 1x na Semana Plus": {1: 349, 2: 419, 3: 529, 4: 629, 5: 749},
    "Aulas em Grupo 2x na Semana Plus": {1: 559, 2: 669, 3: 789, 4: 999, 5: 1379},
    "Aulas em Grupo 3x na Semana Plus": {1: 829, 2: 989, 3: 1249, 4: 1489, 5: 1899},
    "Aulas em Grupo 1x na Semana Smart": {1: 279, 2: 319, 3: 419, 4: 499, 5: 589},
    "Aulas em Grupo 2x na Semana Smart": {1: 439, 2: 519, 3: 609, 4: 799, 5: 1069},
    "Aulas em Grupo 3x na Semana Smart": {1: 669, 2: 789, 3: 999, 4: 1189, 5: 1499},
    "Aulas em Grupo KIDS 1X na semana": {1: 279, 2: 319, 3: 419, 4: 499, 5: 589},
    "Aulas em Grupo KIDS 2X na semana": {1: 439, 2: 519, 3: 609, 4: 799, 5: 1069},
    "Aulas em Grupo KIDS 3X na semana": {1: 669, 2: 789, 3: 999, 4: 1189, 5: 1499},
    "Aula Em Dupla 1x semana": {1: 529, 2: 619, 3: 849, 4: 949, 5: 1399},
    "Aula Individual 1x semana": {1: 899, 2: 1069, 3: 1289, 4: 1569, 5: 1759},
    "Locacao Recorrente": {1: 360, 2: 440, 3: 520, 4: 600, 5: 720},
    "Bolsista + familia franqueado": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "Infinite": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
}

COORDENADORES_MAP = {
    "Fast Tennis Aguas Claras - Brasilia": "Luan",
    "Fast Tennis Alphaville - Sao Paulo": "Alberto",
    "Fast Tennis Alto da Boa Vista - Sao Paulo": "Alberto",
    "Fast Tennis Alto de Pinheiros - Sao Paulo": "Alberto",
    "Fast Tennis Alto do Ipiranga - Sao Paulo": "Alberto",
    "Fast Tennis Anhanguera - Jundiai": "Luan",
    "Fast Tennis Bebedouro - Bebedouro": "Luan",
    "Fast Tennis Belvedere - Belo Horizonte": "Daniel",
    "Fast Tennis Boa Viagem - Recife": "Andressa",
    "Fast Tennis Botafogo - Campinas": "Luan",
    "Fast Tennis Brooklin - Sao Paulo": "Alberto",
    "Fast Tennis Buritis - Belo Horizonte": "Andressa",
    "Fast Tennis Buritis I - Belo Horizonte": "Andressa",
    "Fast Tennis Buritis II - Belo Horizonte": "Andressa",
    "Fast Tennis Buritis I e II - Belo Horizonte": "Andressa",
    "Fast Tennis Buritis I e  II - Belo Horizonte": "Andressa",
    "Fast Tennis Calafate - Belo Horizonte": "Luan",
    "Fast Tennis Campo Belo - Sao Paulo": "Alberto",
    "Fast Tennis Cantareira - Sao Paulo": "Alberto",
    "Fast Tennis Capim Macio - Natal": "Andressa",
    "Fast Tennis Castelo - Belo Horizonte": "Andressa",
    "Fast Tennis Centro Sao Bernardo - Sao Bernardo do Campo": "Alberto",
    "Fast Tennis Chacara Inglesa - Sao Paulo": "Alberto",
    "Fast Tennis Chacara Santo Antonio - Sao Paulo": "Alberto",
    "Fast Tennis Cidade Nova - Cidade Nova": "Andressa",
    "Fast Tennis Contagem - Contagem": "Luan",
    "Fast Tennis Estoril - Belo Horizonte": "Luan",
    "Fast Tennis Estrela Sul - Juiz de Fora": "Andressa",
    "Fast Tennis Eusebio - Eusebio": "Luan",
    "Fast Tennis General Lecor - Sao Paulo": "Alberto",
    "Fast Tennis Guararapes - Fortaleza": "Luan",
    "Fast Tennis Indaiatuba - Sao Paulo": "Andressa",
    "Fast Tennis Jardim Santo Andre - Sao Paulo": "Alberto",
    "Fast Tennis Jardim Portal da Colina - Sorocaba": "Alberto",
    "Fast Tennis Jardim Social - Curitiba": "Andressa",
    "Fast Tennis Lapa - Sao Paulo": "Alberto",
    "Fast Tennis Moema - Sao Paulo": "Alberto",
    "Fast Tennis Monte Pascal - Sao Paulo": "Alberto",
    "Fast Tennis Mooca - Sao Paulo": "Alberto",
    "Fast Tennis Morada da Colina - Uberlandia": "Luan",
    "Fast Tennis Morumbi - Sao Paulo": "Alberto",
    "Fast Tennis Nova Alianca Sul - Ribeirao Preto": "Andressa",
    "Fast Tennis Orla da Pampulha - Belo Horizonte": "Luan",
    "Fast Tennis Pampulha - Belo Horizonte": "Andressa",
    "Fast Tennis Parque Piqueri - Sao Paulo": "Alberto",
    "Fast Tennis Ponte JK - Brasilia": "Andressa",
    "Fast Tennis Praia do Canto - Vitoria": "Andressa",
    "Fast Tennis Praia Grande - Praia Grande": "Luan",
    "FastTennis Radial Leste - Sao Paulo": "Alberto",
    "Fast Tennis Recreio - Rio de Janeiro": "Andressa",
    "Fast Tennis Rio Claro - Sao Paulo": "Luan",
    "Fast Tennis Salgado Filho - Curitiba": "Andressa",
    "Fast Tennis Salto - Sao Paulo": "Andressa",
    "Fast Tennis Santa Lucia - Belo Horizonte": "Luan",
    "Fast Tennis Santana - Sao Paulo": "Alberto",
    "Fast Tennis Santa Rosa -  Niteroi": "Luan",
    "Fast Tennis Santo Amaro": "Alberto",
    "Fast Tennis Sao Bento - Belo Horizonte": "Luan",
    "Fast Tennis Sao Caetano - Sao Caetano do Sul": "Alberto",
    "Fast Tennis Saude - Sao Paulo": "Alberto",
    "Fast Tennis Saul Macedo - Belo Horizonte": "Andressa",
    "Fast Tennis Savassi - Belo Horizonte": "Luan",
    "Fast Tennis Sete Lagoas - Sete Lagoas": "Luan",
    "Fast Tennis Setor Bueno - Goiania": "Andressa",
    "Fast Tennis Taquaral - Campinas": "Luan",
    "Fast Tennis Tirol- Natal": "Andressa",
    "Fast Tennis Tres Poderes - Sao Paulo": "Alberto",
    "Fast Tennis Verbo Divino - Sao Paulo": "Alberto",
    "Fast Tennis Vila Olimpia - Sao Paulo": "Alberto",
    "Fast Tennis Vila Sonia - Sao Paulo": "Alberto",
    "Fast Tennis Vilhena - Rondonia": "Luan",
    "Fast Tennis Ypiranga - Sao Paulo": "Alberto",
    "Fast Tennis L4 Sul": "Andressa",
}

QUADRAS_MAP = {
    "Fast Tennis Aguas Claras - Brasilia": 3,
    "Fast Tennis Alphaville - Sao Paulo": 1,
    "Fast Tennis Alto da Boa Vista - Sao Paulo": 1,
    "Fast Tennis Alto de Pinheiros - Sao Paulo": 1,
    "Fast Tennis Alvaro Guimaraes - SBS": 1,
    "Fast Tennis Alto do Ipiranga - Sao Paulo": 2,
    "Fast Tennis Anhanguera - Jundiai": 1,
    "Fast Tennis Bebedouro - Bebedouro": 2,
    "Fast Tennis Belvedere - Belo Horizonte": 5,
    "Fast Tennis Boa Viagem - Recife": 2,
    "Fast Tennis Botafogo - Campinas": 1,
    "Fast Tennis Brooklin - Sao Paulo": 2,
    "Fast Tennis Buritis I - Belo Horizonte": 1,
    "Fast Tennis Buritis II - Belo Horizonte": 2,
    "Fast Tennis Buritis I e  II - Belo Horizonte": 3,
    "Fast Tennis Buritis I e II - Belo Horizonte": 3,
    "Fast Tennis Buritis - Belo Horizonte": 3,
    "Fast Tennis Calafate - Belo Horizonte": 1,
    "Fast Tennis Campo Belo - Sao Paulo": 1,
    "Fast Tennis Cantareira - Sao Paulo": 1,
    "Fast Tennis Capim Macio - Natal": 2,
    "Fast Tennis Castelo - Belo Horizonte": 1,
    "Fast Tennis Centro Sao Bernardo - Sao Bernardo do Campo": 1,
    "Fast Tennis Chacara Inglesa - Sao Paulo": 1,
    "Fast Tennis Chacara Santo Antonio - Sao Paulo": 2,
    "Fast Tennis Cidade Nova - Cidade Nova": 2,
    "Fast Tennis Contagem - Contagem": 1,
    "Fast Tennis Estoril - Belo Horizonte": 1,
    "Fast Tennis Estrela Sul - Juiz de Fora": 2,
    "Fast Tennis Eusebio - Eusebio": 2,
    "Fast Tennis General Lecor - Sao Paulo": 1,
    "Fast Tennis Guararapes - Fortaleza": 3,
    "Fast Tennis Indaiatuaba - Sao Paulo": 1,
    "Fast Tennis Interlagos - Sao Paulo": 1,
    "Fast Tennis Jardim - Sao Paulo": 1,
    "Fast Tennis Jardim Portal da Colina - Sorocaba": 2,
    "Fast Tennis Jardim Social - Curitiba": 2,
    "Fast Tennis L4 Sul": 2,
    "Fast Tennis Lapa - Sao Paulo": 4,
    "Fast Tennis Moema - Sao Paulo": 1,
    "Fast Tennis Monte Pascal - Sao Paulo": 1,
    "Fast Tennis Mooca - Sao Paulo": 1,
    "Fast Tennis Morada da Colina - Uberlandia": 1,
    "Fast Tennis Morumbi - Sao Paulo": 1,
    "Fast Tennis Nova Alianca Sul - Ribeirao Preto": 2,
    "Fast Tennis Orla da Pampulha - Belo Horizonte": 4,
    "Fast Tennis Pampulha - Belo Horizonte": 1,
    "Fast Tennis Parque Piqueri - Sao Paulo": 1,
    "Fast Tennis Ponte JK - Brasilia": 3,
    "Fast Tennis Praia do Canto - Vitoria": 1,
    "Fast Tennis Praia Grande - Praia Grande": 2,
    "Fast Tennis Radial Leste - Sao Paulo": 1,
    "Fast Tennis Recreio - Rio de Janeiro": 1,
    "Fast Tennis Rio Claro - Sao Paulo": 2,
    "Fast Tennis Salgado Filho - Curitiba": 1,
    "Fast Tennis Salto - Sao Paulo": 1,
    "Fast Tennis Santa Lucia - Belo Horizonte": 2,
    "Fast Tennis Santana - Sao Paulo": 2,
    "Fast Tennis Santa Rosa - Niteroi": 1,
    "Fast Tennis Santo Amaro": 1,
    "Fast Tennis Sao Bento - Belo Horizonte": 2,
    "Fast Tennis Sao Caetano - Sao Caetano do Sul": 2,
    "Fast Tennis Saude - Sao Paulo": 1,
    "Fast Tennis Saul Macedo - Belo Horizonte": 1,
    "Fast Tennis Savassi - Belo Horizonte": 1,
    "Fast Tennis Sete Lagoas - Sete Lagoas": 2,
    "Fast Tennis Setor Bueno - Goiania": 1,
    "Fast Tennis Taquaral - Campinas": 1,
    "Fast Tennis Taubate - Taubate": 1,
    "Fast Tennis Tirol- Natal": 1,
    "Fast Tennis Tres Poderes - Sao Paulo": 1,
    "Fast Tennis Verbo Divino - Sao Paulo": 1,
    "Fast Tennis Vila Olimpia - Sao Paulo": 2,
    "Fast Tennis Vila Sonia": 1,
    "Fast Tennis Vilhena - Rondonia": 1,
    "Fast Tennis Ypiranga - Sao Paulo": 1,
}

ORDEM_MESES_MAP = {
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
    "atual": 99,
}

def normalizar_texto(texto):
    txt = unicodedata.normalize("NFD", str(texto)).encode("ascii", "ignore").decode("utf-8")
    txt = txt.replace("\t", " ").replace("\n", " ").replace("-", " ").replace("fasttennis", "fast tennis")
    return " ".join(txt.lower().split())

def formatar_nome_mes(nome_aba):
    txt = nome_aba.replace("Mix de Produtos", "").replace("Mix", "").strip()
    return txt if txt else "Atual"

def obter_ordem_mes(rotulo_mes):
    norm = normalizar_texto(rotulo_mes)
    for m_key, val_ord in ORDEM_MESES_MAP.items():
        if m_key in norm:
            return val_ord
    return 50

VARIACOES_OFICIAIS = {
    # 1x Plus
    "aulas em grupo 1x na semana plus": "Aulas em Grupo 1x na Semana Plus",
    "aula em grupo 1x na semana plus": "Aulas em Grupo 1x na Semana Plus",
    "aula em grupo 1x por semana plus": "Aulas em Grupo 1x na Semana Plus",
    "aulas em grupo 1x por semana plus": "Aulas em Grupo 1x na Semana Plus",

    # 2x Plus
    "aulas em grupo 2x na semana plus": "Aulas em Grupo 2x na Semana Plus",
    "aula em grupo 2x na semana plus": "Aulas em Grupo 2x na Semana Plus",
    "aula em grupo 2x por semana plus": "Aulas em Grupo 2x na Semana Plus",
    "aulas em grupo 2x por semana plus": "Aulas em Grupo 2x na Semana Plus",

    # 3x Plus
    "aulas em grupo 3x na semana plus": "Aulas em Grupo 3x na Semana Plus",
    "aula em grupo 3x na semana plus": "Aulas em Grupo 3x na Semana Plus",
    "aula em grupo 3x por semana plus": "Aulas em Grupo 3x na Semana Plus",
    "aulas em grupo 3x por semana plus": "Aulas em Grupo 3x na Semana Plus",

    # 1x Smart
    "aulas em grupo 1x na semana smart": "Aulas em Grupo 1x na Semana Smart",
    "aula em grupo 1x na semana smart": "Aulas em Grupo 1x na Semana Smart",
    "aula em grupo 1x por semana smart": "Aulas em Grupo 1x na Semana Smart",
    "aulas em grupo 1x por semana smart": "Aulas em Grupo 1x na Semana Smart",

    # 2x Smart
    "aulas em grupo 2x na semana smart": "Aulas em Grupo 2x na Semana Smart",
    "aula em grupo 2x na semana smart": "Aulas em Grupo 2x na Semana Smart",
    "aula em grupo 2x por semana smart": "Aulas em Grupo 2x na Semana Smart",
    "aulas em grupo 2x por semana smart": "Aulas em Grupo 2x na Semana Smart",

    # 3x Smart
    "aulas em grupo 3x na semana smart": "Aulas em Grupo 3x na Semana Smart",
    "aula em grupo 3x na semana smart": "Aulas em Grupo 3x na Semana Smart",
    "aula em grupo 3x por semana smart": "Aulas em Grupo 3x na Semana Smart",
    "aulas em grupo 3x por semana smart": "Aulas em Grupo 3x na Semana Smart",

    # KIDS 1x
    "aulas em grupo kids 1x na semana": "Aulas em Grupo KIDS 1X na semana",
    "aula em grupo 1x por semana kids": "Aulas em Grupo KIDS 1X na semana",
    "aula kids em grupo 1x na semana": "Aulas em Grupo KIDS 1X na semana",
    "aulas em grupo kids 1x por semana": "Aulas em Grupo KIDS 1X na semana",

    # KIDS 2x
    "aulas em grupo kids 2x na semana": "Aulas em Grupo KIDS 2X na semana",
    "aula em grupo 2x por semana kids": "Aulas em Grupo KIDS 2X na semana",
    "aula kids em grupo 2x na semana": "Aulas em Grupo KIDS 2X na semana",
    "aulas em grupo kids 2x por semana": "Aulas em Grupo KIDS 2X na semana",

    # KIDS 3x
    "aulas em grupo kids 3x na semana": "Aulas em Grupo KIDS 3X na semana",
    "aula em grupo 3x por semana kids": "Aulas em Grupo KIDS 3X na semana",
    "aula kids em grupo 3x na semana": "Aulas em Grupo KIDS 3X na semana",
    "aulas em grupo kids 3x por semana": "Aulas em Grupo KIDS 3X na semana",

    # Dupla
    "aula em dupla 1x semana": "Aula Em Dupla 1x semana",
    "aula em dupla 1x por semana plus": "Aula Em Dupla 1x semana",

    # Individual
    "aula individual 1x semana": "Aula Individual 1x semana",
    "aula individual 1x por semana": "Aula Individual 1x semana",

    # Locacao Recorrente
    "locacao recorrente": "Locacao Recorrente",

    # Bolsista / Familia
    "bolsista": "Bolsista + familia franqueado",

    # Infinite
    "infinite": "Infinite",
}

def categorizar_plano_ampliado(plano_raw, mapa_excel=None):
    p_norm = normalizar_texto(plano_raw)

    if mapa_excel and p_norm in mapa_excel:
        return mapa_excel[p_norm]

    if p_norm in VARIACOES_OFICIAIS:
        return VARIACOES_OFICIAIS[p_norm]

    for var_key, cat_val in VARIACOES_OFICIAIS.items():
        if var_key in p_norm or p_norm in var_key:
            return cat_val

    return str(plano_raw).strip()

def categorizar_plano_v1(plano_raw, mapa_excel=None):
    cat = categorizar_plano_ampliado(plano_raw, mapa_excel)
    
    # LISTA FIXA E ESTRITA DOS 11 PLANOS SOLICITADOS
    LISTA_MIX_PADRAO_EXATA = [
        "Aulas em Grupo 1x na Semana Plus",
        "Aulas em Grupo 2x na Semana Plus",
        "Aulas em Grupo 3x na Semana Plus",
        "Aulas em Grupo 1x na Semana Smart",
        "Aulas em Grupo 2x na Semana Smart",
        "Aulas em Grupo 3x na Semana Smart",
        "Aulas em Grupo KIDS 1X na semana",
        "Aulas em Grupo KIDS 2X na semana",
        "Aulas em Grupo KIDS 3X na semana",
        "Aula Em Dupla 1x semana",
        "Aula Individual 1x semana",
    ]
    
    if cat in LISTA_MIX_PADRAO_EXATA:
        return cat
        
    return None

def formatar_kpi_cor(valor_num):
    if valor_num is None or pd.isna(valor_num): return "N/A", "#64748B"
    try:
        val_float = float(valor_num)
        pct_val = val_float * 100 if abs(val_float) <= 10.0 else val_float
        cor = "#DC2626" if pct_val < 80.0 else ("#D97706" if pct_val < 90.0 else "#16A34A")
        return f"{pct_val:.1f}%", cor
    except Exception:
        return str(valor_num), "#64748B"

def formatar_nao_fechamento_cor(valor_num):
    if valor_num is None or pd.isna(valor_num): return "N/A", "#64748B"
    try:
        val_float = float(valor_num)
        pct_val = val_float * 100 if abs(val_float) <= 10.0 else val_float
        cor = "#DC2626" if pct_val > 15.0 else ("#D97706" if pct_val >= 10.0 else "#16A34A")
        return f"{pct_val:.1f}%", cor
    except Exception:
        return str(valor_num), "#64748B"

def obter_dados_unidade(nome_unidade):
    u_norm = normalizar_texto(nome_unidade)
    gr = "Nao Cadastrado"
    for k, v in COORDENADORES_MAP.items():
        k_norm = normalizar_texto(k)
        if k_norm in u_norm or u_norm in k_norm or ("buritis" in u_norm and "buritis" in k_norm):
            gr = v
            break
    quadras = "N/A"
    for k, v in QUADRAS_MAP.items():
        k_norm = normalizar_texto(k)
        if k_norm in u_norm or u_norm in k_norm or ("buritis" in u_norm and "buritis" in k_norm):
            quadras = str(v)
            break
    return gr, quadras

def obter_comparacao_tkm(tabela_str, tkm_unidade):
    digits = re.findall(r"\d+", str(tabela_str))
    if not digits: return ""
    num_tabela = int(digits[0])
    tkm_rede = TKM_REDE_REFERENCIA.get(num_tabela)
    if not tkm_rede or not isinstance(tkm_unidade, (int, float)) or tkm_unidade == 0:
        return ""
    diff_pct = ((tkm_unidade - tkm_rede) / tkm_rede) * 100
    sinal = "+" if diff_pct >= 0 else ""
    return f"({sinal}{diff_pct:.1f}% em relacao a Tabela {num_tabela} Rede - R$ {tkm_rede})"

def obter_observacao_excel(row_data):
    for col_name in row_data.index:
        col_clean = normalizar_texto(col_name)
        if any(term in col_clean for term in ["observac", "sugestao", "recomendac", "comentario"]):
            val = str(row_data[col_name]).strip()
            if val and val.lower() != "nan" and val.lower() != "none":
                return val
    return None

def desenhar_grafico_barras_altair(df_input, col_x, col_y, tipo_formato="numero"):
    df_sorted = df_input.sort_values(by="Ordem").reset_index(drop=True)
    
    if tipo_formato == "moeda":
        df_sorted["Rotulo"] = df_sorted[col_y].apply(lambda x: f"R$ {x:,.2f}")
    else:
        df_sorted["Rotulo"] = df_sorted[col_y].apply(lambda x: f"{x:,.0f}")

    base = alt.Chart(df_sorted).encode(
        x=alt.X(f"{col_x}:N", sort=df_sorted[col_x].tolist(), axis=alt.Axis(title=None, labelAngle=0, labelFontWeight="bold")),
        y=alt.Y(f"{col_y}:Q", axis=None)
    )

    bars = base.mark_bar(color=HEX_BLUE, cornerRadiusTopLeft=4, cornerRadiusTopRight=4, size=38)
    
    text = base.mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        fontWeight='bold',
        color=HEX_NAVY,
        fontSize=12
    ).encode(
        text='Rotulo:N'
    )

    chart = (bars + text).properties(height=210).configure_view(strokeWidth=0)
    st.altair_chart(chart, use_container_width=True)

# ==============================================================================
# 4. GESTÃO DE DADOS & PERSISTÊNCIA VIA GITHUB API (COM CACHE)
# ==============================================================================
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "").strip()
REPO_NAME = st.secrets.get("REPO_NAME", "").strip()
EXCEL_FILE = "Planejamento Reajuste.xlsx"
DECISOES_FILE = "decisoes_comite.json"

def obter_cliente_github():
    if not GITHUB_TOKEN: return None
    return Github(auth=Auth.Token(GITHUB_TOKEN))

@st.cache_data(ttl=10)
def carregar_decisoes_salvas():
    if not GITHUB_TOKEN or not REPO_NAME: return {}
    try:
        g = obter_cliente_github()
        repo = g.get_repo(REPO_NAME)
        file_content = repo.get_contents(DECISOES_FILE)
        return json.loads(file_content.decoded_content.decode("utf-8"))
    except Exception:
        return {}

def salvar_decisoes_github(novas_decisoes):
    if not GITHUB_TOKEN or not REPO_NAME:
        st.error("Secrets GITHUB_TOKEN ou REPO_NAME nao configuradas.")
        return False
    try:
        g = obter_cliente_github()
        repo = g.get_repo(REPO_NAME)
        content = json.dumps(novas_decisoes, indent=4, ensure_ascii=False)
        try:
            file_content = repo.get_contents(DECISOES_FILE)
            repo.update_file(path=DECISOES_FILE, message="Atualizacao de decisoes do Comite Fast Tennis", content=content, sha=file_content.sha)
        except GithubException:
            repo.create_file(path=DECISOES_FILE, message="Inicializacao de decisoes do Comite Fast Tennis", content=content)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Erro na comunicacao com o repositorio: {e}")
        return False

def formatar_data_br(data_val):
    if pd.isna(data_val): return "N/A"
    try:
        dt = pd.to_datetime(data_val, dayfirst=True, errors="coerce")
        return str(data_val) if pd.isna(dt) else dt.strftime("%d/%m/%Y")
    except:
        return str(data_val)

def calcular_meses_operacao(data_val):
    try:
        dt = pd.to_datetime(data_val, dayfirst=True, errors="coerce")
        if pd.isna(dt): return 0
        hoje = datetime.now()
        return max(0, (hoje.year - dt.year) * 12 + (hoje.month - dt.month))
    except:
        return 0

def sanitizar_recomendacao(texto):
    if not isinstance(texto, str) or not texto.strip(): return "Sem sugestao previa cadastrada."
    txt = " ".join(texto.strip().split()).replace(" ( ", " (").replace(" ,", ",").replace(" ,)", ")")
    txt = txt.replace("clienets", "clientes").replace("atabela", "a tabela")
    return txt[0].upper() + txt[1:]

def converter_para_numero(valor):
    if pd.isna(valor): return 0.0
    val_str = str(valor).replace("R$", "").replace("r$", "").replace(" ", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(val_str)
    except:
        return 0.0

def limpar_texto_ascii(texto):
    txt_str = str(texto)
    return unicodedata.normalize("NFD", txt_str).encode("ascii", "ignore").decode("utf-8")

@st.cache_data(ttl=300)
def carregar_dados_planilha(caminho_ou_file):
    try:
        xls = pd.ExcelFile(caminho_ou_file)
        
        df_m = pd.read_excel(xls, sheet_name=0)
        df_m.columns = df_m.columns.astype(str).str.strip()

        dict_mix_historico = {}
        for nome_aba in xls.sheet_names:
            col_aba_norm = normalizar_texto(nome_aba)
            if "mix" in col_aba_norm:
                if any(m in col_aba_norm for m in ["janeiro", "fevereiro", "marco"]):
                    continue
                df_temp = pd.read_excel(xls, sheet_name=nome_aba)
                df_temp.columns = df_temp.columns.astype(str).str.strip()
                dict_mix_historico[nome_aba] = df_temp

        if not dict_mix_historico:
            if "Mix de Produtos Atual" in xls.sheet_names:
                df_temp = pd.read_excel(xls, sheet_name="Mix de Produtos Atual")
                df_temp.columns = df_temp.columns.astype(str).str.strip()
                dict_mix_historico["Mix de Produtos Atual"] = df_temp
            else:
                dict_mix_historico["Mix de Produtos Atual"] = pd.DataFrame()

        df_ft = pd.read_excel(xls, sheet_name="Faturamento e LL") if "Faturamento e LL" in xls.sheet_names else None
        if df_ft is not None: df_ft.columns = df_ft.columns.astype(str).str.strip()

        # LEITURA DA ABA VARIAÇÕES DE PLANO
        mapa_excel = {}
        if "Variacoes de Plano" in xls.sheet_names or "Variações de Plano" in xls.sheet_names:
            nome_aba_vp = next(c for c in xls.sheet_names if "variac" in normalizar_texto(c))
            df_vp = pd.read_excel(xls, sheet_name=nome_aba_vp)
            if len(df_vp.columns) >= 2:
                col_de = df_vp.columns[0]
                col_para = df_vp.columns[1]
                for _, r_vp in df_vp.iterrows():
                    val_de = normalizar_texto(r_vp[col_de])
                    val_para = str(r_vp[col_para]).strip()
                    if val_de and val_para:
                        mapa_excel[val_de] = val_para

        tabela_precos = TABELA_PRECOS_FALLBACK.copy()
        if "Tabelas Praticadas" in xls.sheet_names:
            df_tp = pd.read_excel(xls, sheet_name="Tabelas Praticadas")
            if not df_tp.empty and len(df_tp.columns) >= 2:
                col_plano = df_tp.columns[0]
                for _, row_tp in df_tp.iterrows():
                    plano_cat = str(row_tp[col_plano]).strip()
                    if plano_cat in tabela_precos:
                        for idx_t in range(1, 6):
                            col_t_found = next((c for c in df_tp.columns if f"tabela {idx_t}" in normalizar_texto(c) or f"tabela{idx_t}" in normalizar_texto(c)), None)
                            if col_t_found:
                                tabela_precos[plano_cat][idx_t] = converter_para_numero(row_tp[col_t_found])

        return df_m, dict_mix_historico, df_ft, mapa_excel, tabela_precos
    except Exception as e:
        st.error(f"Erro no carregamento das abas: {e}")
        return None, {}, None, {}, TABELA_PRECOS_FALLBACK

st.sidebar.markdown("### Base de Dados")
uploaded_file = st.sidebar.file_uploader("Carregar Planilha (.xlsx)", type=["xlsx", "csv"])

if uploaded_file is not None:
    df, dict_mix_historico, df_fat, mapa_excel_carregado, tabela_precos_carregada = carregar_dados_planilha(uploaded_file)
else:
    df, dict_mix_historico, df_fat, mapa_excel_carregado, tabela_precos_carregada = carregar_dados_planilha(EXCEL_FILE)

if df is None: st.stop()

col_unidade_df = next((c for c in df.columns if normalizar_texto(c) in ["unidade", "unidades"]), df.columns[0])
col_tabela_df = next((c for c in df.columns if "tabela praticada" in normalizar_texto(c) or "tabela" in normalizar_texto(c)), None)
col_uf_df = next((c for c in df.columns if normalizar_texto(c) == "uf"), None)

if "Inicio da Operacao" in df.columns or "Início da Operação" in df.columns:
    col_ini = "Início da Operação" if "Início da Operação" in df.columns else "Inicio da Operacao"
    df["Tempo de Operacao (Meses)"] = df[col_ini].apply(calcular_meses_operacao)

df["GR Responsavel"] = df[col_unidade_df].apply(lambda u: obter_dados_unidade(u)[0])

decisoes_salvas = carregar_decisoes_salvas()

def calcular_alunos_mix_unidade_df(df_mix_ref, nome_unidade):
    if df_mix_ref is None or df_mix_ref.empty: return None
    col_u_mix = next((c for c in df_mix_ref.columns if "unid" in str(c).lower()), None)
    col_p_mix = next((c for c in df_mix_ref.columns if "plano" in str(c).lower() or "produto" in str(c).lower()), None)
    if not col_u_mix or not col_p_mix: return None

    u_main_norm = normalizar_texto(nome_unidade)
    def pertence_unidade(u_mix_val):
        u_mix_norm = normalizar_texto(u_mix_val)
        return u_mix_norm in u_main_norm or u_main_norm in u_mix_norm or ("buritis" in u_mix_norm and "buritis" in u_main_norm) or ("orla" in u_mix_norm and "orla" in u_main_norm)

    df_mix_u = df_mix_ref[df_mix_ref[col_u_mix].apply(pertence_unidade)].copy()
    if df_mix_u.empty: return None
    df_mix_u["Plano_Cat"] = df_mix_u[col_p_mix].apply(lambda p: categorizar_plano_ampliado(p, mapa_excel_carregado))
    val_count = df_mix_u["Plano_Cat"].notnull().sum()
    return val_count if val_count > 0 else None

# EXPORTACAO EXCEL COMPLETA, SEM ACENTOS E SEM EMOJIS
st.sidebar.markdown("---")
st.sidebar.markdown("### Exportar Resultados")

def gerar_excel_limpo_comite(df_orig, decisoes):
    lista_linhas = []
    for _, r in df_orig.iterrows():
        u_nome = r[col_unidade_df]
        gr_resp = obter_dados_unidade(u_nome)[0]
        tab_praticada = r.get(col_tabela_df, "N/A") if col_tabela_df else "N/A"
        
        dec_info = decisoes.get(u_nome, {})
        dec_atuais = dec_info.get("decisao_atuais", "Pendente")
        dec_novos = dec_info.get("decisao_novos", "Pendente")
        tab_vigentes = ", ".join(dec_info.get("tabelas_vigentes", [])) if dec_info.get("tabelas_vigentes") else "Pendente"
        conceito_txt = dec_info.get("observacoes_comite", "")

        lista_linhas.append({
            "Unidade": u_nome,
            "Tabela Praticada": tab_praticada,
            "Decisao - Clientes Atuais": dec_atuais,
            "Decisao - Novos Clientes": dec_novos,
            "Tabelas Vigentes": tab_vigentes,
            "GR Responsavel": gr_resp,
            "Conceito": conceito_txt
        })
    
    df_exp = pd.DataFrame(lista_linhas)
    
    for col in df_exp.columns:
        df_exp[col] = df_exp[col].apply(limpar_texto_ascii)

    buffer = io.BytesIO()
    try:
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df_exp.to_excel(writer, index=False, sheet_name="Decisoes Comite")
            worksheet = writer.sheets["Decisoes Comite"]
            for i, col in enumerate(df_exp.columns):
                max_len = max(df_exp[col].astype(str).map(len).max(), len(col)) + 3
                worksheet.set_column(i, i, max_len)
    except Exception:
        with pd.ExcelWriter(buffer) as writer:
            df_exp.to_excel(writer, index=False, sheet_name="Decisoes Comite")

    return buffer.getvalue()

excel_bytes = gerar_excel_limpo_comite(df, decisoes_salvas)

st.sidebar.download_button(
    label="Baixar Resumo Executivo (Excel)",
    data=excel_bytes,
    file_name=f"decisoes_comite_fasttennis_{datetime.now().strftime('%Y%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.markdown(
    f"""
    <div class='header-box'>
        <div>
            <span class='header-subtitle'>Programacao Reajuste Rede 2026</span>
            <h1 class='header-title'>Analise e Decisao de Reajustes Fast Tennis</h1>
        </div>
        <div>
            <span style='background-color: rgba(255,255,255,0.12); color: #FFFFFF; font-size: 0.78rem; font-weight: 700; padding: 6px 12px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2);'>Comite Executivo</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

tab_visao_geral, tab_analise_decisao = st.tabs(["Visao Geral Consolidada", "Analise e Decisao por Unidade"])

# ==============================================================================
# TAB 1: VISÃO GERAL CONSOLIDADA
# ==============================================================================
with tab_visao_geral:
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        if col_tabela_df:
            opcoes_tabela = ["Todas"] + sorted([str(t) for t in df[col_tabela_df].dropna().unique() if str(t).strip() != ""])
        else:
            opcoes_tabela = ["Todas"]
        tabela_filtro = st.selectbox("Tabela Praticada:", opcoes_tabela, index=0)

    with col_f2:
        if col_uf_df:
            opcoes_uf = ["Todos"] + sorted([str(u) for u in df[col_uf_df].dropna().unique() if str(u).strip() != ""])
        else:
            opcoes_uf = ["Todos"]
        uf_filtro = st.selectbox("Estado (UF):", opcoes_uf, index=0)

    with col_f3:
        grs_unicos = sorted([str(g) for g in df["GR Responsavel"].dropna().unique() if str(g).strip() != ""])
        opcoes_gr = ["Todos"] + grs_unicos
        gr_filtro = st.selectbox("Gerente de Resultados (GR):", opcoes_gr, index=0)

    with col_f4:
        dict_meses_rotulados = {formatar_nome_mes(k): k for k in dict_mix_historico.keys()}
        opcoes_rotulos_mes = list(dict_meses_rotulados.keys())
        idx_default_mes = next((i for i, m in enumerate(opcoes_rotulos_mes) if "atual" in normalizar_texto(m)), len(opcoes_rotulos_mes) - 1)
        rotulo_mes_selecionado = st.selectbox("Mes de Referencia:", opcoes_rotulos_mes, index=max(0, idx_default_mes))
        mes_mix_chave_real = dict_meses_rotulados[rotulo_mes_selecionado]

    df_mix_atual = dict_mix_historico.get(mes_mix_chave_real, pd.DataFrame())

    df_filtrado = df.copy()
    if tabela_filtro != "Todas" and col_tabela_df:
        df_filtrado = df_filtrado[df_filtrado[col_tabela_df].astype(str) == tabela_filtro]
    if uf_filtro != "Todos" and col_uf_df:
        df_filtrado = df_filtrado[df_filtrado[col_uf_df].astype(str) == uf_filtro]
    if gr_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["GR Responsavel"].astype(str) == gr_filtro]

    total_unidades = len(df_filtrado)
    analisadas = sum(1 for u in df_filtrado[col_unidade_df].unique() if u in decisoes_salvas)
    pendentes = total_unidades - analisadas
    pct_concluido = (analisadas / total_unidades * 100) if total_unidades > 0 else 0

    if df_mix_atual is not None and not df_mix_atual.empty:
        col_u_mix_gen = next((c for c in df_mix_atual.columns if "unid" in str(c).lower()), None)
        col_p_mix_gen = next((c for c in df_mix_atual.columns if "plano" in str(c).lower() or "produto" in str(c).lower()), None)
        if col_u_mix_gen and col_p_mix_gen:
            unidades_permitidas_norm = [normalizar_texto(u) for u in df_filtrado[col_unidade_df].unique()]
            def pertence_selecao(u_mix_val):
                u_mix_norm = normalizar_texto(u_mix_val)
                for u_perm in unidades_permitidas_norm:
                    if u_mix_norm in u_perm or u_perm in u_mix_norm or ("buritis" in u_mix_norm and "buritis" in u_perm) or ("orla" in u_mix_norm and "orla" in u_perm):
                        return True
                return False

            df_mix_filt_total = df_mix_atual[df_mix_atual[col_u_mix_gen].apply(pertence_selecao)].copy()
            df_mix_filt_total["Cat_Total"] = df_mix_filt_total[col_p_mix_gen].apply(lambda p: categorizar_plano_ampliado(p, mapa_excel_carregado))
            total_alunos = df_mix_filt_total["Cat_Total"].notnull().sum()
        else:
            total_alunos = sum([df_filtrado[df_filtrado[col_unidade_df] == u]["Clientes Recorrentes"].values[0] for u in df_filtrado[col_unidade_df].unique() if "Clientes Recorrentes" in df_filtrado.columns and len(df_filtrado[df_filtrado[col_unidade_df] == u]) > 0])
    else:
        total_alunos = sum([df_filtrado[df_filtrado[col_unidade_df] == u]["Clientes Recorrentes"].values[0] for u in df_filtrado[col_unidade_df].unique() if "Clientes Recorrentes" in df_filtrado.columns and len(df_filtrado[df_filtrado[col_unidade_df] == u]) > 0])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-card-bar' style='background-color: {HEX_NAVY};'></div>
                <div class='kpi-title'>Total de Unidades</div>
                <div class='kpi-value'>{total_unidades}</div>
                <div class='kpi-sub'>Unidades na selecao</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-card-bar' style='background-color: {HEX_BLUE};'></div>
                <div class='kpi-title'>Decisoes Concluidas</div>
                <div class='kpi-value' style='color: {HEX_BLUE};'>{analisadas}</div>
                <div class='kpi-sub'>{pct_concluido:.1f}% do total concluido</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-card-bar' style='background-color: #D97706;'></div>
                <div class='kpi-title'>Unidades Pendentes</div>
                <div class='kpi-value' style='color: #D97706;'>{pendentes}</div>
                <div class='kpi-sub'>Aguardando decisao do comite</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-card-bar' style='background-color: {HEX_BLUE};'></div>
                <div class='kpi-title'>BASE TOTAL DE CLIENTES</div>
                <div class='kpi-value' style='color: {HEX_NAVY};'>{total_alunos:,}</div>
                <div class='kpi-sub'>Clientes em {rotulo_mes_selecionado}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='font-size:1.1rem; color:{HEX_NAVY}; margin-bottom: 10px;'>Acompanhamento de Governanca por Unidade</h3>", unsafe_allow_html=True)

    df_status = df_filtrado.copy()
    df_status["Clientes Recorrentes"] = df_status[col_unidade_df].apply(lambda u: calcular_alunos_mix_unidade_df(df_mix_atual, u) or (df_status[df_status[col_unidade_df] == u]["Clientes Recorrentes"].values[0] if len(df_status[df_status[col_unidade_df] == u]) > 0 else 0))
    df_status["Status Decisao"] = df_status[col_unidade_df].apply(lambda u: "Concluido" if u in decisoes_salvas else "Pendente")
    df_status["Decisao Clientes Atuais"] = df_status[col_unidade_df].apply(lambda u: decisoes_salvas.get(u, {}).get("decisao_atuais", "Pendente"))
    df_status["Decisao Novos Clientes"] = df_status[col_unidade_df].apply(lambda u: decisoes_salvas.get(u, {}).get("decisao_novos", "Pendente"))
    df_status["Tabelas Vigentes apos Reajuste (Governanca)"] = df_status[col_unidade_df].apply(lambda u: ", ".join(decisoes_salvas.get(u, {}).get("tabelas_vigentes", [])))

    cols_exibir = [c for c in [col_unidade_df, "Cidade", "UF", "Tabela Praticada", "Tabelas na Unidade", "Clientes Recorrentes", "Tempo de Operacao (Meses)", "Status Decisao", "Decisao Clientes Atuais", "Decisao Novos Clientes", "Tabelas Vigentes apos Reajuste (Governanca)"] if c in df_status.columns]
    
    st.dataframe(
        df_status[cols_exibir],
        use_container_width=True,
        height=380,
        hide_index=True,
        column_config={
            "Status Decisao": st.column_config.SelectboxColumn(
                "Status Decisao",
                options=["Concluido", "Pendente"],
                required=True,
            ),
            "Clientes Recorrentes": st.column_config.NumberColumn(
                f"Clientes ({rotulo_mes_selecionado})",
                format="%d",
            ),
            "Tempo de Operacao (Meses)": st.column_config.NumberColumn(
                "Tempo Operacao (Meses)",
                format="%d m",
            )
        }
    )

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='font-size:1.15rem; color:{HEX_NAVY}; margin-bottom: 12px;'>Mix de Produtos Consolidado ({rotulo_mes_selecionado})</h3>", unsafe_allow_html=True)

    if df_mix_atual is not None and not df_mix_atual.empty:
        col_u_mix_gen = next((c for c in df_mix_atual.columns if "unid" in str(c).lower()), None)
        col_p_mix_gen = next((c for c in df_mix_atual.columns if "plano" in str(c).lower() or "produto" in str(c).lower()), None)

        if col_u_mix_gen and col_p_mix_gen:
            unidades_permitidas_norm = [normalizar_texto(u) for u in df_filtrado[col_unidade_df].unique()]
            def pertence_selecao(u_mix_val):
                u_mix_norm = normalizar_texto(u_mix_val)
                for u_perm in unidades_permitidas_norm:
                    if u_mix_norm in u_perm or u_perm in u_mix_norm or ("buritis" in u_mix_norm and "buritis" in u_perm) or ("orla" in u_mix_norm and "orla" in u_perm):
                        return True
                return False

            df_mix_filt = df_mix_atual[df_mix_atual[col_u_mix_gen].apply(pertence_selecao)].copy()

            if not df_mix_filt.empty:
                col_m1, col_m2 = st.columns(2)

                with col_m1:
                    with st.container(border=True):
                        st.markdown("""
                            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'>
                                <h4 style='font-size:0.95rem; color:#022D8A; margin:0;'>Mix Padrao (Core 11 Planos Oficial)</h4>
                                <span style='background-color:rgba(5, 60, 216, 0.08); color:#053CD8; font-size:0.72rem; font-weight:700; padding:3px 7px; border-radius:4px;'>Core 11 Planos</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        df_v1 = df_mix_filt.copy()
                        df_v1["Cat_V1"] = df_v1[col_p_mix_gen].apply(lambda p: categorizar_plano_v1(p, mapa_excel_carregado))
                        df_v1_valid = df_v1[df_v1["Cat_V1"].notnull()]

                        if not df_v1_valid.empty:
                            counts_v1 = df_v1_valid["Cat_V1"].value_counts()
                            tot_v1 = counts_v1.sum()
                            pcts_v1 = (counts_v1 / tot_v1 * 100).round(1)

                            for plano_name, pct_val in pcts_v1.items():
                                st.markdown(f"""
                                    <div class="mix-bar-container">
                                        <div class="mix-label"><span>{plano_name}</span><span>{pct_val:.1f}% ({counts_v1[plano_name]:,} alunos)</span></div>
                                        <div class="mix-bar-bg"><div class="mix-bar-fill" style="width: {pct_val}%;"></div></div>
                                    </div>
                                """, unsafe_allow_html=True)
                            st.markdown(f"<p style='font-size:0.83rem; color:{HEX_NAVY}; font-weight:700; margin-top:12px; border-top:1px solid #E2E8F0; padding-top:8px;'>Total Alunos (Mix Padrao): {tot_v1:,}</p>", unsafe_allow_html=True)

                    # EVOLUÇÃO GLOBAL DA BASE ENCAIXADA LOGO ABAIXO DO MIX PADRÃO
                    st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
                    with st.expander("Evolucao Global da Base de Clientes da Rede", expanded=True):
                        dados_rede_hist = []
                        for key_aba_m, df_m_hist in dict_mix_historico.items():
                            lbl_m = formatar_nome_mes(key_aba_m)
                            if df_m_hist is not None and not df_m_hist.empty:
                                col_p_temp = next((c for c in df_m_hist.columns if "plano" in str(c).lower() or "produto" in str(c).lower()), None)
                                if col_p_temp:
                                    df_temp_cat = df_m_hist[col_p_temp].apply(lambda p: categorizar_plano_ampliado(p, mapa_excel_carregado))
                                    tot_rede_m = df_temp_cat.notnull().sum()
                                    ord_m = obter_ordem_mes(lbl_m)
                                    dados_rede_hist.append({"Mes": lbl_m, "Base Total Rede": tot_rede_m, "Ordem": ord_m})

                        if dados_rede_hist:
                            df_rede_cron = pd.DataFrame(dados_rede_hist).sort_values(by="Ordem").reset_index(drop=True)
                            df_rede_cron["Crescimento %"] = df_rede_cron["Base Total Rede"].pct_change() * 100
                            df_rede_cron["Crescimento %"] = df_rede_cron["Crescimento %"].fillna(0.0)

                            df_rede_display = df_rede_cron.sort_values(by="Ordem", ascending=False).reset_index(drop=True)

                            desenhar_grafico_barras_altair(df_rede_cron, "Mes", "Base Total Rede", "numero")
                            
                            st.dataframe(
                                df_rede_display[["Mes", "Base Total Rede", "Crescimento %"]],
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "Base Total Rede": st.column_config.NumberColumn("Base Total", format="%d"),
                                    "Crescimento %": st.column_config.NumberColumn("Crescimento %", format="%+.1f%%")
                                }
                            )

                    # SIMULADOR E EVOLUÇÃO DO TKM ENCAIXADO LOGO ABAIXO DA EVOLUÇÃO DA BASE
                    st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
                    with st.expander("Simulador e Evolucao do TKM PONDERADO por Tabela de Preco", expanded=False):
                        st.markdown("<p style='font-size:0.85rem; color:#475569; margin-bottom:15px;'>Selecione a tabela de preco para calcular o Ticket Medio Ponderado considerando apenas a aderencia das unidades que praticam estritamente a tabela selecionada no mes de referencia.</p>", unsafe_allow_html=True)
                        
                        num_tabela_sim = st.selectbox(
                            "Simular para Tabela:",
                            options=[1, 2, 3, 4, 5],
                            format_func=lambda x: f"Tabela {x}",
                            index=0
                        )

                        if col_tabela_df:
                            unidades_da_tabela = df[df[col_tabela_df].astype(str).str.contains(str(num_tabela_sim), na=False)][col_unidade_df].unique()
                        else:
                            unidades_da_tabela = df[col_unidade_df].unique()

                        unidades_tab_norm = [normalizar_texto(u) for u in unidades_da_tabela]

                        def pertence_tabela_estrita(u_mix_val):
                            u_mix_norm = normalizar_texto(u_mix_val)
                            for u_perm in unidades_tab_norm:
                                if u_mix_norm in u_perm or u_perm in u_mix_norm or ("buritis" in u_mix_norm and "buritis" in u_perm) or ("orla" in u_mix_norm and "orla" in u_perm):
                                    return True
                            return False

                        df_mix_sim = df_mix_atual[df_mix_atual[col_u_mix_gen].apply(pertence_tabela_estrita)].copy() if not df_mix_atual.empty else pd.DataFrame()

                        faturamento_v1 = 0.0
                        tot_v1_sim = 0
                        if not df_mix_sim.empty:
                            df_sim_v1 = df_mix_sim.copy()
                            df_sim_v1["Cat_V1"] = df_sim_v1[col_p_mix_gen].apply(lambda p: categorizar_plano_v1(p, mapa_excel_carregado))
                            df_sim_v1_valid = df_sim_v1[df_sim_v1["Cat_V1"].notnull()]
                            
                            if not df_sim_v1_valid.empty:
                                tot_v1_sim = len(df_sim_v1_valid)
                                for cat_p, q_p in df_sim_v1_valid["Cat_V1"].value_counts().items():
                                    preco_p = tabela_precos_carregada.get(cat_p, {}).get(num_tabela_sim, 0.0)
                                    faturamento_v1 += q_p * preco_p

                        tkm_v1_ponderado = (faturamento_v1 / tot_v1_sim) if tot_v1_sim > 0 else 0.0

                        faturamento_v2 = 0.0
                        tot_v2_sim = 0
                        if not df_mix_sim.empty:
                            df_sim_v2 = df_mix_sim.copy()
                            df_sim_v2["Cat_V2"] = df_sim_v2[col_p_mix_gen].apply(lambda p: categorizar_plano_ampliado(p, mapa_excel_carregado))
                            df_sim_v2_valid = df_sim_v2[df_sim_v2["Cat_V2"].notnull()]
                            
                            if not df_sim_v2_valid.empty:
                                tot_v2_sim = len(df_sim_v2_valid)
                                for cat_p, q_p in df_sim_v2_valid["Cat_V2"].value_counts().items():
                                    preco_p = tabela_precos_carregada.get(cat_p, {}).get(num_tabela_sim, 0.0)
                                    faturamento_v2 += q_p * preco_p

                        tkm_v2_ponderado = (faturamento_v2 / tot_v2_sim) if tot_v2_sim > 0 else 0.0
                        tkm_oficial_rede = TKM_REDE_REFERENCIA.get(num_tabela_sim, 0.0)

                        cs1, cs2, cs3 = st.columns(3)
                        with cs1:
                            st.markdown(f"""
                                <div class='sim-card'>
                                    <span style='font-size:0.72rem; font-weight:700; color:#64748B; text-transform:uppercase;'>TKM (Mix Padrao)</span>
                                    <h3 style='margin:4px 0 0 0; color:{HEX_BLUE} !important; font-size:1.3rem;'>R$ {tkm_v1_ponderado:,.2f}</h3>
                                    <span style='font-size:0.7rem; color:#94A3B8;'>{tot_v1_sim:,} alunos</span>
                                </div>
                            """, unsafe_allow_html=True)
                        with cs2:
                            st.markdown(f"""
                                <div class='sim-card'>
                                    <span style='font-size:0.72rem; font-weight:700; color:#64748B; text-transform:uppercase;'>TKM (Mix Ampliado)</span>
                                    <h3 style='margin:4px 0 0 0; color:{HEX_NAVY} !important; font-size:1.3rem;'>R$ {tkm_v2_ponderado:,.2f}</h3>
                                    <span style='font-size:0.7rem; color:#94A3B8;'>{tot_v2_sim:,} alunos</span>
                                </div>
                            """, unsafe_allow_html=True)
                        with cs3:
                            st.markdown(f"""
                                <div class='sim-card' style='background-color:#F8FAFC;'>
                                    <span style='font-size:0.72rem; font-weight:700; color:#64748B; text-transform:uppercase;'>TKM Rede</span>
                                    <h3 style='margin:4px 0 0 0; color:#334155 !important; font-size:1.3rem;'>R$ {tkm_oficial_rede:,.2f}</h3>
                                    <span style='font-size:0.7rem; color:#94A3B8;'>Tabela {num_tabela_sim}</span>
                                </div>
                            """, unsafe_allow_html=True)

                        # GRÁFICO EM BARRAS DO TKM HISTÓRICO ALTAIR
                        st.markdown("<hr style='margin:12px 0;'>", unsafe_allow_html=True)
                        st.markdown(f"<h4 style='font-size:0.88rem; color:{HEX_NAVY}; margin-bottom:8px;'>Evolucao Historica do TKM - Tabela {num_tabela_sim}</h4>", unsafe_allow_html=True)
                        
                        dados_tkm_hist = []
                        for key_aba_m, df_m_hist in dict_mix_historico.items():
                            lbl_m = formatar_nome_mes(key_aba_m)
                            ord_m = obter_ordem_mes(lbl_m)
                            if df_m_hist is not None and not df_m_hist.empty:
                                col_u_temp = next((c for c in df_m_hist.columns if "unid" in str(c).lower()), None)
                                col_p_temp = next((c for c in df_m_hist.columns if "plano" in str(c).lower() or "produto" in str(c).lower()), None)
                                
                                if col_u_temp and col_p_temp:
                                    df_m_sim = df_m_hist[df_m_hist[col_u_temp].apply(pertence_tabela_estrita)].copy()
                                    df_m_sim["Cat_V2"] = df_m_sim[col_p_temp].apply(lambda p: categorizar_plano_ampliado(p, mapa_excel_carregado))
                                    df_m_sim_val = df_m_sim[df_m_sim["Cat_V2"].notnull()]
                                    
                                    tot_al = len(df_m_sim_val)
                                    if tot_al > 0:
                                        fat_m = sum([q_p * tabela_precos_carregada.get(cat_p, {}).get(num_tabela_sim, 0.0) for cat_p, q_p in df_m_sim_val["Cat_V2"].value_counts().items()])
                                        tkm_calc = fat_m / tot_al
                                        dados_tkm_hist.append({"Mes": lbl_m, "TKM Ponderado": round(tkm_calc, 2), "Base Alunos": tot_al, "Ordem": ord_m})

                        if dados_tkm_hist:
                            df_tkm_cron = pd.DataFrame(dados_tkm_hist).sort_values(by="Ordem").reset_index(drop=True)
                            df_tkm_cron["Crescimento %"] = df_tkm_cron["TKM Ponderado"].pct_change() * 100
                            df_tkm_cron["Crescimento %"] = df_tkm_cron["Crescimento %"].fillna(0.0)

                            df_tkm_display = df_tkm_cron.sort_values(by="Ordem", ascending=False).reset_index(drop=True)

                            desenhar_grafico_barras_altair(df_tkm_cron, "Mes", "TKM Ponderado", "moeda")
                            
                            st.dataframe(
                                df_tkm_display[["Mes", "TKM Ponderado", "Crescimento %"]],
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "TKM Ponderado": st.column_config.NumberColumn("TKM Ponderado", format="R$ %.2f"),
                                    "Crescimento %": st.column_config.NumberColumn("Crescimento %", format="%+.1f%%")
                                }
                            )

                with col_m2:
                    with st.container(border=True):
                        st.markdown("""
                            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;'>
                                <h4 style='font-size:0.95rem; color:#022D8A; margin:0;'>Mix Ampliado (Base Completa Mapeada)</h4>
                                <span style='background-color:rgba(13, 242, 5, 0.12); color:#16A34A; font-size:0.72rem; font-weight:700; padding:3px 7px; border-radius:4px;'>12 Categorias</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        df_v2 = df_mix_filt.copy()
                        df_v2["Cat_V2"] = df_v2[col_p_mix_gen].apply(lambda p: categorizar_plano_ampliado(p, mapa_excel_carregado))
                        df_v2_valid = df_v2[df_v2["Cat_V2"].notnull()]

                        if not df_v2_valid.empty:
                            counts_v2 = df_v2_valid["Cat_V2"].value_counts()
                            tot_v2 = counts_v2.sum()
                            pcts_v2 = (counts_v2 / tot_v2 * 100).round(1)

                            for plano_name, pct_val in pcts_v2.items():
                                st.markdown(f"""
                                    <div class="mix-bar-container">
                                        <div class="mix-label"><span>{plano_name}</span><span>{pct_val:.1f}% ({counts_v2[plano_name]:,} alunos)</span></div>
                                        <div class="mix-bar-bg"><div class="mix-bar-fill" style="width: {pct_val}%;"></div></div>
                                    </div>
                                """, unsafe_allow_html=True)
                            st.markdown(f"<p style='font-size:0.83rem; color:{HEX_NAVY}; font-weight:700; margin-top:12px; border-top:1px solid #E2E8F0; padding-top:8px;'>Total Alunos (Mix Ampliado): {tot_v2:,}</p>", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: ANÁLISE E DECISÃO POR UNIDADE
# ==============================================================================
with tab_analise_decisao:
    opcoes_atuais = ["Sem reajuste", "Ajuste IPCA para tabela vigente", "Aplicar nova tabela (atualizada)", "Migrar toda base para tabela vigente atualmente na unidade"]
    opcoes_novos = ["Sem reajuste", "Ajuste IPCA para tabela vigente", "Aplicar nova tabela (atualizada)"]
    opcoes_tabelas_governanca = [f"Tabela {t} - {v}" for t in range(1, 6) for v in ["Antiga", "IPCA", "Nova"]]

    unidade_sel = st.selectbox("Selecione a Unidade para Analise:", df[col_unidade_df].unique(), index=0)
    row = df[df[col_unidade_df] == unidade_sel].iloc[0]
    decisao_previa = decisoes_salvas.get(unidade_sel, {})
    gr_responsavel, qtd_quadras = obter_dados_unidade(row[col_unidade_df])

    col_main, col_sidebar_estado = st.columns([3.2, 1.1])

    with col_main:
        st.markdown(f"""
            <div class='sticky-unit-header'>
                <div style='display: flex; justify-content: space-between; align-items: center; width: 100%;'>
                    <div><h2 style='font-size: 1.85rem !important; margin: 0; color: {HEX_NAVY}; font-weight: 800;'>{row[col_unidade_df]}</h2><span style='color: #64748B; font-size: 0.95rem; font-weight: 600;'>{row.get('Cidade', 'N/A')} - {row.get('UF', 'N/A')}</span></div>
                    <div style='text-align: right; background-color: rgba(5, 60, 216, 0.06); padding: 6px 12px; border-radius: 6px;'><span style='font-size: 0.8rem; color: {HEX_NAVY}; font-weight: 700;'>GR: {gr_responsavel}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_sidebar_estado:
        uf_atual = row.get("UF", "")
        df_estado = df[df["UF"] == uf_atual] if "UF" in df.columns else df
        
        with st.expander(f"Rede no Estado ({uf_atual}) - {len(df_estado)} unidade(s)", expanded=True):
            for _, u_row in df_estado.iterrows():
                nome_u = u_row[col_unidade_df]
                status_tag = "OK" if nome_u in decisoes_salvas else "..."
                css_class = "state-unit-selected" if nome_u == unidade_sel else "state-unit-default"
                st.markdown(f"<div class='state-unit-item {css_class}'><span style='white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 170px;'>{nome_u.replace('Fast Tennis ', '')}</span><span>{status_tag}</span></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
        
        st.markdown(f"<h4 style='font-size:0.95rem; color:{HEX_NAVY}; margin-bottom: 8px;'>Mix de Produtos da Unidade</h4>", unsafe_allow_html=True)
        rotulo_mes_unit_sel = st.selectbox("Mes de Referencia:", opcoes_rotulos_mes, key="sel_mes_mix_unidade", index=max(0, idx_default_mes))
        chave_real_unit_mes = dict_meses_rotulados[rotulo_mes_unit_sel]
        df_mix_u_ref = dict_mix_historico.get(chave_real_unit_mes, pd.DataFrame())

        df_mix_u_valid = pd.DataFrame()
        if df_mix_u_ref is not None and not df_mix_u_ref.empty:
            col_u_mix = next((c for c in df_mix_u_ref.columns if "unid" in str(c).lower()), None)
            col_p_mix = next((c for c in df_mix_u_ref.columns if "plano" in str(c).lower() or "produto" in str(c).lower()), None)

            if col_u_mix and col_p_mix:
                u_main_norm = normalizar_texto(unidade_sel)
                def pertence_unidade_sidebar(u_mix_val):
                    u_mix_norm = normalizar_texto(u_mix_val)
                    return u_mix_norm in u_main_norm or u_main_norm in u_mix_norm or ("buritis" in u_mix_norm and "buritis" in u_main_norm) or ("orla" in u_mix_norm and "orla" in u_main_norm)

                df_mix_u = df_mix_u_ref[df_mix_u_ref[col_u_mix].apply(pertence_unidade_sidebar)].copy()
                if not df_mix_u.empty:
                    df_mix_u["Plano_Cat"] = df_mix_u[col_p_mix].apply(lambda p: categorizar_plano_ampliado(p, mapa_excel_carregado))
                    df_mix_u_valid = df_mix_u[df_mix_u["Plano_Cat"].notnull()]
                    if not df_mix_u_valid.empty:
                        counts = df_mix_u_valid["Plano_Cat"].value_counts()
                        pcts = (counts / counts.sum() * 100).round(1)
                        for plano, pct in pcts.items():
                            st.markdown(f"<div class='mix-bar-container'><div class='mix-label'><span>{plano}</span><span>{pct:.1f}%</span></div><div class='mix-bar-bg'><div class='mix-bar-fill' style='width: {pct}%;'></div></div></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 0.6rem;'></div>", unsafe_allow_html=True)

        raw_tabela_u = str(row.get("Tabela Praticada", "1"))
        digits_u = re.findall(r"\d+", raw_tabela_u)
        num_tabela_u_default = int(digits_u[0]) if digits_u else 1

        # SIMULADOR DE TKM DA UNIDADE
        with st.expander("Simulador de Impacto de Reajuste (TKM Unidade)", expanded=False):
            opcoes_simulacao_u = [f"Tabela {t}" for t in range(1, 6)] + [f"Tabela {t} + IPCA (+{PERCENTUAL_IPCA*100:.2f}%)" for t in range(1, 6)]
            
            idx_sim_default = max(0, min(4, num_tabela_u_default - 1))
            
            tabela_sim_str = st.selectbox(
                "Selecione a Tabela / Reajuste:",
                options=opcoes_simulacao_u,
                index=idx_sim_default + 5,
                key="sel_tab_unidade_sim"
            )

            digits_sim = re.findall(r"\d+", tabela_sim_str)
            num_tabela_sim_u = int(digits_sim[0]) if digits_sim else 1
            tem_ipca = "IPCA" in tabela_sim_str

            tkm_simulado_bruto = 0.0
            tot_alunos_u = len(df_mix_u_valid) if not df_mix_u_valid.empty else 0

            if tot_alunos_u > 0:
                fat_u_sim = 0.0
                for cat_p, q_p in df_mix_u_valid["Plano_Cat"].value_counts().items():
                    preco_base = tabela_precos_carregada.get(cat_p, {}).get(num_tabela_sim_u, 0.0)
                    if tem_ipca:
                        preco_p = preco_base * (1 + PERCENTUAL_IPCA)
                    else:
                        preco_p = preco_base
                    fat_u_sim += q_p * preco_p
                tkm_simulado_bruto = fat_u_sim / tot_alunos_u

            tkm_simulado_liquido = tkm_simulado_bruto * (1 - DESCONTO_MEDIO_REDE)

            st.markdown(f"""
                <div class='sim-card-inline'>
                    <span style='font-size:0.7rem; font-weight:700; color:#64748B; text-transform:uppercase;'>TKM LIQUIDO PROJETADO ({rotulo_mes_unit_sel.upper()})</span>
                    <h3 style='margin:4px 0 2px 0; color:{HEX_BLUE} !important; font-size:1.6rem; font-weight:800;'>R$ {tkm_simulado_liquido:,.2f}</h3>
                    <span style='font-size:0.68rem; color:#94A3B8; display:block; margin-top:4px;'>Simulação na {tabela_sim_str} ({tot_alunos_u:,} alunos) | Dedução preventiva de {DESCONTO_MEDIO_REDE*100:.2f}% (desconto médio)</span>
                </div>
            """, unsafe_allow_html=True)

        # EVOLUÇÃO DA BASE DA UNIDADE (COM GRÁFICO ALTAIR PADRONIZADO)
        st.markdown("<div style='margin-top: 0.6rem;'></div>", unsafe_allow_html=True)
        with st.expander("Evolucao da Base da Unidade", expanded=True):
            hist_evolucao_u = []
            for nome_aba_hist, df_hist in dict_mix_historico.items():
                qtd_hist = calcular_alunos_mix_unidade_df(df_hist, unidade_sel) or 0
                label_mes = formatar_nome_mes(nome_aba_hist)
                ord_mes = obter_ordem_mes(label_mes)
                hist_evolucao_u.append({"Mes": label_mes, "Alunos": qtd_hist, "Ordem": ord_mes})

            if hist_evolucao_u:
                df_hist_cron = pd.DataFrame(hist_evolucao_u).sort_values(by="Ordem").reset_index(drop=True)
                desenhar_grafico_barras_altair(df_hist_cron, "Mes", "Alunos", "numero")

    with col_main:
        col_top1, col_top2 = st.columns(2)
        with col_top1:
            st.markdown(f"<div class='executive-card-half'><div><div class='executive-card-title'>Localizacao & Operacao</div><p style='margin: 3px 0; font-size: 0.88rem;'><strong>Endereco:</strong> {row.get('Endereço', row.get('Endereco', 'N/A'))}</p><p style='margin: 3px 0; font-size: 0.88rem;'><strong>Inicio Operacao:</strong> {formatar_data_br(row.get('Início da Operação', row.get('Inicio da Operacao')))}</p><p style='margin: 3px 0; font-size: 0.88rem;'><strong>Gerente de Resultados (GR):</strong> {gr_responsavel}</p><p style='margin: 3px 0; font-size: 0.88rem;'><strong>Quantidade de Quadras:</strong> {qtd_quadras}</p></div><p style='margin: 0; font-size: 0.98rem; font-weight: 800; color: {HEX_BLUE};'>Maturidade: {row.get('Tempo de Operação (Meses)', row.get('Tempo de Operacao (Meses)', 0))} meses</p></div>", unsafe_allow_html=True)

        with col_top2:
            val_fat_raw, val_ll_raw = None, None
            if df_fat is not None and not df_fat.empty:
                col_u_fat = next((c for c in df_fat.columns if "unid" in str(c).lower()), None)
                if col_u_fat:
                    u_main_norm = normalizar_texto(unidade_sel)
                    row_fat = df_fat[df_fat[col_u_fat].apply(lambda u: normalizar_texto(u) in u_main_norm or u_main_norm in normalizar_texto(u))]
                    if not row_fat.empty:
                        col_fat_num = next((c for c in df_fat.columns if "faturamento" in str(c).lower()), None)
                        col_ll_num = next((c for c in df_fat.columns if "ll" in str(c).lower()), None)
                        if col_fat_num: val_fat_raw = row_fat.iloc[0].get(col_fat_num)
                        if col_ll_num: val_ll_raw = row_fat.iloc[0].get(col_ll_num)

            pct_fat_str, cor_fat = formatar_kpi_cor(val_fat_raw)
            pct_ll_str, cor_ll = formatar_kpi_cor(val_ll_raw)
            clientes_rec_final = calcular_alunos_mix_unidade_df(df_mix_atual, unidade_sel) or row.get("Clientes Recorrentes", "N/A")
            pct_nao_fech_str, cor_nao_fech = formatar_nao_fechamento_cor(row.get("% de não fechamento por preço (Pós PE)", row.get("% Não Fechamento", None)))

            st.markdown(f"<div class='executive-card-half'><div><div class='executive-card-title'>Metricas Comerciais & Entorno</div><p style='margin: 3px 0; font-size: 0.88rem; color:#475569;'>Clientes Recorrentes: <span style='color:{HEX_NAVY}; font-size: 1.15rem; font-weight:800;'>{clientes_rec_final}</span></p><p style='margin: 3px 0; font-size: 0.88rem;'><strong>% Atingimento Faturamento:</strong> <span style='color:{cor_fat}; font-weight:800;'>{pct_fat_str}</span> | <strong>% Atingimento LL:</strong> <span style='color:{cor_ll}; font-weight:800;'>{pct_ll_str}</span></p><p style='margin: 3px 0; font-size: 0.88rem;'><strong>% de nao fechamento por preco:</strong> <span style='color:{cor_nao_fech}; font-weight:800;'>{pct_nao_fech_str}</span></p></div><p style='margin: 0; font-size: 0.82rem; color:#64748B;'>Unidade Proxima: {row.get('Unidade Próxima', row.get('Unidade Proxima', '-'))} ({row.get('Distância', row.get('Distancia', '-'))})</p></div>", unsafe_allow_html=True)

        raw_tabela_praticada = str(row.get("Tabela Praticada", "N/A"))
        tabela_limpa = raw_tabela_praticada.replace("Tabela", "Tabela ").replace("  ", " ")
        tkm_val = row.get("TKM (último mês)", row.get("TKM (ultimo mes)", 0))
        tkm_str = f"R$ {tkm_val:,.2f}" if isinstance(tkm_val, (int, float)) else str(tkm_val)
        obs_excel_txt = obter_observacao_excel(row)

        if obs_excel_txt:
            st.markdown(f"""
                <div class='table-highlight-card-full'>
                    <div class='executive-card-title' style='margin-bottom:2px; color:{HEX_BLUE};'>TABELA PRATICADA ATUALMENTE</div>
                    <h2 style='margin: 0; color:{HEX_NAVY} !important; font-size: 2.1rem;'>{tabela_limpa}</h2>
                    <div style='display: flex; justify-content: space-between; align-items: flex-end; margin-top: 8px;'>
                        <div>
                            <p style='margin: 0 0 2px 0; font-size: 0.88rem; color:#475569;'><strong>Tabelas na Unidade:</strong> {row.get('Tabelas na Unidade', tabela_limpa)}</p>
                            <p style='margin: 0; font-size: 0.88rem; color:#334155;'><strong>TKM (Ultimo Mes):</strong> <span style='font-weight:700; color:{HEX_NAVY};'>{tkm_str}</span> <span style='font-size:0.78rem; color:{HEX_BLUE}; font-weight:600;'>{obter_comparacao_tkm(raw_tabela_praticada, tkm_val)}</span></p>
                        </div>
                        <div style='max-width: 48%; text-align: right;'>
                            <span style='font-size: 0.88rem; color: #475569; font-weight: 600;'>{sanitizar_recomendacao(obs_excel_txt)}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='table-highlight-card-full'>
                    <div class='executive-card-title' style='margin-bottom:2px; color:{HEX_BLUE};'>TABELA PRATICADA ATUALMENTE</div>
                    <h2 style='margin: 0; color:{HEX_NAVY} !important; font-size: 2.1rem;'>{tabela_limpa}</h2>
                    <p style='margin: 4px 0 2px 0; font-size: 0.88rem; color:#475569;'><strong>Tabelas na Unidade:</strong> {row.get('Tabelas na Unidade', tabela_limpa)}</p>
                    <p style='margin: 2px 0 0 0; font-size: 0.88rem; color:#334155;'><strong>TKM (Ultimo Mes):</strong> <span style='font-weight:700; color:{HEX_NAVY};'>{tkm_str}</span> <span style='font-size:0.78rem; color:{HEX_BLUE}; font-weight:600;'>{obter_comparacao_tkm(raw_tabela_praticada, tkm_val)}</span></p>
                </div>
            """, unsafe_allow_html=True)

        # QUADRANTE DE DECISÃO RETRÁTIL
        with st.expander("Registrar Decisao do Comite Executivo", expanded=True):
            with st.form("form_registro_comite"):
                col_f1, col_f2 = st.columns(2)
                with col_f1: decisao_atuais = st.selectbox("Decisao - Clientes Atuais:", options=opcoes_atuais)
                with col_f2: decisao_novos = st.selectbox("Decisao - Novos Clientes:", options=opcoes_novos)
                tabelas_vigentes_selecionadas = st.multiselect("Tabelas vigentes apos reajuste:", options=opcoes_tabelas_governanca)
                observacoes_comite = st.text_area("Observacoes / Justificativa:", height=90)

                col_b1, col_b2 = st.columns([1, 1])
                with col_b1: btn_salvar = st.form_submit_button("Salvar Decisao no GitHub")
                with col_b2: btn_limpar = st.form_submit_button("Resetar Decisao")

                if btn_salvar:
                    decisoes_salvas[unidade_sel] = {"decisao_atuais": decisao_atuais, "decisao_novos": decisao_novos, "tabelas_vigentes": tabelas_vigentes_selecionadas, "observacoes_comite": observacoes_comite, "data_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    if salvar_decisoes_github(decisoes_salvas):
                        st.success("Salvo com sucesso!")
                        st.rerun()

                if btn_limpar and unidade_sel in decisoes_salvas:
                    del decisoes_salvas[unidade_sel]
                    if salvar_decisoes_github(decisoes_salvas):
                        st.rerun()
