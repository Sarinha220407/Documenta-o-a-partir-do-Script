# Documentação Técnica

**Arquivo:** `headcount.qvs`  
**Última atualização:** 15/08/2025 13:51:19

# **Documentação de Regras de Negócio – Dashboard de Recursos Humanos (RH)**

---

## **1. Visão Geral**
### **Objetivo do Documento**
Este documento explica as regras de negócio aplicadas aos indicadores do **Dashboard de RH**, incluindo:
- **Critérios de inclusão e exclusão** para cada métrica.
- **Condicionais** que definem como os dados são classificados.
- **Casos especiais** e exceções tratadas no cálculo.

### **Como Identificar o Que Deve Ser Contado**
Cada métrica segue regras específicas para determinar:
- **O que é incluído** (ex.: funcionários ativos, demissões voluntárias).
- **O que é excluído** (ex.: estagiários, aprendizes, transferências sem ônus).
- **Segmentações** (ex.: por idade, tempo de empresa, tipo de demissão).

---
## **2. Regras de Negócio por Indicador/Métrica**

---

### **2.1 Headcount (Número de Funcionários)**
#### **Definição**
Quantidade total de funcionários **ativos** na empresa em um determinado período, considerando critérios de elegibilidade.

#### **Critérios de Inclusão**
São contados como **Headcount** os funcionários que atendem **todos** os seguintes requisitos:
- **Situação ativa** no sistema (código `A`, `E`, `F`, `V`).
  - `A`: Ativo.
  - `E`: Licença maternidade.
  - `F`: Férias.
  - `V`: Aviso prévio.
- **Tipo de funcionário** elegível:
  - `N`: Normal.
  - `D`: Diretor.
  - `M`: Misto.
  - `R`: Rural.
  - Outros tipos **exceto** `U` (Outros), `S` (Pensionista), `T` (Estagiário), `C` (Conselheiro).
- **Centro de custo válido** (código numérico maior que `99`).
- **Data de admissão** anterior ou igual à data atual (não conta admissões futuras).
- **Não são conselheiros, fiscais ou cargos específicos excluídos** (ex.: `Conselheiro Adm`, `703`, `704`).

#### **Critérios de Exclusão**
Não são contados no **Headcount**:
- Funcionários com **situação inativa** (ex.: `D` = Demitido, `Z` = Admissão futura).
- **Estagiários** (`Tipo Funcionário = T`).
- **Aprendizes** (`Tipo Funcionário = Z`).
- **Pensionistas** (`Tipo Funcionário = S`).
- **Transferências sem ônus** (código de demissão `5`).
- **Funcionários com centro de custo inválido** (ex.: `#`, códigos ≤ `99`).
- **Matrículas apagadas** (situação `9`).
- **Funcionários offshore** (trados separadamente).
- **Listagem específica de chapas excluídas** (ex.: `999907338`, `50003102` – ver lista completa no script).

#### **Casos Especiais**
- **Admitidos e demitidos no mesmo mês**:
  - São contados como **Headcount** apenas se a demissão não for por transferência (`Tipo de Demissão ≠ 5`).
  - Recebem o status `"C/Dem no mês"` para identificação.
- **Funcionários readmitidos**:
  - São contados normalmente, mas recebem a flag `"Sim"` no campo `readimitido`.
- **Funcionários com menos de 1 ano de empresa**:
  - Recebem a classificação `"Novo Contratado"` e a flag `new_hire_flag = TRUE`.
- **Funcionários afastados por atestado**:
  - São contados no **Headcount** se a situação for `A`, `E`, `F` ou `V`.

---

### **2.2 Turnover (Rotatividade)**
#### **Definição**
Porcentagem de funcionários que deixaram a empresa **voluntária ou involuntariamente** em um período, em relação ao **Headcount médio**.

#### **Critérios de Inclusão**
São contadas como **Turnover** as demissões que atendem:
- **Situação = Demitido** (`D`).
- **Tipo de demissão elegível** (exclui transferências, falecimentos, aposentadorias):
  - **Voluntárias**: Códigos `4`, `V` (ex.: pedido do funcionário).
  - **Involuntárias**: Códigos `1`, `2`, `8`, `N`, `T` (ex.: demissão por justa causa, performance).
- **Tipo de funcionário elegível** (exclui estagiários, aprendizes, conselheiros):
  - Não pode ser `T`, `S`, `C`, `U`, `Z`.

#### **Critérios de Exclusão**
Não são contadas como **Turnover**:
- **Transferências sem ônus** (`Tipo de Demissão = 5`).
- **Falecimentos** (`8`).
- **Aposentadorias** (códigos `A`, `D`, `E`, `F`, `I`, `J`, `P`, `R`, `S`, `U`).
- **Estagiários e aprendizes** (`Tipo Funcionário = T ou Z`).
- **Pensionistas e conselheiros** (`Tipo Funcionário = S ou C`).

#### **Casos Especiais**
- **Demissões no mesmo mês da admissão**:
  - Não são contadas como **Turnover** se a demissão for por transferência (`5`).
- **Classificação da demissão**:
  - **Voluntária**: Quando o funcionário pede demissão.
  - **Involuntária**: Quando a empresa demite (ex.: performance, redução de quadro).

---

### **2.3 Vagas Abertas (Posições em Aberto)**
#### **Definição**
Quantidade de **posições disponíveis para contratação**, incluindo vagas em andamento ou em processo de admissão.

#### **Critérios de Inclusão**
São contadas como **Vagas Abertas**:
- Posições com **status** `Em Andamento` ou `Em Admissão`.
- **Classificação** diferente de `Substituição`.
- **Não são vagas para aprendizes ou estagiários** (exclui termos como `APRENDIZ`, `ESTAG`).
- **Responsável pela vaga definido** (exclui `"NAO DEFINIDO"`).

#### **Critérios de Exclusão**
Não são contadas como **Vagas Abertas**:
- Posições **arquivadas ou canceladas**.
- Vagas para **aprendizes ou estagiários**.
- Vagas **sem responsável definido**.

#### **Casos Especiais**
- **Vagas de substituição**:
  - São marcadas com a flag `rp_classificacao = "Substituição"` e **não são contadas** no total de vagas abertas padrão.

---

### **2.4 Taxa de Ocupação**
#### **Definição**
Porcentagem de **posições preenchidas** em relação ao **total de posições previstas** (orçamento).

#### **Critérios de Inclusão**
- **Headcount atual** (funcionários ativos).
- **Orçamento de posições** (quantidade planejada por centro de custo/função).

#### **Critérios de Exclusão**
- Posições **não orçadas** (sem registro no histórico de orçamento).
- **Vagas em aberto** não preenchidas.

#### **Cálculo**
```
Taxa de Ocupação = (Headcount Atual / Orçamento de Posições) × 100
```

---

### **2.5 Admissões (New Hires)**
#### **Definição**
Funcionários **contratados recentemente** (até 1 ano de empresa).

#### **Critérios de Inclusão**
- **Tempo de empresa < 1 ano** (365 dias).
- **Situação ativa** (`A`, `E`, `F`, `V`).
- **Não são estagiários ou aprendizes**.

#### **Critérios de Exclusão**
- Funcionários **readmitidos** (contam como admissão apenas na primeira contratação).
- **Transferências internas** (não contam como nova admissão).

#### **Classificações**
| Classificação          | Critério                                  |
|------------------------|-------------------------------------------|
| Novo Contratado        | < 1 ano de empresa.                       |
| Admitido no Mês        | Admissão no mês de referência.            |
| Admitido até 3 Meses   | ≤ 90 dias de empresa.                     |

---

### **2.6 Demissões (Terminations)**
#### **Definição**
Funcionários que **deixaram a empresa**, classificados por tipo (voluntária/involuntária).

#### **Critérios de Inclusão**
- **Situação = Demitido** (`D`).
- **Tipo de demissão válido** (exclui transferências, falecimentos, aposentadorias).
- **Data de demissão** dentro do período analisado.

#### **Critérios de Exclusão**
- **Transferências sem ônus** (`Tipo de Demissão = 5`).
- **Falecimentos** (`8`).
- **Aposentadorias** (códigos `A`, `D`, `E`, etc.).
- **Estagiários e aprendizes**.

#### **Classificação de Demissões**
| Tipo               | Códigos de Demissão                     |
|--------------------|-----------------------------------------|
| Voluntária         | `4`, `V`                                |
| Involuntária       | `1`, `2`, `8`, `N`, `T`                |

---

### **2.7 Readmissões**
#### **Definição**
Funcionários que **retornaram à empresa** após demissão anterior.

#### **Critérios de Inclusão**
- **Quantidade de admissões > 1** para a mesma pessoa.
- **Não são estagiários ou aprendizes**.

#### **Critérios de Exclusão**
- **Primeira admissão** (não conta como readmissão).
- **Transferências internas** (não contam como readmissão).

---

### **2.8 Faixas Salariais (Positioning FS)**
#### **Definição**
Classificação do salário do funcionário em relação à **faixa salarial de referência** para seu cargo.

#### **Critérios de Inclusão**
- **Salário base** do funcionário.
- **Tabela salarial** associada ao cargo (por GS, coligada, filial).

#### **Classificação**
| Faixa               | Salário em Relação à Referência |
|---------------------|----------------------------------|
| Menor que 80%       | < 80% do salário de referência.  |
| Entre 80% e 90%     | ≥ 80% e < 90%.                   |
| Entre 90% e 100%    | ≥ 90% e < 100%.                  |
| Entre 100% e 110%   | ≥ 100% e ≤ 110%.                 |
| Acima de 120%        | > 120%.                          |

---

## **3. Condicionais e Classificações**
Os dados são segmentados pelos seguintes critérios:

### **3.1 Por Período**
- **Mês de referência**: Dados agregados por mês calendário.
- **Data de admissão/demissão**: Usada para calcular tempo de empresa.
- **Idade**: Calculada a partir da data de nascimento.

### **3.2 Por Faixa de Valor**
| Classificação       | Critério                                  |
|---------------------|-------------------------------------------|
| Até 30 anos         | Idade ≤ 30.                              |
| De 31 a 50 anos     | Idade > 30 e ≤ 50.                       |
| Acima de 50 anos    | Idade > 50.                              |
| Novo Contratado     | Tempo de empresa < 1 ano.                |
| Ticket Médio < R$100| Salário mensal < R$100 (exemplo genérico).|

### **3.3 Por Categoria**
- **Tipo de funcionário**: Normal, Diretor, Estagiário, etc.
- **Situação**: Ativo, Férias, Licença Maternidade, etc.
- **Grupo de cargo**: Operacional, Técnico, Líder, Não Líder.
- **Diretoria/Área**: Industrial, Florestal, Corporativo, etc.

### **3.4 Por Status**
- **Ativo/Inativo**: Baseado na situação (`A` = Ativo, `D` = Demitido).
- **Turnover**: Voluntário ou Involuntário.
- **Vagas**: Em andamento, preenchidas, arquivadas.

### **3.5 Por Região**
- **Filial**: Unidade onde o funcionário está alocado.
- **Centro de custo**: Associado à diretoria/área.

---

## **4. Campos e Flags de Apoio**
Campos utilizados para aplicar as regras de negócio:

| Campo                     | Descrição                                                                 |
|---------------------------|---------------------------------------------------------------------------|
| `situacao_cod`            | Código da situação do funcionário (ex.: `A` = Ativo, `D` = Demitido).   |
| `tipo_funcionario_cod`    | Tipo de funcionário (ex.: `N` = Normal, `T` = Estagiário).               |
| `coligada_cod`            | Código da coligada (ex.: `1` = Eldorado, `2` = Florestal).               |
| `centro_de_custo`         | Centro de custo associado ao funcionário.                               |
| `funcao_cod`              | Código da função/cargo.                                                  |
| `data_admissao`           | Data de admissão do funcionário.                                         |
| `demissao_tipo_cod`       | Tipo de demissão (ex.: `1` = Involuntária, `4` = Voluntária).            |
| `turnover_flag`           | `TRUE` se a demissão deve ser contada como Turnover.                     |
| `new_hire_flag`           | `TRUE` se o funcionário tem menos de 1 ano de empresa.                   |
| `readimitido`             | `Sim` se o funcionário foi readmitido.                                  |
| `headcount_flag_new`      | `TRUE` se o funcionário deve ser contado no Headcount.                   |
| `gestor_direto_nome`      | Nome do gestor imediato do funcionário.                                  |
| `posic_fs`                | Posicionamento salarial (ex.: `0.95` = 95% da referência).               |
| `grupo_diretoria`        | Grupo da diretoria (ex.: `Industrial`, `Corporativo`).                   |

---

## **5. O que é Incluído e o que é Excluído no Dashboard**

### **5.1 Headcount**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Funcionários ativos (`A`, `E`, `F`, `V`). | Estagiários (`Tipo Funcionário = T`). |
| Tempo de empresa ≥ 0 dias.            | Aprendizes (`Tipo Funcionário = Z`).  |
| Centro de custo válido (> 99).        | Transferências sem ônus (`Tipo Demissão = 5`). |
| Tipo de funcionário elegível (`N`, `D`, `M`, etc.). | Funcionários offshore (trados separadamente). |
|                                       | Matrículas apagadas (`Situação = 9`). |
|                                       | Conselheiros, fiscais, cargos específicos (`703`, `704`). |

### **5.2 Turnover**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Demissões voluntárias (`4`, `V`).     | Transferências sem ônus (`5`).       |
| Demissões involuntárias (`1`, `2`, `N`). | Falecimentos (`8`).                  |
| Funcionários com ≥ 1 dia de empresa.  | Aposentadorias (`A`, `D`, `E`, etc.). |
|                                       | Estagiários e aprendizes (`T`, `Z`). |
|                                       | Conselheiros (`C`).                  |

### **5.3 Vagas Abertas**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Status `Em Andamento` ou `Em Admissão`. | Vagas para aprendizes/estagiários.    |
| Responsável pela vaga definido.      | Vagas arquivadas/canceladas.          |
| Não é substituição.                   |                                       |

### **5.4 Admissões (New Hires)**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Tempo de empresa < 1 ano.            | Readmissões (contam apenas na 1ª admissão). |
| Situação ativa (`A`, `E`, `F`, `V`).  | Transferências internas.             |
|                                       | Estagiários/aprendizes.              |

### **5.5 Demissões (Terminations)**
| **Inclusão**                          | **Exclusão**                          |
|---------------------------------------|---------------------------------------|
| Situação `Demitido` (`D`).            | Transferências sem ônus (`5`).       |
| Tipo de demissão elegível.            | Falecimentos (`8`).                  |
|                                       | Aposentadorias (`A`, `D`, etc.).      |
|                                       | Estagiários/aprendizes.              |

---

## **6. Glossário**
| Termo                  | Definição                                                                 |
|------------------------|---------------------------------------------------------------------------|
| **Headcount**          | Número total de funcionários ativos em um período.                       |
| **Turnover**           | Rotatividade de funcionários (demissões voluntárias/involuntárias).      |
| **New Hire**           | Funcionário com menos de 1 ano de empresa.                               |
| **Readmissão**         | Funcionário que retornou após demissão anterior.                         |
| **Coligada**           | Empresa do grupo (ex.: Eldorado, Florestal, Offshore).                    |
| **Centro de Custo**    | Unidade organizacional associada a despesas e receitas.                 |
| **GS**                 | Grau Salarial (nível hierárquico do cargo).                              |
| **PCD**                | Pessoa com Deficiência.                                                  |
| **CBO**                | Classificação Brasileira de Ocupações (código do cargo).                 |
| **Offshore**           | Funcionários alocados em unidades no exterior.                           |
| **RP (Requisition)**   | Posição/vaga aberta para contratação.                                    |
| **FS (Positioning)**   | Posicionamento salarial em relação à faixa de referência.                |
| **Short Tenure**       | Funcionário admitido e demitido no mesmo mês.                            |
