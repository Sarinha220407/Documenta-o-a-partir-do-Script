# Documentação Técnica

**Arquivo:** `People Analytics Measures.qvs`  
**Última atualização:** 15/08/2025 13:52:54

# **Documentação de Regras de Negócio – Dashboard de Gestão de Horas**

---
## **1. Visão Geral**
### **Objetivo do Documento**
Este documento explica as regras de negócio aplicadas às métricas de **Horas Extras**, **Absenteísmo** e **Banco de Horas** no dashboard.
Cada indicador segue critérios específicos de **inclusão** e **exclusão**, além de tratamentos para casos especiais.

### **Como Identificar o Que Deve Ser Contado**
- **Critérios de Inclusão**: Definem quais registros são considerados no cálculo.
- **Critérios de Exclusão**: Definem quais registros são ignorados.
- **Casos Especiais**: Situações que exigem tratamentos diferenciados (ex.: eventos recorrentes vs. esporádicos, elegibilidade de colaboradores).

---
## **2. Regras de Negócio por Indicador**

---
### **2.1. Horas Extras**
#### **2.1.1. Total de Horas Extras (`horas_total_extras`)**
- **Definição**: Soma de todas as horas extras registradas no período.
- **Critérios de Inclusão**:
  - Apenas eventos do tipo **"Hora extra"**.
  - Horas registradas no sistema (independente de aprovação ou pagamento).
- **Critérios de Exclusão**:
  - Horas de outros tipos de eventos (ex.: faltas, abonos, jornada normal).
  - Horas não registradas ou com flag de exclusão.
- **Casos Especiais**:
  - Horas extras **recorrentes** (pagas mensalmente) e **esporádicas** (pagas pontualmente) são tratadas separadamente em outros indicadores.

---
#### **2.1.2. Horas Extras – Mês Atual vs. Ano Anterior (`horas_extras_atual` / `horas_extras_anterior`)**
- **Definição**: Comparação das horas extras entre:
  - **Mês atual**: Horas do mês selecionado no filtro.
  - **Ano anterior**: Horas do mesmo mês no ano anterior.
- **Critérios de Inclusão**:
  - Mesma lógica de `horas_total_extras`, mas segmentado por período.
- **Critérios de Exclusão**:
  - Meses sem dados completos (ex.: mês em andamento sem fechamento).
- **Casos Especiais**:
  - Se o mês atual não tiver dados, o indicador retorna **zero** ou **nulo**.

---
#### **2.1.3. Custo Médio por Hora Extra (`custo_medio_he`)**
- **Definição**: Valor médio pago por hora extra, calculado como:
  ```
  (Valor total de horas extras) / (Quantidade total de horas extras)
  ```
- **Critérios de Inclusão**:
  - Apenas eventos com **flag de hora extra = "1"** (horas válidas para pagamento).
  - Inclui todos os custos associados (encargos, benefícios, etc.).
- **Critérios de Exclusão**:
  - Horas extras não pagas (ex.: horas em análise ou rejeitadas).
  - Eventos sem valor financeiro registrado.
- **Casos Especiais**:
  - Se não houver horas extras no período, o custo médio é **zero**.

---
#### **2.1.4. Custo Médio por Pessoa (`custo_medio_por_pessoa_he`)**
- **Definição**: Custo total de horas extras dividido pelo número de colaboradores que registraram horas extras.
- **Critérios de Inclusão**:
  - Apenas colaboradores com **pelo menos 1 registro de hora extra** no período.
- **Critérios de Exclusão**:
  - Colaboradores sem registros de horas extras.
- **Casos Especiais**:
  - Se nenhum colaborador registrar horas extras, o indicador retorna **nulo**.

---
#### **2.1.5. Pessoas Elegíveis vs. Inelegíveis para Horas Extras**
| Indicador               | Critérios de Inclusão                          | Critérios de Exclusão                     |
|-------------------------|-----------------------------------------------|-------------------------------------------|
| **Pessoas elegíveis**   | Colaboradores do grupo **"8 - Demais"**.      | Líderes, coordenadores ou grupos específicos. |
| **Pessoas inelegíveis** | Colaboradores **não** do grupo **"8 - Demais"**. | —                                         |

---
#### **2.1.6. % de Horas Extras na Remuneração Total (`%_HE_remuneracao_total`)**
- **Definição**: Participação do valor de horas extras no salário total dos colaboradores elegíveis.
- **Critérios de Inclusão**:
  - Salários de colaboradores dos grupos **"4 - Coordenador"** e **"8 - Demais"**.
  - Valor total de horas extras pagas.
- **Critérios de Exclusão**:
  - Salários de outros grupos (ex.: estagiários, terceiros).
  - Horas extras não pagas.

---
#### **2.1.7. % de Horas Extras Esporádicas vs. Recorrentes**
| Tipo               | Critérios de Inclusão                          |
|--------------------|-----------------------------------------------|
| **Esporádicas**    | Horas pagas via conta de débito **"Esporádico"**. |
| **Recorrentes**    | Horas pagas via conta de débito **"Recorrente"**. |

---
#### **2.1.8. Variação Mensal/Anual (MoM/YoY)**
- **Definição**: Comparação percentual entre:
  - **MoM (Month-over-Month)**: Mês atual vs. mês anterior.
  - **YoY (Year-over-Year)**: Ano atual vs. ano anterior.
- **Critérios de Inclusão**:
  - Mesma base de dados dos indicadores originais (ex.: `horas_total_extras`, `custo_medio_he`).
- **Casos Especiais**:
  - Se o período de comparação não tiver dados, o resultado é **nulo**.

---
### **2.2. Absenteísmo**
#### **2.2.1. Dias de Absenteísmo (`dias_absenteismo`)**
- **Definição**: Soma de dias perdidos por:
  - Atestados médicos.
  - Faltas não justificadas.
  - Atrasos.
  - Abonos (folgas concedidas).
- **Critérios de Inclusão**:
  - Apenas eventos com **horas registradas** convertidas em dias (base: jornada mensal do colaborador).
- **Critérios de Exclusão**:
  - Horas de jornada normal ou horas extras.
  - Eventos sem registro de horas (ex.: faltas não lançadas).

---
#### **2.2.2. Dias Não Planeados (`dias_nao_planejados`)**
- **Definição**: Soma de **faltas** e **atrasos** (exclui atestados e abonos).
- **Critérios de Inclusão**:
  - Apenas eventos dos tipos **"Falta"** e **"Atraso"**.
- **Critérios de Exclusão**:
  - Abonos, atestados ou eventos justificados.

---
#### **2.2.3. Índice de Absenteísmo (`%_indice_absenteismo`)**
- **Definição**: Percentual de horas de absenteísmo em relação à jornada total mensal.
  ```
  (Horas de absenteísmo) / (Horas de jornada mensal)
  ```
- **Critérios de Inclusão**:
  - Todas as horas de absenteísmo (atestados, faltas, atrasos, abonos).
- **Critérios de Exclusão**:
  - Horas de trabalho efetivo ou horas extras.

---
#### **2.2.4. Índice de Horas Não Planeadas (`%_indice_horas_nao_planejadas`)**
- **Definição**: Percentual de horas perdidas por **faltas e atrasos** (não inclui atestados/abonos).
- **Critérios de Inclusão**:
  - Apenas horas de **faltas** e **atrasos**.
- **Casos Especiais**:
  - Se não houver horas não planejadas, o índice é **zero**.

---
#### **2.2.5. Valor de Faltas (`valor_eventos_faltas`)**
- **Definição**: Custo total associado a **faltas** e **reembolsos** (ex.: multas, descontos).
- **Critérios de Inclusão**:
  - Eventos dos tipos **"Falta"** e **"Reembolso"**.
- **Critérios de Exclusão**:
  - Outros tipos de absenteísmo (ex.: atestados).

---
#### **2.2.6. Variação MoM/YoY de Absenteísmo**
- **Definição**: Comparação percentual do índice de absenteísmo entre períodos.
- **Casos Especiais**:
  - Se o período base não tiver dados, a variação é **nula**.

---
### **2.3. Banco de Horas**
#### **2.3.1. Saldo de Banco de Horas (`horas_total_saldo_banco`)**
- **Definição**: Total de horas acumuladas no banco de horas (positivas ou negativas).
- **Critérios de Inclusão**:
  - Apenas eventos do tipo **"Saldo Banco"**.
- **Critérios de Exclusão**:
  - Horas extras ou jornada normal.

---
#### **2.3.2. Saldo Positivo vs. Negativo**
| Tipo               | Critérios de Inclusão                          |
|--------------------|-----------------------------------------------|
| **Saldo positivo** | Eventos com descrição **"SALDO POSITIVO"**.  |
| **Saldo negativo** | Eventos com descrição **"SALDO NEGATIVO"**.  |

---
#### **2.3.3. % de Colaboradores com Saldo (`%_colaboradores_com_saldo_banco`)**
- **Definição**: Percentual de colaboradores com **qualquer saldo** (positivo ou negativo) no banco de horas.
- **Critérios de Inclusão**:
  - Colaboradores com **pelo menos 1 registro** de saldo.
- **Critérios de Exclusão**:
  - Colaboradores sem registros ou com saldo zero.

---
#### **2.3.4. Pagamento de Banco (Março/Setembro) (`%_MAR_SET_pgt_banco`)**
- **Definição**: Comparação do valor pago em **março** e **setembro** (períodos de liquidação) vs. o mesmo período do ano anterior.
- **Critérios de Inclusão**:
  - Apenas eventos com códigos **"695"**, **"696"** ou **"698"** (pagamentos de banco).
  - Datas específicas: **15/03** e **15/09**.
- **Casos Especiais**:
  - Se não houver pagamentos nos períodos, o indicador retorna **nulo**.

---
## **3. Condicionais e Classificações**
### **3.1. Segmentação por Período**
- **Mês Atual vs. Mês Anterior (MoM)**: Compara o mês selecionado no filtro com o mês anterior.
- **Ano Atual vs. Ano Anterior (YoY)**: Compara o ano selecionado com o mesmo período do ano anterior.
- **Março/Setembro**: Períodos específicos para pagamento de banco de horas.

### **3.2. Segmentação por Tipo de Evento**
| Categoria          | Subcategorias                          |
|--------------------|----------------------------------------|
| **Horas Extras**   | Recorrentes, esporádicas.              |
| **Absenteísmo**    | Faltas, atrasos, atestados, abonos.   |
| **Banco de Horas** | Saldo positivo, saldo negativo.        |

### **3.3. Segmentação por Grupo de Colaboradores**
- **Elegíveis para horas extras**: Grupo **"8 - Demais"**.
- **Não elegíveis**: Líderes, coordenadores ou outros grupos específicos.

---
## **4. Campos e Flags de Apoio**
| Campo/Flag               | Descrição                                                                 |
|--------------------------|---------------------------------------------------------------------------|
| `flag_hora_extra`        | **1** = Hora extra válida para cálculo; **0** = Excluída.                 |
| `grupo_relatorio`        | Classificação do colaborador (ex.: "8 - Demais", "4 - Coordenador").     |
| `tipo_evento`            | Tipo do registro (ex.: "Hora extra", "Falta", "Atestado").                |
| `nome_conta_debito`      | Origem do pagamento (ex.: "Recorrente", "Esporádico").                    |
| `descricao_evento`       | Detalhe do evento (ex.: "SALDO POSITIVO", "SALDO NEGATIVO").              |
| `codigo_evento`          | Código interno do evento (ex.: "695" para pagamento de banco).           |

---
## **5. Resumo: O que é Incluído e Excluído no Dashboard**

### **5.1. Horas Extras**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Eventos do tipo "Hora extra".         | Horas não registradas ou rejeitadas.  |
| Horas com `flag_hora_extra = 1`.      | Horas de outros tipos (faltas, abonos).|
| Colaboradores com registros válidos.  | Colaboradores inelegíveis (ex.: líderes). |

### **5.2. Absenteísmo**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Atestados, faltas, atrasos, abonos.  | Horas trabalhadas ou horas extras.    |
| Eventos com horas registradas.        | Eventos sem lançamento de horas.      |

### **5.3. Banco de Horas**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Eventos do tipo "Saldo Banco".        | Horas extras ou jornada normal.        |
| Saldos positivos e negativos.         | Colaboradores sem saldo registrado.    |

---
## **6. Glossário**
| Termo                  | Definição                                                                 |
|------------------------|---------------------------------------------------------------------------|
| **Absenteísmo**        | Ausências do colaborador (faltas, atestados, atrasos, abonos).          |
| **Banco de Horas**     | Sistema que acumula horas trabalhadas além da jornada para uso futuro.   |
| **Custo Médio**        | Valor médio pago por hora extra ou evento.                                |
| **Elegibilidade**      | Condição que define se um colaborador pode receber horas extras.          |
| **Evento Esporádico**  | Hora extra paga pontualmente (não recorrente).                           |
| **Evento Recorrente**  | Hora extra paga mensalmente (ex.: acordo trabalhista).                   |
| **Flag**               | Marcador que indica se um registro deve ser considerado (ex.: `flag_hora_extra = 1`). |
| **MoM (Month-over-Month)** | Comparação entre dois meses consecutivos.                           |
| **YoY (Year-over-Year)**  | Comparação entre o mesmo período em anos diferentes.                |
