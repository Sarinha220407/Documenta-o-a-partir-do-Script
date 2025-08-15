# Documentação Técnica

**Arquivo:** `People Analytics Model.qvs`  
**Última atualização:** 15/08/2025 13:54:10

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos**
*Objetivo:* Explicar as regras de inclusão, exclusão e condicionais aplicadas às métricas do dashboard de **Recursos Humanos**, garantindo clareza para usuários finais não técnicos.

---

## **1. Visão Geral**
### **Objetivo do Documento**
- Detalhar **o que é contado** e **o que não é contado** em cada métrica do dashboard.
- Explicar **critérios de segmentação** (ex.: por período, tipo de funcionário, situação).
- Orientar como identificar **casos especiais** ou exceções nas regras.

### **Como os Dados São Estruturados**
Cada métrica segue **regras específicas** para:
- **Inclusão:** Quais registros são considerados válidos.
- **Exclusão:** Quais registros são ignorados (ex.: dados incompletos, situações temporárias).
- **Classificação:** Como os dados são agrupados (ex.: por faixa etária, tipo de contratação).

---
## **2. Regras de Negócio por Indicador/Métrica**

### **2.1 Headcount (Número de Funcionários Ativos)**
**Definição:**
Total de funcionários **ativos** na empresa em um determinado período.

#### **Critérios de Inclusão**
- Funcionários com **situação ativa** (ex.: em exercício, afastados por licença médica ou férias).
- Funcionários com **vínculo empregatício formal** (CLT, temporários, terceirizados *quando aplicável*).
- Funcionários **alocados em qualquer unidade ou centro de custo** da empresa.

#### **Critérios de Exclusão**
- Funcionários **desligados** (demitidos, aposentados, falecidos).
- Candidatos em **processo seletivo** (ainda não contratados).
- Estagiários ou aprendizes **sem registro em folha** (quando não considerados como headcount pela política da empresa).
- Registros com **dados incompletos** (ex.: falta de matrícula, centro de custo não identificado).

#### **Casos Especiais**
- **Afastamentos longos (ex.: licença maternidade):**
  - **Incluídos** no headcount se o vínculo empregatício permanecer ativo.
  - **Excluídos** se o afastamento resultar em rescisão.
- **Terceirizados:**
  - Incluídos **somente se** houver acordo contratual para contabilização no headcount.
- **Funcionários em período de experiência:**
  - Incluídos **apenas após a assinatura do contrato**.

---

### **2.2 Turnover (Rotatividade de Funcionários)**
**Definição:**
Porcentagem de funcionários que **saíram da empresa** em um período, em relação ao headcount médio.

#### **Critérios de Inclusão**
- **Desligamentos voluntários** (pedido de demissão).
- **Desligamentos involuntários** (demissão por justa causa, performance, redução de quadro).
- **Aposentadorias** (quando não há realocação interna).
- **Falecimentos**.
- **Término de contrato temporário** (quando não há renovação).

#### **Critérios de Exclusão**
- **Transferências internas** (funcionário que muda de área, mas permanece na empresa).
- **Afastamentos temporários** (ex.: licença saúde, férias).
- **Funcionários em processo de desligamento** mas ainda não efetivado (ex.: aviso prévio em curso).
- **Terceirizados** (a menos que o contrato preveja contabilização no turnover).

#### **Casos Especiais**
- **Demissões em massa (layoffs):**
  - Contabilizadas no turnover, mas **podem ser destacadas em relatório separado** para análise de impacto.
- **Funcionários readmitidos no mesmo período:**
  - **Excluídos** do cálculo se a readmissão ocorrer em até 30 dias após o desligamento.
- **Contratos temporários não renovados:**
  - Incluídos **apenas se** a não renovação for considerada desligamento pela política da empresa.

---

### **2.3 Vagas Abertas (Posições em Aberto)**
**Definição:**
Total de **posições disponíveis para contratação**, ainda não preenchidas.

#### **Critérios de Inclusão**
- Vagas **aprovadas no orçamento** e com processo seletivo em andamento.
- Vagas **temporárias** (ex.: substituição de licença maternidade).
- Vagas **para novos projetos** ou expansão de equipe.

#### **Critérios de Exclusão**
- Vagas **canceladas** antes do preenchimento.
- Vagas **congeladas** por decisão estratégica (ex.: crise financeira).
- Posições **ocupadas por funcionários em transição** (ex.: realocação interna).
- Vagas **para terceirizados** (a menos que sejam gerenciadas pelo RH interno).

#### **Casos Especiais**
- **Vagas reabertas:**
  - Contabilizadas como **nova vaga** se o processo seletivo anterior foi encerrado sem contratação.
- **Vagas sazonais:**
  - Incluídas **apenas no período de necessidade** (ex.: contratações para fim de ano).

---

### **2.4 Taxa de Ocupação (Fill Rate)**
**Definição:**
Porcentagem de **vagas preenchidas** em relação ao total de posições previstas no orçamento.

#### **Critérios de Inclusão**
- Posições **efetivamente ocupadas** por funcionários ativos.
- Vagas **preenchidas por transferência interna**.
- Contratações **temporárias** que suprem a demanda (quando aplicável).

#### **Critérios de Exclusão**
- Vagas **em processo seletivo** (ainda não preenchidas).
- Posições **orçamentárias não aprovadas**.
- Vagas **ocupadas por funcionários em período de experiência** (se a política considerar apenas contratações efetivas).

#### **Casos Especiais**
- **Over-hiring (contratação acima do orçamento):**
  - **Não impacta a taxa de ocupação** (o cálculo usa apenas as posições previstas).
- **Vagas compartilhadas (job sharing):**
  - Contabilizadas como **1 posição preenchida**, independentemente do número de funcionários alocados.

---

### **2.5 Custo por Funcionário (Custo de Pessoal)**
**Definição:**
Valor médio gasto por funcionário, incluindo salários, benefícios e encargos.

#### **Critérios de Inclusão**
- **Salário base** (fixo e variável).
- **Benefícios** (vale-refeição, plano de saúde, transporte).
- **Encargos trabalhistas** (INSS, FGTS, 13º salário, férias).
- **Bônus e comissões** (quando pagos no período analisado).
- **Custos de treinamento** (quando alocados por funcionário).

#### **Critérios de Exclusão**
- **Despesas administrativas** do RH (ex.: software, aluguel de escritório).
- **Custos com terceirizados** (a menos que sejam rateados por headcount).
- **Multas ou indenizações** por rescisão (contabilizadas separadamente).
- **Benefícios não utilizados** (ex.: vale-refeição não sacado).

#### **Casos Especiais**
- **Funcionários em home office:**
  - Custos com **equipamentos ou internet** podem ser incluídos, dependendo da política da empresa.
- **Contratos temporários:**
  - Custos contabilizados **proporcionalmente ao período trabalhado**.

---

### **2.6 Tempo Médio de Empresa (Tenure)**
**Definição:**
Tempo médio que os funcionários permanecem na empresa, calculado em anos.

#### **Critérios de Inclusão**
- Funcionários **ativos** (incluindo afastados temporariamente).
- Funcionários **desligados no período analisado** (para cálculo histórico).
- **Tempo parcial** (ex.: 6 meses = 0,5 ano).

#### **Critérios de Exclusão**
- **Estagiários ou aprendizes** (quando não considerados no headcount).
- **Funcionários com dados de admissão incompletos**.
- **Terceirizados** (a menos que tenham registro de tempo na empresa).

#### **Casos Especiais**
- **Readmissões:**
  - O tempo é **somatizado** (ex.: funcionário que saiu e voltou após 2 anos tem tenure total de 5 anos).
- **Fusões/aquisições:**
  - Funcionários de empresas adquiridas **podem ter o tempo recalculado** a partir da data de integração.

---
## **3. Condicionais e Classificações**
Como os dados são segmentados para análise:

| **Critério**          | **Classificações Possíveis**                                                                 |
|-----------------------|---------------------------------------------------------------------------------------------|
| **Período**           | Diário, mensal, trimestral, anual ou personalizado (ex.: "Últimos 12 meses").              |
| **Tipo de Funcionário** | CLT, temporário, terceirizado, estagiário, aprendiz.                                      |
| **Situação**          | Ativo, afastado, em aviso prévio, desligado.                                               |
| **Faixa Etária**      | Até 25 anos, 26–35 anos, 36–45 anos, 46–55 anos, acima de 55 anos.                          |
| **Tempo de Empresa**  | Até 1 ano, 1–3 anos, 3–5 anos, 5–10 anos, acima de 10 anos.                                |
| **Centro de Custo**   | Administrativo, operacional, comercial, TI, etc.                                          |
| **Região**            | Sudeste, Sul, Nordeste, Norte, Centro-Oeste (ou por unidade/fábrica).                      |
| **Tipo de Contratação** | Efetivo, trainee, substituição, projeto específico.                                       |
| **Jornada de Trabalho** | Integral (40h), parcial (20h), flexível, home office.                                    |

---
## **4. Campos e Flags de Apoio**
Campos usados para aplicar as regras (sem detalhes técnicos):

| **Campo**               | **Significado**                                                                 |
|-------------------------|---------------------------------------------------------------------------------|
| **situacao_sk**         | Status do funcionário (ativo, afastado, desligado).                           |
| **tipo_funcionario_sk** | Classificação do vínculo (CLT, temporário, terceirizado).                     |
| **jornada_sk**          | Tipo de jornada (integral, parcial, flexível).                                 |
| **contratacao_tipo_sk** | Forma de admissão (efetivo, trainee, substituição).                            |
| **evento_sk**           | Tipo de evento (admissão, demissão, promoção, transferência).                 |
| **status_sk**           | Estado atual (em experiência, efetivado, em aviso prévio).                     |
| **pessoa_hc**           | Flag para identificar se o funcionário deve ser contado no **headcount**.      |
| **pessoa_to**           | Flag para identificar se o funcionário deve ser contado no **turnover**.       |

---
## **5. O que é Incluído e o que é Excluído no Dashboard**

### **5.1 Resumo Geral**
| **Métrica**       | **Incluído**                                                                 | **Excluído**                                                                 |
|-------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Headcount**     | Funcionários ativos, afastados temporários, terceirizados (quando aplicável). | Desligados, candidatos em seleção, estagiários sem registro.                 |
| **Turnover**      | Demissões voluntárias/involuntárias, aposentadorias, falecimentos.         | Transferências internas, afastamentos, terceirizados (geralmente).           |
| **Vagas Abertas** | Posições aprovadas no orçamento em processo seletivo.                       | Vagas canceladas, congeladas, ocupadas por realocação interna.               |
| **Taxa de Ocupação** | Vagas preenchidas (inclusive transferências internas).                     | Vagas em seleção, posições não orçamentárias.                                |
| **Custo por Funcionário** | Salários, benefícios, encargos, bônus.                                   | Despesas administrativas, multas, custos com terceirizados (geralmente).     |
| **Tempo Médio de Empresa** | Funcionários ativos e desligados (para histórico).                       | Estagiários, dados incompletos, terceirizados (quando não registrados).      |

---
## **6. Glossário**
| **Termo**               | **Definição**                                                                 |
|-------------------------|------------------------------------------------------------------------------|
| **Headcount**           | Número total de funcionários ativos na empresa.                             |
| **Turnover**            | Taxa de rotatividade (saída de funcionários em relação ao headcount médio).  |
| **Vagas Abertas**       | Posições disponíveis para contratação, ainda não preenchidas.                |
| **Taxa de Ocupação**    | Porcentagem de vagas preenchidas em relação ao orçamento.                    |
| **CLT**                 | Contrato de trabalho regido pela Consolidação das Leis do Trabalho.          |
| **Terceirizado**        | Funcionário contratado via empresa prestadora de serviços.                   |
| **Centro de Custo**     | Unidade organizacional que acumula despesas (ex.: departamento, projeto).    |
| **Flag**                | Indicador (sim/não) usado para classificar registros (ex.: "contabilizar no headcount"). |
| **Orçamento**           | Planejamento financeiro aprovado para contratações e despesas.               |
| **Job Sharing**         | Modelo onde uma posição é dividida entre dois ou mais funcionários.         |
| **Over-hiring**         | Contratação acima do número de vagas previstas no orçamento.                 |
