"""Independent, standard-library geometry checks (all lengths in cm)."""

import argparse
import json
import math
from itertools import combinations
from pathlib import Path


def verify_packing(data, tolerance_cm=1e-6):
    """Validate side/upper contact, non-overlap, and the optional floor.

    This is a floating-point feasibility check, not an optimality certificate.
    Centers at z >= 0 exclude contacts with the lower face of the cylinder.
    """
    r = float(data["cylinder_radius_cm"])
    R = float(data["sphere_radius_cm"])
    h = float(data["height_cm"])
    points = data["centers_cm"]
    n = data["n_spheres"]
    floor = data["floor_enabled"]
    if (not isinstance(n, int) or n < 2 or len(points) != n
            or not isinstance(floor, bool) or not math.isfinite(tolerance_cm)
            or tolerance_cm <= 0):
        raise ValueError("Invalid sphere count, floor flag, or tolerance.")
    if any(len(p) != 3 for p in points):
        raise ValueError("Every center must contain three coordinates.")
    values = [r, R, h] + [v for p in points for v in p]
    if not all(math.isfinite(v) for v in values) or min(r, R) <= 0 or h <= 0:
        raise ValueError("Geometry must be finite, with positive radii and height.")

    pair_gaps = [math.dist(a, b) - 2 * R for a, b in combinations(points, 2)]
    contact_errors = []
    kinds = []
    for x, y, z in points:
        rho = math.hypot(x, y)
        # Distance to the entire finite solid cylinder; independent of the solver.
        horizontal = max(rho - r, 0.0)
        vertical = max(-z, z - h, 0.0)
        contact_errors.append(abs(math.hypot(horizontal, vertical) - R))
        if z <= h + tolerance_cm:
            kinds.append("side")
        elif rho <= r + tolerance_cm:
            kinds.append("top")
        else:
            kinds.append("upper_rim")

    min_z = min(p[2] for p in points)
    floor_gap = min_z - R
    valid = (min(pair_gaps) >= -tolerance_cm
             and max(contact_errors) <= tolerance_cm
             and min_z >= -tolerance_cm
             and (not floor or floor_gap >= -tolerance_cm))
    return {
        "valid_within_tolerance": valid,
        "tolerance_cm": tolerance_cm,
        "min_pair_gap_cm": min(pair_gaps),
        "max_cylinder_contact_error_cm": max(contact_errors),
        "min_center_z_cm": min_z,
        "min_floor_gap_cm": floor_gap if floor else None,
        "contact_kinds": kinds,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--tolerance-cm", type=float, default=1e-6)
    args = parser.parse_args()
    with args.file.open(encoding="utf-8") as handle:
        result = verify_packing(json.load(handle), args.tolerance_cm)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["valid_within_tolerance"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
