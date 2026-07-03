import streamlit as st
import pandas as pd
import numpy as np
import requests

# Configuração da página e layout focado em dados e clareza
st.set_page_config(page_title="Fast Tennis - Login Seguro", layout="wide")

# ==========================================
# CONTROLE DE AMBIENTE SEGURO (AUTENTICAÇÃO)
# ==========================================

# Dicionário de e-mails e senhas oficiais
USUARIOS_PERMITIDOS = {
    "rayane@fasttennis.com.br": "Simulador8734"
}

# Inicializa o estado de login caso não exista na sessão
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# Função para processar a verificação de credenciais
def realizar_login():
    email_input = st.session_state["login_email"].strip()
    senha_input = st.session_state["login_senha"]
    
    if email_input in USUARIOS_PERMITIDOS and USUARIOS_PERMITIDOS[email_input] == senha_input:
        st.session_state["autenticado"] = True
        st.session_state["usuario_logado"] = email_input
        st.rerun()
    else:
        st.error("Credenciais inválidas ou usuário não autorizado no comitê.")

# SE NÃO ESTIVER AUTENTICADO: Exibe exclusivamente a tela de login bloqueando a ferramenta
if not st.session_state["autenticado"]:
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color:#F8F9FA; padding:30px; border-radius:8px; border-top:5px solid #0D47A1; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <h3 style="color:#1E2229; margin-top:0; margin-bottom:5px;">Acesso Restrito Fast Tennis</h3>
                <p style="color:#6C757D; font-size:13px; margin-bottom:25px;">Insira suas credenciais corporativas autorizadas para acessar o simulador.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.text_input("E-mail Corporativo:", key="login_email")
        st.text_input("Senha de Acesso:", type="password", key="login_senha")
        st.button("Validar Credenciais e Entrar", on_click=realizar_login, use_container_width=True)
        
    st.stop()

# ==========================================
# AMBIENTE AUTENTICADO - CARREGAMENTO DO SISTEMA
# ==========================================

st.markdown("""
    <style>
        .faixa-resultados {
            background-color: #E3F2FD;
            color: #0D47A1;
            padding: 18px 20px;
            margin: 40px -4rem 20px -4rem; 
            font-size: 25px; 
            font-weight: 700;
            letter-spacing: 0.5px;
            border-left: 6px solid #1E88E5;
            display: flex;
            align-items: center;
        }
        .tabela-sugerida-box {
            background-color: #F8F9FA;
            padding: 18px;
            border-radius: 6px;
            border-left: 5px solid #A3D133;
            margin-bottom: 25px;
        }
        .tabela-sugerida-box h2 {
            margin: 0;
            color: #1E2229 !important;
            font-size: 28px;
            font-weight: 700;
        }
        .tabela-sugerida-box p {
            margin: 6px 0 0 0;
            font-size: 15px;
            color: #495057;
        }
        .espacador-bloco {
            margin-top: 30px;
        }
        .nota-rodape {
            background-color: #FFF8E1;
            border-left: 5px solid #FFB300;
            padding: 15px;
            border-radius: 4px;
            font-size: 13.5px;
            color: #5D4037;
            margin-top: 50px;
        }
    </style>
""", unsafe_allow_html=True)

col_header1, col_header2 = st.columns([3, 1])
with col_header2:
    st.markdown(f"<p style='text-align:right; font-size:12px; color:#6C757D; margin-bottom:2px;'>Sessão: <b>{st.session_state['usuario_logado']}</b></p>", unsafe_allow_html=True)
    if st.button("Efetuar Logout", use_container_width=True):
        st.session_state["autenticado"] = False
        st.rerun()

with col_header1:
    st.title("Simulador Estratégico de Precificação")
st.markdown("---")

# ==========================================
# SEÇÃO 1: DADOS DA ÁREA DE ESTUDO
# ==========================================
st.subheader("📊 1. Dados da Área de Estudo")
st.markdown("<p style='font-size:14px; color:#5A6578; margin-bottom:15px;'>Os dados imputados abaixo devem ser retirados da área de estudo delimitada no Geofusion de acordo com as diretrizes de praça.</p>", unsafe_allow_html=True)

with st.expander("📌 Diretrizes de Delimitação da Área de Estudo (Clique para expandir/recolher)"):
    st.markdown("""
    ### Passo 1: Delimitação Inicial
    * Estabeleça, a partir do endereço do ponto comercial, um **raio inicial por deslocamento de 2 km**. Colete os dados desse raio no Geofusion e prossiga para o Passo 2.
    
    ### Passo 2: Classificação da Região (Perfil da Praça)
    Avalie as respostas abaixo de forma sequencial para determinar a vocação da região:
    1. **Residencial:** A população do raio (2 km) é $\geq$ 60 mil habitantes **e** o público-alvo (A++, A+ e B1) é de no mínimo 15 mil habitantes? Se **SIM**, classifique como **Residencial**.
    2. **Comercial (Polo):** O PEA Dia é superior em mais de 40% à população residente da área? Se **SIM**, classifique como **Comercial**.
    3. **Residencial:** A população residente é superior em mais de 40% ao PEA Dia da área? Se **SIM**, classifique como **Residencial**.
    4. **Análise de Renda (Mista):** A diferença entre PEA Dia e População está na faixa de $\pm$40%? 
        * Renda Média Domiciliar **> R$ 16.500**: Classifique como **Mista Qualificada**.
        * Renda Média Domiciliar **$\leq$ R$ 16.500**: Classifique como **Mista**.
    
    ### Passo 3: Definição do Raio Final de Estudo
    Utilize o perfil definido no passo anterior para ajustar a abrangência final da coleta de dados:
    * **Comercial (Polo) – Cidade de São Paulo:** Utilizar raio por deslocamento de **Até 20 minutos**.
    * **Comercial (Polo) – Demais Localidades:** Utilizar raio por deslocamento de **Até 15 minutos**.
    * **Perfis Residencial / Mista / Mista Qualificada:**
        * Se a área de estudo tiver no mínimo 30.000 habitantes: **Manter raio de 2 km**.
        * Se tiver menos de 30.000 habitantes na região de **Média ou Alta densidade**: **Expandir para até 3 km**.
        * Se tiver menos de 30.000 habitantes na região de **Baixa densidade**: Utilizar raio por deslocamento de **Até 15 minutos**.
    
    *Nota de Densidade Demográfica:* **Baixa:** < 3.000 hab/km² | **Média:** 3.000 a 7.000 hab/km² | **Alta:** > 7.000 hab/km².
    """)

st.markdown("<br>", unsafe_allow_html=True)

@st.cache_data(ttl=86400)
def buscar_cidades_ibge(uf):
    # Dicionário interno para garantir que as siglas corretas busquem os dados certos no IBGE
    mapa_uf_correto = {
        "AMAZONAS": "AM",
        "GOIÁS": "GO",
        "MATO GROSSO DO SUL": "MS",
        "PARANÁ": "PR",
        "RIO GRANDE DO NORTE": "RN",
        "TOCANTINS": "TO"
    }
    uf_busca = mapa_uf_correto.get(uf, uf)
    try:
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf_busca}/municipios"
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            lista_cidades = [c["nome"] for c in resposta.json()]
            return sorted(lista_cidades)
    except:
        pass
    return ["São Paulo", "Belo Horizonte", "Rio de Janeiro", "Curitiba"]

# LISTA EXIBIDA CORRIGIDA EXATAMENTE COMO VOCÊ PEDIU:
estados_br = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

dados_unidades_existentes = [
    {"Unidade": "Fast Tennis Alphaville", "Estado": "SP", "Renda Média": 27400, "População": 44300, "% Classe A+": 0.54, "Praça": "Comercial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Alto da Boa Vista", "Estado": "SP", "Renda Média": 23654, "População": 85519, "% Classe A+": 0.55, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Alto de Pinheiros", "Estado": "SP", "Renda Média": 23900, "População": 82500, "% Classe A+": 0.46, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Alto do Ipiranga", "Estado": "SP", "Renda Média": 19775, "População": 177000, "% Classe A+": 0.37, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Anhanguera - Jundiaí", "Estado": "SP", "Renda Média": 11650, "População": 67900, "% Classe A+": 0.16, "Praça": "Residencial", "REGIC": "Capital Regional C"},
    {"Unidade": "Fast Tennis Bebedouro", "Estado": "SP", "Renda Média": 5900, "População": 44900, "% Classe A+": 0.04, "Praça": "Residencial", "REGIC": "Centro Sub-Regional"},
    {"Unidade": "Fast Tennis Botafogo - Campinas", "Estado": "SP", "Renda Média": 12300, "População": 96574, "% Classe A+": 0.20, "Praça": "Residencial", "REGIC": "Capital Regional B"},
    {"Unidade": "Fast Tennis Brooklin", "Estado": "SP", "Renda Média": 29400, "População": 162400, "% Classe A+": 0.58, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Campo Belo", "Estado": "SP", "Renda Média": 27328, "População": 117500, "% Classe A+": 0.53, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Cantareira", "Estado": "SP", "Renda Média": 11500, "População": 95500, "% Classe A+": 0.18, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Centro São Bernardo", "Estado": "SP", "Renda Média": 10800, "População": 164300, "% Classe A+": 0.15, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Chácara Inglesa", "Estado": "SP", "Renda Média": 21400, "População": 178712, "% Classe A+": 0.41, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Chácara Santo Antônio", "Estado": "SP", "Renda Média": 25795, "População": 78250, "% Classe A+": 0.50, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Indaiatuba", "Estado": "SP", "Renda Média": 11187, "População": 53898, "% Classe A+": 0.16, "Praça": "Mista", "REGIC": "Centro Sub-Regional"},
    {"Unidade": "Fast Tennis Jardim", "Estado": "SP", "Renda Média": 14195, "População": 128600, "% Classe A+": 0.22, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Jardim Portal da Colina", "Estado": "SP", "Renda Média": 11900, "População": 52624, "% Classe A+": 0.17, "Praça": "Mista", "REGIC": "Capital Regional B"},
    {"Unidade": "Fast Tennis Lapa", "Estado": "SP", "Renda Média": 14200, "População": 107250, "% Classe A+": 0.24, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Moema", "Estado": "SP", "Renda Média": 28900, "População": 143796, "% Classe A+": 0.56, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Monte Pascal", "Estado": "SP", "Renda Média": 21446, "População": 90476, "% Classe A+": 0.41, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Mooca", "Estado": "SP", "Renda Média": 13400, "População": 147000, "% Classe A+": 0.22, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Morumbi", "Estado": "SP", "Renda Média": 14200, "População": 165700, "% Classe A+": 0.25, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Nova Aliança Sul - Ribeirão", "Estado": "SP", "Renda Média": 12900, "População": 90800, "% Classe A+": 0.20, "Praça": "Mista", "REGIC": "Capital Regional A"},
    {"Unidade": "Fast Tennis Parque Piqueri", "Estado": "SP", "Renda Média": 12800, "População": 138700, "% Classe A+": 0.21, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Praia Grande", "Estado": "SP", "Renda Média": 8900, "População": 84400, "% Classe A+": 0.09, "Praça": "Residencial", "REGIC": "Capital Regional B"},
    {"Unidade": "Fast Tennis Radial Leste", "Estado": "SP", "Renda Média": 15700, "População": 146400, "% Classe A+": 0.27, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Rio Claro", "Estado": "SP", "Renda Média": 7400, "População": 72800, "% Classe A+": 0.08, "Praça": "Residencial", "REGIC": "Centro Sub-Regional"},
    {"Unidade": "Fast Tennis Salto", "Estado": "SP", "Renda Média": 6560, "População": 54900, "% Classe A+": 0.05, "Praça": "Residencial", "REGIC": "Centro Sub-Regional"},
    {"Unidade": "Fast Tennis Santana", "Estado": "SP", "Renda Média": 17700, "População": 153100, "% Classe A+": 0.31, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Santo Amaro", "Estado": "SP", "Renda Média": 21100, "População": 82400, "% Classe A+": 0.40, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis São Caetano", "Estado": "SP", "Renda Média": 10200, "População": 122900, "% Classe A+": 0.13, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Saúde", "Estado": "SP", "Renda Média": 17700, "População": 186000, "% Classe A+": 0.32, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Taquaral", "Estado": "SP", "Renda Média": 12738, "População": 40203, "% Classe A+": 0.22, "Praça": "Residencial", "REGIC": "Capital Regional A"},
    {"Unidade": "Fast Tennis Três Poderes", "Estado": "SP", "Renda Média": 18100, "População": 587000, "% Classe A+": 0.32, "Praça": "Comercial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Verbo Divino", "Estado": "SP", "Renda Média": 24800, "População": 77600, "% Classe A+": 0.48, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    {"Unidade": "Fast Tennis Vila Olímpia", "Estado": "SP", "Renda Média": 30900, "População": 160900, "% Classe A+": 0.60, "Praça": "Residencial", "REGIC": "Grande Metrópole"},
    
    # --- UNIDADES OUTROS ESTADOS ---
    {"Unidade": "Fast Tennis Águas Claras", "Estado": "DF", "Renda Média": 20740, "População": 80388, "% Classe A+": 0.43, "Praça": "Residencial", "REGIC": "Metrópole Nacional"},
    {"Unidade": "Fast Tennis Belvedere", "Estado": "MG", "Renda Média": 23100, "População": 63400, "% Classe A+": 0.49, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Boa Viagem", "Estado": "PE", "Renda Média": 12214, "População": 102900, "% Classe A+": 0.23, "Praça": "Mista", "REGIC": "Capital Regional A"},
    {"Unidade": "Fast Tennis Buritis I", "Estado": "MG", "Renda Média": 16700, "População": 80900, "% Classe A+": 0.34, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Calafate", "Estado": "MG", "Renda Média": 13100, "População": 121200, "% Classe A+": 0.25, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Capim Macio", "Estado": "RN", "Renda Média": 14700, "População": 64400, "% Classe A+": 0.32, "Praça": "Mista", "REGIC": "Capital Regional A"},
    {"Unidade": "Fast Tennis Castelo", "Estado": "MG", "Renda Média": 10500, "População": 111575, "% Classe A+": 0.17, "Praça": "Mista", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Cidade Nova", "Estado": "MG", "Renda Média": 10969, "População": 123470, "% Classe A+": 0.18, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Contagem", "Estado": "MG", "Renda Média": 7860, "População": 73600, "% Classe A+": 0.10, "Praça": "Mista", "REGIC": "Capital Regional B"},
    {"Unidade": "Fast Tennis Estoril", "Estado": "MG", "Renda Média": 12612, "População": 85000, "% Classe A+": 0.23, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Estrela sul", "Estado": "MG", "Renda Média": 10480, "População": 113000, "% Classe A+": 0.15, "Praça": "Residencial", "REGIC": "Capital Regional B"},
    {"Unidade": "Fast Tennis Guararapes", "Estado": "CE", "Renda Média": 12450, "População": 54706, "% Classe A+": 0.25, "Praça": "Mista", "REGIC": "Capital Regional A"},
    {"Unidade": "Fast Tennis Morada da Colina", "Estado": "MG", "Renda Média": 14528, "População": 54900, "% Classe A+": 0.25, "Praça": "Mista", "REGIC": "Capital Regional B"},
    {"Unidade": "Fast Tennis Orla da Pampulha", "Estado": "MG", "Renda Média": 9940, "População": 42149, "% Classe A+": 0.16, "Praça": "Mista", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Pampulha", "Estado": "MG", "Renda Média": 11675, "População": 75076, "% Classe A+": 0.20, "Praça": "Mista", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Ponte JK", "Estado": "DF", "Renda Média": 25400, "População": 95617, "% Classe A+": 0.54, "Praça": "Comercial", "REGIC": "Metrópole Nacional"},
    {"Unidade": "Fast Tennis Praia do Canto", "Estado": "ES", "Renda Média": 16840, "População": 83239, "% Classe A+": 0.32, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Recreio", "Estado": "RJ", "Renda Média": 22000, "População": 74360, "% Classe A+": 0.42, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Salgado Filho", "Estado": "PR", "Renda Média": 8900, "População": 64000, "% Classe A+": 0.12, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Santa Lúcia", "Estado": "MG", "Renda Média": 19400, "População": 88597, "% Classe A+": 0.41, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Santa Rosa", "Estado": "RJ", "Renda Média": 17400, "População": 178510, "% Classe A+": 0.33, "Praça": "Mista", "REGIC": "Capital Regional A"},
    {"Unidade": "Fast Tennis São Bento", "Estado": "MG", "Renda Média": 16700, "População": 127317, "% Classe A+": 0.33, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Saul Macedo", "Estado": "MG", "Renda Média": 23100, "População": 63400, "% Classe A+": 0.49, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Sete Lagoas", "Estado": "MG", "Renda Média": 12514, "População": 50780, "% Classe A+": 0.23, "Praça": "Mista", "REGIC": "Capital Regional C"},
    {"Unidade": "Fast Tennis Setor Bueno", "Estado": "GO", "Renda Média": 17800, "População": 94500, "% Classe A+": 0.37, "Praça": "Residencial", "REGIC": "Metrópole"},
    {"Unidade": "Fast Tennis Tirol", "Estado": "RN", "Renda Média": 15400, "População": 72800, "% Classe A+": 0.33, "Praça": "Residencial", "REGIC": "Centro Sub-Regional"},
    {"Unidade": "Fast Tennis Vilhena", "Estado": "RO", "Renda Média": 6100, "População": 42800, "% Classe A+": 0.06, "Praça": "Residencial", "REGIC": "Centro Sub-Regional"}
]
df_unidades = pd.DataFrame(dados_unidades_existentes)

# Inputs de Dados
col_in1, col_in2, col_in3 = st.columns(3)
with col_in1:
    estado = st.selectbox("Estado (UF):", estados_br, index=24)
    cidades_disponiveis = buscar_cidades_ibge(estado)
    cidade = st.selectbox("Cidade:", cidades_disponiveis)
    populacao = st.number_input("População Total da Área:", min_value=0, value=85000, step=1000)

with col_in2:
    regic = st.selectbox("Classificação REGIC:", ["Centro Sub-Regional", "Capital Regional C", "Capital Regional B", "Capital Regional A", "Metrópole", "Grande Metrópole", "Metrópole Nacional"], index=5)
    residentes_alvo = st.number_input("Residentes (Público-Alvo B1, A+ e A++):", min_value=0, value=16500, step=500)
    classe_a_mais_input = st.number_input("% Classe A+ (ex: 0.35 para 35%):", min_value=0.0, max_value=1.0, value=0.35, step=0.01)

with col_in3:
    tipo_praca = st.selectbox("Tipo de Praça (Perfil):", ["Comercial", "Mista", "Residencial", "Mista Qualificada"], index=2)
    renda_media = st.number_input("Renda Média (R$):", min_value=0.0, value=19700.0, step=500.0)

st.markdown("---")

# ==========================================
# SEÇÃO 2: DADOS DE MERCADO
# ==========================================
st.subheader("📊 2. Dados de Mercado")
col_merc1, col_merc2 = st.columns([1, 2])
with col_merc1:
    media_mercado = st.number_input("Preço Médio dos Concorrentes (Plano Plus 1x):", min_value=0.0, value=405.0, step=10.0)

# Processamento lógico
score_praca = {"Comercial": -1, "Mista": 0, "Residencial": 1, "Mista Qualificada": 1}.get(tipo_praca, 0)
score_populacao = -1 if populacao < 40000 else (1 if residentes_alvo >= 15000 else 0)
score_regic = {"Centro Sub-Regional": -1, "Capital Regional B": -1, "Capital Regional C": -1, "Capital Regional A": 0, "Metrópole": 0, "Grande Metrópole": 1, "Metrópole Nacional": 1}.get(regic, 0)
score_total = score_praca + score_populacao + score_regic

if estado == "SP":
    if renda_media <= 8500: tab_min, tab_max = 1, 2
    elif renda_media <= 15000: tab_min, tab_max = 2, 3
    elif renda_media <= 19500: tab_min, tab_max = 3, 4
    else: tab_min, tab_max = 4, 5
else:
    if renda_media <= 8500: tab_min, tab_max = 1, 2
    elif renda_media <= 15000: tab_min, tab_max = 2, 3
    elif renda_media <= 29500: tab_min, tab_max = 3, 4
    else: tab_min, tab_max = 4, 5

# Mapeamento da classificação e tabela recomendada
if score_total <= -1:
    classificacao = "Inferior"
    tabela_sugerida = tab_min
elif score_total in [0, 1]:
    classificacao = "Intermediário"
    tabela_sugerida = int(np.median([tab_min, tab_max]))
else:
    classificacao = "Superior"
    tabela_sugerida = tab_max

precos_plano_plus = {1: 329, 2: 399, 3: 499, 4: 599, 5: 710}
tabelas_tkm = {1: 338, 2: 411, 3: 470, 4: 580, 5: 690}

preco_fast_automatico = precos_plano_plus.get(tabela_sugerida, 499)
tabela_tkm_sugerido = tabelas_tkm.get(tabela_sugerida, 338)
diferenca_fast_mercado = (preco_fast_automatico - media_mercado) / media_mercado if media_mercado > 0 else 0

if diferenca_fast_mercado < -0.10:
    alerta_mercado, diagnostico, recomendacao = "Atenção: Preço Abaixo do Mercado", "Abaixo da Média Regional", "O valor sugerido está muito abaixo do praticado localmente. Avaliar se há margem para aproveitamento ou reposicionamento estratégico."
elif diferenca_fast_mercado <= 0.20:
    alerta_mercado, diagnostico, recomendacao = "Preço Aderente", "Compatível com o Cenário Regional", "Manter a tabela sugerida. O posicionamento de preço demonstra-se totalmente adequado ao contexto de mercado analisado."
else:
    alerta_mercado, diagnostico, recomendacao = "Atenção: Descolamento de Preço", "Muito Acima da Concorrência Local", "Atenção: O valor proposto apresenta uma diferença superior demais à concorrência regional. É mandatória a revisão do cenário em Comitê de Expansão."

# ==========================================
# PAINEL DE RESULTADOS DA SIMULAÇÃO
# ==========================================
st.markdown('<div class="faixa-resultados">📊 Análise de dados e recomendações</div>', unsafe_allow_html=True)
st.markdown("<p style='font-size:14px; color:#5A6578; margin-bottom:20px;'>Diretrizes e recomendações considerando os dados da área de estudo imputados.</p>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="tabela-sugerida-box">
        <p style="margin:0; font-size:11px; color:#6C757D; font-weight:bold; text-transform:uppercase;">Tabela Inicial Sugerida</p>
        <h2>Tabela {tabela_sugerida}</h2>
        <p>Preço de Referência do Plano Plus 1x: <b>R$ {preco_fast_automatico},00</b> &nbsp;|&nbsp; TKM Técnico da Tabela: <b>R$ {tabela_tkm_sugerido},00</b></p>
    </div>
""", unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1: 
    st.markdown(f"<small style='color:#6C757D; font-weight:600;'>PONTUAÇÃO DA ÁREA</small><br><span style='font-size:18px; font-weight:700;'>{score_total}</span> <span style='font-size:14px; color:#6C757D;'>({classificacao})</span>", unsafe_allow_html=True)
    st.caption(f"Praça: {score_praca} | População: {score_populacao} | REGIC: {score_regic}")
with col_m2: 
    st.markdown(f"<small style='color:#6C757D; font-weight:600;'>INTERVALO DE TABELAS POSSÍVEIS</small><br><span style='font-size:18px; font-weight:700;'>Tab {tab_min} a {tab_max}</span>", unsafe_allow_html=True)
with col_m3: 
    st.markdown(f"<small style='color:#6C757D; font-weight:600;'>DIFERENÇA MERCADO X FAST</small><br><span style='font-size:18px; font-weight:700;'>{diferenca_fast_mercado*100:+.1f}%</span>", unsafe_allow_html=True)

st.markdown('<div class="espacador-bloco"></div>', unsafe_allow_html=True)
st.markdown("##### 🔍 Relatório de Viabilidade de Mercado")
col_v1, col_v2 = st.columns(2)
with col_v1: st.info(f"**Diretriz Diagnóstica:** {diagnostico}\n\nStatus: {alerta_mercado}")
with col_v2: st.warning(f"**Recomendação Técnico:** {recomendacao}")

st.markdown('<div class="espacador-bloco"></div>', unsafe_allow_html=True)
st.markdown("##### 📈 Viabilidade de Rentabilidade do Business Plan (BP)")
col_bp1, col_bp2 = st.columns(2)
with col_bp1:
    st.metric(label="TKM Técnico para inserir no BP:", value=f"R$ {tabela_tkm_sugerido},00")
    st.write("👉 **Instrução:** Insira este TKM no BP (business negócio da unidade) e consulte se o modelo projeta uma rentabilidade saudável para o ponto e selecione o status ao lado.")
with col_bp2:
    viabilidade_bp_selecao = st.selectbox("Selecione a viabilidade da tabela no projeto:", ["Aguardando simulação técnica...", "Viável (Rentabilidade Saudável)", "Inviável (Rentabilidade Comprometida)"], index=0)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("##### 🏢 Unidades da Rede em Operação com Perfil Similar")
df_filtrado = df_unidades[df_unidades["Estado"] == "SP"].copy() if estado == "SP" else df_unidades[df_unidades["Estado"] != "SP"].copy()

if not df_filtrado.empty:
    std_renda, std_pop, std_classe = df_unidades["Renda Média"].std() or 1, df_unidades["População"].std() or 1, df_unidades["% Classe A+"].std() or 0.1
    df_filtrado["Métrica Proximidade"] = (np.abs(df_filtrado["Renda Média"] - renda_media)/std_renda) + (np.abs(df_filtrado["População"] - populacao)/std_pop) + (np.abs(df_filtrado["% Classe A+"] - classe_a_mais_input)/std_classe)
    df_filtrado = df_filtrado.sort_values(by="Métrica Proximidade")
    
    df_filtrado["Similaridade"] = [f"{p*100:.2f}%" for p in np.linspace(0.985, 0.45, len(df_filtrado))]
    df_filtrado["% Classe A+"] = df_filtrado["% Classe A+"].apply(lambda x: f"{x*100:.0f}%")
    st.dataframe(df_filtrado[["Unidade", "Praça", "REGIC", "Renda Média", "População", "% Classe A+", "Similaridade"]].head(3), use_container_width=True, hide_index=True)

st.markdown(f"""<div class="nota-rodape">💡 <b>Observação Relevante de Governança:</b> O simulador atua exclusivamente como um direcionador estratégico inicial, toda decisão deve ser validada no <b>Comitê de Expansão</b>.</div>""", unsafe_allow_html=True)
