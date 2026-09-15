---
name: analise-diaria
description: Rotina diária de análise de performance de conteúdo dos perfis de moda monitorados e sugestão de pautas para a Swisz. Coleta os posts públicos do painel, mede desempenho relativo e velocidade, compara com a leitura do dia anterior, classifica cada tema em subindo / no pico / esfriando, e entrega pautas numeradas para escolha. Use quando pedirem a análise do dia, o relatório de tendências, as pautas do dia, ou quando a rotina agendada disparar.
---

# Análise diária de conteúdo — painel de moda

Você produz, todo dia, uma leitura do que está performando nos perfis monitorados
e transforma isso em pauta acionável para a Swisz.

O produto final não é um relatório de métrica. É uma **lista numerada de pautas**
que a pessoa escolhe, e que depois vira roteiro no agente `roteirista-swisz`.

Regra que atravessa tudo: **o valor desta rotina está na comparação com ontem.**
Um número isolado não diz se um tema está nascendo ou morrendo. Sem o dia
anterior, você tem uma fotografia; com ele, você tem direção.

---

## Passo 0 — Situar-se antes de olhar número

Sempre, nesta ordem:

1. `dados/temas.json` — o registro vivo dos temas, com estado e histórico.
2. O relatório mais recente em `dados/relatorios/` — a leitura de ontem.
3. `referencias/00-marca.md` e `referencias/01-publico.md` — para não sugerir
   pauta que a Swisz não tem produto para sustentar.

Você precisa saber, antes de abrir a coleta de hoje: quais temas estavam
subindo, qual já estava no pico, o que você já mandou produzir, e o que a pessoa
escolheu ou descartou.

---

## Passo 1 — Coleta

```bash
python3 scripts/coletar.py && python3 scripts/consolidar.py
```

O primeiro grava `dados/brutos/AAAA-MM-DD.json`. O segundo grava
`dados/consolidado/AAAA-MM-DD.json` e o digesto `.md`, que é o que você lê.

**Se a coleta falhar**, não improvise. Vá para o *Modo sem dado* no fim deste
arquivo. Nunca produza um relatório com número inventado, estimado ou lembrado.

Contas que não retornarem aparecem em "Contas que não retornaram" no digesto.
Repasse isso no relatório — um perfil confirmado pela Swisz que some do painel
é informação, não ruído.

---

## Passo 2 — Ler os números certos

O digesto traz três listas e cada uma responde a uma pergunta diferente.
Não confunda:

| Lista | Pergunta que responde |
|---|---|
| **IPR** (desempenho relativo) | O que rendeu acima da régua da própria conta |
| **Velocidade** | O que está ganhando tração **agora**, nas últimas 24h |
| **Últimas 30h** | O que acabou de sair e ainda não tem julgamento |

**IPR** é engajamento do post dividido pela mediana da conta. IPR 3,0 = rendeu o
triplo do normal daquele perfil. Neutraliza tamanho — um post de @joyalano_ com
IPR 4 é sinal mais forte que um post da @renner com IPR 1,2, mesmo a Renner
tendo cinquenta vezes mais seguidor.

**Velocidade** é o ganho das últimas 24h, também em múltiplo da mediana. Um post
com IPR alto e velocidade baixa já deu o que tinha que dar. Um post com IPR médio
e velocidade alta é o que você quer olhar.

Ignore número absoluto de curtida. Ele só mede o tamanho da conta.

Dois cuidados:
- Post com menos de 20h ainda está acumulando. Ele aparece em "últimas 30h" e
  não no ranking de IPR. Não conclua nada sobre ele além de "existe".
- Conta com `curtidas_ocultas` só tem comentário no cálculo. O engajamento dela
  sai subestimado. Diga isso se ela aparecer no topo.

---

## Passo 3 — Classificar em temas

Post não é pauta. **Tema** é pauta. Um tema é um assunto de conteúdo que dá para
a Swisz produzir: uma peça, uma combinação, um problema de vestir, um momento de
uso, um formato de conteúdo recorrente.

Exemplos de recorte bom: "alfaiataria com tênis", "saia longa no calor",
"o que vestir em reunião online", "provador com três corpos diferentes",
"por que essa calça não marca".

Exemplos de recorte ruim, largo demais para virar roteiro: "verão", "conforto",
"tendência 2027".

### A regra mais importante desta rotina

**Slug de tema é permanente.** A comparação com ontem só funciona se o mesmo
assunto carregar o mesmo identificador todo dia.

- Reutilize o slug existente em `dados/temas.json` sempre que o post couber nele.
  Na dúvida entre encaixar num tema existente e criar um novo, **encaixe**.
- Crie tema novo só quando for genuinamente outro assunto.
- **Nunca renomeie um slug.** Se o rótulo em português precisar mudar, mude
  `rotulo` e guarde o antigo em `aliases`. O slug fica.
- Um post pode entrar em até dois temas. Mais que isso, o recorte está largo.

### Score do tema

Para cada tema, sobre os posts dos últimos 14 dias:

- `score` = soma dos IPR dos posts do tema. Conte no máximo 3 posts por conta,
  os de maior IPR — senão uma conta que postou dez vezes sobre o assunto
  sequestra a leitura.
- `calor` = soma das velocidades dos posts do tema. Pode ser negativo.
- `n_contas` = quantas contas distintas tocaram o tema.
- `tiers` = quais tiers do painel aparecem (`farol`, `traducao`, `concorrente`,
  `massa`). Ignore `casa` — a Swisz não é sinal de mercado.

---

## Passo 4 — Trajetória: os três estados que a Swisz pediu

Cada tema recebe um estado, cruzando **dois eixos independentes**. Usar um só
engana.

**Eixo 1 — engajamento.** `score` e `calor` de hoje contra os de ontem, e contra
o pico registrado em `dados/temas.json`.

**Eixo 2 — difusão.** Por onde o tema está andando no painel. Tendência de moda
desce: nasce em `farol`, passa por `traducao` e `concorrente`, e termina em
`massa`. Quando chega no varejo grande, já é tarde para parecer novidade.

### Os estados

**RADAR** — apareceu há 2 dias ou menos, ou está em menos de 3 contas.
Sinal fraco demais para decidir. Anote e observe.

**SUBINDO** — é onde a Swisz ganha dinheiro. Vale ao menos um destes:
- `score` cresceu 15% ou mais em relação a ontem;
- `calor` positivo e maior que o de ontem;
- `n_contas` aumentou;
- a difusão desceu um tier (estava só em `farol`, entrou em `traducao`).

E ainda **não** está em `massa`.

**NO PICO** — está em alta e parou de acelerar:
- `score` alto e variação entre −15% e +15% contra ontem; ou
- difusão em 3 tiers ou mais; ou
- entrou em `massa` nos últimos 2 dias.

**ESFRIANDO** — veio e está passando. Vale qualquer um:
- `score` caiu para 80% ou menos do pico registrado, e o pico foi há 2 dias ou mais;
- `calor` virou negativo ou desabou (estava acima de 1,0 e caiu abaixo de 0,3);
- está em `massa` há 3 dias ou mais.

Esses cortes são régua, não lei. Se o dado for pouco — poucas contas, pouco
histórico, primeira semana da rotina — diga que a classificação está frágil em
vez de fingir precisão. Tema com 3 dias de histórico não tem pico confiável.

### Quando o histórico ainda não existe

Na primeira coleta não há eixo 1. Classifique só por difusão e diga, com
todas as letras, que a leitura de trajetória começa no segundo dia. A rotina
fica confiável a partir do terceiro ou quarto dia.

---

## Passo 5 — De trajetória para decisão

A Swisz leva de um a três dias entre escolher a pauta e publicar. Isso muda tudo:

- **SUBINDO → produza.** É onde o atraso de produção trabalha a favor. Prioridade
  máxima, e a maior parte das pautas do dia deve sair daqui.
- **NO PICO → produza só se sair em 24h, ou com ângulo próprio.** O ângulo
  próprio da Swisz é produção nacional, modelagem e corpo real — coisa que
  ninguém do painel consegue copiar. Com esse ângulo, entrar no pico ainda paga.
- **ESFRIANDO → não produza a versão óbvia.** Só entre com contraponto, que é
  conteúdo forte: "por que [tema] não funciona na semana de quem trabalha", ou
  "a versão de [tema] que sobrevive ao ano que vem". Pega o interesse residual e
  ainda constrói autoridade.
- **RADAR → não produza.** Observe. Exceção: se o tema cai exatamente no catálogo
  da Swisz, vale uma aposta barata — um story, não um Reels.

Antes de escrever a pauta, confira duas coisas:

1. **A Swisz tem produto para isso?** Categoria em `referencias/00-marca.md`.
   Pauta sem peça para vender é conteúdo de portal de moda, não de e-commerce.
2. **Já virou pauta antes?** Campo `ja_virou_pauta` em `dados/temas.json`. Não
   repita o que já foi entregue, a menos que o ângulo seja outro — e aí diga
   qual é a diferença.

---

## Passo 6 — Escrever o relatório

Grave em `dados/relatorios/AAAA-MM-DD.md` e entregue o mesmo conteúdo no chat.
Sem preâmbulo e sem comentar o próprio trabalho.

```markdown
# Pautas do dia — DD/MM/AAAA

## O que mudou desde ontem
[3 a 6 linhas. Só movimento: tema que mudou de estado, tema que entrou,
tema que saiu, conta que sumiu do painel. Se nada mudou de verdade, escreva
que nada mudou — dia parado é informação.]

## Subindo
| tema | score (ontem) | calor | contas | difusão |
[uma linha por tema, com a variação explícita]

## No pico
[mesma tabela]

## Esfriando
[mesma tabela]

## Radar
[lista curta, uma linha por tema]

## Swisz no painel
[Como as publicações do @swiszoficial renderam contra a régua do painel.
O que a casa publicou e o que deixou passar. 3 a 5 linhas.]

---

## Pautas

**P1 — [título da pauta]**
Tema: [rótulo] · Estado: [subindo/pico/esfriando] · Formato: [Reels/carrossel/story]
Por que agora: [1 ou 2 linhas ancoradas no número — cite IPR, velocidade ou difusão]
Ângulo Swisz: [qual categoria de produto sustenta, por atributo técnico ou benefício]
Direção de gancho: [uma linha. Não escreva o roteiro — isso é do roteirista-swisz.]
Evidência: [@conta link, @conta link]

**P2 — ...**
```

Entre 6 e 12 pautas. Menos que 6 num dia com dado bom quer dizer que você não
olhou direito; mais que 12 vira lista que ninguém lê.

Ordene por prioridade, não por estado. A P1 é a que você produziria primeiro.

Feche com uma linha só:

> Escolha as pautas que quer desenvolver (ex.: "desenvolve P2, P5 e P7") e eu
> passo para o roteirista-swisz.

---

## Passo 7 — Atualizar o registro

Atualize `dados/temas.json` **antes** de terminar. É ele que faz a rotina de
amanhã enxergar hoje. Para cada tema tocado:

- acrescente a entrada de hoje em `historico` (data, score, calor, n_contas,
  tiers, estado);
- atualize `estado`;
- atualize `pico_em` e `score_pico` se o score de hoje for o maior já visto;
- registre em `ja_virou_pauta` toda pauta que entrou no relatório, com o número.

Mantenha `historico` nos últimos 30 registros por tema. Tema sem aparição há
mais de 21 dias recebe `estado: "dormente"` e sai das tabelas — mas o registro
fica, porque tendência de moda volta e o histórico antigo é o que vai permitir
reconhecer o retorno.

## Passo 8 — Commit

```bash
git add dados/ monitoramento/contas.yml
git commit -m "Análise diária AAAA-MM-DD"
git push -u origin <branch>
```

O snapshot bruto precisa estar versionado, senão a comparação de amanhã não tem
com o que comparar.

---

## Passo 9 — Quando a pessoa escolher as pautas

Ela responde com os números. Você então:

1. Chama o agente `roteirista-swisz`, uma chamada por pauta escolhida.
2. Entrega para ele a pauta inteira — tema, estado, por que agora, ângulo,
   direção de gancho e os links de evidência. O roteirista não viu o relatório;
   se você resumir demais, ele escreve no escuro.
3. Marca `desenvolvida: true` em `ja_virou_pauta`.
4. Entrega os roteiros no chat, sem reescrever o que ele produziu.

Pauta não escolhida **não** é pauta rejeitada. Se o tema continuar subindo
amanhã, pode voltar — com ângulo diferente, e dizendo que voltou e por quê.

---

## Modo sem dado

A coleta depende de `IG_TOKEN` e `IG_USER_ID` (ver `monitoramento/README.md`) e
de acesso de rede a `graph.facebook.com`. Quando qualquer um faltar:

1. Diga qual é a barreira, com a mensagem de erro real.
2. **Não produza relatório de pauta.** Sem dado do dia não existe comparação com
   ontem, e o que sobra é palpite com cara de análise.
3. Ofereça as duas saídas concretas:
   - a credencial e o que ela destrava;
   - um caminho manual — a pessoa manda print ou exportação do que performou, e
     você roda os passos 3 a 7 sobre isso, marcando a origem como manual no
     relatório.
4. Se a falha for de poucas contas e o resto tiver vindo, siga normalmente e
   liste as que faltaram. Análise parcial declarada é útil; análise parcial
   silenciosa, não.

Vale aqui a regra do `roteirista-swisz`: não inventar. Nem número, nem tendência,
nem post que você não viu.
