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
# Introdução recuperada com sucesso:
st.markdown("<p style='font-size:14px; color:#5A6578; margin-bottom:15px;'>Os dados imputados abaixo devem ser retirados da área de estudo delimitada no Geofusion de acordo com as diretrizes de praça e concorrência local.</p>", unsafe_allow_html=True)

with st.expander("📌 Diretrizes Geofusion (Clique para ver)"):
    st.markdown("Instruções de raio de 2km, PEA Dia e vocação de praça conforme manual de expansion.")

# CAIXA DE INPUTS
with st.container(border=True):
    c1, c2, col_in3 = st.columns(3)
    with c1:
        estado = st.selectbox("Estado (UF):", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], index=14)
        cidade = st.text_input("Cidade:", value="Belo Horizonte")
        populacao = st.number_input("População Total (Área):", min_value=0, value=85000)
    with c2:
        regic = st.selectbox("REGIC:", ["Centro Sub-Regional", "Capital Regional C", "Capital Regional B", "Capital Regional A", "Metrópole", "Grande Metrópole", "Metrópole Nacional"], index=4)
        residentes_alvo = st.number_input("Público Alvo (B1, A+, A++):", min_value=0, value=16500)
        classe_a_mais = st.number_input("% Classe A+ (Ex: 0.35):", min_value=0.0, max_value=1.0, value=0.35)
    with col_in3:
        tipo_praca = st.selectbox("Perfil da Praça:", ["Comercial", "Mista", "Residencial", "Mista Qualificada"], index=2)
        renda_media = st.number_input("Renda Média (R$):", min_value=0.0, value=19700.0)
        tempo_proxima = st.number_input("Tempo até unidade próxima (min):", min_value=0, value=30)
        # Observação entre parênteses recuperada com sucesso:
        media_mercado = st.number_input("Preço Médio Concorrentes (Plano Plus 1x - Grupo):", min_value=0.0, value=405.0)

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

# BLOCO 1: TABELA E MERCADO (JUNTO NO MESMO QUADRADO)
with st.container(border=True):
    st.markdown(f"""
        <div class="tabela-sugerida-box">
            <p style="margin:0; font-size:11px; color:#6C757D; font-weight:bold; text-transform:uppercase;">Tabela Inicial Sugerida</p>
            <h2>Tabela {tabela_sugerida}</h2>
            <p style="margin:0; font-size:14px;">Preço Ref. Plano Plus 1x: <b>R$ {preco_ref},00</b> | TKM Técnico: <b>R$ {tkm_ref},00</b></p>
        </div>
    """, unsafe_allow_html=True)

    if tempo_proxima <= 15:
        st.error("🚨 **Proteção de Rede:** Existe unidade próxima. Verificar compatibilidade de tabelas.")

    # Intervalo de Tabelas mantido aqui de forma limpa
    st.markdown(f"<small style='color:#6C757D;'>Intervalo de tabelas possíveis:</small> <b>Tab {tab_min} a {tab_max}</b>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Diferença mercado x Fast trazida para cá (próxima das informações de viabilidade de mercado)
    st.markdown(f"##### 🔍 Relatório de Viabilidade de Mercado &nbsp;&nbsp;<span style='font-size:14px; color:#6C757D; font-weight:normal;'>(Diferença mercado x Fast: <b>{dif_mercado*100:+.1f}%</b>)</span>", unsafe_allow_html=True)
    
    cv1, cv2 = st.columns(2)
    with cv1: st.info(f"**Diretriz:** {diag}\n\n**Status:** {status}")
    with cv2: st.warning(f"**Recomendação:** {rec}")

# BLOCO 2: RENTABILIDADE (SOZINHO)
st.write("")
with st.container(border=True):
    st.markdown("##### 📈 Viabilidade de Rentabilidade do Business Plan (BP)")
    cb
