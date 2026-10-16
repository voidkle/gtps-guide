# OnEndMission

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Send it (server side)

```cpp
send_varlist(peer, { "OnEndMission", "..." });
```
