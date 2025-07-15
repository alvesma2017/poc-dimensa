import openai
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_mtt64J3Pm5GzvCOiGlttosbj"

def enviar_para_openai(documento_texto, prompt_extra="", usar_prompt_padrao=True):
    """
    Se usar_prompt_padrao=True, concatena prompt base e análise de arquivo.
    Se usar_prompt_padrao=False, envia só o prompt_extra (ex: quebra-gelo).
    """
    openai.api_key = OPENAI_API_KEY

    if usar_prompt_padrao:
        prompt_base = """
Eu sou um agente especializado em analise detalhada de documentações de especificação funcional.
"""
        full_prompt = prompt_base + "\n\nDocumento enviado:\n" + documento_texto
        if prompt_extra:
            full_prompt += "\n\nObservações adicionais do usuário:\n" + prompt_extra
    else:
        # Só manda o texto do prompt_extra (quebra-gelo)
        full_prompt = documento_texto.strip()  # Aqui deve vir o texto do botão quebra-gelo

    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Você é um assistente jurídico especializado na Lei 14.133/2021."},
            {"role": "user", "content": full_prompt},
        ],
        temperature=0.1,
        max_tokens=10000
    )
    return response.choices[0].message.content
