import csv
from pathlib import Path


DATA = Path(__file__).parent/"data"/"raw"/"matches.csv"
TEAMS = ["Benfica", "Porto", "Sporting", "Braga", "Vitoria SC", "Famalicao"]
CANON = {t.strip().lower(): t for t in TEAMS}


def read_matches(path: Path) -> list[dict[str, str]]:
    """Read matches from a CSV file and return a list of dictionaries."""
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def validate(matches: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep only matches that were played (have a score)."""
    played = [m for m in matches if m["home_goals"] and m["away_goals"]]
    seen = set()
    unique = []
    for m in played:
        if m["match_id"] in seen:
            continue
        seen.add(m["match_id"])
        m["home_team"] = CANON.get(m["home_team"].strip().lower())
        m["away_team"] = CANON.get(m["away_team"].strip().lower())
        unique.append(m)
    return unique


def points(goals_for: int, goals_against: int) -> int:
    """Return league points for one team in one match."""
    if goals_for > goals_against:
        return 3
    elif goals_for == goals_against:
        return 1
    else:
        return 0


def build_table(matches: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    """Return P, W, D, L, GF, GA, Pts per team."""
    table = {t: {"P": 0, "W": 0, "D": 0, "L": 0,
                 "GF": 0, "GA": 0, "Pts": 0} for t in TEAMS}
    for m in matches:
        hg, ag = int(m["home_goals"]), int(m["away_goals"])
        for team, gf, ga in [(m["home_team"], hg, ag), (m["away_team"], ag, hg)]:
            row = table[team]
            row["P"] += 1
            row["GF"] += gf
            row["GA"] += ga
            pts = points(gf, ga)
            row["Pts"] += pts
            if pts == 3:
                row["W"] += 1
            elif pts == 1:
                row["D"] += 1
            else:
                row["L"] += 1
    return table


def main():
    matches = read_matches(DATA)
    played = validate(matches)
    table = build_table(played)
    ranked = sorted(table.items(), key=lambda item: (
        item[1]["Pts"], item[1]["GF"] - item[1]["GA"], item[1]["GF"]), reverse=True)
    for pos, (team, r) in enumerate(ranked, start=1):
        print(
            f"{pos}.{team:<12} P{r['P']} W{r['W']} D{r['D']} L{r['L']} GD{r['GF'] - r['GA']:+} Pts{r['Pts']}")


main()
