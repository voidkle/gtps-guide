# OnSendFavItemsList

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Replaces the list of favourite items in your inventory, and sets how many favourites are allowed.

| # | Type | Meaning |
|---|---|---|
| 1 | string | item ids separated by `,` (e.g. `2,14,242`); empty = no favourites |
| 2 | int | the favourites limit, shown as `Favorited Items: <count>/<limit>` |

Global function: send it with `netID` -1 in the [CALL_FUNCTION](/packets/01-call-function) header.

- Ignored unless the server's `proto` (login settings, app+0xc08) is at least 193. The client's feature table
  (`0x7fec10`) maps feature 3, favourites, to 193.
- The old list is cleared first. Each id goes through `atoi` and is kept only if the client allows that item
  as a favourite (`0x156d3d0`, which also re-checks the proto).
- If the inventory's current tab is `Favourites`, the inventory is redrawn.

### Decompiled handler

```c
void GameLogic::OnSendFavItemsList(GameLogic *self, VariantList *vl) {
    if (GetApp()->proto < FeatureProto(3)) return;                // 0x117e8cc, 0x1457158 (193)
    Inventory::SetFavourites(&self->inventory, vl[1].s);          // 0x15966e0: clear, split ",", atoi, mark fav
    self->favouritesLimit = vl[2].i;                               // self+0x500
    if (currentInventoryTab == "Favourites") {                     // 0x29dc258
        self->inventoryDirty = 1;                                  // self+0x268
        RefreshInventoryUI();                                      // 0x1396288
        UpdateItemFavButton(self->selectedItem);                   // 0x16fbd58, self+0x298
    }
}
```

<small>Handler: `0x1372868` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x15966e0`, `0x156d3d0`, `0x1457158`, `0x16fbd58`; limit read at `0x1395090`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSendFavItemsList", "...", 1 });
```
