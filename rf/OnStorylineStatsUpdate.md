Builds (or rebuilds) the storyline stats panel in `GameMenu` with three numbers: "Ship: ", "Crew: " and "Reputation: ".

| # | Type | Meaning |
|---|---|---|
| 1 | int | ship (label `labelShip`) |
| 2 | int | crew (label `labelCrew`) |
| 3 | int | reputation (label `labelReputation`) |

The old panel is removed first. The numbers are formatted by `0x177b564`.

### Decompiled handler

```c
// v[n] = argument n
void OnStorylineStatsUpdate(GameLogic *self, VariantList *v) {
    if (!v || !GetGUIRoot()) return;
    int ship = v[1].GetINT32(), crew = v[2].GetINT32(), rep = v[3].GetINT32();
    ShowStorylineStats(GetEntityByName(GetGUIRoot(), "GameMenu"), ship, crew, rep);   // 0x177b840
}
```

<small>Handler: `0x1371db8` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x177b840`.</small>

<!-- args: int,int,int -->
