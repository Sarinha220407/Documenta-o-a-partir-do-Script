# Documentação Técnica

**Arquivo:** `gd_headcount.qvs`  
**Última atualização:** 15/08/2025 10:02:01

# **Documentação do Script QVS – Processamento de Dados de Recursos Humanos**

mod
## **1. Introdução**
Este documento explica, de forma clara e organizada, o funcionamento de um script utilizado para processar e estruturar dados de **Recursos Humanos (RH)**. O objetivo principal é transformar informações brutas sobre funcionários, hierarquias, desligamentos e orçamentos em tabelas organizadas, facilitando a análise e a geração de relatórios.

O script segue uma abordagem chamada **"Medallion Architecture"**, que divide os dados em três camadas:
- **Bronze**: Dados brutos (não processados).
- **Silver**: Dados limpos e validados.
- **Gold**: Dados prontos para análise, com tabelas dimensionais e fatos bem estruturados.

---
## **2. Configurações Iniciais**
Antes de processar os dados, o script define padrões de formatação para garantir que números, datas, moedas e textos sejam exibidos de maneira consistente.

### **2.1. Formatação de Números, Datas e Moedas**
| Configuração               | Descrição                                                                 | Exemplo               |
|----------------------------|---------------------------------------------------------------------------|-----------------------|
| **ThousandSep**            | Separador de milhar (ponto).                                              | `1.000`               |
| **DecimalSep**             | Separador decimal (vírgula).                                              | `3,14`                |
| **MoneyFormat**            | Formato de moeda (Real Brasileiro).                                       | `R$1.234,56`          |
| **DateFormat**             | Formato de data (dia.mês.ano).                                            | `31.12.2023`          |
| **TimeFormat**             | Formato de hora (horas:minutos:segundos).                                 | `14:30:45`            |
| **MonthNames**             | Nomes dos meses abreviados.                                               | `jan`, `fev`, `mar`   |
| **LongMonthNames**         | Nomes dos meses por extenso.                                              | `janeiro`, `fevereiro`|
| **FirstWeekDay**           | Primeiro dia da semana (6 = domingo).                                     |                       |
| **CollationLocale**        | Idioma para ordenação de textos (`pt-BR` = Português do Brasil).         |                       |

---
## **3. Definição dos Caminhos dos Arquivos**
O script define onde os dados serão lidos e salvos, usando **variáveis** para facilitar a manutenção.

| Variável               | Descrição                                                                 | Exemplo de Caminho                                                                 |
|------------------------|---------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **bronze_layer**       | Local onde estão os dados brutos (não processados).                       | `lib://Eldorado Data Folder/.../01. Bronze/`                                        |
| **silver_layer**       | Local onde estão os dados limpos e validados.                             | `lib://Eldorado Data Folder/.../02. Silver/`                                        |
| **gold_layer**         | Local onde são salvos os dados prontos para análise.                       | `lib://Eldorado Data Folder/.../03. Gold/`                                          |
| **manual_source**      | Local para dados inseridos manualmente (planilhas, por exemplo).           | `lib://Eldorado Data Folder/.../02. Manual Source/`                                  |
| **ti_layer**           | Área temporária para processamento.                                       | `lib://Staging Recursos Humanos/`                                                   |
| **external_layer**     | Dados externos (fornecedores, pesquisas, etc.).                           | `lib://Eldorado Data Folder/.../04. Fontes Externas/`                                |

---
## **4. Criação de Tabelas de Suporte**
Antes de processar os dados de funcionários, o script cria duas tabelas essenciais para análise:

### **4.1. Tabela de Calendário (`gd_calendario_d`)**
**Objetivo**: Criar um calendário com todas as datas entre **01/01/2014** e **31/12 do ano atual**, incluindo informações como:
- Dia da semana.
- Mês e ano.
- Se é feriado ou final de semana.
- Se pertence ao mês/ano atual.

**Exemplo de dados gerados:**

| date_key   | dia_semana_nome | mes_nome | ano | semana_ano | final_semana | periodo_status |
|------------|-----------------|----------|-----|------------|--------------|----------------|
| 01.01.2024 | seg             | jan      | 2024| 1          | Não          | Histórico     |
| 06.01.2024 | sáb             | jan      | 2024| 1          | Sim          | Histórico     |
| 15.03.2025 | dom             | mar      | 2025| 11         | Sim          | Futuro        |

**Para que serve?**
- Permite analisar dados por **períodos** (mês, trimestre, ano).
- Identifica **dias úteis vs. fins de semana**.
- Filtra dados por **períodos históricos ou futuros**.
 

---

### **4.2. Tabela de Tempo na Empresa (`gd_tempo_companhia_d`)**
**Objetivo**: Criar uma tabela que classifica o tempo de um funcionário na empresa em **grupos gerenciais e operacionais**.

**Exemplo de classificações:**
| tempo_empresa_key | dias_totais | anos_totais | grupo_gerencial       | grupo_operacao       | new_hire |
|-------------------|-------------|-------------|-----------------------|----------------------|----------|
| 1                 | 1           | 0,0027      | Ano 1                 | 0-3 meses            | TRUE     |
| 365               | 365         | 1           | Ano 1                 | 9-12 meses           | FALSE    |
| 1.095             | 1.095       | 3           | Ano 3-4               | Ano 3 - 12-18 meses  | FALSE    |
| 5.475             | 5.475       | 15          | Mais que 15 anos      | Mais que 4 anos      | FALSE    |

**Para que serve?**
- Agrupar funcionários por **tempo de casa** (ex.: "1-2 anos", "5-10 anos").
- Identificar **novos contratados** (`new_hire = TRUE`).
- Analisar **rotatividade** (turnover) por faixa de tempo.

---
## **5. Carregamento dos Dados Brutos**
O script lê os dados já limpos da camada **Silver** e os prepara para transformação.

### **5.1. Tabelas Carregadas**
| Tabela                          | Descrição                                                                 |
|---------------------------------|---------------------------------------------------------------------------|
| **sv_headcount_f_raw**          | Dados de funcionários ativos (nome, cargo, salário, hierarquia, etc.).   |
| **sv_termination_f_raw**        | Dados de funcionários desligados (motivo, data de saída, etc.).           |
| **sv_excel_hc_orcamento_historico_raw** | Histórico de orçamento de pessoal (metas de contratação).        |
| **sv_posicoes_raw**             | Informações sobre cargos e posições na empresa.                           |

**O que é feito neste passo?**
- **Geração de chaves únicas** (`Hash128`) para relacionar tabelas.
  - Exemplo: `hierarquia_sk` (identifica a hierarquia de um funcionário).
- **Associação com datas** (`date_key`) e tempo na empresa (`tempo_empresa_key`).

---
## **6. Criação das Tabelas Dimensionais (Dimensões)**
As **tabelas dimensionais** armazenam informações descritivas (ex.: nomes de cargos, hierarquias, localidades). Elas são usadas para **filtrar e agrupar** dados nos relatórios.

### **6.1. Dimensão de Funcionários (`gd_employee_d`)**
**O que contém?**
- Dados pessoais dos funcionários (nome, CPF, data de nascimento, gênero, etc.).
- **Última data de atualização** (`ultima_data`).

**Exemplo:**
| pessoa | nome          | nascimento_data | genero | cpf          | ultima_data   |
|--------|---------------|-----------------|--------|--------------|---------------|
| 1001   | João Silva    | 15.05.1985      | M      | 123.456.789-00 | 31.12.2023    |

---

### **6.2. Dimensão de Hierarquia (`gd_hierarquia_d`)**
**O que contém?**
- Estrutura hierárquica da empresa (níveis 1 a 6, gestor direto).

**Exemplo:**
| hierarquia_sk | hierarquia_nome_n1 | hierarquia_nome_n2 | gestor_direto_nome |
|---------------|--------------------|--------------------|--------------------|
| ABC123        | Diretoria X        | Gerência Y         | Maria Souza        |

---

### **6.3. Outras Dimensões Criadas**
| Tabela                     | Descrição                                                                 |
|----------------------------|---------------------------------------------------------------------------|
| **gd_funcao_d**            | Cargos e funções (código, nome, tipo de carreira).                        |
| **gd_eldorado_entity_d**   | Unidades da empresa (filiais, coligadas).                               |
| **gd_secao_d**             | Seções/departamentos.                                                    |
| **gd_centro_de_custo_d**   | Centros de custo (áreas de despesas).                                     |
| **gd_situacao_d**          | Situação do funcionário (ativo, afastado, desligado).                    |
| **gd_tipo_funcionario_d**  | Tipo de contratação (CLT, temporário, estagiário).                        |
| **gd_escalada_d**          | Escalas de trabalho (jornada mensal).                                     |
| **gd_idade_d**             | Faixas etárias e gerações (Baby Boomers, Geração Z, etc.).                |
| **gd_contratacao_tipo_d**  | Tipo de admissão (contratação interna, externa).                          |
| **gd_status_d**            | Status do funcionário (ativo, desligado).                                 |

---
## **7. Criação das Tabelas Fato (Fatos)**
As **tabelas fato** armazenam **métricas e eventos** (ex.: número de funcionários, desligamentos). Elas se relacionam com as dimensões para análise.

### **7.1. Tabela Fato de Headcount (`gd_headcount_f`)**
**O que contém?**
- **Contagem de funcionários ativos** por data, cargo, hierarquia, etc.
- **Campos removidos**: Dados pessoais (CPF, RG) são excluídos para proteger privacidade.

**Exemplo:**
| pessoa | date_key   | funcao_sk | centro_de_custo_sk | tempo_empresa_key | salario |
|--------|------------|-----------|--------------------|-------------------|---------|
| 1001   | 01.01.2024 | FGH456    | CC789              | 365               | 5.000   |

---

### **7.2. Tabela Fato de Desligamentos (`gd_termination_f`)**
**O que contém?**
- **Funcionários desligados**, com motivo, data e tempo na empresa.

**Exemplo:**
| pessoa | date_key   | motivo_desligamento | tempo_empresa_key |
|--------|------------|---------------------|-------------------|
| 1002   | 15.03.2024 | Demissão            | 1.095             |

---

### **7.3. Tabela Fato de Orçamento (`gd_excel_hc_orcamento_historico_f`)**
**O que contém?**
- **Metas de contratação** (orçamento planejado vs. real).

---

### **7.4. Tabela Fato de Posições (`gd_posicoes_f`)**
**O que contém?**
- **Cargos disponíveis** na empresa (mesmo sem ocupantes).

---
## **8. Atualização das Dimensões de Desligamento**
As dimensões de **situação**, **status** e **tipo de funcionário** são atualizadas com dados de desligamentos para garantir consistência.

---
## **9. Limpeza Final**
Ao final, o script **exclui tabelas temporárias** para liberar memória e evitar redundâncias.

---
## **10. Resumo do Fluxo de Dados**
1. **Configurações iniciais** (formatação, caminhos).
2. **Criação de tabelas de suporte** (calendário, tempo na empresa).
3. **Carregamento dos dados brutos** (Silver → Gold).
4. **Criação de dimensões** (funcionários, hierarquias, cargos).
5. **Criação de tabelas fato** (headcount, desligamentos, orçamento).
6. **Atualização de dimensões** (desligamentos).
7. **Exclusão de tabelas temporárias**.

---
## **11. Glossário de Termos**
| Termo               | Significado                                                                 |
|---------------------|---------------------------------------------------------------------------|
| **Headcount**       | Contagem de funcionários ativos.                                          |
| **Hash128**         | Código único gerado para relacionar tabelas (ex.: `hierarquia_sk`).      |
| **Fato**           | Tabela com métricas (ex.: salários, desligamentos).                       |
| **Dimensão**       | Tabela com descrições (ex.: cargos, filiais).                              |
| **QVD**            | Formato de arquivo do Qlik (semelhante a um banco de dados compactado).   |
| **NoConcatenate**  | Garante que tabelas não sejam mescladas automaticamente.                  |

---
## **12. Exemplo Prático de Análise**
**Pergunta:** *"Quantos funcionários com menos de 1 ano na empresa foram contratados em 2024?"*

**Como o script ajuda?**
1. **Filtra por `date_key`** (datas de 2024).
2. **Usa `tempo_empresa_key`** para selecionar funcionários com menos de 365 dias.
3. **Conta registros** na tabela `gd_headcount_f`.

**Resultado possível:**
| Ano | Funcionários com <1 ano | % do Total |
|-----|-------------------------|------------|
| 2024| 120                     | 15%        |

---
## **13. Conclusão**
Este script **automatiza a transformação de dados de RH**, tornando-os prontos para análise em ferramentas como **Qlik Sense, Power BI ou Tableau**. Ele:
- **Organiza informações** em tabelas dimensionais e fatos.
- **Padroniza formatos** (datas, moedas, textos).
- **Facilita relatórios** sobre headcount, turnover, orçamento e muito mais.

Com essa estrutura, gestores podem tomar decisões baseadas em dados **confiáveis e bem estruturados**.
