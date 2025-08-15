# Documentação Técnica

**Arquivo:** `headcount.qvs`  
**Última atualização:** 15/08/2025 11:54:14

# **Documentação do Script QVS – Processamento de Dados de Recursos Humanos**

## **1. Introdução**
Este documento explica, de forma clara e organizada, o funcionamento de um script utilizado para processar e preparar dados de **Recursos Humanos (RH)** em um ambiente de análise. O objetivo principal é transformar informações brutas (como registros de funcionários, demissões, cargos e hierarquias) em tabelas estruturadas, prontas para serem usadas em relatórios e painéis de gestão.

O script segue uma abordagem de **camadas de dados** (Bronze, Silver e Gold), onde:
- **Bronze**: Dados originais, sem tratamento.
- **Silver**: Dados limpos, enriquecidos e padronizados.
- **Gold**: Dados prontos para análise, com indicadores e métricas calculadas.

---

## **2. Configurações Iniciais**
Antes de processar os dados, o script define padrões de formatação para garantir que números, datas, moedas e textos sejam exibidos de maneira consistente, seguindo o padrão brasileiro.

### **2.1. Formatação de Números e Moedas**
- **Separador de milhar**: `.` (ponto) → Exemplo: `1.000`
- **Separador decimal**: `,` (vírgula) → Exemplo: `R$ 1.234,56`
- **Formato de moeda**: `R$` (Real brasileiro), com duas casas decimais.

### **2.2. Formatação de Data e Hora**
- **Data**: `DD.MM.AAAA` → Exemplo: `15.05.2024`
- **Hora**: `hh:mm:ss` → Exemplo: `14:30:00`
- **Primeiro dia da semana**: Domingo (configurado como `6`).
- **Idioma**: Português do Brasil (`pt-BR`), para nomes de meses e dias.

### **2.3. Caminhos dos Arquivos (Pastas de Dados)**
O script define onde os dados serão lidos e salvos, usando **caminhos lógicos** (como `lib://`), que apontam para pastas específicas no servidor. Exemplos:
- **Bronze**: Dados brutos (`bz_headcount_f.QVD`).
- **Silver**: Dados processados (`sv_headcount_f.QVD`).
- **Gold**: Dados finais para análise.
- **Manual Source**: Dados inseridos manualmente.
- **Fontes Externas**: Dados de sistemas externos.

---
## **3. Carregamento dos Dados Brutos (Bronze)**
Nesta etapa, o script **lê os arquivos originais** (no formato `.QVD`, um tipo de arquivo otimizado para dados) e os armazena em tabelas temporárias para processamento.

### **3.1. Tabelas Carregadas**
| **Tabela** | **Descrição** |
|------------|---------------|
| `bz_headcount_f` | Registros atuais de funcionários (matrícula, nome, cargo, salário, etc.). |
| `bz_headcount_hist_f` | Histórico de movimentações de funcionários (admissões, demissões, transferências). |
| `bz_headcount_latest_f` | Último registro de cada funcionário (dados mais recentes). |
| `bz_posicoes_f` | Posições (vagas) abertas ou ocupadas na empresa. |
| `bz_pessoa_d` | Dados pessoais dos funcionários (CPF, RG, endereço, etc.). |
| `bz_hierarquia_d` | Hierarquia organizacional (quem reporta a quem). |
| `bz_excel_funcao_d` | Catálogo de cargos (códigos, descrições, níveis hierárquicos). |
| `bz_externo_centro_custo_d` | Centros de custo (áreas ou departamentos da empresa). |

---
## **4. Tabelas de Mapeamento (Dicionários)**
Para padronizar informações, o script usa **tabelas de mapeamento**, que funcionam como "dicionários" para traduzir códigos em nomes legíveis.

### **4.1. Exemplos de Mapeamentos**
| **Mapeamento** | **Finalidade** |
|----------------|----------------|
| `coligada_d` | Converte códigos de empresas do grupo (ex: `1 = Eldorado`, `2 = Florestal`). |
| `CLASSIFICAÇÃO_MAP` | Classifica demissões como **Voluntárias** ou **Involuntárias**. |
| `MAP_EVENTOS` | Traduz códigos de eventos (ex: `2 = Salário Bruto`, `5 = Férias`). |
| `Map_funcao` | Associa nomes de cargos aos seus códigos (ex: `Analista = 10001`). |

---
## **5. Processamento dos Dados (Silver)**
Nesta fase, os dados brutos são **limpos, enriquecidos e transformados** em tabelas estruturadas para análise.

### **5.1. Tabelas Processadas**
#### **a) Centro de Custo (`sv_centro_de_custo_d`)**
- **O que faz**: Organiza os centros de custo (departamentos) e os classifica em grupos (ex: `Corporativo`, `Industrial`, `Florestal`).
- **Exemplo**:
  - Código `1000` → Departamento `Financeiro` → Grupo `Corporativo`.

#### **b) Funções (`sv_funcao_d`)**
- **O que faz**: Padroniza os cargos, classificando-os como **Líder/Não Líder** e **Operacional/Não Operacional**.
- **Exemplo**:
  - Cargo `Gerente de Produção` → **Líder** e **Não Operacional**.

#### **c) Headcount (`sv_headcount_f`)**
- **O que faz**: Consolida todos os registros de funcionários, calculando métricas como:
  - Tempo na empresa.
  - Faixa salarial (ex: `Entre 90% e 100% do salário de referência`).
  - Status (`Ativo`, `Afastado`, `Novo Contratado`).
  - Hierarquia (quem é o gestor direto).
- **Exemplo de cálculo**:
  - Se um funcionário foi admitido em `01.01.2024` e hoje é `15.05.2024`, o script calcula que ele está há **135 dias** na empresa.

#### **d) Demissões (`sv_termination_f`)**
- **O que faz**: Registra funcionários demitidos, classificando:
  - Tipo de demissão (`Voluntária` ou `Involuntária`).
  - Motivo (`Aposentadoria`, `Desempenho`, etc.).
  - Se o funcionário era **novo** (menos de 1 ano na empresa).
- **Exemplo**:
  - Um funcionário demitido com código `2` → Classificado como **Involuntário**.

#### **e) Posições (`sv_posicoes_f`)**
- **O que faz**: Lista vagas abertas ou em processo de preenchimento, indicando:
  - Status (`Em Andamento`, `Concluída`).
  - Se é para **aprendiz** ou **estagiário**.
- **Exemplo**:
  - Vaga `Analista de TI` → Status `Em Andamento` → Não é para aprendiz.

---
## **6. Regras de Negócio Aplicadas**
O script aplica **regras específicas** para garantir que os dados reflitam a realidade do negócio.

### **6.1. Exemplos de Regras**
| **Regra** | **Descrição** |
|-----------|---------------|
| **Funcionários admitidos e demitidos no mesmo mês** | São marcados como `C/Dem no mês` para não distorcer métricas de turnover. |
| **Exclusão de registros inválidos** | Remove matrículas vazias (`''`), funcionários com tipo `U` (Outros) ou `S` (Pensionista). |
| **Cálculo de faixa salarial** | Compara o salário do funcionário com a referência do cargo (ex: `90% do salário padrão`). |
| **Classificação por idade** | Agrupa funcionários em `Até 30 anos`, `31 a 50 anos` ou `Acima de 50 anos`. |
| **Identificação de gestores** | Define quem é o gestor direto de cada funcionário, buscando na hierarquia. |

---
## **7. Salvamento dos Dados Processados (Silver)**
Após o processamento, as tabelas são **salvas em arquivos `.QVD`** na pasta **Silver**, prontas para serem usadas em relatórios ou painéis.

### **7.1. Tabelas Salvas**
| **Tabela** | **Arquivo Gerado** | **Uso** |
|------------|--------------------|---------|
| `sv_centro_de_custo_d` | `sv_centro_de_custo_d.QVD` | Análise por departamento. |
| `sv_funcao_d` | `sv_funcao_d.QVD` | Catálogo de cargos. |
| `sv_headcount_f` | `sv_headcount_f.QVD` | Base principal de funcionários. |
| `sv_termination_f` | `sv_termination_f.QVD` | Registros de demissões. |
| `sv_posicoes_f` | `sv_posicoes_f.QVD` | Vagas abertas. |

---
## **8. Limpeza Final**
Ao final, o script **exclui as tabelas temporárias** para liberar memória e evitar conflitos em execuções futuras.

---
## **9. Resumo do Fluxo de Dados**
1. **Leitura**: Dados brutos são carregados da camada **Bronze**.
2. **Transformação**: Dados são limpos, enriquecidos e calculados.
3. **Salvamento**: Tabelas processadas são salvas na camada **Silver**.
4. **Uso**: Os dados estão prontos para análise em relatórios ou dashboards.

---
## **10. Exemplos Práticos**
### **Exemplo 1: Cálculo de Tempo na Empresa**
- **Dados brutos**:
  - `Data Admissão`: `01.01.2020`
  - `Data Atual`: `15.05.2024`
- **Cálculo do script**:
  - `(15.05.2024 - 01.01.2020) = 4 anos e 4 meses` → `1.584 dias`.
  - Classificado como **Não Novo Contratado** (mais de 1 ano).

### **Exemplo 2: Classificação de Demissão**
- **Dados brutos**:
  - `Tipo de Demissão`: `2` (Código para demissão por desempenho).
- **Aplicação do mapeamento**:
  - `2` → `Involuntário` (segundo a tabela `CLASSIFICAÇÃO_MAP`).

### **Exemplo 3: Identificação de Gestor**
- **Dados brutos**:
  - Hierarquia do funcionário `A`:
    - Nível 1: `João` (código `1001`)
    - Nível 2: `Maria` (código `1002`)
- **Resultado**:
  - Gestor direto de `A` = `Maria` (primeiro nível acima na hierarquia).

---
## **11. Conclusão**
Este script é uma **ferramenta essencial** para preparar dados de RH, permitindo que a empresa:
- **Monitore o quadro de funcionários** (admissões, demissões, transferências).
- **Analise métricas-chave** (turnover, tempo na empresa, faixa salarial).
- **Tome decisões baseadas em dados** (ex: contratações, treinamentos, políticas de retenção).

Ao seguir uma estrutura organizada (Bronze → Silver → Gold), garante-se que os dados sejam **confiáveis, consistentes e úteis** para a gestão.
