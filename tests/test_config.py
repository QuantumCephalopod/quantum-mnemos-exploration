import json
import pathlib


def test_load_claude_config():
    config_path = pathlib.Path(__file__).resolve().parents[1] / "config" / "claude_desktop_config.template.json"
    with config_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert "mcpServers" in data
