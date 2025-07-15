import streamlit as st
from utils import extrair_texto_docx, extrair_texto_pdf
from openai_assistant import enviar_para_openai

st.set_page_config(layout="wide", page_title="Eugenia - Analista Funcional", initial_sidebar_state="expanded")

with st.sidebar:
    st.image("logo_eug.png", width=220)

st.title("Eugenia - Analista Funcional")

if "historico" not in st.session_state:
    st.session_state["historico"] = []

if "texto_modelo" not in st.session_state:
    st.session_state["texto_modelo"] = None
if "titulo_modelo" not in st.session_state:
    st.session_state["titulo_modelo"] = None

# ---- FORMULÁRIO NORMAL ----
with st.form(key="form_envio", clear_on_submit=False):
    uploaded_files = st.file_uploader(
        "Anexe até 5 arquivos Word (.docx) ou PDF (.pdf):",
        type=["docx", "pdf"],
        accept_multiple_files=True
    )
    prompt_extra = st.text_area("Observações adicionais ou texto livre para análise (opcional):", height=100, key="prompt")
    col1, col2 = st.columns([1, 1])
    enviar = col1.form_submit_button("Analisar conteúdo (arquivos e/ou texto livre)")
    limpar = col2.form_submit_button("Limpar histórico")

if limpar:
    st.session_state["historico"] = []
    st.session_state["texto_modelo"] = None
    st.session_state["titulo_modelo"] = None
    st.experimental_rerun()

if enviar:
    # Limite de no máximo 5 arquivos
    if uploaded_files and len(uploaded_files) > 5:
        st.error("Você pode anexar no máximo 5 arquivos por vez.")
    # Checa se ao menos um arquivo ou prompt foi enviado
    elif (not uploaded_files or len(uploaded_files) == 0) and not prompt_extra.strip():
        st.error("Por favor, escreva algo nas observações ou anexe ao menos um arquivo para análise.")
    else:
        with st.spinner("Analisando o conteúdo..."):
            textos = []
            nomes_arquivos = []

            if uploaded_files:
                for uploaded_file in uploaded_files:
                    if uploaded_file.type == "application/pdf":
                        texto = extrair_texto_pdf(uploaded_file)
                    else:
                        texto = extrair_texto_docx(uploaded_file)
                    textos.append(texto)
                    nomes_arquivos.append(uploaded_file.name)
                texto_total = "\n\n---\n\n".join(textos)
                if prompt_extra.strip():
                    texto_total += "\n\n" + prompt_extra
            else:
                texto_total = prompt_extra
                nomes_arquivos = ["Sem arquivo anexado"]

            resposta = enviar_para_openai(texto_total, prompt_extra)
            st.session_state["historico"].append({
                "documento": ", ".join(nomes_arquivos),
                "prompt": prompt_extra,
                "resposta": resposta,
            })
        st.session_state["texto_modelo"] = None
        st.session_state["titulo_modelo"] = None

# ---- EXIBIR HISTÓRICO ----
for idx, item in enumerate(reversed(st.session_state["historico"])):
    st.markdown(f"**Arquivo(s) analisado(s):** {item['documento']}")
    if item['prompt']:
        st.markdown(f"**Prompt enviado:** {item['prompt']}")
    st.markdown("---")
    st.markdown(item["resposta"], unsafe_allow_html=True)
    st.markdown("---")
