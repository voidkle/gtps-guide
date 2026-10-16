# 0x04 SEND_MAP_DATA

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="tip" text="confirmed" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Loads a whole world from the extra data and enters it. The client throws away the current world and renderer,
creates new ones, parses the world, then runs `OnInitNewWorld`.

| Field | Used as |
|---|---|
| `extraDataLength` | size of the world data; 0 is treated as an error (but the load still runs) |
| `flags` | bit 3 (0x08, `S_EXTENDED`) must be set, or the client sees no extra data |
| `tileX` | the server's clock in ms. The client adds half the connection's round-trip time and keeps it running: every frame `OnUpdate` (`0x136a80c`) sets self+0x388 = `tileX` + ms elapsed since the packet arrived. That running clock times moving objects (`0x194428c`, `0x1945768`, `0x193ed2c`; "Skipping Movement") so every client in the world moves them in step |
| `itemID` | stored in the new world (world+0x1b4, zeroed by the World constructor `0x15db578`); no load of world+0x1b4 was found anywhere in 5.60, so the client doesn't use it |

### Checks before loading

The first `u16` of the extra data is the **world version**. If the extra data is missing, the version is below 27
(`0x1b`) or `extraDataLength` is 0, the client logs `ERROR: Wrong world version: %d, dataSize %d`, records
`map_version` and `map_data_size` for its crash reporter and reports "World version or size mismatch". **It loads
the world anyway.** gurotopia sends version 0, so it always hits this path, and works.

A version above 27 logs `World::LoadFromMem() m_version %d > LATEST_TILE_FORMAT_VERSION(27) might be vital error`.
The version also changes the tile format: above 20, some tiles carry an extra block (see below).

### Extra data

As read by `World::LoadFromMem` (`0x15dd348`) and the tile map loader (`0x1620e9c`). [World data](/guide/world-data) has every field in full:

```text
u16 version
u32 flags                          logged as "f: %d"
u16 name_len, name
i32 width, i32 height
i32 tile_count                     must be < 65026 ("Map wants to load %d tiles?")
5 bytes                            skipped
repeat tile_count:                 row-major, (x, y) = entry y*width + x
  u16 fg, u16 bg
  u16 parent                       index of the lock tile covering this tile
  u16 flags                        0x01 has extra, 0x02 locked, 0x20 flipped, 0x40 on, 0x1000 fire, 0xe000 paint...
  if flags & 0x02: u16             (also stored as the lock index)
  if flags & 0x01: u8 extra_type + that type's data
  if version > 20 and the item has a "component": i32 len, len bytes
12 bytes                           skipped
i32 object_count                   more than 300000 rejects the load
i32 last_object_uid
repeat object_count: dropped item (id, position, count, uid)
if version >= 3:  u16 a, u16 b, u16 c, u16 d, i32 e        (world+0x1a8..0x1b0; b == 25 changes the tutorial hints)
if version >= 27: i32 f                                    (world+0x1a4)
```

Tiles with an id outside items.dat are cleared (`Illegal item %d in %s`). If the tile map is invalid the load stops
with `Map %s failed load due to corruption`. The world name and version are saved as `last_world` and
`last_world_version`.

### After loading

- Runs `OnInitNewWorld` with no arguments.
- If the saved settings `sendSkinColor`, `sendRoleSkin` or `sendRoleIcon` are set, sends
  `action|setSkin` / `action|setRoleSkin` / `action|setRoleIcon` to the server and clears them.
- Calls the function that may send `action|chaching` (its contents weren't decoded).
- Closes open dialogs and the loading message before all this.

### Decompiled handler

```c
case 0x04: // SEND_MAP_DATA
    CloseDialogs(0, 0, 0);                                  // 0x168f370: DialogTabs, GenericDialog...
    self->field_2f0 = 0;
    RemoveLoadingMessage(0);                                // 0x1713d24: "LoadingMessage"
    sub_1dabd98(sub_16e8854(), 0);
    int t = pkt->tileX;
    if (Net()->peer) t += Net()->peer->roundTripTime / 2;   // peer+200
    self->serverTime = t;                                   // +0x380, also copied to +0x388 (the running clock)
    self->serverTimeAt = sub_1422568();                     // +0x384: monotonic ms clock (clock_gettime)
    NewWorld(self, self->world != NULL);                    // 0x1377144: new World + WorldRenderer, "WorldSpecificGUI"
    self->world->field_1b4 = pkt->itemID;
    sub_1845240(&self->renderer->field_34e0);

    u16 *data = ExtraData(pkt);
    u16 version = 0;
    if (!data) LogMsg("MapData is empty!");
    else version = data[0];
    if (!data || version < 0x1b || pkt->extraDataLength == 0) {
        LogError("ERROR: Wrong world version: %d, dataSize %d", version, pkt->extraDataLength);
        CrashKey("map_version", version);
        CrashKey("map_data_size", pkt->extraDataLength);
        CrashReport("World version or size mismatch");
    }
    World_LoadFromMem(self->world, data, true, 0);          // 0x15dd348
    Renderer_OnWorldLoaded(self->renderer);                 // 0x11a3d24
    sub_1182b34(&self->field_1b0);
    CallFunctionNow(self, "OnInitNewWorld", VariantList());
    sub_14977c0(self->field_1600, self->world);
    if (sub_117e8cc() > 999998) { gameRoot->field_268 = 1; RefreshInventoryUI(); }

    if (Setting("sendSkinColor")) { SendSkinColor();  /* action|setSkin\ncolor|... */      ClearSetting("sendSkinColor"); }
    if (Setting("sendRoleSkin"))  { SendRoleSkin();   /* action|setRoleSkin\nroleType|... */ ClearSetting("sendRoleSkin"); }
    if (Setting("sendRoleIcon"))  { SendRoleIcon();   /* action|setRoleIcon\nroleType|... */ ClearSetting("sendRoleIcon"); }

    self->field_2c4 = GetTick() + 6500;
    if (IsFTUEHintEnabled(gameRoot->field_438) && self->world->field_1aa == 25) { ...tutorial hints... }
    sub_1f17bd4(sub_1087010(), self->world->field_1aa != 25);
    MaybeSendChaching();                                    // 0x1083db8: "action|chaching\r\n" + data
    break;
```

<small>Handler: case 0x04 of `0x1373e20` in the 5.60 arm64 client; callees read: `0x15dd348`, `0x1620e9c`, `0x15b0b14`, `0x15b1144`, `0x16188d0`, `0x1377144`, `0x1083db8`, `0x13774e0`, `0x13776c4`, `0x13778a8`.</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `flags` | `S_EXTENDED` |
| `extraDataLength` | size of the world |

## Extra data

The whole world. See [World data](/guide/world-data).

## gurotopia

`include/action/join_request.cpp` with `world::serialize()`.

## Official client

**Received:** handled at `0x1374730` in the incoming switch (`0x1373e20`).
