"""Tests for the symmetry-axis and pore-verdict helpers in hole_scan (no HOLE binary needed)."""
import numpy as np
import pytest

mda = pytest.importorskip("MDAnalysis")
import hole_scan as hs


def _write_pdb(path, chains):
    """Write a C-alpha-only PDB; ``chains`` maps chain id -> (n, 3) coordinates."""
    lines, serial = [], 1
    for chain, coords in chains.items():
        for res, (x, y, z) in enumerate(coords, 1):
            lines.append(
                f"ATOM  {serial:5d}  CA  ALA {chain}{res:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C"
            )
            serial += 1
    path.write_text("\n".join(lines) + "\nEND\n")
    return str(path)


def _ring(n_chains, radius=15.0):
    """n chains with 4 C-alpha atoms each, placed symmetrically around the z axis."""
    chains = {}
    for i in range(n_chains):
        angle = 2 * np.pi * i / n_chains
        centre = np.array([radius * np.cos(angle), radius * np.sin(angle), 0.0])
        offsets = np.array([[0, 0, -10.0], [0, 0, -3.0], [0, 0, 3.0], [0, 0, 10.0]])
        chains["ABCDEF"[i]] = centre + offsets
    return chains


@pytest.mark.parametrize("order", [3, 4, 6])
def test_axis_of_a_ring_is_the_ring_normal(tmp_path, order):
    universe = mda.Universe(_write_pdb(tmp_path / "ring.pdb", _ring(order)))
    centre, axis = hs.symmetry_axis(universe)
    assert np.allclose(centre, [0, 0, 0], atol=1e-3)
    assert np.isclose(abs(axis[2]), 1.0, atol=1e-6)
    assert np.isclose(np.linalg.norm(axis), 1.0)


def test_axis_of_a_dimer_follows_the_long_axis(tmp_path):
    chains = {"A": np.array([[x, 0.0, 0.0] for x in (-20.0, -10.0, 0.0)]),
              "B": np.array([[x, 0.5, 0.0] for x in (0.0, 10.0, 20.0)])}
    universe = mda.Universe(_write_pdb(tmp_path / "dimer.pdb", chains))
    _, axis = hs.symmetry_axis(universe)
    assert np.isclose(abs(axis[0]), 1.0, atol=1e-2)


@pytest.mark.parametrize(
    "radius, expected",
    [(2.0, "OPEN(water)"), (1.15, "OPEN(water)"), (1.1, "Na+only"), (1.0, "Na+only"), (0.4, "OCCLUDED")],
)
def test_verdict_thresholds(radius, expected):
    assert hs.verdict(radius) == expected
