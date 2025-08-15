# Documentação Técnica

**Arquivo:** `People Analytics Model.qvs`  
**Última atualização:** 15/08/2025 13:34:32

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos**
*(Aplicável a métricas de Headcount, Turnover, Vagas, Custos e Eventos)*

---

## **1. Visão Geral**
### **Objetivo do Documento**
Este guia explica **o que é contado** e **o que não é contado** em cada métrica do dashboard, além de regras para segmentação e casos especiais.
**Todas as métricas seguem critérios específicos** para garantir consistência nos dados.

### **Como Identificar o que Deve ser Contado?**
- Cada métrica tem **critérios de inclusão** (o que entra no cálculo) e **critérios de exclusão** (o que não entra).
- **Casos especiais** são exceções às regras gerais (ex.: funcionários em licença, contratos temporários).
- **Segmentações** (por período, região, tipo de funcionário etc.) ajudam a filtrar os dados.

---

## **2. Regras de Negócio por Indicador/Métrica**

---

### **2.1. Headcount (Número de Funcionários Ativos)**
#### **Definição**
Quantidade de **pessoas ativas na empresa** em um determinado período, considerando sua situação contratual.

#### **Critérios de Inclusão**
✅ **São contados como Headcount:**
- Funcionários com **situação ativa** (ex.: trabalhando normalmente, em home office, em treinamento).
- Funcionários **em licença médica ou férias** (mesmo afastados temporariamente).
- **Contratos temporários ou terceirizados** que estejam **vinculados à folha de pagamento** da empresa.
- Funcionários **em período de experiência** (ainda não efetivados).
- Pessoas **em jornada reduzida** (ex.: part-time).

#### **Critérios de Exclusão**
❌ **Não são contados como Headcount:**
- Funcionários **demitidos ou com contrato encerrado** (mesmo que a demissão tenha ocorrido no mês atual).
- **Aposentados** ou em **licença não remunerada** (ex.: licença sem vencimento).
- **Estagiários** (a menos que estejam registrados como funcionários).
- Pessoas **em processo de admissão** (ainda não contratadas oficialmente).
- **Funcionários de empresas parceiras** (terceirizados não vinculados à folha da empresa).

#### **Casos Especiais**
⚠ **Tratamentos diferenciados:**
- **Licença maternidade/paternidade**: Contados como ativos.
- **Afastamento por acidente de trabalho**: Contados como ativos (até o término do benefício).
- **Funcionários em transferência entre unidades**: Contados na unidade de **destino** a partir da data oficial da mudança.
- **Contratos suspensos** (ex.: por investigação interna): **Não contados** até a regularização.

---

### **2.2. Turnover (Rotatividade de Funcionários)**
#### **Definição**
Porcentagem de **funcionários que saíram da empresa** em um período, em relação ao total de funcionários no início do período.

#### **Critérios de Inclusão**
✅ **São contados no Turnover:**
- **Demissões voluntárias** (pedido do funcionário).
- **Demissões por justa causa** (iniciativa da empresa).
- **Término de contrato temporário** (não renovado).
- **Aposentadorias** (saída definitiva).
- **Mortes** (falecimento do funcionário).

#### **Critérios de Exclusão**
❌ **Não são contados no Turnover:**
- **Transferências internas** (funcionário que muda de área/unidade, mas permanece na empresa).
- **Licenças temporárias** (ex.: licença médica, férias).
- **Funcionários em processo de desligamento** (ainda não oficializado).
- **Terceirizados** (não fazem parte do quadro próprio).

#### **Casos Especiais**
⚠ **Tratamentos diferenciados:**
- **Demissões em massa** (ex.: fechamento de uma unidade): Contadas individualmente, mas podem ser analisadas em relatórios separados.
- **Funcionários que saem e voltam no mesmo período**: Contados **apenas na saída** (não na readmissão).
- **Saídas por acordo mútuo**: Contadas como demissão voluntária.

---

### **2.3. Vagas Abertas (Posições em Aberto)**
#### **Definição**
Número de **posições disponíveis para contratação**, independentemente de estarem em processo seletivo ou não.

#### **Critérios de Inclusão**
✅ **São contadas como Vagas Abertas:**
- Vagas **aprovadas no orçamento** e ainda não preenchidas.
- Vagas **em processo seletivo** (com candidaturas em andamento).
- Vagas **temporariamente suspensas** (ex.: congelamento por crise, mas ainda não canceladas).
- **Reposições** (vagas de funcionários que saíram).

#### **Critérios de Exclusão**
❌ **Não são contadas como Vagas Abertas:**
- Vagas **já preenchidas**, mas com contratação ainda não oficializada.
- Vagas **canceladas** (não serão mais ocupadas).
- **Posições futuras** (previstas no planejamento, mas ainda não aprovadas).
- Vagas **para estagiários ou terceirizados**.

#### **Casos Especiais**
⚠ **Tratamentos diferenciados:**
- **Vagas sazonais** (ex.: contratações para período de safra): Contadas apenas no período ativo.
- **Vagas compartilhadas** (ex.: função dividida entre duas pessoas): Contada como **uma única vaga**.
- **Vagas em realocação interna**: Não contadas (já ocupadas por funcionários da empresa).

---

### **2.4. Taxa de Ocupação (Fill Rate)**
#### **Definição**
Porcentagem de **vagas preenchidas** em relação ao total de vagas **orçamentadas** para um período.

#### **Critérios de Inclusão**
✅ **São contados no cálculo:**
- Vagas **orçamentadas** (previstas no planejamento anual).
- Vagas **efetivamente ocupadas** (com funcionário ativo).
- Vagas **em processo de contratação** (com candidato selecionado, mas ainda não admitido).

#### **Critérios de Exclusão**
❌ **Não são contados no cálculo:**
- Vagas **não orçamentadas** (ex.: contratações emergenciais).
- Vagas **canceladas** após aprovação.
- **Posições temporárias** (ex.: substituições por licença).
- Vagas **para terceirizados**.

#### **Casos Especiais**
⚠ **Tratamentos diferenciados:**
- **Vagas com contratação atrasada**: Contadas como **não preenchidas** até a admissão oficial.
- **Vagas em realocação interna**: Contadas como **preenchidas** (mesmo que o funcionário ainda não tenha assumido).
- **Orçamento revisado**: A taxa é recalculada com base no **número atualizado de vagas**.

---

### **2.5. Custo com Pessoal (OPEX de RH)**
#### **Definição**
Total de **despesas com salários, benefícios e encargos** relacionados à mão de obra em um período.

#### **Critérios de Inclusão**
✅ **São contados nos custos:**
- **Salários e encargos** (INSS, FGTS, 13º salário, férias).
- **Benefícios** (vale-refeição, vale-transporte, plano de saúde, previdência privada).
- **Bonificações e comissões**.
- **Encargos trabalhistas** (multas rescisórias, aviso prévio).
- **Custos com terceirizados** (se pagos pela empresa).

#### **Critérios de Exclusão**
❌ **Não são contados nos custos:**
- **Investimentos em treinamento** (cursos, certificações).
- **Despesas com recrutamento** (anúncios, headhunters).
- **Benefícios não monetários** (ex.: ginástica laboral, programas de bem-estar).
- **Custos com estagiários** (bolsas-auxílio).

#### **Casos Especiais**
⚠ **Tratamentos diferenciados:**
- **Férias provisionadas**: Contabilizadas no mês de **competência** (não no pagamento).
- **13º salário**: Rateado mensalmente (1/12 por mês).
- **Multas por demissão sem justa causa**: Contadas no mês do desligamento.
- **Benefícios flexíveis** (ex.: vale-cultura): Contados apenas se **utilizados pelo funcionário**.

---

### **2.6. Eventos de RH (Admissões, Promoções, Transferências)**
#### **Definição**
Registro de **movimentações de funcionários** (entradas, saídas, mudanças de cargo, etc.) em um período.

#### **Critérios de Inclusão**
✅ **São contados como eventos:**
- **Admissões** (novas contratações).
- **Demissões** (saídas voluntárias ou involuntárias).
- **Promoções** (mudança de cargo com aumento de responsabilidade).
- **Transferências** (mudança de área/unidade).
- **Reajustes salariais** (aumentos ou reduções).
- **Licenças** (médicas, maternidade, férias).

#### **Critérios de Exclusão**
❌ **Não são contados como eventos:**
- **Atualizações cadastrais** (ex.: mudança de endereço, estado civil).
- **Treinamentos internos** (sem mudança de cargo ou salário).
- **Afastamentos não oficiais** (ex.: faltas não justificadas).
- **Movimentações de terceirizados**.

#### **Casos Especiais**
⚠ **Tratamentos diferenciados:**
- **Recontratações**: Contadas como **nova admissão** (não como readmissão).
- **Transferências temporárias**: Contadas apenas se durarem **mais de 3 meses**.
- **Promoções com mudança de salário**: Registradas como **promoção + reajuste**.

---

## **3. Condicionais e Classificações**
Como os dados são segmentados no dashboard:

| **Segmentação**       | **Exemplos de Filtros**                                                                 |
|----------------------|----------------------------------------------------------------------------------------|
| **Período**          | Mês atual, ano fiscal, trimestre, data específica (ex.: "Jan/2024").                  |
| **Tipo de Funcionário** | Efetivo, temporário, terceirizado, estagiário.                                        |
| **Situação**         | Ativo, inativo, em licença, em processo de demissão.                                  |
| **Faixa Etária**     | "Até 30 anos", "31 a 50 anos", "Acima de 50 anos".                                    |
| **Região/Unidade**  | Matriz, filiais, unidades operacionais (ex.: "Unidade São Paulo").                     |
| **Jornada**          | Integral (40h), parcial (20h), flexível.                                             |
| **Tempo de Empresa**| "Até 1 ano", "1 a 5 anos", "Mais de 10 anos".                                         |
| **Centro de Custo** | Áreas como "Produção", "Administrativo", "Vendas".                                   |
| **Evento**           | Admissão, demissão, promoção, transferência.                                         |

---

## **4. Campos e Flags de Apoio**
Campos usados para aplicar as regras (sem detalhes técnicos):

| **Campo/Flag**            | **Significado**                                                                          |
|--------------------------|----------------------------------------------------------------------------------------|
| **situacao_sk**          | Status do funcionário (ativo, inativo, licença, etc.).                                 |
| **tipo_funcionario_sk**  | Classificação do contrato (efetivo, temporário, terceirizado).                        |
| **jornada_sk**           | Tipo de jornada (integral, parcial, flexível).                                        |
| **idade**                | Faixa etária do funcionário.                                                            |
| **tempo_empresa_key**    | Tempo de casa (em meses/anos).                                                          |
| **evento_sk**            | Tipo de evento (admissão, demissão, promoção).                                         |
| **centro_de_custo_sk**   | Área/departamento do funcionário.                                                      |
| **status_sk**            | Estado atual (ex.: "em processo de demissão", "em treinamento").                       |
| **pessoa_hc**            | Identificador único para Headcount.                                                    |
| **pessoa_to**            | Identificador único para Turnover.                                                     |

---

## **5. O que é Incluído e o que é Excluído no Dashboard**

### **5.1. Headcount**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Funcionários ativos.                  | Demitidos ou com contrato encerrado. |
| Em licença médica/férias.             | Aposentados.                          |
| Contratos temporários na folha.       | Estagiários (não registrados).        |
| Em período de experiência.            | Em processo de admissão.               |
| Jornada reduzida (part-time).         | Terceirizados não vinculados.          |

### **5.2. Turnover**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Demissões voluntárias.                | Transferências internas.              |
| Demissões por justa causa.            | Licenças temporárias.                 |
| Término de contrato temporário.        | Processo de desligamento não oficial. |
| Aposentadorias.                       | Terceirizados.                        |
| Mortes.                               |                                       |

### **5.3. Vagas Abertas**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Vagas aprovadas no orçamento.        | Vagas já preenchidas.                 |
| Em processo seletivo.                 | Vagas canceladas.                     |
| Temporariamente suspensas.            | Posições futuras não aprovadas.      |
| Reposições.                           | Vagas para estagiários.               |

### **5.4. Taxa de Ocupação**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Vagas orçamentadas.                  | Vagas não orçamentadas.               |
| Vagas ocupadas.                       | Vagas canceladas.                     |
| Em processo de contratação.           | Posições temporárias.                 |

### **5.5. Custo com Pessoal**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Salários e encargos.                  | Treinamentos.                         |
| Benefícios (VR, VT, saúde).            | Despesas com recrutamento.            |
| Bonificações.                         | Benefícios não monetários.            |
| Encargos trabalhistas.               | Custos com estagiários.              |

### **5.6. Eventos de RH**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Admissões.                            | Atualizações cadastrais.              |
| Demissões.                            | Treinamentos sem mudança de cargo.    |
| Promoções.                            | Afastamentos não oficiais.            |
| Transferências.                       | Movimentações de terceirizados.       |

---

## **6. Glossário**
| **Termo**               | **Definição**                                                                          |
|-------------------------|----------------------------------------------------------------------------------------|
| **Headcount**           | Número total de funcionários ativos em um período.                                    |
| **Turnover**            | Taxa de rotatividade (saídas de funcionários em relação ao total).                      |
| **Vagas Abertas**      | Posições disponíveis para contratação, aprovadas no orçamento.                         |
| **Taxa de Ocupação**   | Porcentagem de vagas preenchidas em relação ao planejado.                              |
| **OPEX de RH**          | Despesas operacionais com pessoal (salários, benefícios, encargos).                  |
| **Eventos de RH**       | Movimentações como admissões, demissões, promoções.                                   |
| **Situação Ativa**      | Funcionário trabalhando ou em licença remunerada.                                     |
| **Jornada Parcial**     | Contrato com menos horas que o padrão (ex.: 20h/semana).                             |
| **Centro de Custo**     | Área/departamento responsável por um gasto (ex.: "Produção", "TI").                   |
| **Flag**                | Indicador que classifica um registro (ex.: "tipo_funcionario_sk = temporário").        |
| **Link Key**            | Identificador único que relaciona dados de diferentes tabelas.                        |
