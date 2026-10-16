# World data

The extra data of [SEND_MAP_DATA (0x04)](/packets/04-send-map-data), as the 5.60 client reads it:
`World::LoadFromMem` (`0x15dd348`), the tile map loader (`0x1620e9c`), `Tile_Serialize` (`0x15b0b14`) and
the dropped-object reader (`0x16188d0`). The same tile record is used by
[SEND_TILE_UPDATE_DATA (0x05)](/packets/05-send-tile-update-data). Numbers are little-endian; a string is
`u16 length` + bytes. The client calls these readers with a **from server** flag; fields only in its
own saved copy of a world (`last_world`) are noted, and the server never sends them.

## Layout

```text
u16   version              world+2. 5.60 knows up to 27; a higher number logs an error but still loads
u32   flags                world+0x1a0, logged as "f: %d"; nothing else reads it
str   name
i32   width, i32 height    tiles
u32   tile_count           65026 or more: "Map wants to load %d tiles?" and the load fails
5 B   skipped              (from server only)
tile_count × tile          row-major: tile (x, y) is entry y*width + x
12 B  skipped              (from server only)
u32   object_count
u32   last_object_uid      the next drop the client creates gets uid ++last_object_uid
object_count × object      16 bytes each
if version >= 3:
  u16 base weather         world+0x1a8 (see OnSetBaseWeather)
  u16 terraform type       world+0x1aa ("terraformType")
  u16 current weather      world+0x1ac (see OnSetCurrentWeather)
  u16 unknown              world+0x1ae, no reader found
  u32 unknown              world+0x1b0, no reader found
if version >= 27 (from server only):
  u32 unknown              world+0x1a4, no reader found
```

After loading, the world name and version are saved as `last_world` and `last_world_version`, and
[OnInitNewWorld](/functions/OnInitNewWorld) runs (see [0x04](/packets/04-send-map-data)). A few items get
[fix-ups](#special-items) while loading.

Version notes:

- Below 3 there is no weather footer at all.
- Above 20 a tile can carry [component data](#tile-components).
- gurotopia sends version 0, so the client logs "Wrong world version" in 0x04 and reads no footer.
  Its world still loads.

### Terraform type

`world+0x1aa` is passed to the client's script conditions as `terraformType` (`0x1b3076c`). The value 25
is special: the client sends its own movement every 100 ms instead of 200 ms (`0x1381a2c`), and the world
screen skips part of its setup (`0x1bff3ec`, `0x13131f8`). What kind of world 25 is wasn't found; it is
probably an event world type.

### Weather ids

From the client's `WEATHER_TYPE_*` table (`0xcecca0`):

0 `DEFAULT`, 1 `SUNSET`, 2 `NIGHT`, 3 `DESERT`, 4 `SUNNY`, 6 `HARVEST`, 7 `MARS`, 8 `SPOOKY`, 9 `MAW`, 10 `BLANK`, 11 `SNOWY`, 12 `GROWCH`, 14 `UNDERSEA`, 15 `WARP`, 16 `COMET`, 17 `COMET2`, 18 `PARTY`, 19 `PINEAPPLE`, 21 `SPRING`, 22 `WOLF`, 25 `FIRE_HAZE`, 27 `AQUA_HAZE`, 28 `CUSTOM_HAZE`, 29 `CUSTOM_ITEMS`, 30 `PAGODA`, 31 `APOCALYPSE`, 32 `JUNGLE`, 33 `BALLOON_WARZ`, 34 `BACKGROUND`, 35 `AUTUMN`, 36 `HEART`, 37 `STPATRICKS`, 38 `ICE_AGE`, 39 `VOLCANO`, 40 `FLOATING_ISLANDS`, 41 `MASCOT`, 42 `DIGITAL_RAIN`, 43 `MONOCHROME`, 44 `TREASURE`, 45 `SURGERY`, 46 `BOUNTIFUL`, 47 `METEOR`, 48 `STARS`, 49 `ASCENDED`, 50 `DESTROYED`, 51 `GROWTOPIA_SIGN`, 52 `DUNGEON`, 53 `LEGENDARY_CITY`, 54 `BLOOD_DRAGON`, 55 `POP_CITY`, 56 `ANZU`, 57 `TMNT_CITY`, 58 `RAD_CITY`, 59 `PLAZA`, 60 `NEBULA`, 61 `PROTOSTAR`, 62 `DARK_MOUNTAINS`, 63 `AC15`, 64 `MOUNT_GROWMORE`, 65 `CRACK_IN_REALITY`, 66 `LNY_NIAN`, 67 `RAYMAN_LOCK`, 68 `STEAMPUNK`, 69 `REALM_OF_SPIRITS`, 70 `BLACK_HOLE`, 71 `GEMS`, 72 `HOLIDAY_HAVEN`, 73 `FENYX_LOCK`, 74 `ENCHANTED_LOCK`, 75 `ROYAL_ENCHANTED_LOCK`, 76 `NEPTUNES_ATLANTIS`, 77 `PINUSKI_PETAL_PURRFECT_HAVEN`, 78 `CANDY_LAND`, 79 `DRAGONS_KEEP`, 80 `EMERALD_CITY`, 81 `ANCESTRAL_PLANE`, 82 `BLACK_DIGITAL_RAIN`.

Missing numbers (5, 13, 20, 23, 24, 26) weren't decoded from the table.

## Tile

```text
u16 fg                     item id; outside items.dat: "Illegal item %d in %s", set to 0
u16 bg                     item id, same check
u16 parent                 tile+0xc0: index (y*width + x) of the lock tile that owns this tile
u16 flags                  tile+0x52, see below
if flags & 0x02:  u16      replaces parent (tile+0xc0)
if flags & 0x01:  u8 extra type + its data   -> Tile extras page, then the common trailer below
if version > 20 and fg has a component:  u32 len + len bytes   -> Tile components below
```

See [Tile extras](/guide/tile-extras) for each extra type.

gurotopia writes `i16 fg, i16 bg, u8 state[4]`: its `state` is `parent` and `flags` as two u16s.

### Tile flags

The client's own names (`TILE_FLAG_*`, from a table in several static initializers, e.g. `0x108ea9c`):

| Bit | Name | What the client does with it |
|---|---|---|
| `0x0001` | `HAS_EXTRA_DATA` | a tile extra follows; if the parsed extra turns out empty the flag is cleared |
| `0x0002` | `HAS_PARENT` | an extra `u16` parent index follows |
| `0x0004` | `WAS_SPLICED` | the seed's splice is marked as discovered (`0x1483fa0`, probably the seed diary) |
| `0x0008` | `WILL_SPAWN_SEEDS_TOO` | a tree drops seeds too ([0x0c](/packets/0c-send-tile-tree-state)) |
| `0x0010` | `IS_SEEDLING` | [0x0c](/packets/0c-send-tile-tree-state) |
| `0x0020` | `FLIPPED_X` | drawn mirrored |
| `0x0040` | `IS_ON` | switched on; for Deathtrap Wall (6154), Prickly Pineapple (8528) and Storm Cloud (7202) a change restarts a timer |
| `0x0080` | `IS_OPEN_TO_PUBLIC` | |
| `0x0100` | `BG_IS_ON` | |
| `0x0200` | `FG_ALT_MODE` | |
| `0x0400` | `IS_WET` | |
| `0x0800` | `GLUED` | |
| `0x1000` | `ON_FIRE` | counted per world (tilemap+0x10) |
| `0x2000` | `PAINTED_RED` | |
| `0x4000` | `PAINTED_GREEN` | |
| `0x8000` | `PAINTED_BLUE` | the three paint bits are cleared on lock tiles (action type 3) |

The values of `IS_OPEN_TO_PUBLIC` and `PAINTED_GREEN` are inferred from the order of the table and the
gaps; the others were read from it.

### Which tiles have an extra

The server decides: the client reads an extra whenever flag `0x01` is set. When the client itself sets a
foreground (placing a block), `0x15d1014` picks the extra type from the item's action type. The server
must send the same type the client would pick, or the client reads the wrong bytes and the rest of the
world is garbage. Action types not in this table have no extra.

| Action type | Client name | Extra type |
|---|---|---|
| 2 | `USER_DOOR` | [0x01](/guide/tile-extras#0x01) Door |
| 3 | `LOCK` | [0x03](/guide/tile-extras#0x03) Lock |
| 10 | `SIGN` | [0x02](/guide/tile-extras#0x02) Sign |
| 13 | `DOOR` | [0x01](/guide/tile-extras#0x01) Door |
| 15 | `BEDROCK` | [0x2a](/guide/tile-extras#0x2a) Data Bedrock |
| 19 | `SEED` | [0x04](/guide/tile-extras#0x04) Seed |
| 26 | `PORTAL` | [0x01](/guide/tile-extras#0x01) Door |
| 30 | `RACE_FLAG` | [0x05](/guide/tile-extras#0x05) (no data) |
| 33 | `MAILBOX` | [0x06](/guide/tile-extras#0x06) Mailbox |
| 34 | `BULLETIN` | [0x07](/guide/tile-extras#0x07) Bulletin board |
| 36 | `DICE` | [0x08](/guide/tile-extras#0x08) Dice block |
| 38 | `PROVIDER` | [0x09](/guide/tile-extras#0x09) Provider |
| 40 | `ACHIEVEMENT` | [0x0a](/guide/tile-extras#0x0a) Achievement block |
| 43 | `SUNGATE` | [0x01](/guide/tile-extras#0x01) Door |
| 46 | `HEART_MONITOR` | [0x0b](/guide/tile-extras#0x0b) Heart monitor |
| 47 | `DONATION_BOX` | [0x0c](/guide/tile-extras#0x0c) Donation box |
| 48 | `TOYBOX` | [0x0d](/guide/tile-extras#0x0d) (mailbox layout) |
| 49 | `MANNEQUIN` | [0x0e](/guide/tile-extras#0x0e) Mannequin |
| 50 | `CAMERA` | [0x07](/guide/tile-extras#0x07) Bulletin board |
| 51 | `MAGICEGG` | [0x0f](/guide/tile-extras#0x0f) Bunny egg |
| 52 | `TEAM` | [0x10](/guide/tile-extras#0x10) Game block |
| 53 | `GAME_GEN` | [0x11](/guide/tile-extras#0x11) Game generator |
| 54 | `XENONITE` | [0x12](/guide/tile-extras#0x12) Xenonite crystal |
| 55 | `DRESSUP` | [0x13](/guide/tile-extras#0x13) Phone booth |
| 56 | `CRYSTAL` | [0x14](/guide/tile-extras#0x14) Crystal |
| 57 | `BURGLAR` | [0x15](/guide/tile-extras#0x15) Crime in progress |
| 59 | `SPOTLIGHT` | [0x16](/guide/tile-extras#0x16) Spotlight |
| 61 | `DISPLAY_BLOCK` | [0x17](/guide/tile-extras#0x17) Display block |
| 62 | `VENDING` | [0x18](/guide/tile-extras#0x18) Vending machine |
| 63 | `FISHTANK` | [0x19](/guide/tile-extras#0x19) Fish tank port |
| 65 | `SOLAR` | [0x1a](/guide/tile-extras#0x1a) Solar collector |
| 66 | `FORGE` | [0x1b](/guide/tile-extras#0x1b) Forge |
| 67 | `GIVING_TREE` | [0x1c](/guide/tile-extras#0x1c) Giving Tree |
| 68 | `GIVING_TREE_STUMP` | [0x1d](/guide/tile-extras#0x1d) Giving Tree Stump |
| 71 | `STEAM_ORGAN` | [0x1e](/guide/tile-extras#0x1e) Steam Organ |
| 72 | `TAMAGOTCHI` | [0x1f](/guide/tile-extras#0x1f) Silkworm |
| 73 | `SEWING` | [0x20](/guide/tile-extras#0x20) Sewing Machine |
| 74 | `FLAG` | [0x21](/guide/tile-extras#0x21) Country Flag / Challenge flags |
| 75 | `LOBSTER_TRAP` | [0x22](/guide/tile-extras#0x22) Lobster Trap |
| 76 | `ARTCANVAS` | [0x23](/guide/tile-extras#0x23) Painting Easel |
| 77 | `BATTLE_CAGE` | [0x24](/guide/tile-extras#0x24) Battle Pet Cage |
| 78 | `PET_TRAINER` | [0x25](/guide/tile-extras#0x25) Pet Trainer |
| 79 | `STEAM_ENGINE` | [0x26](/guide/tile-extras#0x26) Steam Engine |
| 80 | `LOCK_BOT` | [0x27](/guide/tile-extras#0x27) Lock-Bot |
| 81 | `WEATHER_SPECIAL` | [0x28](/guide/tile-extras#0x28) Weather Machine (one setting) |
| 82 | `SPIRIT_STORAGE` | [0x29](/guide/tile-extras#0x29) Spirit Storage Unit |
| 83 | `DISPLAY_SHELF` | [0x2b](/guide/tile-extras#0x2b) Display Shelf |
| 84 | `VIP_DOOR` | [0x2c](/guide/tile-extras#0x2c) VIP Entrance |
| 85 | `CHAL_TIMER` | [0x2d](/guide/tile-extras#0x2d) Challenge Timer |
| 86 | `CHAL_FLAG` | [0x21](/guide/tile-extras#0x21) Country Flag / Challenge flags |
| 87 | `FISH_MOUNT` | [0x2f](/guide/tile-extras#0x2f) Fish Wall Mount |
| 88 | `PORTRAIT` | [0x30](/guide/tile-extras#0x30) Portrait |
| 89 | `WEATHER_SPECIAL2` | [0x31](/guide/tile-extras#0x31) Weather Machine (several settings) |
| 91 | `FOSSIL_PREP` | [0x32](/guide/tile-extras#0x32) Fossil Prep Station |
| 92 | `DNA_MACHINE` | [0x33](/guide/tile-extras#0x33) DNA Processor |
| 93 | `BLASTER` | [0x34](/guide/tile-extras#0x34) Howler / Trickster |
| 96 | `CHEMTANK` | [0x35](/guide/tile-extras#0x35) Chemsynth Tank |
| 97 | `STORAGE` | [0x36](/guide/tile-extras#0x36) Storage box |
| 98 | `OVEN` | [0x37](/guide/tile-extras#0x37) Oven |
| 99 | `SUPER_MUSIC` | [0x38](/guide/tile-extras#0x38) Audio Rack |
| 100 | `GEIGERCHARGE` | [0x39](/guide/tile-extras#0x39) Geiger Charger |
| 101 | `ADVENTURE_RESET` | [0x3a](/guide/tile-extras#0x3a) Adventure Begins |
| 102 | `TOMB_ROBBER` | [0x3b](/guide/tile-extras#0x3b) Tomb Robber |
| 103 | `FACTION` | [0x3c](/guide/tile-extras#0x3c) Faction block |
| 104 | `RED_FACTION` | [0x3c](/guide/tile-extras#0x3c) Faction block |
| 105 | `GREEN_FACTION` | [0x3c](/guide/tile-extras#0x3c) Faction block |
| 106 | `BLUE_FACTION` | [0x3c](/guide/tile-extras#0x3c) Faction block |
| 109 | `FISHGOTCHI_TANK` | [0x3d](/guide/tile-extras#0x3d) Training Port |
| 111 | `ITEM_SUCKER` | [0x3e](/guide/tile-extras#0x3e) Item Sucker (MAGPLANT) |
| 113 | `ROBOT` | [0x3f](/guide/tile-extras#0x3f) Robot |
| 115 | `LUCKY_TICKET` | [0x40](/guide/tile-extras#0x40) Lucky Token |
| 116 | `STATS_BLOCK` | [0x42](/guide/tile-extras#0x42) GrowScan 9000 |
| 117 | `FIELD_NODE` | [0x43](/guide/tile-extras#0x43) Containment Field Power Node |
| 118 | `OUIJA_BOARD` | [0x44](/guide/tile-extras#0x44) Spirit Board |
| 123 | `AUTO_ACTION_BREAK` | [0x45](/guide/tile-extras#0x45) Tesseract Manipulator |
| 124 | `AUTO_ACTION_HARVEST` | [0x46](/guide/tile-extras#0x46) Heart of Gaia |
| 125 | `AUTO_ACTION_HARVEST_SUCK` | [0x47](/guide/tile-extras#0x47) Techno-Organic Engine |
| 126 | `LIGHTNING_CLOUD` | [0x48](/guide/tile-extras#0x48) Storm Cloud |
| 127 | `PHASED_BLOCK` | [0x49](/guide/tile-extras#0x49) Phased block |
| 130 | `PASSWORD_STORAGE` | [0x4a](/guide/tile-extras#0x4a) Safe Vault |
| 131 | `PHASED_BLOCK_2` | [0x4b](/guide/tile-extras#0x4b) Angelic Counting Cloud |
| 133 | `PVE_NPC` | [0x4c](/guide/tile-extras#0x4c) PvE NPC |
| 134 | `INFINITY_WEATHER_MACHINE` | [0x4d](/guide/tile-extras#0x4d) Infinity Weather Machine |
| 137 | `COMPLETIONIST` | [0x4e](/guide/tile-extras#0x4e) Completionist |
| 140 | `FEEDING_BLOCK` | [0x4f](/guide/tile-extras#0x4f) Feeding block |
| 141 | `KRANKENS_BLOCK` | [0x50](/guide/tile-extras#0x50) Kranken's block |
| 142 | `FRIENDS_ENTRANCE` | [0x51](/guide/tile-extras#0x51) Friends Entrance |

Action type names are the client's `ITEM_TYPE_*` names; see [items.dat](/guide/items-dat#action-types).

### Common trailer

After an extra's own bytes, `TileExtra_Serialize` (`0x15ce080`, label `0x15d04a8`) reads more bytes for two
kinds of foreground:

- **Guild items** (items.dat flag `GUILD_ITEM`, `flags2 & 0x200`; 67 items in 5.60: the Guild Lock (5814),
  Guild Key, entrances, banners, flag poles and flags):

  ```text
  u8   unknown            extra+9; not present for the Guild Lock itself (5814)
  u32  probably the guild id                          extra+0xe0
  u32  guild emblem: low 16 bits the foreground item, high 16 bits the background item (0 = none)  extra+0xe4
  u32  guild level                                     extra+0xe8
  u32  must be non-zero for the emblem to be drawn    extra+0xec
  ```

  The drawing code (`0x11b4230`) uses `+0xe8` for the Guild Lock's frame (4, 5 above level 5, one more
  above 10) and its flag overlay (`level % 5`). It draws the emblem items only when `+0xe4` and `+0xec`
  are both non-zero.

- **Data Starship Hull (6546)** in worlds of version 5 or newer, when it isn't a guild item:

  ```text
  6 × u32                 extra+0xf0, +0xf8, +0xf4, +0x104, +0xfc, +0x100
  u64                     extra+0x130, version 11+, saved copy only (not sent by the server)
  u32                     extra+0x110, version 15+
  ```

- Any tile whose extra type is `0x2a` (`'*'`, Data Bedrock) in version 11+: a `u64` (extra+0x130), saved copy
  only.

What the starship values mean wasn't traced.

## Tile components

From version 21 a tile can also carry a **component**: a `u32` length followed by that many bytes of
[CBOR](https://cbor.io/)-encoded JSON (`nlohmann::json::from_cbor`, `0x15b15f8`). The client creates
the component from the foreground item (`0x145a0bc`) and only reads the bytes if the item has one. A
length of 0 removes it. If the world's version is below the component's minimum, no bytes are read.

| Item | Component (RTTI name) | Min version | Sent by server | JSON keys |
|---|---|---|---|---|
| Battle Pet Cage (3548) | `BattleCageData` | 24 | yes | `pet` (3 numbers), `damage` |
| Offering Table (12598) | `OfferingTableData` | 0 | **no** (saved copy only) | `itemsInSlots`, `lastReward`, `lastRewardCount` |
| Operating Table (14662) | `OperatingTableData` | 0 | yes | `isInSurgery` (bool), `currentState`, `nextSwitchAt` |
| Auto Surgeon Station (14666) | `AutoSurgeonStationData` | 0 | yes | `outOfOrder`, `wlCount`, `selectedIllness`, `stockedItems`, `lastUpdateTime`, `wlCost`, `disabled` |
| Reception Desk (14668) | `ReceptionDeskData` | 0 | **no** (saved copy only) | `HL`, `CI`, `TS`, `SS`, `DL`, `IC` |
| Party Projector (15376) | `PartyProjectorData` | 0 | yes | `MovementSpeed`, `SpinningSpeed` (floats), `SelectedPatternID` |
| Auction Block (15546) | `AuctionBlockData` | 0 | yes | `Item`, `DurationHrs`, `StartingPrice`, `State`, `EndTime` (64-bit) |
| Weather Machine - Concert Lights (16094) | `WeatherMachineData` | 0 | yes | `jsonString` (a string) |
| Bountiful roots: 8624, 8630, ... 8714 (every 6th id, 16 items) | `RootsData` | 25 | yes | `IsGreyRoot` (bool), `RootLevel` (0–3, larger becomes 0) |

"Sent by server: no" means the component's `+0x20` method returns true, and the client then skips it
when reading from the server: send no length for those items. A missing key reads as 0/false.

Before version 24 a Battle Pet Cage's data is converted from its tile extra, and before 25 a root's from
its flags (`IsGreyRoot` = `IS_ON` clear; `RootLevel` from bits `0x20` and `0x200`). This only happens for the saved copy.

## Dropped object

```text
u16 item id          not in items.dat -> becomes 2 (Dirt)
f32 x, f32 y         pixels
u8  count
u8  flags            object+0xb; meaning not traced
u32 uid
```

gurotopia writes `i16 id, f32 x, f32 y, i16 count, i32 uid`, which is the same bytes when count < 256
and the flags byte is 0.

## Special items

These only apply when the client loads its own saved copy (not from the server):

- Busted Game Block (1620), Missing Game Flag (1624) and Missing Game Egg (5994) are read as Game Block
  (1618), Game Flag (1622) and Game Egg (5992).
- Locke The Salesman (2398) is removed.
- Surg-E (4296) and the Chemsynth Processor/Tank (4430, 4432) are switched off (`IS_ON` cleared).
- A Dice Block (456) in a version-0 world is removed ("Found dice, removing").

From the server, a Containment Field Power Node (6084) that is replaced by another item runs the
field-removal code (`0x15e09a0`).

<small>Readers: `0x15dd348`, `0x1620e9c`, `0x15b0b14`, `0x15b1144`, `0x145a0bc`, `0x15b15f8`, `0x16188d0`, `0x161493c`; trailer: `0x15ce080`; type table: `0x15d1014`.</small>
