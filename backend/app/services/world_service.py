from math import cos, sin, tau

LANGUAGE_COLORS = {
    "JavaScript": "#FBC4AB",
    "TypeScript": "#A7C7E7",
    "Python": "#CDB4DB",
    "Unknown": "#BDE0FE",
}


def _circle_positions(count: int, radius: float = 22.0) -> list[dict]:
    if count <= 0:
        return []
    return [
        {
            "x": radius * cos((i / count) * tau),
            "y": 0,
            "z": radius * sin((i / count) * tau),
        }
        for i in range(count)
    ]


def build_world(profile: dict, home: dict | None = None, repo_buildings: dict | None = None) -> dict:
    repos = profile["repos"][:15]
    positions = _circle_positions(len(repos))

    buildings = []
    for idx, repo in enumerate(repos):
        buildings.append(
            {
                "name": repo["name"],
                "position": positions[idx],
                "size": max(1, repo["stars"] + 1),
                "height": max(1, int(repo["commits_proxy"] / 20) + 1),
                "color": LANGUAGE_COLORS.get(repo["language"], "#D9D9D9"),
                "url": repo["url"],
                "language": repo["language"],
            }
        )

    return {
        "resident": profile["username"],
        "district": "Builder's Grove",
        "spawn": {"x": 0, "y": 1.2, "z": 8},
        "home": {
            "size": max(2, int(profile["problems_solved"] / 100) + 2),
            "glow": min(1.0, profile["activity"]["followers"] / 1000),
            "position": {"x": 0, "y": 0, "z": 0},
            "ai": home or {},
        },
        "buildings": repo_buildings.get("buildings", buildings) if repo_buildings else buildings,
        "trees": [
            {"x": -8, "y": 0, "z": -6},
            {"x": 10, "y": 0, "z": -4},
            {"x": -12, "y": 0, "z": 9},
        ],
        "paths": [
            {"from": {"x": 0, "z": 0}, "to": {"x": b["position"]["x"], "z": b["position"]["z"]}}
            for b in buildings
        ],
    }
