import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página corporativa da Fast Tennis
st.set_page_config(page_title="Fast Tennis - Simulador Estratégico", layout="wide")

# ==========================================
# APLICAÇÃO DA IDENTIDADE VISUAL FAST TENNIS (GUIDELINE 2025)
# Paleta Oficial: Blue FT (#053CD8), Navy FT (#022D8A), Green FT (#0DF205), Black (#000000)
# Tipografia: Bw Nista Geometric / Montserrat
# ==========================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,700;0,800;1,800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Bw Nista Geometric', 'Montserrat', sans-serif !important;
        }
        
        /* Títulos institucionais em Navy FT (#022D8A) */
        h1, h2, h3, h4, h5, h6 {
            color: #022D8A !important;
            font-weight: 800 !important;
        }
        
        /* Botões padronizados em Green FT (#0DF205) com cantos arredondados */
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
        
        /* Faixa de Destaque de Resultados */
        .faixa-resultados {
            background-color: #022D8A;
            color: #FFFFFF;
            padding: 15px 20px;
            margin: 25px -4rem 15px -4rem; 
            font-size: 20px; 
            font-weight: 800;
            border-left: 6px solid #0DF205;
        }
        
        /* Caixa do Destaque da Tabela Sugerida */
        .tabela-sugerida-box {
            background-color: #F8F9FA;
            padding: 18px;
            border-radius: 8px;
            border-left: 6px solid #0DF205;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        }
        .tabela-sugerida-box h2 {
            margin: 4px 0;
            color: #022D8A !important;
            font-size: 28px;
            font-weight: 800;
        }

        /* Caixa de Exceção Selecionada */
        .tabela-excecao-box {
            background-color: #FFF8E1;
            padding: 18px;
            border-radius: 8px;
            border-left: 6px solid #FFB300;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        }
        .tabela-excecao-box h2 {
            margin: 4px 0;
            color: #B78103 !important;
            font-size: 28px;
            font-weight: 800;
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
        st.error("Credenciais inválidas.")

if not st.session_state["autenticado"]:
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color:#F8F9FA; padding:30px; border-radius:12px; border-top:6px solid #022D8A; box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
                <h3 style="color:#022D8A; margin-top:0; margin-bottom:5px; font-weight:800;">🔒 Acesso Restrito Fast Tennis</h3>
                <p style="color:#6C757D; font-size:13px; margin-bottom:25px;">Insira suas credenciais corporativas autorizadas.</p>
            </div>
        """, unsafe_allow_html=True)
        st.text_input("E-mail Corporativo:", key="login_email")
        st.text_input("Senha de Acesso:", type="password", key="login_senha")
        st.button("Entrar", on_click=realizar_login, use_container_width=True)
    st.stop()

# ==========================================
# FUNÇÃO PARA LIMPAR OS CAMPOS (NOVA SIMULAÇÃO)
# ==========================================
def limpar_campos():
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

if "val_estado" not in st.session_state:
    limpar_campos()

# ==========================================
# AMBIENTE AUTENTICADO - HEADER
# ==========================================

col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("🎾 Simulador Estratégico de Precificação")
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

# CAIXA DE INPUTS (CIDADE LIVRE)
with st.container(border=True):
    c1, c2, col_in3 = st.columns(3)
    with c1:
        lista_estados = ["Selecione...", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        
        estado = st.selectbox("Estado (UF):", lista_estados, key="val_estado")
        cidade = st.text_input("Cidade:", placeholder="Digite a cidade...", key="val_cidade")
        populacao = st.number_input("População Total (Área):", min_value=0, step=1, key="val_populacao")
        
        st.markdown("**📌 Percentuais de Classes (Geofusion)**")
        classe_a_mais_mais = st.number_input("% Classe A++ (Ex: 0.15):", min_value=0.0, max_value=1.0, step=0.01, key="val_classe_a_mais_mais")
        classe_a_mais = st.number_input("% Classe A+ (Ex: 0.23):", min_value=0.0, max_value=1.0, step=0.01, key="val_classe_a_mais")
        classe_b1 = st.number_input("% Classe B1 (Ex: 0.21):", min_value=0.0, max_value=1.0, step=0.01, key="val_classe_b1")
        
    with c2:
        regic = st.selectbox("REGIC:", ["Selecione...", "Centro Sub-Regional", "Capital Regional C", "Capital Regional B", "Capital Regional A", "Metrópole", "Grande Metrópole", "Metrópole Nacional"], key="val_regic")
        tipo_praca = st.selectbox("Perfil da Praça:", ["Selecione...", "Comercial", "Mista", "Residencial", "Mista Qualificada"], key="val_tipo_praca")
        
        soma_percentuais = classe_b1 + classe_a_mais + classe_a_mais_mais
        calculo_alvo = int(soma_percentuais * populacao)
        
        st.metric(label="🎯 Público Alvo Calculado (B1 + A+ + A++):", value=f"{calculo_alvo:,} hab.")
        st.caption(f"Soma das classes: {soma_percentuais*100:.1f}% da população total.")

    with col_in3:
        renda_media = st.number_input("Renda Média (R$):", min_value=0.0, step=100.0, key="val_renda_media")
        tempo_proxima = st.number_input("Tempo até unidade próxima (min):", min_value=0, step=1, key="val_tempo_proxima")
        media_mercado = st.number_input("Preço Médio dos Concorrentes (Plano Plus 1x / Grupo):", min_value=0.0, step=10.0, key="val_media_mercado")

    st.write("")
    col_btn1, col_btn2 = st.columns([5, 1])
    with col_btn2:
        st.button("🧹 Nova Simulação", on_click=limpar_campos, use_container_width=True)

# Validação dos campos obrigatórios
dados_preenchidos = (
    estado != "Selecione..." and 
    regic != "Selecione..." and 
    tipo_praca != "Selecione..." and 
    cidade.strip() != "" and
    cidade.strip() != "Selecione a cidade..." and
    renda_media > 0 and 
    media_mercado > 0
)

if not dados_preenchidos:
    st.info("💡 **Aguardando dados...** Por favor, preencha as informações da Área de Estudo acima para gerar a análise.")
else:
    # ==========================================
    # LÓGICA MATEMÁTICA DE PRECIFICAÇÃO
    # ==========================================
    
    # 1º PONTO: INTERVALO DE TABELAS BASEADO NA RENDA MÉDIA
    if estado == "SP":
        if renda_media <= 8500.00:
            tab_min, tab_max = 1, 2
        elif renda_media <= 11500.00:
            tab_min, tab_max = 2, 3
        elif renda_media <= 16000.00:
            tab_min, tab_max = 3, 4
        elif renda_media <= 22000.00:
            tab_min, tab_max = 4, 5
        else:
            tab_min, tab_max = 5, 5
    else:
        if renda_media <= 9500.00:
            tab_min, tab_max = 1, 2
        elif renda_media <= 13500.00:
            tab_min, tab_max = 2, 3
        elif renda_media <= 18000.00:
            tab_min, tab_max = 3, 4
        elif renda_media <= 25000.00:
            tab_min, tab_max = 4, 5
        else:
            tab_min, tab_max = 5, 5

    # 2º PONTO: DIRECIONAMENTO DENTRO DO INTERVALO
    if populacao < 40000:
        tabela_sugerida = tab_min
    else:
        if calculo_alvo >= 25000:
            tabela_sugerida = tab_max
        else:
            if soma_percentuais >= 0.40:
                tabela_sugerida = tab_max
            elif soma_percentuais >= 0.30:
                tabela_sugerida = int(np.round((tab_min + tab_max) / 2))
            else:
                tabela_sugerida = tab_min

    precos = {1: 329, 2: 399, 3: 499, 4: 599, 5: 710}
    tkms = {1: 338, 2: 411, 3: 470, 4: 580, 5: 690}
    
    # ==========================================
    # PAINEL DE RESULTADOS E RECOMENDAÇÕES
    # ==========================================
    st.markdown('<div class="faixa-resultados">📊 Análise de Dados e Recomendações</div>', unsafe_allow_html=True)

    with st.container(border=True):
        
        # EXIBIÇÃO DA TABELA SUGERIDA PELOS DADOS
        preco_sugerido = precos[tabela_sugerida]
        tkm_sugerido = tkms[tabela_sugerida]
        
        st.markdown(f"""
            <div class="tabela-sugerida-box">
                <p style="margin:0; font-size:11px; color:#6C757D; font-weight:bold; text-transform:uppercase;">Tabela Sugerida pelo Algoritmo (Dados)</p>
                <h2>Tabela {tabela_sugerida}</h2>
                <p style="margin:0; font-size:14px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {preco_sugerido},00</b> | TKM Técnico: <b>R$ {tkm_sugerido},00</b></p>
            </div>
        """, unsafe_allow_html=True)

        # ----------------------------------------------------
        # 🟡 NOVO RECURSO: BOTÃO / CHECKBOX DE EXCEÇÃO TÉCNICA
        # ----------------------------------------------------
        st.markdown("##### ⚠️ Ajuste de Exceção / Percepção de Mercado")
        aplicar_excecao = st.checkbox("Ativar exceção técnica (Sobrevir tabela baseada no comportamento de mercado além dos dados)", key="chk_excecao")

        if aplicar_excecao:
            col_exc1, col_exc2 = st.columns([1, 2])
            with col_exc1:
                tabela_escolhida = st.selectbox(
                    "Selecione a Tabela Definitiva:",
                    [1, 2, 3, 4, 5],
                    index=tabela_sugerida - 1,
                    key="val_tabela_excecao"
                )
            with col_exc2:
                justificativa_excecao = st.text_input(
                    "Justificativa da Exceção (Obrigatório):",
                    placeholder="Ex: Concorrência local com forte posicionamento premium, alta percepção de valor na zona de influência...",
                    key="val_justificativa_excecao"
                )

            tabela_final = tabela_escolhida
            
            # Caixa destacando a tabela escolhida por exceção
            st.markdown(f"""
                <div class="tabela-excecao-box">
                    <p style="margin:0; font-size:11px; color:#B78103; font-weight:bold; text-transform:uppercase;">📌 Tabela Escolhida por Decisão Técnica (Exceção)</p>
                    <h2>Tabela {tabela_final}</h2>
                    <p style="margin:0; font-size:14px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {precos[tabela_final]},00</b> | TKM Técnico: <b>R$ {tkms[tabela_final]},00</b></p>
                    {f'<p style="margin:6px 0 0 0; font-size:12px; color:#5D4037;"><b>Justificativa:</b> {justificativa_excecao}</p>' if justificativa_excecao else ''}
                </div>
            """, unsafe_allow_html=True)
        else:
            tabela_final = tabela_sugerida

        # Cálculo de preço e mercado baseado na TABELA FINAL (Seja sugerida ou de exceção)
        preco_ref = precos[tabela_final]
        tkm_ref = tkms[tabela_final]

        if tempo_proxima <= 15 and tempo_proxima > 0:
            st.error("🚨 **Proteção de Rede:** Existe unidade próxima. Verificar compatibilidade de tabelas.")

        st.markdown(f"<small style='color:#6C757D;'>Intervalo de tabelas possíveis calculado:</small> <b>Tab {tab_min} a {tab_max}</b>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Diagnóstico com base na Tabela Final definida
        dif_mercado = (preco_ref - media_mercado) / media_mercado if media_mercado > 0 else 0

        if dif_mercado < -0.10: diag, status, rec = "Abaixo da Média Regional", "Preço Abaixo do Mercado", "Avaliar margem para reposicionamento."
        elif dif_mercado <= 0.20: diag, status, rec = "Compatível com o Cenário", "Preço Aderente", "Posicionamento adequado ao mercado."
        else: diag, status, rec = "Muito Acima da Concorrência", "Descolamento de Preço", "Revisão mandatória em Comitê."

        st.markdown("##### 🔍 Relatório de Viabilidade de Mercado")
        cv1, cv2, cv3 = st.columns([1.2, 1.2, 1])
        with cv1: 
            st.info(f"**Diretriz:** {diag}\n\n**Status:** {status}")
        with cv2: 
            st.warning(f"**Recomendação:** {rec}")
        with cv3:
            st.markdown(f"""
                <div style="background-color: #F8F9FA; padding: 12px; border-radius: 6px; border: 1px solid #E0E0E0; height: 100%;">
                    <span style="color:#6C757D; font-size:13px; font-weight:500;">Diferença Mercado x Fast</span><br>
                    <span style="font-size:20px; font-weight:800; color:{'#D32F2F' if dif_mercado > 0.20 else '#2E7D32'};">{dif_mercado*100:+.1f}%</span>
                </div>
            """, unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.markdown("##### 📈 Viabilidade de Rentabilidade do Business Plan (BP)")
        cbp1, cb2 = st.columns(2)
        with cbp1:
            st.metric(label="TKM Técnico para o BP:", value=f"R$ {tkm_ref},00")
        with cb2:
            viabilidade_bp = st.selectbox(
                "Status de rentabilidade projetada:", 
                [
                    "Aguardando simulação...", 
                    "Viável (Alinhado às Diretrizes do BP)", 
                    "Inviável (Payback projetado superior a 60 meses)", 
                    "Margem Líquida abaixo de R$ 10.000,00", 
                    "Margem Líquida entre R$ 10.000,00 e R$ 15.000,00", 
                    "Margem Líquida entre R$ 15.000,00 e R$ 20.000,00", 
                    "Margem Líquida acima de R$ 20.000,00"
                ]
            )
            st.caption("⚠️ *Nota: Em caso de inviabilidade é necessário revisar a decisão no Comitê.*")

    # ==========================================
    # CÁLCULO DE SIMILARIDADE REAL MULTI-CLASSES
    # ==========================================
    st.write("")
    st.markdown("##### 🏢 Unidades da Rede com Perfil Similar")
    
    df_existentes = [
        {"Unidade": "FT AGUAS CLARAS - DF", "Cidade": "Brasília", "IsSP": False, "Renda Média": 20740, "População": 80388, "REGIC": "Metrópole Nacional", "Tabela Praticada": "Tabela 4", "A++": 0.23, "A+": 0.27, "B1": 0.21},
        {"Unidade": "FT ALPHAVILLE - SP", "Cidade": "Barueri", "IsSP": True, "Renda Média": 27400, "População": 44300, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.15, "A+": 0.23, "B1": 0.21},
        {"Unidade": "FT ALTO DA BOA VISTA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 23654, "População": 85519, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.17, "A+": 0.20, "B1": 0.18},
        {"Unidade": "FT ALTO DOS PINHEIROS - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 23900, "População": 82500, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.22, "A+": 0.20, "B1": 0.18},
        {"Unidade": "FT ALTO DO IPIRANGA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 19775, "População": 177000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.14, "A+": 0.16, "B1": 0.15},
        {"Unidade": "FT ANHANGUERA - SP", "Cidade": "Jundiaí", "IsSP": True, "Renda Média": 11650, "População": 67900, "REGIC": "Capital Regional C", "Tabela Praticada": "Tabela 3", "A++": 0.00, "A+": 0.10, "B1": 0.18},
        {"Unidade": "FT BEBEDOURO - SP", "Cidade": "Bebedouro", "IsSP": True, "Renda Média": 5900, "População": 44900, "REGIC": "Centro Sub-Regional B", "Tabela Praticada": "Tabela 1", "A++": 0.02, "A+": 0.09, "B1": 0.15},
        {"Unidade": "FT BELVEDERE - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 23100, "População": 63400, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3", "A++": 0.22, "A+": 0.26, "B1": 0.17},
        {"Unidade": "FT BOA VIAGEM - PE", "Cidade": "Recife", "IsSP": False, "Renda Média": 12214, "População": 102000, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2", "A++": 0.08, "A+": 0.14, "B1": 0.16},
        {"Unidade": "FT BOTAFOGO - SP", "Cidade": "Campinas", "IsSP": True, "Renda Média": 12300, "População": 96574, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 3", "A++": 0.07, "A+": 0.13, "B1": 0.20},
        {"Unidade": "FT BROOKLIN - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 29400, "População": 162400, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.30, "A+": 0.27, "B1": 0.15},
        {"Unidade": "FT BURITIS - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 16700, "População": 80900, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2", "A++": 0.10, "A+": 0.24, "B1": 0.24},
        {"Unidade": "FT CALAFATE - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 13100, "População": 121200, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 1", "A++": 0.09, "A+": 0.17, "B1": 0.20},
        {"Unidade": "FT CAMPO BELO - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 27328, "População": 117500, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.27, "A+": 0.25, "B1": 0.15},
        {"Unidade": "FT CANTAREIRA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 11500, "População": 95500, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 3", "A++": 0.09, "A+": 0.18, "B1": 0.23},
        {"Unidade": "FT CAPIM MACIO - RN", "Cidade": "Natal", "IsSP": False, "Renda Média": 14700, "População": 64400, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2", "A++": 0.10, "A+": 0.18, "B1": 0.22},
        {"Unidade": "FT CASTELO - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 10500, "População": 111575, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2", "A++": 0.05, "A+": 0.13, "B1": 0.20},
        {"Unidade": "FT CENTRO SÃO BERNARDO - SP", "Cidade": "São Bernardo do Campo", "IsSP": True, "Renda Média": 10800, "População": 164300, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 3", "A++": 0.05, "A+": 0.12, "B1": 0.18},
        {"Unidade": "FT CHÁCARA INGLESA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 21400, "População": 178712, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.18, "A+": 0.22, "B1": 0.15},
        {"Unidade": "FT CHÁCARA SANTO ANTÔNIO - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 25795, "População": 78250, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.24, "A+": 0.25, "B1": 0.14},
        {"Unidade": "FT CIDADE NOVA - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 10969, "População": 123470, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2", "A++": 0.03, "A+": 0.15, "B1": 0.19},
        {"Unidade": "FT CONTAGEM - MG", "Cidade": "Contagem", "IsSP": False, "Renda Média": 7860, "População": 73600, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 1", "A++": 0.00, "A+": 0.08, "B1": 0.15},
        {"Unidade": "FT ESTORIL - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 12612, "População": 85000, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2", "A++": 0.05, "A+": 0.17, "B1": 0.22},
        {"Unidade": "FT ESTRELA SUL - JF", "Cidade": "Juiz de Fora", "IsSP": False, "Renda Média": 10480, "População": 113000, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 1", "A++": 0.04, "A+": 0.12, "B1": 0.18},
        {"Unidade": "FT GUARARAPES - CE", "Cidade": "Fortaleza", "IsSP": False, "Renda Média": 12450, "População": 54706, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2", "A++": 0.08, "A+": 0.14, "B1": 0.21},
        {"Unidade": "FT INDAIATUBA - SP", "Cidade": "Indaiatuba", "IsSP": True, "Renda Média": 11187, "População": 53898, "REGIC": "Centro Sub-Regional", "Tabela Praticada": "Tabela 2", "A++": 0.02, "A+": 0.10, "B1": 0.14},
        {"Unidade": "FT JARDIM - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 14195, "População": 128600, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4", "A++": 0.07, "A+": 0.18, "B1": 0.23},
        {"Unidade": "FT JARDIM PORTAL DA COLINA - SP", "Cidade": "Sorocaba", "IsSP": True, "Renda Média": 11900, "População": 52624, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 3", "A++": 0.02, "A+": 0.10, "B1": 0.14},
        {"Unidade": "FT JARDIM SOCIAL - PR", "Cidade": "Curitiba", "IsSP": False, "Renda Média": 31000, "População": 56708, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.10, "A+": 0.31, "B1": 0.21},
        {"Unidade": "FT LAPA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 14200, "População": 107250, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4", "A++": 0.08, "A+": 0.18, "B1": 0.22},
        {"Unidade": "FT MOEMA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 28900, "População": 143796, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.30, "A+": 0.26, "B1": 0.13},
        {"Unidade": "FT MOOCA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 13400, "População": 147000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4", "A++": 0.07, "A+": 0.18, "B1": 0.23},
        {"Unidade": "FT MORADA DA COLINA - MG", "Cidade": "Uberlândia", "IsSP": False, "Renda Média": 14528, "População": 54900, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 2", "A++": 0.07, "A+": 0.16, "B1": 0.18},
        {"Unidade": "FT MORUMBI - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 14200, "População": 165700, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.12, "A+": 0.21, "B1": 0.20},
        {"Unidade": "FT NOVA ALIANÇA SUL - SP", "Cidade": "Ribeirão Preto", "IsSP": True, "Renda Média": 12900, "População": 90800, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 3", "A++": 0.08, "A+": 0.15, "B1": 0.18},
        {"Unidade": "FT ORLA PAMPULHA - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 9940, "População": 42149, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2", "A++": 0.01, "A+": 0.11, "B1": 0.17},
        {"Unidade": "FT PAMPULHA - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 11675, "População": 75076, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2", "A++": 0.04, "A+": 0.12, "B1": 0.18},
        {"Unidade": "FT PARQUE PIQUERI - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 12800, "População": 138700, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4", "A++": 0.08, "A+": 0.14, "B1": 0.17},
        {"Unidade": "FT PONTE JK - DF", "Cidade": "Brasília", "IsSP": False, "Renda Média": 25400, "População": 95617, "REGIC": "Metrópole Nacional", "Tabela Praticada": "Tabela 4", "A++": 0.24, "A+": 0.30, "B1": 0.14},
        {"Unidade": "FT PRAIA DO CANTO - ES", "Cidade": "Vitória", "IsSP": False, "Renda Média": 16840, "População": 83239, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3", "A++": 0.11, "A+": 0.18, "B1": 0.22},
        {"Unidade": "FT PRAIA GRANDE - SP", "Cidade": "Praia Grande", "IsSP": True, "Renda Média": 8900, "População": 84400, "REGIC": "Capital Regional B", "Tabela Praticada": "Tabela 3", "A++": 0.02, "A+": 0.11, "B1": 0.18},
        {"Unidade": "FT RADIAL LESTE TATUAPÉ - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 15700, "População": 146400, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 4", "A++": 0.11, "A+": 0.19, "B1": 0.21},
        {"Unidade": "FT RECREIO - RJ", "Cidade": "Rio de Janeiro", "IsSP": False, "Renda Média": 22000, "População": 74360, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2", "A++": 0.16, "A+": 0.25, "B1": 0.24},
        {"Unidade": "FT RIO CLARO - SP", "Cidade": "Rio Claro", "IsSP": True, "Renda Média": 7400, "População": 72800, "REGIC": "Centro Sub-Regional I", "Tabela Praticada": "Tabela 1", "A++": 0.01, "A+": 0.04, "B1": 0.12},
        {"Unidade": "FT SALGADO FILHO - PR", "Cidade": "Curitiba", "IsSP": False, "Renda Média": 8900, "População": 64000, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2", "A++": 0.02, "A+": 0.08, "B1": 0.14},
        {"Unidade": "FT SALTO - SP", "Cidade": "Salto", "IsSP": True, "Renda Média": 6560, "População": 54900, "REGIC": "Centro Sub-Regional A", "Tabela Praticada": "Tabela 2", "A++": 0.01, "A+": 0.04, "B1": 0.10},
        {"Unidade": "FT SANTA LÚCIA - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 19400, "População": 88597, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3", "A++": 0.16, "A+": 0.24, "B1": 0.24},
        {"Unidade": "FT SANTA ROSA - RJ", "Cidade": "Niterói", "IsSP": False, "Renda Média": 17400, "População": 178510, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2", "A++": 0.11, "A+": 0.18, "B1": 0.24},
        {"Unidade": "FT SANTANA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 17700, "População": 153100, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.15, "A+": 0.22, "B1": 0.18},
        {"Unidade": "FT SANTO AMARO - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 21100, "População": 82400, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.17, "A+": 0.21, "B1": 0.22},
        {"Unidade": "FT SÃO BENTO - BH", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 16700, "População": 127317, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 2", "A++": 0.11, "A+": 0.22, "B1": 0.24},
        {"Unidade": "FT SÃO CAETANO - SP", "Cidade": "São Caetano do Sul", "IsSP": True, "Renda Média": 10200, "População": 122900, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 3", "A++": 0.04, "A+": 0.06, "B1": 0.19},
        {"Unidade": "FT SAÚDE - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 17700, "População": 186000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.13, "A+": 0.19, "B1": 0.21},
        {"Unidade": "FT SAUL MACEDO - MG", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 23100, "População": 63400, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3", "A++": 0.22, "A+": 0.26, "B1": 0.17},
        {"Unidade": "FT SAVASSI - MG", "Cidade": "Belo Horizonte", "IsSP": False, "Renda Média": 19885, "População": 192365, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3", "A++": 0.15, "A+": 0.27, "B1": 0.22},
        {"Unidade": "FT SETE LAGOAS - MG", "Cidade": "Sete Lagoas", "IsSP": False, "Renda Média": 12514, "População": 50760, "REGIC": "Capital Regional C", "Tabela Praticada": "Tabela 1", "A++": 0.09, "A+": 0.14, "B1": 0.16},
        {"Unidade": "FT SETOR BUENO - GO", "Cidade": "Goiânia", "IsSP": False, "Renda Média": 17800, "População": 94500, "REGIC": "Metrópole", "Tabela Praticada": "Tabela 3", "A++": 0.15, "A+": 0.24, "B1": 0.22},
        {"Unidade": "FT TAQUARAL - SP", "Cidade": "Campinas", "IsSP": True, "Renda Média": 12738, "População": 40203, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 3", "A++": 0.08, "A+": 0.14, "B1": 0.23},
        {"Unidade": "FT TIROL - RN", "Cidade": "Natal", "IsSP": False, "Renda Média": 15400, "População": 72800, "REGIC": "Capital Regional A", "Tabela Praticada": "Tabela 2", "A++": 0.11, "A+": 0.18, "B1": 0.24},
        {"Unidade": "FT TRÊS PODERES - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 18100, "População": 587000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.19, "A+": 0.18, "B1": 0.22},
        {"Unidade": "FT VERBO DIVINO - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 24800, "População": 77600, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.22, "A+": 0.23, "B1": 0.18},
        {"Unidade": "FT VILA OLIMPIA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 30900, "População": 160900, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.33, "A+": 0.26, "B1": 0.12},
        {"Unidade": "FT VILHENA - RO", "Cidade": "Vilhena", "IsSP": False, "Renda Média": 6100, "População": 42800, "REGIC": "Centro Sub-Regional", "Tabela Praticada": "Tabela 1", "A++": 0.03, "A+": 0.10, "B1": 0.17},
        {"Unidade": "FT YPIRANGA - SP", "Cidade": "São Paulo", "IsSP": True, "Renda Média": 19000, "População": 120000, "REGIC": "Grande Metrópole", "Tabela Praticada": "Tabela 5", "A++": 0.10, "A+": 0.17, "B1": 0.20}
    ]
    
    df_base = pd.DataFrame(df_existentes)
    
    if not df_base.empty:
        alvo_sp = (estado == "SP")
        df_filtrado = df_base[df_base['IsSP'] == alvo_sp].copy()
        
        if not df_filtrado.empty:
            r_ref = renda_media if renda_media > 0 else 1
            p_ref = populacao if populacao > 0 else 1
            a2_ref = classe_a_mais_mais if classe_a_mais_mais > 0 else 1
            a1_ref = classe_a_mais if classe_a_mais > 0 else 1
            b1_ref = classe_b1 if classe_b1 > 0 else 1
            
            # Cálculo da distância vetorial expandido
            df_filtrado['Distancia'] = np.sqrt(
                ((df_filtrado['Renda Média'] - renda_media) / r_ref)**2 + 
                ((df_filtrado['População'] - populacao) / p_ref)**2 +
                ((df_filtrado['A++'] - classe_a_mais_mais) / a2_ref)**2 +
                ((df_filtrado['A+'] - classe_a_mais) / a1_ref)**2 +
                ((df_filtrado['B1'] - classe_b1) / b1_ref)**2
            )
            
            # Conversão matemática de distância para percentual de similaridade
            df_filtrado['% Similaridade'] = df_filtrado['Distancia'].apply(
                lambda d: f"{max(0.0, min(100.0, (1 - d/(d+1.5)) * 100)):.1f}%"
            )
            
            # Ranking Top 3
            df_ranking = df_filtrado.sort_values(by='Distancia').head(3)
            
            st.dataframe(
                df_ranking[["Unidade", "Cidade", "Renda Média", "População", "REGIC", "Tabela Praticada", "% Similaridade"]], 
                use_container_width=True, 
                hide_index=True
            )
        else:
            st.info("Nenhuma unidade encontrada nessa região para comparação.")
    else:
        st.info("Nenhuma unidade cadastrada na base de dados.")

    st.markdown("""<div style="background-color:#FFF8E1; border-left:5px solid #FFB300; padding:15px; border-radius:4px; font-size:13px; color:#5D4037; margin-top:30px;">💡 <b>Governança:</b> O simulador é um direcionador estratégico. Decisões finais cabem ao Comitê de Expansão.</div>""", unsafe_allow_html=True)
