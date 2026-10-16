# OnEquipNewItem

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Plays the equip effect of an item on a player. The client looks up the item's special-behaviour object, if it
has one, and calls its "equipped" method (slot 0x118) on the player's visuals. It doesn't change what the player
wears; use [OnSetClothing](/functions/OnSetClothing) for that.

| # | Type | Meaning |
|---|---|---|
| 1 | int | item id |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world. Items without a behaviour object do nothing.

### Decompiled handler

```c
void NetAvatar::OnEquipNewItem(NetAvatar *a, VariantList *vl) {
    ItemBehaviour *b = ItemBehaviours()->Find(vl[1].i);            // 0x11f5fac, 0x11f60d8
    if (b) b->OnEquip(&a->visual);                                 // 0x10d8eb0: vtable+0x118 (avatar+0x330)
}
```

<small>Handler: `0x12f6c98` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x10d8eb0`, `0x11f60d8`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnEquipNewItem"` |
| 1 | int | item id |

The game packet header's `netID` names the player this call is about.

gurotopia: `include/gamePacket/item_activate.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnEquipNewItem", 1 }, pPeer->netid);
```
