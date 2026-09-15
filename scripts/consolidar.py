#!/usr/bin/env python3
"""Transforma dois snapshots em métricas comparáveis.

O snapshot bruto traz contagem acumulada de curtida e comentário no instante da
coleta. Isso sozinho não diz quase nada: um post de marca grande tem número
grande porque a marca é grande, e um post de três dias tem número maior que um
de três horas. Este script tira as duas distorções.

Três métricas, e cada uma responde a uma pergunta diferente:

  IPR — índice de performance relativa.
    Engajamento do post dividido pela mediana da própria conta. IPR 3,0 quer
    dizer "rendeu o triplo do que essa conta costuma render". Neutraliza tamanho
    de seguidor e cultura de engajamento da conta. Responde: o que performou.

  VELOCIDADE.
    Quanto o post ganhou nas últimas 24h, em múltiplos da mediana da conta.
    Só existe para post visto em duas coletas. Responde: o que está esquentando
    agora — que é coisa diferente do que já acumulou muito.

  DIFUSÃO (calculada no relatório, não aqui).
    Em quantos tiers do painel o tema aparece. Tema só em 'farol' é cedo; tema
    que chegou em 'massa' já é tarde.

Entrada : dados/brutos/AAAA-MM-DD.json (hoje e o anterior disponível)
Saída   : dados/consolidado/AAAA-MM-DD.json  — completo, para consulta
          dados/consolidado/AAAA-MM-DD.md    — digesto curto, para o agente ler
"""

import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTOS = RAIZ / "dados" / "brutos"
SAIDA = RAIZ / "dados" / "consolidado"

# Comentário custa muito mais esforço que curtida, e prevê melhor tema que
# mexeu com a pessoa. Peso 5 é arbitrado — ajuste depois de ter série própria.
PESO_COMENTARIO = 5

# Post com menos de 18h ainda está acumulando: não entra no cálculo da mediana
# da conta, senão a base de comparação afunda.
IDADE_MIN_BASELINE_H = 18
IDADE_MAX_BASELINE_D = 45

# Janela do ranking de desempenho.
IDADE_MIN_RANKING_H = 20
IDADE_MAX_RANKING_D = 14


def agora():
    return datetime.now(timezone.utc)


def ler_ts(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def engajamento(post):
    curtidas = post.get("like_count")
    comentarios = post.get("comments_count") or 0
    ocultas = curtidas is None
    return (0 if ocultas else curtidas) + PESO_COMENTARIO * comentarios, ocultas


def snapshots():
    arquivos = sorted(BRUTOS.glob("*.json"))
    if not arquivos:
        print("nenhum snapshot em dados/brutos/. Rode scripts/coletar.py antes.", file=sys.stderr)
        sys.exit(2)
    hoje = json.loads(arquivos[-1].read_text(encoding="utf-8"))
    ontem = json.loads(arquivos[-2].read_text(encoding="utf-8")) if len(arquivos) > 1 else None
    return arquivos[-1], hoje, (arquivos[-2].stem if len(arquivos) > 1 else None), ontem


def indexar(snap):
    """post_id -> (engajamento ponderado, handle)"""
    idx = {}
    if not snap:
        return idx
    for handle, conta in snap.get("contas", {}).items():
        for p in conta.get("posts", []):
            eng, _ = engajamento(p)
            idx[p["id"]] = eng
    return idx


def main():
    caminho_hoje, hoje, data_ontem, ontem = snapshots()
    t_hoje = ler_ts(hoje.get("coletado_em")) or agora()
    t_ontem = ler_ts(ontem.get("coletado_em")) if ontem else None
    horas_entre = ((t_hoje - t_ontem).total_seconds() / 3600) if t_ontem else None

    anterior = indexar(ontem)
    seguidores_ontem = {
        h: c.get("followers_count") for h, c in (ontem or {}).get("contas", {}).items()
    }

    contas_saida = {}
    posts = []

    for handle, conta in hoje.get("contas", {}).items():
        seguidores = conta.get("followers_count") or 0
        tier = conta.get("tier", "traducao")
        brutos = conta.get("posts", [])

        # Mediana da conta: só posts maduros, para a régua não afundar.
        base = []
        for p in brutos:
            ts = ler_ts(p.get("timestamp"))
            if not ts:
                continue
            idade_h = (t_hoje - ts).total_seconds() / 3600
            if IDADE_MIN_BASELINE_H <= idade_h <= IDADE_MAX_BASELINE_D * 24:
                eng, _ = engajamento(p)
                base.append(eng)
        mediana = statistics.median(base) if len(base) >= 3 else None

        fo = seguidores_ontem.get(handle)
        contas_saida[handle] = {
            "tier": tier,
            "seguidores": seguidores,
            "delta_seguidores_24h": (seguidores - fo) if (fo and seguidores) else None,
            "mediana_engajamento": mediana,
            "posts_na_base": len(base),
            "posts_coletados": len(brutos),
            "er_mediano": (mediana / seguidores) if (mediana and seguidores) else None,
        }

        for p in brutos:
            ts = ler_ts(p.get("timestamp"))
            eng, ocultas = engajamento(p)
            idade_h = ((t_hoje - ts).total_seconds() / 3600) if ts else None

            eng_ontem = anterior.get(p["id"])
            delta = (eng - eng_ontem) if eng_ontem is not None else None
            # Normaliza o ganho para taxa de 24h — a coleta nunca cai no mesmo minuto.
            delta_24h = (delta / horas_entre * 24) if (delta is not None and horas_entre) else None

            posts.append({
                "id": p["id"],
                "handle": handle,
                "tier": tier,
                "permalink": p.get("permalink"),
                "tipo": p.get("media_type"),
                "publicado_em": p.get("timestamp"),
                "idade_h": round(idade_h, 1) if idade_h is not None else None,
                "curtidas": p.get("like_count"),
                "comentarios": p.get("comments_count"),
                "curtidas_ocultas": ocultas,
                "engajamento": eng,
                "ipr": round(eng / mediana, 2) if mediana else None,
                "delta_24h": round(delta_24h, 1) if delta_24h is not None else None,
                "velocidade": round(delta_24h / mediana, 2) if (delta_24h is not None and mediana) else None,
                "novo": eng_ontem is None and ontem is not None,
                "legenda": (p.get("caption") or "").strip(),
            })

    def maduro(p):
        return (
            p["idade_h"] is not None
            and IDADE_MIN_RANKING_H <= p["idade_h"] <= IDADE_MAX_RANKING_D * 24
        )

    top_ipr = sorted(
        [p for p in posts if maduro(p) and p["ipr"] and p["tier"] != "casa"],
        key=lambda p: p["ipr"], reverse=True,
    )[:40]

    top_velocidade = sorted(
        [p for p in posts if p["velocidade"] is not None and p["tier"] != "casa"],
        key=lambda p: p["velocidade"], reverse=True,
    )[:30]

    recem = sorted(
        [p for p in posts if p["idade_h"] is not None and p["idade_h"] <= 30 and p["tier"] != "casa"],
        key=lambda p: p["engajamento"], reverse=True,
    )[:30]

    casa = sorted(
        [p for p in posts if p["tier"] == "casa" and p["idade_h"] is not None and p["idade_h"] <= 14 * 24],
        key=lambda p: p["publicado_em"] or "", reverse=True,
    )

    saida = {
        "data": caminho_hoje.stem,
        "coletado_em": hoje.get("coletado_em"),
        "comparado_com": data_ontem,
        "horas_entre_coletas": round(horas_entre, 1) if horas_entre else None,
        "primeira_coleta": ontem is None,
        "falhas": hoje.get("falhas", {}),
        "peso_comentario": PESO_COMENTARIO,
        "contas": contas_saida,
        "ranking_desempenho": top_ipr,
        "ranking_velocidade": top_velocidade,
        "publicados_ultimas_30h": recem,
        "swisz": casa,
        "todos_os_posts": posts,
    }

    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / ("%s.json" % saida["data"])).write_text(
        json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (SAIDA / ("%s.md" % saida["data"])).write_text(digesto(saida), encoding="utf-8")
    print("consolidado: dados/consolidado/%s.json e .md" % saida["data"])
    print("%d posts | %d contas | comparação com %s" % (
        len(posts), len(contas_saida), data_ontem or "— (primeira coleta)"))
    return 0


def linha(p, metrica):
    legenda = " ".join(p["legenda"].split())
    if len(legenda) > 320:
        legenda = legenda[:320] + "…"
    valor = {
        "ipr": "IPR %.2f" % p["ipr"] if p["ipr"] else "IPR —",
        "vel": "vel %.2f" % p["velocidade"] if p["velocidade"] is not None else "vel —",
        "eng": "eng %d" % p["engajamento"],
    }[metrica]
    extra = " · NOVO" if p.get("novo") else ""
    return (
        "- **@%s** [%s] · %s · %s · %sh · %s curtidas / %s comentários%s\n"
        "  %s\n  %s\n"
    ) % (
        p["handle"], p["tier"], valor, p["tipo"] or "?",
        int(p["idade_h"]) if p["idade_h"] is not None else "?",
        p["curtidas"] if p["curtidas"] is not None else "ocultas",
        p["comentarios"], extra, legenda or "_(sem legenda)_", p["permalink"] or "",
    )


def digesto(s):
    L = []
    L.append("# Digesto da coleta — %s\n" % s["data"])
    if s["primeira_coleta"]:
        L.append(
            "> **Primeira coleta.** Não há dia anterior para comparar, então não\n"
            "> existe velocidade nem leitura de subindo/esfriando. Este relatório\n"
            "> só descreve o estado atual. A leitura de trajetória começa amanhã.\n"
        )
    else:
        L.append("Comparado com **%s** (%.1fh de intervalo). Peso do comentário: %dx.\n"
                 % (s["comparado_com"], s["horas_entre_coletas"] or 0, s["peso_comentario"]))

    if s["falhas"]:
        L.append("\n## Contas que não retornaram\n")
        for h, r in s["falhas"].items():
            L.append("- @%s — %s: %s\n" % (h, r["status"], (r.get("detalhe") or "")[:160]))

    L.append("\n## Painel\n\n| conta | tier | seguidores | Δ24h | mediana eng. | posts |\n")
    L.append("|---|---|---|---|---|---|\n")
    for h, c in sorted(s["contas"].items(), key=lambda kv: -(kv[1]["seguidores"] or 0)):
        L.append("| @%s | %s | %s | %s | %s | %d |\n" % (
            h, c["tier"],
            "{:,}".format(c["seguidores"]).replace(",", ".") if c["seguidores"] else "—",
            ("+%d" % c["delta_seguidores_24h"]) if c["delta_seguidores_24h"] is not None else "—",
            int(c["mediana_engajamento"]) if c["mediana_engajamento"] else "—",
            c["posts_coletados"],
        ))

    L.append("\n## Maior desempenho relativo (IPR) — o que rendeu acima da própria régua\n\n")
    for p in s["ranking_desempenho"][:25]:
        L.append(linha(p, "ipr"))

    if not s["primeira_coleta"]:
        L.append("\n## Maior velocidade nas últimas 24h — o que está esquentando agora\n\n")
        for p in s["ranking_velocidade"][:20]:
            L.append(linha(p, "vel"))

    L.append("\n## Publicado nas últimas 30h\n\n")
    for p in s["publicados_ultimas_30h"][:20]:
        L.append(linha(p, "eng"))

    if s["swisz"]:
        L.append("\n## Swisz — últimas publicações (linha de base da casa)\n\n")
        for p in s["swisz"][:12]:
            L.append(linha(p, "ipr"))

    return "".join(L)


if __name__ == "__main__":
    sys.exit(main())
