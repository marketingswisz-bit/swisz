#!/usr/bin/env python3
"""Coleta diária de posts públicos dos perfis monitorados.

Usa o endpoint business_discovery da Instagram Graph API, que é a única via
oficial de ler dados públicos de outra conta. Restrições da API que moldam
este script:

  - a conta que consulta precisa ser Business/Creator ligada a uma Página do
    Facebook, e o token precisa de instagram_basic + pages_read_engagement;
  - a conta consultada também precisa ser Business/Creator. Conta pessoal não
    é retornada, mesmo pública;
  - não existe contagem de visualização/reprodução em business_discovery.
    O sinal de engajamento disponível é curtida + comentário;
  - limite de 200 chamadas por hora por conta consultada. Fazemos 1 por dia.

Saída: dados/brutos/AAAA-MM-DD.json — um retrato do painel no instante da
coleta. Nada é interpretado aqui. Interpretação é do consolidar.py.

Variáveis de ambiente:
  IG_TOKEN        token de acesso de longa duração (obrigatório)
  IG_USER_ID      ID da conta Instagram Business que faz a consulta (obrigatório)
  IG_API_VERSION  opcional; se ausente, tenta versões recentes em ordem
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = RAIZ / "monitoramento" / "contas.yml"
SAIDA = RAIZ / "dados" / "brutos"

VERSOES = ["v23.0", "v22.0", "v21.0", "v20.0", "v19.0"]

# Ordem importa: o degrade tira do fim para o começo quando a API recusa campo.
CAMPOS_MIDIA = [
    "id",
    "caption",
    "like_count",
    "comments_count",
    "media_type",
    "permalink",
    "timestamp",
    "media_url",
    "thumbnail_url",
]
CAMPOS_PERFIL = ["username", "followers_count", "media_count", "biography", "website"]


def erro_da_api(corpo):
    try:
        return json.loads(corpo).get("error", {})
    except Exception:
        return {}


def chamar(versao, ig_user_id, token, handle, campos_midia, campos_perfil, limite):
    sub = "{" + ",".join(campos_perfil) + ",media.limit(%d){%s}}" % (
        limite,
        ",".join(campos_midia),
    )
    fields = "business_discovery.username(%s)%s" % (handle, sub)
    url = "https://graph.facebook.com/%s/%s?%s" % (
        versao,
        ig_user_id,
        urllib.parse.urlencode({"fields": fields, "access_token": token}),
    )
    req = urllib.request.Request(url, headers={"User-Agent": "swisz-monitor/1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, erro_da_api(e.read().decode("utf-8", "replace"))
    except Exception as e:  # rede, DNS, timeout
        return None, {"message": str(e), "type": "TransportError"}


def campo_recusado(err):
    """Devolve o nome do campo que a API recusou, quando ela diz qual."""
    msg = (err.get("message") or "") + " " + (err.get("error_user_msg") or "")
    for campo in CAMPOS_MIDIA + CAMPOS_PERFIL:
        if ("field '%s'" % campo) in msg or ('"%s"' % campo) in msg:
            if "nonexisting" in msg or "does not exist" in msg or "not supported" in msg:
                return campo
    return None


def buscar_conta(estado, handle, limite):
    """Uma conta, com degrade de campo e de versão. Nunca levanta exceção."""
    campos_midia = list(estado["campos_midia"])
    campos_perfil = list(estado["campos_perfil"])
    tentativas_rede = 0
    tentativas_limite = 0

    for _ in range(len(CAMPOS_MIDIA) + len(CAMPOS_PERFIL) + 6):
        dados, err = chamar(
            estado["versao"], estado["ig_user_id"], estado["token"],
            handle, campos_midia, campos_perfil, limite,
        )

        if dados is not None:
            # Campos que sobreviveram viram o padrão das próximas contas.
            estado["campos_midia"] = campos_midia
            estado["campos_perfil"] = campos_perfil
            bd = dados.get("business_discovery")
            if not bd:
                return {"status": "sem_retorno", "detalhe": "resposta sem business_discovery"}
            return {"status": "ok", "perfil": bd}

        codigo = err.get("code")
        sub = err.get("error_subcode")
        msg = err.get("message", "")

        # Versão de API inválida: desce uma.
        if "Unsupported get request" in msg and "version" in msg.lower():
            prox = proxima_versao(estado)
            if prox:
                continue
            return {"status": "erro", "detalhe": msg}

        # Campo inexistente: tira e tenta de novo.
        campo = campo_recusado(err)
        if campo:
            if campo in campos_midia and len(campos_midia) > 3:
                campos_midia.remove(campo)
                continue
            if campo in campos_perfil and len(campos_perfil) > 2:
                campos_perfil.remove(campo)
                continue

        # Handle não existe, ou existe e não é Business/Creator.
        if codigo == 110 or sub == 2207013 or "does not exist" in msg or "Invalid user id" in msg:
            return {"status": "invalida", "detalhe": msg or "handle não resolve"}
        if sub in (2207041, 2207042) or "not a Business" in msg or "Business Account" in msg:
            return {"status": "nao_business", "detalhe": msg}

        # Limite de chamada da API: vale esperar, mas só duas vezes.
        if codigo in (4, 17, 32, 613):
            tentativas_limite += 1
            if tentativas_limite > 2:
                return {"status": "limite", "detalhe": msg}
            time.sleep(20)
            continue

        # Rede fora do ar: duas tentativas e desiste. Sem isso, um ambiente sem
        # saída de rede prende a coleta por minutos em cada conta do painel.
        if err.get("type") == "TransportError":
            tentativas_rede += 1
            if tentativas_rede > 2:
                return {"status": "sem_rede", "detalhe": msg}
            time.sleep(3)
            continue

        return {"status": "erro", "detalhe": msg or json.dumps(err)[:300]}

    return {"status": "erro", "detalhe": "excedeu tentativas de degrade"}


def proxima_versao(estado):
    try:
        i = VERSOES.index(estado["versao"])
    except ValueError:
        return None
    if i + 1 < len(VERSOES):
        estado["versao"] = VERSOES[i + 1]
        return estado["versao"]
    return None


def main():
    token = os.environ.get("IG_TOKEN", "").strip()
    ig_user_id = os.environ.get("IG_USER_ID", "").strip()
    if not token or not ig_user_id:
        print(
            "FALTA CREDENCIAL: defina IG_TOKEN e IG_USER_ID.\n"
            "Sem isso não há coleta. Veja monitoramento/README.md.",
            file=sys.stderr,
        )
        return 2

    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    limite = int(cfg.get("posts_por_conta", 25))
    contas = [c for c in cfg["contas"] if c.get("status") != "invalida"]

    estado = {
        "versao": os.environ.get("IG_API_VERSION") or VERSOES[0],
        "ig_user_id": ig_user_id,
        "token": token,
        "campos_midia": list(CAMPOS_MIDIA),
        "campos_perfil": list(CAMPOS_PERFIL),
    }

    agora = datetime.now(timezone.utc)
    resultado = {
        "coletado_em": agora.isoformat(),
        "versao_api": None,
        "campos_midia": None,
        "contas": {},
        "falhas": {},
    }

    for conta in contas:
        handle = conta["handle"]
        r = buscar_conta(estado, handle, limite)
        if r["status"] == "ok":
            perfil = r["perfil"]
            resultado["contas"][handle] = {
                "tier": conta.get("tier", "traducao"),
                "nota": conta.get("nota", ""),
                "followers_count": perfil.get("followers_count"),
                "media_count": perfil.get("media_count"),
                "biography": perfil.get("biography", ""),
                "posts": (perfil.get("media") or {}).get("data", []),
            }
            print("ok      %-28s %s posts" % (handle, len(resultado["contas"][handle]["posts"])))
        else:
            resultado["falhas"][handle] = r
            print("FALHA   %-28s %s — %s" % (handle, r["status"], r.get("detalhe", "")[:120]))
        time.sleep(1)

    resultado["versao_api"] = estado["versao"]
    resultado["campos_midia"] = estado["campos_midia"]

    # Coleta que não trouxe nada não vira snapshot. Um arquivo vazio em
    # dados/brutos/ passaria a ser o "ontem" da próxima rodada e destruiria a
    # comparação — todo post apareceria como novo e toda velocidade, inventada.
    if not resultado["contas"]:
        motivos = sorted({r["status"] for r in resultado["falhas"].values()})
        print(
            "\nNENHUMA CONTA RETORNOU (%s). Snapshot não gravado, para não\n"
            "corromper a comparação de amanhã." % ", ".join(motivos),
            file=sys.stderr,
        )
        return 1

    SAIDA.mkdir(parents=True, exist_ok=True)
    destino = SAIDA / ("%s.json" % agora.strftime("%Y-%m-%d"))
    destino.write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8"
    )
    print("\nsnapshot: %s" % destino.relative_to(RAIZ))

    marcar_invalidas(cfg, resultado["falhas"])
    podar(int(cfg.get("retencao_dias_bruto", 90)))
    return 0


def marcar_invalidas(cfg, falhas):
    """Handle que não resolve vira status: invalida no contas.yml, com o motivo.

    Só mexe em conta 'a_validar'. Conta confirmada pela Swisz falha em silêncio
    no arquivo e aparece no relatório — quem decide tirar é a pessoa, não o script.
    """
    mudou = False
    texto = CONFIG.read_text(encoding="utf-8")
    for handle, r in falhas.items():
        if r["status"] not in ("invalida", "nao_business"):
            continue
        conta = next((c for c in cfg["contas"] if c["handle"] == handle), None)
        if not conta or conta.get("status") != "a_validar":
            continue
        alvo = "  - handle: %s\n" % handle
        if alvo not in texto:
            continue
        bloco_antigo = "    status: a_validar"
        i = texto.index(alvo)
        j = texto.index(bloco_antigo, i)
        motivo = "handle não existe" if r["status"] == "invalida" else "não é conta Business/Creator"
        texto = texto[:j] + "    status: invalida  # %s (coleta de %s)" % (
            motivo, datetime.now(timezone.utc).strftime("%d/%m/%Y")
        ) + texto[j + len(bloco_antigo):]
        mudou = True
        print("contas.yml: %s marcada invalida (%s)" % (handle, motivo))
    if mudou:
        CONFIG.write_text(texto, encoding="utf-8")


def podar(dias):
    arquivos = sorted(SAIDA.glob("*.json"))
    for f in arquivos[:-dias] if len(arquivos) > dias else []:
        f.unlink()
        print("podado: %s" % f.name)


if __name__ == "__main__":
    sys.exit(main())
