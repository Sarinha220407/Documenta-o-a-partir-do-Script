import os
import time
from datetime import datetime
from mistralai import Mistral
from markdown import markdown
from xhtml2pdf import pisa


#API Mistral
MISTRAL_API_KEY = "JmNoW35BSmQA7UJPpCCiqiru1m1MbODu"
client = Mistral(api_key=MISTRAL_API_KEY)


def gerar_documentacao_qvs(conteudo: str, nome_arquivo: str) -> str:
    """Gera documentação para um arquivo QVS usando a API Mistral."""
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    prompt = f"""
Você é um gerador de documentação formal e clara.

Gere uma explicação detalhada e bem organizada para o script QVS abaixo,
no formato de um documento formal, mas que seja fácil de entender mesmo por
pessoas que não têm conhecimento técnico.

O texto deve ser:
- Escrito em português claro e acessível.
- Com tom formal e objetivo.
- Sem termos técnicos complexos ou siglas sem explicação.
- Organizado em seções e tópicos para facilitar a leitura.
- Explicar o que o script faz, para que serve e como funciona de forma simplificada.
- Incluir exemplos ilustrativos quando necessário.
- Não sugerir alterações ou melhorias no código.
- Não colocar versões ou datas, ou publico alvo, apenas o conteúdo do script.

Script:
{conteudo}
    """

    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        conteudo_gerado = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao chamar API Mistral: {e}")
        conteudo_gerado = ""

    cabecalho = (
        f"# Documentação Técnica\n\n"
        f"**Arquivo:** `{nome_arquivo}`  \n"
        f"**Última atualização:** {data_hora}\n\n"
        f"{conteudo_gerado}\n"
    )
    return cabecalho


def salvar_documentacao_em_md(conteudo_doc: str, nome_arquivo: str):
    nome_base = os.path.splitext(nome_arquivo)[0]
    nome_md = nome_base + "_documentacao.md"

    try:
        # Salva como Markdown
        with open(nome_md, "w", encoding="utf-8") as f:
            f.write(conteudo_doc)
        print(f"Markdown salvo: {nome_md}")

    except Exception as e:
        print(f"Erro ao salvar PDF: {e}")


def atualizar_documentacao_qvs(diretorio: str):
    """Gera documentação em Markdown para todos os arquivos .qvs no diretório informado."""
    for root, _, files in os.walk(diretorio):
        for file in files:
            if file.lower().endswith(".qvs"):
                caminho = os.path.join(root, file)

                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = f.read()

                linhas = conteudo.splitlines()
                while linhas and linhas[0].strip().startswith("//"):
                    linhas.pop(0)
                conteudo_sem_doc = "\n".join(linhas)

                print(f"Gerando documentação para: {caminho}")
                nova_doc = gerar_documentacao_qvs(conteudo_sem_doc, file)

                salvar_documentacao_em_md(nova_doc, file)

                time.sleep(15)


if __name__ == "__main__":
    atualizar_documentacao_qvs(".")
    print("Documentação gerada para todos os arquivos .qvs e exportada para Markdown.")
