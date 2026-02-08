import re

ROLE_PATTERNS = [
    r"\banalista s[eê]nior\b",
    r"\bcoordenador(a)?\b",
    r"\bsupervisor(a)?\b",
    r"\bgerente\b",
]

AREA_PATTERNS = [
    # Riscos e seguros (sem expandir para atuária/sinistros por padrão)
    r"\bgest[aã]o de risco(s)?\b",
    r"\brisco(s)?\b",
    r"\bseguro(s)?\b",
    r"\bcorretagem\b",
    # Qualidade
    r"\bqualidade\b",
    r"\bsgq\b",
    r"\biso 9001\b",
    # ESG
    r"\besg\b",
    r"\bsustentabil(idade|ty)\b",
]

SECTOR_PATTERNS = [
    r"\blog[ií]stica\b",
    r"\btransportadora(s)?\b",
    r"\bseguradora(s)?\b",
    r"\bcorretora(s)?\b",
]

CLT_PATTERNS = [
    r"\bclt\b",
    r"\bcarteira assinada\b",
    r"\bregime clt\b",
]

REMOTE_PATTERNS = [
    r"\bremoto\b",
    r"\bhome office\b",
    r"\b100% remoto\b",
    r"\bfully remote\b",
]

HYBRID_PATTERNS = [
    r"\bh[ií]brido\b",
    r"\bh[ií]brida\b",
]

ONSITE_PATTERNS = [
    r"\bpresencial\b",
]

SP_CITY_PATTERNS = [
    r"\bs[aã]o paulo\b",
    r"\bsao paulo\b",
]

def _any(patterns, text: str) -> bool:
    t = (text or "").lower()
    return any(re.search(p, t) for p in patterns)

def is_match(job: dict) -> bool:
    """
    Regra:
      - cargo/senioridade: analista sênior, coordenador, supervisor, gerente
      - área: riscos/seguro OR qualidade OR ESG (qualquer um já passa)
      - CLT
      - localidade:
          - remoto: Brasil inteiro
          - híbrido/presencial: apenas São Paulo (cidade)
    """
    text = " ".join([
        job.get("title",""),
        job.get("description",""),
        job.get("company",""),
        job.get("location",""),
        job.get("employment_type",""),
        job.get("work_model",""),
    ])

    if not _any(ROLE_PATTERNS, text):
        return False
    if not _any(AREA_PATTERNS, text):
        return False

    clt_ok = "clt" in (job.get("employment_type","") or "").lower() or _any(CLT_PATTERNS, text)
    if not clt_ok:
        return False

    work_model = (job.get("work_model") or "").lower()
    location = (job.get("location") or "").lower()

    is_remote = _any(REMOTE_PATTERNS, work_model) or _any(REMOTE_PATTERNS, text)
    is_hybrid = _any(HYBRID_PATTERNS, work_model) or _any(HYBRID_PATTERNS, text)
    is_onsite = _any(ONSITE_PATTERNS, work_model) or _any(ONSITE_PATTERNS, text)

    if is_remote:
        pass
    else:
        # presencial/híbrido somente São Paulo (cidade)
        if not (_any(SP_CITY_PATTERNS, location) or _any(SP_CITY_PATTERNS, text)):
            return False
        if not (is_hybrid or is_onsite):
            # se a fonte não informar work_model, assume não elegível
            return False

    sector_ok = _any(SECTOR_PATTERNS, text)
    job["match_reason"] = f"role+area+clt{' +setor' if sector_ok else ''}"
    return True
