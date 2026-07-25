from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_homepage_mounts_workspace_selector_behavior_without_owning_styles():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    script = (ROOT / "workspace-selector.js").read_text(encoding="utf-8")

    assert 'data-semax-workspace-selector' in html
    assert '<script src="workspace-selector.js"></script>' in html
    assert 'https://auth.ideanexusventures.com' in script
    assert 'semax:workspace-selected' in script
    assert 'innerHTML' not in script
    assert 'style.' not in script
