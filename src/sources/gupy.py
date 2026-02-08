import requests
from datetime import datetime

def fetch_gupy(cutoff: datetime) -> list[dict]:
    """
    Conector Gupy (best-effort).
    Algumas listagens são públicas via endpoints de consulta de vagas.
    Como a disponibilidade/rota pode variar, tratamos falhas com segurança.
    """
    out = []

    # Estratégia: buscar por palavras-chave gerais.
    # Ajuste conforme você identificar endpoints/empresas-alvo.
    keywords = [
        "riscos",
        "seguros",
        "qualidade",
        "esg",
    ]

    # Endpoint público de referência pode variar; mantemos robusto.
    # Se falhar, retorna [] sem quebrar o pipeline.
    for kw in keywords:
        try:
            # Exemplo comum de busca (pode precisar ajuste):
            # https://api.gupy.io/api/v1/jobs?name=...  (varia)
            r = requests.get("https://api.gupy.io/api/v1/jobs", params={"name": kw}, timeout=45)
            if r.status_code >= 400:
                continue
            data = r.json()
            jobs = data.get("data", []) if isinstance(data, dict) else data
            if not isinstance(jobs, list):
                continue

            for j in jobs:
                out.append({
                    "source": "gupy",
                    "external_id": str(j.get("id") or ""),
                    "url": j.get("careerPageUrl") or j.get("url") or "",
                    "title": j.get("name") or j.get("title") or "",
                    "company": (j.get("company") or {}).get("name","") if isinstance(j.get("company"), dict) else (j.get("company") or ""),
                    "location": (j.get("location") or {}).get("name","") if isinstance(j.get("location"), dict) else (j.get("location") or ""),
                    "work_model": j.get("workplaceType") or "",
                    "employment_type": j.get("employmentType") or "",
                    "posted_at": j.get("publishedDate") or j.get("createdAt") or "",
                    "description": j.get("description") or "",
                })
        except Exception:
            continue

    return out
