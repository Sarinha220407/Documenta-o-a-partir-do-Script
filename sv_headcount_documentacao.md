# Documentação Técnica

**Arquivo:** `sv_headcount.qvs`  
**Última atualização:** 15/08/2025 13:55:23

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos (RH)**
*Documentação técnica para usuários finais não técnicos*

---

## **1. Visão Geral**
### **Objetivo do Documento**
Este documento explica as **regras de negócio** aplicadas aos indicadores do dashboard de RH, incluindo:
- **O que é contado** (critérios de inclusão).
- **O que não é contado** (critérios de exclusão).
- **Casos especiais** (exceções e tratamentos atípicos).

### **Como Identificar o Que Deve Ser Contado**
Cada métrica segue critérios específicos. Para verificar se um registro deve ser incluído:
1. Confira se atende aos **critérios de inclusão**.
2. Verifique se **não se enquadra nos critérios de exclusão**.
3. Considere **casos especiais** (exceções).

---

## **2. Regras de Negócio por Indicador/Métrica**

### **2.1. Headcount (Número de Funcionários)**
#### **Definição**
Quantidade de funcionários **ativos** em um determinado período, considerando contratações, demissões e afastamentos.

#### **Critérios de Inclusão**
- Funcionários com **situação ativa** (`Situação = 'A'`).
- Funcionários em **licenças remuneradas** (ex.: licença-maternidade, férias, afastamento médico).
- Funcionários **contratados até a data de referência** (mesmo que a admissão seja futura, desde que cadastrados no sistema).
- Funcionários **offshore** (marcados com `offshore = 1`).
- Funcionários **recontratados** (com mais de uma admissão no histórico).

#### **Critérios de Exclusão**
- Funcionários **demitidos** (`Situação = 'D'`).
- Funcionários com **matrícula apagada** (`Situação = 'Z'`).
- **Estagiários** (`Tipo Funcionário = 'T'` ou `Funções TEXT` contém "Estagiário").
- **Aprendizes** (`Tipo Funcionário = 'Z'`).
- Funcionários com **centro de custo inválido** (ex.: `Centro de Custo = '#'` ou menor que 100).
- **Conselheiros e cargos especiais** (ex.: "Conselheiro Adm", "Conselheiro Fiscal").
- Funcionários com **chapa específica excluída** (lista de IDs no script).

#### **Casos Especiais**
- **Admitidos e demitidos no mesmo mês**:
  - São contados como **headcount**, mas marcados com `short_tenure = 1` e `Situação TEXT = 'C/Dem no mês'`.
- **Funcionários com salário fora da faixa**:
  - Classificados em grupos como:
    - `Menor 80%` (salário < 80% da referência).
    - `Entre 80% e 90%`.
    - `Acima 120%`.
- **Funcionários sem hierarquia definida**:
  - O gestor direto é definido como o primeiro nível válido na hierarquia (do nível 1 ao 6).

---

### **2.2. Turnover (Rotatividade)**
#### **Definição**
Taxa de funcionários que **saíram da empresa** em um período, considerando demissões voluntárias e involuntárias.

#### **Critérios de Inclusão**
- Funcionários com **demissão registrada** (`Situação = 'D'`).
- Demissões **não relacionadas a transferências** (`Tipo de Demissão ≠ 5`).
- Funcionários **não estagiários/aprendizes** (`Tipo Funcionário ≠ 'T', 'Z'`).
- Demissões **classificadas como turnover** (exclui aposentadorias, falecimentos, transferências).

#### **Critérios de Exclusão**
- **Transferências internas** (`Tipo de Demissão = 5`).
- **Aposentadorias** (`Tipo de Demissão = 'A', 'D', 'E', 'F', 'I', 'J', 'P', 'R', 'S', 'U'`).
- **Falecimentos** (`Tipo de Demissão = '8'`).
- **Estagiários e aprendizes** (`Tipo Funcionário = 'T', 'Z'`).

#### **Casos Especiais**
- **Demissões voluntárias vs. involuntárias**:
  - **Voluntárias**: `Tipo de Demissão = '4', 'V'`.
  - **Involuntárias**: `Tipo de Demissão = '2', '8', 'N', 'T'`.
- **Funcionários readmitidos**:
  - Marcados com `readimitido = 'Sim'` se tiverem mais de uma admissão.

---

### **2.3. Vagas Abertas (Posições em Aberto)**
#### **Definição**
Quantidade de **vagas em processo de recrutamento**, incluindo substituições e novas posições.

#### **Critérios de Inclusão**
- Vagas com **status "Em Andamento"** ou **"Em Admissão"**.
- Vagas com **data de abertura válida** (`DTAABERTURA` preenchida).
- Vagas **não relacionadas a estagiários/aprendizes** (`POSICAO` não contém "APRENDIZ" ou "ESTAG").

#### **Critérios de Exclusão**
- Vagas **sem responsável definido** (`RESPONSAVELVAGA = 'NÃO DEFINIDO'`).
- Vagas **para aprendizes/estagiários** (`POSICAO` contém "APRENDIZ" ou "ESTAG").
- Vagas **sem centro de custo válido** (`CCUSTO` vazio).

#### **Casos Especiais**
- **Tempo de recrutamento**:
  - Calculado como a diferença entre `DTAABERTURA` e `DTACOMITE` (data de comitê).
  - Se a vaga estiver **em andamento**, usa a data atual (`TODAY()`).
- **Classificação da vaga**:
  - **Substituição**: `CLASSIFICACAO = 'Substituição'`.
  - **Nova posição**: Outros casos.

---

### **2.4. New Hires (Novas Contratações)**
#### **Definição**
Funcionários **contratados recentemente** (até 1 ano de empresa).

#### **Critérios de Inclusão**
- Funcionários com **menos de 1 ano de admissão** (`tempo_empresa_dias < 365`).
- Funcionários **ativos** (`headcount_flag_new = 'TRUE'`).
- Funcionários **não estagiários/aprendizes**.

#### **Critérios de Exclusão**
- Funcionários **demitidos** (`Situação ≠ 'A'`).
- **Estagiários e aprendizes** (`Funções TEXT` contém "Estagiário" ou `Tipo Funcionário = 'T'`).

#### **Casos Especiais**
- **Contratações no mês**:
  - Marcadas com `admitido_flag = 'TRUE'` se admitidos no mesmo mês da referência.
- **Contratações nos últimos 3 meses**:
  - Marcadas com `admitido_flag_3meses = 'TRUE'`.

---

### **2.5. Salário e Faixas Salariais**
#### **Definição**
Análise da **posição salarial** dos funcionários em relação à faixa de referência.

#### **Critérios de Inclusão**
- Funcionários com **salário registrado** (`salario` preenchido).
- Funcionários **ativos ou em afastamentos remunerados**.

#### **Critérios de Exclusão**
- Funcionários **sem salário cadastrado**.
- **Estagiários e aprendizes**.

#### **Casos Especiais**
- **Faixas salariais**:
  - `Menor 80%`: Salário < 80% da referência.
  - `Entre 100% e 110%`: Salário entre 100% e 110%.
  - `Acima 120%`: Salário > 120%.
- **Funcionários offshore**:
  - Salários podem seguir faixas diferentes (`offshore = 1`).

---

## **3. Condicionais e Classificações**
### **Segmentação dos Dados**
Os dados são classificados por:
- **Período**: Mês/ano de referência (`load_date`).
- **Faixa etária**:
  - `Até 30 anos`.
  - `De 31 a 50 anos`.
  - `Acima de 50 anos`.
- **Gênero**: `Masculino`, `Feminino`, `Não informado`.
- **Tipo de funcionário**:
  - `Normal`, `Líder`, `Operacional`, `Técnico`.
- **Status da vaga**:
  - `Em Andamento`, `Concluída`, `Cancelada`.
- **Classificação de demissão**:
  - `Voluntária`, `Involuntária`.

---

## **4. Campos e Flags de Apoio**
| **Campo/Flag**               | **Significado**                                                                 |
|------------------------------|-------------------------------------------------------------------------------|
| `headcount_flag_new`          | Indica se o funcionário deve ser contado no headcount (`TRUE`/`FALSE`).       |
| `new_hire_flag`              | Funcionário com menos de 1 ano de empresa (`TRUE`/`FALSE`).                   |
| `admitido_flag`              | Funcionário admitido no mês de referência (`TRUE`/`FALSE`).                  |
| `turnover_flag`               | Demissão considerada no cálculo de turnover (`TRUE`/`FALSE`).                 |
| `offshore`                   | Funcionário offshore (`1` = Sim, `0` = Não).                                  |
| `short_tenure`               | Funcionário admitido e demitido no mesmo mês (`1` = Sim).                     |
| `readimitido`                | Funcionário readmitido (`Sim`/`Não`).                                         |
| `gestor_direto_nome`         | Nome do gestor direto (primeiro nível válido na hierarquia).                  |
| `posic_fs`                   | Posição do salário em relação à faixa de referência (ex.: `95%`).             |
| `agrup_fs`                   | Grupo de faixa salarial (ex.: `Entre 90% e 100%`).                            |

---

## **5. O que é Incluído e o que é Excluído no Dashboard**

| **Métrica**          | **Inclusão**                                                                 | **Exclusão**                                                                 |
|----------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Headcount**        | Funcionários ativos, em licença, offshore, recontratados.                  | Demitidos, estagiários, aprendizes, matrículas apagadas, conselheiros.      |
| **Turnover**         | Demissões voluntárias/involuntárias (exceto transferências).               | Aposentadorias, falecimentos, transferências, estagiários.                   |
| **Vagas Abertas**    | Vagas em andamento com responsável definido.                              | Vagas para estagiários, sem centro de custo, sem responsável.                |
| **New Hires**        | Funcionários com <1 ano de empresa, ativos.                                | Demitidos, estagiários, aprendizes.                                         |
| **Salário**          | Funcionários ativos com salário cadastrado.                                | Sem salário, estagiários, aprendizes.                                       |

---

## **6. Glossário**
| **Termo**               | **Definição**                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| **Headcount**           | Contagem total de funcionários ativos em um período.                       |
| **Turnover**            | Taxa de rotatividade (saída de funcionários).                              |
| **New Hire**            | Funcionário contratado recentemente (até 1 ano).                           |
| **Offshore**            | Funcionários alocados em unidades no exterior.                              |
| **Short Tenure**        | Funcionário admitido e demitido no mesmo mês.                              |
| **Faixa Salarial**      | Intervalos de salário em relação a uma referência (ex.: 80%-90%).          |
| **Gestor Direto**       | Primeiro nível de hierarquia acima do funcionário.                          |
| **RP (Requisição de Pessoal)** | Processo de abertura de vaga.                                          |
| **Coligada**            | Empresa do grupo (ex.: Eldorado, Florestal).                                |
| **Centro de Custo**     | Unidade organizacional responsável por custos (ex.: RH, Produção).         |
| **PCD**                 | Pessoa com Deficiência.                                                    |
