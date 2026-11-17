"""Testes que não chamam a API (não gastam cota). Rode com: python -m pytest"""

import pytest

from src import config


def _isolar(monkeypatch, tmp_path):
    """Aponta o config para uma pasta vazia e remove a chave do ambiente."""
    monkeypatch.setattr(config, "BASE_DIR", tmp_path)
    monkeypatch.setattr(config, "ENV_PATH", tmp_path / ".env")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)


def test_prompt_existe_e_nao_esta_vazio():
    prompt = config.load_prompt()
    assert len(prompt) > 50
    assert "SENAI" in prompt


def test_sem_chave_gera_erro_claro(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="Chave da API"):
        config.get_api_key()


def test_chave_de_exemplo_e_rejeitada(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "sua_chave_aqui")
    with pytest.raises(RuntimeError):
        config.get_api_key()


def test_chave_valida_e_aceita(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "abc123")
    assert config.get_api_key() == "abc123"


def test_chave_com_aspas_e_aceita(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", '"abc123"')
    assert config.get_api_key() == "abc123"


def test_diagnostico_quando_env_nao_existe(monkeypatch, tmp_path):
    _isolar(monkeypatch, tmp_path)
    with pytest.raises(RuntimeError, match="não existe"):
        config.get_api_key()


def test_diagnostico_chave_colada_no_env_example(monkeypatch, tmp_path):
    _isolar(monkeypatch, tmp_path)
    (tmp_path / ".env.example").write_text("GEMINI_API_KEY=ABC123\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="env.example"):
        config.get_api_key()


def test_diagnostico_env_salvo_como_txt(monkeypatch, tmp_path):
    _isolar(monkeypatch, tmp_path)
    (tmp_path / ".env.txt").write_text("GEMINI_API_KEY=ABC123\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match=r"\.env\.txt"):
        config.get_api_key()


def test_diagnostico_variavel_com_nome_errado(monkeypatch, tmp_path):
    _isolar(monkeypatch, tmp_path)
    (tmp_path / ".env").write_text("GEMINI_KEY=abc\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="GEMINI_KEY"):
        config.get_api_key()
