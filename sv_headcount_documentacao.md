# Documentação Técnica

**Arquivo:** `sv_headcount.qvs`  
**Última atualização:** 15/08/2025 11:57:40

# **Documentação do Script QVS – Processamento de Dados de Recursos Humanos**

---

## **1. Introdução**
Este documento explica um script utilizado para processar dados de **Recursos Humanos (RH)** em uma ferramenta de análise de dados chamada **QlikView/Qlik Sense**. O objetivo principal do script é **organizar, transformar e preparar informações sobre funcionários**, como admissões, demissões, cargos, salários e hierarquias, para que possam ser usadas em relatórios e painéis de controle.

O script segue uma estrutura organizada em **camadas** (Bronze, Silver e Gold), onde:
- **Bronze**: Dados brutos (originais, sem tratamento).
- **Silver**: Dados limpos e transformados (prontos para análise).
- **Gold**: Dados consolidados (usados em relatórios finais).

---

## **2. Configurações Iniciais**
Antes de carregar os dados, o script define **formatações padrões** para garantir que números, datas, moedas e textos sejam exibidos corretamente. Alguns exemplos:

| Configuração               | Descrição                                                                 |
|----------------------------|---------------------------------------------------------------------------|
| `ThousandSep='.'`          | Separador de milhar (ex: `1.000`).                                      |
| `DecimalSep=','`          | Separador decimal (ex: `R$ 1.000,50`).                                  |
| `DateFormat='DD.MM.YYYY'`  | Formato de data (ex: `01.01.2023`).                                      |
| `MonthNames='jan;fev;...'` | Nomes dos meses em português.                                             |
| `CollationLocale='pt-BR'` | Configura o idioma para português do Brasil (afeta ordenação de textos). |

Além disso, são definidos **caminhos (pastas)** onde os dados serão salvos ou lidos:
- `bronze_layer`: Dados brutos.
- `silver_layer`: Dados processados.
- `gold_layer`: Dados finais para relatórios.
- `manual_source`: Dados manuais (planilhas, por exemplo).
- `external_layer`: Dados externos (de outras fontes).

---

## **3. Carregamento dos Dados Brutos (Bronze)**
Nesta etapa, o script **carrega arquivos de dados brutos** (no formato `.QVD`, um tipo de arquivo do Qlik) para a memória. Cada tabela carregada representa um tipo de informação:

| Tabela                                      | Descrição                                                                                     |
|---------------------------------------------|-----------------------------------------------------------------------------------------------|
| `bz_headcount_f`                           | Histórico de funcionários ativos e inativos (com filtro para dados a partir de 01/01/2019).    |
| `bz_headcount_hist_f`                      | Histórico completo de funcionários (sem filtro de data).                                      |
| `bz_headcount_latest_f`                    | Dados mais recentes dos funcionários.                                                          |
| `bz_posicoes_f`                            | Informações sobre posições (cargos) na empresa.                                                |
| `bz_excel_hc_orcamento_historico_f`       | Histórico de orçamento de headcount (quantidade de funcionários planejada).                  |
| `bz_headcount_offshore_f`                  | Funcionários que trabalham fora do Brasil (offshore).                                           |
| `bz_excel_posicoes_f`                      | Posições (vagas) em aberto ou preenchidas.                                                    |
| `bz_excel_estrutura_cc_d`                  | Estrutura de centros de custo (áreas da empresa).                                              |
| `bz_pessoa_d`                              | Dados pessoais dos funcionários (CPF, RG, endereço, etc.).                                     |
| `bz_hierarquia_d`                          | Hierarquia organizacional (quem reporta para quem).                                             |
| `bz_excel_funcao_d`                        | Descrição dos cargos (funções) na empresa.                                                     |
| `bz_excel_range_salario_d`                 | Faixas salariais por cargo.                                                                   |
| `bz_excel_filial_d`                        | Informações sobre filiais da empresa.                                                          |
| `bz_externo_centro_custo_d`               | Centros de custo externos (fornecedores ou parceiros).                                        |

---
## **4. Tabelas de Mapeamento (Dicionários)**
Para padronizar termos e facilitar análises, o script cria **tabelas de mapeamento**, que funcionam como "dicionários" para traduzir códigos em nomes legíveis. Exemplo:

### **4.1. Mapeamento de Empresas (`coligada_d`)**
| Código (`CODCOLIGADA`) | Nome da Empresa (`COLIGADA`)          |
|------------------------|----------------------------------------|
| 1                      | Eldorado                                |
| 2                      | Florestal                               |
| 3                      | OffShore                                |
| 30                     | Cellulose Eldorado Austria GmbH        |

### **4.2. Mapeamento de Tipos de Demissão (`CLASSIFICAÇÃO_MAP`)**
| Código (`Tipo de Demissão`) | Classificação          |
|------------------------------|------------------------|
| 2                            | Involuntário           |
| 8                            | Involuntário           |
| V                            | Voluntário             |
| 4                            | Voluntário             |

### **4.3. Mapeamento de Eventos (`MAP_EVENTOS`)**
| Código (`CODEVENTO`) | Tipo de Evento         |
|----------------------|------------------------|
| 2                    | Salário Base (SB)      |
| 5                    | Salário Família (SF)   |
| 24                   | Hora Extra Esporádica  |
| 28                   | Hora Extra Recorrente  |
| 80                   | PLR (Participação nos Lucros) |

---
## **5. Transformação dos Dados (Silver)**
Nesta etapa, os dados brutos são **limpos, enriquecidos e organizados** para análise. As principais transformações são:

### **5.1. Centro de Custo (`centro_de_custo`)**
- **Objetivo**: Padronizar os centros de custo (áreas da empresa) e classificá-los em grupos (ex: "Corporativo", "Industrial").
- **Exemplo de classificação**:
  - Se a `Diretoria` for "Financeiro" → Grupo = "Corporativo".
  - Se a `Diretoria` for "Industrial" → Grupo = "Industrial".

### **5.2. Funções (`funcao`)**
- **Objetivo**: Padronizar os nomes dos cargos e classificá-los (ex: "Líder", "Operacional").
- **Exemplo**:
  - Cargo: "01234 - Analista de TI" → Código: `01234`, Nome: "Analista de TI".
  - Se o cargo pertence à carreira "1-Gestão" → Classificado como "Líder".

### **5.3. Headcount (Funcionários Ativos)**
- **Objetivo**: Consolidar informações sobre funcionários ativos, como:
  - Tempo na empresa.
  - Se é um novo contratado (`new_hire_flag`).
  - Se foi admitido no mês (`admitido_flag`).
  - Salário e posição na faixa salarial (`posic_fs`).
- **Exemplo de cálculo**:
  - `tempo_empresa_dias = Data Atual - Data de Admissão`.
  - Se `tempo_empresa_dias < 365` → "Novo Contratado".

### **5.4. Terminação (Demissões)**
- **Objetivo**: Analisar demissões, classificando-as como **voluntárias** ou **involuntárias**.
- **Exemplo**:
  - Se `Tipo de Demissão = 2` → Classificação = "Involuntário".
  - Se `Tipo de Demissão = 4` → Classificação = "Voluntário".

### **5.5. Posições (Vagas)**
- **Objetivo**: Acompanhar vagas em aberto, tempo de recrutamento e contratação.
- **Exemplo**:
  - `tempo_recrutamento = Data de Contratação - Data de Abertura da Vaga`.
  - Se `STATUS = "EM ANDAMENTO"` → Vaga ainda não preenchida.

---
## **6. Consolidação dos Dados (Gold)**
Os dados transformados são **salvos em arquivos `.QVD`** na camada Silver para uso em relatórios. As principais tabelas geradas são:

| Tabela                     | Descrição                                                                 |
|----------------------------|---------------------------------------------------------------------------|
| `sv_headcount_f`           | Funcionários ativos com detalhes como cargo, salário, tempo na empresa.  |
| `sv_termination_f`        | Demissões com classificação (voluntária/involuntária) e motivos.          |
| `sv_posicoes_f`            | Vagas em aberto ou preenchidas, com tempo de recrutamento.                |
| `sv_centro_de_custo_d`    | Centros de custo padronizados.                                            |
| `sv_funcao_d`              | Cargos padronizados com classificações (líder, operacional, etc.).        |

---
## **7. Limpeza Final**
Ao final do script, as **tabelas temporárias** (usadas apenas para processamento) são **excluídas** para liberar memória:
```qlik
DROP TABLE bz_headcount_f, bz_pessoa_d, bz_hierarquia_d, ...;
```

---
## **8. Exemplo Prático: Análise de Turnover**
Suponha que a empresa queira analisar **demissões voluntárias** no último ano. O script permite:
1. **Filtrar demissões voluntárias**:
   - Usar a tabela `sv_termination_f` com o campo `demissao_classificacao = "Voluntário"`.
2. **Calcular a taxa de turnover**:
   - `Taxa de Turnover = (Número de Demissões Voluntárias / Número Total de Funcionários) × 100`.
3. **Identificar padrões**:
   - Quais áreas (`centro_de_custo`) têm mais demissões?
   - Qual o tempo médio na empresa (`tempo_empresa_dias`) dos funcionários que saíram?

---
## **9. Conclusão**
Este script é uma **ferramenta poderosa para análise de RH**, permitindo:
✅ **Acompanhar o headcount** (quantidade de funcionários).
✅ **Analisar demissões** (voluntárias vs. involuntárias).
✅ **Monitorar vagas em aberto** e tempo de recrutamento.
✅ **Classificar cargos** (líderes, operacionais, etc.).
✅ **Cruzar dados** com salários, centros de custo e hierarquia.

Com os dados processados, a empresa pode **tomar decisões baseadas em dados**, como:
- Reduzir turnover em áreas críticas.
- Ajustar salários para reter talentos.
- Otimizar o processo de recrutamento.

---
**Fim da Documentação**
