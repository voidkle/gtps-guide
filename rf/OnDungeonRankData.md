Fills the dungeon leaderboard.
Registered by `DungeonLeaderboardController::OnActivate` (`0x1cbf7c0`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | string | JSON, below |

| Key | Type | Meaning |
|---|---|---|
| `Entries` | array | the rows: `{"Position": n, "Name": "...", "Score": n}` |
| `Position` | int | your position |
| `Points` | int | your points |
| `PlayerCount` | int | players in the group |
| `Promotion`, `Demotion` | int | the promotion and demotion thresholds |
| `EndTime` | int | when the season ends |
| `PositionInfo`, `PromotionInfo`, `GroupName` | string | texts shown on the screen |

At most 100 rows are kept: when scrolling up the rows at the end are dropped, when scrolling down those at the
start. The `DungeonLeaderboardModel` is then refreshed and the list scrolls to your row or to the requested one.

<small>Handler: lambda `0x1cc32e0` → `0x1cc06b8` (reader `0x1cc0f9c`) in the 5.60 arm64 client.</small>

<!-- args: string -->
