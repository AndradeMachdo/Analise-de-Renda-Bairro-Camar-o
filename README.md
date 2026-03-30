[README.md](https://github.com/user-attachments/files/26338384/README.md)
# 📍 Locus · Método IAT — Índice de Aderência Territorial

> Metodologia proprietária da **Locus Inteligência de Mercado** para calcular o potencial de abertura de negócios em territórios específicos — bairro a bairro.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-piloto_público-brightgreen)
![Território](https://img.shields.io/badge/território-São_Gonçalo_RJ-00b4d8)

---

## O que é o IAT?

O **Índice de Aderência Territorial (IAT)** é um score de 0 a 100 que responde uma pergunta direta:

> *"Este bairro tem condições para sustentar este tipo de negócio?"*

Em vez de análises genéricas por cidade ou estado, o IAT trabalha na escala do **bairro** — onde a decisão de abrir um negócio de fato acontece. Um bairro de São Gonçalo pode ter IAT 77 para barbearia e IAT 42 para restaurante formal. A cidade inteira não diz isso.

---

## Como o Score é Calculado

O IAT é composto por **3 componentes**, cada um com peso igual (1/3):

```
IAT = (C1 + C2 + C3) / 3
```

### C1 · Potencial do Território
Avalia as condições estruturais do bairro — o que já existe independente do negócio.

| Subfator | O que mede |
|----------|-----------|
| Densidade populacional | Há pessoas suficientes para gerar demanda? |
| Renda estimada | A renda local suporta o ticket do negócio? |
| Infraestrutura de mobilidade | O bairro é acessível? Tem fluxo de passagem? |
| Infraestrutura básica | Saneamento, energia, coleta — ambiente mínimo de operação |

### C2 · Aderência do Consumidor
Avalia se o perfil de quem vive no bairro combina com o tipo de negócio.

| Subfator | O que mede |
|----------|-----------|
| Faixa etária predominante | O público-alvo do negócio existe neste bairro? |
| Comportamento digital | Há busca ativa por esse serviço na área? (Google Trends) |
| Frequência de consumo | O produto é comprado todo dia, toda semana, todo mês? |
| Compatibilidade de ticket | O preço do produto cabe na renda local? |

### C3 · Janela Competitiva
Avalia se há espaço no mercado — se a concorrência já saturou a demanda ou se a janela ainda está aberta.

| Subfator | O que mede |
|----------|-----------|
| Densidade de concorrentes | Quantos negócios do mesmo tipo já existem no bairro? |
| Qualidade da concorrência | Os existentes atendem bem ou há gap de qualidade? |
| Tendência do setor | O setor está crescendo ou em retração? |
| Barreira de entrada de redes | Há risco de rede nacional entrar e ocupar o espaço? |

---

## Tabela de Classificação

| IAT | Classificação | Veredito |
|-----|--------------|---------|
| 80–100 | 🟢 Território Ideal | Entrar com velocidade. Risco baixo, janela aberta. |
| 65–79 | 🟡 Território Favorável | Entrar com atenção ao fator de menor score. |
| 50–64 | 🟠 Território Neutro | Possível, mas exige diferenciação e mais análise. |
| 35–49 | 🔴 Território Desafiador | Alto risco. Só com vantagem competitiva clara. |
| 0–34 | ⛔ Território Inviável | Não recomendado. Redirecionar esforço. |

---

## Intervalo de Confiança

Todo score IAT vem acompanhado de um **±IC** que reflete a qualidade dos dados utilizados.

```
IAT Serviços (Barbearia) · Camarão:  77 ± 4   → [73, 81]  → Favorável em qualquer cenário
IAT Saúde & Bem-Estar   · Camarão:  58 ± 7   → [51, 65]  → Pode ser Neutro ou Favorável
```

Quanto maior o IC, menor a confiança — e maior a necessidade de aprofundamento antes de decisão.

---

## Fontes de Dados

O IAT é calculado em dois níveis de produto:

### Nível 1 · Diagnóstico de Território (este repositório)
Usa exclusivamente **dados secundários públicos**:
- IBGE Censo 2022 / PNAD Contínua — demografia e renda
- POF 2017–2018 — padrões de consumo por faixa de renda
- Google Trends — volume de busca por categoria + localidade
- Google Maps — densidade e qualidade percebida da concorrência
- Brasil.io — abertura de CNPJs por setor (jan/2024–mar/2026)
- Prefeitura de SG / EIV — infraestrutura urbana

### Nível 2 · Diagnóstico Aprofundado
Adiciona **dados primários**:
- Survey de 200–400 respondentes no bairro
- Visita de campo com Protocolo de Coleta (PLC) presencial
- Entrevistas qualitativas com comerciantes locais

---

## Resultado: Bairro Camarão · São Gonçalo (março/2026)

| Categoria | C1 | C2 | C3 | IAT | Classificação | Veredito |
|-----------|----|----|-----|-----|--------------|---------|
| Alimentação (marmita/lanchonete) | 73 | 74 | 65 | **71 ± 5** | 🟡 Favorável | ABRIR |
| Saúde & Bem-Estar | 68 | 60 | 44 | **58 ± 7** | 🟠 Neutro | APROFUNDAR |
| Serviços (barbearia masculina) | 73 | 82 | 79 | **77 ± 4** | 🟡 Favorável | ABRIR |

**Maior oportunidade identificada:** barbearia masculina de bairro, com agendamento por WhatsApp/app, ticket R$40–70, próxima ao fluxo da RJ-104.

---

## Estrutura do Repositório

```
locus-metodo-iat/
│
├── src/
│   └── iat_calculator.py       # Implementação do cálculo do IAT
│
├── data/
│   └── camarao_inputs.json     # Inputs do relatório piloto (Camarão)
│
├── outputs/
│   ├── 01_iat_componentes.png  # Gráfico de radar por componente
│   ├── 02_iat_comparativo.png  # Comparativo entre categorias
│   ├── 03_sensibilidade.png    # Análise de sensibilidade dos pesos
│   └── relatorio_camarao.csv   # Scores consolidados exportados
│
└── README.md
```

---

## Como Executar

```bash
pip install pandas numpy matplotlib
python src/iat_calculator.py
```

---

## Limitações Documentadas

| Limitação | Impacto | Mitigação |
|-----------|---------|-----------|
| POF 2017–18 como referência de consumo | Dados de gasto desatualizados (8 anos) | Google Trends + volume de avaliações Google Maps como proxy |
| Censo 2010 como base demográfica do bairro | Projeção 2022 estimada, não medida | Crescimento proporcional ao município (erro < 15%) |
| Sem pesquisa de campo presencial | Concorrência observada indiretamente | Diagnóstico Aprofundado inclui visita com PLC |
| Sem survey de consumidores | Preferências não medidas diretamente | Survey de 200–400 respondentes no nível 2 |

---

## Sobre a Locus

**Locus · inteligência do lugar** é uma empresa de inteligência de mercado local sediada em São Gonçalo, RJ. Vendemos clareza territorial — relatórios que dizem, com dados, se um bairro específico tem condições para sustentar um tipo de negócio.

> *"O lugar certo não é o melhor bairro da cidade. É o bairro certo para o seu negócio."*

📬 andradejoaomachado@Outlook.com · São Gonçalo, RJ · 2026
