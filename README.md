# Roteirista Social-First — Swisz

Agente especialista em roteiro de conteúdo social para a Swisz, e-commerce de
moda feminina.

## Como usar

No Claude Code, chame o subagente `roteirista-swisz`:

```
Use o agente roteirista-swisz para criar 5 roteiros de Reels sobre conjuntos de
alfaiataria para a semana do Dia do Cliente.
```

Ele entrega direto no chat. Peça documento só quando quiser um.

## Estrutura

```
.claude/agents/roteirista-swisz.md   definição do agente
referencias/
  00-marca.md                        Swisz: catálogo, posicionamento, lacunas
  01-publico.md                      a cliente: rotina, objeções, vocabulário
  02-reels.md                        gancho, retenção, duração, CTA
  03-linguagem.md                    gatilhos, persuasão, lista negra de vícios
  04-moda-tecnica.md                 tecido, caimento, cor, produção, varejo
  05-tendencia-sazonalidade.md       P/V 26/27 e calendário do varejo BR
  06-fontes.md                       onde pesquisar e com que peso
  07-aprendizado.md                  log vivo de hipóteses e resultados
```

## Regras que definem o agente

- Reels curto (15-30s), gancho nos 3 primeiros segundos, uma informação de valor,
  CTA único no fim.
- Sempre puxa para o produto — por atributo técnico ou por benefício adquirido.
- Nunca diz "use o que você já tem". Diz "escolha uma peça nova que converse com
  o que você já tem".
- Ensina estilo pessoal antes de tendência, e mostra a dose de tendência que cabe
  numa rotina de trabalho.
- Sem vícios de linguagem de IA: nada de trio genérico, frase de efeito no fecho
  ou dualismo "não é sobre X, é sobre Y".
- Não inventa. Quando falta informação ou a fonte está bloqueada, pergunta.
- Se aperfeiçoa: pesquisa fontes de moda, comportamento e consumo, e registra
  aprendizado em `referencias/07-aprendizado.md`.

## Pendências

O agente está operacional, mas calibrado com benchmark de mercado.
Ver `referencias/07-aprendizado.md` para a lista do que é preciso fornecer —
principalmente a exportação do Instagram Insights do @swiszoficial e o catálogo
com preço e composição de tecido.
