# Documentação Técnica

**Arquivo:** `People Analytics Measures.qvs`  
**Última atualização:** 15/08/2025 10:04:30

# **Documentação do Script de Cálculo de Indicadores de Gestão de Pessoas**

Este documento explica, de forma clara e organizada, o funcionamento de um script utilizado para calcular indicadores relacionados a **horas extras**, **absenteísmo** e **banco de horas** em uma organização. O objetivo é fornecer informações que auxiliam na análise de custos, produtividade e comportamento dos colaboradores em relação ao tempo de trabalho.

---

## **1. Visão Geral do Script**
O script é dividido em **três grandes blocos**, cada um responsável por calcular métricas específicas:

1. **Horas Extras** – Indicadores sobre horas trabalhadas além da jornada regular, seus custos e impactos.
2. **Absenteísmo** – Métricas relacionadas a faltas, atrasos, atestados e abonos, além de seus custos e frequência.
3. **Banco de Horas** – Cálculos sobre saldos positivos e negativos de horas, pagamentos e utilização do banco de horas.

Cada bloco contém **fórmulas** que extraem dados de um sistema de registro de eventos (como ponto eletrônico) e os transformam em indicadores úteis para gestão.

---

## **2. Bloco 1: Indicadores de Horas Extras**
Este bloco calcula métricas relacionadas ao trabalho além da jornada padrão, incluindo custos, quantidade de horas e comparações entre períodos.

### **2.1. O que são Horas Extras?**
Horas extras são aquelas trabalhadas além do horário contratual do colaborador. Elas geram custos adicionais para a empresa e podem indicar sobrecarga de trabalho, necessidade de contratações ou problemas de produtividade.

### **2.2. Principais Indicadores Calculados**

| **Indicador**                     | **O que mede**                                                                 | **Exemplo Prático**                                                                 |
|-----------------------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **Horas totais de hora extra**    | Soma de todas as horas extras registradas.                                    | Se 100 colaboradores fizeram 2h extras cada, o total é **200 horas**.              |
| **Custo médio da hora extra**     | Valor médio pago por cada hora extra.                                          | Se R$ 10.000 foram gastos em 500h extras, o custo médio é **R$ 20 por hora**.   |
| **Pessoas com registro de HE**    | Quantidade de colaboradores que fizeram hora extra.                           | Se 200 pessoas registraram HE em um mês, o valor é **200**.                       |
| **% de horas extras na jornada**  | Proporção das horas extras em relação ao total de horas trabalhadas.         | Se em 10.000h totais, 500h são extras, o índice é **5%**.                         |
| **Custo HE recorrente vs. esporádico** | Divide os custos entre horas extras **recorrentes** (previstas) e **esporádicas** (eventuais). | Se R$ 8.000 são recorrentes e R$ 2.000 esporádicos, a proporção é **80% vs. 20%**. |
| **Comparações (MoM e YoY)**       | Variação dos indicadores em relação ao **mês anterior (MoM)** ou **ano anterior (YoY)**. | Se o custo médio era R$ 18 no mês passado e agora é R$ 20, a variação MoM é **+11%**. |

### **2.3. Como os Dados São Filtrados?**
- **Por período**: Os cálculos podem ser feitos para um **mês específico**, **ano atual** ou **ano anterior**.
- **Por grupo de colaboradores**: Alguns indicadores separam dados de **líderes** e **demais funcionários**.
- **Por tipo de custo**: Diferença entre horas extras **recorrentes** (previstas em contrato) e **esporádicas** (eventuais).

### **2.4. Exemplos de Uso**
- **Análise de custos**: Verificar se os gastos com horas extras estão aumentando e por quê.
- **Planejamento de equipe**: Identificar se há sobrecarga em determinados setores.
- **Comparação histórica**: Avaliar se as horas extras estão crescendo em relação ao ano passado.

---

## **3. Bloco 2: Indicadores de Absenteísmo**
Este bloco calcula métricas relacionadas a **faltas, atrasos, atestados e abonos**, além de seus impactos financeiros e operacionais.

### **3.1. O que é Absenteísmo?**
Absenteísmo refere-se às ausências dos colaboradores, sejam elas **justificadas** (atestados) ou **não justificadas** (faltas, atrasos). Alto absenteísmo pode indicar problemas de saúde, desmotivação ou falhas na gestão.

### **3.2. Principais Indicadores Calculados**

| **Indicador**                     | **O que mede**                                                                 | **Exemplo Prático**                                                                 |
|-----------------------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **Dias de absenteísmo**           | Soma de dias perdidos por faltas, atrasos, atestados e abonos.               | Se 50 pessoas faltaram 1 dia cada, o total é **50 dias**.                         |
| **Índice de absenteísmo**         | Proporção de horas perdidas em relação ao total de horas trabalhadas.         | Se 2.000h foram perdidas em 50.000h totais, o índice é **4%**.                    |
| **Horas não planejadas**          | Horas perdidas por faltas e atrasos (exclui atestados e abonos).              | Se 1.000h foram por faltas e 500h por atrasos, o total é **1.500h**.               |
| **Custo das faltas**              | Valor financeiro perdido com faltas e reembolsos.                             | Se 100 faltas custaram R$ 5.000, o valor é **R$ 5.000**.                           |
| **Comparações (MoM e YoY)**       | Variação do absenteísmo em relação ao **mês anterior (MoM)** ou **ano anterior (YoY)**. | Se o índice era 3% no mês passado e agora é 5%, a variação MoM é **+66%**. |

### **3.3. Como os Dados São Filtrados?**
- **Por tipo de evento**:
  - **Faltas** (não justificadas).
  - **Atestados** (justificadas por motivo médico).
  - **Abonos** (ausências autorizadas, como licenças).
  - **Atrasos** (chegada após o horário).
  - **Reembolsos** (compensações por horas não trabalhadas).
- **Por grupo de colaboradores**: Alguns indicadores separam **líderes** e **demais funcionários**.
- **Por período**: Comparações entre **mês atual**, **mês anterior** e **ano anterior**.

### **3.4. Exemplos de Uso**
- **Identificar problemas de saúde**: Aumento de atestados pode indicar surto de doenças ou estresse.
- **Avaliar política de faltas**: Verificar se as ausências estão crescendo e quais os motivos.
- **Reduzir custos**: Entender o impacto financeiro das faltas e buscar soluções.

---

## **4. Bloco 3: Indicadores de Banco de Horas**
Este bloco calcula métricas relacionadas ao **saldo de horas** dos colaboradores, incluindo horas positivas (a receber) e negativas (devidas).

### **4.1. O que é Banco de Horas?**
O banco de horas é um sistema que registra:
- **Horas positivas**: Horas extras trabalhadas que podem ser compensadas com folga.
- **Horas negativas**: Horas não trabalhadas que devem ser repostas.
- **Pagamentos**: Quando a empresa paga pelas horas extras acumuladas.

### **4.2. Principais Indicadores Calculados**

| **Indicador**                     | **O que mede**                                                                 | **Exemplo Prático**                                                                 |
|-----------------------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **Saldo total do banco de horas** | Diferença entre horas positivas e negativas de todos os colaboradores.       | Se 1.000h são positivas e 500h negativas, o saldo é **+500h**.                      |
| **% de colaboradores com saldo** | Proporção de funcionários que têm horas no banco (positivas ou negativas).     | Se 150 de 200 colaboradores têm saldo, o índice é **75%**.                         |
| **Pagamento de banco (Mar/Set)**  | Valor pago em **março** e **setembro** (períodos comuns de acerto de horas).   | Se em março foram pagos R$ 20.000 e em setembro R$ 18.000, a variação é **-10%**. |
| **Saldo positivo vs. negativo**   | Quantidade de horas **a receber** (positivas) e **devidas** (negativas).       | Se 800h são positivas e 300h negativas, a relação é **800 vs. 300**.                |

### **4.3. Como os Dados São Filtrados?**
- **Por tipo de saldo**:
  - **Positivo** (horas a compensar).
  - **Negativo** (horas devidas).
- **Por período de pagamento**: Foco nos meses de **março** e **setembro**, quando geralmente são feitos acertos.
- **Por código de evento**: Identifica transações específicas de pagamento de banco de horas.

### **4.4. Exemplos de Uso**
- **Gestão de folgas**: Verificar se os colaboradores estão compensando horas extras.
- **Planejamento financeiro**: Prever gastos com pagamento de horas acumuladas.
- **Equilíbrio da equipe**: Identificar se há muitos colaboradores com saldo negativo (risco de sobrecarga).

---

## **5. Como o Script Funciona na Prática?**
O script **extrai dados de um sistema de registros** (como um banco de dados de ponto eletrônico) e aplica **fórmulas matemáticas** para gerar os indicadores. Cada linha do script define uma métrica específica, como:

- **`SET horas_total_extras = '{<tipo_evento={''Hora extra''}>} [#_hora_total]'`**
  → **Tradução**: "Some todas as horas registradas como 'Hora extra' e armazene o total."

- **`SET %_indice_absenteismo = '[#_horas_total_absenteismo]/[#_horas_total_jornada_mensal]'`**
  → **Tradução**: "Divida as horas perdidas por absenteísmo pelo total de horas trabalhadas no mês para obter a porcentagem."

### **5.1. Comparações Temporais (MoM e YoY)**
Muitas métricas incluem comparações entre períodos:
- **MoM (Month-over-Month)**: Compara o mês atual com o anterior.
  - Exemplo: `(%_MoM_horas_extras)` → "Quanto as horas extras aumentaram ou diminuíram em relação ao mês passado?"
- **YoY (Year-over-Year)**: Compara o ano atual com o anterior.
  - Exemplo: `(%_YoY_absenteísmo)` → "O absenteísmo está maior ou menor do que no mesmo período do ano passado?"

### **5.2. Filtros por Grupo de Colaboradores**
Alguns indicadores separam dados por **cargo ou função**, como:
- **Líderes** (`grupo_relatorio={''7 - Líder'}'`).
- **Demais colaboradores** (`grupo_relatorio={''8 - Demais'}'`).

Isso ajuda a identificar se problemas são generalizados ou concentrados em determinados grupos.

---

## **6. Resumo dos Benefícios do Script**
Este script permite que a empresa:
✅ **Monitore custos** com horas extras e absenteísmo.
✅ **Identifique tendências** (aumento ou redução de indicadores).
✅ **Tome decisões baseadas em dados**, como:
   - Contratar mais pessoas se houver muitas horas extras.
   - Investigar causas de alto absenteísmo.
   - Ajustar políticas de banco de horas.
✅ **Compare períodos** para avaliar melhorias ou pioras na gestão de pessoas.

---
## **7. Considerações Finais**
Este script é uma **ferramenta de análise** que transforma dados brutos de registro de ponto em **informações estratégicas**. Seu uso adequado ajuda a:
- **Reduzir custos desnecessários**.
- **Melhorar a produtividade**.
- **Garantir o bem-estar dos colaboradores**.

Não é necessário entender programação para interpretar seus resultados, basta conhecer os conceitos de **horas extras, absenteísmo e banco de horas** e como eles impactam a organização.

---
**Fim da Documentação**
