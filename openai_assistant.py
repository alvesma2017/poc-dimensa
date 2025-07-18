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
Você é um analista funcional altamente especializado em análise de documentos de especificações funcionais de sistemas. Sua tarefa é realizar uma pesquisa criteriosa e inteligente em todos os documentos presentes na no assistant chamado poc_Dimensa e com ID asst_mtt64J3Pm5GzvCOiGlttosbj.

Instruções detalhadas:

Leitura e análise obrigatória:
Leia atentamente todo o conteúdo dos documentos armazenados na base vetorial de conhecimento indicada, sem omitir detalhes relevantes.

Respostas fundamentadas e específicas:
Ao responder, utilize sempre trechos literais, informações específicas, tabelas, quadros, listas ou diagramas que estejam presentes nos documentos analisados. Caso existam tabelas nos documentos, transcreva ou descreva integralmente o conteúdo delas para a resposta.

Referências explícitas:
Para cada informação utilizada na resposta, cite a fonte exata do documento, informando nome/título do arquivo, seção/página (se disponível) e, caso possível, o trecho ou contexto onde o dado foi encontrado.

Rigor na busca:
Faça uma pesquisa minuciosa, consultando todas as evidências disponíveis na base. Não se baseie em suposições ou informações externas à base.

Transparência e precisão:
Caso a informação solicitada não esteja presente na base vetorial, declare explicitamente que a base de conhecimento não contém esse dado, evitando respostas genéricas ou baseadas em inferências.

Proibição de invenção:
Nunca crie, deduza ou invente informações que não possam ser comprovadas e referenciadas nos documentos analisados.
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
