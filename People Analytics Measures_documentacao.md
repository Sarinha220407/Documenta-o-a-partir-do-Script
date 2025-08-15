# Documentação Técnica

**Arquivo:** `People Analytics Measures.qvs`  
**Última atualização:** 15/08/2025 13:32:50

# **Documentação de Regras de Negócio – Dashboard de Gestão de Horas e Absenteísmo**
*(Horas Extras, Absenteísmo e Banco de Horas)*

---

## **1. Visão Geral**
### **Objetivo do Documento**
Este guia explica **o que é contado** e **o que não é contado** em cada métrica do dashboard, além de casos especiais e classificações.
Todas as métricas seguem critérios específicos de **inclusão e exclusão** para garantir consistência nos dados.

### **Como Identificar o Que Deve Ser Contado?**
- **Critérios de Inclusão**: Regras que definem **quando um registro deve ser considerado** na métrica.
- **Critérios de Exclusão**: Situações em que **um registro não deve ser contabilizado**, mesmo que pareça relacionado.
- **Casos Especiais**: Exceções ou tratamentos diferenciados para cenários específicos.

---
---

## **2. Regras de Negócio por Indicador/Métrica**

### **📌 Grupo: Horas Extras**
#### **1. Total de Horas Extras (`horas_total_extras`)**
- **Definição**: Soma de **todas as horas extras registradas** no período.
- **Critérios de Inclusão**:
  - Apenas eventos classificados como **"Hora extra"** (tipo_evento = 'Hora extra').
  - Inclui horas extras **pagas, compensadas ou em aberto**.
- **Critérios de Exclusão**:
  - Horas de **jornada normal**, **abonos**, **atrasos** ou **faltas** não são contabilizadas.
  - Horas de **banco de horas** (saldo positivo/negativo) não entram neste cálculo.
- **Casos Especiais**:
  - Se uma hora extra for **cancelada ou ajustada**, o valor original é desconsiderado.

---
#### **2. Horas Extras – Mês Atual vs. Ano Anterior (`horas_extras_atual` / `horas_extras_anterior`)**
- **Definição**: Comparação das horas extras entre:
  - **Mês atual** (mês selecionado no filtro).
  - **Mesmo mês do ano anterior**.
- **Critérios de Inclusão**:
  - Mesma regra de `horas_total_extras`, mas **filtrado por período**:
    - *Atual*: Mês/ano selecionado no dashboard.
    - *Anterior*: Mesmo mês, mas do ano passado.
- **Critérios de Exclusão**:
  - Eventos fora dos períodos definidos acima.
- **Casos Especiais**:
  - Se o mês atual não tiver dados, o indicador mostra **zero ou "N/A"**.

---
#### **3. Custo Médio por Hora Extra (`custo_medio_he`)**
- **Definição**: Valor médio **pago por hora extra**, calculado como:
  - **Total gasto com horas extras** ÷ **Total de horas extras registradas**.
- **Critérios de Inclusão**:
  - Apenas eventos com **flag_hora_extra = "1"** (horas extras válidas).
  - Inclui **todos os custos** (salários, encargos, benefícios) associados à hora extra.
- **Critérios de Exclusão**:
  - Horas extras **não pagas** (ex.: compensadas ou em banco de horas).
  - Eventos sem valor financeiro registrado.
- **Casos Especiais**:
  - Se não houver horas extras no período, o custo médio é **zero**.

---
#### **4. Custo Médio por Pessoa (`custo_medio_por_pessoa_he`)**
- **Definição**: Gasto médio **por colaborador** com horas extras.
  - **Total gasto com horas extras** ÷ **Número de pessoas com registro de horas extras**.
- **Critérios de Inclusão**:
  - Apenas colaboradores com **pelo menos 1 hora extra registrada** no período.
- **Critérios de Exclusão**:
  - Colaboradores **sem horas extras** não são contados no denominador.
- **Casos Especiais**:
  - Se apenas 1 pessoa tiver horas extras, o custo médio = **valor total gasto com ela**.

---
#### **5. Pessoas Elegíveis vs. Inelegíveis para Horas Extras**
| Métrica                     | Critérios de Inclusão                                                                 | Critérios de Exclusão                                                                 |
|-----------------------------|--------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| **Pessoas elegíveis**       | Colaboradores do grupo **"8 - Demais"** com horas extras registradas.               | Colaboradores de outros grupos (ex.: líderes) ou sem horas extras.                     |
| **Pessoas inelegíveis**     | Colaboradores **fora do grupo "8 - Demais"** com horas extras.                        | Colaboradores do grupo "8 - Demais" sem horas extras.                                  |
| **Total com registro**      | **Todas as pessoas** com pelo menos 1 hora extra, independentemente do grupo.       | Pessoas sem qualquer registro de hora extra.                                          |

---
#### **6. % de Horas Extras na Remuneração Total (`%_HE_remuneracao_total`)**
- **Definição**: Participação do **valor gasto com horas extras** na **remuneração total** (salário + horas extras).
- **Critérios de Inclusão**:
  - Numerador: **Valor total de horas extras** (todos os grupos).
  - Denominador: **Salário base** (grupos "4 - Coordenador" e "8 - Demais") + **valor de horas extras**.
- **Critérios de Exclusão**:
  - Outros benefícios (ex.: PLR, vale-refeição) **não entram** no denominador.
- **Casos Especiais**:
  - Se não houver salário registrado para um grupo, o cálculo **ignora esse grupo**.

---
#### **7. Horas Extras Recorrentes vs. Esporádicas**
| Tipo               | Critérios de Inclusão                                                                 | Critérios de Exclusão                                                                 |
|--------------------|--------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| **Recorrentes**    | Horas extras debitadas na conta **"Recorrente"** (ex.: horas fixas por projeto).     | Horas extras pontuais ou sem classificação como "Recorrente".                         |
| **Esporádicas**    | Horas extras debitadas na conta **"Esporádico"** (ex.: horas eventuais).             | Horas recorrentes ou sem classificação.                                               |

---
#### **8. Variações Mensal e Anual (MoM / YoY)**
- **Definição**: Comparação de métricas entre:
  - **MoM (Month-over-Month)**: Mês atual vs. mês anterior.
  - **YoY (Year-over-Year)**: Ano atual vs. mesmo período do ano passado.
- **Critérios Gerais**:
  - Usam os **mesmos filtros de período** das métricas originais.
  - Se não houver dados no período de comparação, o resultado é **zero ou "N/A"**.
- **Exemplo**:
  - `%_MoM_horas_extras`: `(Horas extras deste mês - Horas extras do mês passado) / Horas extras do mês passado`.

---
---

### **📌 Grupo: Absenteísmo**
#### **1. Dias de Absenteísmo (`dias_absenteismo`)**
- **Definição**: Soma de **todos os dias não trabalhados**, convertidos em dias úteis.
- **Critérios de Inclusão**:
  - **Atestados médicos** (conversão de horas para dias).
  - **Faltas injustificadas**.
  - **Atrasos** (convertidos em dias proporcionalmente).
  - **Abonos** (folgas concedidas).
- **Critérios de Exclusão**:
  - **Férias**, **licenças remuneradas** ou **afastamentos legais** (ex.: maternidade).
  - **Horas extras** ou **jornadas normais**.
- **Casos Especiais**:
  - **Reembolsos**: Incluídos se forem por faltas abonadas (ex.: falta justificada com desconto revertido).

---
#### **2. Índice de Absenteísmo (`%_indice_absenteismo`)**
- **Definição**: Percentual de **horas não trabalhadas** em relação à **jornada total esperada**.
  - **Horas de absenteísmo** ÷ **Horas totais da jornada mensal**.
- **Critérios de Inclusão**:
  - Numerador: Somatório de **atestados, faltas, atrasos e abonos** (em horas).
  - Denominador: **Jornada mensal contratual** (ex.: 220h/mês).
- **Critérios de Exclusão**:
  - Horas de **banco de horas** ou **férias** não entram no numerador.
- **Casos Especiais**:
  - Se a jornada mensal não estiver registrada, usa-se a **média histórica**.

---
#### **3. Horas Não Planeadas (`horas_nao_planejadas`)**
- **Definição**: Horas perdidas por **faltas ou atrasos**, sem aviso prévio.
- **Critérios de Inclusão**:
  - **Faltas injustificadas**.
  - **Atrasos** (mesmo que abonados depois).
- **Critérios de Exclusão**:
  - **Atestados médicos** (são planejados após registro).
  - **Abonos** (folgas autorizadas).
- **Casos Especiais**:
  - Se um atraso for **justificado depois**, ainda conta como não planejado.

---
#### **4. Valor de Faltas (`valor_eventos_faltas`)**
- **Definição**: Custo financeiro das **faltas e reembolsos** (descontos ou pagamentos).
- **Critérios de Inclusão**:
  - **Faltas injustificadas** (valor descontado do salário).
  - **Reembolsos** (valores pagos ao colaborador por faltas abonadas).
- **Critérios de Exclusão**:
  - **Atestados médicos** ou **abonos** não geram valor (a menos que haja reembolso).
- **Casos Especiais**:
  - Faltas de **líderes** são separadas de **colaboradores operacionais** (`grupo_relatorio`).

---
#### **5. Índice de Abonos (`%_indice_abono`)**
- **Definição**: Percentual de **horas de abono** em relação à jornada mensal.
- **Critérios de Inclusão**:
  - Apenas **abonos registrados** (folgas concedidas).
- **Critérios de Exclusão**:
  - **Faltas** ou **atrasos**, mesmo que abonados depois, não entram aqui.
- **Casos Especiais**:
  - Abonos **coletivos** (ex.: folga por feriado) são contabilizados individualmente.

---
---

### **📌 Grupo: Banco de Horas**
#### **1. Saldo de Banco de Horas (`horas_total_saldo_banco`)**
- **Definição**: Total de horas **acumuladas ou devedoras** no banco de horas.
- **Critérios de Inclusão**:
  - **Saldo positivo**: Horas extras **não pagas** e disponíveis para uso.
  - **Saldo negativo**: Horas **devidas** pelo colaborador (ex.: saídas antecipadas).
- **Critérios de Exclusão**:
  - Horas **já pagas** ou **compensadas** não aparecem no saldo.
- **Casos Especiais**:
  - Saldos **pagos em março/setembro** (`%_MAR_SET_pgt_banco`) são zerados após pagamento.

---
#### **2. % de Colaboradores com Saldo (`%_colaboradores_com_saldo_banco`)**
- **Definição**: Percentual de pessoas com **qualquer saldo** (positivo ou negativo) no banco.
- **Critérios de Inclusão**:
  - Colaboradores com **pelo menos 1 hora registrada** no banco.
- **Critérios de Exclusão**:
  - Colaboradores com **saldo zero** ou **sem registro**.
- **Casos Especiais**:
  - Saldos **muito antigos** (ex.: +2 anos) podem ser excluídos por política interna.

---
#### **3. Pagamento de Banco (Março/Setembro)**
- **Definição**: Comparação do **valor pago** no banco de horas em **março e setembro** vs. **6 meses antes**.
- **Critérios de Inclusão**:
  - Apenas eventos com códigos **"695", "696", "698"** (pagamentos de banco).
  - Períodos: **15/03 e 15/09** (datas de corte).
- **Critérios de Exclusão**:
  - Pagamentos fora dessas datas ou com outros códigos.
- **Casos Especiais**:
  - Se não houver pagamento no período, o indicador mostra **null**.

---
---

## **3. Condicionais e Classificações**
### **Segmentação dos Dados**
As métricas são classificadas por:
- **Período**:
  - *Mês atual* vs. *Mês anterior* vs. *Ano anterior*.
  - *Ano até a data* (YTD).
- **Grupo de Colaboradores**:
  - **"8 - Demais"** (operacionais).
  - **"4 - Coordenador"** ou **"7 - Líder"** (gestores).
- **Tipo de Evento**:
  - Hora extra, falta, atestado, abono, atraso, reembolso.
- **Status Financeiro**:
  - *Recorrente* (horas fixas) vs. *Esporádico* (eventuais).
  - *Pago* vs. *Não pago* (banco de horas).

---
### **Exemplos de Classificação**
| Classificação          | Critério                                                                 |
|------------------------|--------------------------------------------------------------------------|
| **Idade < 30 anos**    | Colaboradores com data de nascimento **após 01/01/1994** (exemplo).     |
| **Ticket Médio < R$100** | Valor médio por hora extra **inferior a R$100**.                        |
| **Região Sudeste**      | Filial localizada em **SP, RJ, MG ou ES**.                               |
| **Saldo Positivo**      | Banco de horas com **mais de 0 horas acumuladas**.                      |

---
---

## **4. Campos e Flags de Apoio**
### **Campos Usados nas Regras**
| Campo                  | Descrição                                                                 |
|------------------------|---------------------------------------------------------------------------|
| **tipo_evento**        | Classifica o evento: "Hora extra", "Falta", "Atestado", etc.              |
| **flag_hora_extra**    | "1" = hora extra válida; "0" ou vazio = não é hora extra.                 |
| **grupo_relatorio**    | Agrupamento do colaborador: "8 - Demais", "4 - Coordenador", etc.         |
| **nome_conta_debito**  | Origem do pagamento: "Recorrente", "Esporádico".                          |
| **descricao_evento**   | Detalhe do evento: "SALDO POSITIVO", "SALDO NEGATIVO".                     |
| **codigo_evento**      | Código interno: "695", "696", "698" (pagamentos de banco de horas).      |
| **gd_eventos_f.load_date** | Data de registro do evento (usada para filtros de período).            |

---
### **Flags Importantes**
| Flag                     | Significado                                                                 |
|--------------------------|----------------------------------------------------------------------------|
| **flag_hora_extra = 1**  | Evento é uma hora extra válida.                                            |
| **flag_horas_nao_planejadas = 1** | Evento é falta ou atraso (não planejado).                                  |

---
---

## **5. O que é Incluído e o que é Excluído no Dashboard**
### **📊 Resumo Geral**
| Métrica                     | **Inclusões**                                                                 | **Exclusões**                                                                 |
|-----------------------------|------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Horas Extras**            | Eventos com `tipo_evento = "Hora extra"` e `flag_hora_extra = 1`.           | Jornadas normais, abonos, faltas.                                            |
| **Absenteísmo**             | Atestados, faltas, atrasos, abonos.                                         | Férias, licenças remuneradas, horas extras.                                  |
| **Banco de Horas**          | Saldos positivos/negativos com `tipo_evento = "Saldo Banco"`.               | Horas já pagas ou compensadas.                                               |
| **Custo Médio**             | Valor de horas extras pagas.                                                | Horas compensadas ou em banco.                                               |
| **Índice de Absenteísmo**   | Horas de faltas, atrasos, atestados.                                        | Horas de férias ou afastamentos legais.                                     |

---
### **📊 Tabelas Detalhadas por Métrica**
#### **Horas Extras**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Horas extras registradas.             | Horas de jornada normal.               |
| Horas pagas ou a pagar.               | Abonos ou faltas.                      |
| Eventos com `flag_hora_extra = 1`.   | Eventos sem valor financeiro.          |

#### **Absenteísmo**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Atestados médicos.                    | Férias ou licenças remuneradas.       |
| Faltas injustificadas.                | Horas extras.                          |
| Atrasos (convertidos em dias).        | Afastamentos por lei (ex.: maternidade). |

#### **Banco de Horas**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Saldos positivos/negativos.           | Horas já pagas ou compensadas.         |
| Eventos com `tipo_evento = "Saldo Banco"`. | Horas sem registro no banco.       |

---
---

## **6. Glossário**
| Termo                     | Definição                                                                 |
|---------------------------|---------------------------------------------------------------------------|
| **Hora Extra**            | Hora trabalhada além da jornada contratual, remunerada ou compensada.    |
| **Atestado**              | Ausência justificada por documento médico.                               |
| **Abono**                 | Folga concedida pela empresa (ex.: compensação por trabalho extra).       |
| **Falta**                 | Ausência não justificada ou sem aviso prévio.                            |
| **Atraso**                | Chegada após o horário estabelecido, convertido em horas/dias.           |
| **Banco de Horas**        | Sistema que acumula horas extras para uso futuro ou pagamento.           |
| **Saldo Positivo**        | Horas extras não utilizadas, disponíveis para compensação.                |
| **Saldo Negativo**        | Horas devidas pelo colaborador (ex.: saídas antecipadas).                |
| **Recorrente**            | Hora extra fixa (ex.: por projeto contínuo).                            |
| **Esporádico**            | Hora extra eventual (ex.: demanda pontual).                               |
| **MoM (Month-over-Month)**| Comparação entre o mês atual e o anterior.                               |
| **YoY (Year-over-Year)**  | Comparação entre o mesmo período deste ano e do ano passado.             |
| **Jornada Mensal**        | Total de horas contratadas para o mês (ex.: 220h).                       |
| **Flag**                  | Indicador booleano (ex.: `flag_hora_extra = 1` = hora extra válida).     |
