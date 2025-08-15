# Documentação Técnica

**Arquivo:** `People Analytics Model.qvs`  
**Última atualização:** 15/08/2025 11:56:24

# **Documentação do Script QVS – Estrutura de Dados para Análise de Recursos Humanos e Operações**

Este documento explica, de forma clara e organizada, o funcionamento de um script utilizado para preparar e relacionar dados em um sistema de análise de informações. O objetivo principal é integrar dados de **Recursos Humanos (RH)** e **operacionais** (como produção, vendas e custos) para que possam ser visualizados e analisados de maneira consistente.

O script não altera os dados originais, mas os organiza em uma estrutura que facilita a criação de relatórios, painéis e tomadas de decisão baseadas em informações confiáveis.

---

## **1. Configurações Iniciais**
Antes de carregar os dados, o script define padrões de formatação para garantir que números, datas, moedas e textos sejam exibidos de maneira uniforme e adequada ao português do Brasil.

### **1.1. Formatação de Números e Moedas**
- **Separador de milhar:** `.` (ponto) → Exemplo: `1.000` (mil).
- **Separador decimal:** `,` (vírgula) → Exemplo: `R$ 1.000,50`.
- **Formato de moeda:** `R$` (Real brasileiro), com duas casas decimais e sinal negativo para valores abaixo de zero.
  - Exemplo: `R$ 1.234,56` (positivo) ou `-R$ 1.234,56` (negativo).

### **1.2. Formatação de Data e Hora**
- **Data:** `DD.MM.AAAA` → Exemplo: `15.05.2024` (15 de maio de 2024).
- **Hora:** `hh:mm:ss` → Exemplo: `14:30:00`.
- **Data + Hora:** `DD.MM.AAAA hh:mm:ss` → Exemplo: `15.05.2024 14:30:00`.

### **1.3. Configurações de Calendário**
- **Primeiro dia da semana:** Domingo (definido como `6`).
- **Primeiro mês do ano:** Janeiro (definido como `1`).
- **Idioma:** Português do Brasil (`pt-BR`), para nomes de meses e dias da semana.
  - Exemplo: `janeiro`, `fevereiro`, `segunda-feira`, `terça-feira`, etc.

### **1.4. Caminhos dos Arquivos (Pastas de Dados)**
O script define onde os dados estão armazenados, organizados em **camadas** (como pastas em um computador):
- **Bronze:** Dados brutos (originais, sem tratamento).
- **Silver:** Dados limpos e padronizados.
- **Gold:** Dados prontos para análise (os utilizados neste script).
- **Manual Source:** Dados inseridos manualmente (como planilhas).
- **Fontes Externas:** Dados de fora da empresa (como pesquisas ou bases públicas).

---
## **2. Carregamento dos Dados**
O script carrega dois tipos de informações:
1. **Fatos (Tabelas de Eventos):** Registros de ocorrências, como admissões, demissões, produção, vendas, etc.
2. **Dimensões (Tabelas de Referência):** Informações descritivas, como nomes de funcionários, cargos, centros de custo, etc.

### **2.1. Tabelas de Fatos (O Que Aconteceu?)**
São carregadas as seguintes tabelas com dados operacionais e de RH:

| **Tabela**                     | **Descrição**                                                                 | **Exemplo de Uso**                          |
|--------------------------------|-------------------------------------------------------------------------------|---------------------------------------------|
| **gd_headcount_f**             | Quantidade de funcionários ativos em um determinado dia.                     | "Em janeiro de 2024, havia 500 funcionários na fábrica X." |
| **gd_termination_f**           | Registros de demissões (quem saiu, quando e por quê).                        | "10 funcionários pediram demissão em março." |
| **gd_excel_orcamento_historico_f** | Orçamento planejado de funcionários (metas de contratação).              | "O plano era ter 550 funcionários em 2024." |
| **gd_posicoes_f**              | Posições (vagas) disponíveis na empresa, mesmo que não estejam ocupadas.      | "Existem 20 vagas abertas para o cargo Y."  |
| **gd_eventos_f**               | Eventos relacionados a funcionários (treinamentos, promoções, etc.).         | "50 funcionários fizeram treinamento em segurança em abril." |
| **gd_custo_origem_opex_f**     | Custos operacionais (despesas da empresa, como salários, energia, etc.).     | "O custo com salários em fevereiro foi R$ 200.000,00." |
| **gd_producao_celulose_f**     | Produção de celulose (quantidade produzida por dia/mês).                     | "Em janeiro, foram produzidas 1.000 toneladas." |
| **gd_vendas_celulose_f**       | Vendas de celulose (quantidade vendida e faturamento).                        | "Vendemos 800 toneladas em fevereiro."      |
| **gd_receita_liquida_f**       | Receita líquida da empresa (faturamento após descontos).                      | "A receita em março foi R$ 5.000.000,00."     |

#### **Como os Dados São Identificados?**
Cada tabela de fatos recebe um **`link_key`**, um código único gerado automaticamente que serve como uma "etiqueta" para relacionar as informações. Esse código é criado a partir de dados como:
- Data (`date_key`),
- Funcionário (`pessoa`),
- Cargo (`funcao_sk`),
- Centro de custo (`centro_de_custo_sk`), entre outros.

**Exemplo:**
Se um funcionário foi admitido em `01.01.2024` no cargo `Analista` no centro de custo `Fábrica A`, o sistema gera um `link_key` único para esse registro. Isso permite vincular esse evento a outras informações, como seu salário ou treinamentos.

---

### **2.2. Tabelas de Dimensões (Quem? O Quê? Onde?)**
São informações descritivas que ajudam a entender **quem são os funcionários**, **quais são os cargos**, **onde trabalham**, etc.

| **Tabela**                 | **Descrição**                                                                 | **Exemplo**                                |
|----------------------------|-------------------------------------------------------------------------------|--------------------------------------------|
| **gd_calendario_d**        | Datas e informações de calendário (feriados, dias úteis, etc.).             | "01.01.2024 foi feriado (Ano Novo)."       |
| **gd_hierarquia_d**        | Estrutura hierárquica da empresa (gerentes, diretores, etc.).               | "João é gerente da área de Produção."      |
| **gd_funcao_d**            | Cargos existentes na empresa (Analista, Operador, etc.).                     | "Cargo: Operador de Máquinas."             |
| **gd_eldorado_entity_d**   | Unidades da empresa (fábricas, escritórios, filiais).                        | "Fábrica de Três Lagoas - MS."              |
| **gd_employee_d**          | Dados dos funcionários (nome, matrícula, etc.).                              | "Maria Silva, Matrícula 12345."            |
| **gd_situacao_d**          | Situação do funcionário (ativo, afastado, etc.).                              | "Situação: Ativo."                         |
| **gd_tipo_funcionario_d**  | Tipo de contratação (CLT, temporário, estagiário, etc.).                      | "Tipo: CLT."                               |
| **gd_centro_de_custo_d**   | Áreas ou departamentos que geram custos (Produção, RH, etc.).                 | "Centro de Custo: Manutenção."             |
| **gd_conta_contabil_d**    | Contas contábeis (salários, energia, matérias-primas, etc.).                  | "Conta: Salários e Encargos."              |
| **gd_evento_d**            | Tipos de eventos (treinamento, promoção, advertência, etc.).                   | "Evento: Treinamento de Segurança."        |

---
## **3. Relacionamento dos Dados (Tabela "Link")**
Após carregar todas as tabelas, o script cria uma **tabela central chamada `Link`**, que funciona como um "índice" para conectar todas as informações.

### **Como Funciona?**
1. **Cada tabela de fatos contribui com seus registros** para a tabela `Link`, mas apenas com os campos que são relevantes.
   - Exemplo: A tabela de **demissões (`gd_termination_f`)** não tem informações sobre produção, então esses campos ficam vazios (`''`).
2. **O `link_key` é a chave que une tudo**:
   - Se um registro de **produção** e um registro de **custos** têm o mesmo `link_key`, significa que estão relacionados (por exemplo, custos da produção daquele dia).
3. **Campos não utilizados são removidos** ao final para otimizar o espaço.

### **Exemplo Prático:**
| **link_key** (código único) | **date_key** (data) | **pessoa** (funcionário) | **funcao_sk** (cargo) | **centro_de_custo_sk** (área) | **conta_contabil_sk** (despesa) |
|----------------------------|--------------------|--------------------------|-----------------------|--------------------------------|----------------------------------|
| ABC123                      | 01.01.2024         | João Silva              | Operador              | Produção                      | Salários                        |
| DEF456                      | 01.01.2024         | -                        | -                     | Produção                      | Energia Elétrica                |

- **Interpretação:**
  - No dia **01.01.2024**, o funcionário **João Silva** (Operador) gerou um custo de **salário** na área de **Produção**.
  - No mesmo dia, houve um gasto com **energia elétrica** na **Produção**, mas não está vinculado a um funcionário específico.

---
## **4. Limpeza Final**
Ao final, o script **remove campos duplicados ou desnecessários** das tabelas originais para:
- Evitar confusão (por exemplo, não precisamos do nome do funcionário em todas as tabelas, apenas na tabela de dimensão).
- Otimizar o desempenho (menos dados repetidos = sistema mais rápido).

---
## **5. Resumo: Para Que Serve Esse Script?**
Este script **prepara os dados** para que possam ser usados em:
- **Relatórios de RH:** Quantidade de funcionários, rotatividade (quem entra/sai), custos com pessoal.
- **Análise de produção:** Relação entre funcionários, produção e vendas.
- **Controle de custos:** Quanto se gasta em cada área (salários, energia, matérias-primas).
- **Tomada de decisão:** Identificar padrões, como:
  - "Quando aumentamos a produção, os custos com horas extras sobem?"
  - "Quais áreas têm maior rotatividade de funcionários?"

### **Analogia Simples:**
Imagine que você tem:
- **Uma lista de compras do mercado** (fatos: o que foi comprado, quando e por quanto).
- **Uma lista de produtos** (dimensões: o que é "arroz", "feijão", etc.).
- **Uma lista de lojas** (dimensões: onde você comprou).

Esse script **junta tudo em uma planilha única**, onde você pode ver:
- "Em janeiro, comprei 2kg de arroz na Loja A por R$ 10,00."
- "O feijão ficou 20% mais caro na Loja B em fevereiro."

Assim, você consegue **analisar seus gastos** de forma organizada.

---
## **6. Fluxo Simplificado do Script**

1. **Configurações:** Define como números, datas e moedas serão exibidos.
2. **Localiza os dados:** Indica onde estão os arquivos (pastas Bronze, Silver, Gold, etc.).
3. **Carrega tabelas de fatos:** Dados de eventos (admissões, produção, vendas, etc.).
   - Cada tabela recebe um `link_key` para relacionamento.
4. **Carrega tabelas de dimensões:** Informações descritivas (funcionários, cargos, centros de custo, etc.).
5. **Cria a tabela `Link`:** Une todos os dados em um só lugar, usando o `link_key`.
6. **Remove dados repetidos:** Otimiza o espaço.
7. **Finaliza:** O script está pronto para ser usado em relatórios ou painéis.

---
## **7. Exemplos de Perguntas que Podem Ser Respondidas com Esses Dados**
| **Pergunta**                                      | **Tabelas Utilizadas**                          | **Como o `link_key` Ajuda?**                     |
|---------------------------------------------------|------------------------------------------------|-----------------------------------------------|
| Quantos funcionários foram admitidos em 2024?     | `gd_headcount_f` + `gd_employee_d`             | Filtra por data e conta os registros únicos.   |
| Qual o custo médio por funcionário na área X?     | `gd_custo_origem_opex_f` + `gd_centro_de_custo_d` | Relaciona custos com o centro de custo.       |
| A produção aumentou depois de um treinamento?    | `gd_producao_celulose_f` + `gd_eventos_f`      | Verifica se há correlação entre eventos e produção. |
| Quais cargos têm maior rotatividade?              | `gd_termination_f` + `gd_funcao_d`             | Agrupa demissões por cargo.                   |

---
## **8. Considerações Finais**
- **Objetivo:** Organizar dados de forma que possam ser **analisados juntos**, mesmo vindos de fontes diferentes.
- **Benefício:** Permite criar **relatórios confiáveis** e **tomar decisões baseadas em dados**.
- **Não altera os dados originais:** Apenas os prepara para uso em ferramentas de análise (como o Qlik Sense).

Este script é como um **"organizador de informações"**, garantindo que tudo esteja no lugar certo para que gestores e analistas possam entender o que acontece na empresa.
