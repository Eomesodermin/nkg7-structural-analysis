# Tier 0E — NKG7 Monomer Pore Analysis

## Method
Pore-radius profile computed along the membrane normal of the AlphaFold **monomer** models
(human Q16617, mouse Q99PA5), HOLE-style. The external HOLE binary and the `hole2` conda
package are not installable in this sandbox (not on any allowlisted conda channel; not on
PyPI), so a HOLE-equivalent **geometric probe-sphere** algorithm was used, which is the
method HOLE itself implements:

1. Load heavy atoms; assign Bondi van der Waals radii.
2. Define the membrane normal as the **long (principal) axis of the four-TM CA bundle**
   (TM helices res 9–29, 61–81, 92–112, 133–153); align this axis to *z*.
3. At each 0.5 Å slice along *z*, find the (x,y) point maximizing the largest sphere that
   fits without overlapping any atom's vdW surface (radius = min over atoms of |p−atom|−r_vdw),
   tethered within 8 Å of the bundle central axis so the search tracks a *connected* pathway
   rather than escaping into bulk solvent.
4. Pore radius = that maximal-sphere radius vs. axial position.

Reference radii: a single water needs a channel radius ≳ **1.15 Å**; a dehydrated Na⁺
needs ≳ **0.95–1.0 Å**; a fully hydrated cation needs ≳ **3 Å**.

## Results
| Species | TM span (Å) | Min pore radius in TM span (Å) | Position of constriction | Max radius in TM |
|---|---|---|---|---|
| Human (Q16617) | 40.5 | **0.65** | z = 15.9 | 3.08 |
| Mouse (Q99PA5) | 40.3 | **0.79** | z = -10.3 | 2.52 |

Fraction of TM-span slices with radius < 1.0 Å: human 17%, mouse 10%.

## Verdict
**No continuous through-membrane pore in the monomer.** In both species the narrowest
constriction inside the TM span is ~0.65–0.79 Å — below the ~1.15 Å a single water molecule
requires and below the ~1.0 Å a fully dehydrated Na⁺ requires. The radius stays under the
water threshold across a substantial fraction of the TM span. The four-TM bundle packs as a
closed helical bundle with no water-accessible axial channel; the wider values (>2 Å) occur
only at the membrane-boundary mouths, not through the core.

## Bearing on the channel hypothesis — the *informative negative*
This is the **expected result** and it is not evidence against the hypothesis. A single 4-TM
subunit almost never encloses its own conducting pore: essentially all tetraspan/4-TM ion
channels (and the Ca_V γ / claudin family NKG7 is placed in) build their permeation pathway
at the **interface between multiple subunits** (claudins line paracellular pores between
cells; connexins/innexins are hexameric; the pore of oligomeric channels sits on the symmetry
axis of the assembly). A monomer being occluded is therefore fully consistent with either
model — a real oligomeric channel OR a non-conducting regulatory subunit.

**What it implies for Tier 1:** the monomer analysis cannot discriminate the two hypotheses;
the decisive test is the **homo-oligomer prediction** (dimer → hexamer with symmetry). Re-run
this exact pore analysis on the predicted oligomer assemblies: if a continuous, appropriately
wide (≥~1–3 Å) axial pathway *opens at the subunit interfaces* upon oligomerization, that
would be computationally consistent with a conducting channel; if the interfaces remain
occluded even in a high-confidence (high ipTM) oligomer, that argues NKG7 is a regulatory /
scaffolding tetraspan rather than a pore. Proceed to Tier 1.

## Caveats
- Static AlphaFold monomer model; no membrane, no side-chain relaxation, no gating dynamics —
  a closed monomer state may not represent any physiological conducting state.
- Geometric probe-sphere (HOLE-equivalent), not the reference HOLE binary; the numeric
  constriction radii are approximate (±~0.2 Å) but the qualitative verdict (occluded, sub-water)
  is robust to that uncertainty.
- Membrane normal inferred from the TM-CA principal axis, not from an explicit bilayer fit.
