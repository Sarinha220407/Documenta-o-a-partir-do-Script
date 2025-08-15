# Documentação Técnica

**Arquivo:** `sv_headcount.qvs`  
**Última atualização:** 15/08/2025 13:35:57

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos (RH)**
*Documentação técnica para usuários finais não técnicos*

---

## **1. Visão Geral**
### **Objetivo do Documento**
Este documento explica as **regras de negócio** aplicadas nos indicadores do dashboard de RH, incluindo:
- **O que é contado** (critérios de inclusão).
- **O que não é contado** (critérios de exclusão).
- **Casos especiais** (exceções e tratamentos atípicos).
- **Como os dados são segmentados** (por período, faixa etária, tipo de contratação, etc.).

### **Como Identificar o Que Deve Ser Contado**
Cada métrica segue critérios específicos. Para verificar se um registro deve ser incluído ou excluído:
1. **Consulte a seção da métrica** (ex.: *Headcount*, *Turnover*).
2. **Verifique as tabelas de inclusão/exclusão** no final do documento.
3. **Atente-se aos casos especiais** (ex.: funcionários readmitidos, contratações temporárias).

---

## **2. Regras de Negócio por Indicador/Métrica**

---

### **2.1 Headcount (Número de Funcionários Ativos)**
#### **Definição**
Contagem de **funcionários ativos** na empresa em um determinado período, considerando seu status, tipo de contratação e situação cadastral.

#### **Critérios de Inclusão**
São contados como **Headcount** os funcionários que:
- Estão com **situação ativa** (`Situação = 'A'`, `'E'`, `'F'`, `'V'`).
  - `A`: Ativo.
  - `E`: Licença maternidade.
  - `F`: Férias.
  - `V`: Aviso prévio.
- São do **tipo "Normal"** (`Tipo Funcionário = 'N'`).
- Não são **estagiários** ou **aprendizes** (`Funções TEXT ≠ 'Estagiário'`).
- Possuem **centro de custo válido** (código > 99).
- Foram admitidos **até a data atual** (`Data Admissão ≤ Hoje`).
- Não estão em **situações excluídas** (ex.: transferências sem ônus, matrículas apagadas).

#### **Critérios de Exclusão**
Não são contados:
- Funcionários com **situação inativa** (`Situação = 'D'` (demitido), `'Z'` (admissões futuras), `'9'` (matrículas apagadas)).
- **Estagiários** (`Tipo Funcionário = 'T'`).
- **Aprendizes** (`Tipo Funcionário = 'Z'`).
- **Conselheiros** ou **cargos especiais** (`Funções TEXT = 'Conselheiro Adm'`, `'Conselheiro Fiscal'`).
- Funcionários com **centro de custo inválido** (código ≤ 99 ou `#`).
- **Funcionários offshore** (`offshore = 1`), exceto quando especificado.
- **Funcionários readmitidos no mesmo mês** (trados como exceção).

#### **Casos Especiais**
- **Admitidos e demitidos no mesmo mês**:
  - São **forçadamente classificados como "C/Dem no mês"** (`Situação TEXT = 'C/Dem no mês'`).
  - Não são contados no *Headcount* padrão, mas aparecem em relatórios de *Turnover*.
- **Funcionários com short tenure** (demitidos antes do fim do mês de admissão):
  - São **excluídos do Headcount**, mas registrados em métricas de rotatividade.
- **Funcionários offshore**:
  - São **excluídos do Headcount padrão**, mas podem ser incluídos em filtros específicos.
- **Funcionários com múltiplas admissões** (readmitidos):
  - São contados **apenas uma vez por pessoa**, mas a quantidade de readmissões é registrada (`qtd_readimissoes`).

---

### **2.2 Turnover (Rotatividade de Funcionários)**
#### **Definição**
Taxa de **saída de funcionários** da empresa, calculada com base em demissões voluntárias e involuntárias.

#### **Critérios de Inclusão**
São contadas como **Turnover** as demissões que:
- Têm **situação "Demitido"** (`Situação = 'D'`).
- Não são **transferências sem ônus** (`Tipo de Demissão ≠ '5'`).
- Não são de **cargos especiais** (`Tipo Funcionário ≠ 'C'`, `'S'`, `'T'`, `'U'`, `'Z'`).
  - `C`: Conselheiro.
  - `S`: Pensionista.
  - `T`: Estagiário.
  - `U`: Outros.
  - `Z`: Aprendiz.
- Não são por **motivos excluídos** (`Tipo de Demissão ≠ 'A'`, `'D'`, `'E'`, `'F'`, `'I'`, `'J'`, `'P'`, `'R'`, `'S'`, `'U'`).
  - Exemplo: Aposentadoria, falecimento, rescisão por idade.

#### **Critérios de Exclusão**
Não são contadas como *Turnover*:
- **Transferências internas** (`Tipo de Demissão = '5'`).
- **Falecimentos** (`Tipo de Demissão = '8'`).
- **Aposentadorias** (`Tipo de Demissão = 'A'`, `'D'`, `'E'`, etc.).
- **Demissões de estagiários/aprendizes**.
- **Funcionários offshore** (a menos que especificado).

#### **Casos Especiais**
- **Demissões voluntárias vs. involuntárias**:
  - **Voluntárias**: `Tipo de Demissão = '4'`, `'V'`.
  - **Involuntárias**: `Tipo de Demissão = '1'`, `'2'`, `'3'`, `'8'`, `'N'`, `'T'`.
- **Funcionários readmitidos**:
  - São marcados com `readimitido = 'Sim'` e contabilizados separadamente.

---

### **2.3 New Hire (Novas Contratações)**
#### **Definição**
Funcionários **contratados recentemente** (até 1 ano de empresa).

#### **Critérios de Inclusão**
São classificados como *New Hire* os funcionários que:
- Têm **menos de 1 ano de empresa** (`tempo_empresa_dias < 365`).
- Estão **ativos** (`headcount_flag_new = 'TRUE'`).
- Não são **estagiários/aprendizes**.

#### **Critérios de Exclusão**
Não são contados como *New Hire*:
- Funcionários com **mais de 1 ano de empresa**.
- **Estagiários/aprendizes**.
- **Funcionários inativos**.

#### **Casos Especiais**
- **Admitidos no mês**:
  - Marcados com `admitido_flag = 'TRUE'`.
- **Admitidos nos últimos 3 meses**:
  - Marcados com `admitido_flag_3meses = 'TRUE'`.

---

### **2.4 Vagas Abertas (Posições em Aberto)**
#### **Definição**
Vagas **em processo de recrutamento**, desde a abertura até o fechamento.

#### **Critérios de Inclusão**
São contadas como **vagas abertas** as posições que:
- Estão com **status "Em Andamento"** ou **"Em Admissão"**.
- Não são para **aprendizes/estagiários** (`POSICAO ≠ '*APRENDIZ*'`, `'*ESTAG*'`).
- Têm **responsável pela vaga definido** (`RESPONSAVELVAGA ≠ '*NAO DEFINIDO*'`).

#### **Critérios de Exclusão**
Não são contadas:
- Vagas **fechadas** ou **canceladas**.
- Vagas para **aprendizes/estagiários**.
- Vagas sem **responsável definido**.

#### **Casos Especiais**
- **Tempo de recrutamento**:
  - Calculado como a diferença entre `DTAABERTURA` (data de abertura) e `DTACOMITE` (data de comitê).
- **Tempo de admissão**:
  - Diferença entre `DTAINICIO` (data de início) e `DTACOMITE`.

---

### **2.5 Salário Posicionado (Faixas Salariais)**
#### **Definição**
Posicionamento do **salário do funcionário** em relação à faixa salarial de referência para seu cargo.

#### **Critérios de Inclusão**
São classificados em faixas salariais os funcionários que:
- Possuem **salário registrado** (`salario ≠ '#'`).
- Têm **cargo com faixa salarial definida** (`range_salario_key` válido).

#### **Critérios de Exclusão**
Não são classificados:
- Funcionários sem **salário registrado**.
- Cargos sem **faixa salarial cadastrada**.

#### **Casos Especiais**
- **Faixas salariais**:
  | Faixa               | Critério                     |
  |---------------------|------------------------------|
  | Menor que 80%       | `salario/100 < 0.8`          |
  | Entre 80% e 90%     | `0.8 ≤ salario/100 < 0.9`    |
  | Entre 90% e 100%    | `0.9 ≤ salario/100 < 1`     |
  | Entre 100% e 110%   | `1 ≤ salario/100 < 1.1`     |
  | Acima de 120%        | `salario/100 > 1.2`         |

---

## **3. Condicionais e Classificações**
Os dados são segmentados conforme as seguintes regras:

| **Segmentação**          | **Critérios**                                                                 |
|--------------------------|------------------------------------------------------------------------------|
| **Faixa Etária**         | - Até 30 anos: `idade ≤ 30`.<br>- 31 a 50 anos: `30 < idade ≤ 50`.<br>- Acima de 50: `idade > 50`. |
| **Tipo de Contratação**  | - **Líder**: `Carreira = '1-Gestão'` ou `Grupo Relatório = '5 - Especialista'`.<br>- **Operacional**: `Grupo de Cargo 2 = 'Operacional'`. |
| **Gênero**               | - Masculino: `Sexo = 'M'`.<br>- Feminino: `Sexo = 'F'`.<br>- Não informado: `Sexo ≠ 'M' ou 'F'`. |
| **Tipo de Demissão**    | - **Voluntária**: `Tipo de Demissão = '4' ou 'V'`.<br>- **Involuntária**: `Tipo de Demissão = '1', '2', 'N', 'T'`. |
| **Status da Vaga**      | - **Em Andamento**: `STATUS = 'EM ANDAMENTO'`.<br>- **Fechada**: `STATUS ≠ 'EM ANDAMENTO'`. |

---

## **4. Campos e Flags de Apoio**
Campos utilizados para aplicar as regras de negócio:

| **Campo**                     | **Significado**                                                                 |
|-------------------------------|---------------------------------------------------------------------------------|
| `headcount_flag_new`          | Indica se o funcionário deve ser contado no *Headcount* (`TRUE`/`FALSE`).       |
| `new_hire_flag`               | Indica se o funcionário é uma nova contratação (`TRUE`/`FALSE`).               |
| `admitido_flag`               | Indica se o funcionário foi admitido no mês (`TRUE`/`FALSE`).                  |
| `turnover_flag`               | Indica se a demissão deve ser contada no *Turnover* (`TRUE`/`FALSE`).           |
| `offshore`                    | Indica se o funcionário é offshore (`1` = Sim, `0` = Não).                     |
| `short_tenure`                | Indica se o funcionário foi demitido antes do fim do mês de admissão (`1` = Sim).|
| `readimitido`                 | Indica se o funcionário foi readmitido (`Sim`/`Não`).                           |
| `demissao_classificacao`     | Classifica a demissão como `Voluntária` ou `Involuntária`.                     |
| `posic_fs`                    | Posicionamento do salário em relação à faixa salarial (ex.: `85%`).              |
| `agrup_fs`                    | Faixa salarial agrupada (ex.: `Entre 90% e 100%`).                              |

---

## **5. O Que é Incluído e o Que é Excluído no Dashboard**

### **5.1 Headcount**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Funcionários ativos (`Situação = 'A'`). | Estagiários (`Tipo Funcionário = 'T'`). |
| Funcionários em férias/licença.       | Aprendizes (`Tipo Funcionário = 'Z'`). |
| Funcionários com centro de custo válido. | Conselheiros/cargos especiais.       |
|                                       | Funcionários offshore (`offshore = 1`). |
|                                       | Admitidos e demitidos no mesmo mês. |

### **5.2 Turnover**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Demissões voluntárias/involuntárias.  | Transferências internas (`Tipo Demissão = '5'`). |
| Funcionários com mais de 3 meses.     | Falecimentos (`Tipo Demissão = '8'`). |
|                                       | Aposentadorias.                      |
|                                       | Estagiários/aprendizes.              |

### **5.3 New Hire**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Funcionários com menos de 1 ano.      | Estagiários/aprendizes.              |
| Ativos no mês.                        | Funcionários inativos.               |

### **5.4 Vagas Abertas**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Vagas em andamento.                   | Vagas para aprendizes/estagiários.   |
| Vagas com responsável definido.       | Vagas fechadas/canceladas.            |

---

## **6. Glossário**
| **Termo**               | **Definição**                                                                 |
|-------------------------|------------------------------------------------------------------------------|
| **Headcount**           | Número total de funcionários ativos em um período.                         |
| **Turnover**            | Taxa de rotatividade (saída de funcionários).                              |
| **New Hire**            | Funcionário contratado há menos de 1 ano.                                   |
| **Short Tenure**        | Funcionário demitido antes do fim do mês de admissão.                      |
| **Offshore**            | Funcionário alocado em outra país/sede.                                     |
| **Readmitido**          | Funcionário que foi demitido e recontratado.                                |
| **Faixa Salarial**      | Intervalos de salário referência para cada cargo (ex.: 80%-90% do mercado). |
| **Centro de Custo**     | Unidade organizacional que acumula custos (ex.: departamento, filial).      |
| **Coligada**            | Empresa do mesmo grupo (ex.: Eldorado, Florestal, Offshore).                 |
| **RP (Requisição de Pessoal)** | Processo de abertura de vaga.                                          |
