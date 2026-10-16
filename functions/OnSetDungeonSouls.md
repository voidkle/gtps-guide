# OnSetDungeonSouls

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the number of dungeon souls shown in the dungeon UI.
Registered by `DungeonWorldUIController::OnActivate` (`0x1c3e388`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | int | the new soul count; missing reads as 0 |

The value is stored in the `DungeonInfo` UI model (+0x30) and the model is marked changed, so the counter redraws.

```c
void OnSetDungeonSouls(DungeonWorldUIController *self, VariantList *v) {
    DungeonInfo *m = self->dungeonInfo;              // self+1000, +0x18
    m->souls = v[1].GetINT32();                   // +0x30
    if (m->bound) m->model.DirtyVariable(...);       // "DungeonInfo"
}
```

<small>Handler: lambda `0x1c3f0c0` → `0x1c36c94` (registered by `0x1c3e388`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetDungeonSouls", 1 });
```
