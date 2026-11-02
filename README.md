# Template Quatre-Cinquième

![CI](https://github.com/pekosmaggle/quatre-cinquieme-template/actions/workflows/ci.yml/badge.svg)

Template de projet Python pour les missions d'automatisation IA de Quatre-Cinquième.

## Contenu

- Gestion du projet avec [uv](https://docs.astral.sh/uv/)
- Lint et formatage avec ruff, typage strict avec mypy, tests avec pytest
- Client Claude minimal (`llm.py`) : clé API par variable d'environnement, réessais automatiques, logging
- CI GitHub Actions à chaque push

## Démarrage

```bash
uv sync
export ANTHROPIC_API_KEY="..."
```

## Vérifications

```bash
uv run ruff check
uv run ruff format --check
uv run mypy src
uv run pytest
```
