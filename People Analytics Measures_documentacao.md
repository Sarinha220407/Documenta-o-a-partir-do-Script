# Documentação Técnica

**Arquivo:** `People Analytics Measures.qvs`  
**Última atualização:** 15/08/2025 11:55:18

# **Documentação do Script QVS – Análise de Horas Extras, Absenteísmo e Banco de Horas**

## **1. Introdução**
Este documento explica o funcionamento de um script utilizado para calcular indicadores relacionados a **horas extras**, **absenteísmo** (faltas, atrasos, atestados) e **banco de horas** em uma organização.

O script é composto por **fórmulas matemáticas** que extraem dados de um sistema de registro de ponto e os transformam em informações úteis para gestão, como:
- Quantidade de horas extras trabalhadas.
- Custos associados a horas extras.
- Índices de faltas e atrasos.
- Saldo de banco de horas dos colaboradores.

Essas informações ajudam a empresa a **monitorar a produtividade, controlar custos e tomar decisões baseadas em dados**.

---

## **2. Estrutura do Script**
O script está dividido em **três seções principais**, cada uma responsável por um tipo de análise:

1. **Horas Extras** – Cálculos relacionados a horas trabalhadas além da jornada normal.
2. **Absenteísmo** – Análise de faltas, atrasos, atestados e abonos.
3. **Banco de Horas** – Controle do saldo de horas positivas e negativas dos colaboradores.

Cada seção contém **fórmulas (chamadas de "variáveis" ou "medidas")** que realizam cálculos específicos.

---

## **3. Seção 1: Análise de Horas Extras**
Esta parte do script calcula indicadores relacionados às **horas extras** trabalhadas pelos colaboradores.

### **3.1. O que são horas extras?**
Horas extras são aquelas trabalhadas **além da jornada regular** do colaborador. Elas podem ser:
- **Recorrentes** (quando acontecem com frequência).
- **Esporádicas** (quando ocorrem eventualmente).

### **3.2. Principais Cálculos Realizados**

| **Variável** | **O que faz?** | **Exemplo Prático** |
|-------------|---------------|---------------------|
| **`horas_total_extras`** | Soma todas as horas extras registradas. | Se 10 pessoas trabalharam 2h extras cada, o total é **20h**. |
| **`horas_extras_atual`** | Calcula as horas extras do **mês atual**. | Em janeiro de 2024, foram trabalhadas **50h extras**. |
| **`horas_extras_anterior`** | Calcula as horas extras do **mesmo mês no ano anterior**. | Em janeiro de 2023, foram trabalhadas **30h extras**. |
| **`custo_medio_he`** | Calcula o **custo médio por hora extra**. | Se o total gasto com horas extras foi R$ 2.000 e foram trabalhadas 100h, o custo médio é **R$ 20/h**. |
| **`pessoas_com_registro_he`** | Conta quantas pessoas **fizeram hora extra**. | Se 20 de 100 colaboradores fizeram hora extra, o valor é **20**. |
| **`%_HE_pessoas_elegiveis`** | Calcula a **porcentagem de pessoas que podem fazer hora extra**. | Se 80 de 100 colaboradores são elegíveis, o resultado é **80%**. |
| **`%_MoM_horas_extras`** | Compara as horas extras do **mês atual com o mês anterior** (variação mensal). | Se em dezembro foram 40h e em janeiro 50h, a variação é **+25%**. |
| **`%_YoY_horas_extras`** | Compara as horas extras do **ano atual com o ano anterior** (variação anual). | Se em 2023 foram 100h e em 2024 foram 120h, a variação é **+20%**. |
| **`%_HE_remuneracao_total`** | Mostra quanto as horas extras representam **do total da folha de pagamento**. | Se o salário total é R$ 50.000 e as horas extras custaram R$ 5.000, o resultado é **10%**. |

### **3.3. Para que servem esses cálculos?**
Esses indicadores ajudam a empresa a:
✅ **Controlar custos** com horas extras.
✅ **Identificar padrões** (ex.: se há muitos colaboradores fazendo hora extra recorrente).
✅ **Comparar desempenho** entre meses e anos.
✅ **Verificar elegibilidade** (quem pode ou não fazer hora extra).

---

## **4. Seção 2: Análise de Absenteísmo**
Esta parte calcula indicadores relacionados a **faltas, atrasos, atestados e abonos**.

### **4.1. O que é absenteísmo?**
Absenteísmo é a **ausência do colaborador no trabalho**, seja por:
- **Faltas** (não comparecimento sem justificativa).
- **Atestados médicos** (afastamento por saúde).
- **Abonos** (folgas concedidas pela empresa).
- **Atrasos** (chegada após o horário).
- **Reembolsos** (horas não trabalhadas que são descontadas).

### **4.2. Principais Cálculos Realizados**

| **Variável** | **O que faz?** | **Exemplo Prático** |
|-------------|---------------|---------------------|
| **`dias_absenteismo`** | Soma todos os dias de ausência (faltas, atrasos, atestados, abonos). | Se em um mês houve 10 faltas, 5 atrasos e 3 atestados, o total é **18 dias**. |
| **`dias_nao_planejados`** | Soma apenas **faltas e atrasos** (ausências não programadas). | Se houve 10 faltas e 5 atrasos, o total é **15 dias**. |
| **`%_indice_absenteismo`** | Calcula a **porcentagem de horas perdidas** em relação à jornada total. | Se a jornada mensal é 2.000h e foram perdidas 200h, o índice é **10%**. |
| **`media_faltantes`** | Calcula a **média de dias perdidos por pessoa**. | Se 100 pessoas perderam 200 dias, a média é **2 dias por pessoa**. |
| **`%_MoM_absenteismo`** | Compara o absenteísmo do **mês atual com o mês anterior**. | Se em dezembro foi 8% e em janeiro 10%, a variação é **+25%**. |
| **`%_YoY_absenteismo`** | Compara o absenteísmo do **ano atual com o ano anterior**. | Se em 2023 foi 5% e em 2024 foi 7%, a variação é **+40%**. |
| **`valor_eventos_faltas`** | Calcula o **custo total das faltas e reembolsos**. | Se 10 faltas custaram R$ 1.000, o valor é **R$ 1.000**. |

### **4.3. Para que servem esses cálculos?**
Esses indicadores ajudam a empresa a:
✅ **Reduzir faltas e atrasos** identificando padrões.
✅ **Melhorar a saúde dos colaboradores** (se houver muitos atestados).
✅ **Controlar custos com ausências não planejadas**.
✅ **Comparar o absenteísmo entre equipes ou períodos**.

---

## **5. Seção 3: Análise de Banco de Horas**
Esta parte calcula indicadores relacionados ao **saldo de horas** dos colaboradores.

### **5.1. O que é banco de horas?**
Banco de horas é um sistema onde:
- **Horas extras trabalhadas** são **acumuladas** como saldo positivo.
- **Horas não trabalhadas** (faltas, atrasos) geram **saldo negativo**.
- O colaborador pode **usar o saldo positivo** para folgar ou receber pagamento.

### **5.2. Principais Cálculos Realizados**

| **Variável** | **O que faz?** | **Exemplo Prático |
|-------------|---------------|-------------------|
| **`horas_total_saldo_banco`** | Soma **todas as horas no banco** (positivas e negativas). | Se 50 pessoas têm 10h positivas cada, o total é **500h**. |
| **`horas_total_saldo_banco_positivo`** | Soma apenas as **horas positivas** (excedentes). | Se 30 pessoas têm 5h positivas cada, o total é **150h**. |
| **`horas_total_saldo_banco_negativo`** | Soma apenas as **horas negativas** (déficit). | Se 20 pessoas devem 2h cada, o total é **-40h**. |
| **`%_colaboradores_com_saldo_banco`** | Calcula a **porcentagem de pessoas com saldo no banco**. | Se 80 de 100 colaboradores têm saldo, o resultado é **80%**. |
| **`%_MAR_SET_pgt_banco`** | Compara o **pagamento de banco de horas em março e setembro**. | Se em março foram pagas 100h e em setembro 120h, a variação é **+20%**. |

### **5.3. Para que servem esses cálculos?**
Esses indicadores ajudam a empresa a:
✅ **Gerenciar o saldo de horas** dos colaboradores.
✅ **Evitar acúmulo excessivo** de horas positivas ou negativas.
✅ **Planejar pagamentos** de horas extras acumuladas.
✅ **Identificar colaboradores com saldo negativo** (que podem estar faltando muito).

---

## **6. Como o Script Funciona na Prática?**
O script **não exibe dados diretamente**, mas **prepara as fórmulas** para que um sistema de business intelligence (como QlikView ou Qlik Sense) possa:
1. **Coletar dados** de registros de ponto, folha de pagamento e eventos de RH.
2. **Aplicar as fórmulas** para calcular os indicadores.
3. **Exibir os resultados** em **gráficos, tabelas e dashboards**.

### **Exemplo de Uso:**
- Um gestor pode abrir um **dashboard** e ver:
  - **"Em janeiro, 30% dos colaboradores fizeram hora extra, custando R$ 15.000."**
  - **"O absenteísmo aumentou 10% em relação a dezembro, principalmente por atestados."**
  - **"20% dos colaboradores têm saldo negativo no banco de horas."**

---
## **7. Conclusão**
Este script é uma **ferramenta de análise** que transforma dados brutos de registro de ponto em **informações estratégicas** para a gestão de pessoas.

### **Principais Benefícios:**
✔ **Controle de custos** com horas extras e faltas.
✔ **Melhoria na produtividade** ao identificar padrões de absenteísmo.
✔ **Gestão mais eficiente do banco de horas**.
✔ **Tomada de decisão baseada em dados** (ex.: necessidade de contratação, treinamentos, políticas de horário).

---
**Observação:**
Este documento explica **o que o script faz**, mas não ensina a modificá-lo. Para ajustes, é necessário conhecimento técnico em **linguagem de script Qlik (QVS)**.
