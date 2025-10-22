
# ============================================================
# DASHBOARD BH - TRANSPORTE E ECONOMIA
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Dashboard BH",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {padding: 0rem 1rem;}
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {color: #1f77b4;}
    </style>
""", unsafe_allow_html=True)

# ============================================================
# CARREGAR DADOS
# ============================================================

@st.cache_data
def carregar_dados():
    """Carrega todos os dados necessários"""
    try:
        df_bairros = pd.read_csv('raw_data/20230502_bairro_oficial.csv', delimiter=',')
        df_economia = pd.read_csv('raw_data/20240926_atividade_economica.csv', delimiter=';')
        df_onibus = pd.read_csv('raw_data/20240902_ponto_onibus.csv', delimiter=';')
        return df_bairros, df_economia, df_onibus
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None, None

df_bairros, df_economia, df_onibus = carregar_dados()

# Verificar se dados foram carregados
if df_bairros is None:
    st.stop()

# ============================================================
# SIDEBAR - NAVEGAÇÃO
# ============================================================

with st.sidebar:
    st.title("🏙️ Dashboard BH")
    st.markdown("---")

    pagina = st.radio(
        "Navegação",
        ["🏠 Visão Geral", 
         "💼 Análise Econômica", 
         "🚌 Análise de Transporte",
         "🎯 Classificação de Bairros",
         "🗺️ Mapas Interativos",
         "📊 Dados Brutos"]
    )

    st.markdown("---")
    st.markdown("### 📌 Sobre")
    st.info("""
    **Projeto:** Análise Espacial BH  
    **Dados:** 2023-2025  
    **Tech:** Python, GeoPandas, Streamlit
    """)

# ============================================================
# PÁGINA 1: VISÃO GERAL
# ============================================================

if pagina == "🏠 Visão Geral":
    st.title("🏙️ Dashboard Executivo - Belo Horizonte")
    st.markdown("### Análise de Transporte Público e Desenvolvimento Econômico")
    st.markdown("---")

    # MÉTRICAS PRINCIPAIS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🏘️ Bairros",
            value=f"{len(df_bairros):,}",
            delta="100% cobertura"
        )

    with col2:
        st.metric(
            label="💼 Empresas",
            value=f"{len(df_economia):,}",
            delta="512 mil"
        )

    with col3:
        st.metric(
            label="🚌 Pontos Ônibus",
            value=f"{len(df_onibus):,}",
            delta="47 mil"
        )

    with col4:
        total_meis = (df_economia['IND_MEI'] == 'S').sum()
        perc_mei = (total_meis / len(df_economia)) * 100
        st.metric(
            label="🎯 MEIs",
            value=f"{perc_mei:.1f}%",
            delta=f"{total_meis:,} empresas"
        )

    st.markdown("---")

    # PRINCIPAIS INSIGHTS
    st.markdown("### 🔍 Principais Descobertas")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 📊 Correlação Transporte × Economia
        - **Coeficiente de Pearson:** 0.505
        - **Interpretação:** Correlação MODERADA e POSITIVA
        - **Conclusão:** Bairros com mais transporte TENDEM a ter mais empresas

        #### 💼 Perfil Empreendedor
        - **62.7%** das empresas são MEIs
        - **270.788 microempreendedores** ativos
        - BH é uma cidade **altamente empreendedora**
        """)

    with col2:
        st.markdown("""
        #### 🎯 Setores Predominantes
        1. **Cabeleireiros/Manicure:** 21.976 empresas
        2. **Condomínios Prediais:** 21.748 empresas
        3. **Promoção de Vendas:** 18.036 empresas

        #### 🗺️ Classificação de Bairros
        - 🟢 **30% Bem Desenvolvidos** (96 bairros)
        - 🟡 **20% Oportunidades** (64 bairros) ⭐
        - 🟠 **20% Potencial** (64 bairros)
        - 🔴 **30% Prioridade** (96 bairros)
        """)

    st.markdown("---")

    # GRÁFICO: TOP 10 BAIRROS
    st.markdown("### 🏆 Top 10 Bairros por Número de Empresas")

    top10_bairros = df_economia['NOME_BAIRRO'].value_counts().head(10)

    fig = px.bar(
        x=top10_bairros.values,
        y=top10_bairros.index,
        orientation='h',
        labels={'x': 'Número de Empresas', 'y': 'Bairro'},
        color=top10_bairros.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PÁGINA 2: ANÁLISE ECONÔMICA
# ============================================================

elif pagina == "💼 Análise Econômica":
    st.title("💼 Análise Econômica Detalhada")
    st.markdown("---")

    # FILTROS
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown("### 🔍 Filtros")

        tipo_mei = st.radio(
            "Tipo de Empresa",
            ["Todas", "Apenas MEIs", "Apenas Não-MEIs"]
        )

        top_bairros = df_economia['NOME_BAIRRO'].value_counts().head(20).index.tolist()
        bairro_selecionado = st.selectbox(
            "Selecione um Bairro",
            ["Todos"] + top_bairros
        )

    # Aplicar filtros
    df_filtrado = df_economia.copy()

    if tipo_mei == "Apenas MEIs":
        df_filtrado = df_filtrado[df_filtrado['IND_MEI'] == 'S']
    elif tipo_mei == "Apenas Não-MEIs":
        df_filtrado = df_filtrado[df_filtrado['IND_MEI'] == 'N']

    if bairro_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['NOME_BAIRRO'] == bairro_selecionado]

    with col2:
        col_m1, col_m2, col_m3 = st.columns(3)

        with col_m1:
            st.metric("Total Empresas", f"{len(df_filtrado):,}")

        with col_m2:
            total_meis_filt = (df_filtrado['IND_MEI'] == 'S').sum()
            st.metric("MEIs", f"{total_meis_filt:,}")

        with col_m3:
            perc_mei_filt = (total_meis_filt / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
            st.metric("% MEIs", f"{perc_mei_filt:.1f}%")

    st.markdown("---")

    # GRÁFICOS
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Top 10 CNAEs Mais Comuns")
        top_cnaes = df_filtrado['DESCRICAO_CNAE_PRINCIPAL'].value_counts().head(10)

        fig = px.bar(
            x=top_cnaes.values,
            y=[desc[:40] + "..." if len(desc) > 40 else desc for desc in top_cnaes.index],
            orientation='h',
            labels={'x': 'Quantidade', 'y': 'Atividade'},
            color=top_cnaes.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🥧 Distribuição MEI vs Não-MEI")

        mei_counts = df_filtrado['IND_MEI'].value_counts()

        fig = go.Figure(data=[go.Pie(
            labels=['MEI', 'Não-MEI'],
            values=[mei_counts.get('S', 0), mei_counts.get('N', 0)],
            hole=.4,
            marker_colors=['#2ecc71', '#e74c3c']
        )])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PÁGINA 3: ANÁLISE DE TRANSPORTE
# ============================================================

elif pagina == "🚌 Análise de Transporte":
    st.title("🚌 Análise de Transporte Público")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_linhas = df_onibus['COD_LINHA'].nunique()
        st.metric("🚌 Linhas de Ônibus", f"{total_linhas:,}")

    with col2:
        total_pontos = len(df_onibus)
        st.metric("📍 Pontos de Ônibus", f"{total_pontos:,}")

    with col3:
        media_pontos = total_pontos / total_linhas
        st.metric("📊 Média Pontos/Linha", f"{media_pontos:.1f}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Top 15 Linhas com Mais Pontos")
        top_linhas = df_onibus.groupby('NOME_LINHA').size().sort_values(ascending=False).head(15)

        fig = px.bar(
            x=top_linhas.values,
            y=[nome[:35] + "..." if len(nome) > 35 else nome for nome in top_linhas.index],
            orientation='h',
            labels={'x': 'Número de Pontos', 'y': 'Linha'},
            color=top_linhas.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 Distribuição por Origem")
        origem_counts = df_onibus['ORIGEM'].value_counts().head(10)

        fig = px.pie(
            values=origem_counts.values,
            names=origem_counts.index
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PÁGINA 4: CLASSIFICAÇÃO DE BAIRROS
# ============================================================

elif pagina == "🎯 Classificação de Bairros":
    st.title("🎯 Matriz de Classificação de Bairros")
    st.markdown("---")

    st.markdown("""
    ### 📊 Metodologia

    Bairros classificados em 4 categorias baseadas em:
    - **Eixo X:** Densidade de Transporte (pontos de ônibus/km²)
    - **Eixo Y:** Densidade Econômica (empresas/km²)
    - **Limiar:** Mediana de cada métrica
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        ### 🟢 BEM DESENVOLVIDO
        **96 bairros (30%)**

        Alta economia +  
        Alto transporte

        **Ação:** Manter
        """)

    with col2:
        st.markdown("""
        ### 🟡 OPORTUNIDADE
        **64 bairros (20%)** ⭐

        Alta economia +  
        Baixo transporte

        **Ação:** INVESTIR!
        """)

    with col3:
        st.markdown("""
        ### 🟠 POTENCIAL
        **64 bairros (20%)**

        Baixa economia +  
        Alto transporte

        **Ação:** Incentivar
        """)

    with col4:
        st.markdown("""
        ### 🔴 PRIORIDADE
        **96 bairros (30%)**

        Baixa economia +  
        Baixo transporte

        **Ação:** URGENTE!
        """)

    st.markdown("---")

    st.markdown("### 🟡 TOP 10 OPORTUNIDADES (investir em transporte)")

    # Dados fictícios baseados nos seus resultados
    exemplos_oport = {
        'Bairro': ['Buritis', 'Castelo', 'Santa Lúcia', 'Lindéia', 'Sagrada Família',
                   'Itatiaia', 'São João Batista', 'Coqueiros', 'Jardim Leblon', 'João Pinheiro'],
        'Empresas': [6855, 6653, 4281, 3995, 3988, 3881, 3468, 3020, 2897, 2814],
        'Dens.Econ': [2332, 2765, 1808, 1975, 3087, 2141, 1842, 1960, 2119, 1878],
        'Dens.Trans': [75, 90, 136, 50, 135, 123, 109, 100, 118, 126]
    }

    df_oport = pd.DataFrame(exemplos_oport)
    st.dataframe(df_oport, use_container_width=True)

# ============================================================
# PÁGINA 5: MAPAS INTERATIVOS
# ============================================================

elif pagina == "🗺️ Mapas Interativos":
    st.title("🗺️ Mapas Interativos")
    st.markdown("---")

    st.markdown("### 📍 Visualizações Geoespaciais")

    mapa_opcao = st.selectbox(
        "Escolha o mapa",
        ["Classificação de Bairros (4 categorias)", "Densidade Econômica"]
    )

    arquivo_map = {
        "Classificação de Bairros (4 categorias)": "mapa_classificacao_bairros.html",
        "Densidade Econômica": "mapa_densidade_economica.html"
    }

    arquivo = arquivo_map[mapa_opcao]
    caminho = Path(f"mapas_exportados/{arquivo}")

    if caminho.exists():
        with open(caminho, 'r', encoding='utf-8') as f:
            html_content = f.read()

        st.components.v1.html(html_content, height=600, scrolling=True)

        st.download_button(
            label="📥 Download do Mapa (HTML)",
            data=html_content,
            file_name=arquivo,
            mime="text/html"
        )
    else:
        st.error(f"Arquivo não encontrado: {caminho}")
        st.info("Execute as células que geram os mapas primeiro!")

# ============================================================
# PÁGINA 6: DADOS BRUTOS
# ============================================================

elif pagina == "📊 Dados Brutos":
    st.title("📊 Exploração de Dados Brutos")
    st.markdown("---")

    dataset = st.selectbox(
        "Selecione o dataset",
        ["Bairros", "Empresas", "Pontos de Ônibus"]
    )

    if dataset == "Bairros":
        st.markdown(f"### 🏘️ Bairros ({len(df_bairros)} registros)")
        st.dataframe(df_bairros.head(100), use_container_width=True)

    elif dataset == "Empresas":
        st.markdown(f"### 💼 Empresas ({len(df_economia):,} registros)")

        busca = st.text_input("🔍 Buscar por nome fantasia ou CNAE")

        if busca:
            df_filtrado = df_economia[
                df_economia['NOME_FANTASIA'].str.contains(busca, case=False, na=False) |
                df_economia['DESCRICAO_CNAE_PRINCIPAL'].str.contains(busca, case=False, na=False)
            ]
            st.markdown(f"**{len(df_filtrado)} resultados encontrados**")
            st.dataframe(df_filtrado.head(100), use_container_width=True)
        else:
            st.dataframe(df_economia.head(100), use_container_width=True)

    elif dataset == "Pontos de Ônibus":
        st.markdown(f"### 🚌 Pontos de Ônibus ({len(df_onibus):,} registros)")
        st.dataframe(df_onibus.head(100), use_container_width=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Dashboard desenvolvido com Streamlit | Dados: Prefeitura de Belo Horizonte | 2023-2025</p>
</div>
""", unsafe_allow_html=True)
