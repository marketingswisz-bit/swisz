# Log de aprendizado

Arquivo vivo. O agente atualiza sozinho. Dado da casa sempre ganha de benchmark
de mercado.

---

## Status da análise de performance

**Instagram @swiszoficial: não analisado. Bloqueio de login, não de rede.**

Em 15/09/2026 o acesso à internet desta sessão funciona (swisz.com.br foi lido
por inteiro), mas o Instagram exige autenticação: a API pública responde
`require_login` e a página do perfil devolve página de erro. Métrica de
performance — alcance, retenção, watch time, sends, salvamento — só existe
dentro do Insights da conta e nenhuma ferramenta externa lê isso sem login.

**Nada foi presumido sobre o desempenho do perfil.** Os parâmetros de formato que
o agente usa hoje vêm de benchmark público e devem ser substituídos assim que
houver dado real.

### O que é preciso receber

Exportação do Instagram Insights ou prints, dos últimos 90 dias, com:

- Reels ordenados por **alcance**, por **visualizações**, por **watch time médio**
  e por **sends** — as quatro listas, porque elas não coincidem
- Salvamentos por post
- Duração de cada Reels e % de retenção
- Taxa de seguidores vs. não seguidores no alcance
- Os 10 melhores e os 10 piores, com o tema e o gancho de cada um
- Cliques no link da bio e origem de tráfego para o site, se houver
- Faixa etária e localização da audiência

Com isso, preencher as seções abaixo e revisar `02-reels.md`.

**Loja: analisada.** Ver `08-catalogo.md`. O ranking de mais vendidos da vitrine
é o melhor proxy disponível de preferência da cliente enquanto o Insights não chega.

---

## O que funciona (validado com dado da casa)

**Venda (vitrine de mais vendidos, 15/09/2026):**

- **Peça única que resolve o look inteiro vende mais.** Três macacões entre as
  seis primeiras posições; vestidos ocupam 12 das 40 primeiras. A cliente compra
  a solução pronta, não o desafio de combinar.
- **Casaco sustenta ticket alto.** Posições 1, 2 e 22 são jaquetas, de R$ 179,90
  a R$ 299,00, num catálogo de mediana R$ 78,90.
- **Elastano é o atributo dominante da casa.** 22 das 25 peças com composição
  declarada no top 40 têm elastano. Roteiro de caimento, conforto e "não marca"
  fala do que a marca realmente entrega.
- **Drapeado e poá aparecem repetidamente no topo** dos vestidos.

**Conteúdo:** nada validado. Aguardando Insights.

## O que não funciona (validado com dado da casa)

Nada validado ainda.

## Hipóteses em teste

| # | Hipótese | Base | Status |
|---|---|---|---|
| 1 | Conteúdo de modelagem/caimento gera mais **send** que conteúdo de look montado | Send é o sinal de alcance em não seguidores; dúvida de caimento é compartilhável entre amigas | A testar |
| 2 | Bastidor de produção própria gera mais **salvamento** e mais confiança que conteúdo de tendência | Diferencial que concorrente revendedor não tem, e a régua de autenticidade de 2026 favorece | A testar |
| 3 | Reels de 15-22s supera os de 40s+ no alcance a não seguidores | Watch time e taxa de replay são o sinal dominante | A testar |
| 4 | CTA "manda para a amiga que..." supera "comenta a palavra X" em alcance | Aciona send diretamente | A testar |
| 5 | Roteiro que nomeia a objeção da cliente na primeira frase retém mais que gancho de tendência | Espelhamento de objeção; público de baixa consciência de moda | A testar |
| 6 | **Macacão** é o melhor gerador de conteúdo de conversão da casa | É o que mais vende e resolve o look inteiro num item só | A testar |
| 7 | Roteiro de duas peças que se combinam supera roteiro de peça solta em valor de carrinho | Peça mediana R$ 78,90 contra frete grátis a partir de R$ 199,90 — duas peças cruzam a régua | A testar |
| 8 | Conteúdo que usa o vocabulário da própria ficha ("não fica transparente quando você agacha") retém mais que descrição genérica de tecido | Linguagem de objeção concreta, já testada em página de produto | A testar |

Hipótese aposentada: **"conjunto é a peça de maior valor por roteiro"**. A loja
tem só duas fichas na categoria conjuntos. O lugar que a hipótese ocupava passa
a ser do macacão (hipótese 6).

---

## Registro de atualizações

**15/09/2026 — levantamento do catálogo real.**
187 fichas de produto lidas em swisz.com.br, com nome, preço, SKU, tecido,
composição, grade, comprimento, estoque e posição na vitrine de mais vendidos.
Gerados `08-catalogo.md` e `catalogo-swisz.json`. Atualizados `00-marca.md`
(condições comerciais, categorias, faixa de preço) e `05-tendencia-sazonalidade.md`
(datas comerciais confirmadas de 2026, horizonte P/V 27).
Atualizado `02-reels.md`: os sinais de ranqueamento são watch time, **sends por
alcance** e **curtidas por alcance** — razão, não número absoluto — e a régua de
autenticidade anunciada no balanço de fim de 2025 passou a penalizar estética de
campanha e material gerado por IA.
Confirmado que o Instagram exige login; registrado em `06-fontes.md`.

**15/09/2026 — criação.**
Base montada com: sinais de ranqueamento do Instagram em 2026, benchmark público
de duração e retenção de Reels, tendências P/V 26 e 26/27 (WGSN, via blog
público), Pinterest Predicts 2026, calendário do varejo de moda brasileiro, dados
de consumo de moda e e-commerce no Brasil, e informação pública sobre a Swisz.

<!-- Novas entradas abaixo, mais recente primeiro. Formato:
**DD/MM/AAAA — título.** O que mudou, qual a fonte, qual arquivo de referência
foi atualizado. -->
