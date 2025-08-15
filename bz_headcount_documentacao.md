# Documentação Técnica

**Arquivo:** `bz_headcount.qvs`  
**Última atualização:** 15/08/2025 13:28:20

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos (Headcount e Métricas Relacionadas)**
*Objetivo:* Explicar de forma clara e acessível as regras de inclusão, exclusão e condicionais aplicadas às métricas de **Headcount** e indicadores relacionados no dashboard de RH.

---

## **1. Visão Geral**
### **Objetivo do Documento**
- Detalhar **o que é contado** e **o que não é contado** em cada métrica do dashboard.
- Explicar **critérios de inclusão/exclusão** para evitar dúvidas na interpretação dos dados.
- Orientar como identificar **casos especiais** (exceções ou tratamentos atípicos).

### **Princípios Gerais**
- Todas as métricas seguem **regras de negócio específicas** para garantir consistência.
- Dados são **segmentados** por:
  - Período (data de referência, mês, ano).
  - Status do funcionário (ativo, inativo, afastado, etc.).
  - Tipo de contrato (CLT, temporário, offshore, etc.).
  - Localização (filial, centro de custo, região).
  - Classificações funcionais (cargo, carreira, grupo salarial).

---
## **2. Regras de Negócio por Indicador/Métrica**

---

### **2.1 Headcount (Total de Funcionários)**
**Definição:**
Número total de **funcionários ativos** na empresa em um determinado período, considerando critérios de vínculo empregatício e status.

#### **Critérios de Inclusão (o que é contado)**
✅ **Funcionários ativos** com contrato **CLT** (Consolidação das Leis do Trabalho) ou **equivalente** (ex.: offshore com vínculo direto).
✅ **Funcionários em período de experiência** (mesmo que ainda não efetivados).
✅ **Funcionários afastados por licença médica ou férias** (mantêm vínculo ativo).
✅ **Funcionários em home office ou regime híbrido** (independentemente da localização física).
✅ **Funcionários de filiais nacionais e internacionais** (desde que vinculados à empresa matriz).
✅ **Trainees e estagiários** (se registrados no sistema com matrícula ativa).

#### **Critérios de Exclusão (o que não é contado)**
❌ **Funcionários demitidos ou com contrato encerrado** (mesmo que ainda constem em sistemas legados).
❌ **Terceirizados ou prestadores de serviço** (sem vínculo direto com a empresa).
❌ **Funcionários em processo de desligamento** (após comunicação formal da demissão).
❌ **Aposentados** (mesmo que recebam benefícios da empresa).
❌ **Funcionários de empresas coligadas ou parceiras** (exceto se houver integração contratual específica).
❌ **Candidatos em processo seletivo** (não contratados).

#### **Casos Especiais (exceções)**
🔹 **Funcionários offshore:**
   - Incluídos **somente se** o contrato for gerenciado diretamente pela empresa (não por intermediárias).
   - Excluídos se forem **terceirizados** via empresa local no exterior.

🔹 **Afastamentos longos (acima de 12 meses):**
   - **Incluídos** se o afastamento for por **licença médica ou maternidade**.
   - **Excluídos** se for por **licença não remunerada** ou acordo de suspensão contratual.

🔹 **Funcionários em transição entre cargos:**
   - Contados **apenas uma vez**, no cargo de destino (evita duplicidade).

---
### **2.2 Headcount Histórico (2014–2018)**
**Definição:**
Total de funcionários em anos anteriores, usado para **análise de tendências e crescimento**.

#### **Critérios de Inclusão**
✅ Mesmos critérios do **Headcount atual**, mas aplicados a dados históricos.
✅ **Ajustes retroativos** (ex.: correção de registros errados em anos passados).

#### **Critérios de Exclusão**
❌ Dados **não consolidados** ou com inconsistências graves (ex.: falta de matrícula).
❌ Funcionários de **empresas adquiridas** que não foram integradas ao sistema.

#### **Casos Especiais**
🔹 **Fusões/aquisições:**
   - Funcionários de empresas adquiridas são incluídos **a partir da data de integração oficial**.

---
### **2.3 Movimentações de Pessoal (Admissões, Demissões, Transferências)**
**Definição:**
Registro de **entrada, saída ou realocação** de funcionários no período.

#### **Critérios de Inclusão**
✅ **Admissões:** Contratações com registro em folha de pagamento.
✅ **Demissões:** Desligamentos com data de saída formalizada.
✅ **Transferências:** Mudanças de cargo, filial ou centro de custo **com registro no sistema**.

#### **Critérios de Exclusão**
❌ **Movimentações canceladas** (ex.: admissão desfeita antes da data de início).
❌ **Transferências internas sem alteração contratual** (ex.: mudança de mesa sem mudança de cargo).

#### **Casos Especiais**
🔹 **Recontratações:**
   - Contadas como **nova admissão** se houver intervalo de mais de 6 meses desde a demissão.

---
### **2.4 Posições Abertas (Vagas em Aberto)**
**Definição:**
Vagas **autorizadas para contratação** mas ainda não preenchidas.

#### **Critérios de Inclusão**
✅ Vagas com **budget aprovado** e publicadas internamente/externamente.
✅ Vagas **em processo seletivo** (mesmo sem candidatos ainda).

#### **Critérios de Exclusão**
❌ Vagas **congeladas** (sem previsão de preenchimento).
❌ Vagas **canceladas** (budget revogado).

---
### **2.5 Turnover (Rotatividade)**
**Definição:**
Percentual de **funcionários que saíram da empresa** em relação ao total no período.

#### **Critérios de Inclusão**
✅ **Demissões voluntárias e involuntárias** (exceto aposentadorias).
✅ **Término de contrato temporário** (se não houver renovação).

#### **Critérios de Exclusão**
❌ **Transferências internas** (não são consideradas saída).
❌ **Falecimentos** (não impactam a métrica de rotatividade).

#### **Cálculo**
```
Turnover (%) = (Nº de saídas no período / Headcount médio no período) × 100
```
---
## **3. Condicionais e Classificações**
Como os dados são **agrupados e filtrados** no dashboard:

| **Classificação**       | **Descrição**                                                                 |
|--------------------------|-------------------------------------------------------------------------------|
| **Por Período**          | Mês/ano de referência (ex.: "Headcount em dezembro/2023").                  |
| **Por Status**           | Ativo, inativo, afastado, em experiência.                                   |
| **Por Tipo de Contrato** | CLT, temporário, offshore, trainee.                                         |
| **Por Localização**      | Filial, centro de custo, região (Sudeste, Nordeste, etc.).                   |
| **Por Faixa Salarial**   | Ex.: "Até R$ 3.000", "R$ 3.001 a R$ 8.000", "Acima de R$ 15.000".           |
| **Por Cargo/Carreira**  | Gerente, analista, operacional; carreira técnica ou administrativa.          |
| **Por Idade**            | "Até 30 anos", "31 a 50 anos", "Acima de 50 anos".                          |

---
## **4. Campos e Flags de Apoio**
Campos usados para aplicar as regras (sem detalhes técnicos):

| **Campo/Flag**               | **Significado**                                                                 |
|------------------------------|---------------------------------------------------------------------------------|
| **Status do Funcionário**    | "Ativo", "Inativo", "Afastado", "Em Experiência".                             |
| **Tipo de Contrato**         | "CLT", "Temporário", "Offshore", "Trainee".                                   |
| **Flag de Movimentação**     | "Admissão", "Demissão", "Transferência", "Promoção".                          |
| **Centro de Custo**          | Unidade organizacional responsável pelo custo do funcionário.                |
| **Grupo de Cargo**           | Classificação por nível hierárquico (ex.: "Operacional", "Gerencial").        |
| **Flag Offshore**            | "Sim" (contrato direto), "Não" (terceirizado).                                 |

---
## **5. O que é Incluído e o que é Excluído no Dashboard**
### **Tabela Resumo**

| **Métrica**               | **Inclusão**                                                                 | **Exclusão**                                                                 |
|----------------------------|------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Headcount**              | Funcionários ativos (CLT, offshore direto, trainees).                       | Terceirizados, demitidos, aposentados.                                      |
| **Headcount Histórico**    | Dados consolidados de 2014–2018 com ajustes retroativos.                     | Dados não validados ou de empresas não integradas.                          |
| **Movimentações**          | Admissões, demissões e transferências registradas.                          | Movimentações canceladas ou sem alteração contratual.                       |
| **Posições Abertas**       | Vagas com budget aprovado e em processo seletivo.                           | Vagas congeladas ou canceladas.                                              |
| **Turnover**               | Demissões voluntárias/involuntárias e término de temporários.               | Transferências internas, falecimentos, aposentadorias.                      |

---
## **6. Glossário**
| **Termo**               | **Definição**                                                                 |
|-------------------------|------------------------------------------------------------------------------|
| **CLT**                 | Contrato regido pela Consolidação das Leis do Trabalho (vínculo empregatício formal). |
| **Offshore**            | Funcionário contratado para trabalhar no exterior, com vínculo direto ou indireto. |
| **Centro de Custo**     | Unidade organizacional que acumula os custos de um funcionário ou projeto.  |
| **Headcount Médio**     | Média do número de funcionários em um período (ex.: (Jan + Dez)/2).         |
| **Budget**              | Orçamento aprovado para contratações ou despesas.                            |
| **Trainee**             | Programa de treinamento para novos funcionários (geralmente recém-formados). |
| **Flag**                | Indicador (sim/não) usado para classificar registros (ex.: "Flag Offshore").  |

---
**Observação Final:**
- Em caso de dúvidas sobre **casos não cobertos**, consulte a equipe de People Analytics.
- Regras podem ser ajustadas para **filiais específicas** ou **projetos especiais** (verifique com o gestor de RH).
