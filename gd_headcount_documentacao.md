# Documentação Técnica

**Arquivo:** `gd_headcount.qvs`  
**Última atualização:** 15/08/2025 13:29:53

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos (RH)**
*Objetivo:* Explicar de forma clara e acessível as regras de inclusão, exclusão e condicionais aplicadas às métricas do dashboard de RH.

---

## **1. Visão Geral**
### **Objetivo do Documento**
Este documento detalha:
- **O que é contado** em cada métrica (ex.: *Headcount*, *Turnover*, *Tempo na Empresa*).
- **O que é excluído** e por quê.
- **Casos especiais** (exceções ou tratamentos específicos).
- **Como os dados são segmentados** (por período, faixa etária, região, etc.).

### **Critérios Gerais de Inclusão/Exclusão**
Todas as métricas seguem regras baseadas em:
- **Status do funcionário** (ativo, desligado, afastado, etc.).
- **Tipo de contratação** (CLT, temporário, estagiário, etc.).
- **Período de referência** (data de admissão, desligamento ou corte do relatório).
- **Hierarquia e localização** (filial, centro de custo, diretoria).

---
## **2. Regras de Negócio por Indicador/Métrica**

---

### **2.1 Headcount (Número de Funcionários Ativos)**
**Definição:**
Contagem de **funcionários ativos** na empresa em um determinado período.

#### **Critérios de Inclusão**
- Funcionários com **status = "Ativo"** na data de referência.
- Todos os **tipos de contratação** (CLT, temporários, estagiários, etc.), **exceto** os listados em *Critérios de Exclusão*.
- Funcionários **readmitidos** (contados como novos registros a partir da data de readmissão).
- Funcionários em **afastamentos temporários** (ex.: licença médica, férias) **se mantiverem vínculo ativo**.

#### **Critérios de Exclusão**
- Funcionários **desligados** (independentemente da data).
- **Terceirizados** (não são contabilizados no *Headcount* interno).
- **Funcionários em processo de demissão** (status = "Avisado" ou "Demissionário").
- **Estagiários não remunerados** (se houver).
- **Funcionários com contrato suspenso** (ex.: licença não remunerada).

#### **Casos Especiais**
- **Funcionários em transição entre áreas:**
  - Contados na **nova área** a partir da data oficial de transferência.
- **Funcionários com dupla função:**
  - Contados **uma única vez**, na função principal (definida pelo sistema).
- **Contratos temporários:**
  - Incluídos no *Headcount* **somente durante o período de vigência do contrato**.

---

### **2.2 Turnover (Rotatividade)**
**Definição:**
Porcentagem de funcionários que **saíram da empresa** em um período, em relação ao *Headcount* médio do mesmo período.

#### **Critérios de Inclusão**
- **Desligamentos voluntários ou involuntários** (demissões, pedidos de demissão, aposentadorias).
- Funcionários com **status = "Desligado"** na data de referência.
- **Todas as causas de desligamento** (performance, redução de quadro, falecimento, etc.).

#### **Critérios de Exclusão**
- **Transferências internas** (não são consideradas saídas).
- **Afastamentos temporários** (ex.: licença maternidade, se o vínculo permanecer ativo).
- **Terceirizados** (não entram no cálculo).
- **Funcionários em processo de demissão** (ainda não desligados oficialmente).

#### **Casos Especiais**
- **Readmissões:**
  - Se um funcionário sai e retorna, o desligamento **é contado no *Turnover***, mas a readmissão **não reduz o indicador**.
- **Desligamentos em massa (layoffs):**
  - Tratados como um **evento único** no cálculo (evita distorções).
- **Funcionários com contrato temporário encerrado:**
  - Incluídos no *Turnover* **somente se não forem recontratados** em até 30 dias.

---
### **2.3 Tempo na Empresa**
**Definição:**
Tempo médio ou distribuído que os funcionários permanecem na empresa, segmentado por faixas.

#### **Critérios de Inclusão**
- **Funcionários ativos e desligados** (para análise histórica).
- **Tempo calculado em dias** a partir da **data de admissão** até:
  - Data atual (para ativos).
  - Data de desligamento (para inativos).

#### **Critérios de Exclusão**
- **Períodos de afastamento não remunerado** (ex.: licença sem vínculo).
- **Tempo em outras empresas do grupo** (somente o período na empresa atual é considerado).

#### **Faixas de Tempo (Grupos)**
| **Grupo Gerencial**       | **Grupo Operacional**       |
|---------------------------|-----------------------------|
| Ano 1                     | 0–3 meses                   |
| Ano 2                     | 3–6 meses                   |
| Ano 3                     | 9–12 meses                  |
| Anos 4–6                  | Ano 2 – 18–24 meses         |
| Anos 7–10                 | Ano 3 – 24–30 meses         |
| Anos 11–15                | Ano 4 – 30–36 meses         |
| Mais que 15 anos          | Mais que 4 anos             |

#### **Casos Especiais**
- **Funcionários readmitidos:**
  - O tempo é **zerado** na readmissão (novo ciclo).
- **Transferências entre empresas do grupo:**
  - O tempo é **acumulado** se houver continuidade contratual.

---
### **2.4 Vagas Abertas**
**Definição:**
Número de **posições disponíveis para contratação** em um período.

#### **Critérios de Inclusão**
- Vagas **aprovadas no orçamento** e ainda não preenchidas.
- Vagas **em processo seletivo** (independentemente do status).
- Vagas **reabertas** após desligamento.

#### **Critérios de Exclusão**
- Vagas **congeladas** (sem previsão de preenchimento).
- Vagas **temporárias** (ex.: substituição de licença médica).
- Posições **em reestruturação** (sem definição clara).

#### **Casos Especiais**
- **Vagas recém-criadas:**
  - Contadas a partir da **data de aprovação oficial**.
- **Vagas com múltiplas oportunidades:**
  - Contadas como **uma única vaga** (ex.: 5 vagas para o mesmo cargo = 1 registro).

---
### **2.5 Taxa de Ocupação**
**Definição:**
Porcentagem de **vagas preenchidas** em relação ao total de posições previstas no orçamento.

#### **Cálculo:**
```
Taxa de Ocupação = (Headcount Atual / Total de Posições Orçamentadas) × 100
```

#### **Critérios de Inclusão**
- **Todas as posições orçamentadas** (independentemente de estarem abertas ou não).
- **Funcionários ativos** (incluindo afastamentos temporários).

#### **Critérios de Exclusão**
- Posições **não orçamentadas** (ex.: contratações emergenciais).
- Vagas **em processo de fechamento** (ex.: realocação de verba).

#### **Casos Especiais**
- **Orçamento revisado:**
  - A taxa é recalculada com base no **número mais recente** de posições aprovadas.
- **Overstaffing (excesso de funcionários):**
  - Se o *Headcount* superar o orçamento, a taxa **ultrapassa 100%**.

---
### **2.6 Admissões (New Hires)**
**Definição:**
Número de **novos funcionários contratados** em um período.

#### **Critérios de Inclusão**
- **Primeira admissão** na empresa (independentemente do tipo de contrato).
- **Readmissões** (contadas como novas admissões).
- Contratações **efetivas ou temporárias** (desde que com vínculo formal).

#### **Critérios de Exclusão**
- **Transferências internas** (não são novas admissões).
- **Terceirizados** (não entram no cálculo).
- **Estagiários não remunerados**.

#### **Casos Especiais**
- **Contratos de experiência:**
  - Contados como admissão **somente após a efetivação**.
- **Funcionários em período probatório:**
  - Incluídos na data de **início do contrato**.

---
### **2.7 Demissões (Terminations)**
**Definição:**
Número de **funcionários desligados** da empresa em um período.

#### **Critérios de Inclusão**
- **Todos os tipos de desligamento** (voluntário, involuntário, aposentadoria, falecimento).
- **Desligamentos oficiais** (data de saída registrada no sistema).

#### **Critérios de Exclusão**
- **Transferências para outras empresas do grupo** (não são demissões).
- **Afastamentos temporários** (ex.: licença médica).
- **Funcionários em processo de demissão** (ainda não desligados).

#### **Casos Especiais**
- **Demissões em massa:**
  - Registradas como um **evento único** para evitar distorções.
- **Funcionários que saem e retornam:**
  - O desligamento é contado, mas a readmissão **não anula a demissão**.

---
### **2.8 Diversidade (Gênero, Idade, Raça)**
**Definição:**
Distribuição de funcionários por **grupos demográficos**.

#### **Segmentações**
| **Categoria**       | **Faixas**                                                                 |
|---------------------|---------------------------------------------------------------------------|
| **Idade**           | 0–10, 11–20, 21–30, 31–40, 41–50, 51–60, 61–70, 71+                       |
| **Geração**         | Geração Alpha, Z, Y, X, Boomers, Silenciosa                              |
| **Gênero**          | Masculino, Feminino, Não binário, Outros                                 |
| **Raça/Etnia**      | Branca, Negra, Parda, Amarela, Indígena, Não declarada                  |

#### **Critérios de Inclusão**
- **Todos os funcionários ativos** (independentemente do tipo de contrato).
- Dados **autodeclarados** (priorizados sobre registros antigos).

#### **Critérios de Exclusão**
- Funcionários **sem informação declarada** (ex.: raça ou gênero não preenchidos).
- **Terceirizados** (não incluídos na análise de diversidade interna).

#### **Casos Especiais**
- **Funcionários com gênero não binário:**
  - Classificados em **"Outros"** se não houver categoria específica.
- **Raça/Etnia não declarada:**
  - Registrados como **"Não informado"** (não são excluídos do total).

---
## **3. Condicionais e Classificações**
### **Como os Dados São Segmentados**
| **Critério**          | **Exemplos de Segmentação**                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------|
| **Período**           | Mês atual, trimestre, ano, histórico vs. futuro                                           |
| **Faixa Etária**      | 21–30 anos, 41–50 anos, Geração Y                                                          |
| **Localização**       | Filial, região, centro de custo, diretoria                                                |
| **Tipo de Contrato**  | CLT, temporário, estagiário, terceirizado (quando aplicável)                             |
| **Status**            | Ativo, desligado, afastado, em transição                                                 |
| **Tempo na Empresa**  | 0–3 meses, 1–3 anos, 10+ anos                                                             |
| **Cargo/Nível**       | Operacional, liderança, diretoria                                                         |
| **Gênero**            | Masculino, feminino, não binário                                                         |
| **Raça/Etnia**        | Branca, negra, parda, indígena                                                            |

---
## **4. Campos e Flags de Apoio**
### **Campos Usados para Aplicar Regras**
| **Campo**                     | **Significado**                                                                                     | **Exemplo de Uso**                                  |
|-------------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------|
| `headcount_status`            | Status do funcionário (Ativo, Desligado, Afastado).                                                 | Filtrar só ativos para *Headcount*.                |
| `tipo_funcionario_cod`       | Tipo de contrato (CLT, temporário, estagiário).                                                    | Excluir terceirizados das métricas.                |
| `situacao_cod`                | Situação do funcionário (ex.: "Demissionário", "Aposentado").                                      | Identificar desligamentos para *Turnover*.         |
| `tempo_empresa_dias`          | Dias desde a admissão.                                                                             | Classificar em faixas de tempo.                   |
| `new_hire_flag`               | Indica se o funcionário é uma nova contratação (sim/não).                                          | Contar admissões no período.                      |
| `grupo_gerencial`             | Faixa de tempo na empresa (ex.: "Ano 1", "Anos 4–6").                                              | Análise de senioridade.                            |
| `grupo_idade`                 | Faixa etária (ex.: "21–30", "41–50").                                                              | Relatórios de diversidade.                         |
| `geracao`                     | Geração do funcionário (ex.: "Millennial", "Boomer").                                              | Segmentação por perfil demográfico.               |
| `contratacao_tipo`            | Tipo de admissão (ex.: "Efetivo", "Temporário").                                                   | Filtrar contratações temporárias.                  |
| `jornada_mensal`              | Carga horária mensal (ex.: 160h, 220h).                                                            | Classificar por regime de trabalho.                |
| `grupo_diretoria`             | Área de atuação (ex.: "Operações", "RH").                                                          | Análise por departamento.                           |

---
## **5. O que é Incluído e o que é Excluído no Dashboard**
### **Resumo Geral**
| **Métrica**          | **Incluído**                                                                 | **Excluído**                                                                 |
|----------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **Headcount**         | Funcionários ativos, afastados com vínculo, readmitidos.                  | Desligados, terceirizados, estagiários não remunerados.                     |
| **Turnover**          | Desligamentos voluntários/involuntários.                                   | Transferências internas, afastamentos temporários.                        |
| **Tempo na Empresa**  | Dias desde a admissão (ativos e desligados).                               | Períodos sem vínculo (ex.: licença não remunerada).                        |
| **Vagas Abertas**     | Posições orçamentadas e não preenchidas.                                   | Vagas congeladas ou temporárias.                                           |
| **Taxa de Ocupação**  | Headcount vs. posições orçamentadas.                                       | Posições não orçamentadas.                                                |
| **Admissões**         | Novas contratações (inclui readmissões).                                    | Transferências internas, terceirizados.                                   |
| **Demissões**         | Todos os desligamentos oficiais.                                           | Transferências para outras empresas do grupo.                             |
| **Diversidade**       | Funcionários ativos com dados declarados.                                  | Terceirizados, dados não informados.                                       |

---
## **6. Glossário**
| **Termo**               | **Definição**                                                                                     |
|-------------------------|---------------------------------------------------------------------------------------------------|
| **Headcount**           | Número total de funcionários ativos em um período.                                               |
| **Turnover**            | Taxa de rotatividade (saídas de funcionários em relação ao total).                                |
| **New Hire**            | Funcionário recém-contratado (geralmente nos primeiros 6–12 meses).                              |
| **Terceirizado**        | Profissional contratado por empresa externa (não faz parte do quadro interno).                  |
| **Readmissão**          | Funcionário que saiu e voltou a trabalhar na empresa.                                            |
| **Orçamento de Pessoal**| Número de posições aprovadas para contratação em um período.                                    |
| **Overstaffing**        | Situação em que o número de funcionários supera o orçamento.                                    |
| **Afiliada/Coligada**   | Empresa do mesmo grupo econômico.                                                                |
| **Escala de Trabalho**  | Regime de horas trabalhadas (ex.: 160h/mês, 220h/mês).                                           |
| **CBO**                | Classificação Brasileira de Ocupações (código que padroniza cargos).                            |
| **Jornada Mensal**      | Total de horas trabalhadas por mês conforme contrato.                                           |
| **Flag**               | Indicador booleano (sim/não) para classificar registros (ex.: `new_hire_flag`).                   |
| **Hash/Chave (SK)**     | Código único gerado para identificar registros sem repetição (ex.: `hierarquia_sk`).            |
| **Diretoria**          | Nível hierárquico acima das gerências (ex.: Diretoria de Operações).                              |
| **Centro de Custo**    | Unidade organizacional que acumula despesas (ex.: RH, Produção).                                  |
| **Geração Alpha/Z/Y**   | Classificação por faixa etária/nascimento (ex.: Geração Y = nascidos entre 1981–1995).           |
