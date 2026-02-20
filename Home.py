import streamlit as st

st.set_page_config(page_title="Dashboard ENEM 2023", layout="wide")
st.title("Dashboard ENEM 2023")
st.markdown("---")

st.markdown("""
### Visão Geral do Projeto

Esta **Dashboard ENEM 2023** é uma aplicação **Full Stack** desenvolvida com o objetivo de 
**analisar e visualizar dados educacionais** de forma interativa e acessível.

O projeto foi construído com duas camadas principais:

- **Backend (API)** — Desenvolvido com **[FastAPI](https://fastapi.tiangolo.com/)**, responsável por processar as requisições, conectar-se ao banco de dados **PostgreSQL** e disponibilizar os dados de forma otimizada por meio de endpoints REST.
- **Frontend (Dashboard)** — Criado com **[Streamlit](https://streamlit.io/)**, que consome a API e apresenta os resultados de maneira visual, com gráficos interativos, métricas e filtros dinâmicos.

Essa integração permite atualizar os dados de forma **modular e escalável**, garantindo que as análises estejam sempre sincronizadas com as informações reais armazenadas no banco de dados.
""")

st.markdown("---")
st.subheader("📊 Estrutura da Dashboard")

st.markdown("""
A interface está dividida em duas seções principais, acessíveis pelo menu lateral:

1. **Análise por Região**  
   Exibe as **médias das notas** e **distribuições estatísticas** por região geográfica do Brasil.  
   Também apresenta dados demográficos e socioeconômicos agregados.

2. **Análise por Estado**  
   Permite uma visão detalhada dos resultados por **unidade federativa**, 
   comparando médias de desempenho, distribuição de notas e perfil dos participantes.

Essas duas páginas estão interligadas com a API, que retorna os dados de forma 
filtrada e otimizada para cada seleção feita pelo usuário.
""")

st.markdown("---")
st.subheader("🛠️ Tecnologias Utilizadas")

cols = st.columns(3)

with cols[0]:
    st.markdown("""
    - **Python**  
    - **FastAPI**  
    - **SQLAlchemy**  
    - **PostgreSQL**
    """)

with cols[1]:
    st.markdown("""
    - **Streamlit**  
    - **Plotly Express**  
    - **Streamlit Extras**  
    - **Dotenv (Configuração de variáveis)**
    """)

with cols[2]:
    st.markdown("""
    - **Docker**  
    - **Alembic (migrações)**  
    - **Pandas / NumPy**  
    - **Requests (integração API)**
    """)

st.markdown("---")
st.info("""
💡 **Dica:** Use o menu lateral à esquerda para escolher entre as análises por **Região** e **Estado**.  
Os gráficos e métricas serão atualizados automaticamente conforme sua seleção.
""")

st.markdown("""
---
*Projeto desenvolvido com foco em visualização educacional e integração entre dados e APIs modernas.*
""")
