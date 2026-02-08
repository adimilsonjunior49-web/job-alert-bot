import os
import requests
from datetime import datetime

def _has_creds() -> bool:
    return bool(os.environ.get("INFOJOBS_CLIENT_ID","").strip() and os.environ.get("INFOJOBS_CLIENT_SECRET","").strip())

def fetch_infojobs(cutoff: datetime) -> list[dict]:
    """
    InfoJobs API:
    - Exige fluxo OAuth/client credentials de acordo com sua conta.
    - Aqui deixamos um stub "pronto para ligar" quando você inserir o token/fluxo.
    Se não houver credenciais, retorna [].
    """
    if not _has_creds():
        return []

    # ⚠️ Implementação do auth varia conforme plano/credencial.
    # Coloque seu token obtido via OAuth aqui:
    token = os.environ.get("INFOJOBS_ACCESS_TOKEN", "").strip()
    if not token:
        # Sem token: não tenta.
        return []

    headers = {"Authorization": f"Bearer {token}"}

    # Endpoint ilustrativo — ajuste conforme sua doc/conta.
    # Você pode consultar por palavras-chave e local.
    params_list = [
        {"q": "analista sênior riscos", "city": "Brasil"},
        {"q": "coordenador seguros", "city": "Brasil"},
        {"q": "supervisor qualidade", "city": "São Paulo"},
        {"q": "gerente ESG", "city": "Brasil"},
    ]

    out = []
    for params in params_list:
        try:
            r = requests.get("https://api.infojobs.com.br/api/1/offer", headers=headers, params=params, timeout=45)
            if r.status_code >= 400:
                continue
            data = r.json()
            offers = data if isinstance(data, list) else data.get("offers", []) or []
            for o in offers:
                out.append({
                    "source": "infojobs",
                    "external_id": str(o.get("id") or ""),
                    "url": o.get("link") or "",
                    "title": o.get("title") or "",
                    "company": (o.get("company") or {}).get("name","") if isinstance(o.get("company"), dict) else (o.get("company") or ""),
                    "location": o.get("city") or "",
                    "work_model": o.get("contractType") or "",
                    "employment_type": o.get("contractType") or "",
                    "posted_at": o.get("published") or "",
                    "description": o.get("description") or "",
                })
        except Exception:
            continue

    return out
