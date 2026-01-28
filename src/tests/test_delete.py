from filecleanup.main import deleteFiles

def test_delete_files(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"

    f1.write_text("x")
    f2.write_text("y")

    deleteFiles([f1, f2])

    assert not f1.exists()
    assert not f2.exists()
