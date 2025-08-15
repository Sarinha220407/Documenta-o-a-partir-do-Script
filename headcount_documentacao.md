# Documentação Técnica

**Arquivo:** `headcount.qvs`  
**Última atualização:** 15/08/2025 13:31:22

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos (RH)**
*Objetivo:* Explicar as regras de inclusão, exclusão e condicionais aplicadas às métricas do dashboard de RH, garantindo clareza para usuários finais não técnicos.

---

## **1. Visão Geral**
### **Objetivo do Documento**
- Detalhar **o que é contado** e **o que é excluído** em cada métrica do dashboard.
- Explicar **critérios de segmentação** (ex.: por idade, tipo de demissão, cargo, etc.).
- Listar **casos especiais** e exceções nas regras.

### **Como Identificar o Que Deve Ser Contado?**
Cada métrica segue **regras de inclusão e exclusão** baseadas em:
- **Status do funcionário** (ativo, afastado, demitido, etc.).
- **Tipo de contrato** (CLT, estagiário, aprendiz, etc.).
- **Período de referência** (data de admissão, demissão, etc.).
- **Características demográficas** (idade, gênero, PCD, etc.).
- **Flags de negócio** (ex.: "Novo Contratado", "Readmitido", etc.).

---
---

## **2. Regras de Negócio por Indicador/Métrica**

---

### **2.1 Headcount (Número de Funcionários)**
**Definição:**
Total de funcionários **ativos** ou **afastados temporariamente** na empresa em um determinado período.

#### **Critérios de Inclusão (o que é contado):**
- Funcionários com **situação ativa** (`A`), incluindo:
  - Em férias (`F`).
  - Licença maternidade (`E`).
  - Licença médica (`O`).
  - Aviso prévio (`V`).
- Funcionários **admitidos no mês** (mesmo que demitidos no mesmo mês).
- Funcionários **offshore** (coligadas 30, 31, 32).
- Funcionários **readmitidos** (com mais de uma admissão no histórico).
- Funcionários com **centro de custo válido** (código > 99).

#### **Critérios de Exclusão (o que NÃO é contado):**
- **Tipos de funcionários excluídos:**
  - Conselheiros (`Conselheiro Adm`, `Conselheiro Fiscal`).
  - Cargos com códigos `703`, `704`, `706`.
  - Tipos de contrato: `U` (Outros), `S` (Pensionista).
- **Situações excluídas:**
  - Demitidos (`D`) **exceto** se demitidos no mesmo mês da admissão.
  - Matrículas apagadas (`Z`).
  - Admissões futuras (data de admissão > data atual).
- **Funcionários específicos:**
  - Lista de chapas excluídas manualmente (ex.: `999907338`, `50003102`, etc.).

#### **Casos Especiais:**
- **Admitidos e demitidos no mesmo mês:**
  - São contados como **headcount**, mas marcados com `Situação TEXT = "C/Dem no mês"`.
- **Funcionários com salário fora da faixa padrão:**
  - Classificados em grupos como:
    - `Menor 80%` do salário de referência.
    - `Entre 80% e 90%`.
    - `Acima de 120%`.
- **Estagiários e aprendizes:**
  - **Não são contados** no headcount principal, mas aparecem em métricas específicas.

---

### **2.2 Turnover (Rotatividade)**
**Definição:**
Porcentagem de funcionários que **saíram da empresa** em um período, considerando apenas demissões **voluntárias ou involuntárias** relevantes.

#### **Critérios de Inclusão:**
- Demissões com **tipos específicos**:
  - Voluntárias: `1` (Aposentadoria), `4` (Voluntária), `V` (Voluntária).
  - Involuntárias: `2`, `8`, `N`, `T`.
- Funcionários com **tempo mínimo de 1 dia** na empresa.
- **Exclui transferências sem ônus** (`Tipo de Demissão = 5`).

#### **Critérios de Exclusão:**
- **Tipos de demissão não considerados:**
  - Falecimento (`8` – excluído por regra de negócio).
  - Aposentadorias por invalidez (`A`, `D`).
  - Transferências (`5`).
- **Tipos de funcionários excluídos:**
  - Estagiários (`T`).
  - Aprendizes (`Z`).
  - Conselheiros (`C`).
  - Pensionistas (`S`).

#### **Casos Especiais:**
- **Demissões no mesmo mês da admissão:**
  - Não são contadas no turnover (são tratadas como **short tenure**).
- **Readmitidos:**
  - Se demitidos e readmitidos, a demissão **não conta** para turnover.

---

### **2.3 Admissões (New Hires)**
**Definição:**
Funcionários **contratados recentemente**, segmentados por período (ex.: admitidos no mês, nos últimos 3 meses).

#### **Critérios de Inclusão:**
- Funcionários com **data de admissão ≤ data atual**.
- **Flags aplicadas:**
  - `new_hire_flag = TRUE`: Admitidos há **menos de 1 ano**.
  - `admitido_flag = TRUE`: Admitidos **no mês de referência**.
  - `admitido_flag_3meses = TRUE`: Admitidos **nos últimos 3 meses**.

#### **Critérios de Exclusão:**
- Admissões **futuras** (data de admissão > hoje).
- **Tipos de contrato excluídos:**
  - Estagiários (`T`).
  - Aprendizes (`Z`).

---

### **2.4 Vagas Abertas (Posições em Aberto)**
**Definição:**
Vagas **disponíveis para contratação**, incluindo substituições e novas posições.

#### **Critérios de Inclusão:**
- Vagas com **status** `Em Andamento` ou `Em Admissão`.
- Vagas **não preenchidas** (sem responsável definido como `NAO DEFINIDO`).
- **Exclui vagas para aprendizes/estagiários** (palavras-chave no nome da posição).

#### **Critérios de Exclusão:**
- Vagas **arquivadas ou canceladas**.
- Vagas para **aprendizes/estagiários** (ex.: `*APRENDIZ*`, `*ESTAG*`).

#### **Casos Especiais:**
- **Substituições:**
  - Marcadas com `rp_classificacao = "Substituição"`.
- **Vagas por tipo de RP:**
  - Classificadas como `Temporário`, `Efetivo`, etc.

---

### **2.5 Taxa de Ocupação**
**Definição:**
Relação entre **posições ocupadas** e **posições totais** (ocupadas + vagas).

#### **Critérios de Inclusão:**
- **Posições ocupadas:** Headcount ativo.
- **Posições totais:** Headcount + vagas abertas (excluindo aprendizes/estagiários).

#### **Critérios de Exclusão:**
- Vagas **sem centro de custo válido**.
- Posições **excluídas manualmente** (ex.: conselheiros).

---

### **2.6 Demissões (Terminations)**
**Definição:**
Funcionários que **saíram da empresa**, classificados por tipo (voluntária/involuntária).

#### **Critérios de Inclusão:**
- Demissões com **data válida** (≤ hoje).
- **Classificação por tipo:**
  - Voluntária: `1`, `4`, `V`.
  - Involuntária: `2`, `8`, `N`, `T`.

#### **Critérios de Exclusão:**
- **Tipos de demissão não contabilizados:**
  - Transferências (`5`).
  - Falecimentos (`8`).
  - Aposentadorias (`A`, `D`, `E`, etc.).
- **Funcionários excluídos:**
  - Estagiários (`T`).
  - Aprendizes (`Z`).

#### **Casos Especiais:**
- **Demissões no mesmo mês da admissão:**
  - Tratadas como **short tenure** (não entram no turnover).
- **Readmitidos:**
  - Se demitidos e readmitidos, a demissão **não conta** para métricas de rotatividade.

---

### **2.7 Faixas Salariais (Range Salarial)**
**Definição:**
Classificação dos salários em **faixas percentuais** em relação à média do cargo.

#### **Critérios de Inclusão:**
- Salários **normalizados** (divididos por 100 para comparação).
- **Faixas definidas:**
  - `Menor 80%`.
  - `Entre 80% e 90%`.
  - `Entre 100% e 110%`.
  - `Acima de 120%`.

#### **Critérios de Exclusão:**
- Salários **nulos ou inválidos**.
- Cargos **sem tabela salarial definida**.

---

### **2.8 Diversidade (Gênero, Idade, PCD)**
**Definição:**
Distribuição de funcionários por **gênero**, **faixa etária** e **pessoas com deficiência (PCD)**.

#### **Critérios de Inclusão:**
- **Gênero:** `Masculino`, `Feminino`, `Não informado`.
- **Faixa etária:**
  - `Até 30 anos`.
  - `De 31 a 50 anos`.
  - `Acima de 50 anos`.
- **PCD:** Funcionários com `cota_pcd = "Sim"`.

#### **Critérios de Exclusão:**
- Dados **não preenchidos** (ex.: raça não informada).
- Funcionários **excluídos do headcount**.

---

## **3. Condicionais e Classificações**
### **Segmentação dos Dados**
Os dados são agrupados por:

| **Critério**          | **Exemplos de Classificação**                          |
|-----------------------|-------------------------------------------------------|
| **Período**           | Mês atual, último trimestre, ano fiscal.             |
| **Faixa etária**      | Até 30 anos, 31-50 anos, acima de 50 anos.           |
| **Tipo de contrato**  | CLT, estagiário, aprendiz, temporário.               |
| **Status**            | Ativo, afastado, demitido, aviso prévio.            |
| **Localização**       | Filial, centro de custo, diretoria (Corporativo, Industrial, Florestal). |
| **Salário**           | Faixas percentuais (80%-90%, 100%-110%, etc.).        |
| **Turnover**          | Voluntário vs. involuntário.                          |
| **Diversidade**       | Gênero, raça, PCD.                                    |

---

## **4. Campos e Flags de Apoio**
### **Campos Utilizados para Regras de Negócio**

| **Campo**                     | **Descrição**                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `Situação`                    | Status do funcionário (`A`=Ativo, `D`=Demitido, `F`=Férias, etc.).         |
| `Tipo Funcionário`            | Tipo de contrato (`N`=Normal, `T`=Estagiário, `Z`=Aprendiz).               |
| `Tipo de Demissão`            | Classificação da saída (`1`=Voluntária, `2`=Involuntária, `5`=Transferência). |
| `Data Admissão`               | Data de entrada na empresa.                                                 |
| `Data Demissão`               | Data de saída (se aplicável).                                               |
| `Centro de Custo`             | Código do centro de custo (exclui códigos inválidos ou `<= 99`).           |
| `Coligada`                    | Empresa do grupo (ex.: `1`=Eldorado, `30`=Offshore).                       |
| `new_hire_flag`               | `TRUE` se admitido há menos de 1 ano.                                        |
| `turnover_flag`               | `TRUE` se a demissão deve ser contabilizada no turnover.                    |
| `readimitido`                 | `Sim` se o funcionário foi readmitido.                                      |
| `operacional_flag`            | `Operacional` ou `Não Operacional` (baseado no grupo de cargo).              |
| `lider_flag`                  | `Líder` ou `Não Líder` (baseado em carreira ou grupo de relatório).         |
| `cota_pcd`                    | `Sim` se o funcionário é pessoa com deficiência.                           |
| `gestor_direto_nome`          | Nome do gestor imediato (extraído da hierarquia).                           |

---

## **5. O que é Incluído e o que é Excluído no Dashboard**
### **Resumo Geral**

| **Métrica**            | **Incluído**                                                                 | **Excluído**                                                                 |
|------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Headcount**          | Ativos, afastados temporários, offshore, admitidos/demitidos no mesmo mês. | Demitidos (exceto short tenure), conselheiros, aprendizes, matrículas apagadas. |
| **Turnover**           | Demissões voluntárias/involuntárias (exceto transferências).               | Falecimentos, aposentadorias, estagiários, aprendizes.                      |
| **Admissões**          | Novos contratados (há menos de 1 ano).                                      | Admissões futuras, estagiários, aprendizes.                                 |
| **Vagas Abertas**      | Posições em andamento/admissão (exceto aprendizes).                        | Vagas canceladas ou para aprendizes.                                        |
| **Taxa de Ocupação**   | Posições ocupadas + vagas abertas (exceto aprendizes).                     | Vagas sem centro de custo válido.                                           |
| **Demissões**          | Saídas classificadas como voluntárias/involuntárias.                       | Transferências, falecimentos, aposentadorias.                              |
| **Faixas Salariais**   | Salários normalizados em faixas percentuais.                               | Salários nulos ou sem referência.                                           |
| **Diversidade**        | Funcionários com gênero, idade e PCD registrados.                         | Dados não preenchidos.                                                      |

---

## **6. Glossário**
| **Termo**               | **Definição**                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| **Headcount**           | Total de funcionários ativos ou afastados temporariamente.                 |
| **Turnover**            | Taxa de rotatividade (saída de funcionários).                              |
| **New Hire**            | Funcionário admitido há menos de 1 ano.                                     |
| **Short Tenure**        | Admitido e demitido no mesmo mês.                                          |
| **Offshore**            | Funcionários de coligadas internacionais (ex.: Áustria, EUA).              |
| **PCD**                | Pessoa com Deficiência.                                                     |
| **Coligada**            | Empresa do grupo (ex.: Eldorado, Florestal, Offshore).                       |
| **Centro de Custo**    | Unidade organizacional que agrega despesas (ex.: Diretoria Industrial).     |
| **Readmitido**          | Funcionário que saiu e foi recontratado.                                   |
| **Flag**               | Indicador booleano (`TRUE`/`FALSE`) para classificar dados.                 |
| **RP (Requisition)**   | Vaga aberta para contratação.                                               |
| **GS (Grade Salarial)**| Nível salarial do cargo.                                                     |
