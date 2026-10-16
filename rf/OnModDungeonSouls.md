Adds to the number of dungeon souls shown in the dungeon UI.
Registered by `DungeonWorldUIController::OnActivate` (`0x1c3e388`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | int | the change (may be negative); missing reads as 0 |

The value is stored in the `DungeonInfo` UI model (+0x30) and the model is marked changed, so the counter redraws.

```c
void OnModDungeonSouls(DungeonWorldUIController *self, VariantList *v) {
    DungeonInfo *m = self->dungeonInfo;              // self+1000, +0x18
    m->souls += v[1].GetINT32();                   // +0x30
    if (m->bound) m->model.DirtyVariable(...);       // "DungeonInfo"
}
```

<small>Handler: lambda `0x1c3f190` → `0x1c36d54` (registered by `0x1c3e388`) in the 5.60 arm64 client.</small>

<!-- args: int -->
