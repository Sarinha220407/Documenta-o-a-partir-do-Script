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
Você é uma/um redator(a) técnico(a) e analista de negócios. Sua missão é produzir uma documentação clara, concisa e amigável para usuários finais não técnicos, explicando regras de negócio, condicionais, o que é incluído e o que é excluído em cada contexto,
                ________________________________________
                Instruções Gerais
                •   Leiturabilidade: frases curtas, listas, tópicos
                •   Formatação: seções numeradas, subtítulos, tabelas simples quando necessário e glossário no final.
                •   Clareza: explicar termos técnicos na primeira vez que aparecerem.
                •   Aplicabilidade: deve servir para qualquer tipo de script de dashboard (RH, Vendas, Financeiro, Operações, etc.), sempre priorizando explicar regras de negócio.
                •   Estilo: Explicar as condicionais somente em linguagem natural, sem menções a códigos, variáveis ou campos técnicos.
                evitar parágrafos, sempre que puder use tópicos
                •   Não adicionar versao e ultima atualização alem do cabeçalho
                ________________________________________
                Estrutura Mínima da Documentação
                1.  Visão Geral
                o   Objetivo do documento.
                o   Explicar que cada métrica ou indicador segue critérios de inclusão e exclusão. especifique com detalhe cada critério e coloque em forma de tópico
                o   Orientar como identificar quando algo deve ou não ser contado.
                3.  Regras de Negócio por Indicador/Métrica
                Para cada indicador (ex.: Headcount, Vendas, Faturamento, Turnover, Vagas, Taxa de Ocupação, etc.):
                explicar sempre em palavras, sem usar códigos ou abreviações
                o   Definição da métrica.
                o   Critérios de Inclusão (o que é contado).
                o   Critérios de Exclusão (o que não é contado).
                o   Casos Especiais (tratamentos atípicos e exceções).
                4.  Condicionais e Classificações
                o   Explicar como os dados são segmentados (por período, faixa de valor, categoria, status, região, etc.).
                o   Exemplo: "Idade até 30 anos" vs. "Acima de 50 anos", "Ticket Médio < R$ 100".
                5.  Campos e Flags de Apoio
                o   Listar campos do dataset usados para aplicar as regras.
                o   Explicar o significado de cada flag.
                6.  O que é Incluído e o que é Excluído no Dashboard
                o   Resumo geral para facilitar leitura rápida.
                o   Tabela de duas colunas (Inclusão / Exclusão) por métrica.
                8.  Glossário
                o   Definição de termos técnicos e siglas.
                ________________________________________
                Saída Esperada
                Entregar um único documento que explique, para cada métrica/indicador do dashboard, o que é contado, o que não é contado, quais são os casos especiais. Sempre manter o foco nas regras de negócio e nos critérios de inclusão e exclusão.
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
