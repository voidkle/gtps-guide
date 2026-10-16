# 0x09 SEND_INVENTORY_STATE

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="tip" text="confirmed" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Replaces your whole inventory with the list in the extra data, then sorts it, cleans up the quick-access
slots and refreshes the inventory UI. Items the client considers invalid are skipped with a log line.

| Field | Used as |
|---|---|
| `itemID` | stored on the game logic object (`self+0xa0`); its use wasn't traced. gurotopia sends 0 |
| `extraDataLength` | not checked; the parser trusts the counts in the data |

`netID` is not read: the packet always applies to you.

### Extra data

Read by `PlayerItems::LoadFromMem` (`0x1594d54`):

```
u8  version
u32 backpack slots
count:  u16 if version != 0 and the client's "big backpack" flag is on (it is, with gurotopia), else u8
count × {
    u16 itemID
    u8  amount
    u8  flags      bit 0 = equipped
}
```

Per item:

- `itemID` 0, `itemID` ≥ the number of items in items.dat, or `amount` 0: skipped, "Illegal item %d in player inventory, skipping".
- An item the client flags as illegal: skipped, "[Removing Illegal Item] [Glitch] %d for player".
- Item 5814 (Guild Lock): skipped, "[ILLEGAL_GUILD_LOCK] removing guild lock for player".
- Items 18 (Fist), 32 (Wrench) and 9638 always get amount 1.
- `equipped` on a clothing item (type 20) puts it in the clothing slot for its body part; on anything else it logs
  "Tried to equipment item %d, a non clothes item?".

Afterwards, quick-access slots that point at items you no longer have are cleared, and slot 0 is set to the Fist.

### Decompiled handler

```c
case 0x09: {
    sub_13850f0(..., GetApp()->guiRoot->field_200, ...);   // rebuilds a GUI-side object kept at self+0x550
    int offset = 0;
    inventory->LoadFromMem(extra, NULL, &offset, ...);      // 0x1594d54, layout above
    inventory->Sort();                                      // 0x1596150
    inventory->DropMissingQuickSlots();                     // 0x15953bc
    inventory->FillEmptyQuickSlots();                       // 0x1595e6c
    self->field_a0 = pkt->itemID;
    RefreshInventoryUI();                                   // 0x1396288
}

void PlayerItems::LoadFromMem(u8 *p, ..., int *off, ...)   // read mode
{
    version = p[*off]; *off += 1;
    slots   = *(u32 *)(p + *off); *off += 4;
    int count;
    if (GameLogic()->bigBackpack && version) { count = *(u16 *)(p + *off); *off += 2; }
    else                                     { count = p[*off];            *off += 1; }
    version = GameLogic()->bigBackpack;
    items.clear(); clothes.clear();

    while (count--) {
        u16 id = *(u16 *)(p + *off); u8 amount = p[*off + 2]; *off += 3;
        if (id == 0 || id >= itemCount || amount == 0) { LogError("Illegal item %d in player inventory, skipping", id); *off += 1; continue; }
        if (IsIllegalItem(id, 1))                     { LogError("[Removing Illegal Item] [Glitch] %d for player", id); *off += 1; continue; }
        if (id == 5814)                               { LogError("[ILLEGAL_GUILD_LOCK] removing guild lock for player"); *off += 1; continue; }
        Item *it = items.push_back({ id, amount, p[*off] }); *off += 1;
        if (id == 18 || id == 9638 || id == 32) it->amount = 1;
        if (it->flags & 1) {
            ItemInfo *info = GetItem(id);
            if (info && info->type == 20) clothes[info->bodyPart] = id;     // item+0xb0
            else LogError("Tried to equipment item %d, a non clothes item?", id);
        }
    }
    // clear quick slots (inv+0x50..0x56) whose item is gone
    quickSlot[0] = 18;
}
```

<small>Handler: `0x137488c` (switch case) in the 5.60 arm64 client; callees read: `0x1594d54`, `0x1596150`, `0x15953bc`, `0x1595e6c`.</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `netID` | you |
| `flags` | `S_EXTENDED` |

## Extra data

`u8 1, i32 slot_count, i16 item_count`, then per item `i16 id, i16 count`.

## gurotopia

`send_inventory_state()` in `include/database/peer.cpp`, sent after `enter_game`.

## Official client

**Received:** handled at `0x137488c` in the incoming switch (`0x1373e20`).
