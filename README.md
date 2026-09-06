# LiftMix v3 — compact twist-crown powder cap

This is the printable engineering version of the newer flat-top concept. Hold the lower body and turn the outer crown about 90° clockwise, viewed from above. Two hidden cam tracks raise a captive cross pin and plug by 6 mm. Powder can then pass around the plug and through the 16 mm outlet. Turn the crown back to reseat the plug. The whole cap unscrews from the bottle for drinking access.

**Status: an unbuilt mechanical bench prototype.** The supplied meshes and nominal movement have been checked computationally. Bottle compatibility, operating force, powder flow, moisture protection, leakage, durability, and food-contact suitability have not been physically validated. A closed STL mesh does not establish a liquid-tight printed part. Use initial prints for dry operation and non-consumption tests with unpressurized water; this is not a carbonated-drink closure.

## Start here

1. Extract the ZIP. All STL dimensions are millimeters; import at 100% scale.
2. Print `stl/bottle_thread_coupon.stl` first and check it gently on the intended bottle. Its approximate thread is based on a nominal 28 mm PCO1881 neck. It is not a universal bottle thread or an exact reproduction of the supplied Karma cap.
3. If that fit is suitable, print the seven rigid parts and four soft seals below. Inspect the slicer preview, especially the small pin, guide slots, and cam channels.
4. Read the assembly sequence before loading any powder. Use the CAD sheet, assembly map, and motion clip in `visuals/` to identify the parts.

The optional `thread_test_receiver.stl` is a matching approximate neck on a catch cup. It is useful for mechanism demonstrations. Agreement between these two printed test pieces does not prove agreement with a commercial bottle.

## Size and powder capacity

| Property | Supplied v3 geometry |
|---|---:|
| Outside diameter | 46.2 mm |
| Overall height, closed or open | 54.6 mm |
| Crown rotation | Approximately 90° clockwise to open |
| Hidden plug travel | 6 mm |
| Powder outlet diameter | 16 mm |
| Main reservoir inside diameter | 35 mm |
| Calculated free volume below fill plane | 14.60 mL |
| Suggested initial test fill | At most 14 mL |
| Fill plane | 2 mm below the body's top rim |

The capacity calculation subtracts the plug, stem, and seated valve seal from the modeled chamber. It is geometric volume, not a measured discharge result. Leave the suggested headspace and keep the refill thread and sealing rim clear of powder.

**For 5 g creatine plus other powders:** weigh your actual 5 g portion and measure its loosely poured volume. Add other ingredients only if the combined volume stays within the 14 mL test fill. For example, if your particular 5 g portion occupies 9 mL, that leaves approximately 5 mL for other powders; 9 mL is an illustration, not a density claim. This device holds a weighed portion; it does not automatically meter 5 g.

This cap is still substantially larger than an ordinary water-bottle cap. The reservoir and concealed mechanism account for the added size.

## Parts and starting print settings

Print one of each required file. The supplied STLs are already oriented with their lowest surface at Z = 0. Separate material jobs are sufficient; a multi-material printer is not required.

| Required STL | Material for mechanical trials | Orientation in file / purpose |
|---|---|---|
| `body.stl` | PETG | Bottle opening down; reservoir and two threaded interfaces |
| `guide_lid.stl` | PETG | Inverted, guide tower down; stationary lid and stem guide |
| `twist_crown.stl` | PETG | Flat top down; contains both concealed cam tracks |
| `plunger.stl` | PETG | Flat plug face down; integral stem upright |
| `cross_pin.stl` | PETG | Pin axis upright; use a brim and print a spare |
| `lid_lock_key.stl` | PETG | Small key upright; use a brim and print a spare |
| `top_retainer.stl` | PETG | Flat slotted head down; holds crown on guide |
| `bottle_gasket_TPU.stl` | Flexible TPU | Flat; 26.8 mm OD × 21.3 mm ID × 1 mm |
| `lid_gasket_TPU.stl` | Flexible TPU | Flat; 37.3 mm OD × 35.2 mm ID × 1 mm |
| `valve_gasket_TPU.stl` | Flexible TPU | Flat; 22.4 mm OD × 16.5 mm ID × 1.5 mm |
| `stem_seal_TPU.stl` | Flexible TPU | Flat; nominal 6 mm ID × 1 mm round section |

Suggested starting settings for the rigid parts: 0.4 mm nozzle, 0.16–0.20 mm layers, four perimeters where the wall width permits, five top/bottom layers, and approximately 40% infill. Use solid infill for the pin, key, and retainer. These are starting points for a calibrated printer, not a validated process specification.

The inverted guide lid needs removable support under its wide plate, outside the guide tower. Keep support out of the stem bore, seal gland, and threaded surfaces. The inverted crown exposes its underside for cleanup. Inspect the rounded cam-slot roofs and small top shoulders in the slicer; short bridges may work on a tuned printer, but use locally removable support where your profile requires it. Do not fill the internal tracks with inaccessible support. The body also has a short overhang above its bottle-thread bore that needs a slicer check.

TPU 95A can be tried for the soft parts using solid infill and a slow, established flexible-filament profile. The tiny round stem seal is the most demanding print and may not seal reliably. A suitably specified stock elastomer ring can be used for later sealing experiments. The supplied all-plastic concept uses rigid polymer parts plus soft TPU polymer seals; it requires no metal spring, metal screw, or disposable foil.

PETG and TPU labels alone do not qualify a printed assembly for drinking use. Material formulation, printing equipment, layer porosity, cleaning, and seal performance still matter. See the food-contact printing reference below.

## Assembly sequence

First assemble empty. Remove support and loose strands, clean the threads and cam tracks, and check the moving surfaces by hand. Do not force a jam with tools.

1. **Fit the stem seal.** Flex the small TPU ring into the internal groove near the underside of `guide_lid`. Its center is 1.5 mm above the lid's underside. The round 6 mm shaft passes through this seal; use a blunt tool that will not cut it.
2. **Fit the valve washer.** Press `valve_gasket_TPU` into the shallow circular recess around the body's bottom outlet. It stays in the body. It does not attach to the moving plug. Its outside edge has a small nominal interference fit to help retain it.
3. **Seat the plunger.** Lower the plunger into the reservoir with its flat face on the valve washer and its stem pointing upward. The modeled closed position compresses the 1.5 mm washer to approximately 1.1 mm.
4. **Place the refill-lid gasket.** Lay `lid_gasket_TPU` on the top annular rim of the body. For a loaded assembly, add powder around the seated plunger now, keeping below the fill limit and keeping this rim and the threads clean.
5. **Install the guide lid.** Pass the stem through the lid's seal and screw the lid clockwise onto the body's coarse outer thread. Stop when the side key holes align and the rim gasket is seated. Nominal gasket compression is 0.25 mm. If the holes cannot align without excessive force, correct the printed fit or gasket thickness; do not force the key through misaligned holes.
6. **Insert the side key.** Push `lid_lock_key` into the aligned side hole until its head is within the lid's outside surface. It prevents the refill lid from turning with the crown. The crown will enclose it.
7. **Insert the cross pin.** Align the stem's cross-hole with the paired vertical guide slots. Slide the 22 mm plastic pin through and center it so both ends project equally. The cam ring captures its ends after the crown is installed.
8. **Install the crown in the closed position.** Align the two entry openings at the bottom of the cam ring with the two pin ends. The top radial index line is parallel to the pin axis. With the plug held gently on its seal, lower the crown over the guide and pin. It does not require opening the powder valve. A short index groove on the lower body's upper band marks the same closed direction.
9. **Install the top retainer.** Screw the flat center retainer clockwise into the guide. Use the coin slot gently. It seats on the fixed guide, leaving a nominal 0.2 mm axial running gap under its flange for the crown. If tightening it traps the crown, correct the mating print surfaces rather than leaving the retainer loose. It is a retainer, not the dosing control.
10. **Mount the cap.** Place the bottle gasket on the bottle lip and screw the complete cap on using the lower body. For a catch-cup trial, use the printed receiver. The bottle gasket is a loose prototype washer; check its location whenever the cap is removed.

All stated clearances and seal compressions are nominal CAD values. Printed dimensions, surface texture, seal stiffness, and backlash change them. Fine powder or water may still pass the seals even if the parts assemble.

## Operation and refill

- Hold the lower body steady. Turn the **outer crown**, not its center disk, approximately 90° clockwise viewed from above. The first and last 8° of the modeled tracks are flat dwells; the middle portion produces the lift. These are not spring detents.
- In the open position, the plug rises by 6 mm and the powder has a path into the bottle. Sticky or damp powders may bridge; flow has not been tested. Tap gently during dry bench trials if needed, and do not use excessive torque to clear a jam.
- Turn back to the closed index before an unpressurized water-leak trial. The cap can then serve as a screw-on closure in concept, but its leak resistance has not been established. Unscrew the entire cap by the lower body for bottle-mouth access.
- Refill by closing the valve, removing the whole cap, removing the center retainer, lifting the crown straight off in the closed orientation, removing the cross pin and side key, and unscrewing the guide lid. Clean and dry the parts fully before refilling. Keep the plunger seated while adding the next measured powder portion, then reassemble in the sequence above.

This prototype prioritizes a printable concealed mechanism. Refilling currently requires this disassembly; it has no separate quick-fill hatch.

## Files and CAD editing

| File or folder | Contents |
|---|---|
| `stl/` | 11 required part meshes and 2 optional thread test meshes |
| `LiftMix_v3.scad` | Generated, self-contained OpenSCAD CSG geometry; select a part or preview assembly motion |
| `source/build_compact.py` | Authoritative editable Python geometry, dimensions, exports, and clearance checks |
| `source/geometry_core.py` | Boolean geometry and mesh utilities |
| `source/make_visuals.py` | Exact CAD sections and animation generator |
| `LiftMix_v3_closed.glb`, `LiftMix_v3_open.glb` | Color 3D assemblies for compatible viewers |
| `visuals/LiftMix_v3_CAD.png` | Assembled view and closed/open sections |
| `visuals/LiftMix_v3_assembly.png` | Exploded section and part identification |
| `visuals/LiftMix_v3_motion.mp4` | 12-second CAD cutaway motion preview |
| `visuals/LiftMix_v3_motion.gif` | Animated image alternative to the MP4 |
| `validation.json` | Dimensions, mesh checks, sampled motion and insertion checks |

In OpenSCAD, set `part` to an individual STL name without its extension, render, and export STL. Set `part="assembly"` and vary `angle` from 0 to 90 to inspect the mechanism. The individual-part selections use the same print orientations as the supplied STL files. The CSG is generated with explicit dimensions. Make coordinated dimensional changes in the Python source, then regenerate the SCAD and STLs; mechanical changes can require updating multiple related dimensions.

To regenerate geometry:

```sh
python -m pip install numpy trimesh manifold3d
python source/build_compact.py
```

The build used Manifold3D 3.5.2, trimesh 5.1.0, and NumPy 2.5.2. Visual generation additionally needs Pillow and Matplotlib, system DejaVu Sans fonts, and FFmpeg:

```sh
python -m pip install pillow matplotlib
python source/make_visuals.py
```

The Python builder and exported STL meshes were executed and checked. The standalone OpenSCAD file was generated from the same CSG construction; an OpenSCAD render was not run in this environment. There is no STEP file in this package.

## What was checked

- Each of the 13 exported STL files is a single connected, closed mesh with consistent winding and positive volume, and its saved STL was read back to check closure.
- All 21 pairs of rigid cap components were checked at 37 nominal positions through the 90° motion. No rigid overlap was detected at those sampled positions.
- Bottle-thread engagement, refill-lid threading, and retainer threading were each checked at 25 insertion positions with matching rotation and axial travel.
- Crown installation over the closed valve and cross pin was checked at 21 axial positions.
- Capacity was calculated from the CAD solids. Seal deformation is represented only by nominal compressed geometry.

These are sampled geometric checks, not force, stress, particle-flow, fatigue, continuous-motion, or physical fit tests. The bottle neck is approximate. The supplied STLs have not been printed or sliced here. The cap's key, pin, polymer threads, and thin sealing features need physical evaluation. Check that the retainer remains seated during repeated operation.

## Reference basis

- Bottle-thread dimensional reference: [BOSL2 bottlecaps.scad](https://github.com/BelfrySCAD/BOSL2/blob/master/bottlecaps.scad), using its PCO1881-related dimensions as a starting reference. The helical mesh construction in this package is independently written.
- Neck-finish standards context: [ISBT thread specifications](https://www.isbt.com/resources/isbt-threadspecs). A nominal neck designation is not proof of closure fit or performance.
- Food-contact printing considerations: [Prusa — Food safe FDM printing](https://help.prusa3d.com/article/food-safe-fdm-printing_112313).

LiftMix is a working prototype name. This is an independent concept inspired by the supplied cap photographs, with no claim of affiliation or exact Karma compatibility.
