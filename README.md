# Conteúdo social da Swisz

Dois sistemas que se encaixam:

1. **Rotina diária de análise** — lê todo dia o que performou nos perfis de moda
   monitorados, compara com a leitura do dia anterior e entrega pautas numeradas.
2. **Roteirista** — agente que transforma a pauta escolhida em roteiro de Reels,
   carrossel ou stories.

O fluxo é: a rotina sugere → você escolhe os números → o roteirista escreve.

## Rotina diária

Dispara sozinha todo dia às 07:00 de Brasília. Também dá para chamar na mão:

```
/analise-diaria
```

Ela entrega um relatório com os temas separados em **subindo**, **no pico** e
**esfriando**, e de 6 a 12 pautas numeradas. Você responde com os números:

```
desenvolve P2, P5 e P7
```

E os roteiros saem pelo `roteirista-swisz`.

### Como ela decide o que está subindo

Duas medidas independentes, porque cada uma sozinha engana.

**Desempenho relativo (IPR).** Engajamento do post dividido pela mediana da
própria conta. IPR 3,0 quer dizer que rendeu o triplo do normal daquele perfil.
Neutraliza tamanho de seguidor — um post de uma criadora de 90 mil com IPR 4 é
sinal mais forte que um da Renner com IPR 1,2.

**Velocidade.** O quanto o post ganhou nas últimas 24h. Separa o que já acumulou
muito do que está esquentando agora, que é o que interessa.

**Difusão.** Cada conta do painel tem um tier. Tendência de moda desce: nasce em
`farol`, passa por `traducao` e `concorrente`, morre em `massa`. O tier em que um
tema aparece diz em que ponto da curva ele está, independente do número.

Cruzando os três, e comparando com o registro de ontem em `dados/temas.json`, cada
tema recebe um estado. A recomendação sai daí: **subindo** é onde produzir,
porque os dois dias entre pauta e publicação trabalham a favor; **no pico** só
vale com ângulo que ninguém copia (produção própria, modelagem, corpo real);
**esfriando** só entra com contraponto.

### O que precisa ser ligado

A coleta usa o endpoint oficial `business_discovery` da Instagram Graph API e
depende de um token. **Enquanto ele não existir, a rotina não produz relatório** —
ela diz o que falta em vez de inventar número. Instruções em
`monitoramento/README.md`.

## Roteirista

```
Use o agente roteirista-swisz para criar 5 roteiros de Reels sobre conjuntos de
alfaiataria para a semana do Dia do Cliente.
```

Entrega direto no chat. Peça documento só quando quiser um.

Regras que o definem:

- Reels curto (15-30s), gancho nos 3 primeiros segundos, uma informação de valor,
  CTA único no fim.
- Sempre puxa para o produto — por atributo técnico ou por benefício adquirido.
- Nunca diz "use o que você já tem". Diz "escolha uma peça nova que converse com
  o que você já tem".
- Ensina estilo pessoal antes de tendência.
- Sem vícios de linguagem de IA.
- Não inventa. Quando falta informação ou a fonte está bloqueada, pergunta.

## Estrutura

```
.claude/
  agents/roteirista-swisz.md         o roteirista
  skills/analise-diaria/SKILL.md     o método da rotina diária
monitoramento/
  contas.yml                         painel monitorado, por tier
  README.md                          como ligar a coleta, e os limites da API
scripts/
  coletar.py                         API -> snapshot bruto do dia
  consolidar.py                      dois snapshots -> IPR, velocidade, digesto
dados/
  brutos/AAAA-MM-DD.json             retrato do painel no dia
  consolidado/AAAA-MM-DD.{json,md}   métricas e digesto para leitura
  relatorios/AAAA-MM-DD.md           relatório do dia com as pautas
  temas.json                         registro vivo dos temas e da trajetória
referencias/
  00-marca.md                        Swisz: catálogo, posicionamento, lacunas
  01-publico.md                      a cliente: rotina, objeções, vocabulário
  02-reels.md                        gancho, retenção, duração, CTA
  03-linguagem.md                    gatilhos, persuasão, lista negra de vícios
  04-moda-tecnica.md                 tecido, caimento, cor, produção, varejo
  05-tendencia-sazonalidade.md       P/V 26/27 e calendário do varejo BR
  06-fontes.md                       onde pesquisar e com que peso
  07-aprendizado.md                  log vivo de hipóteses e resultados
.github/workflows/coleta-diaria.yml  coleta agendada fora da sessão
```

`dados/temas.json` é a peça que faz a rotina ter memória. É ele que permite dizer
que um tema está crescendo e não apenas que está grande. Se ele for apagado, a
leitura de trajetória recomeça do zero.

## Pendências

- Token da Instagram Graph API — sem ele não há coleta.
- Exportação do Instagram Insights do @swiszoficial. É o único lugar com alcance,
  retenção, salvamento e compartilhamento, e vale mais que todo o resto do painel.
  Lista do que é preciso em `referencias/07-aprendizado.md`.
- Catálogo com preço e composição de tecido, para a pauta virar venda de peça
  específica em vez de conselho genérico.
