# Documentação Técnica

**Arquivo:** `sv_headcount.qvs`  
**Última atualização:** 15/08/2025 09:46:34

# **Documentação do Script QVS – Processamento de Dados de Recursos Humanos**

---

## **1. Introdução**
Este documento explica, de forma clara e organizada, o funcionamento de um script escrito na linguagem **QlikView Script (QVS)**, utilizado para processar e transformar dados relacionados a **Recursos Humanos (RH)**. O objetivo principal do script é **coletar, limpar, enriquecer e preparar informações** sobre funcionários, demissões, posições, salários e outros dados relevantes para análise em ferramentas de *business intelligence* (como QlikView ou Qlik Sense).

O script segue uma estrutura lógica que:
1. **Configura o ambiente** (formatação de datas, moedas, etc.).
2. **Carrega dados brutos** de arquivos externos (como QVDs).
3. **Transforma e enriquece os dados** com regras de negócio.
4. **Armazena os dados processados** em novos arquivos para uso posterior.

---

## **2. Estrutura Geral do Script**
O script está dividido em **seções principais**, cada uma com um propósito específico:

| **Seção**                     | **Descrição**                                                                 |
|-------------------------------|-------------------------------------------------------------------------------|
| **Configurações Iniciais**    | Define formatações de números, datas, moedas e localização.                   |
| **Definição de Caminhos**     | Indica onde os arquivos de entrada e saída estão armazenados.                 |
| **Carregamento de Dados Brutos** | Lê arquivos QVD com informações de funcionários, posições, salários, etc.  |
| **Tabelas de Mapeamento**     | Cria tabelas auxiliares para classificar dados (ex: tipos de demissão).      |
| **Transformação de Dados**    | Aplica regras de negócio, limpa dados e prepara informações para análise.   |
| **Geração de Tabelas Finais** | Produz tabelas otimizadas para relatórios e *dashboards*.                     |
| **Armazenamento dos Resultados** | Salva os dados processados em novos arquivos QVD.                           |
| **Limpeza de Tabelas Temporárias** | Remove tabelas não mais necessárias para liberar memória.                |

---

## **3. Configurações Iniciais**
### **3.1. Formatação de Números, Datas e Moedas**
O script começa definindo como números, datas e valores monetários serão exibidos no sistema. Isso garante que os dados sejam apresentados de forma consistente e alinhada com o padrão brasileiro.

| **Configuração**               | **Valor Definido**       | **Exemplo de Saída**       |
|---------------------------------|--------------------------|----------------------------|
| Separador de milhares           | `.` (ponto)              | `1.000`                    |
| Separador decimal               | `,` (vírgula)            | `R$ 1.000,50`              |
| Formato de data                 | `DD.MM.AAAA`             | `31.12.2023`               |
| Formato de moeda                | `R$#.##0,00`             | `R$ 1.234,56`              |
| Primeiro dia da semana          | Domingo (`6`)            | Calendários começam no domingo. |

**Por que isso é importante?**
- Garante que relatórios e gráficos exibam valores corretamente.
- Evita erros de interpretação (ex: `1.000,50` vs `1,000.50`).

---

## **4. Definição de Caminhos para Arquivos**
O script utiliza **variáveis** para indicar onde os arquivos de entrada e saída estão localizados. Isso facilita a manutenção, pois basta alterar o caminho em um único lugar.

| **Variável**          | **Descrição**                                                                 | **Exemplo de Caminho**                                                                 |
|-----------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `bronze_layer`        | Local onde estão os dados brutos (não processados).                        | `lib://Pasta RH/HR Medallion/Bronze/`                                                   |
| `silver_layer`        | Local onde são salvos os dados processados e limpos.                       | `lib://Pasta RH/HR Medallion/Silver/`                                                   |
| `gold_layer`          | Local para dados finais, prontos para análise.                            | `lib://Pasta RH/HR Medallion/Gold/`                                                     |
| `manual_source`       | Dados manuais ou complementares.                                           | `lib://Pasta RH/Manual Source/`                                                         |

**Analogia:**
- **Bronze** = Matéria-prima (dados crus).
- **Silver** = Produto semiacabado (dados limpos).
- **Gold** = Produto final (dados prontos para análise).

---

## **5. Carregamento de Dados Brutos**
Nesta seção, o script **lê arquivos QVD** (formato otimizado do Qlik) que contêm informações sobre:
- **Funcionários ativos e demitidos** (`bz_headcount_f`).
- **Histórico de funcionários** (`bz_headcount_hist_f`).
- **Posições e cargos** (`bz_posicoes_f`).
- **Estrutura de centros de custo** (`bz_excel_estrutura_cc_d`).
- **Hierarquia organizacional** (`bz_hierarquia_d`).

**Exemplo de carregamento:**
```qlikview
bz_headcount_f:
Load *
FROM [$(bronze_layer)bz_headcount_f.QVD] (qvd)
where Date#([Dia do calendário], 'DD.MM.YYYY') >= Date#('01.01.2019', 'DD.MM.YYYY');
```
- **O que faz?**
  - Carrega todos os campos (`*`) do arquivo `bz_headcount_f.QVD`.
  - Filtra apenas registros a partir de **01/01/2019**.

**Por que filtrar por data?**
- Reduz o volume de dados processados, melhorando performance.
- Foca apenas em informações relevantes para análise.

---

## **6. Tabelas de Mapeamento**
São tabelas auxiliares que **classificam ou traduzem códigos** para nomes legíveis. Exemplos:

### **6.1. Mapeamento de Empresas (`coligada_d`)**
| **Código (CODCOLIGADA)** | **Nome (COLIGADA)**          |
|--------------------------|------------------------------|
| 1                        | Eldorado                     |
| 2                        | Florestal                    |
| 3                        | OffShore                     |

**Uso:**
- Permite substituir `CODCOLIGADA = 1` por `COLIGADA = "Eldorado"` em relatórios.

### **6.2. Classificação de Demissões (`CLASSIFICAÇÃO_MAP`)**
| **Tipo de Demissão** | **Classificação**      |
|----------------------|-------------------------|
| 2                    | Involuntário            |
| V                    | Voluntário              |

**Uso:**
- Agrupa demissões em categorias para análise de *turnover*.

### **6.3. Mapeamento de Eventos (`MAP_EVENTOS`)**
| **Código do Evento (CODEVENTO)** | **Tipo (TIPO)**          |
|----------------------------------|---------------------------|
| 2                               | Salário Base (SB)         |
| 5                               | Salário Família (SF)      |
| 25                              | Hora Extra Esporádica     |

**Uso:**
- Traduz códigos de eventos de folha de pagamento para nomes compreensíveis.

---
## **7. Transformação de Dados**
Esta é a **parte central do script**, onde os dados brutos são **limpos, enriquecidos e preparados** para análise. As principais transformações incluem:

### **7.1. Tratamento de Centros de Custo (`centro_de_custo`)**
- **O que faz?**
  - Carrega dados de centros de custo (`bz_externo_centro_custo_d`).
  - Classifica diretorias em grupos (ex: "Financeiro" → "Corporativo").
  - Remove registros inválidos (ex: centros de custo vazios ou com `#`).

**Exemplo de código:**
```qlikview
centro_de_custo:
Load
    [Centro Custo] as centro_de_custo,
    [Descrição] as centro_de_custo_nome,
    If(Match([Diretoria], 'Financeiro', 'RH'), 'Corporativo', [Diretoria]) as grupo_diretoria
Resident bz_externo_centro_custo_d
WHERE Len(Trim([Centro Custo])) > 0 AND [Centro Custo] <> '#';
```

### **7.2. Tratamento de Funções (`funcao`)**
- **O que faz?**
  - Padroniza códigos de funções (ex: `123` → `00123`).
  - Classifica funções como "Líder" ou "Não Líder".
  - Identifica funções operacionais vs. administrativas.

**Exemplo:**
```qlikview
funcao:
Load Distinct
    RIGHT('00000' & KEEPCHAR([Cargo], '0123456789'), 5) as funcao_cod,
    SubField([Cargo], ' - ', 2) as funcao_nome,
    IF([Carreira] = '1-Gestão', 'Líder', 'Não Líder') as lider_flag
Resident bz_excel_funcao_d;
```

### **7.3. Identificação de Funcionários com Curto Tempo de Empresa**
- **Problema:** Funcionários admitidos e demitidos no mesmo mês não aparecem corretamente nos relatórios.
- **Solução:** O script identifica esses casos e os marca com um flag (`short_tenure = 1`).

**Exemplo:**
```qlikview
bz_admitidos_demitidos_temp:
Load *
Resident bz_headcount_latest_f
WHERE
    Date(Date#([Data Demissão], 'DD.MM.YYYY')) < Date(MonthEnd(Date#([Data Admissão], 'DD.MM.YYYY')))
    AND [Tipo de Demissão] <> 5  // Exclui transferências
    AND NOT Match([Tipo de Admissão], 'T');  // Exclui temporários
```

### **7.4. Cálculo de Indicadores de RH**
O script calcula métricas como:
- **Tempo na empresa** (em dias).
- **Idade do funcionário** (a partir da data de nascimento).
- **Posição salarial** (ex: "Entre 90% e 100% da faixa salarial").
- **Flags de novos contratados** (`new_hire_flag`).

**Exemplo de cálculo de tempo na empresa:**
```qlikview
(Date#([Dia do calendário], 'DD.MM.YYYY') - Date#([Data Admissão], 'DD.MM.YYYY')) as tempo_empresa_dias
```

---
## **8. Geração de Tabelas Finais**
Após as transformações, o script **consolida os dados em tabelas otimizadas** para análise. As principais tabelas geradas são:

| **Tabela**               | **Descrição**                                                                 | **Arquivo de Saída**                          |
|--------------------------|-----------------------------------------------------------------------------|-----------------------------------------------|
| `sv_headcount_f`         | Dados detalhados de todos os funcionários (ativos e inativos).             | `sv_headcount_f.QVD`                          |
| `sv_termination_f`       | Informações sobre demissões (motivos, classificações, etc.).               | `sv_termination_f.QVD`                        |
| `sv_posicoes_f`           | Posições abertas, tempo de recrutamento e status.                          | `sv_posicoes_f.QVD`                           |
| `sv_centro_de_custo_d`   | Centros de custo classificados por diretoria e área.                       | `sv_centro_de_custo_d.QVD`                    |

**Exemplo de armazenamento:**
```qlikview
STORE sv_headcount_f INTO [$(silver_layer)sv_headcount_f.QVD] (qvd);
```

---
## **9. Limpeza de Tabelas Temporárias**
Ao final, o script **remove tabelas que não são mais necessárias** para liberar memória e evitar confusão.

**Exemplo:**
```qlikview
Drop Table bz_headcount_f, bz_headcount_latest_f, centro_de_custo;
```

---
## **10. Fluxo Completo do Script**
Para visualizar o processo de forma simplificada:

1. **Entrada:**
   - Arquivos QVD brutos (`bronze_layer`).
2. **Processamento:**
   - Aplicação de regras de negócio.
   - Cálculo de indicadores.
   - Junção de tabelas.
3. **Saída:**
   - Arquivos QVD processados (`silver_layer`).
4. **Uso Final:**
   - Os dados são utilizados em *dashboards* de RH para análise de:
     - *Turnover* (rotatividade).
     - Distribuição de funcionários por área.
     - Tempo médio de recrutamento.
     - Posicionamento salarial.

---
## **11. Exemplos Práticos**
### **11.1. Cálculo de Turnover**
**Problema:** Identificar demissões voluntárias vs. involuntárias.
**Solução:** O script usa a tabela `CLASSIFICAÇÃO_MAP` para classificar cada demissão.

| **Tipo de Demissão** | **Classificação** |
|----------------------|-------------------|
| 2                    | Involuntário      |
| V                    | Voluntário        |

**Resultado:**
- Relatórios podem mostrar:
  - `% de demissões voluntárias = 30%`.
  - `% de demissões involuntárias = 70%`.

### **11.2. Identificação de Gestores**
**Problema:** Saber quem é o gestor direto de cada funcionário.
**Solução:** O script percorre a hierarquia (Nível 1 a Nível 6) e identifica o primeiro gestor válido.

**Exemplo de código:**
```qlikview
IF(
    [hierarquia_cod_n1] <> [chapa] AND [hierarquia_cod_n1] <> '#',
    [hierarquia_nome_n1],  // Se Nível 1 é válido, usa este nome.
    IF(
        [hierarquia_cod_n2] <> [chapa] AND [hierarquia_cod_n2] <> '#',
        [hierarquia_nome_n2],  // Senão, verifica Nível 2.
        ...  // E assim por diante.
    )
) AS [gestor_direto_nome]
```

---
## **12. Conclusão**
Este script é uma **ferramenta poderosa para transformar dados de RH em informações úteis**, permitindo que a empresa:
- **Monitore a rotatividade de funcionários** (*turnover*).
- **Analise a distribuição de cargos e salários**.
- **Acompanhe o tempo de recrutamento e admissão**.
- **Identifique padrões em demissões** (voluntárias vs. involuntárias).

**Benefícios:**
- **Automatização:** Elimina trabalho manual de limpeza de dados.
- **Consistência:** Garante que todos os relatórios usem as mesmas regras.
- **Flexibilidade:** Permite ajustes nas regras de negócio sem alterar a origem dos dados.

---
**Nota Final:**
Este documento explicou o script de forma **simplificada e acessível**, sem entrar em detalhes técnicos profundos. O objetivo é que qualquer pessoa, mesmo sem conhecimento em programação, possa entender **o que o script faz, por que faz e como contribui para a análise de dados de RH**.
