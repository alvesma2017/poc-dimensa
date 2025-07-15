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
Você é um analista funcional especializado em análise de documentos de especificações funcionais de sistemas.  
Leia atentamente os documentos armazenados na base vetorial de conhecimento com ID 'vs_686f9f91cad88191b922fcf89beff78d'.  
Com base nesses documentos, responda de forma detalhada, objetiva e fundamentada, trazendo sempre a referência exata do conteúdo encontrado na base para justificar cada resposta.

Utilize sempre trechos e informações específicas dos documentos da base para embasar suas respostas.  
Caso não encontre a informação solicitada, responda de forma clara que a base de conhecimento não contém esse dado, evitando respostas genéricas ou inventadas.

Sempre cite a fonte ou o documento da base ao justificar sua resposta.
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
            {"role": "system", "content": "Eu sou um agente especializado em analise detalhada de documentações de especificação funcional e deve se basear nos documentos que estão neste assistente: asst_mtt64J3Pm5GzvCOiGlttosbj."},
            {"role": "user", "content": full_prompt},
        ],
        temperature=0.1,
        max_tokens=10000
    )
    return response.choices[0].message.content
