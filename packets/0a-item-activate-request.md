# 0x0a ITEM_ACTIVATE_REQUEST

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="confirmed" />

## What the client sends

<Badge type="tip" text="decompiled from the 5.60 client" />

The client never handles this type; it **sends** it, to wear, take off or use an item from your inventory.
The sender is `0x13817b8`:

| Field | Value |
|---|---|
| `type` | 0x0a |
| `itemID` | the item |
| everything else | 0 |

Sent reliable, no extra data. The server answers with the result (for clothing, gurotopia sends
[OnSetClothing](/functions/OnSetClothing) and [OnEquipNewItem](/functions/OnEquipNewItem)).

### When it's sent

- **Tapping an inventory item a second time** (`0x13940cc`): the first tap selects the item; tapping the
  selected item again sends 0x0a when it is:
  - clothing (action type 20), or an item of action type 107;
  - or one of these: World Lock (242), Diamond Lock (1796), Blue Gem Lock (7188), Profile (980),
    Growtoken (1486), Mega Growtoken (6802), Buckazoid (6418), Mega Buckazoid (6734), Growpedia (6336),
    Caduceus (4298), Golden Caduceus (4300), Wolf Ticket (4354), Enchanted Wolf Ticket (4356),
    Zombie Brain (4450), Pile of Zombie Brains (4452), Mac n' Cheese Star (4612),
    Plethora Of Mac n' Cheese Stars (4614), the six War Balloon items (4844-4854), Halloween Candy (12766),
    Halloween Basket (12768), items 8530 and 8532.

  At most once every 333 ms. For a non-clothing item the client then selects your Fist again (or item 9638 in
  worlds where `0x15e7cb0` is true). Nothing is sent while you're in a pet battle (avatar+0x3294 ≥ 0, the battle id that
  [0x21](./21-pet-battle) uses) or while avatar+0x3298 ≥ 0 (probably the card battle), or while GameLogic+0xc0 is set.
- **The wardrobe screen** (`WardrobeChangeItemModel.ItemClick`, `0x1d43ee4`): clicking an item whose
  `button_id` differs from the one in that slot sends it, if it's clothing (type 20) or type 107 other than
  Ancient Shards (9236).

Tapping other items doesn't send 0x0a. Increase Backpack (9412) sends
`action|storenavigate\nitem|locks\nselection|upgrade_backpack\n` instead, and Remove Favorites (13720) sends
`action|inventoryfavuitrigger\n` (with a high enough `proto`).

<small>Sender: `0x13817b8`; callers `0x13940cc` (inventory slot tap), `0x1d43ee4` (wardrobe).</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `itemID` | the item to use or wear |

## gurotopia

`include/gamePacket/item_activate.cpp`: clothing toggles on or off (`OnEquipNewItem`, `OnSetClothing`); some items have special effects.

## Official client

**Received:** ignored (falls to the switch's default).

**Sent:** `0x1381810` sets the type to 0x0a and `itemID` from its argument.

## Send it yourself

Using `compress_state()` from `include/database/peer.cpp` (as `client/main.cpp` does):

```cpp
send_packet(gamePacket{ .type = 0x0a, .netid = my_netid, .id = item_id });
```
