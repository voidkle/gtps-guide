# items.dat

The item database. The server sends it in [SEND_ITEM_DATABASE_DATA (0x10)](/packets/10-send-item-database-data)
when the client's copy is out of date; the client checks that with the hash in
[OnSuperMainStartAcceptLogon…](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a). This page follows
the 5.60 client's reader (`ItemInfoManager::LoadFromMem`, `0x1563a38`, and the per-item reader `0x1574f08`).
A decoder written from it reads the 5.60 items.dat (version 27, 16434 items, 5,748,732 bytes) to the last byte.

Numbers are little-endian. `str` is a `u16` length followed by that many bytes (no terminator).

## File

```text
u16 version        27 in 5.60
i32 item_count
item_count × item  item i has id i
```

## Item record

The second column is where the client stores the value in its 0x748-byte item struct; other pages
on this site refer to these offsets (`item+4`, `item+8`, ...). Names marked *(PS)* are the names
private servers use; the client code doesn't name those fields.

| Version | Field | Struct | Meaning |
|---|---|---|---|
| all | `i32` id | +0x00 | |
| all | `u16` flags | +0x62 | [item flags](#item-flags) |
| all | `u8` action type | +0x04 | [action type](#action-types): what the item does |
| all | `u8` material | +0x08 | hit and break sound: 1 glass, 2 rock, 3 metal, else wood |
| all | `str` name | +0x10 | from version 3 [encrypted](#name-encryption) |
| all | `str` texture | +0x30 | file in `game/` |
| all | `i32` texture hash | +0x28 | |
| all | `u8` visual effect *(PS)* | +0x48 | |
| all | `i32` cooking time *(PS)* | +0x4c | -1 for almost every item |
| all | `u8` texture x, `u8` texture y | +0x50, +0x51 | tile position in the texture |
| all | `u8` spread type *(PS)* | +0x54 | how the sprite joins its neighbours |
| all | `u8` is stripey wallpaper *(PS)* | +0x58 | |
| all | `u8` collision type *(PS)* | +0x5c | 0 none, 1 solid, ... |
| all | `u8` break hits | +0x60 | hits × 6 (120 = 20 hits); gurotopia divides by 6 |
| all | `i32` reset time *(PS)* | +0xac | seconds before a damaged block heals |
| all | `u8` clothing type *(PS)* | +0xb0 | body slot for clothes |
| all | `u16` rarity *(PS)* | +0x116 | |
| all | `u8` max amount *(PS)* | +0x118 | stack size, 200 for most items |
| all | `str` extra file | +0x120 | sound or other file the item uses |
| all | `i32` extra file hash | +0x138 | |
| all | `i32` audio volume *(PS)* | +0x13c | |
| 4+ | `str` pet name, `str` pet prefix, `str` pet suffix | +0x168, +0x180, +0x198 | also copied to the pet table (`0x14d1d34`) |
| 5+ | `str` pet ability | +0x1b0 | |
| all | `u8` seed base, `u8` seed overlay, `u8` tree base, `u8` tree leaves *(PS)* | +0xb4..+0xb7 | seed and tree sprite indexes |
| all | `i32` seed color, `i32` seed overlay color | +0xb8, +0xbc | ARGB |
| all | `u16`, `u16` | | skipped by the reader; the splice recipe moved to version 23 |
| all | `i32` grow time *(PS)* | +0xc4 | seconds for a tree to grow |
| 7+ | `i32` | +0x2ac | mostly 0; 1, 3, 13, 33, 4096 on some items |
| 7+ | `str` extra options | +0x2b0 | e.g. `0,0\|1,0\|2,0\|3,0\|4,0\|` |
| 8+ | `str` texture 2 | +0x2e0 | |
| 8+ | `str` extra options 2 | +0x2c8 | |
| all | `u64` | +0x2f8 | 0 on all but 3 items |
| 9+ | `i32` flags2 | +0x64 | [second item flags](#item-flags-2) |
| 9+ | 15 × `i32` | +0x6c..+0xa4 | robot and command parameters; 0 on all other items |
| 10+ | `i32`, `i32` | +0x334, +0x338 | the second is probably a capacity (20, 40, 90 on the Storage Box Xtreme levels) |
| 11+ | `str` punch options | +0x368 | punch effect script: `ONPUNCHSTART;op_particle2:193;op_audio:...` |
| 12+ | `i32` + 9 × `u8` | +0x360, +0x33c.. | the bytes are 9 except on one item |
| 13+ | `i32` | +0x304 | |
| 14+ | `i32` | +0x160 | |
| 15+ | `u8`, 3 × `u64`, `str` | +0x600.., +0x620 | the string is a sit texture (`game/player_sit2.rttex`) on 2 items |
| 16+ | `str` | +0x650 | an XML file (`GrowchBod.xml`, `InfinityAura.xml`) |
| 17+ | `i32` | +0x6d0 | |
| 18+ | `i32` | +0x668 | probably the hash of the version-16 file |
| 19+ | `u8`, `i32`, `i32` | +0x638, +0x63c, +0x640 | |
| 20+ | `u8` | +0x68 | |
| 21+ | `u8` | +0x66d | |
| 22+ | `str` info | +0x140 | the item's description ("Yep, it's dirt.") |
| 23+ | `u16`, `u16` splice | +0xc0, +0xc2 | the two seeds that splice into this item |
| 24+ | `u8` | +0x6f4 | |
| 25+ | `str`, `i32` | +0x6d8, +0x6f0 | a hit effect name (`BandageCannonPlayerHitFx`) and a number (3000) |
| 26+ | `u8` | +0x6f8 | |
| 27+ | `str` | +0x700 | e.g. `6` on the Immortal items |

The reader has a second mode with more fields (between the seed colors and the grow time, and before
version 22's info string), but every caller (the 0x10 packet and loading the saved file) uses the compact
mode above. Fields without a meaning were not traced to a reader; their example values come from the 5.60 file.

### Name encryption

From version 3 the name is XORed with the 16-byte key `PBG892FXX982ABC*`, starting at key position
`id % 16` (`0x1e742b0`):

```cpp
for (int i = 0; i < len; ++i) name[i] = data[i] ^ key[(i + id) % 16];
```

### File hash

The hash the server sends in `OnSuperMainStartAcceptLogon…` argument 1 is proton's `HashString` run over
the whole file (`0x1e69d5c`, the same function as in [0x16](/packets/16-ping-request)):

```cpp
uint32_t h = 0x55555555;
for (size_t i = 0; i < size; ++i) h = ((h >> 27) | (h << 5)) + data[i];
```

If it differs from the client's file, the client sends `action|refresh_item_data`.

## Item flags

`u16` at +0x62, the client's `ITEM_INFO_FLAG_*` names:

| Bit | Name | Bit | Name |
|---|---|---|---|
| `0x0001` | `FLIPPABLE` | `0x0100` | `BETA` |
| `0x0002` | `EDITABLE` | `0x0200` | `AUTOPICKUP` |
| `0x0004` | `SEEDLESS` | `0x0400` | `MOD` |
| `0x0008` | `PERMANENT` | `0x0800` | `RANDOM_GROW` |
| `0x0010` | `DROPLESS` | `0x1000` | `PUBLIC` |
| `0x0020` | `NO_SELF` | `0x2000` | `FOREGROUND` |
| `0x0040` | `NO_SHADOW` | `0x4000` | `HOLIDAY` |
| `0x0080` | `WORLDLOCKED` | `0x8000` | `UNTRADEABLE` |

`WORLDLOCKED`, `AUTOPICKUP` and `UNTRADEABLE` are placed by elimination; the rest were read from the
client's table and match the items that have them (locks are `PERMANENT` and `AUTOPICKUP`, the Fist and
Wrench `UNTRADEABLE`, portals `NO_SHADOW`).

## Item flags 2

`i32` at +0x64 (version 9+), the client's `ITEM_INFO_*` names:

| Bit | Name | Bit | Name |
|---|---|---|---|
| `0x00000001` | `ROBOT_DEADLY` | `0x00008000` | `TILE_DEADLY_IF_ON` |
| `0x00000002` | `ROBOT_SHOOT_LEFT` | `0x00010000` | `LONG_HAND_ITEM64x32` |
| `0x00000004` | `ROBOT_SHOOT_RIGHT` | `0x00020000` | `GEMLESS` |
| `0x00000008` | `ROBOT_SHOOT_DOWN` | `0x00040000` | `CLOTHES_TRANSMUTABLE` |
| `0x00000010` | `ROBOT_SHOOT_UP` | `0x00080000` | `ILLEGAL` |
| `0x00000020` | `ROBOT_CAN_SHOOT` | `0x00100000` | `ILLEGAL_INVENTORY_FLOAT` |
| `0x00000040` | `ROBOT_LAVA` | `0x00200000` | `ILLEGAL_WORLD` |
| `0x00000080` | `ROBOT_POINTY` | `0x00400000` | `UNUSED` |
| `0x00000100` | `ROBOT_SHOOT_DEADLY` | `0x00800000` | `ONE_IN_WORLD` |
| `0x00000200` | `GUILD_ITEM` | `0x01000000` | `ONLY_FOR_WORLD_OWNER` |
| `0x00000400` | `GUILD_FLAG` | `0x02000000` | `NO_UPGRADE` |
| `0x00000800` | `STARSHIP_HELM` | `0x04000000` | `EXTINGUISH_FIRE` |
| `0x00001000` | `STARSHIP_REACTOR` | `0x08000000` | `EXTINGUISH_FIRE_NO_DAMAGE` |
| `0x00002000` | `STARSHIP_VIEWSCREEN` | `0x10000000` | `NEED_RECEPTION_DESK` |
| `0x00004000` | `SUPER_MOD` | | |

`ROBOT_SHOOT_UP`, `ROBOT_CAN_SHOOT` and `ROBOT_SHOOT_DEADLY` are matched to bits by the items that have them
(Command - Shot Up, Shooter/Flame Bots); the others were read from the table. `GUILD_ITEM` tiles carry the
[common trailer](/guide/world-data#common-trailer) after their tile extra.

## Action types

The `u8` at +0x04. The client's `ITEM_TYPE_*` names (static initializer `0x157ae40`), with the first item
of each type in the 5.60 file. The table also has `ANY` (-1) and `ANY_BUT_SEED` (254) for its own
scripts. Which [tile extra](/guide/tile-extras) each type uses is on [World data](/guide/world-data#which-tiles-have-an-extra).

| Value | Name | Example item |
|---|---|---|
| 0 | `FIST` | Fist |
| 1 | `WRENCH` | Wrench |
| 2 | `USER_DOOR` | Door |
| 3 | `LOCK` | Small Lock |
| 4 | `GEMS` | Gems |
| 5 | `TREASURE` | Mystery Block |
| 6 | `DEADLY` | Death Spikes |
| 7 | `TRAMPOLINE` | Mushroom |
| 8 | `CONSUMABLE` | Devil Horns |
| 9 | `GATEWAY` | Portcullis |
| 10 | `SIGN` | Sign |
| 11 | `SFX_WITH_EXTRA_FRAME` | Toilet |
| 12 | `BOOMBOX` | Boombox |
| 13 | `DOOR` | Main Door |
| 14 | `PLATFORM` | Wooden Platform |
| 15 | `BEDROCK` | Bedrock |
| 16 | `LAVA` | Lava |
| 17 | `NORMAL` | Blank |
| 18 | `BACKGROUND` | Cave Background |
| 19 | `SEED` | Blank Seed |
| 20 | `CLOTHES` | Shades |
| 21 | `NORMAL_WITH_EXTRA_FRAME` | Evil Bricks |
| 22 | `BACKGD_SFX_EXTRA_FRAME` | Bubble Wrap |
| 23 | `BACK_BOOMBOX` | Art Wall |
| 24 | `BOUNCY` | Pinball Bumper |
| 25 | `POINTY` | Cactus |
| 26 | `PORTAL` | Time-Space Rupture |
| 27 | `CHECKPOINT` | Checkpoint |
| 28 | `MUSICNOTE` | Sheet Music: Blank |
| 29 | `ICE` | Ice |
| 30 | `RACE_FLAG` |  |
| 31 | `SWITCHEROO` | Dragon Gate |
| 32 | `CHEST` | Treasure Chest |
| 33 | `MAILBOX` | Mailbox |
| 34 | `BULLETIN` | Bulletin Board |
| 35 | `PINATA` | Ultra Pinata |
| 36 | `DICE` | Dice Block |
| 37 | `COMPONENT` | Chemical G |
| 38 | `PROVIDER` | Cow |
| 39 | `LAB` | Laboratory |
| 40 | `ACHIEVEMENT` | Achievement Block |
| 41 | `WEATHER_MACHINE` | Weather Machine - Sunny |
| 42 | `SCOREBOARD` | Scoreboard |
| 43 | `SUNGATE` | Sungate |
| 44 | `PROFILE` | Profile |
| 45 | `DEADLY_IF_ON` | Evil Eye |
| 46 | `HEART_MONITOR` | Heart Monitor |
| 47 | `DONATION_BOX` | Holiday Gift Box |
| 48 | `TOYBOX` |  |
| 49 | `MANNEQUIN` | Mannequin |
| 50 | `CAMERA` | Security Camera |
| 51 | `MAGICEGG` | Bunny Egg |
| 52 | `TEAM` | Staging Platform |
| 53 | `GAME_GEN` | Game Generator |
| 54 | `XENONITE` | Xenonite Crystal |
| 55 | `DRESSUP` | Phone Booth |
| 56 | `CRYSTAL` | Red Crystal |
| 57 | `BURGLAR` | Crime In Progress |
| 58 | `COMPACTOR` | Clothing Compactor |
| 59 | `SPOTLIGHT` | Spotlight |
| 60 | `WIND` | Summer Breeze |
| 61 | `DISPLAY_BLOCK` | Display Block |
| 62 | `VENDING` | Vending Machine |
| 63 | `FISHTANK` | Fish Tank Port |
| 64 | `PETFISH` | Goldfish |
| 65 | `SOLAR` | Solar Collector |
| 66 | `FORGE` | Forge |
| 67 | `GIVING_TREE` | Giving Tree |
| 68 | `GIVING_TREE_STUMP` | Giving Tree Stump |
| 69 | `STEAMPUNK` | Steam Gear |
| 70 | `STEAM_LAVA_IF_ON` | Steam Vent |
| 71 | `STEAM_ORGAN` | Steam Organ |
| 72 | `TAMAGOTCHI` | Silkworm |
| 73 | `SEWING` | Sewing Machine |
| 74 | `FLAG` | Country Flag |
| 75 | `LOBSTER_TRAP` | Lobster Trap |
| 76 | `ARTCANVAS` | Painting Easel |
| 77 | `BATTLE_CAGE` | Battle Pet Cage |
| 78 | `PET_TRAINER` | Pet Trainer |
| 79 | `STEAM_ENGINE` | Steam Engine |
| 80 | `LOCK_BOT` | Lock-Bot |
| 81 | `WEATHER_SPECIAL` | Weather Machine - Heatwave |
| 82 | `SPIRIT_STORAGE` | Spirit Storage Unit |
| 83 | `DISPLAY_SHELF` | Display Shelf |
| 84 | `VIP_DOOR` | VIP Entrance |
| 85 | `CHAL_TIMER` | Challenge Timer |
| 86 | `CHAL_FLAG` | Challenge Start Flag |
| 87 | `FISH_MOUNT` | Fish Wall Mount |
| 88 | `PORTRAIT` | Portrait |
| 89 | `WEATHER_SPECIAL2` | Weather Machine - Stuff |
| 90 | `FOSSIL` | Fossil Rock |
| 91 | `FOSSIL_PREP` | Fossil Prep Station |
| 92 | `DNA_MACHINE` | DNA Processor |
| 93 | `BLASTER` | Howler |
| 94 | `VALHOWLA` | Valhowla Treasure |
| 95 | `CHEMSYNTH` | Chemsynth Processor |
| 96 | `CHEMTANK` | Chemsynth Tank |
| 97 | `STORAGE` | Untrade-a-Box |
| 98 | `OVEN` | Commercial Oven |
| 99 | `SUPER_MUSIC` | Audio Gear |
| 100 | `GEIGERCHARGE` | Geiger Charger |
| 101 | `ADVENTURE_RESET` | The Adventure Begins |
| 102 | `TOMB_ROBBER` | Tomb Robber |
| 103 | `FACTION` | Balloon-O-Matic |
| 104 | `RED_FACTION` | Team Entrance - Punch |
| 105 | `GREEN_FACTION` | Team Entrance - Grow |
| 106 | `BLUE_FACTION` | Team Entrance - Build |
| 107 | `ARTIFACT` | Ancestral Totem of Wisdom |
| 108 | `TRAMPOLINE_MOMENTUM` | Lemon Jelly Block |
| 109 | `FISHGOTCHI_TANK` | Training Port |
| 110 | `FISHING_BLOCK` | Uranium Block |
| 111 | `ITEM_SUCKER` | MAGPLANT 5000 |
| 112 | `ITEM_PLANTER` | MAGPLANT 5000 Remote |
| 113 | `ROBOT` | ShockBot - Level 1 |
| 114 | `COMMAND` | Command - Move Left |
| 115 | `LUCKY_TICKET` | Lucky Token |
| 116 | `STATS_BLOCK` | GrowScan 9000 |
| 117 | `FIELD_NODE` | Containment Field Power Node |
| 118 | `OUIJA_BOARD` | Dark Spirit Board |
| 119 | `ARCHITECT_MACHINE` | World Architect |
| 120 | `STARSHIP` | Imperial Starship Helm - Mk.I |
| 121 | `AUTODELETE` |  |
| 122 | `BOOMBOX2` | Gravity Well |
| 123 | `AUTO_ACTION_BREAK` | Tesseract Manipulator |
| 124 | `AUTO_ACTION_HARVEST` | Heart of Gaia |
| 125 | `AUTO_ACTION_HARVEST_SUCK` | Techno-Organic Engine |
| 126 | `LIGHTNING_CLOUD` | Storm Cloud |
| 127 | `PHASED_BLOCK` | Cracked Stone Slab |
| 128 | `MUD` | Mud Puddle |
| 129 | `ROOT_CUTTING` | Bountiful Flowering Lattice Root Cutting |
| 130 | `PASSWORD_STORAGE` | Safe Vault |
| 131 | `PHASED_BLOCK_2` | Angelic Counting Cloud |
| 132 | `BOMB` | Mining Explosives |
| 133 | `PVE_NPC` |  |
| 134 | `INFINITY_WEATHER_MACHINE` | Infinity Weather Machine |
| 135 | `SLIME` | Ghost Block |
| 136 | `ACID` | Acid |
| 137 | `COMPLETIONIST` |  |
| 138 | `PUNCH_TOGGLE` | Waving Inflatable Arm Guy |
| 139 | `ANZU_BLOCK` |  |
| 140 | `FEEDING_BLOCK` | Pineapple Guzzler |
| 141 | `KRANKENS_BLOCK` | Kranken's Galactic Block |
| 142 | `FRIENDS_ENTRANCE` | Friends Entrance |
| 143 | `PEARLS` |  |
| 144 | `CONVEYOR_BELT` | Conveyor Belt |
| 145 | `CLIMB` | Climbing Wall |
| 254 | `ANY_BUT_SEED` |  |

<small>Readers: `0x1563a38`, `0x1574f08`; name decryption `0x1e742b0`; tables `0x157ae40`, `0x108ea9c`.</small>
