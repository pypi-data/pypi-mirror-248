from shapely.geometry import Polygon
from shapely.validation import explain_validity


def check_holes(geom: Polygon) -> bool:
    """Return True if the geometry has holes (interior rings)."""
    return len(geom.interiors) > 0


def check_self_intersection(geom: Polygon) -> bool:
    """Return True if the geometry is self-intersecting."""
    # TODO: Shapely independent?
    self_intersection = False
    if not geom.is_valid:
        self_intersection = "Self-intersection" in explain_validity(geom)
    return self_intersection


def check_excessive_coordinate_precision(geometry: dict, precision=6) -> bool:
    """Return True if any coordinate has more than 6 decimal places in the longitude."""
    # For speedup, only checks the x coordinate of first 2 coordinate pairs in the geometry
    # TODO: Correct, do more than first 2?
    coords = geometry["coordinates"][0]
    return any(len(str(coord[0]).split(".")[1]) > precision for coord in coords[:2])


def check_more_than_2d_coordinates(geometry: dict, check_all_coordinates=False) -> bool:
    """Return True if any coordinates are more than 2D."""
    # TODO: should check_all_coordinates be activated?
    coords = geometry["coordinates"][0]
    if check_all_coordinates:
        for ring in coords:
            for coord in ring:
                if len(coord) > 2:
                    return True
    first_coordinate = coords[0]
    return len(first_coordinate) > 2


def check_crosses_antimeridian(geometry: dict) -> bool:
    """Return True if the geometry crosses the antimeridian."""
    coords = geometry["coordinates"][0]
    for start, end in zip(coords, coords[1:]):
        # Normalize longitudes to -180 to 180 range
        norm_start_lon = (start[0] + 180) % 360 - 180
        norm_end_lon = (end[0] + 180) % 360 - 180

        # Check for longitude switch indicating crossing
        if abs(norm_end_lon - norm_start_lon) > 180:
            return True
    return False
