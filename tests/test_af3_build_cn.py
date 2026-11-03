"""Tests for the AlphaFold3 homo-oligomer input builder."""
import json

import af3_build_cn as build
import pytest

SEQ = "MKQLLED"
CARRIED = {"unpairedMsa": ">q\nMKQLLED", "pairedMsa": "", "templates": []}


def test_build_input_names_and_chains_follow_the_order():
    entry = build.build_input(SEQ, CARRIED, order=4)
    protein = entry["sequences"][0]["protein"]
    assert entry["name"] == "nkg7_c4"
    assert protein["id"] == ["A", "B", "C", "D"]
    assert protein["sequence"] == SEQ
    assert entry["dialect"] == "alphafold3"


def test_build_input_carries_the_monomer_msa_unchanged():
    protein = build.build_input(SEQ, CARRIED, order=2)["sequences"][0]["protein"]
    for key, value in CARRIED.items():
        assert protein[key] == value


def test_find_monomer_data_prefers_the_named_file(tmp_path):
    (tmp_path / "x").mkdir()
    named = tmp_path / "x" / "nkg7_monomer_data.json"
    other = tmp_path / "x" / "other_data.json"
    named.write_text("{}")
    other.write_text("{}")
    assert build.find_monomer_data(str(tmp_path)) == str(named)


def test_find_monomer_data_fails_clearly_when_missing(tmp_path):
    with pytest.raises(FileNotFoundError, match="no monomer data JSON"):
        build.find_monomer_data(str(tmp_path))


def test_main_writes_c2_to_c6(tmp_path, monkeypatch):
    af_out = tmp_path / "af_out" / "x"
    af_out.mkdir(parents=True)
    monomer = {"sequences": [{"protein": {"id": "A", "sequence": SEQ, **CARRIED}}]}
    (af_out / "nkg7_monomer_data.json").write_text(json.dumps(monomer))
    out_dir = tmp_path / "af_in"
    monkeypatch.setattr("sys.argv", ["af3_build_cn.py", "--af-out", str(tmp_path / "af_out"), "--out-dir", str(out_dir)])
    build.main()
    written = sorted(p.name for p in out_dir.iterdir())
    assert written == [f"af3_C{n}.json" for n in range(2, 7)]
    c6 = json.loads((out_dir / "af3_C6.json").read_text())
    assert len(c6["sequences"][0]["protein"]["id"]) == 6
