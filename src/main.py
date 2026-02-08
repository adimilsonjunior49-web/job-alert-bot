from datetime import datetime, timezone, timedelta

from src.sources.jooble import fetch_jooble
from src.sources.infojobs import fetch_infojobs
from src.sources.gupy import fetch_gupy
from src.filters import is_match
from src.dedupe import SeenStore
from src.telegram import send_message
from src.normalize import normalize_job

RECENT_HOURS = 72  # ajuste: 24/48/72

def format_job(job: dict) -> str:
    lines = [
        f"🔔 *{job['title'][:180]}*",
        f"🏢 {job.get('company','(não informado)')}",
        f"📍 {job.get('location','(não informado)')} | {job.get('work_model','(não informado)')}",
        f"🧾 Regime: {job.get('employment_type','(não informado)')}",
        f"🕒 Publicada: {job.get('posted_at','(não informado)')}",
        "",
        f"🧠 Filtro: {job.get('match_reason','')}",
        "",
        f"🔗 {job.get('url','')}",
    ]
    return "\n".join(lines)

def main():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=RECENT_HOURS)

    seen = SeenStore("data/seen.json")

    raw_jobs: list[dict] = []
    raw_jobs += fetch_jooble(cutoff=cutoff)
    raw_jobs += fetch_infojobs(cutoff=cutoff)
    raw_jobs += fetch_gupy(cutoff=cutoff)

    jobs = [normalize_job(j) for j in raw_jobs]

    new_hits = []
    for job in jobs:
        if not is_match(job):
            continue
        if seen.has(job["job_key"]):
            continue
        seen.add(job["job_key"])
        new_hits.append(job)

    # Ordena para ficar mais previsível (título/empresa)
    new_hits.sort(key=lambda x: (x.get("company",""), x.get("title","")))

    if new_hits:
        # Limite para evitar flood
        for job in new_hits[:25]:
            send_message(format_job(job))
        if len(new_hits) > 25:
            send_message(f"📌 Mais {len(new_hits)-25} vagas encontradas (limite de envio por rodada).")
    # se vazio, fica silencioso

    seen.save()

if __name__ == "__main__":
    main()
