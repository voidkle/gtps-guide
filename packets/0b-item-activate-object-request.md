# 0x0b ITEM_ACTIVATE_OBJECT_REQUEST

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="confirmed" />

## What the client sends

<Badge type="tip" text="decompiled from the 5.60 client" />

The client never handles this type; it **sends** it, to pick up a dropped item it is touching. The sender is
`0x1381a50`, called every frame from the avatar update (`0x1304fc8`):

| Field | Value |
|---|---|
| `type` | 0x0b |
| `itemID` | the dropped object's uid (object+0xc), not its item id |
| `posX`, `posY` | your avatar's position in pixels |
| `tileX` | `(int)posX + (int)posY + 4`: a check value computed from the position (not a tile) |
| everything else | 0 |

Sent reliable, no extra data. The server answers with [ITEM_CHANGE_OBJECT (0x0e)](./0e-item-change-object).

### When it's sent

Every frame, for each dropped object whose box overlaps your avatar's box, once it has fully faded in
(alpha 1.0), while you're alive (avatar+0x170 bit 0 clear):

- Each object is requested once: the client stores the request time in the object (+0x14) and skips objects
  that already have one.
- Carried Game Egg (5996) and Carried Game Flag (1626) are only picked up while you're on a team and not
  already carrying one (avatar+0x26d / +0x26e).
- Wearing the Present Goblin Disguise (4260) stops all pickups. With Heroic Tights of Prevention (7138) only
  Gems (112) are picked up; with a Magic Magnet (8304) set to an item (GameLogic+0xb0) only Gems, Royal Winter
  Seal (9186) and that item.
- The tile under the object must be one you can access (`0x15b5f08`, `0x15b2a80`: probably the lock checks).
- If your inventory can take it (`0x1596e30`), the client plays `audio/object_collect.wav`, sets avatar
  flag 0x4000 and sends the packet. If not, it shows "`` `4(Backpack full)`` ``" (no room) or
  "`` `!(item maxed)`` ``" (stack full) at the object and doesn't send.

<small>Sender: `0x1381a50`; caller `0x1304fc8` (from the avatar update `0x1305f9c`, `0x13063d8`).</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `itemID` | the dropped object's uid (not its item id) |
| `pos` | your position |

## gurotopia

`include/gamePacket/item_activate_object.cpp`: picks up the drop (gems go to `OnSetBux`), then `ITEM_CHANGE_OBJECT` removes it for everyone.

## Official client

**Received:** ignored (falls to the switch's default).

**Sent:** `0x1381c98` sets the type to 0x0b.

## Send it yourself

Using `compress_state()` from `include/database/peer.cpp` (as `client/main.cpp` does):

```cpp
send_packet(gamePacket{ .type = 0x0b, .netid = my_netid, .id = object_uid, .pos = my_pos });
```
