from src.shared.infra.core.settings import Settings


def test_settings_accept_log_level_override() -> None:
    settings = Settings(log_level="debug")

    assert settings.log_level == "debug"
