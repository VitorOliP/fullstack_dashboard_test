import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import json

# CONFIGURAÇÃO GERAL

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

REGIOES = ["Brasil", "Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

COMPETENCIAS = {
    "Ciências da Natureza": "nota_cn",
    "Ciências Humanas": "nota_ch",
    "Linguagens e Códigos": "nota_lc",
    "Matemática": "nota_mt",
    "Redação": "nota_redacao"
}

st.set_page_config(
    page_title="Dashboard ENEM - Regiões",
    layout="wide"
)

st.title("📊 Análise por Região - ENEM 2023")

# SIDEBAR
with st.sidebar:
    regiao = st.selectbox("Selecione a região:", REGIOES)


# FUNÇÕES PARA CONSULTAR API
@st.cache_data(ttl=600)
def get_medias_regiao(regiao):
    response = requests.get(f"{API_BASE_URL}/regioes/medias/regiao/{regiao}")
    return response.json() if response.status_code == 200 else None

@st.cache_data(ttl=600)
def get_distribuicao_regiao(regiao):
    response = requests.get(f"{API_BASE_URL}/regioes/distribuicao/regiao/{regiao}")
    return response.json() if response.status_code == 200 else None

@st.cache_data(ttl=600)
def get_status_redacao(regiao):
    response = requests.get(f"{API_BASE_URL}/regioes/status_redacao/regiao/{regiao}")
    return response.json() if response.status_code == 200 else None

@st.cache_data(ttl=600)
def get_distribuicao_sexo(regiao):
    response = requests.get(f"{API_BASE_URL}/regioes/distribuicao-sexo/regiao/{regiao}")
    return response.json() if response.status_code == 200 else None

@st.cache_data(ttl=600)
def get_distribuicao_faixa(regiao):
    response = requests.get(f"{API_BASE_URL}/regioes/distribuicao-faixa-etaria/regiao/{regiao}")
    return response.json() if response.status_code == 200 else None

@st.cache_data(ttl=600)
def get_distribuicao_raca(regiao):
    response = requests.get(f"{API_BASE_URL}/regioes/distribuicao_raca/regiao/{regiao}")
    return response.json() if response.status_code == 200 else None

@st.cache_data(ttl=600)
def get_ausencia_renda(regiao):
    response = requests.get(f"{API_BASE_URL}/regioes/distribuicao_ausencia_renda/regiao/{regiao}")
    return response.json() if response.status_code == 200 else None

@st.cache_data(ttl=600)
def get_ausencia_faixa_etaria(regiao):
    response = requests.get(f"{API_BASE_URL}/regioes/distribuicao_ausencia_faixa_etaria/regiao/{regiao}")
    return response.json() if response.status_code == 200 else None

@st.cache_data(ttl=600)
def get_ausencia_raca(regiao):
    response = requests.get(f"{API_BASE_URL}/regioes/distribuicao_ausencia_raca/regiao/{regiao}")
    return response.json() if response.status_code == 200 else None

# DADOS PRINCIPAIS

with st.spinner("Carregando dados..."):
    medias = get_medias_regiao(regiao)
    dist = get_distribuicao_regiao(regiao)
    status_redacao = get_status_redacao(regiao)
    sexo = get_distribuicao_sexo(regiao)
    faixa = get_distribuicao_faixa(regiao)
    raca = get_distribuicao_raca(regiao)
    dados_ausencia_renda = get_ausencia_renda(regiao)
    dados_ausencia_faixa_etaria = get_ausencia_faixa_etaria(regiao)
    dados_ausencia_raca = get_ausencia_raca(regiao)

if medias is None or dist is None:
    st.error("Não foi possível carregar os dados.")
else:
    # Métricas
    st.subheader(f"Médias das Notas - {regiao}")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Ciências da Natureza", f"{medias['media_cn']}")
    col2.metric("Ciências Humanas", f"{medias['media_ch']}")
    col3.metric("Linguagens e Códigos", f"{medias['media_lc']}")
    col4.metric("Matemática", f"{medias['media_mt']}")
    col5.metric("Redação", f"{medias['media_redacao']}")
    style_metric_cards(border_left_color="#ff6200", border_color="#6B6B6B", background_color="#FFFFFF")

    st.divider()

    # Gráfico de distribuição
    competencia = st.selectbox("Selecione a área de conhecimento:", list(COMPETENCIAS.keys()))
    st.subheader(f"Distribuição das Notas - {regiao} ({competencia})")
    df = pd.DataFrame(dist)
    nota_col = COMPETENCIAS[competencia]

    fig = px.histogram(
        df,
        x=nota_col,
        nbins=30,
        title=competencia,
        labels={nota_col: "Nota"},
        color_discrete_sequence=['#000d3c']
    )
    fig.update_layout(
        bargap=0.1,
        xaxis_title="Nota",
        yaxis_title="Frequência",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111111"),
        title=dict(font=dict(size=18, color="#111111"))
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e0e0e0", color="#111111")
    fig.update_yaxes(showgrid=True, gridcolor="#e0e0e0", color="#111111")

    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
    if competencia == "Redação" and regiao != "Brasil":
        st.subheader(f"Distribuição do Status das Redações - {regiao}")
        if status_redacao:
            df_status_redacao = pd.DataFrame(status_redacao)
            df_status_redacao = df_status_redacao.sort_values(by="total", ascending=True)

            fig = px.bar(
                df_status_redacao,
                x="total",
                y="status",
                orientation='h',
                title=f"Status das Redações",
                color_discrete_sequence=["#ff6200"]
            )

            fig.update_layout(
                xaxis_title="Total",
                yaxis_title="Status da Redação",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#111111"),
                title=dict(font=dict(size=18, color="#111111")),
                coloraxis_showscale=False,
                bargap=0.2
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Sem dados de status disponíveis.")

        st.divider()

    # Gráficos demográficos
    st.subheader(f"Distribuições Demográficas - {regiao}")
    col1, col2, col3 = st.columns(3)

    if sexo:
        df_sexo = pd.DataFrame(sexo)
        fig1 = px.pie(df_sexo, values="total", names="sexo", title="Distribuição por Sexo",
                      color_discrete_sequence=["#ff6200", "#000d3c"])
        col1.plotly_chart(fig1, use_container_width=True)
    else:
        col1.warning("Sem dados de sexo disponíveis.")

    if faixa:
        df_faixa = pd.DataFrame(faixa)
        fig2 = px.bar(df_faixa, x="faixa_etaria", y="total", title="Distribuição por Faixa Etária",
                      color_discrete_sequence=["#000d3c"])
        fig2.update_layout(
            xaxis_title="Faixa Etária",
            yaxis_title="Total",
            xaxis_tickangle=-45,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#111111"),
            title=dict(font=dict(size=18, color="#111111")),
            bargap=0.2
        )
        col2.plotly_chart(fig2, use_container_width=True)
    else:
        col2.warning("Sem dados de faixa etária disponíveis.")
        
    if raca:
        df_raca = pd.DataFrame(raca)
        df_raca = df_raca.sort_values(by="total", ascending=True)

        fig3 = px.bar(df_raca, x="raca", y="total", title=f"Distribuição por Etnia",
        color_discrete_sequence=["#ff6200"]
    )

        fig3.update_layout(
            xaxis_title="Etnia",
            yaxis_title="Total",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#111111"),
            title=dict(font=dict(size=18, color="#111111")),
            coloraxis_showscale=False,  # remove a barra lateral de cores
            bargap=0.2
        )

        col3.plotly_chart(fig3, use_container_width=True)
    else:
        col3.warning("Sem dados de raça disponíveis.")
        
    st.divider()
    
    st.subheader(f"Fatores Socioeconômicos e Assiduidade - {regiao}")
    
    if dados_ausencia_renda:
        df_ausencia_renda = pd.DataFrame(dados_ausencia_renda)
        df_ausencia_renda["percentual_ausentes"] = (df_ausencia_renda["ausentes"] / df_ausencia_renda["total"]) * 100
        df_ausencia_renda = df_ausencia_renda.sort_values(by="percentual_ausentes", ascending=False)

        fig = px.line(
            df_ausencia_renda,
            x="renda",
            y="percentual_ausentes",
            text="percentual_ausentes",
            title="Percentual de Ausência por Faixa de Renda Familiar",
            labels={"renda": "Renda Familiar", "percentual_ausentes": "% de Ausentes"},
            markers=True 
        )
        
        fig.update_traces(
        line=dict(color="#ff6200", width=3),
        marker=dict(color="#ff6200"),
        texttemplate="%{text:.1f}%",
        textposition="top center"
        )
        
        fig.update_layout(
        xaxis_title="Renda Familiar",
        yaxis_title="% de Ausentes",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111111"),
        title=dict(font=dict(size=18, color="#111111")),
        yaxis=dict(range=[0, 100])
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para essa região.")
        
    st.divider()
    
    col1, col2 = st.columns(2)
    
    if dados_ausencia_faixa_etaria:
        df_ausencia_faixa_etaria = pd.DataFrame(dados_ausencia_faixa_etaria)
        df_ausencia_faixa_etaria["percentual_ausentes"] = (df_ausencia_faixa_etaria["ausentes"] / df_ausencia_faixa_etaria["total"]) * 100
        df_ausencia_faixa_etaria = df_ausencia_faixa_etaria.sort_values(by="percentual_ausentes", ascending=False)

        fig1 = px.bar(
            df_ausencia_faixa_etaria,
            x="faixa_etaria",
            y="percentual_ausentes",
            text=df_ausencia_faixa_etaria["percentual_ausentes"].map(lambda x: f"{x:.1f}%"),
            title="Percentual de Ausência por Faixa Etária",
            labels={"faixa_etaria": "Faixa Etária", "percentual_ausentes": "% de Ausentes"},
            color="percentual_ausentes",
            color_continuous_scale="Oranges"
        )

        fig1.update_traces(
            marker=dict(line=dict(width=1, color="black")),
            textposition="outside"
        )

        fig1.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#111111"),
            title=dict(font=dict(size=18, color="#111111")),
            yaxis=dict(range=[0, 100]),
            coloraxis_showscale=False
        )

        col1.plotly_chart(fig1, use_container_width=True)
    else:
        col1.warning("Nenhum dado disponível para essa região.")

    if dados_ausencia_raca:
        df_ausencia_raca = pd.DataFrame(dados_ausencia_raca)
        df_ausencia_raca["percentual_ausentes"] = (df_ausencia_raca["ausentes"] / df_ausencia_raca["total"]) * 100
        df_ausencia_raca = df_ausencia_raca.sort_values(by="percentual_ausentes", ascending=False)

        fig2 = px.bar(
            df_ausencia_raca,
            y="raca",
            x="percentual_ausentes",
            text=df_ausencia_raca["percentual_ausentes"].map(lambda x: f"{x:.1f}%"),
            title="Ausência por Cor/Raça",
            labels={"raca": "Raça", "percentual_ausentes": "% de Ausentes"},
            orientation='h',
            color="percentual_ausentes",
            color_continuous_scale="Oranges"
        )

        fig2.update_traces(
            marker=dict(line=dict(width=1, color="black")),
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="black")
        )

        fig2.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#111111"),
            title=dict(font=dict(size=18, color="#111111")),
            xaxis=dict(range=[0, 100]),
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed")
        )

        col2.plotly_chart(fig2, use_container_width=True)
    else:
        col2.warning("Nenhum dado disponível para essa região.")