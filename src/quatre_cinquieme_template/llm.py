"""Client minimal pour l'API Claude."""

import logging
import os

import anthropic
from anthropic.types import TextBlock

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-5-5"


class MissingApiKeyError(RuntimeError):
    """Levée quand la clé API n'est pas configurée."""


def get_client() -> anthropic.Anthropic:
    """Crée un client Claude à partir de la variable d'environnement."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise MissingApiKeyError("La variable ANTHROPIC_API_KEY n'est pas définie.")
    return anthropic.Anthropic(api_key=api_key, max_retries=3)


def ask(
    prompt: str,
    *,
    client: anthropic.Anthropic | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 1024,
) -> str:
    """Envoie un prompt à Claude et renvoie le texte de la réponse."""
    client = client or get_client()
    logger.info("Appel Claude (modèle=%s, prompt=%d caractères)", model, len(prompt))
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if isinstance(block, TextBlock))
