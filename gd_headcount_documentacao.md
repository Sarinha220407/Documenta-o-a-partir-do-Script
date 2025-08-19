# Documentação Técnica

**Arquivo:** `gd_headcount.qvs`  
**Última atualização:** 15/08/2025 13:49:52

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos (RH)**
*Objetivo:* Explicar as regras de inclusão, exclusão e condicionais aplicadas aos indicadores do dashboard de RH, garantindo clareza para usuários finais não técnicos.

---

## **1. Visão Geral**
### **Objetivo do Documento**
- Detalhar **o que é contado** e **o que não é contado** em cada métrica do dashboard.
- Explicar **critérios de segmentação** (ex.: por tempo de empresa, faixa etária, tipo de contratação).
- Orientar como identificar se um registro deve ou não ser incluído nos cálculos.

### **Princípios Gerais**
Todas as métricas seguem regras específicas para:
- **Inclusão:** Quais registros são válidos para o cálculo.
- **Exclusão:** Quais registros são ignorados e por quê.
- **Casos Especiais:** Exceções ou tratamentos diferenciados.

---
## **2. Regras de Negócio por Indicador/Métrica**

---

### **2.1 Headcount (Número de Funcionários Ativos)**
**Definição:**
Total de funcionários **ativos** na empresa em um determinado período, considerando sua situação contratual e tipo de vínculo.

#### **Critérios de Inclusão**
- Funcionários com **status = "Ativo"** na data de referência.
- Todos os **tipos de contratação** (CLT, temporários, estagiários, etc.), **exceto** os listados em "Exclusões".
- Funcionários com **jornada mensal definida** (mesmo que parcial).
- Funcionários **readmitidos** (contados como novos registros, mas com flag de readmissão).

#### **Critérios de Exclusão**
- Funcionários com **status = "Desligado"** (mesmo que a data de desligamento seja recente).
- **Funcionários sem vínculo formal** (ex.: prestadores de serviço PJ sem registro na folha).
- **Funcionários em licença não remunerada** (exceto se a situação contratual permanecer como "Ativo").
- **Registros duplicados** (mesma pessoa com mesmo código em datas sobrepostas).
- **Funcionários com data de admissão futura** (ainda não iniciaram).

#### **Casos Especiais**
- **Funcionários em transição de cargo:**
  - Se a mudança ocorrer **dentro do mesmo mês**, o funcionário é contado **apenas uma vez**, no cargo mais recente.
  - Se a transição envolver **mudança de centro de custo**, o funcionário é contabilizado no novo centro a partir da data efetiva.
- **Funcionários com múltiplos vínculos:**
  - Contados **uma vez por pessoa**, independentemente do número de cargos ou centros de custo.
- **Trainees e estagiários:**
  - Incluídos no headcount, mas **segmentados separadamente** por tipo de contratação.

---

### **2.2 Turnover (Rotatividade)**
**Definição:**
Porcentagem de funcionários que **saíram da empresa** em um período, em relação ao headcount médio do mesmo período.

#### **Critérios de Inclusão**
- **Desligamentos voluntários ou involuntários** com data de término **dentro do período analisado**.
- Funcionários com **situação = "Desligado"** e **tipo de desligamento registrado** (demissão, aposentadoria, falecimento, etc.).
- **Readmissões não são consideradas saídas** (o funcionário não entra no cálculo de turnover se foi readmitido no mesmo período).

#### **Critérios de Exclusão**
- **Transferências internas** (mudança de cargo/área sem desligamento).
- **Funcionários em licença médica ou afastamentos temporários** (não contam como desligados).
- **Desligamentos com data futura** (ex.: aviso prévio ainda em curso).
- **Funcionários com registro de desligamento duplicado** (apenas a primeira ocorrência é considerada).

#### **Casos Especiais**
- **Desligamentos por falecimento ou aposentadoria:**
  - Contabilizados no turnover, mas **segmentados em relatórios específicos**.
- **Funcionários com tempo de empresa < 30 dias:**
  - Incluídos no turnover, mas **identificados como "Desligamentos Precoces"** em análises detalhadas.

---

### **2.3 Tempo de Empresa (Time in Company)**
**Definição:**
Tempo que um funcionário permanece na empresa, medido em **dias, meses ou anos**, e agrupado em faixas para análise.

#### **Critérios de Inclusão**
- **Todos os funcionários ativos ou desligados** com data de admissão registrada.
- **Tempo calculado até a data de referência** (para ativos) ou até a data de desligamento (para inativos).

#### **Critérios de Exclusão**
- Funcionários **sem data de admissão válida** (ex.: campo nulo ou data futura).
- **Funcionários com readmissão:**
  - O tempo é **zerado na readmissão** (novo ciclo de contagem).

#### **Faixas de Agrupamento**
| **Grupo**               | **Faixa (Anos)**       | **Faixa (Meses - Operacional)** |
|-------------------------|------------------------|--------------------------------|
| Novo Funcionário        | –                      | 0–3 meses                      |
| Iniciante               | –                      | 3–6 meses                      |
| Consolidação            | –                      | 6–12 meses                     |
| Ano 1                   | 0–1                    | –                              |
| Ano 2                   | 1–2                    | –                              |
| Ano 3–4                 | 3–4                    | –                              |
| Ano 5–9                 | 5–9                    | –                              |
| Ano 10–14               | 10–14                  | –                              |
| Ano 15+                  | 15+                    | –                              |
| Operacional (curto prazo)| –                      | 0–12 meses                     |
| Operacional (longo prazo)| 1–4 anos               | –                              |

---
### **2.4 Vagas Abertas (Posições Disponíveis)**
**Definição:**
Total de **posições autorizadas** (orçamentadas) que estão **vagas** (sem ocupante) em um determinado período.

#### **Critérios de Inclusão**
- Posições com **centro de custo ativo** e **cargo definido** no sistema.
- Vagas **aprovadas no orçamento** (mesmo que ainda não preenchidas).
- Posições **temporariamente vagas** (ex.: licença-maternidade, afastamento médico).

#### **Critérios de Exclusão**
- Posições **arquivadas ou desativadas** (sem previsão de preenchimento).
- Vagas **sem centro de custo vinculado**.
- Posições **ocupadas por funcionários ativos** (mesmo que em processo de transição).

#### **Casos Especiais**
- **Vagas sazonais:**
  - Contabilizadas apenas no período de necessidade (ex.: contratações para fim de ano).
- **Vagas em processo de realocação:**
  - Não contam como vagas abertas se houver um funcionário já designado para ocupá-las.

---
### **2.5 Taxa de Ocupação**
**Definição:**
Porcentagem de **posições preenchidas** em relação ao **total de posições orçamentadas**.

#### **Fórmula:**
```
Taxa de Ocupação = (Headcount Ativo / Total de Posições Orçamentadas) × 100
```

#### **Critérios de Inclusão**
- **Headcount ativo** na data de referência.
- **Total de posições orçamentadas** (inclui vagas abertas e ocupadas).

#### **Critérios de Exclusão**
- Posições **não orçamentadas** (ex.: cargos criados sem aprovação formal).
- Funcionários **em desligamento** (aviso prévio) não são contados como ocupantes.

---
### **2.6 Admissões (New Hires)**
**Definição:**
Total de **novos funcionários admitidos** em um período, segmentados por tipo de contratação.

#### **Critérios de Inclusão**
- Funcionários com **data de admissão dentro do período analisado**.
- Todos os **tipos de contratação** (CLT, estagiários, trainees, etc.).
- **Readmissões** são contadas como novas admissões (mas com flag específica).

#### **Critérios de Exclusão**
- **Transferências internas** (não são novas admissões).
- **Funcionários com data de admissão futura**.
- **Registros duplicados** (mesma pessoa com mesma data).

#### **Casos Especiais**
- **Contratações temporárias:**
  - Contabilizadas como admissões, mas **segmentadas por duração do contrato**.
- **Funcionários com admissão retroativa:**
  - A data considerada é a **data de registro no sistema**, não a data real de início.

---
### **2.7 Faixas Etárias e Gerações**
**Definição:**
Segmentação dos funcionários por **idade** e **geração**, para análises demográficas.

#### **Faixas de Idade**
| **Grupo**      | **Idade**  | **Geração**               |
|----------------|------------|---------------------------|
| 0–14           | 0–14       | Geração Alpha (2011–hoje) |
| 15–29          | 15–29      | Geração Z (1996–2010)     |
| 30–44          | 30–44      | Geração Y (1981–1995)     |
| 45–60          | 45–60      | Geração X (1965–1980)     |
| 61–79          | 61–79      | Boomers (1946–1964)       |
| 79+            | 79+        | Geração Silenciosa        |

#### **Critérios de Inclusão**
- Funcionários com **data de nascimento registrada**.
- Idade calculada com base na **data de referência do relatório**.

#### **Critérios de Exclusão**
- Funcionários **sem data de nascimento** (idade não pode ser calculada).

---
### **2.8 Tipo de Funcionário**
**Definição:**
Classificação dos funcionários por **tipo de vínculo empregatício**.

#### **Tipos Comuns**
| **Tipo**               | **Descrição**                                  |
|------------------------|------------------------------------------------|
| CLT                    | Contrato por tempo indeterminado.             |
| Temporário             | Contrato por prazo determinado.               |
| Estagiário             | Vinculado a programas de estágio.              |
| Trainee                | Programa de trainees.                          |
| Terceirizado           | Prestador de serviço via empresa terceira.    |
| Aposentado             | Funcionários aposentados ainda na folha.      |

#### **Critérios de Inclusão**
- Todos os tipos **registrados no sistema**.

#### **Critérios de Exclusão**
- **Prestadores de serviço PJ** sem vínculo formal com a empresa.
- **Funcionários sem tipo definido** (campo nulo).

---
## **3. Condicionais e Classificações**
### **Como os Dados São Segmentados**
Os indicadores podem ser filtrados por:

#### **Por Período**
- **Data de referência:** Dia, mês ou ano específico.
- **Status temporal:**
  - **Histórico:** Dados de períodos passados.
  - **Futuro:** Projeções ou dados ainda não consolidados (ex.: orçamento).

#### **Por Faixa de Valor**
- **Tempo de empresa:** Ex.: "Funcionários com menos de 1 ano".
- **Faixa etária:** Ex.: "Geração Y (30–44 anos)".
- **Faixa salarial:** Ex.: "Salário entre R$ 3.000 e R$ 5.000".

#### **Por Categoria**
- **Tipo de contratação:** CLT, temporário, estagiário.
- **Situação:** Ativo, desligado, licença.
- **Área/Diretoria:** Ex.: "Diretoria de Operações".
- **Região/Filial:** Ex.: "Funcionários da filial São Paulo".

#### **Por Status**
- **Ativo vs. Inativo.**
- **New Hire (novo funcionário):** Funcionários com menos de 1 ano de empresa.
- **Final de semana:** Dados de dias não úteis (para análises de produtividade).

---
## **4. Campos e Flags de Apoio**
Campos utilizados para aplicar as regras de negócio:

| **Campo**                  | **Descrição**                                                                 |
|----------------------------|-------------------------------------------------------------------------------|
| **headcount_status**       | Indica se o funcionário está "Ativo" ou "Desligado".                          |
| **tempo_empresa_dias**     | Quantidade de dias que o funcionário está na empresa.                        |
| **new_hire_flag**          | "TRUE" se o funcionário tem menos de 1 ano de empresa.                       |
| **situacao_cod**           | Código da situação (ex.: 1 = Ativo, 2 = Desligado).                         |
| **tipo_funcionario_cod**  | Tipo de vínculo (ex.: CLT, temporário).                                      |
| **contratacao_tipo**       | Como o funcionário foi contratado (ex.: admissão normal, trainee).           |
| **grupo_gerencial**        | Faixa de tempo de empresa para análises gerenciais (ex.: "Ano 5–9").          |
| **grupo_operacional**      | Faixa de tempo de empresa para análises operacionais (ex.: "0–6 meses").     |
| **periodo_status**         | Classifica a data como "Histórico" ou "Futuro".                              |
| **final_semana**           | "Sim" se a data é sábado ou domingo.                                          |

---
## **5. O que é Incluído e o que é Excluído no Dashboard**

### **Resumo Geral**
| **Métrica**          | **Incluído**                                                                 | **Excluído**                                                                 |
|----------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Headcount**        | Funcionários ativos, com vínculo formal e data de admissão válida.         | Desligados, sem vínculo, duplicados, admissões futuras.                      |
| **Turnover**         | Desligamentos voluntários/involuntários no período.                        | Transferências internas, licenças, desligamentos futuros.                   |
| **Tempo de Empresa** | Funcionários com data de admissão registrada.                              | Sem data de admissão, readmissões (tempo zerado).                            |
| **Vagas Abertas**    | Posições orçamentadas e vagas (ativas ou temporárias).                     | Posições desativadas, sem centro de custo.                                   |
| **Taxa de Ocupação** | Headcount ativo + posições orçamentadas.                                   | Posições não orçamentadas, funcionários em desligamento.                   |
| **Admissões**        | Novos funcionários com data de admissão no período.                        | Transferências, admissões futuras, duplicados.                              |
| **Faixas Etárias**   | Funcionários com data de nascimento registrada.                            | Sem data de nascimento.                                                      |
| **Tipo de Funcionário** | Todos os tipos de vínculo registrados.                                   | Sem tipo definido, prestadores PJ sem registro.                             |

---
## **6. Glossário**
| **Termo**               | **Definição**                                                                 |
|-------------------------|------------------------------------------------------------------------------|
| **Headcount**           | Contagem total de funcionários ativos em um período.                        |
| **Turnover**            | Taxa de rotatividade (saída de funcionários em relação ao headcount médio).  |
| **New Hire**            | Funcionário com menos de 1 ano de empresa.                                  |
| **Readmissão**          | Funcionário que retornou à empresa após desligamento.                       |
| **Centro de Custo**     | Unidade organizacional que agrega despesas (ex.: departamento, projeto).     |
| **Escala/Jornada**      | Regime de trabalho (ex.: 44h semanais, 12x36).                              |
| **Situação**            | Status do funcionário (Ativo, Desligado, Licença).                           |
| **Orçamento de HC**     | Planejamento de posições (vagas) aprovadas para um período.                 |
| **Geração (Y, Z, etc.)**| Classificação por faixa etária e período de nascimento.                     |
| **Flag**                | Indicador booleano (Sim/Não, TRUE/FALSE) para classificações específicas.    |
| **Hash/Chave (SK)**     | Código único gerado para agrupar dados sem exposição de informações sensíveis.|
