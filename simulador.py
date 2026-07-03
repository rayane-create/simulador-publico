import streamlit as st
import pandas as pd
import numpy as np
import requests

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

# CAIXA DE INPUTS - Iniciando limpos ou com opção de seleção neutra
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
    s_pop = -1 if populacao < 40000 else (1 if residentes_alvo >= 15000 else 0)
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
            # AJUSTADO: Agora em texto menor e limpo, sem o box gigante do st.metric
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

    # UNIDADES SIMILARES
    st.write("")
    st.markdown("##### 🏢 Unidades da Rede com Perfil Similar")
    df_existentes = [
        {"Unidade": "Fast Tennis Alphaville", "Estado": "SP", "Renda": 27400, "Pop": 44300},
        {"Unidade": "Fast Tennis Belvedere", "Estado": "MG", "Renda": 23100, "Pop": 63400},
        {"Unidade": "Fast Tennis Capim Macio", "Estado": "RN", "Renda": 14700, "Pop": 64400}
    ]
    st.dataframe(pd.DataFrame(df_existentes), use_container_width=True, hide_index=True)

    st.markdown(f"""<div style="background-color:#FFF8E1; border-left:5px solid #FFB300; padding:15px; border-radius:4px; font-size:13px; color:#5D4037; margin-top:30px;">💡 <b>Governança:</b> O simulador é um direcionador estratégico. Decisões finais cabem ao Comitê de Expansão.</div>""", unsafe_allow_html=True)
