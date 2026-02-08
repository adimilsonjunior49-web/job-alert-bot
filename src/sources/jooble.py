import os
import requests
from datetime import datetime, timezone

def fetch_jooble(cutoff: datetime) -> list[dict]:
    """
    Jooble API (requer JOOBLE_API_KEY).
    Retorna lista de jobs no formato "raw" padronizado.
    Se não houver chave, retorna [].
    """
    key = os.environ.get("JOOBLE_API_KEY", "").strip()
    if not key:
        return []

    url = f"https://br.jooble.org/api/{key}"
    # Estratégia: consultas por combinações de termos para melhorar recall.
    queries = [
        "analista sênior riscos CLT remoto",
        "coordenador riscos seguros CLT",
        "supervisor qualidade SGQ CLT",
        "gerente ESG sustentabilidade CLT",
        "coordenador qualidade ISO 9001 CLT",
    ]

    out = []
    for q in queries:
        try:
            r = requests.post(url, json={"keywords": q, "location": "Brasil"}, timeout=45)
            r.raise_for_status()
            data = r.json()
            jobs = data.get("jobs", []) or []
            for j in jobs:
                # Jooble tende a retornar posted date como string; não confiamos sempre
                out.append({
                    "source": "jooble",
                    "external_id": j.get("id"),
                    "url": j.get("link"),
                    "title": j.get("title", ""),
                    "company": j.get("company", ""),
                    "location": j.get("location", ""),
                    "work_model": "",  # nem sempre vem
                    "employment_type": "",  # nem sempre vem
                    "posted_at": j.get("updated") or j.get("created") or "",
                    "description": j.get("snippet", "") or "",
                })
        except Exception:
            # fonte falhou: segue com as demais
            continue

    # Corte por recência: quando posted_at não é parseável, deixa passar (melhor recall)
    return out
