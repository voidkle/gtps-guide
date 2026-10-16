Ends a mission in the UI: removes the storyline stats panel and the message panel, and hides the mission timer.

| # | Type | Meaning |
|---|---|---|
| 1 | string | read, not used (probably the mission name or result) |

### Decompiled handler

```c
// v[n] = argument n
void OnEndMission(GameLogic *self, VariantList *v) {
    if (!v || !GetGUIRoot()) return;
    std::string unused = v[1].s;
    EndMissionUI(GetEntityByName(GetGUIRoot(), "GUI"));      // 0x177c110, see OnHideDialogMessage
}
```

<small>Handler: `0x1371ef4` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x177c110`.</small>

<!-- args: string -->
