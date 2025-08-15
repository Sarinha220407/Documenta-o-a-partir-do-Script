# Documentação Técnica

**Arquivo:** `bz_headcount.qvs`  
**Última atualização:** 15/08/2025 13:48:41

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos (Headcount e Métricas Relacionadas)**

---

## **1. Visão Geral**
### **Objetivo do Documento**
Este documento explica as **regras de negócio** aplicadas aos indicadores do dashboard de **Recursos Humanos**, com foco em **Headcount** (número de funcionários) e métricas relacionadas.

Cada métrica segue **critérios específicos de inclusão e exclusão**, que determinam:
- **O que é contado** (dados válidos para análise).
- **O que não é contado** (dados excluídos por não atenderem às regras).
- **Casos especiais** (exceções ou tratamentos diferenciados).

### **Como Identificar o Que Deve Ser Contado?**
Para verificar se um registro deve ser incluído ou excluído, siga estas perguntas:
1. **O funcionário está ativo no período analisado?**
   - Sim → Incluído.
   - Não → Excluído (exceto em métricas históricas).
2. **O tipo de contrato é elegível?**
   - CLT, temporários (em alguns casos), offshore (quando aplicável) → Incluídos.
   - Estagiários, terceirizados (sem vínculo direto) → Excluídos.
3. **O centro de custo ou filial está dentro do escopo?**
   - Somente filiais e centros de custo **ativos e mapeados** são considerados.
4. **Há flags ou status específicos?**
   - Exemplo: Funcionários em licença médica **podem ser contados** em algumas métricas, mas não em outras.

---

## **2. Regras de Negócio por Indicador/Métrica**

### **2.1. Headcount (Número de Funcionários)**
#### **Definição**
Quantidade total de **funcionários ativos** em um determinado período, considerando vínculo empregatício direto com a empresa.

#### **Critérios de Inclusão**
São contados como **Headcount** os funcionários que atendem **todos** os seguintes requisitos:
- **Status ativo** no sistema de folha de pagamento.
- **Vínculo empregatício direto** (CLT, contratos temporários com registro, offshore quando aplicável).
- **Centro de custo ou filial válidos** (mapeados na base de dados).
- **Data de admissão anterior ou igual ao período de análise**.
- **Data de desligamento posterior ou igual ao período de análise** (ou sem data de desligamento).

#### **Critérios de Exclusão**
Não são contados no **Headcount**:
- Funcionários **desligados** antes do período analisado.
- **Estagiários** (sem vínculo CLT).
- **Terceirizados** (sem contrato direto com a empresa).
- Funcionários com **centro de custo inativo ou não mapeado**.
- Registros com **dados incompletos** (ex.: matrícula inválida, cargo não cadastrado).
- **Funcionários em licença não remunerada** (exceto se houver regra específica para inclusão).

#### **Casos Especiais**
| Situação | Tratamento |
|----------|------------|
| **Funcionários em licença médica remunerada** | Contados no Headcount. |
| **Funcionários em férias** | Contados no Headcount. |
| **Contratos temporários** | Incluídos apenas se tiverem **registro formal** e centro de custo válido. |
| **Funcionários offshore** | Incluídos somente se a fonte de dados (`bz_headcount_offshore_f`) estiver integrada ao dashboard. |
| **Funcionários com dupla matrícula** | Contados uma única vez (evita duplicidade). |
| **Headcount histórico (2014–2018)** | Usa base manual (`hc_historica_f.xlsx`), com validação de consistência dos dados. |

---

### **2.2. Headcount por Cargo/Área**
#### **Definição**
Distribuição dos funcionários por **cargo, carreira, grupo de cargo ou área organizacional**.

#### **Critérios de Inclusão**
- Mesmas regras do **Headcount geral** (status ativo, vínculo direto, etc.).
- **Cargo cadastrado** na tabela de funções (`bz_excel_funcao_d`).
- **Centro de custo associado a uma área válida** (mapeado em `bz_excel_estrutura_cc_d`).

#### **Critérios de Exclusão**
- Funcionários sem **cargo definido** ou com cargo não mapeado.
- Áreas ou centros de custo **desativados**.

#### **Casos Especiais**
| Situação | Tratamento |
|----------|------------|
| **Cargos com múltiplas descrições** | Usa a descrição **oficial** do CBO (Classificação Brasileira de Ocupações). |
| **Grupos de cargo não definidos** | Classificados como **"Outros"** no dashboard. |
| **Funcionários em transição de cargo** | Contados no **cargo atual** (data de referência do dashboard). |

---

### **2.3. Movimentações de Pessoal (Admissões, Desligamentos, Transferências)**
#### **Definição**
Registro de **entrada, saída ou mudança interna** de funcionários em um período.

#### **Critérios de Inclusão**
- **Admissões**: Funcionários com data de admissão **dentro do período analisado**.
- **Desligamentos**: Funcionários com data de desligamento **dentro do período analisado**.
- **Transferências**: Mudanças de **cargo, centro de custo ou filial** registradas no período.

#### **Critérios de Exclusão**
- Movimentações **canceladas ou retroativas** (ex.: admissão registrada erradamente).
- Transferências **entre centros de custo do mesmo grupo** (não contam como movimentação relevante).
- Desligamentos por **falecimento** (tratados separadamente em alguns dashboards).

#### **Casos Especiais**
| Situação | Tratamento |
|----------|------------|
| **Readmissão no mesmo período** | Contada como **uma admissão e um desligamento**. |
| **Transferência para offshore** | Registrada como **desligamento no Brasil** e **admissão no offshore**. |
| **Licenças prolongadas** | Não contam como desligamento, mas podem ser marcadas como **"Inativo Temporário"**. |

---

### **2.4. Headcount Orçado vs. Realizado**
#### **Definição**
Comparação entre o **número planejado de funcionários** (orçamento) e o **número real** em um período.

#### **Critérios de Inclusão**
- **Headcount realizado**: Mesmas regras do **Headcount geral**.
- **Headcount orçado**: Dados extraídos de `hc_orcamento_historico.xlsx`, com validação de:
  - **Centro de custo** compatível com a estrutura atual.
  - **Período orçado** alinhado ao período analisado.

#### **Critérios de Exclusão**
- Orçamentos de **centros de custo desativados**.
- Dados orçamentários **sem data de referência clara**.
- Orçamentos **duplicados** (usado o registro mais recente).

#### **Casos Especiais**
| Situação | Tratamento |
|----------|------------|
| **Diferença > 10% entre orçado e realizado** | Gera alerta no dashboard para revisão. |
| **Orçamento não cadastrado para um centro de custo** | Assume **headcount zero** para comparação. |

---

### **2.5. Posições Abertas (Vagas)**
#### **Definição**
Vagas **autorizadas, mas não preenchidas** em um determinado período.

#### **Critérios de Inclusão**
- Vagas com **status "Aberta"** em `bz_excel_posicoes_f`.
- **Centro de custo ativo** e mapeado.
- **Data de abertura dentro do período analisado** (ou ainda não preenchida).

#### **Critérios de Exclusão**
- Vagas **canceladas ou preenchidas** antes do período.
- Vagas sem **centro de custo válido**.
- Vagas **duplicadas** (mesma posição em mais de um registro).

#### **Casos Especiais**
| Situação | Tratamento |
|----------|------------|
| **Vaga aberta há mais de 90 dias** | Classificada como **"Crítica"** no dashboard. |
| **Vaga com múltiplos candidatos** | Contada uma única vez, independentemente do número de candidatos. |

---

## **3. Condicionais e Classificações**
Os dados são segmentados conforme as seguintes regras:

### **3.1. Por Período**
- **Mês/ano**: Usa a **data de referência** do dashboard (ex.: "Headcount em 31/12/2023").
- **Histórico**: Dados de 2014 a 2018 usam a base manual (`hc_historica_f.xlsx`).
- **Comparativos**: Sempre usa **mesmo dia do mês** para evitar distorções (ex.: 31/01 vs. 28/02).

### **3.2. Por Faixa Etária**
| Classificação | Critério |
|---------------|----------|
| **Jovem** | Até 29 anos. |
| **Adulto** | 30 a 49 anos. |
| **Sênior** | 50 anos ou mais. |

### **3.3. Por Tempo de Casa**
| Classificação | Critério |
|---------------|----------|
| **Novato** | Até 1 ano. |
| **Intermediário** | 1 a 5 anos. |
| **Veterano** | Mais de 5 anos. |

### **3.4. Por Tipo de Contrato**
| Classificação | Critério |
|---------------|----------|
| **CLT** | Contrato padrão. |
| **Temporário** | Contrato por prazo determinado. |
| **Offshore** | Funcionários alocados no exterior. |

### **3.5. Por Status**
| Classificação | Critério |
|---------------|----------|
| **Ativo** | Funcionário em atividade. |
| **Licença** | Afastado por motivo médico, maternidade, etc. |
| **Inativo Temporário** | Licença não remunerada. |
| **Desligado** | Saída registrada. |

---

## **4. Campos e Flags de Apoio**
Campos usados para aplicar as regras de negócio:

| Campo | Origem | Descrição |
|-------|--------|-----------|
| **Status** | `bz_headcount_f` | Indica se o funcionário está ativo, licenciado ou desligado. |
| **Data de Admissão** | `bz_headcount_f` | Data de entrada na empresa. |
| **Data de Desligamento** | `bz_headcount_f` | Data de saída (nulo = ainda ativo). |
| **Centro de Custo** | `bz_externo_centro_custo_d` | Unidade organizacional do funcionário. |
| **Cargo** | `bz_excel_funcao_d` | Função exercida (vinculada ao CBO). |
| **Tipo de Contrato** | `bz_pessoa_d` | CLT, temporário, offshore, etc. |
| **Filial** | `bz_excel_filial_d` | Local de trabalho. |
| **Flag Offshore** | `bz_headcount_offshore_f` | Indica se o funcionário está alocado no exterior. |
| **Grupo de Cargo** | `bz_excel_funcao_d` | Classificação por carreira (ex.: Administrativo, Operacional). |
| **Tabela Salarial** | `bz_excel_salario_d` | Faixa salarial associada ao cargo. |

---

## **5. O que é Incluído e o que é Excluído no Dashboard**

### **5.1. Headcount**
| **Inclusão** | **Exclusão** |
|--------------|--------------|
| Funcionários CLT ativos. | Estagiários. |
| Contratos temporários com registro. | Terceirizados. |
| Funcionários em licença remunerada. | Centros de custo inativos. |
| Funcionários offshore (quando aplicável). | Dados duplicados. |
| Funcionários em férias. | Funcionários desligados antes do período. |

### **5.2. Movimentações**
| **Inclusão** | **Exclusão** |
|--------------|--------------|
| Admissões no período. | Movimentações canceladas. |
| Desligamentos no período. | Transferências internas sem mudança de área. |
| Transferências de cargo/centro de custo. | Desligamentos por falecimento. |

### **5.3. Posições Abertas**
| **Inclusão** | **Exclusão** |
|--------------|--------------|
| Vagas com status "Aberta". | Vagas canceladas. |
| Vagas com centro de custo ativo. | Vagas sem data de abertura. |
| Vagas não preenchidas. | Vagas duplicadas. |

---

## **6. Glossário**
| Termo | Definição |
|-------|-----------|
| **Headcount** | Contagem total de funcionários ativos em um período. |
| **CBO (Classificação Brasileira de Ocupações)** | Código oficial que classifica cargos no Brasil. |
| **Centro de Custo** | Unidade organizacional que agrega despesas e funcionários. |
| **Offshore** | Funcionários alocados em operações no exterior. |
| **Flag** | Indicador (sim/não) usado para classificar registros. |
| **CLT** | Contrato de trabalho regido pela Consolidação das Leis do Trabalho. |
| **Temporário** | Contrato por prazo determinado. |
| **Estagiário** | Vínculo não-CLT, regido por lei de estágio. |
| **Terceirizado** | Funcionário de empresa prestadora de serviços. |
| **Licença Remunerada** | Afastamento com pagamento (ex.: médica, maternidade). |
| **Licença Não Remunerada** | Afastamento sem pagamento. |
