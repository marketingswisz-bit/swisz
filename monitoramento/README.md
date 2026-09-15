# Monitoramento — como a coleta funciona e o que falta ligar

## O problema que este diretório resolve

Não existe forma legítima de ler performance de post de outro perfil raspando o
site do Instagram. A página pública é um muro de login e raspagem viola os termos
de uso. A via oficial é uma só: o endpoint **business_discovery** da Instagram
Graph API.

Ele funciona, é gratuito, e tem limites que moldam toda a análise:

| O que dá | O que não dá |
|---|---|
| Curtidas e comentários por post | Visualização / reprodução de Reels |
| Legenda, tipo de mídia, data, permalink | Alcance, retenção, salvamento, compartilhamento |
| Seguidores e total de publicações | Qualquer métrica privada de outro perfil |
| Qualquer conta **Business ou Creator** pública | Conta pessoal, mesmo pública |

Salvamento e compartilhamento seriam os melhores sinais, e ninguém tem acesso a
eles fora da própria conta. Por isso a análise usa curtida + comentário
(comentário com peso 5) e compara cada post com a mediana do próprio perfil, em
vez de comparar número cru entre contas.

**Para o @swiszoficial isso é diferente:** como a conta é da casa, o Instagram
Insights entrega alcance, retenção, salvamento e compartilhamento. Esse dado vale
mais que tudo que o painel coleta. Ver `referencias/07-aprendizado.md`.

## Ligar a coleta — uma vez só

1. **Conta Instagram Business ou Creator** para o @swiszoficial, vinculada a uma
   Página do Facebook. Provavelmente já existe, se o perfil tem loja ou anúncio.
2. **App no Meta for Developers** (developers.facebook.com) com o produto
   *Instagram Graph API* adicionado.
3. **Permissões** no token: `instagram_basic` e `pages_read_engagement`.
4. **Token de longa duração** (60 dias). O de teste dura 1h e não serve.
5. **ID da conta Instagram** — o número que identifica o @swiszoficial na API,
   não o @. Sai de `GET /me/accounts` → `instagram_business_account`.

Com isso em mãos:

```bash
export IG_TOKEN="..."
export IG_USER_ID="..."
python3 scripts/coletar.py && python3 scripts/consolidar.py
```

**O token expira em 60 dias.** Renove antes, ou a rotina para e o histórico ganha
um buraco. Vale marcar no calendário.

## Onde a coleta roda

O ambiente do Claude Code na web tem saída de rede restrita — `graph.facebook.com`
está bloqueado, então a coleta **não roda de dentro da sessão** enquanto a
política de rede do ambiente não liberar esse domínio.

Duas saídas, e a primeira é a recomendada:

**1. GitHub Actions** (`.github/workflows/coleta-diaria.yml`). Roda todo dia às
06:30 de Brasília, grava o snapshot e dá commit. A sessão diária do Claude só lê
o que já está no repositório. Vantagem: não depende da rede da sessão, e o
histórico fica versionado sozinho.

Para ligar, em *Settings → Secrets and variables → Actions* do repositório:
- `IG_TOKEN`
- `IG_USER_ID`

Workflow agendado só dispara no **branch padrão** do repositório. Enquanto este
trabalho estiver em branch de feature, use *Run workflow* na aba Actions para
testar.

**2. Liberar `graph.facebook.com`** na política de rede do ambiente e definir
`IG_TOKEN` / `IG_USER_ID` como variáveis de ambiente. Aí a própria sessão diária
coleta. Mais simples de entender, depende de mudar a configuração do ambiente.

## Editar o painel

`contas.yml`. O campo `tier` é o que sustenta a leitura de difusão:

- `farol` — onde a tendência aparece primeiro
- `traducao` — quem traduz para a mulher real
- `concorrente` — disputa a mesma cliente
- `massa` — varejo grande; chegou aqui, já passou do pico
- `casa` — o @swiszoficial, linha de base e não fonte de pauta

Contas marcadas `a_validar` são sugestões do agente. A primeira coleta confirma
quais existem como Business/Creator e marca sozinha as que não resolvem. Conta
indicada pela Swisz nunca é removida automaticamente — a falha aparece no
relatório e a decisão é de quem cuida do perfil.
