# Game packet header

A GAME_PACKET (message type 4) is a fixed **56-byte header**, followed by `extraDataLength` bytes of
extra data. Counting the 4-byte message type, the header is 60 bytes.

| Offset | Size | GrowServer name | gurotopia name | Meaning |
|---|---|---|---|---|
| 0 | u8 | `type` | low byte of `type` | the game packet type: see **Game packets** |
| 1 | u8 | `objectType` | byte 1 of `type` (`>> 8`) | |
| 2 | u8 | `jumpCount` | byte 2 of `type` (`>> 16`) | e.g. amount removed in MODIFY_ITEM_INVENTORY |
| 3 | u8 | `buildRange` | byte 3 of `type` (`>> 24`) | e.g. amount added, damage value |
| 4 | i32 | `netID` | `netid` | the player in the world, or -1 |
| 8 | i32 | `targetNetID` | `uid` | a second id: object uid, ... |
| 12 | i32 | `flags` | `state` | state bits, see below |
| 16 | f32 | `float_var` | `count` | object count, ... |
| 20 | i32 | `itemID` | `id` | item in hand (18 Fist, 32 Wrench) or the item placed |
| 24 | f32 | `posX` | `pos.x` | pixels (one tile = 32) |
| 28 | f32 | `posY` | `pos.y` | pixels |
| 32 | f32 | `speedX` | `speed.x` | |
| 36 | f32 | `speedY` | `speed.y` | |
| 40 | f32 | `particleID` | `idk` | |
| 44 | i32 | `tileX` | `punch.x` | tile column |
| 48 | i32 | `tileY` | `punch.y` | tile row |
| 52 | u32 | `extraDataLength` | `size` | bytes of extra data after the header |

gurotopia packs the four leading bytes into one `int`, so `(value << 24) | 0x08` means
TILE_APPLY_DAMAGE with `buildRange = value`. When reading, always compare `type & 0xff`.

The official client's send function (`0x157ee8c` in libgrowtopia.so 5.60) confirms this: it sends 56
bytes and appends the extra data only when `flags` (byte 12) has bit 3 set.

## Flags

| Bit | Name |
|---|---|
| `0x04` | S_UPDATE |
| `0x08` | S_EXTENDED: extra data follows |
| `0x10` | S_MOVE_LEFT (facing left) |
| `0x20` | S_MOVE_RIGHT |
| `0x40` | S_LAVA_HIT |
| `0x80` | S_JUMP |
| `0x4000` | S_ACTIVATE_OBJECT |

## Building one

gurotopia's `compress_state()` (`include/database/peer.cpp`) writes the header from a `gamePacket`:

```cpp
::blob blob = compress_state(::gamePacket{ .type = 0x03, .netid = my_netid, .id = 18, .pos = my_pos, .punch = {25, 37} });
enet_peer_send(server, 0, enet_packet_create(blob.data().data(), blob.size(), ENET_PACKET_FLAG_RELIABLE));
```

Without gurotopia's code, write the 60 bytes yourself:

```cpp
unsigned char p[60] = {};
int message = 4;                  memcpy(p, &message, 4);
p[4] = 0x03;                      // type
int netid = my_netid;             memcpy(p + 8, &netid, 4);
int item = 18;                    memcpy(p + 24, &item, 4);
float x = 21 * 32.f, y = 36 * 32.f; memcpy(p + 28, &x, 4); memcpy(p + 32, &y, 4);
int tx = 25, ty = 37;             memcpy(p + 48, &tx, 4); memcpy(p + 52, &ty, 4);
enet_peer_send(server, 0, enet_packet_create(p, sizeof p, ENET_PACKET_FLAG_RELIABLE));
```
