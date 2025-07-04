CITY_OBJECTS = {
    "scene/glb/house-truck-e2w-3[3].glb": {
        "type": "building",
        "connectors": {
            "west": {"type": "road", "offset": [0, -5, 0]}
        },
        "scale": [2, 2, 2],
        "tags": ["flat", "painted", "basic"],
    },
    "scene/glb/wall-truck-w2e-3[3].glb": {
        "type": "building",
        "connectors": {
            "west": {"type": "road", "offset": [0, 0, 0]},
            "east": {"type": "road", "offset": [0, 0, 0]}
        },
        "scale": [2, 2, 2],
        "tags": ["flat", "painted", "basic"],
    },
    "scene/glb/road-intersection_city.glb": {
        "type": "road",
        "connectors": {
            "north": {"type": "road", "rotation": 90},
            "east": {"type": "road", "rotation": 0},
            "south": {"type": "road", "rotation": 270},
            "west": {"type": "road", "rotation": 180}
        },
        "tags": ["asphalt", "intersection", "city"],
    },
    "scene/glb/road-intersection_province.glb": {
        "type": "road",
        "connectors": {
            "north": {"type": "road", "rotation": 90},
            "east": {"type": "road", "rotation": 0},
            "south": {"type": "road", "rotation": 270},
            "west": {"type": "road", "rotation": 180}
        },
        "tags": ["asphalt", "intersection", "province"]
    },
}

INTERSECTION_TYPES = {
    "city": {
        "tile_size": (10, 10),
        "path": "scene/glb/road-intersection_city.glb"
    },
    "province": {
        "tile_size": (10, 10),
        "path": "scene/glb/road-intersection_province.glb"
    }
}