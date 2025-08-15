# Documentação Técnica

**Arquivo:** `bz_headcount.qvs`  
**Última atualização:** 15/08/2025 10:00:46

# **Documentação do Script QVS – Processamento de Dados de Recursos Humanos**

---

## **1. Introdução**
Este documento explica, de forma clara e organizada, o funcionamento de um script utilizado para **processar e organizar dados relacionados a Recursos Humanos (RH)**. O script é escrito em uma linguagem chamada **QVS** (usada na ferramenta **QlikView/Qlik Sense**), que serve para **extrair, transformar e armazenar informações** de maneira estruturada.

O objetivo principal deste script é **coletar dados de diferentes fontes** (como planilhas e arquivos internos) e **prepará-los para análise**, facilitando relatórios e tomadas de decisão na área de RH.

---

## **2. Configurações Iniciais**
Antes de processar os dados, o script define **configurações gerais** para garantir que números, datas, moedas e outros formatos sejam exibidos corretamente, de acordo com o padrão brasileiro.

### **2.1. Formatação de Números, Datas e Moedas**
| Configuração | Descrição | Exemplo |
|--------------|-----------|---------|
| **`ThousandSep='.'`** | Separador de milhar (ponto) | `1.000` (mil) |
| **`DecimalSep=','`** | Separador decimal (vírgula) | `12,50` (doze vírgula cinquenta) |
| **`MoneyFormat='R$#.##0,00'`** | Formato de moeda (Real brasileiro) | `R$1.250,00` |
| **`DateFormat='DD.MM.YYYY'`** | Formato de data (dia/mês/ano) | `15.05.2024` |
| **`TimestampFormat='DD/MM/YYYY hh:mm:ss'`** | Formato de data e hora | `15/05/2024 14:30:00` |
| **`CollationLocale='pt-BR'`** | Idioma e região (português do Brasil) | Ordenação de palavras em português |

### **2.2. Configuração de Pastas (Caminhos de Arquivos)**
O script define **onde os dados serão buscados e salvos**, utilizando **caminhos de pasta** (chamados de *"layers"* ou camadas). Cada camada tem uma função específica:

| Variável | Descrição | Exemplo de Uso |
|----------|-----------|----------------|
| **`bronze_layer`** | Local onde os dados **brutos** (sem tratamento) são armazenados. | `lib://.../01. Bronze/` |
| **`silver_layer`** | Local para dados **parcialmente tratados** (não usado neste script). | `lib://.../02. Silver/` |
| **`gold_layer`** | Local para dados **prontos para análise** (não usado neste script). | `lib://.../03. Gold/` |
| **`manual_source`** | Pasta com **arquivos manuais** (planilhas Excel). | `lib://.../02. Manual Source/` |
| **`ti_layer`** | Pasta com dados **extraídos de sistemas internos** (como SAP). | `lib://Staging Recursos Humanos/` |
| **`external_layer`** | Pasta com dados **externos** (de outras fontes). | `lib://.../04. Fontes Externas/` |

---
## **3. Processamento dos Dados**
O script **carrega dados de diferentes fontes**, como arquivos **QVD** (formato do Qlik) e **Excel**, e os salva na camada *Bronze* para uso futuro.

Cada seção do script é responsável por **um tipo específico de dado**, como:
- **Headcount** (número de funcionários).
- **Salários e cargos**.
- **Hierarquia organizacional**.
- **Movimentações de funcionários**.
- **Dados de filiais e centros de custo**.

---

### **3.1. Dados de Headcount (Número de Funcionários)**
#### **a) Headcount Atual (`bz_headcount_f`)**
- **O que faz?**
  - Carrega dados **atuais** sobre o número de funcionários da empresa.
  - Esses dados vêm de um arquivo chamado **`0STA_RHRMV012_001.qvd`** (gerado por um sistema interno).
- **Para que serve?**
  - Permite saber **quantos funcionários estão ativos** em um determinado momento.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_headcount_f.QVD`**.

#### **b) Headcount Histórico (`bz_headcount_hist_f`)**
- **O que faz?**
  - Carrega dados **históricos** (de 2014 a 2018) sobre o número de funcionários.
  - Esses dados vêm de uma **planilha Excel** (`hc_historica_f.xlsx`).
- **Para que serve?**
  - Permite **comparar a evolução do número de funcionários ao longo dos anos**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_headcount_hist_f.QVD`**.

#### **c) Headcount Mais Recente (`bz_headcount_latest_f`)**
- **O que faz?**
  - Carrega dados **mais atualizados** sobre funcionários, incluindo informações de **salário**.
  - Renomeia algumas colunas para facilitar o entendimento (ex: `"Funcionário (Salário)"` vira `"Funcionário"`).
- **Para que serve?**
  - Fornece uma **visão detalhada dos funcionários ativos**, com dados de remuneração.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_headcount_latest_f.QVD`**.

---

### **3.2. Dados de Pessoas e Hierarquia**
#### **a) Informações Pessoais (`bz_pessoa_d`)**
- **O que faz?**
  - Carrega dados **pessoais dos funcionários** (nome, documento, etc.).
  - Vem do arquivo **`0STA_DRMPESSOA_001.qvd`**.
- **Para que serve?**
  - Permite **identificar cada funcionário** e cruzar com outros dados (como salário e cargo).
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_pessoa_d.QVD`**.

#### **b) Hierarquia Organizacional (`bz_hierarquia_d`)**
- **O que faz?**
  - Carrega dados sobre a **estrutura hierárquica** da empresa (quem reporta a quem).
  - Vem do arquivo **`0STA_RHRMV007_001.qvd`**.
- **Para que serve?**
  - Ajuda a **visualizar a organização por áreas e gestores**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_hierarquia_d.QVD`**.

---

### **3.3. Dados de Cargos, Salários e Filiais**
#### **a) Cargos e Funções (`bz_excel_funcao_d`)**
- **O que faz?**
  - Carrega uma **lista de cargos** da empresa, com detalhes como:
    - Nome do cargo.
    - **CBO** (Classificação Brasileira de Ocupações).
    - Requisitos (formação, cursos, CNH).
    - Grupo salarial.
  - Vem de uma **planilha Excel** (`funcoes_d.xlsx`).
- **Para que serve?**
  - Permite **classificar funcionários por cargo** e entender requisitos e salários associados.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_excel_funcao_d.QVD`**.

#### **b) Filiais (`bz_excel_filial_d`)**
- **O que faz?**
  - Carrega uma lista de **filiais da empresa**, com código e nome.
  - Vem de uma **planilha Excel** (`filial_d.xlsx`).
- **Para que serve?**
  - Ajuda a **identificar em qual unidade cada funcionário trabalha**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_excel_filial_d.QVD`**.

#### **c) Tabelas Salariais (`bz_excel_salario_d`)**
- **O que faz?**
  - Carrega a **tabela de salários** da empresa (faixas salariais por cargo).
  - Vem de uma **planilha Excel** (`tabela_salarial_d.xlsx`).
- **Para que serve?**
  - Permite **comparar salários pagos com as faixas definidas**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_excel_range_salario_d.QVD`**.

---

### **3.4. Dados de Orçamento e Centros de Custo**
#### **a) Orçamento Histórico de Headcount (`bz_excel_hc_orcamento_historico_f`)**
- **O que faz?**
  - Carrega dados de **previsão (orçamento) de número de funcionários** ao longo do tempo.
  - Vem de uma **planilha Excel** (`hc_orcamento_historico.xlsx`).
- **Para que serve?**
  - Permite **comparar o número real de funcionários com o planejado**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_excel_hc_orcamento_historico_f.QVD`**.

#### **b) Estrutura de Centros de Custo (`bz_excel_estrutura_cc_d`)**
- **O que faz?**
  - Carrega a **estrutura de centros de custo** (áreas da empresa e seus códigos).
  - Vem de uma **planilha Excel** (`centro_de_custo_d.xlsx`).
- **Para que serve?**
  - Ajuda a **agrupar despesas e funcionários por área**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_excel_estrutura_cc_d.QVD`**.

#### **c) Centros de Custo Externos (`bz_externo_centro_custo_d`)**
- **O que faz?**
  - Carrega dados de **centros de custo de fontes externas**.
  - Vem de um arquivo **QVD** (`TRFN_CC.CL.qvd`).
- **Para que serve?**
  - Complementa informações de centros de custo com dados de outros sistemas.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_externo_centro_custo_d.QVD`**.

---

### **3.5. Movimentações e Posições**
#### **a) Movimentações de Funcionários (`bz_movimentos_f`)**
- **O que faz?**
  - Carrega registros de **admissões, demissões, transferências e outras movimentações**.
  - Vem do arquivo **`0STA_RHRMV043_001.qvd`**.
- **Para que serve?**
  - Permite **analisar a rotatividade (turnover) e mudanças na equipe**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_movimentos_f.QVD`**.

#### **b) Posições na Empresa (`bz_posicoes_f`)**
- **O que faz?**
  - Carrega dados sobre **posições (vagas) disponíveis na empresa**.
  - Vem do arquivo **`0STA_RHRMV033_001.qvd`**.
- **Para que serve?**
  - Ajuda a **mapear vagas abertas e ocupadas**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_posicoes_f.QVD`**.

#### **c) Headcount Offshore (`bz_headcount_offshore_f`)**
- **O que faz?**
  - Carrega dados sobre **funcionários que trabalham fora do Brasil (offshore)**.
  - Vem do arquivo **`0STA_RHRMV046_001.qvd`**.
- **Para que serve?**
  - Permite **analisar a força de trabalho em outros países**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_headcount_offshore_f.QVD`**.

#### **d) Posições Abertas (`bz_excel_posicoes_f`)**
- **O que faz?**
  - Carrega uma lista de **vagas em aberto** na empresa.
  - Vem de uma **planilha Excel** (`posicoes_abertas.xlsx`).
- **Para que serve?**
  - Ajuda a **acompanhar o processo de contratação**.
- **Onde salva?**
  - Na camada *Bronze*, como **`bz_excel_posicoes_f.QVD`**.

---

## **4. Fluxo Geral do Script**
1. **Configurações iniciais** (formatos de data, moeda, pastas).
2. **Carregamento dos dados** de diferentes fontes (QVD, Excel).
3. **Salvamento na camada *Bronze*** (dados brutos para uso futuro).
4. **Exclusão das tabelas temporárias** (para liberar memória).

---
## **5. Resumo dos Arquivos Gerados**
Todos os dados processados são salvos na **camada *Bronze*** com o prefixo **`bz_`** (de *"bronze"*). Alguns exemplos:

| Arquivo Gerado | Descrição |
|----------------|-----------|
| `bz_headcount_f.QVD` | Número atual de funcionários. |
| `bz_pessoa_d.QVD` | Dados pessoais dos funcionários. |
| `bz_excel_funcao_d.QVD` | Lista de cargos e requisitos. |
| `bz_movimentos_f.QVD` | Registros de admissões e demissões. |
| `bz_excel_estrutura_cc_d.QVD` | Estrutura de centros de custo. |

---
## **6. Considerações Finais**
Este script **não faz análises diretas**, mas **prepara os dados** para que sejam usados em relatórios e dashboards no **Qlik Sense/QlikView**.

Seu principal objetivo é **centralizar informações de RH em um formato padronizado**, facilitando:
- **Análise de headcount** (número de funcionários).
- **Controle de salários e cargos**.
- **Acompanhamento de movimentações** (contratações, demissões).
- **Gestão de orçamento e centros de custo**.

---
**Fim da Documentação**
