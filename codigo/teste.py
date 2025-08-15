import os
import datetime
from openai import OpenAI

# Sua chave da OpenAI
client = OpenAI(api_key="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")

def gerar_documentacao_qvs(codigo, nome_arquivo):
    prompt = f"""
    Analise o código QlikView Script (.qvs) abaixo e gere uma documentação clara.
    Explique o objetivo geral do script, as etapas principais e variáveis utilizadas.
    Inclua no início a data/hora da última modificação no formato 'Última atualização: DD/MM/AAAA HH:MM'.

    Nome do arquivo: {nome_arquivo}
    Código:
    {codigo}
    """
    
    resposta = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return resposta.choices[0].message.content.strip()

def atualizar_documentacao_qvs(pasta):
    for root, _, files in os.walk(pasta):
        for file in files:
            if file.endswith(".qvs"):  # Aqui trocamos .py por .qvs
                caminho = os.path.join(root, file)
                
                with open(caminho, "r", encoding="utf-8") as f:
                    codigo = f.read()

                docstring = gerar_documentacao_qvs(codigo, file)

                timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                cabecalho = f"// Documentação gerada automaticamente\n// Última atualização: {timestamp}\n\n{docstring}\n\n"
                
                # Remove documentação anterior (se começar com // Documentação)
                if codigo.startswith("// Documentação gerada automaticamente"):
                    codigo = "\n".join(codigo.split("\n")[3:])

                with open(caminho, "w", encoding="utf-8") as f:
                    f.write(cabecalho + codigo)

                print(f"✅ Documentação atualizada para {file}")

# Executa para a pasta atual
atualizar_documentacao_qvs(".")


modificando