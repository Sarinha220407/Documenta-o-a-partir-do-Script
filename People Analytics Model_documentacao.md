# Documentação Técnica

**Arquivo:** `People Analytics Model.qvs`  
**Última atualização:** 15/08/2025 09:45:22

# **Documentação do Script QlikView (QVS) – Estrutura de Dados para Análise de Recursos Humanos e Operações**

---

## **1. Introdução**
Este documento explica, de forma clara e organizada, o funcionamento de um script utilizado em uma ferramenta de análise de dados chamada **QlikView/Qlik Sense**. O objetivo desse script é **preparar e organizar informações** sobre funcionários, custos, produção e receitas de uma empresa, para que elas possam ser analisadas de maneira integrada em relatórios e painéis (*dashboards*).

Em termos simples, o script:
- **Carrega dados** de diferentes áreas (como Recursos Humanos, Finanças e Produção).
- **Cria conexões (links)** entre essas informações para que possam ser cruzadas.
- **Formata os dados** para que fiquem padronizados (moeda, datas, números, etc.).

---

## **2. Configurações Iniciais**
Antes de carregar os dados, o script define algumas **regras de formatação** para garantir que números, datas e moedas apareçam de forma consistente. Isso é importante para evitar confusões (por exemplo, diferenciar milhares de reais com pontos ou vírgulas).

### **2.1. Formatação de Números, Moedas e Datas**
| Configuração               | Descrição                                                                                     | Exemplo de Aplicação                     |
|----------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------|
| **ThousandSep='.'**        | Separa milhares com ponto (ex: 1.000).                                                       | 1.500 funcionários                       |
| **DecimalSep=','**         | Separa decimais com vírgula (ex: 3,14).                                                      | R$ 12,50                                  |
| **MoneyFormat**            | Formato da moeda brasileira (R$), com duas casas decimais e sinal negativo para valores negativos. | R$ 1.250,00 ou -R$ 300,00                 |
| **DateFormat='DD.MM.YYYY'**| Datas no formato **dia.mês.ano** (ex: 15.05.2023).                                           | 31.12.2022                                |
| **CollationLocale='pt-BR'**| Define que o idioma padrão é **português do Brasil**, para ordenação correta de palavras.     | Ordenar "São Paulo" antes de "Santos".    |

### **2.2. Definição de Caminhos para os Dados**
O script indica **onde os dados estão armazenados** usando "caminhos" (como pastas em um computador). Cada tipo de dado está em uma pasta específica:

| Variável               | Descrição                                                                                     | Exemplo de Conteúdo                       |
|------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------|
| **bronze_layer**       | Dados brutos (não processados).                                                              | Planilhas ou arquivos originais.          |
| **silver_layer**       | Dados parcialmente tratados (limpos e organizados).                                          | Tabelas com informações corrigidas.       |
| **gold_layer**         | Dados prontos para análise (já validados e estruturados).                                    | Tabelas usadas em relatórios.             |
| **manual_source**      | Dados inseridos manualmente (como planilhas Excel).                                           | Orçamentos ou metas digitadas.            |
| **ti_layer**           | Dados temporários ou em processo de transferência.                                           | Arquivos em espera para processamento.    |

---
## **3. Carregamento dos Dados**
O script carrega dois tipos principais de informações:
1. **Fatos (Tabelas de Eventos)**: Registros de coisas que aconteceram (ex: contratações, demissões, vendas).
2. **Dimensões (Tabelas de Referência)**: Informações descritivas (ex: nomes de funcionários, departamentos, calendário).

### **3.1. Tabelas de Fatos (O Que Aconteceu)**
Essas tabelas registram **eventos** com detalhes como data, pessoa envolvida, valores, etc.

| Tabela                          | Descrição                                                                                     | Exemplo de Uso                             |
|---------------------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------|
| **gd_headcount_f**              | Quantidade de funcionários ativos em cada período.                                           | "Em janeiro/2023, havia 500 funcionários."|
| **gd_termination_f**            | Registros de demissões (quem saiu, quando e por quê).                                        | "10 pessoas foram demitidas em março."     |
| **gd_excel_orcamento_historico_f** | Orçamentos planejados para contratações (metas de RH).                                      | "Meta: contratar 20 pessoas em 2023."     |
| **gd_posicoes_f**               | Posições (vagas) disponíveis na empresa.                                                     | "Há 5 vagas abertas no departamento X."    |
| **gd_eventos_f**                | Eventos relacionados a funcionários (ex: promoções, transferências).                         | "João foi promovido em 15/06/2023."        |
| **gd_custo_origem_opex_f**      | Custos operacionais (despesas da empresa).                                                   | "O departamento Y gastou R$ 10.000 em abril." |
| **gd_producao_celulose_f**      | Dados de produção de celulose (quantidade produzida).                                        | "Produzimos 1.000 toneladas em maio."      |
| **gd_vendas_celulose_f**        | Vendas de celulose (quantidade e receita).                                                   | "Vendemos 800 toneladas em junho."        |
| **gd_receita_liquida_f**        | Receita líquida da empresa (faturamento menos custos).                                        | "Receita em julho: R$ 500.000."            |

### **3.2. Tabelas de Dimensões (Informações de Referência)**
Essas tabelas **descrevem** os dados das tabelas de fatos (ex: quem é o funcionário, qual seu cargo, etc.).

| Tabela                  | Descrição                                                                                     | Exemplo de Conteúdo                       |
|-------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------|
| **gd_calendario_d**     | Calendário com datas, dias da semana, meses, anos.                                            | "15/05/2023 é uma segunda-feira."          |
| **gd_hierarquia_d**     | Estrutura hierárquica da empresa (quem reporta a quem).                                      | "Maria é gerente de João."                 |
| **gd_funcao_d**         | Cargos e funções dos funcionários.                                                           | "Analista de RH", "Supervisor de Produção".|
| **gd_eldorado_entity_d**| Unidades ou filiais da empresa.                                                               | "Unidade São Paulo", "Unidade Bahia".      |
| **gd_employee_d**       | Dados dos funcionários (nome, matrícula, etc.).                                              | "Nome: Carlos, Matrícula: 12345."         |
| **gd_situacao_d**       | Situação do funcionário (ativo, afastado, demitido).                                          | "Ativo", "Afastado por licença médica."    |
| **gd_centro_de_custo_d**| Departamentos ou áreas da empresa (ex: RH, Finanças).                                        | "Centro de Custo: TI."                    |

---
## **4. Criação de Links entre os Dados**
Para que as informações possam ser **cruzadas** (ex: relacionar um funcionário ao seu departamento e aos custos gerados por ele), o script cria uma **chave de ligação única** chamada **`link_key`**.

### **4.1. Como Funciona o `link_key`**
- É um **código gerado automaticamente** que identifica cada combinação única de dados (ex: funcionário + data + departamento).
- Permite **conectar tabelas diferentes** sem repetir informações.
- Exemplo:
  - Na tabela de funcionários (`gd_headcount_f`), o `link_key` pode ser:
    `Data: 01/01/2023 + Funcionário: João + Departamento: Produção`.
  - Na tabela de custos (`gd_custo_origem_opex_f`), o mesmo `link_key` permite saber quanto João custou para a empresa naquele mês.

### **4.2. Tabela `Link` (Conexão Final)**
O script cria uma tabela chamada **`Link`** que **centraliza todas as chaves** e preenche os campos vazios com valores padrão (ex: `''` para texto ou `0` para números). Isso garante que todas as tabelas possam ser relacionadas corretamente.

---
## **5. Exemplo Prático: Como os Dados São Usados**
Imagine que um gestor queira saber:
> **"Quantos funcionários do departamento de Produção foram demitidos em 2023, e qual foi o impacto nos custos?"**

O script permite cruzar:
1. **Tabela de demissões (`gd_termination_f`)** → Quem saiu e quando.
2. **Tabela de departamentos (`gd_centro_de_custo_d`)** → Filtrar apenas "Produção".
3. **Tabela de custos (`gd_custo_origem_opex_f`)** → Verificar as despesas antes e depois das demissões.
4. **Tabela de calendário (`gd_calendario_d`)** → Filtrar pelo ano de 2023.

**Resultado:** Um relatório mostrando:
- 15 demissões no departamento de Produção em 2023.
- Redução de R$ 120.000 nos custos operacionais após as demissões.

---
## **6. Finalização do Script**
Ao final, o script:
1. **Remove campos duplicados** das tabelas originais (para economizar espaço).
2. **Encerra a execução** com o comando `exit script`.

---
## **7. Resumo Visual**
```
┌───────────────────────┐    ┌───────────────────────┐    ┌───────────────────────┐
│  Tabelas de Fatos     │    │  Tabelas de Dimensões │    │       Tabela Link      │
│ (Eventos)             │    │ (Descrições)          │    │ (Conexão entre dados)  │
│ - Contratações        │    │ - Funcionários        │    │ - Chaves únicas       │
│ - Demissões           │    │ - Departamentos       │    │   (link_key)          │
│ - Custos              │    │ - Calendário          │    │ - Relações entre      │
│ - Produção            │    │ - Cargos             │    │   todas as tabelas    │
└───────────┬───────────┘    └───────────┬───────────┘    └───────────────────────┘
            │                            │
            └───────────────┬────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Relatórios e        │
                │   Dashboards          │
                │ (Análises integradas)│
                └───────────────────────┘
```

---
## **8. Glossário de Termos Simplificados**
| Termo               | Significado                                                                                   |
|---------------------|-----------------------------------------------------------------------------------------------|
| **QVD**             | Arquivo que armazena dados no Qlik (similar a uma planilha Excel, mas otimizado).              |
| **Fatos**           | Registros de eventos (ex: uma venda, uma contratação).                                        |
| **Dimensões**       | Informações descritivas (ex: nome de um produto, categoria de um funcionário).                |
| **`link_key`**      | Código único que conecta informações de tabelas diferentes.                                  |
| **`Load`**          | Comando para carregar dados de um arquivo.                                                   |
| **`Resident`**      | Comando para usar dados já carregados na memória.                                             |
| **`Drop Fields`**   | Remover colunas desnecessárias para otimizar o espaço.                                        |

---
## **9. Considerações Finais**
Este script é uma **peça fundamental** para integrar dados de **Recursos Humanos, Finanças e Produção**, permitindo que a empresa:
- Analise o **desempenho dos funcionários**.
- Controle **custos e orçamentos**.
- Relacione **produção e vendas** com a força de trabalho.
- Tome decisões baseadas em **dados consolidados**.

Ele não altera os dados originais, apenas os **organiza e prepara** para que sejam usados em relatórios e análises.
