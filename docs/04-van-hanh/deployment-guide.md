# Deployment & Runbook Guide

## 1. Local Development Infrastructure
```bash
docker compose up -d
```
Services started:
- PostgreSQL on port `5432`
- Redis on port `6379`
- ChromaDB on port `8000`

## 2. Dev & Prod Deployment Rules (Two-Lane Pipeline)
- **Dev branch**: Manual deploy, feature branch testing.
- **Prod branch**: Deploy by git tag, strictly automated via GitHub Actions / CI pipeline. Always verify health check before routing traffic.

