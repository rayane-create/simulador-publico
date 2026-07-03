import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(page_title="Fast Tennis - Simulador Estratégico", layout="wide")

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
        st.error("Credenciais inválidas.")

if not st.session_state["autenticado"]:
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color:#F8F9FA; padding:30px; border-radius:8px; border-top:5px solid #0D47A1; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <h3 style="color:#1E2229; margin-top:0; margin-bottom:5px;">Acesso Restrito Fast Tennis</h3>
                <p style="color:#6C757D; font-size:13px; margin-bottom:25px;">Insira suas credenciais corporativas autorizadas.</p>
            </div>
        """, unsafe_allow_html=True)
        st.text_input("E-mail Corporativo:", key="login_email")
        st.text_input("Senha de Acesso:", type="password", key="login_senha")
        st.button("Entrar", on_click=realizar_login, use_container_width=True)
    st.stop()

# ==========================================
# AMBIENTE AUTENTICADO - ESTILOS E HEADER
# ==========================================

st.markdown("""
    <style>
        .faixa-resultados {
            background-color: #E3F2FD;
            color: #0D47A1;
            padding: 15px 20px;
            margin: 25px -4rem 15px -4rem; 
            font-size: 22px; 
            font-weight: 700;
            border-left: 6px solid #1E88E5;
        }
        .tabela-sugerida-box {
            background-color: #F8F9FA;
            padding: 15px;
            border-radius: 6px;
            border-left: 5px solid #A3D133;
            margin-bottom: 15px;
        }
        .tabela-sugerida-box h2 {
            margin: 0;
            color: #1E2229 !important;
            font-size: 26px;
        }
    </style>
""", unsafe_allow_html=True)

col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("Simulador Estratégico de Precificação")
with col_header2:
    st.markdown(f"<p style='text-align:right; font-size:12px; color:#6C757D;'>Sessão: <b>{st.session_state['usuario_logado']}</b></p>", unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
        st.session_state["autenticado"] = False
        st.rerun()

st.markdown("---")

# ==========================================
# SEÇÃO 1: DADOS DA ÁREA DE ESTUDO E MERCADO
# ==========================================
st.subheader("📊 1. Dados da Área de Estudo e Mercado")
st.markdown("<p style='font-size:14px; color:#5A6578; margin-bottom:15px;'>Os dados imputados abaixo devem ser retirados da área de estudo delimitada no Geofusion de acordo com as diretrizes de praça e concorrência local.</p>", unsafe_allow_html=True)

with st.expander("📌 Diretrizes Geofusion (Clique para ver)"):
    st.markdown("Instruções de raio de 2km, PEA Dia e vocação de praça conforme manual de expansão.")

# CAIXA DE INPUTS
with st.container(border=True):
    c1, c2, col_in3 = st.columns(3)
    with c1:
        lista_estados = ["Selecione...", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        estado = st.selectbox("Estado (UF):", lista_estados, index=0)
        cidade = st.text_input("Cidade:", value="", placeholder="Digite a cidade...")
        populacao = st.number_input("População Total (Área):", min_value=0, value=0)
    with c2:
        regic = st.selectbox("REGIC:", ["Selecione...", "Centro Sub-Regional", "Capital Regional C", "Capital Regional B", "Capital Regional A", "Metrópole", "Grande Metrópole", "Metrópole Nacional"], index=0)
        residentes_alvo = st.number_input("Público Alvo (B1, A+, A++):", min_value=0, value=0)
        classe_a_mais = st.number_input("% Classe A+ (Ex: 0.35):", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    with col_in3:
        tipo_praca = st.selectbox("Perfil da Praça:", ["Selecione...", "Comercial", "Mista", "Residencial", "Mista Qualificada"], index=0)
        renda_media = st.number_input("Renda Média (R$):", min_value=0.0, value=0.0, step=100.0)
        tempo_proxima = st.number_input("Tempo até unidade próxima (min):", min_value=0, value=0)
        media_mercado = st.number_input("Preço Médio dos Concorrentes (Plano Plus 1x / Grupo):", min_value=0.0, value=0.0, step=10.0)

# Verificação se o usuário já preencheu os dados mínimos para calcular
dados_preenchidos = (
    estado != "Selecione..." and 
    regic != "Selecione..." and 
    tipo_praca != "Selecione..." and 
    cidade.strip() != "" and 
    renda_media > 0 and 
    media_mercado > 0
)

if not dados_preenchidos:
    st.info("💡 **Aguardando dados...** Por favor, preencha as informações da Área de Estudo acima para gerar a análise.")
else:
    # ==========================================
    # LÓGICA MATEMÁTICA (GOVERNANÇA)
    # ==========================================
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

    s_praca = {"Comercial": -1, "Mista": 0, "Residencial": 1, "Mista Qualificada": 1}.get(tipo_praca, 0)
    s_regic = {"Centro Sub-Regional": -1, "Capital Regional B": -1, "Capital Regional C": -1, "Metrópole": 0, "Grande Metrópole": 1, "Metrópole Nacional": 1}.get(regic, 0)
    
    # Nova regra calibrada de score de população por %
    if populacao < 40000:
        s_pop = 0
    else:
        pct_alvo = (residentes_alvo / populacao) if populacao > 0 else 0
        if pct_alvo >= 0.40:
            s_pop = 1
        elif pct_alvo >= 0.25:
            s_pop = 0
        else:
            s_pop = 0

    score_total = s_praca + s_regic + s_pop
    tabela_sugerida = tab_max if score_total >= 1 else tab_min

    precos = {1: 329, 2: 399, 3: 499, 4: 599, 5: 710}
    tkms = {1: 338, 2: 411, 3: 470, 4: 580, 5: 690}
    preco_ref = precos[tabela_sugerida]
    tkm_ref = tkms[tabela_sugerida]
    dif_mercado = (preco_ref - media_mercado) / media_mercado if media_mercado > 0 else 0

    if dif_mercado < -0.10: diag, status, rec = "Abaixo da Média Regional", "Preço Abaixo do Mercado", "Avaliar margem para reposicionamento."
    elif dif_mercado <= 0.20: diag, status, rec = "Compatível com o Cenário", "Preço Aderente", "Posicionamento adequado ao mercado."
    else: diag, status, rec = "Muito Acima da Concorrência", "Descolamento de Preço", "Revisão mandatória em Comitê."

    # ==========================================
    # PAINEL DE RESULTADOS (AGRUPADOS)
    # ==========================================
    st.markdown('<div class="faixa-resultados">📊 Análise de dados e recomendações</div>', unsafe_allow_html=True)

    # BLOCO 1: TABELA E MERCADO
    with st.container(border=True):
        st.markdown(f"""
            <div class="tabela-sugerida-box">
                <p style="margin:0; font-size:11px; color:#6C757D; font-weight:bold; text-transform:uppercase;">Tabela Inicial Sugerida</p>
                <h2>Tabela {tabela_sugerida}</h2>
                <p style="margin:0; font-size:14px;">Preço Ref. Plano Plus 1x: <b>R$ {preco_ref},00</b> | TKM Técnico: <b>R$ {tkm_ref},00</b></p>
            </div>
        """, unsafe_allow_html=True)

        if tempo_proxima <= 15 and tempo_proxima > 0:
            st.error("🚨 **Proteção de Rede:** Existe unidade próxima. Verificar compatibilidade de tabelas.")

        st.markdown(f"<small style='color:#6C757D;'>Intervalo de tabelas possíveis:</small> <b>Tab {tab_min} a {tab_max}</b>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("##### 🔍 Relatório de Viabilidade de Mercado")
        cv1, cv2, cv3 = st.columns([1.2, 1.2, 1])
        with cv1: 
            st.info(f"**Diretriz:** {diag}\n\n**Status:** {status}")
        with cv2: 
            st.warning(f"**Recomendação:** {rec}")
        with cv3:
            st.markdown(f"""
                <div style="background-color: #F8F9FA; padding: 12px; border-radius: 4px; border: 1px solid #E0E0E0; height: 100%;">
                    <span style="color:#6C757D; font-size:13px; font-weight:500;">Diferença Mercado x Fast</span><br>
                    <span style="font-size:20px; font-weight:700; color:{'#D32F2F' if dif_mercado > 0.20 else '#2E7D32'};">{dif_mercado*100:+.1f}%</span>
                </div>
            """, unsafe_allow_html=True)

    # BLOCO 2: RENTABILIDADE
    st.write("")
    with st.container(border=True):
        st.markdown("##### 📈 Viabilidade de Rentabilidade do Business Plan (BP)")
        cbp1, cb2 = st.columns(2)
        with cbp1:
            st.metric(label="TKM Técnico para o BP:", value=f"R$ {tkm_ref},00")
        with cb2:
            viabilidade_bp = st.selectbox("Status de rentabilidade projetada:", ["Aguardando simulação...", "Viável (Rentabilidade Saudável)", "Inviável (Rentabilidade Comprometida)"])
            st.caption("⚠️ *Nota: Em caso de inviabilidade necessário revisar decisão*")

    # ==========================================
    # CÁLCULO DE SIMILARIDADE REAL PARALELO POR REGIAO
    # ==========================================
    st.write("")
    st.markdown("##### 🏢 Unidades da Rede com Perfil Similar")
    
    df_existentes = [
        {"Unidade": "Fast Tennis Alphaville - São Paulo", "Cidade": "Barueri", "IsSP": True, "Renda Média": 27400, "População": 44300, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Alto da Boa Vista - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 23654, "População": 85519, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Alto de Pinheiros - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 23900, "População": 82500, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Alto do Ipiranga - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 19775, "População": 177000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Anhanguera - Jundiaí", "Cidade": "Jundiaí", "IsSP": True, "Renda Média": 11650, "População": 67900, "REGIC": "Capital Regional C", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Bebedouro - Bebedouro", "Cidade": "Bebedouro", "IsSP": True, "Renda Média": 5900, "População": 44900, "REGIC": "Centro Sub-Regional B", "Tabela Praticada": "Tabela 1"},
        {"Unidade": "Fast Tennis Botafogo - Campinas", "Cidade": "Campinas", "IsSP": True, "Renda Média": 12300, "População": 96574, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Brooklin - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 29400, "População": 162400, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Campo Belo - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 27328, "População": 117500, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Cantareira - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 11500, "População": 95500, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Centro São Bernardo - São Bernardo do Campo", "Cidade": "São Bernardo do Campo", "IsSP": True, "Renda Média": 10800, "População": 164300, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Chacará Inglesa - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 21400, "População": 178712, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Chacará Santo Antônio - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 25795, "População": 78250, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Indaiatuba - São Paulo", "Cidade": "Indaiatuba", "IsSP": True, "Renda Média": 11187, "População": 53898, "REGIC": "Centro Sub-Regional", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Jardim - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 14195, "População": 128600, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4"},
        {"Unidade": "Fast Tennis Jardim Portal da Colina - Sorocaba", "Cidade": "Sorocaba", "IsSP": True, "Renda Média": 11900, "População": 52624, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Lapa - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 14200, "População": 107250, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4"},
        {"Unidade": "Fast Tennis Moema - São Paulo", "Cidade": "São Paulo", "Renda Média": 28900, "População": 143796, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "IsSP": True},
        {"Unidade": "Fast Tennis Monte Pascal - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 21446, "População": 90476, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Mooca - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 13400, "População": 147000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4"},
        {"Unidade": "Fast Tennis Morumbi - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 14200, "População": 165700, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Nova Aliança Sul - Ribeirão Preto", "Cidade": "Ribeirão Preto", "IsSP": True, "Renda Média": 12900, "População": 90800, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Parque Piqueri - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 12800, "População": 138700, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4"},
        {"Unidade": "Fast Tennis Praia Grande - Praia Grande", "Cidade": "Praia Grande", "IsSP": True, "Renda Média": 8900, "População": 84400, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "FastTennis Radial Leste - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 15700, "População": 146400, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4"},
        {"Unidade": "Fast Tennis Rio Claro - São Paulo", "Cidade": "Rio Claro", "IsSP": True, "Renda Média": 7400, "População": 72800, "REGIC": "Centro Sub-Regional", "Tabela Praticada": "Tabela 1"},
        {"Unidade": "Fast Tennis Salto - São Paulo", "Cidade": "Salto", "IsSP": True, "Renda Média": 6560, "População": 54900, "REGIC": "Centro Sub-Regional A", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Santana - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 17700, "População": 153100, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Santo Amaro", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 21100, "População": 82400, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis São Caetano - São Caetano do Sul", "Cidade": "São Caetano do Sul", "IsSP": True, "Renda Média": 10200, "População": 122900, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Saúde - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 17700, "População": 186000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Taquaral - Campinas", "Cidade": "Campinas", "IsSP": True, "Renda Média": 12738, "População": 40203, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Três Poderes - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 18100, "População": 587000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Verbo Divino - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 24800, "População": 77600, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Vila Olímpia - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 30900, "População": 160900, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        {"Unidade": "Fast Tennis Ypiranga - São Paulo", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 19000, "População": 120000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5"},
        
        # --- FORA DE SP (IsSP: False) ---
        {"Unidade": "Fast Tennis Aguas Claras - Brasília", "Cidade": "Brasília", "IsSP": False, "Renda Média": 20740, "População": 80388, "REGIC": "Metrópole Nacional", "Tabela Praticada": "Tabela 4"},
        {"Unidade": "Fast Tennis Belvedere - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 23100, "População": 63400, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Boa Viagem - Recife", "Cidade": "Recife", "IsSP": False, "Renda Média": 12214, "População": 102900, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Buritis I - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 16700, "População": 80900, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Calafate - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 13100, "População": 121200, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 1"},
        {"Unidade": "Fast Tennis Capim Macio - Natal", "Cidade": "Natal", "IsSP": False, "Renda Média": 14700, "População": 64400, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Castelo - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 10500, "População": 111575, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Cidade Nova - Cidade Nova", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 10969, "População": 123470, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Contagem - Contagem", "Cidade": "Contagem", "IsSP": False, "Renda Média": 7860, "População": 73600, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 1"},
        {"Unidade": "Fast Tennis Estoril - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 12612, "População": 85000, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Estrela Sul - Juiz de Fora", "Cidade": "Juiz de Fora", "IsSP": False, "Renda Média": 10480, "População": 113000, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 1"},
        {"Unidade": "Fast Tennis Guararapes - Fortaleza", "Cidade": "Fortaleza", "IsSP": False, "Renda Média": 12450, "População": 54706, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Morada da Colina - Uberlândia", "Cidade": "Uberlândia", "IsSP": False, "Renda Média": 14528, "População": 54900, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Orla da Pampulha - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 9940, "População": 42149, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Pampulha - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 11675, "População": 75076, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Ponte JK - Brasília", "Cidade": "Brasília", "IsSP": False, "Renda Média": 25400, "População": 95617, "REGIC": "Metrópole Nacional", "Tabela Praticada": "Tabela 4"},
        {"Unidade": "Fast Tennis Praia do Canto - Vitória", "Cidade": "Vitória", "IsSP": False, "Renda Média": 16840, "População": 83239, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Recreio - Rio de Janeiro", "Cidade": "Rio de Janeiro", "IsSP": False, "Renda Média": 22000, "População": 74360, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Salgado Filho - Curitiba", "Cidade": "Curitiba", "IsSP": False, "Renda Média": 8900, "População": 64000, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Santa Lúcia - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 19400, "População": 88597, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Santa Rosa - Niterói", "Cidade": "Niterói", "IsSP": False, "Renda Média": 17400, "População": 178510, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis São Bento - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 16700, "População": 127317, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Saul Macedo - Belo Horizonte", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 23100, "População": 63400, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Sete Lagoas - Sete Lagoas", "Cidade": "Sete Lagoas", "IsSP": False, "Renda Média": 12514, "População": 50760, "REGIC": "Capital Regional C", "Tabela Praticada": "Tabela 1"},
        {"Unidade": "Fast Tennis Setor Bueno - Goiânia", "Cidade": "Goiânia", "IsSP": False, "Renda Média": 17800, "População": 94500, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3"},
        {"Unidade": "Fast Tennis Tirol- Natal", "Cidade": "Natal", "IsSP": False, "Renda Média": 15400, "População": 72800, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2"},
        {"Unidade": "Fast Tennis Vilhena - Rondônia", "Cidade": "Vilhena", "IsSP": False, "Renda Média": 6100, "População": 42800, "REGIC": "Centro Sub-Regional", "Tabela Praticada": "Tabela 1"}
    ]
    
    df_base = pd.DataFrame(df_existentes)
    
    if not df_base.empty:
        # CRUCIAL: Separação rígida da base com base no input do usuário
        alvo_sp = (estado == "SP")
        df_filtrado = df_base[df_base['IsSP'] == alvo_sp].copy()
        
        if not df_filtrado.empty:
            # Cálculo de similaridade real focado apenas no grupo correto (SP ou Fora de SP)
            df_filtrado['Distancia'] = np.sqrt(
                ((df_filtrado['Renda Média'] - renda_media) / (renda_media if renda_media > 0 else 1))**2 + 
                ((df_filtrado['População'] - populacao) / (populacao if populacao > 0 else 1))**2
            )
            df_ranking = df_filtrado.sort_values(by='Distancia').head(3)
            st.dataframe(df_ranking[["Unidade", "Cidade", "Renda Média", "População", "REGIC", "Tabela Praticada"]], use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma unidade encontrada nessa região regional para comparação.")
    else:
        st.info("Nenhuma unidade cadastrada na base de dados.")

    st.markdown(f"""<div style="background-color:#FFF8E1; border-left:5px solid #FFB300; padding:15px; border-radius:4px; font-size:13px; color:#5D4037; margin-top:30px;">💡 <b>Governança:</b> O simulador é um direcionador estratégico. Decisões finais cabem ao Comitê de Expansão.</div>""", unsafe_allow_html=True)
