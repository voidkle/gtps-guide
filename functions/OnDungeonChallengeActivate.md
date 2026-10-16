# OnDungeonChallengeActivate

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Marks a dungeon challenge as active in the dungeon start screen.
Registered by `DungeonStartUiController::OnActivate` (`0x1cd2668`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | int | the challenge id; missing reads as 0 |

The challenge is looked up in the `DungeonStartUiModel` (`0x1cca8a4`). If it's found, its active flag (+0x48)
is set to 1 and the model is refreshed. Unknown ids are ignored.

```c
void OnDungeonChallengeActivate(DungeonStartUiController *self, VariantList *v) {
    SetChallengeActive(self->model, v[1].GetINT32(), 1);     // 0x1cca7c4
}
```

<small>Handler: lambda `0x1cd327c` → `0x1cca7c4` (registered by `0x1cd2668`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnDungeonChallengeActivate", 1 });
```
