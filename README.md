# Football league table from a raw match export

**Business problem:** the league office needs an accurate table to send to sponsors, built from a messy CSV export.

**Data:** `data/raw/matches.csv` with 31 rows (match_id, date, teams, goals). The raw file is never edited.

**Approach**
1. Read the CSV with `csv.DictReader` and a `pathlib` path, so it runs from any folder.
2. Validate: drop the postponed match (no score), drop the duplicate `match_id`, and map messy team names to an official list (a dict comprehension). 31 rows → 30 played → 29 unique.
3. Build the table: 3/1/0 points; P, W, D, L, GF, GA per team; checked that W + D + L = P.
4. Rank by points → goal difference → goals scored.

**Result**
| Pos | Team | P | Pts | GD |
|---|---|---|---|---|
| 1 | Famalicao | 10 | 22 | +5 |
| 2 | Porto | 10 | 15 | +4 |
| 3 | Braga | 10 | 13 | +4 |
| 4 | Vitoria SC | 10 | 13 | +3 |
| 5 | Benfica | 9 | 7 | −7 |
| 6 | Sporting | 9 | 6 | −9 |

**Recommendation:** say "Famalicao lead after 10 rounds", not "best team". Their lead comes from narrow wins (11 goals scored). See `memo.md`.

**Limitations:** synthetic data; 10 rounds is a small sample; no xG or shot data.

**How to run:** `python3 league_table.py` (Python 3.10+, standard library only)