# OnHideDialogMessage

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Removes the in-game message and storyline panels. It runs the same clean-up as [OnEndMission](./OnEndMission), but on the
`GameMenu` entity instead of `GUI`, so the timer step (which looks for `GameMenu` → `TimerLabel` inside it) probably finds
nothing and the timer stays. No arguments.

### Decompiled handler

```c
void OnHideDialogMessage(GameLogic *self, VariantList *v) {
    if (!GetGUIRoot()) return;
    EndMissionUI(GetEntityByName(GetGUIRoot(), "GameMenu"));     // 0x177c110
}

// 0x177c110
void EndMissionUI(Entity *e) {
    if (!e) return;
    RemoveEntity(GetEntityByName(e, g_storylineStatsName));      // global name at 0x29dff48 (the panel OnStorylineStatsUpdate builds)
    RemoveEntity(GetEntityByName(e, g_dialogMessageName));       // global name at 0x29dff30
    ... clears the shared message state ...
    ShowTimer(e, false);                                         // 0x16f9538
}
```

<small>Handler: `0x1371d04` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x177c110`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnHideDialogMessage" });
```
