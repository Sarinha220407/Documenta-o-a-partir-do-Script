# Documentação Técnica

**Arquivo:** `gd_headcount.qvs`  
**Última atualização:** 15/08/2025 11:53:12

# **Documentação do Script QVS – People Analytics (Recursos Humanos)**

## **1. Introdução**
Este documento explica um script utilizado para organizar e preparar dados de **Recursos Humanos (RH)** em um sistema de análise de dados. O objetivo é transformar informações brutas sobre funcionários, hierarquias, desligamentos e orçamentos em tabelas estruturadas, facilitando relatórios e tomadas de decisão.

O script está dividido em **seções lógicas**, cada uma responsável por uma etapa específica do processo, como:
- Configurações iniciais (formatação de datas, moedas, etc.).
- Criação de calendários e tabelas de tempo.
- Carregamento de dados brutos.
- Organização de dimensões (tabelas de referência).
- Geração de fatos (tabelas com informações operacionais).
- Armazenamento dos resultados.

---

## **2. Configurações Iniciais**
Esta seção define padrões de formatação para que os dados sejam exibidos de maneira consistente.

### **2.1. Formatação de Números, Datas e Moedas**
| Configuração               | Descrição                                                                 | Exemplo de Saída       |
|----------------------------|---------------------------------------------------------------------------|------------------------|
| `ThousandSep='.'`          | Separador de milhar (ponto).                                              | `1.000`                |
| `DecimalSep=','`          | Separador decimal (vírgula).                                              | `12,34`                |
| `MoneyFormat`              | Formato de moeda (Real Brasileiro).                                       | `R$1.234,56`           |
| `DateFormat='DD.MM.YYYY'` | Formato de data (dia/mês/ano).                                            | `15.05.2023`           |
| `MonthNames`               | Nomes abreviados dos meses em português.                                  | `jan`, `fev`, `mar`...|
| `DayNames`                 | Nomes abreviados dos dias da semana.                                      | `seg`, `ter`, `qua`... |

### **2.2. Caminhos de Arquivos (Pastas de Dados)**
O script define **localizações** onde os dados são armazenados ou buscados, organizados em camadas:
- **Bronze**: Dados brutos (sem tratamento).
- **Silver**: Dados limpos e validados.
- **Gold**: Dados prontos para análise.
- **Manual Source**: Dados inseridos manualmente.
- **Fontes Externas**: Dados de outras origens (ex.: planilhas).

---
## **3. Criação de Tabelas Auxiliares**
### **3.1. Tabela de Calendário (`gd_calendario_d`)**
**Objetivo**: Criar um calendário com todas as datas entre **01/01/2014** e o último dia do ano corrente, incluindo informações como:
- Dia da semana.
- Mês e ano.
- Trimestre e semestre.
- Se é feriado, final de semana ou dia útil.

**Exemplo de campos gerados**:
| Campo               | Descrição                                  | Exemplo          |
|---------------------|--------------------------------------------|------------------|
| `date_key`          | Data no formato `DD.MM.YYYY`.              | `15.05.2023`     |
| `dia_semana_nome`   | Nome do dia da semana.                     | `seg`            |
| `mes_atual`         | Indica se é o mês atual (`Sim`/`Não`).      | `Sim`            |
| `final_semana`      | Indica se é final de semana (`Sim`/`Não`).  | `Não`            |

**Uso**: Permite analisar dados por períodos (ex.: "Quantos funcionários foram contratados no 1º trimestre de 2023?").

---

### **3.2. Tabela de Tempo na Empresa (`gd_tempo_companhia_d`)**
**Objetivo**: Classificar o tempo de serviço dos funcionários em grupos, como:
- **Grupos gerenciais** (ex.: "1-3 anos", "4-6 anos").
- **Grupos operacionais** (ex.: "0-3 meses", "3-6 meses").
- Indicador de **novos contratados** (`new_hire`).

**Exemplo de classificação**:
| Dias na Empresa | Grupo Gerencial | Grupo Operacional | `new_hire` |
|-----------------|-----------------|-------------------|------------|
| 45              | Ano 1           | 3-6 meses         | `TRUE`     |
| 1.200           | Ano 3-4         | Ano 3 - 12-18 meses | `FALSE`   |

**Uso**: Auxilia em análises como turnover (rotatividade) por tempo de empresa.

---
## **4. Carregamento de Dados Brutos**
Nesta seção, o script **importa dados já tratados** (da camada *Silver*) e os prepara para análise. Os principais conjuntos de dados são:

| Tabela                          | Descrição                                                                 |
|---------------------------------|---------------------------------------------------------------------------|
| `sv_headcount_f_raw`           | Informações atuais dos funcionários (nome, cargo, salário, hierarquia).  |
| `sv_termination_f_raw`         | Registros de desligamentos (data, motivo, tempo na empresa).              |
| `sv_excel_hc_orcamento_historico_raw` | Orçamentos históricos de headcount (plano vs. real).               |
| `sv_posicoes_raw`               | Posições/cargos disponíveis na empresa.                                  |

**Processo comum**:
1. **Adição de chaves únicas** (`Hash128`): Códigos que identificam registros sem ambiguidade (ex.: `hierarquia_sk` para hierarquias).
2. **Vinculação a datas**: Associação a `date_key` (calendário) ou `tempo_empresa_key` (tempo na empresa).

---
## **5. Criação de Dimensões (Tabelas de Referência)**
Dimensões são **tabelas que descrevem atributos** usados para agrupar dados. Exemplos:

| Dimensão               | Descrição                                                                 | Campos Principais                          |
|------------------------|---------------------------------------------------------------------------|--------------------------------------------|
| `gd_employee_d`        | Dados pessoais dos funcionários.                                          | `pessoa`, `nome`, `cpf`, `genero`, `email` |
| `gd_hierarquia_d`      | Estrutura hierárquica (gestores, níveis).                                 | `hierarquia_sk`, `gestor_direto_nome`      |
| `gd_funcao_d`          | Cargos e funções.                                                         | `funcao_sk`, `funcao_nome`, `carreira`     |
| `gd_idade_d`           | Classificação por faixa etária e geração (ex.: Geração Z).               | `grupo_idade`, `geracao`                   |
| `gd_centro_de_custo_d` | Centros de custo (áreas/departamentos).                                   | `centro_de_custo_sk`, `diretoria`          |

**Exemplo de uso**:
- **"Quantos funcionários da Geração Y trabalham na Diretoria de Operações?"** → Cruza `gd_employee_d` (geração) com `gd_hierarquia_d` (diretoria).

---
## **6. Criação de Tabelas Fato (Informações Operacionais)**
Tabelas fato armazenam **dados transacionais** (ex.: contratações, desligamentos) vinculados às dimensões.

| Tabela Fato                     | Descrição                                                                 | Campos Principais                          |
|---------------------------------|---------------------------------------------------------------------------|--------------------------------------------|
| `gd_headcount_f`                | Headcount atual (funcionários ativos).                                    | `pessoa`, `date_key`, `funcao_sk`          |
| `gd_termination_f`              | Desligamentos.                                                            | `pessoa`, `termination_date`, `motivo`     |
| `gd_excel_hc_orcamento_historico_f` | Comparativo entre orçado e real.                     | `centro_de_custo_sk`, `orcado`, `real`     |
| `gd_posicoes_f`                 | Posições disponíveis.                                                     | `funcao_sk`, `vagas`                       |

**Processo**:
1. **Carrega dados brutos**.
2. **Remove campos desnecessários** (ex.: dados pessoais sensíveis como CPF).
3. **Armazena na camada *Gold*** para uso em relatórios.

---
## **7. Armazenamento e Finalização**
### **7.1. Salvamento dos Dados**
Todas as tabelas geradas são salvas em arquivos `.QVD` (formato otimizado do Qlik) na camada *Gold*, seguindo a estrutura:
```
lib://Eldorado Data Folder - 3 Recursos Humanos - People Analytics/01. HR Medallion/03. Gold/
```
Exemplos:
- `gd_calendario_d.QVD`
- `gd_employee_d.QVD`
- `gd_headcount_f.QVD`

### **7.2. Limpeza de Tabelas Temporárias**
Ao final, o script **exclui tabelas temporárias** (`DROP TABLE`) para liberar memória, mantendo apenas os arquivos salvos.

---
## **8. Fluxo Resumido do Script**
1. **Configurações**: Define formatos e caminhos.
2. **Tabelas auxiliares**: Cria calendário e classificações de tempo.
3. **Carregamento**: Importa dados brutos da camada *Silver*.
4. **Dimensões**: Organiza tabelas de referência (funcionários, cargos, hierarquias).
5. **Fatos**: Prepara tabelas com informações operacionais (headcount, desligamentos).
6. **Salvamento**: Armazena tudo na camada *Gold*.
7. **Finalização**: Exclui tabelas temporárias e encerra.

---
## **9. Exemplo Prático: Análise de Turnover**
**Pergunta**: *"Qual a taxa de desligamentos de funcionários com menos de 1 ano na empresa em 2023?"*

**Como o script ajuda**:
1. **Filtra `gd_termination_f`** por `termination_date` em 2023.
2. **Cruza com `gd_tempo_companhia_d`** para identificar `tempo_empresa_key < 365` (menos de 1 ano).
3. **Agrupa por `grupo_operacao`** (ex.: "0-3 meses", "3-6 meses").
4. **Calcula a taxa**: `(Desligamentos no grupo) / (Total de funcionários no grupo)`.

---
## **10. Observações Finais**
- **Segurança**: Dados sensíveis (como CPF) são removidos das tabelas fato, mantendo apenas chaves anônimas (`sk`).
- **Flexibilidade**: O calendário e as classificações de tempo permitem análises por qualquer período.
- **Integração**: As tabelas *Gold* podem ser usadas diretamente em dashboards ou relatórios.

Este script é **fundamental para transformar dados de RH em informações estratégicas**, como:
- Análise de rotatividade (`turnover`).
- Planejamento de headcount (contratações vs. orçamento).
- Distribuição de funcionários por idade, cargo ou localização.
