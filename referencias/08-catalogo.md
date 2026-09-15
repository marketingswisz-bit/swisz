# Catálogo real da Swisz

_Levantado em 15/09/2026 direto de swisz.com.br (187 fichas de produto, dados
estruturados da loja). Dado bruto completo em `referencias/catalogo-swisz.json`._

Este arquivo existe para o roteirista **nunca inventar** nome de peça, preço,
tecido ou composição. Antes de citar um produto, confira aqui ou no JSON.

## Como consultar o JSON

Cada item tem: `rank_vendas` (posição na vitrine ordenada por mais vendidos),
`nome`, `preco`, `sku`, `categorias`, `tecido`, `composicao`, `tamanhos`,
`estoque`, `descricao` e `url`.

```bash
# peças de linho
grep -i linho referencias/catalogo-swisz.json
# os 20 mais vendidos
python3 -c "import json;[print(x['rank_vendas'],x['nome'],x['preco'],x['tecido']) for x in json.load(open('referencias/catalogo-swisz.json'))[:20]]"
```

`rank_vendas` é ordenação comercial da própria loja, não métrica de Instagram.
Serve para saber **o que a cliente compra**, e é o melhor proxy disponível até
chegarem os dados de Insights.

## O que a loja vende de verdade

Ordem de mais vendidos (topo da vitrine, 15/09/2026):

| # | Peça | Preço | Tecido | Composição |
|---|---|---|---|---|
| 1 | Jaqueta Manga Longa Brasil | R$ 299,00 | Chimpa e ribana canelada | 100% poliéster |
| 2 | Jaqueta Camurça Oversized | R$ 179,90 | Scuba suede com crepinho | 95% poliéster, 5% elastano |
| 3 | Macacão Pantalona com Bolsos | R$ 79,90 | — | — |
| 4 | Blusa Ombro Plissado | R$ 45,90 | Alfaiataria premium | 95% poliéster, 5% elastano |
| 5 | Macacão Drapeado Alça Dupla | R$ 78,90 | Viscolycra | 93% viscose, 7% elastano |
| 6 | Macacão Pantalona Ombro Só | R$ 78,90 | Viscolycra | 96% poliéster, 4% elastano |
| 7 | Vestido Longo Duna | R$ 75,90 | Crepe duna premium | — |
| 8 | Lenço Estampado Bolinhas | R$ 129,90 | Poliéster | — |
| 9 | Vestido Poá Tomara Que Caia | R$ 84,90 | Crepinho | 96% poliéster, 4% elastano |
| 10 | Vestido Assimétrico Drapeado | R$ 84,90 | Suplex premium | 96% poliéster, 4% elastano |
| 11 | Poncho Bico Assimétrico | R$ 79,90 | Tricot premium | — |
| 12 | Blusa Tomara que Caia Peplum | R$ 59,90 | Suplex premium | 96% poliéster, 4% elastano |
| 13 | Vestido Longo Princesa | R$ 78,90 | Duna premium | 96% poliéster, 4% elastano |
| 14 | Blusa Regata Botões | R$ 39,90 | Malha elástica | — |
| 15 | Polo Tricot Manga Longa | R$ 149,90 | Tricot | 86% acrílico, 14% poliéster |
| 17 | Conjunto Cropped Top Brasil | R$ 109,90 | Viscolycra | 96% poliéster, 4% elastano |
| 20 | Macaquinho Soltinho Frente Única | R$ 129,90 | Crepe duna premium | — |
| 22 | Jaqueta Bomber Courino Oversized | R$ 199,90 | Courino com crepinho | 97% poliéster, 3% elastano |
| 28 | Pantalona Alfaiataria Wide Leg | R$ 78,90 | Linho premium | 70% viscose, 30% linho |

Leitura do ranking:

- **Macacão é a peça-chave da casa.** Três macacões entre os seis primeiros.
  Uma peça que resolve o look inteiro ganha da combinação que a cliente precisa
  montar. Esse é o ângulo de roteiro mais alinhado com o que já vende.
- **Vestido é a categoria mais densa no topo** — 12 dos 40 primeiros. Drapeado,
  poá e comprimento longo aparecem repetidamente.
- **Casaco é o ticket alto** (mediana R$ 124,90, topo em R$ 299,00) e ocupa as
  posições 1, 2 e 22. Vale conteúdo de peça-investimento.
- **Conjunto tem só 2 fichas no site.** Não trate conjunto como carro-chefe sem
  confirmar com a cliente se a categoria vai crescer.
- Peças da linha Brasil (Copa 2026) ainda ranqueiam alto, mas a data passou.
  Confirme se seguem em campanha antes de escrever sobre elas.

## Preço

| Faixa | Itens | % |
|---|---|---|
| até R$ 49,90 | 41 | 22% |
| R$ 50 a R$ 79,90 | 76 | 41% |
| R$ 80 a R$ 119,90 | 33 | 18% |
| R$ 120 a R$ 199,90 | 36 | 19% |
| R$ 200+ | 1 | 1% |

Mediana do catálogo: **R$ 78,90**. Mínimo R$ 19,90, máximo R$ 299,00.

Mediana por categoria: vestidos R$ 84,90 · macacões R$ 78,90 · calças R$ 78,90 ·
saias R$ 65,90 · blusas R$ 57,90 · croppeds R$ 42,90 · casacos R$ 124,90 ·
kimonos e ponchos R$ 104,90.

**Implicação de roteiro:** o ticket médio do e-commerce de moda no Brasil está em
torno de R$ 225 e a peça mediana da Swisz custa R$ 78,90. O caminho para o carrinho
maior é **duas ou três peças que conversam**, não uma peça cara. Isso sustenta
roteiro de combinação, e sustenta o frete grátis (ver abaixo).

## Tecidos que a marca realmente usa

Nos 40 mais vendidos: **suplex premium** (8), **viscolycra** (6), **crepe/crepinho/
duna** (6), **courino** (2), além de tricot, alfaiataria com elastano, linho
premium, scuba suede e chimpa.

**22 das 25 peças com composição declarada no top 40 têm elastano.** A promessa
técnica dominante da casa é elasticidade e caimento que acompanha o corpo. É o
atributo que mais aparece e o que mais rende roteiro.

Vocabulário que a própria loja usa para benefício (reaproveite, é linguagem da casa):
"não fica transparente quando você agacha", "não marca", "não amassa", "não embola
nem afina depois de lavar", "segura a barriga e não desce quando você senta",
"tem bojo, dispensa o sutiã".

**Cuidado com a etiqueta.** Algumas fichas nomeiam o tecido como viscolycra mas
declaram composição de poliéster com elastano. Quando houver divergência entre
nome do tecido e composição, **cite a composição** ou não cite nenhum dos dois.
Nunca diga "viscose" apoiado só no nome comercial.

## Grade e modelagem

- Grade mais comum: **P, M, G, GG**; parte do catálogo tem PP.
- Uma parcela grande das peças é **tamanho único, "veste 36/42"**.
- Cada ficha traz comprimento da peça por tamanho, em centímetros.
- Não existe tabela de medidas de busto, cintura e quadril publicada no site.
  **Não afirme medida de corpo.** Se o roteiro precisar disso, pergunte.

## Condições comerciais (confirmadas no site em 15/09/2026)

- **Frete grátis a partir de R$ 199,90.**
- **Entrega no mesmo dia** para São Paulo e Região Metropolitana (entrega expressa
  e turbo).
- **3x sem juros** no cartão.
- **5% de desconto no Pix** (não acumulável com algumas promoções).
- Loja em Nuvemshop. Endereço: Rua Dr. Luís Carlos, 1.212, Chácara Califórnia,
  São Paulo. Razão social Swisz Fashion Group.

O gatilho de frete grátis é material de CTA legítimo quando o roteiro trabalha
combinação de peças, porque duas peças medianas cruzam os R$ 199,90.

## Categorias ativas no site

acessórios · blusas · bodies · calças · casacos · conjuntos · croppeds ·
kimonos e ponchos · macacões · pijamas · saias · saídas de praia · shorts · vestidos

## O que continua faltando

- Venda real por peça (o ranking é ordenação da vitrine, não faturamento).
- Taxa de devolução e motivo — o dado que mais corrigiria roteiro de caimento.
- Tabela de medidas do corpo por tamanho.
- Recompra, ticket médio real e origem de tráfego.
- Calendário de lançamento da coleção de Verão 26/27.
