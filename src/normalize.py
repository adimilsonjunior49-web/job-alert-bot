import hashlib

def make_job_key(source: str, external_id: str | None, url: str | None) -> str:
    raw = f"{source}::{external_id or ''}::{url or ''}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()

def normalize_job(job: dict) -> dict:
    """
    Normaliza formato mínimo para o pipeline.
    Campos esperados:
      - source, external_id, url
      - title, company, location, work_model, employment_type
      - posted_at (string ISO ou legível)
      - description (texto)
    """
    source = job.get("source", "unknown")
    external_id = job.get("external_id")
    url = job.get("url")

    job["job_key"] = make_job_key(source, external_id, url)
    job.setdefault("title", "")
    job.setdefault("company", "")
    job.setdefault("location", "")
    job.setdefault("work_model", "")
    job.setdefault("employment_type", "")
    job.setdefault("posted_at", "")
    job.setdefault("description", "")
    return job
