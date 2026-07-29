import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página corporativa da Fast Tennis
st.set_page_config(page_title="Fast Tennis - Plataforma Estratégica de Precificação", layout="wide")

# ==========================================
# APLICAÇÃO DA IDENTIDADE VISUAL FAST TENNIS (GUIDELINE 2025)
# Paleta Oficial: Blue FT (#053CD8), Navy FT (#022D8A), Green FT (#0DF205), Black (#000000)
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
        
        /* Botões Green FT (#0DF205) */
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
        st.error("Credenciais inválidas.")

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
        st.button("Entrar", on_click=realizar_login, use_container_width=True)
    st.stop()

# ==========================================
# LISTA DE UNIDADES OFICIAS
# ==========================================
UNIDADES_REDE = [
    "Selecione...", "Fast Tennis Aguas Claras - Brasilia", "Fast Tennis Alphaville - São Paulo", "Fast Tennis Alto da Boa Vista - São Paulo",
    "Fast Tennis Alto de Pinheiros - São Paulo", "Fast Tennis Alto do Ipiranga - São Paulo", "Fast Tennis Anhanguera - Jundiaí",
    "Fast Tennis Bebedouro - Bebedouro", "Fast Tennis Belvedere - Belo Horizonte", "Fast Tennis Boa Viagem - Recife",
    "Fast Tennis Botafogo - Campinas", "Fast Tennis Brooklin - São Paulo", "Fast Tennis Buritis I - Belo Horizonte",
    "Fast Tennis Buritis II - Belo Horizonte", "Fast Tennis Calafate - Belo Horizonte", "Fast Tennis Campo Belo - São Paulo",
    "Fast Tennis Cantareira - São Paulo", "Fast Tennis Capim Macio - Natal", "Fast Tennis Castelo - Belo Horizonte",
    "Fast Tennis Centro São Bernardo - São Bernardo do Campo", "Fast Tennis Chácara Inglesa - São Paulo", "Fast Tennis Chácara Santo Antônio - São Paulo",
    "Fast Tennis Cidade Nova - Cidade Nova", "Fast Tennis Contagem - Contagem", "Fast Tennis Estoril - Belo Horizonte",
    "Fast Tennis Estrela Sul - Juiz de Fora", "Fast Tennis Eusébio - Eusébio", "Fast Tennis General Lecor - São Paulo",
    "Fast Tennis Guararapes - Fortaleza", "Fast Tennis Indaiatuaba - São Paulo", "Fast Tennis Interlagos - São Paulo",
    "Fast Tennis Jardim - São Paulo", "Fast Tennis Jardim Portal da Colina - Sorocaba", "Fast Tennis Jardim Social - Curitiba",
    "Fast Tennis Lapa - São Paulo", "Fast Tennis Moema - São Paulo", "Fast Tennis Monte Pascal - São Paulo",
    "Fast Tennis Mooca - São Paulo", "Fast Tennis Morada da Colina - Uberlândia", "Fast Tennis Morumbi - São Paulo",
    "Fast Tennis Nova Aliança Sul - Ribeirão Preto", "Fast Tennis Orla da Pampulha - Belo Horizonte", "Fast Tennis Pampulha - Belo Horizonte",
    "Fast Tennis Parque Piqueri - São Paulo", "Fast Tennis Ponte JK - Brasília", "Fast Tennis Praia do Canto - Vitória",
    "Fast Tennis Praia Grande - Praia Grande", "Fast Tennis Radial Leste - São Paulo", "Fast Tennis Recreio - Rio de Janeiro",
    "Fast Tennis Rio Claro - São Paulo", "Fast Tennis Salgado Filho - Curitiba", "Fast Tennis Salto - São Paulo",
    "Fast Tennis Santa Lúcia - Belo Horizonte", "Fast Tennis Santana - São Paulo", "Fast Tennis Santa Rosa - Niterói",
    "Fast Tennis Santo Amaro", "Fast Tennis São Bento - Belo Horizonte", "Fast Tennis São Caetano - São Caetano do Sul",
    "Fast Tennis Saúde - São Paulo", "Fast Tennis Saul Macedo - Belo Horizonte", "Fast Tennis Savassi - Belo Horizonte",
    "Fast Tennis Sete Lagoas - Sete Lagoas", "Fast Tennis Setor Bueno - Goiânia", "Fast Tennis Taquaral - Campinas",
    "Fast Tennis Tirol - Natal", "Fast Tennis Três Poderes - São Paulo", "Fast Tennis Verbo Divino - São Paulo",
    "Fast Tennis Vila Olímpia - São Paulo", "Fast Tennis Vila Sônia", "Fast Tennis Vilhena - Rondônia", "Fast Tennis Ypiranga - São Paulo"
]

# TABELAS DE REFERÊNCIA OFICIAIS FAST TENNIS
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
    st.markdown("<p style='color:#FFFFFF; font-weight:700;'>Navegação da Plataforma</p>", unsafe_allow_html=True)
    
    modulo_selecionado = st.radio(
        "Selecione a Ferramenta:",
        ["1. Simulador de Precificação Inicial", "2. Reavaliação de Unidades Ativas"],
        key="modulo_navegacao"
    )
    
    st.markdown("---")
    st.markdown(f"<small style='color:#FFFFFF;'>Usuário: <b>{st.session_state['usuario_logado']}</b></small>", unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
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
    st.markdown("<p style='font-size:13.5px; color:#5A6578; margin-bottom:15px;'>Os dados imputados abaixo devem ser retirados da área de estudo delimitada no Geofusion.</p>", unsafe_allow_html=True)

    with st.expander("Diretrizes Geofusion (Clique para ver)"):
        st.markdown("Instruções de raio de 2km, PEA Dia e vocação de praça conforme manual de expansão.")

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
            st.markdown("**Percentuais de Classes (Geofusion)**")
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
            st.markdown("**Mercado e Vocação Local**")
            tipo_praca = st.selectbox("Perfil da Praça:", ["Selecione...", "Comercial", "Mista", "Residencial", "Mista Qualificada"], key="val_tipo_praca")
            renda_media = st.number_input("Renda Média (R$):", min_value=0.0, step=100.0, key="val_renda_media")
            tempo_proxima = st.number_input("Tempo até unidade próxima (min):", min_value=0, step=1, key="val_tempo_proxima")
            media_mercado = st.number_input("Preço Médio dos Concorrentes (Plano Plus 1x / Grupo):", min_value=0.0, step=10.0, key="val_media_mercado")

        st.write("")
        col_btn1, col_btn2 = st.columns([5, 1])
        with col_btn2:
            st.button("Limpar Simulação", on_click=limpar_campos_m1, use_container_width=True)

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
        st.info("Aguardando dados. Por favor, preencha as informações da Área de Estudo acima para gerar a análise.")
    else:
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
        
        st.markdown('<div class="faixa-resultados">Análise de Dados e Recomendações</div>', unsafe_allow_html=True)

        preco_sugerido = precos[tabela_sugerida]
        tkm_sugerido = tkms[tabela_sugerida]

        st.markdown(f"""
            <div class="tabela-sugerida-box">
                <p style="margin:0; font-size:11px; color:#6C757D; font-weight:bold; text-transform:uppercase;">Tabela Sugerida pelo Algoritmo (Perfil Econômico)</p>
                <h2>Tabela {tabela_sugerida}</h2>
                <p style="margin:0; font-size:14px; color:#2D3748;">Preço Ref. Plano Plus 1x: <b>R$ {preco_sugerido},00</b> | TKM Técnico: <b>R$ {tkm_sugerido},00</b></p>
            </div>
        """, unsafe_allow_html=True)

        aplicar_excecao = st.checkbox("Ativar exceção técnica (Sobrevir tabela baseada no comportamento de mercado além dos dados)", key="chk_excecao")

        justificativa_excecao = ""
        if aplicar_excecao:
            col_exc1, col_exc2 = st.columns([1, 2])
            with col_exc1:
                tabela_escolhida = st.selectbox("Selecione a Tabela Definitiva:", [1, 2, 3, 4, 5], index=tabela_sugerida - 1, key="val_tabela_excecao")
            with col_exc2:
                justificativa_excecao = st.text_input("Justificativa da Exceção (Obrigatório):", placeholder="Ex: Concorrência local com forte posicionamento premium...", key="val_justificativa_excecao")

            tabela_final = tabela_escolhida
            st.markdown(f"""
                <div class="tabela-excecao-box">
                    <p style="margin:0; font-size:11px; color:#166534; font-weight:bold; text-transform:uppercase;">Tabela Escolhida por Decisão Técnica (Exceção)</p>
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
            st.markdown('<div class="alerta-fino">Proteção de Rede: Existe unidade próxima em raio inferior a 15 minutos. Verificar compatibilidade de tabelas.</div>', unsafe_allow_html=True)

        st.markdown(f"<small style='color:#6C757D;'>Intervalo de tabelas possíveis calculado:</small> <b>Tab {tab_min} a {tab_max}</b>", unsafe_allow_html=True)
        
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
        with st.expander("📄 Relatório Oficial de Simulação (Para E-mail, PDF e Comitê)", expanded=False):
            st.info("Você pode copiar o código HTML ou clicar no botão verde para gerar e imprimir o PDF oficial da simulação.")
            
            modo_definicao = f"Exceção Técnica ({justificativa_excecao})" if aplicar_excecao else "Análise de Dados do Algoritmo"
            
            info_tabela_economica = ""
            if aplicar_excecao:
                info_tabela_economica = f"""
                <p style="margin:4px 0 0 0; font-size:12px; color:#E2E8F0;">
                    Tabela Sugerida pelo Perfil Econômico (Algoritmo): <b>Tabela {tabela_sugerida}</b> (Ref: R$ {preco_sugerido},00)
                </p>
                """

            html_relatorio = f"""
            <div id="print-area" style="font-family: Arial, sans-serif; background: #ffffff; padding: 25px; border: 2px solid #022D8A; border-radius: 8px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="color:#022D8A; margin:0;">Fast Tennis - Relatório de Precificação Estratégica</h2>
                    <span style="font-size:12px; color:#6C757D;">Comitê de Expansão</span>
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

                <button onclick="window.print()" style="background-color: #0DF205; color: #022D8A; border: none; padding: 10px 20px; font-weight: bold; border-radius: 20px; cursor: pointer;">
                    Imprimir / Salvar PDF
                </button>
            </div>
            """
            st.components.v1.html(html_relatorio, height=560, scrolling=True)

# ==============================================================================
# MÓDULO 2: REAVALIAÇÃO E REPRECIFICAÇÃO DE UNIDADES ATIVAS (CAMPOS LIMPOS E BASE DE UNIDADES)
# ==============================================================================
else:
    st.title("Reavaliação Estratégica de Precificação de Unidades Ativas")
    st.markdown("Diagnóstico contínuo e orientação de decisão baseada nos indicadores operacionais e de mercado.")
    st.markdown("---")

    def limpar_campos_m2():
        st.session_state["m2_nome_u"] = "Selecione..."
        st.session_state["m2_tab_ativa"] = "Selecione..."
        st.session_state["m2_tkm_real"] = 0.0
        st.session_state["m2_ll"] = 0.0
        st.session_state["m2_fat"] = 0.0
        st.session_state["m2_mix"] = "Selecione..."
        st.session_state["m2_objecoes"] = 0.0
        st.session_state["m2_conv_u"] = 0.0
        st.session_state["m2_lead_u"] = 0.0
        st.session_state["m2_churn_u"] = 0.0
        st.session_state["m2_cres_base"] = "Selecione..."
        st.session_state["m2_vendedor"] = "Selecione..."
        st.session_state["m2_conc_p"] = 0.0
        st.session_state["m2_renda_u"] = 0.0
        st.session_state["m2_pop_u"] = 0
        st.session_state["m2_alvo_u"] = 0.0
        st.session_state["m2_med_conv"] = 0.0
        st.session_state["m2_med_lead"] = 0.0
        st.session_state["m2_med_churn"] = 0.0

    if "m2_nome_u" not in st.session_state:
        limpar_campos_m2()

    # 1. MÉDIAS GLOBAIS DA REDE
    st.subheader("1. Parâmetros Médios da Rede Fast Tennis")
    with st.container(border=True):
        mr1, mr2, mr3 = st.columns(3)
        with mr1:
            media_rede_conversao = st.number_input("% Conversão Médio Rede:", min_value=0.0, step=0.5, key="m2_med_conv")
        with mr2:
            media_rede_lead_conect = st.number_input("% Lead Conectado Médio Rede:", min_value=0.0, step=0.5, key="m2_med_lead")
        with mr3:
            media_rede_churn = st.number_input("% Churn Médio Rede:", min_value=0.0, step=0.1, key="m2_med_churn")

    st.write("")
    # 2. DADOS DA UNIDADE AVALIADA
    st.subheader("2. Desempenho Operacional e Comercial da Unidade")
    with st.container(border=True):
        u1, u2, c_merc = st.columns(3)
        
        with u1:
            st.markdown("**Indicadores Financeiros & Comerciais**")
            nome_unidade = st.selectbox("Unidade:", UNIDADES_REDE, key="m2_nome_u")
            tabela_ativa = st.selectbox("Tabela Praticada Atualmente:", ["Selecione...", 1, 2, 3, 4, 5], key="m2_tab_ativa")
            
            if tabela_ativa != "Selecione...":
                tkm_esperado_rede = TABELAS_OFICIAIS[tabela_ativa]["tkm"]
                preco_plus_esperado = TABELAS_OFICIAIS[tabela_ativa]["plus"]
                st.caption(f"TKM Esperado: **R$ {tkm_esperado_rede},00** | Plano Plus 1x: **R$ {preco_plus_esperado},00**")
            else:
                tkm_esperado_rede = 0
                preco_plus_esperado = 0

            tkm_real_unidade = st.number_input("TKM Real Praticado (R$):", min_value=0.0, step=5.0, key="m2_tkm_real")
            atingimento_ll = st.number_input("% Atingimento Meta Lucro Líquido (LL):", min_value=0.0, step=1.0, key="m2_ll")
            atingimento_fat = st.number_input("% Atingimento Meta Faturamento:", min_value=0.0, step=1.0, key="m2_fat")

        with u2:
            st.markdown("**Comportamento de Vendas e Base**")
            mix_produtos = st.selectbox("Mix de Produtos:", ["Selecione...", "Consumo Plus saudável ou acima do esperado", "Smart acima do Plus em até 8% e 15%", "Smart acima do Plus em mais de 15%"], key="m2_mix")
            objecoes_preco = st.number_input("% Objeções por Preço:", min_value=0.0, step=1.0, key="m2_objecoes")
            conversao_unidade = st.number_input("% Conversão da Unidade:", min_value=0.0, step=0.5, key="m2_conv_u")
            lead_conect_unidade = st.number_input("% Lead Conectado da Unidade:", min_value=0.0, step=0.5, key="m2_lead_u")
            churn_unidade = st.number_input("% Churn da Unidade:", min_value=0.0, step=0.1, key="m2_churn_u")

        with c_merc:
            st.markdown("**Base, Equipe e Mercado Local**")
            crescimento_base = st.selectbox("Crescimento da Base:", ["Selecione...", "Crescimento saudável e consistente", "Oscilação", "Crescimento estagnado"], key="m2_cres_base")
            perfil_vendedor = st.selectbox("Perfil do Vendedor:", ["Selecione...", "Vendedor de alta performance", "Necessidade de desenvolvimento", "Vendedor desalinhado"], key="m2_vendedor")
            preco_concorrentes = st.number_input("Preço Médio Concorrentes (R$):", min_value=0.0, step=10.0, key="m2_conc_p")
            renda_media_u = st.number_input("Renda Média Região (R$):", min_value=0.0, step=500.0, key="m2_renda_u")
            populacao_u = st.number_input("População Residente:", min_value=0, step=1000, key="m2_pop_u")
            pct_alvo_u = st.number_input("% Público Alvo (B1+A+ A++):", min_value=0.0, step=1.0, key="m2_alvo_u")

        st.write("")
        col_btn_m2_1, col_btn_m2_2 = st.columns([5, 1])
        with col_btn_m2_2:
            st.button("Limpar Campos", on_click=limpar_campos_m2, use_container_width=True)

    # VALIDAÇÃO DOS DADOS DO MÓDULO 2
    pronto_m2 = (
        nome_unidade != "Selecione..." and
        tabela_ativa != "Selecione..." and
        mix_produtos != "Selecione..." and
        crescimento_base != "Selecione..." and
        perfil_vendedor != "Selecione..." and
        media_rede_conversao > 0 and
        media_rede_lead_conect > 0 and
        media_rede_churn > 0
    )

    if not pronto_m2:
        st.info("Aguardando dados. Preencha as informações operacionais e de mercado acima para gerar o relatório estratégico.")
    else:
        # ==========================================
        # 3. MOTOR DE AVALIAÇÃO E MATRIZ DE DIAGNÓSTICO
        # ==========================================
        st.write("")
        st.markdown('<div class="faixa-resultados">Matriz de Orientação da Decisão</div>', unsafe_allow_html=True)
        
        matriz_sinais = []

        # 1. Lucro Líquido
        if atingimento_ll >= 90.0: s_ll = "Positivo"
        elif atingimento_ll >= 80.0: s_ll = "Atenção"
        else: s_ll = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "Lucro Líquido", "Dados Unidade": f"{atingimento_ll:.1f}% meta", "Sinal": s_ll})

        # 2. Faturamento
        if atingimento_fat >= 90.0: s_fat = "Positivo"
        elif atingimento_fat >= 80.0: s_fat = "Atenção"
        else: s_fat = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "Faturamento", "Dados Unidade": f"{atingimento_fat:.1f}% meta", "Sinal": s_fat})

        # 3. Mix de Produtos
        if "saudável" in mix_produtos: s_mix = "Positivo"
        elif "8% e 15%" in mix_produtos: s_mix = "Atenção"
        else: s_mix = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "Mix de Produtos", "Dados Unidade": mix_produtos, "Sinal": s_mix})

        # 4. Objeções por Preço
        if objecoes_preco <= 10.0: s_obj = "Positivo"
        elif objecoes_preco <= 25.0: s_obj = "Atenção"
        else: s_obj = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "Objeções por Preço", "Dados Unidade": f"{objecoes_preco:.1f}%", "Sinal": s_obj})

        # 5. Conversão
        if conversao_unidade >= media_rede_conversao: s_conv = "Positivo"
        elif conversao_unidade >= (media_rede_conversao * 0.90): s_conv = "Atenção"
        else: s_conv = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "Conversão", "Dados Unidade": f"{conversao_unidade:.1f}% (Rede: {media_rede_conversao:.1f}%)", "Sinal": s_conv})

        # 6. % Lead Conectado
        if lead_conect_unidade >= media_rede_lead_conect: s_lead = "Positivo"
        elif lead_conect_unidade >= (media_rede_lead_conect * 0.90): s_lead = "Atenção"
        else: s_lead = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "% Lead Conectado", "Dados Unidade": f"{lead_conect_unidade:.1f}% (Rede: {media_rede_lead_conect:.1f}%)", "Sinal": s_lead})

        # 7. TKM
        if tkm_real_unidade >= tkm_esperado_rede: s_tkm = "Positivo"
        elif tkm_real_unidade >= (tkm_esperado_rede * 0.90): s_tkm = "Atenção"
        else: s_tkm = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "TKM Praticado", "Dados Unidade": f"R$ {tkm_real_unidade:.0f} (Esp: R$ {tkm_esperado_rede})", "Sinal": s_tkm})

        # 8. Crescimento de Base
        if "saudável" in crescimento_base: s_base = "Positivo"
        elif "Oscilação" in crescimento_base: s_base = "Atenção"
        else: s_base = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "Crescimento de Base", "Dados Unidade": crescimento_base, "Sinal": s_base})

        # 9. % de Churn
        if churn_unidade <= media_rede_churn: s_churn = "Positivo"
        elif churn_unidade <= (media_rede_churn * 1.15): s_churn = "Atenção"
        else: s_churn = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "% de Churn", "Dados Unidade": f"{churn_unidade:.1f}% (Rede: {media_rede_churn:.1f}%)", "Sinal": s_churn})

        # 10. Perfil Vendedor
        if "alta performance" in perfil_vendedor: s_vend = "Positivo"
        elif "desenvolvimento" in perfil_vendedor: s_vend = "Atenção"
        else: s_vend = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "Perfil Vendedor", "Dados Unidade": perfil_vendedor, "Sinal": s_vend})

        # 11. Pesquisa de Mercado
        dif_conc = (preco_plus_esperado - preco_concorrentes) / preco_concorrentes if preco_concorrentes > 0 else 0
        if abs(dif_conc) <= 0.10: s_merc = "Positivo"
        elif abs(dif_conc) <= 0.20: s_merc = "Atenção"
        else: s_merc = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "Pesquisa de Mercado", "Dados Unidade": f"Dif. {dif_conc*100:+.1f}% vs Mercado", "Sinal": s_merc})

        # 12. Potencial da Região
        if renda_media_u >= 15000 and pct_alvo_u >= 35: s_pot = "Positivo"
        elif renda_media_u >= 11000 and pct_alvo_u >= 25: s_pot = "Atenção"
        else: s_pot = "Crítico"
        matriz_sinais.append({"Critério Avaliado": "Potencial da Região", "Dados Unidade": f"R$ {renda_media_u:,.0f} | {pct_alvo_u:.1f}% Alvo", "Sinal": s_pot})

        # CONTAGEM DE SINAIS
        df_sinais = pd.DataFrame(matriz_sinais)
        qtd_positivos = sum(1 for x in matriz_sinais if x["Sinal"] == "Positivo")
        qtd_atencao = sum(1 for x in matriz_sinais if x["Sinal"] == "Atenção")
        qtd_criticos = sum(1 for x in matriz_sinais if x["Sinal"] == "Crítico")
        total_indicadores = len(matriz_sinais)
        pct_positivos = (qtd_positivos / total_indicadores) * 100

        # MATRIZ EXECUTIVA UNIFICADA
        st.dataframe(df_sinais, use_container_width=True, hide_index=True)

        # RESUMO EXECUTIVO LOGO ABAIXO DA MATRIZ
        st.markdown(f"""
            <div style="background-color:#F8F9FA; border:1px solid #E2E8F0; padding:12px 20px; border-radius:8px; margin-top:10px; display:flex; justify-content:space-around;">
                <span style="font-size:14px;">Positivos: <b style="color:#15803D;">{qtd_positivos} ({pct_positivos:.1f}%)</b></span>
                <span style="font-size:14px;">Atenção: <b style="color:#A16207;">{qtd_atencao}</b></span>
                <span style="font-size:14px;">Críticos: <b style="color:#B91C1C;">{qtd_criticos}</b></span>
            </div>
        """, unsafe_allow_html=True)

        # RELATÓRIO ESTRATÉGICO CORPORATIVO
        st.write("")
        st.subheader("3. Relatório Estratégico de Posicionamento")

        indicio_desalinhamento = (s_obj == "Crítico" and s_conv == "Crítico" and "mais de 15%" in mix_produtos)

        if pct_positivos >= 70.0:
            rec_pop = "<b>Tendência de Aumento ou Manutenção Premium</b>: Unidade altamente saudável. Tabela aderente ao perfil do público com oportunidade de elevação em Comitê de Expansão."
            cor_pop = "#166534"
            bg_pop = "#F0FDF4"
        elif qtd_criticos >= 3:
            rec_pop = "<b>Reavaliação de Posicionamento / Redução de Tabela</b>: Concentração de indicadores críticos. Recomendada análise de reposicionamento e estratégias promocionais controladas."
            cor_pop = "#991B1B"
            bg_pop = "#FEF2F2"
        else:
            rec_pop = "<b>Ajuste Operacional Sem Alteração Imidiatada de Preço</b>: Cenário intermediário. Foco na correção dos processos comerciais e equipe antes de alterar a tabela."
            cor_pop = "#975A16"
            bg_pop = "#FFFDF5"

        st.markdown(f"""
            <div style="background-color:{bg_pop}; border-left:6px solid {cor_pop}; padding:18px; border-radius:8px; margin-bottom:15px;">
                <p style="margin:0; font-size:11px; color:{cor_pop}; font-weight:bold; text-transform:uppercase;">Diretriz Estratégica</p>
                <p style="margin:6px 0 0 0; font-size:15px; color:#2D3748;">{rec_pop}</p>
                {f'<p style="margin:8px 0 0 0; font-size:13px; color:#B91C1C;"><b>Alerta Técnico:</b> Identificado indício de desalinhamento de tabela (Alta sensibilidade a preço + Baixa conversão + Concentração no plano Smart).</p>' if indicio_desalinhamento else ''}
            </div>
        """, unsafe_allow_html=True)
