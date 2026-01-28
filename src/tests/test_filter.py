import time
from types import SimpleNamespace
from filecleanup.main import filter

def test_filter_dry_run(tmp_path, capsys):
    f = tmp_path / "a.txt"
    f.write_text("hello")

    args = SimpleNamespace(
        drymode=True,
        lgt=None,
        smt=None,
        ot=None
    )

    result = filter([f], args)

    captured = capsys.readouterr()
    assert "DRY-RUN" in captured.out
    assert result is None

def test_filter_size_constraints(tmp_path):
    small = tmp_path / "small.txt"
    big = tmp_path / "big.txt"

    small.write_text("a")
    big.write_text("a" * 1000)

    args = SimpleNamespace(
        drymode=False,
        lgt=10,
        smt=2000,
        ot=None
    )

    result = filter([small, big], args)
    assert big in result
    assert small not in result
