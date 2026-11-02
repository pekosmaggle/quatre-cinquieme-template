"""Tests du client Claude, sans appel réel à l'API."""

from unittest.mock import MagicMock

import pytest
from anthropic.types import TextBlock

from quatre_cinquieme_template.llm import DEFAULT_MODEL, MissingApiKeyError, ask, get_client


def make_fake_client(content: list[object]) -> MagicMock:
    """Crée un faux client qui renvoie le contenu donné."""
    client = MagicMock()
    client.messages.create.return_value = MagicMock(content=content)
    return client


def test_ask_renvoie_le_texte_de_la_reponse() -> None:
    client = make_fake_client([TextBlock(type="text", text="Bonjour Martin")])

    result = ask("Dis bonjour", client=client)

    assert result == "Bonjour Martin"


def test_ask_envoie_le_bon_modele_et_le_bon_prompt() -> None:
    client = make_fake_client([TextBlock(type="text", text="ok")])

    ask("Mon prompt", client=client)

    kwargs = client.messages.create.call_args.kwargs
    assert kwargs["model"] == DEFAULT_MODEL
    assert kwargs["messages"] == [{"role": "user", "content": "Mon prompt"}]


def test_ask_ignore_les_blocs_qui_ne_sont_pas_du_texte() -> None:
    autre_bloc = MagicMock()
    client = make_fake_client([autre_bloc, TextBlock(type="text", text="seulement ceci")])

    assert ask("test", client=client) == "seulement ceci"


def test_get_client_echoue_sans_cle_api(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(MissingApiKeyError):
        get_client()
