import streamlit as st
from utils import extrair_texto_docx, extrair_texto_pdf
from openai_assistant import enviar_para_openai

st.set_page_config(layout="wide", page_title="Agente Jurídico Prefeitura Goiania", initial_sidebar_state="expanded")

with st.sidebar:
    st.image("logo_eug.png", width=220)
    st.markdown(
        """
        <div style='background-color:#111124;padding:20px;border-radius:10px; text-align:center; margin-top: 10px;'>
            <a href='/' style='color:#fff;text-decoration:none;'><b>Análise Jurídica</b></a>
        </div>
        <div style='background-color:#111124;padding:20px;border-radius:10px; text-align:center; margin-top: 20px;'>
            <a href='https://poc-goiania-gpt-v1.streamlit.app/' style='color:#fff;text-decoration:none;'><b>Gerar Documentação</b></a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.title("Análise Jurídica - Licitações")

if "historico" not in st.session_state:
    st.session_state["historico"] = []

if "texto_modelo" not in st.session_state:
    st.session_state["texto_modelo"] = None
if "titulo_modelo" not in st.session_state:
    st.session_state["titulo_modelo"] = None

# ---- FORMULÁRIO NORMAL ----
with st.form(key="form_envio", clear_on_submit=False):
    uploaded_file = st.file_uploader("Anexe um arquivo Word (.docx) ou PDF (.pdf):", type=["docx", "pdf"])
    prompt_extra = st.text_area("Observações adicionais ou texto livre para análise (opcional):", height=100, key="prompt")
    col1, col2 = st.columns([1, 1])
    enviar = col1.form_submit_button("Analisar conteúdo (arquivo e/ou texto livre)")
    limpar = col2.form_submit_button("Limpar histórico")

if limpar:
    st.session_state["historico"] = []
    st.session_state["texto_modelo"] = None
    st.session_state["titulo_modelo"] = None
    st.experimental_rerun()

if enviar:
    if uploaded_file is None and not prompt_extra.strip():
        st.error("Por favor, escreva algo nas observações ou anexe um arquivo para análise.")
    else:
        with st.spinner("Analisando o conteúdo..."):
            if uploaded_file:
                if uploaded_file.type == "application/pdf":
                    texto = extrair_texto_pdf(uploaded_file)
                else:
                    texto = extrair_texto_docx(uploaded_file)
                # Junta o texto extraído com o texto livre, se houver
                if prompt_extra.strip():
                    texto_total = texto + "\n\n" + prompt_extra
                else:
                    texto_total = texto
                nome_arquivo = uploaded_file.name
            else:
                texto_total = prompt_extra
                nome_arquivo = "Sem arquivo anexado"

            resposta = enviar_para_openai(texto_total, prompt_extra)
            st.session_state["historico"].append({
                "documento": nome_arquivo,
                "prompt": prompt_extra,
                "resposta": resposta,
            })
        st.session_state["texto_modelo"] = None
        st.session_state["titulo_modelo"] = None

# ---- EXIBIR HISTÓRICO ----
for idx, item in enumerate(reversed(st.session_state["historico"])):
    st.markdown(f"**Arquivo analisado:** {item['documento']}")
    if item['prompt']:
        st.markdown(f"**Prompt enviado:** {item['prompt']}")
    st.markdown("---")
    st.markdown(item["resposta"], unsafe_allow_html=True)
    st.markdown("---")
