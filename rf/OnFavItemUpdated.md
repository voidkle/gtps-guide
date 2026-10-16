Marks one item as a favourite or not, then redraws the inventory.

| # | Type | Meaning |
|---|---|---|
| 1 | int | item id |
| 2 | int | 1 = favourite, anything else = not a favourite |

Global function: send it with `netID` -1 in the [CALL_FUNCTION](/packets/01-call-function) header.

Ignored unless the server's `proto` (login settings, app+0xc08) is at least 193 (feature 3 in the client's
table). The item doesn't have to be in the inventory; an entry is created for it.

### Decompiled handler

```c
void GameLogic::OnFavItemUpdated(GameLogic *self, VariantList *vl) {
    if (GetApp()->proto < FeatureProto(3)) return;                // 193
    Inventory::SetFavourite(&self->inventory, vl[1].i, vl[2].i == 1);   // 0x15962c0: entry.fav, entry+0x15 = 0
    self->inventoryDirty = 1;                                      // self+0x268
    RefreshInventoryUI();                                          // 0x1396288
    UpdateItemFavButton(self->selectedItem);                       // 0x16fbd58
}
```

<small>Handler: `0x13729d0` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x15962c0`, `0x1457158`.</small>

<!-- args: int,int -->
