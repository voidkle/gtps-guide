# 0x28 FTUE_SET_ITEM_TO_QUICK_INVENTORY

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1374a44`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Puts an item into the first empty quick-access slot. The client has four slots; slot 0 is the Fist, so this
fills slot 1, 2 or 3. If all three are taken, or the item is clothing, nothing happens. "FTUE" is the
first-time user experience (the tutorial). GrowServer calls this number ON_STEP_ON_TILE_MOD, but in the
5.60 client that is 0x2e.

| Field | Used as |
|---|---|
| `itemID` | the item to place in the slot |

The item doesn't have to be in your inventory, and `itemID` isn't range-checked before its item info is read.

### Decompiled handler

```c
case 0x28: {
    ItemInfo *info = GetItem(pkt->itemID);                 // 0x1563ef8
    if (info->type == 20) break;                            // clothing
    int slot;
    if      (inventory->quickSlot[1] == 0) slot = 1;        // inv+0x52
    else if (inventory->quickSlot[2] == 0) slot = 2;        // inv+0x54
    else if (inventory->quickSlot[3] == 0) slot = 3;        // inv+0x56
    else break;
    inventory->quickSlot[slot] = (u16)pkt->itemID;
}
```

<small>Handler: `0x1374a44` (switch case) in the 5.60 arm64 client; callees read: `0x1563ef8`, `0x15954e8`.</small>

## Official client

**Received:** handled at `0x1374a44` in the incoming switch (`0x1373e20`).
