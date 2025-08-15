# Documentação Técnica

**Arquivo:** `headcount.qvs`  
**Última atualização:** 15/08/2025 10:03:24

# **Documentação do Script QVS – Processamento de Dados de Recursos Humanos**
*(Explicação detalhada e acessível sobre o funcionamento do script)*

---

## **1. Introdução**
Este documento explica, de forma clara e organizada, o que faz o script **QVS** (QlikView Script) apresentado. O script é responsável por **processar e transformar dados de Recursos Humanos (RH)**, preparando-os para análise em ferramentas como Qlik Sense ou QlikView.

O objetivo principal é **organizar informações sobre funcionários, demissões, cargos, salários e hierarquias** em um formato padronizado, facilitando relatórios e tomadas de decisão.

---
---

## **2. Estrutura Geral do Script**
O script está dividido em **etapas lógicas**, cada uma com uma função específica:

1. **Configurações Iniciais** – Define formatações de dados (moeda, data, idioma).
2. **Caminhos de Arquivos** – Indica onde os dados estão armazenados.
3. **Carregamento de Dados Brutos** – Importa tabelas com informações de funcionários, cargos, salários, etc.
4. **Transformações e Regras de Negócio** – Aplica cálculos, classificações e padronizações.
5. **Geração de Tabelas Finais** – Cria versões processadas dos dados para uso em relatórios.
6. **Limpeza de Tabelas Temporárias** – Remove dados desnecessários após o processamento.

---
---

## **3. Configurações Iniciais**
### **3.1. Formatação de Dados**
O script começa definindo como os dados devem ser exibidos:
- **Separadores numéricos**:
  - `ThousandSep='.'` → Milhares separados por ponto (ex: `1.000`).
  - `DecimalSep=','` → Decimais separados por vírgula (ex: `R$ 1.000,50`).
- **Formato de moeda**: `R$#.##0,00;-R$#.##0,00` → Valores monetários no padrão brasileiro.
- **Formato de data e hora**:
  - `DD.MM.YYYY` (ex: `15.05.2023`).
  - `hh:mm:ss` (ex: `14:30:00`).
- **Idioma**: `pt-BR` (português do Brasil).
- **Primeiro dia da semana**: Domingo (`FirstWeekDay=6`).

### **3.2. Caminhos dos Arquivos (Pastas de Dados)**
O script define onde estão os arquivos de origem e destino:
- **Bronze Layer**: Dados brutos (origem).
- **Silver Layer**: Dados processados (destino).
- **Gold Layer**: Dados finais para relatórios.
- **Manual Source**: Fontes manuais (ex: planilhas).
- **TI Layer e External Layer**: Outras fontes de dados.

---
---

## **4. Carregamento de Dados Brutos**
Nesta etapa, o script **importa tabelas** com informações de RH armazenadas em arquivos `.QVD` (formato do Qlik). Cada tabela contém um tipo específico de dado:

| **Tabela**                          | **Descrição**                                                                 |
|-------------------------------------|-------------------------------------------------------------------------------|
| `bz_headcount_f`                    | Lista de funcionários ativos e seus dados (matrícula, nome, cargo, salário). |
| `bz_headcount_hist_f`               | Histórico de movimentações de funcionários (admissões, demissões).          |
| `bz_headcount_latest_f`             | Dados mais recentes dos funcionários.                                        |
| `bz_posicoes_f`                     | Cargos/vagas disponíveis na empresa.                                         |
| `bz_pessoa_d`                       | Dados pessoais (CPF, RG, endereço, estado civil).                            |
| `bz_hierarquia_d`                   | Hierarquia organizacional (quem reporta a quem).                            |
| `bz_excel_funcao_d`                 | Descrição dos cargos (nome, código, carreira).                               |
| `bz_excel_range_salario_d`          | Faixas salariais por cargo.                                                   |
| `bz_externo_centro_custo_d`         | Centros de custo (áreas/departamentos da empresa).                           |

---
---

## **5. Transformações e Regras de Negócio**
### **5.1. Tabelas de Mapeamento (MAPPING LOAD)**
São criadas **tabelas de referência** para padronizar informações:
- **`coligada_d`**: Lista de empresas do grupo (ex: Eldorado, Florestal).
- **`CLASSIFICAÇÃO_MAP`**: Classifica demissões como "Voluntárias" ou "Involuntárias".
- **`MAP_EVENTOS`**: Tipos de eventos (férias, horas extras, atestados).
- **`Map_funcao`**: Relaciona nomes de cargos aos seus códigos.

### **5.2. Processamento de Centros de Custo**
- **Filtra centros de custo inválidos** (ex: vazios ou com "#").
- **Classifica diretorias** em grupos (ex: "Corporativo", "Industrial").
- **Armazena em `sv_centro_de_custo_d.QVD`** para uso posterior.

### **5.3. Processamento de Funções (Cargos)**
- **Padroniza códigos de cargo** (ex: `00123`).
- **Classifica cargos** como "Líder" ou "Não Líder".
- **Define se são operacionais ou não** (ex: "Técnico" vs. "Administrativo").
- **Armazena em `sv_funcao_d.QVD`**.

### **5.4. Processamento de Headcount (Funcionários)**
#### **a) Tratamento de Admissões e Demissões no Mesmo Mês**
- Identifica funcionários **admitidos e demitidos no mesmo mês** (ex: contratações temporárias).
- **Marca esses casos** com um status especial (`Situação = 'C/Dem no mês'`).

#### **b) Consolidação dos Dados**
- **Une tabelas** de headcount histórico, atual e offshore.
- **Aplica filtros** para excluir:
  - Funcionários com centros de custo inválidos.
  - Tipos de funcionários não relevantes (ex: estagiários, conselheiros).
  - Matrículas específicas (ex: testes ou registros obsoleto).

#### **c) Cálculos e Classificações**
- **Tempo de empresa** (em dias e anos).
- **Classificação por idade** (ex: "Até 30 anos", "Acima de 50 anos").
- **Status de contratação** (ex: "Novo Contratado" se menos de 1 ano na empresa).
- **Faixas salariais** (ex: "Entre 80% e 90%" da média do cargo).

#### **d) Junção com Outras Tabelas**
- **Hierarquia**: Quem é gestor de quem.
- **Dados pessoais**: CPF, endereço, estado civil.
- **Centros de custo**: Departamento do funcionário.
- **Faixas salariais**: Compara salário com a média do cargo.

#### **e) Geração da Tabela Final (`sv_headcount_f`)**
- **Armazena em `sv_headcount_f.QVD`** com todos os dados processados.

---
### **5.5. Processamento de Demissões (`sv_termination_f`)**
- **Filtra apenas demissões** (exclui transferências ou falecimentos).
- **Classifica demissões** como voluntárias/involuntárias.
- **Calcula tempo de empresa** até a demissão.
- **Inclui dados de hierarquia, salário e motivos da demissão**.
- **Armazena em `sv_termination_f.QVD`**.

---
### **5.6. Processamento de Orçamento Histórico**
- **Carrega dados de orçamento** (previsão de headcount por centro de custo).
- **Armazena em `sv_excel_hc_orcamento_historico_f.QVD`**.

---
### **5.7. Processamento de Posições (Vagas)**
- **Filtra vagas ativas** (exclui aprendizes ou vagas sem responsável).
- **Classifica por status** (ex: "Em Andamento", "Substituição").
- **Armazena em `sv_posicoes_f.QVD`**.

---
---

## **6. Limpeza de Tabelas Temporárias**
Ao final, o script **remove tabelas temporárias** usadas durante o processamento para:
- Liberar memória.
- Evitar confusão com dados desatualizados.

---
---

## **7. Exemplo Prático: Fluxo de um Funcionário**
Para ilustrar como o script funciona, acompanhe o **caminho de um funcionário fictício** chamado *Ana Silva*:

1. **Dados Brutos (`bz_headcount_f`)**:
   - Matrícula: `12345`
   - Nome: `Ana Silva`
   - Cargo: `Analista de RH`
   - Salário: `R$ 4.500,00`
   - Data de Admissão: `15.01.2020`
   - Centro de Custo: `1001` (RH)

2. **Processamento**:
   - O script **calcula seu tempo de empresa** (ex: 3 anos em 2023).
   - **Classifica seu cargo** como "Não Líder" e "Não Operacional".
   - **Verifica sua faixa salarial** (ex: "Entre 90% e 100%" da média).
   - **Identifica seu gestor** (ex: *Carlos Oliveira*, do centro de custo `1000`).

3. **Resultado Final (`sv_headcount_f`)**:
   - Ana aparece na tabela com todos os dados padronizados, pronta para relatórios.

---
---

## **8. Resumo dos Arquivos Gerados**
| **Arquivo Gerado**                     | **Descrição**                                                                 |
|----------------------------------------|-------------------------------------------------------------------------------|
| `sv_headcount_f.QVD`                   | Lista completa de funcionários com dados detalhados.                        |
| `sv_termination_f.QVD`                 | Registros de demissões com motivos e classificações.                        |
| `sv_centro_de_custo_d.QVD`             | Centros de custo e suas hierarquias.                                        |
| `sv_funcao_d.QVD`                      | Cargos da empresa com códigos e classificações.                             |
| `sv_posicoes_f.QVD`                    | Vagas abertas e suas características.                                       |
| `sv_excel_hc_orcamento_historico_f.QVD`| Histórico de orçamento de headcount por área.                              |

---
---

## **9. Considerações Finais**
### **Para que serve este script?**
- **Automatizar** o processamento de dados de RH.
- **Padronizar** informações para evitar erros em relatórios.
- **Facilitar análises** como:
  - Taxa de turnover (rotatividade).
  - Distribuição de funcionários por idade, cargo ou departamento.
  - Comparação entre salários e faixas de mercado.

### **Quem se beneficia?**
- **Analistas de RH**: Para criar relatórios precisos.
- **Gestores**: Para tomar decisões baseadas em dados.
- **Área de Folha de Pagamento**: Para validar consistência de informações.

---
**Fim da Documentação**
