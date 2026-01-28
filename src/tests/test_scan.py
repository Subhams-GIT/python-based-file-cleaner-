import pathlib
from filecleanup.main import scan1, scan2

def create_files(base: pathlib.Path):
    (base / "a.txt").write_text("hello")
    (base / "b.py").write_text("print('hi')")
    sub = base / "sub"
    sub.mkdir()
    (sub / "c.py").write_text("print('sub')")
    (sub / "d.jpg").write_text("img")

def test_scan1_only_level1(tmp_path):
    create_files(tmp_path)

    ignored = set()
    exts = [".py"]

    result = scan1(tmp_path, ignored, exts)

    names = {p.name for p in result}
    assert "b.py" in names
    assert "a.txt" not in names
    assert "c.py" not in names  # scan1 should NOT go deeper

def test_scan2_two_levels(tmp_path):
    create_files(tmp_path)

    ignored = set()
    exts = [".py"]

    result = scan2(tmp_path, ignored, exts)

    names = {p.name for p in result}
    assert "b.py" in names
    assert "c.py" in names
    assert "a.txt" not in names

def test_scan2_all_files(tmp_path):
    create_files(tmp_path)

    ignored = set()
    exts = [None]

    result = scan2(tmp_path, ignored, exts)

    names = {p.name for p in result}
    assert {"a.txt", "b.py", "c.py", "d.jpg"} <= names
