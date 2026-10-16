# Tile extras

A tile whose flags have bit `0x01` carries extra data after its record (see [World data](/guide/world-data)):
a `u8` type, then that type's bytes. This page lists every type the 5.60 client's parser
(`TileExtra_Serialize`, `0x15ce080`) knows, in the direction the client reads them from the server
([SEND_MAP_DATA 0x04](/packets/04-send-map-data) and [SEND_TILE_UPDATE_DATA 0x05](/packets/05-send-tile-update-data)).

- Which type a tile uses comes from its foreground item's **action type** in items.dat (`0x15d1014`, run when
  the foreground is set). If the server sends a type that doesn't match, the client reads the wrong bytes and
  the rest of the world is garbage.
- Some fields exist only in the client's own saved copy of a world. They are marked **not sent by the
  server**; don't send them.
- After the type's own bytes, items with a certain item flag have a common trailer. It is described on
  [World data](/guide/world-data).
- Numbers are little-endian. Strings are `u16 length` + bytes, with no terminator.

| Type | Name |
|---|---|
| [0x01](#0x01) | Door |
| [0x02](#0x02) | Sign |
| [0x03](#0x03) | Lock |
| [0x04](#0x04) | Seed |
| [0x05](#0x05) | (no data) |
| [0x06](#0x06) | Mailbox |
| [0x07](#0x07) | Bulletin board |
| [0x08](#0x08) | Dice block |
| [0x09](#0x09) | Provider |
| [0x0a](#0x0a) | Achievement block |
| [0x0b](#0x0b) | Heart monitor |
| [0x0c](#0x0c) | Donation box |
| [0x0d](#0x0d) | (mailbox layout) |
| [0x0e](#0x0e) | Mannequin |
| [0x0f](#0x0f) | Bunny egg |
| [0x10](#0x10) | Game block |
| [0x11](#0x11) | Game generator |
| [0x12](#0x12) | Xenonite crystal |
| [0x13](#0x13) | Phone booth |
| [0x14](#0x14) | Crystal |
| [0x15](#0x15) | Crime in progress |
| [0x16](#0x16) | Spotlight |
| [0x17](#0x17) | Display block |
| [0x18](#0x18) | Vending machine |
| [0x19](#0x19) | Fish tank port |
| [0x1a](#0x1a) | Solar collector |
| [0x1b](#0x1b) | Forge |
| [0x1c](#0x1c) | Giving Tree |
| [0x1d](#0x1d) | Giving Tree Stump |
| [0x1e](#0x1e) | Steam Organ |
| [0x1f](#0x1f) | Silkworm |
| [0x20](#0x20) | Sewing Machine |
| [0x21](#0x21) | Country Flag / Challenge flags |
| [0x22](#0x22) | Lobster Trap |
| [0x23](#0x23) | Painting Easel |
| [0x24](#0x24) | Battle Pet Cage |
| [0x25](#0x25) | Pet Trainer |
| [0x26](#0x26) | Steam Engine |
| [0x27](#0x27) | Lock-Bot |
| [0x28](#0x28) | Weather Machine (one setting) |
| [0x29](#0x29) | Spirit Storage Unit |
| [0x2a](#0x2a) | Data Bedrock |
| [0x2b](#0x2b) | Display Shelf |
| [0x2c](#0x2c) | VIP Entrance |
| [0x2d](#0x2d) | Challenge Timer |
| [0x2e](#0x2e) | (unused) |
| [0x2f](#0x2f) | Fish Wall Mount |
| [0x30](#0x30) | Portrait |
| [0x31](#0x31) | Weather Machine (several settings) |
| [0x32](#0x32) | Fossil Prep Station |
| [0x33](#0x33) | DNA Processor |
| [0x34](#0x34) | Howler / Trickster |
| [0x35](#0x35) | Chemsynth Tank |
| [0x36](#0x36) | Storage box |
| [0x37](#0x37) | Oven |
| [0x38](#0x38) | Audio Rack |
| [0x39](#0x39) | Geiger Charger |
| [0x3a](#0x3a) | Adventure Begins |
| [0x3b](#0x3b) | Tomb Robber |
| [0x3c](#0x3c) | Faction block |
| [0x3d](#0x3d) | Training Port |
| [0x3e](#0x3e) | Item Sucker (MAGPLANT) |
| [0x3f](#0x3f) | Robot |
| [0x40](#0x40) | Lucky Token |
| [0x41](#0x41) | (no data) |
| [0x42](#0x42) | GrowScan 9000 |
| [0x43](#0x43) | Containment Field Power Node |
| [0x44](#0x44) | Spirit Board |
| [0x45](#0x45) | Tesseract Manipulator |
| [0x46](#0x46) | Heart of Gaia |
| [0x47](#0x47) | Techno-Organic Engine |
| [0x48](#0x48) | Storm Cloud |
| [0x49](#0x49) | Phased block |
| [0x4a](#0x4a) | Safe Vault |
| [0x4b](#0x4b) | Angelic Counting Cloud |
| [0x4c](#0x4c) | PvE NPC |
| [0x4d](#0x4d) | Infinity Weather Machine |
| [0x4e](#0x4e) | Completionist |
| [0x4f](#0x4f) | Feeding block |
| [0x50](#0x50) | Kranken's block |
| [0x51](#0x51) | Friends Entrance |
| [0x52](#0x52) | (no data) |

## 0x01 Door {#0x01}

Doors, the Main Door, portals and the Sungate: items with action type 2 (Door), 13 (Main Door), 26 (Portal) and 43
(Sungate). Created by `0x15d1014` for those action types.

From the server (the 0x04 world load and 0x05 tile updates both pass "from server"):

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | label | the text shown over the door (extra+0x28) |
| u8 | flags | extra+9. Bit 3 (0x08): locked. The client then checks whether you may use it (`0x15b2a80`) and shows `` `w<Locked>`` `` instead of the label if you may not |

Not sent by the server: the client's own saved copy has three strings instead of one: extra+0x10, +0x28 (label), +0x40,
then the u8. +0x10 is shown in place of the label when it isn't empty, so it is probably the destination
(`WORLD:ID`) and +0x40 the door's id.

- The label is drawn by the tile-info code (`0x13002b4`). Item 9358 (0x248e) never shows its label.
- When the client writes a door that came from a server (only for its local copy) and the item isn't Gateway To
  Adventure (1682), Mystery Door (4718) or Mystery Portal (11136), it writes the destination if it has one, cut at `:`.

<small>Read by `0x15ce080` case 1 (falls through to the u8 of case 0x42); shown by `0x13002b4`.</small>

## 0x02 Sign {#0x02}

Signs, tombstones, banners and markers: item action type 10. Created by `0x15d1014`.

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | text | the sign's text (extra+0x28), shown in a bubble by the tile-info code (`0x13002b4`, through `0x15b1de8`) |
| u32 | value | extra+0xc. Not read by the sign display; gurotopia sends `-1`. Its meaning wasn't traced |

For seven items the text goes to extra+0x40 instead and isn't shown as a sign: Path Marker (1684), Carnival Landing (1912),
Gruesome Marker (4446), Objective Marker (4482), Hospital Chair (14678), Fashion Show Bouncer (15598) and Fashion Show
Voting Box (15600) (`0x15b17d0`). For those it is probably an id the item uses.

When the client writes a sign it filters the text first (`0x1585028`).

<small>Read by `0x15ce080` case 2.</small>

## 0x03 Lock {#0x03}

Every lock (Small/Big/Huge Lock, World Lock, Diamond Lock, Guild Lock, ...): item action type 3. Created by `0x15d1014`.

| Bytes | Field | Meaning |
|---|---|---|
| u8 | flags | extra+9: the lock's settings bits |
| u32 | owner | extra+0xc: the owner's user id |
| u32 | count | number of entries that follow |
| u32 × count | access | extra+0x80: user ids with access |
| u32 | (world version ≥ 12) | extra+0x138; meaning not traced |
| u32 | (world version ≥ 13) | extra+0x13c; meaning not traced |

The world version is the `u16` at the start of the world data (world+2). A tile update (0x05) uses the version of the
world that is loaded.

- Changing a tile away from its lock removes the lock's area (`0x15aef40` → `0x1625994`).
- The Guild Lock (5814) is followed by the guild block described in the common trailer, without its first u8.

<small>Read by `0x15ce080` case 3.</small>

## 0x04 Seed {#0x04}

A planted tree: item action type 19 (seeds). Created by `0x15d1014` with the age 0 and 3 fruit.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | age | extra+0x5c: seconds since it was planted. The client keeps counting from here |
| u8 | fruit | extra+0x60: how many fruit the tree has |

- The client adds the seconds that pass to the age by itself (`0x15d0b24`, run before every serialize and by `0x15d1a64`).
- The tile text (`0x15b2604`) shows the time left, the seed item's grow time (item+0xc4) minus the age, as
  "... to harvest", or `` `w(Punch to harvest)`` `` when it is ready.

<small>Read by `0x15ce080` case 4 (`switchD…caseD_4`).</small>

## 0x05 (no data) {#0x05}

Created by `0x15d1014` for item action type 30, with extra+9 = 2. No item in the 5.60 items.dat has that action type.

The switch in `0x15ce080` has no case for 5, so it carries no bytes of its own (only the common trailer, if the item's
flag asks for it).

## 0x06 Mailbox {#0x06}

Mailbox, Blue Mailbox, Hacker's Dialog, Message in a Bottle, Message in a Diamond Bottle: item action type 33.

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | string 1 | extra+0x10 |
| u16 len + bytes | string 2 | extra+0x28 |
| u16 len + bytes | string 3 | extra+0x40 |
| u8 | flag | extra+9 |

The same four fields are read for every type that shares this code (6, 7, 0x0c, 0x0d). Reading also clears extra+0x58.
The tile code in this range doesn't read the strings; they are probably filled only for the owner, and the byte
probably tells whether something is inside (neither was traced).

<small>Read by `0x15ce080` case 6 (shared with 7, 0x0c, 0x0d).</small>

## 0x07 Bulletin board {#0x07}

Bulletin Board, Letter, Guestbook, Scroll Bulletin, Retinal Scan Data Repository (action type 34), and the Security
Camera, Starship Security Camera and Pigeon (action type 50; created with extra+9 = 8).

Same layout as [0x06](#0x06): three strings (extra+0x10, +0x28, +0x40) and a u8 (extra+9).

## 0x08 Dice block {#0x08}

Dice Block and Roshambo Block: item action type 36.

| Bytes | Field | Meaning |
|---|---|---|
| u8 | value | extra+0x60: probably the face shown (the dice roll itself comes in TILE_APPLY_DAMAGE, 0x08) |

<small>Read by `0x15ce080` case 8 (`switchD…caseD_8`, shared with 0x10).</small>

## 0x09 Provider {#0x09}

Things that produce an item over time (Cow, Chicken, ATM Machine, Science Station, Coffee Maker, Well, Tackle Box, ...):
item action type 38.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | age | extra+0x5c: seconds since it was last collected; the client keeps counting |
| u32 | (only some items) | extra+100, read only for the Winterfest Calendar - 2017 (5318), and for the Well of Love (10656) when the world version is above 16 |

- The tile text (`0x15b45d0`) shows "Ready in ..." (the item's grow time, item+0xc4, minus the age) or
  "(`wPunch to collect``)".
- For the Well of Love it compares extra+100 with the grow time / 60 and shows "(n/m)", so that value is probably how
  many times it has been used.

<small>Read by `0x15ce080` case 9.</small>

## 0x0a Achievement block {#0x0a}

The Achievement Block (982): item action type 40. Created with extra+0x60 = 0x7f.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | value | extra+0xc (0 when created); probably the user id of the player whose achievement it shows (not traced) |
| u8 | achievement | extra+0x60: the icon drawn. 0–127 picks a frame of `game/amorkolg.rttex`, a negative value a frame of `game/amorkasd.rttex` (renderer `0x11a9ee4`) |

<small>Read by `0x15ce080` case 0x0a (u32, then the u8 of `caseD_8`).</small>

## 0x0b Heart monitor {#0x0b}

The Heart Monitor (1240): item action type 46.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | user | extra+0xc: probably the user id of the player it tracks |
| u16 len + bytes | name | extra+0x28: the player's name |

The tile text shows the name and `Status: Online`, or `` `4Offline`` ``. Online comes from the tile's "on" flag (tile
flags 0x40), not from the extra data.

<small>Read by `0x15ce080` case 0x0b (u32, then the string of case 0x40); shown by `0x13002b4`.</small>

## 0x0c Donation box {#0x0c}

Holiday Gift Box, Donation Box, Donut Donation Box: item action type 47.

Same layout as [0x06](#0x06): three strings (extra+0x10, +0x28, +0x40) and a u8 (extra+9).

## 0x0d (mailbox layout) {#0x0d}

Created for item action type 48. No item in the 5.60 items.dat has that action type.

Same layout as [0x06](#0x06): three strings and a u8.

## 0x0e Mannequin {#0x0e}

Mannequins (Mannequin, Holographic Mannequin, Snowtopian, the OMG/SAD/LOL/TROLL Mannequins, Shiny, Pearl and Diamond
Mannequin, Sandtopian): item action type 49. Created with an `AvatarData` object (extra+0x98) that holds the clothes.

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | label | extra+0x28: text, shown like a sign's (`0x15b1de8` treats types 2 and 0x0e as signs) |
| u8 | flag | extra+9 |
| u32 | value | extra+0x58 |
| u16 × 9 | clothes | item ids of the 9 clothing slots, copied into the AvatarData (+0x14), probably in the [OnSetClothing](/functions/OnSetClothing) order (hair, shirt, legs, feet, face, hand, back, head, charm). The tint is set to `0xb4b4b4ff` |
| u32, u32 | (only if a slot holds Will of the Wild (5712) or Golem's Gift (10044), world version ≥ 4) | ORed into AvatarData+0x28 and +0x2c; probably those items' extra state bits |

The renderer (`0x11a9ee4`) draws the AvatarData on the tile.

<small>Read by `0x15ce080` case 0x0e; AvatarData setters `0x14ce8f8`, `0x14ce85c`.</small>

## 0x0f Bunny egg {#0x0f}

The Bunny Egg (610): item action type 51.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | count | extra+0x5c. The client doesn't age this type (`0x15d0b24` skips it), so it is a plain counter, probably the eggs put in |

Types 0x1b, 0x26, 0x27, 0x32 and 0x39 share this one-u32 code.

<small>Read by `0x15ce080` case 0x0f (`switchD…caseD_f`).</small>

## 0x10 Game block {#0x10}

The team items of the game blocks (Staging Platform, Game Block, Game Flag, Game Grave, Game Goal, Game Egg, ...):
item action type 52. Created with extra+0x60 = 4.

| Bytes | Field | Meaning |
|---|---|---|
| u8 | team | extra+0x60: the team the block belongs to. The touch code compares it with the player's team (avatar+0x26d) to decide whether the flag, goal or grave reacts. 4 (the default) is probably "no team" |

Same code as [0x08](#0x08).

<small>Read by `0x15ce080` case 0x10; compared in `0x13002b4`.</small>

## 0x11 Game generator {#0x11}

The Game Generator (1660): item action type 53.

The switch in `0x15ce080` has no case for 0x11, so it carries no bytes of its own.

## 0x12 Xenonite crystal {#0x12}

The Xenonite Crystal (2072): item action type 54.

| Bytes | Field | Meaning |
|---|---|---|
| u8 | flags | extra+9: probably the effects it turns on in the world (not traced) |
| u32 | value | extra+0x5c. Not aged by the client |

Type 0x1a reads the same way.

<small>Read by `0x15ce080` case 0x12.</small>

## 0x13 Phone booth {#0x13}

Phone Booth (2208) and Transmutabooth (9170): item action type 55.

| Bytes | Field | Meaning |
|---|---|---|
| u16 × 9 | clothes | 9 item ids, as in [0x0e](#0x0e). They are copied only if the extra has an AvatarData, which `0x15d1014` creates only for mannequins, so for these items the 18 bytes are skipped |

Reading also stores the current tick in extra+0x58.

<small>Read by `0x15ce080` case 0x13.</small>

## 0x14 Crystal {#0x14}

The Red, Green, Blue, White and Black Crystal: item action type 56.

From the server:

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | text | extra+0x10; probably the crystal sequence (not traced) |

Not sent by the server: only the client's saved copy adds the u32 count + u32 list of type 0x20.

<small>Read by `0x15ce080` case 0x14 (then case 0x33, which reads nothing from a server).</small>

## 0x15 Crime in progress {#0x15}

Crime In Progress (2302): item action type 57.

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | text | extra+0x10; probably the villain's name (not traced) |
| u32 | age | extra+0x5c: seconds; the client keeps counting |
| u8 | value | extra+0x60 |

Reading clears extra+0xc. The tile-info code shows something for this type (or for item 3528) through `0x15b1e40`.

<small>Read by `0x15ce080` case 0x15 (the string, then `caseD_4`, like a seed).</small>

## 0x16 Spotlight {#0x16}

The Spotlight (2646): item action type 59.

No bytes. Reading only clears extra+0xc.

<small>`0x15ce080` case 0x16.</small>

## 0x17 Display block {#0x17}

The Display Block (2946): item action type 61.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | item | extra+0xc: the item shown in the block. The renderer draws that item's icon on it (`0x11a9ee4`, item 0xb82) |

Reading clears extra+0x58.

<small>Read by `0x15ce080` case 0x17.</small>

## 0x18 Vending machine {#0x18}

Vending Machine (2978) and DigiVend Machine (9268): item action type 62.

From the server:

| Bytes | Field | Meaning |
|---|---|---|
| u32 | item | extra+0x58: the item for sale, 0 if none |
| i32 | price | extra+0xc. Above 0: World Locks per item. Below 0: that many items per World Lock |

Not sent by the server: the client's saved copy adds a u32 stock (extra+0x5c) and a u32 (extra+100, probably the World Locks earned),
and turns tile flags 0x40 and 0x200 on or off from them. When it writes a machine whose items-per-lock is more than
its stock, it writes item 0.

The tile text (`0x13002b4`) shows `Selling `2&lt;item>`` ` ... ` World Locks each` or ` per World Lock`, or
`` `wOUT OF ORDER`` `` when the item or price is 0. Vending Hub - Checkout Counter (9270) doesn't show it.

<small>Read by `0x15ce080` case 0x18.</small>

## 0x19 Fish tank port {#0x19}

The Fish Tank Port (3002): item action type 63.

| Bytes | Field | Meaning |
|---|---|---|
| u8 | flags | extra+9 |
| u32 | count | number of u32 values that follow |
| u32 × count | values | extra+0x80; probably pairs of fish item id and weight (not traced) |

<small>Read by `0x15ce080` case 0x19 (u8, then the list of `caseD_20`).</small>

## 0x1a Solar collector {#0x1a}

The Solar Collector (3078): item action type 65. Created with extra+9 = 0x18.

| Bytes | Field | Meaning |
|---|---|---|
| u8 | mode | extra+9: bits 0x08 and 0x10 pick the text "Only works when planting", "Only works when splicing" or "Disabled" |
| u32 | charge | extra+0x5c: seconds of charge; the client keeps counting. Full at 86400 (one day) |

The tile text (`0x15b4298`) shows `Solar Collector`, then `n% charged` (charge × 100 / 86400) or `Fully charged!`, then
the mode.

<small>Read by `0x15ce080` case 0x1a (same code as 0x12).</small>

## 0x1b Forge {#0x1b}

The Forge (3194): item action type 66.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | time | extra+0x5c: seconds. Unlike most types the client counts this one **down** to 0 (`0x15d0b24`), so it is probably the time left on the current job |

Same code as [0x0f](#0x0f).

<small>Read by `0x15ce080` case 0x1b.</small>

## 0x1c Giving Tree {#0x1c}

Item action type 67, the **Giving Tree** (3200). It grows a gift you can punch out.

| Bytes | Field | Meaning |
|---|---|---|
| u8 | flags (extra+9) | bit 0: no tooltip is shown (probably "already harvested") |
| u32 | age (+0x5c) | seconds since planting; the client keeps adding real time to it |
| u8 | decorated (+0x60) | percent decorated; shown as "`N% Decorated`" when non-zero |

- Tooltip (`0x15b30f4`): "`` `7Giving Tree`` ``", then "`&lt;time> to gift!`" while `item.growTime − age > 0`
  (item+0x13c), otherwise " (`` `wPunch to nab a gift!`` ``)" if you have access to the tile.

<small>Read by `0x15ce080`; tooltip `0x15b30f4`; timer `0x15d0b24`.</small>

## 0x1d Giving Tree Stump {#0x1d}

Item action type 68, the **Giving Tree Stump** (3202).

No bytes. When reading, the client starts a local timer (+0x58 = now, +0x5c = 600), which its tick
function then counts up like any other age field.

<small>Read by `0x15ce080`.</small>

## 0x1e Steam Organ {#0x1e}

Item action type 71, the **Steam Organ** (3282).

| Bytes | Field | Meaning |
|---|---|---|
| u8 | +0x60 | not traced |
| u32 | +0xc | not traced |

The renderer draws steam pieces (action types 69 and 71) with a frame picked from their neighbours, not
from these values. No reader of the two fields was found.

<small>Read by `0x15ce080`.</small>

## 0x1f Silkworm {#0x1f}

Item action type 72, the **Silkworm** (3316). A pet that needs food and water and makes silk.

| Bytes | Field | Meaning |
|---|---|---|
| u8 | flags (+9) | bit 0: dead. Bit 5 is used locally for its blink animation |
| u16 len + bytes | name (+0x10) | shown as "`` `7<name> the Silkworm`` ``" |
| u32 | age (+0x5c) | seconds; it dies of old age after 1,728,000 s (20 days) |
| u32 | silk (+0x64) | at 86,400 or more the tooltip says "(Punch to collect silk)" |
| u32 | +0xc | probably the illness timer: counts down; while it is above 0 the tooltip says "Feeling ill." |
| u8 | +0x60 | reset to 0 when the +0xc timer ends (probably the illness kind) |
| u32 | food (+0xa8+0) | seconds of food left; starts at 21,600 (6 h) |
| u32 | water (+0xa8+4) | seconds of water left; starts at 21,600 |
| u32 | colour (+0xa8+8) | RGBA; a new silkworm gets a random colour |
| u32 | neglect (+0xa8+0xc) | seconds without food or water; above 86,400 (1 day) it dies |

The last four u32s are read **only if the tile's item is a Silkworm**: the 16-byte block is allocated when
the foreground is set, so it is absent for any other item.

- The tooltip adds a status line when food or water is below about 43,300 s or above 259,200 s (3 days):
  probably "Hungry!"/"Thirsty!" when low and "Stuffed full!"/"Bloated!" when high (the strings are all in the
  tooltip function, but which test picks which wasn't pinned down).
- The client ages it itself between updates (`0x15d0b24`): food and water count down, neglect counts up,
  silk grows after its first day. A dead worm's tooltip says "R.I.P. Died at N days of old age / illness /
  starvation / thirst / neglect".

<small>Read by `0x15ce080`; tooltip `0x15b3bb0`; timer `0x15d0b24`; getters `0x15d1a8c`, `0x15d1acc`, `0x15d1b0c`; drawn by `0x11b220c`.</small>

## 0x20 Sewing Machine {#0x20}

Item action type 73, the **Sewing Machine** (3354).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | count | number of values |
| u32 × count | list (+0x80) | the project. Entry 0 is an item id shown as "Current project:\n&lt;item name>". With more entries, entry 1 is a small number (below 7 it adds a line) and entry 2 is another item whose name is shown |

The exact meaning of entries 1 and 2 is probably the step and the next bolt; it wasn't traced further.

<small>Read by `0x15ce080`; tooltip `0x15b4004`.</small>

## 0x21 Country Flag / Challenge flags {#0x21}

Item action type 74, the **Country Flag** (3394), and action type 86, the **Challenge Start Flag** (3806) and
**Challenge End Flag** (3808).

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | country (+0x10) | **only if the tile is a Country Flag (3394)**: the country code. The renderer draws `interface/flags/<code>.rttex` on it |

For the challenge flags (or any other item) a server sends **no bytes** for this type.

<small>Read by `0x15ce080`; drawn in `0x11a9ee4`.</small>

## 0x22 Lobster Trap {#0x22}

Item action type 75, the **Lobster Trap** (3448).

No bytes from a server. Two u32s (+0x5c, +0x64) exist only in the client's own saved copy.

<small>Read by `0x15ce080`.</small>

## 0x23 Painting Easel {#0x23}

Item action type 76, the **Painting Easel** (3528).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | +0x64 | probably the painted item's id (not traced) |
| u16 len + bytes | label (+0x10) | shown in a speech bubble when you point at the easel |

<small>Read by `0x15ce080`; tooltip `0x13002b4`.</small>

## 0x24 Battle Pet Cage {#0x24}

Item action type 77, the **Battle Pet Cage** (3548).

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | name (+0x10) | the pet's name, shown in a speech bubble when you point at the cage |
| u32 | +0x64 | not traced (probably the pet or one of its abilities) |
| u32 | +0x58 | not traced |
| u32 | +0x5c | not traced (this type has no client timer, so it isn't an age) |

<small>Read by `0x15ce080`; tooltip `0x13002b4`.</small>

## 0x25 Pet Trainer {#0x25}

Item action type 78: the **Pet Trainer** (3554), **Pet Battle Gym Leader** (15222) and **Pet Battle Gym Trainer** (15224).

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | name (+0x10) | probably the trainer's name |
| u32 | count | number of list values |
| u32 | +0x5c | age in seconds (counted up by the client) |
| u32 × count | list (+0x80) | probably the trainer's battle pets (item ids) |

The count comes **before** the +0x5c value, and the list after it. A u16 string (+0x40) follows only in
the client's own saved copy (world version above 23), never from a server.
New trainers are registered with the pet-battle manager (`0x14d1e54`).

<small>Read by `0x15ce080`; created by `0x15d1014`.</small>

## 0x26 Steam Engine {#0x26}

Item action type 79, the **Steam Engine** (3558).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | temperature (+0x5c) | shown as "`` `4Steam Engine`` ``\n`&lt;N> degrees`"; the client lowers it by 1 each second (not below 0) |

<small>Read by `0x15ce080`; tooltip `0x15b3728`; timer `0x15d0b24`.</small>

## 0x27 Lock-Bot {#0x27}

Item action type 80, the **Lock-Bot** (3682).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | +0x5c | seconds, counted up by the client (probably how long it has been running) |

<small>Read by `0x15ce080`.</small>

## 0x28 Weather Machine (one setting) {#0x28}

Item action type 81: **Weather Machine - Heatwave** (3694), **Balloon Warz** (4892), **Background** (5000),
**Valentine's** (5654), **St. Paddy's Day** (5716), **Digital Rain** (6854), **Black Digital Rain** (15802).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | setting (+0x64) | the machine's one setting. A new machine starts at `0x4080ff00`, so for Heatwave it's probably a colour; for Background it's probably an item id |

<small>Read by `0x15ce080`; default from `0x15d1014`.</small>

## 0x29 Spirit Storage Unit {#0x29}

Item action type 82, the **Spirit Storage Unit** (3724).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | ghosts (+0x64) | ghosts stored. The tooltip shows `ghosts × 5`% of capacity; at 21 or more it turns red and adds "RISK OF EXPLOSION" |

<small>Read by `0x15ce080`; tooltip `0x15b4c90`.</small>

## 0x2a Data Bedrock {#0x2a}

Item action type 15 (bedrock) when the item has tile data: **Data Bedrock** (3760), **Data Starship Hull** (6546).

| Bytes | Field | Condition | Meaning |
|---|---|---|---|
| u8 | | always | read and thrown away |
| u32 | +0xe0 | world version > 18 | not traced (default 1) |
| u32 | +0xe4 | world version > 18 | not traced (default 1) |
| u32 | +0xe8 | world version > 18 | not traced (default 1) |
| u32 | +0x11c | world version > 19 | not traced (default 0) |
| u32 | +0x118 | world version > 19 | not traced (default −1) |

Six more values (+0x60, +0xec, +0x114, +0x120, +0x13c) exist only in the client's own saved copy.
For the Data Starship Hull (6546) the common trailer adds starship values; see that section.

<small>Read by `0x15ce080`; defaults from `0x15d1014`.</small>

## 0x2b Display Shelf {#0x2b}

Item action type 83: **Display Shelf** (3794), **Spooky Display Shelf** (10190), **Black Display Shelf** (10552), **Shirt Rack** (14962).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | +0x64 | item shown top right |
| u32 | +0xc | item shown top left |
| u32 | +0x58 | item shown bottom left |
| u32 | +0x5c | item shown bottom right |

The renderer draws each of the four items at 35% scale in its corner, plus a faint offset copy (probably a
shadow) when the detail setting (app+0xbd0) is above 0.5.

<small>Read by `0x15ce080`; drawn in `0x11a9ee4` (action type 0x53).</small>

## 0x2c VIP Entrance {#0x2c}

Item action type 84, the **VIP Entrance** (3798).

| Bytes | Field | Meaning |
|---|---|---|
| u8 | flags (+9) | probably like a lock's flags (for example "open to everyone") |
| u32 | +0xc | probably the owner's user id |
| u32 | count | number of list values |
| u32 × count | list (+0x80) | probably the user ids that may enter |

It has the same layout as a lock's first fields. Its readers weren't traced.

<small>Read by `0x15ce080`.</small>

## 0x2d Challenge Timer {#0x2d}

Item action type 85, the **Challenge Timer** (3804).

No bytes from a server. A string, four u32s and a u8 exist only in the client's own saved copy, and +0x60 is
reset to 0 on every read.

<small>Read by `0x15ce080`.</small>

## 0x2e (unused) {#0x2e}

Not used by the 5.60 client: no `case` reads it, and no item action type creates it. The type byte is read
and nothing else.

## 0x2f Fish Wall Mount {#0x2f}

Item action type 87: **Fish Wall Mount** (3810), **Fancy Fish Wall Mount** (5624), **Crab Wall Mount** (6328).

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | label (+0x10) | not traced (probably the catcher's name or the fish's name) |
| u32 | fish (+0x64) | the item id of the mounted fish; when it isn't 0 the renderer draws it at 70% scale |
| u8 | +0x60 | probably the fish's weight in pounds (not traced) |

<small>Read by `0x15ce080`; drawn in `0x11a9ee4` (action type 0x57).</small>

## 0x30 Portrait {#0x30}

Item action type 88: **Portrait** (3818), **Posh Portrait** (11196), **Heart Portrait** (15950). A painting of a player's head.

| Bytes | Field | Condition | Meaning |
|---|---|---|---|
| u16 len + bytes | label (+0x10) | always | shown in a speech bubble when you point at it |
| u32 | +0x64 | always | the portrait is only drawn when this isn't 0; `value − 1` goes to the drawn avatar (probably the expression) |
| u32 | +0x5c | always | passed to the drawn avatar (not traced) |
| u32 | +0x58 | always | passed to the drawn avatar (not traced) |
| u32 | skin (clothes+8) | always | probably the skin colour |
| u16 | face | always | clothing slot 4 |
| u16 | hat | always | clothing slot 0 |
| u16 | hair | always | clothing slot 7 |
| u32, u32 | flags | world version > 3, and one of the three items is 5712 (Will of the Wild) or 10044 (Golem's Gift) | OR-ed into the clothes' flag words (+0x28, +0x2c), probably those items' look settings |
| u32 | head skin | world version > 8 | picks `game/player_head_skin<N>.rttex` (default 6) |
| u16 len + bytes | crown settings (+0x28) | world version > 22, and the hat is 12958 (Infinity Crown) | the Infinity Crown's look string |

The renderer builds a small avatar from these values and draws it in the frame.

<small>Read by `0x15ce080`; drawn in `0x11a9ee4` (action type 0x58); tooltip `0x13002b4`; clothes object `0x14ce7bc`.</small>

## 0x31 Weather Machine (several settings) {#0x31}

Item action type 89: **Weather Machine - Stuff** (3832), **Epoch Machine** (5958), **Weather Machine - Guild** (6280),
**Concert Lights** (16094), **Paradise City** (16406).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | +0x64 | default 2. For "Stuff" probably the item that falls (2 = Dirt) |
| u32 | +0xc | default 50. For "Stuff" probably the gravity |
| u8 | flags (+9) | probably option bits (for example spin or invert) |

The meanings are probably right for "Stuff"; the other machines reuse the fields differently, which wasn't traced.

<small>Read by `0x15ce080`; defaults from `0x15d1014`.</small>

## 0x32 Fossil Prep Station {#0x32}

Item action type 91, the **Fossil Prep Station** (3938).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | +0x5c | seconds left; the client lowers it by 1 each second (not below 0). Probably the time until the fossil is prepared |

<small>Read by `0x15ce080`; timer `0x15d0b24`.</small>

## 0x33 DNA Processor {#0x33}

Item action type 92, the **DNA Processor** (4080).

No bytes from a server. A u32 count plus that many u32s exist only in the client's own saved copy.

<small>Read by `0x15ce080`.</small>

## 0x34 Howler / Trickster {#0x34}

Item action type 93: **Howler** (4344), **Trickster** (8020).

No bytes from a server. The client's own saved copy has a u8 (+9), a u8 (+0x60, clamped to 2–20, default 10)
and a u32 (+0x64, clamped to 10–250, default 100).

<small>Read by `0x15ce080`; defaults from `0x15d1014`.</small>

## 0x35 Chemsynth Tank {#0x35}

Item action type 96, the **Chemsynth Tank** (4432).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | +0x64 | not traced (probably the chemical's item id) |
| u32 | +0xc | not traced |

Unusually, these two values are read **only from a server**; the client's own saved copy has no bytes.

<small>Read by `0x15ce080`.</small>

## 0x36 Storage box {#0x36}

Item action type 97: **Untrade-a-Box** (4516), **Storage Box Xtreme** Levels 1–3 (6286–6290), **Dynasty Vase** (10584).

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | +0x10 | not traced (the stored items aren't in the tile data) |

<small>Read by `0x15ce080`.</small>

## 0x37 Oven {#0x37}

Item type 98 (`ITEM_TYPE_OVEN`): Commercial Oven, Home Oven, Master Chef's Oven, Replicator, Taco Truck Oven.
What is in the oven, the heat, and how long it has cooked.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | heat | 0 off, 1 low, 2 medium, 3 high (the description shows "Cooking on Low/Medium/High"); 0 = no description |
| u32 | n | number of u32 values that follow (2 per ingredient) |
| n × u32 | ingredients | pairs of (item id, heat received so far) |
| u32 | timer | seconds counted since the last update (the client adds to it every frame) |
| u64 | started | only if world version > 13: a Unix time; the description adds "Elapsed Sec:" since then |

Only sent this way **from the server**. In the client's own save format (`fromServer` false) the type has no data.

- Every update the client adds `heat × seconds` to the second value of each pair, so cooking goes on
  between server updates (`0x15d0b24`).
- The description (`0x15b5234`) lists each ingredient with a doneness word chosen by comparing its
  value with the item's cook time from items.dat (item+0x4c, -1 = not cookable): Raw, Cold, Uncooked,
  Underdone, Cooked, Perfect, Well-Done, Overcooked, Burnt. Salt, Pepper, Sugar (4568, 4570, 4572) and item
  726 are left out.
- With heat > 0 the oven is drawn with its "lit" frame, and the nearest lit oven plays the item's sound
  (`0x11a6a9c`).

<small>Read by `0x15ce080` (case 0x37); used by `0x15d0b24`, `0x15b5234`, `0x11a6a9c`.</small>

## 0x38 Audio Rack {#0x38}

Item type 99 (`ITEM_TYPE_SUPER_MUSIC`): Audio Gear, Audio Rack. A short tune that plays when you walk past.

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | notes | the tune, see below |
| u32 | volume | sound volume in percent (played at `volume / 100`); 0 or less = silent, not drawn as active |

The notes are read 3 characters at a time: an instrument letter, a note, and an accidental.
- Instrument: `B` bass, `D` drum, `E` electric guitar, `F` flute, `G` Spanish guitar, `L` lyre, `P` piano,
  `S` sax, `T` Mexican trumpet, `V` violin (the letters the parser accepts; the file each one plays is
  probably the instrument it starts with). A space is a rest (one character).
- Note: `a`–`g` or `A`–`G` (the two cases are probably two octaves).
- Accidental: `#` sharp, `b` flat, anything else natural.
Parsing stops at the first character that doesn't fit. The sounds are `audio/notes/<instrument>_<n>.wav`.

<small>Read by `0x15ce080` (case 0x38); used by `0x11a50bc`, `0x11a497c`.</small>

## 0x39 Geiger Charger {#0x39}

Item type 100 (`ITEM_TYPE_GEIGERCHARGE`): Geiger Charger.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | timer | seconds counted so far; the client keeps adding the elapsed seconds every update (probably the charging time) |

<small>Read by `0x15ce080` (case 0x39, shared code with types 0x0f/0x1b/0x26/0x27/0x32); timer in `0x15d0b24`.</small>

## 0x3a Adventure Begins {#0x3a}

Item type 101 (`ITEM_TYPE_ADVENTURE_RESET`): The Adventure Begins.

**From the server: no data.** The fields exist only in the client's own save format (`fromServer` false):
u8, u32, then a u16-length string.

<small>Read by `0x15ce080` (case 0x3a).</small>

## 0x3b Tomb Robber {#0x3b}

Item type 102 (`ITEM_TYPE_TOMB_ROBBER`): Tomb Robber.

**From the server: no data.** In the client's own save format (`fromServer` false) it holds two u16-length
strings and a u8.

<small>Read by `0x15ce080` (case 0x3b).</small>

## 0x3c Faction block {#0x3c}

Item types 103–106 (`ITEM_TYPE_FACTION`, `RED_FACTION`, `GREEN_FACTION`, `BLUE_FACTION`): Balloon-O-Matic,
Team Entrance - Punch, Team Entrance - Grow, Team Entrance - Build.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | value | not traced |
| u8 | faction | 0 Balloon-O-Matic, 1 punch, 2 grow, 3 build (the client sets it from the item type when the block is placed) |

For the Balloon-O-Matic (item type 103) the faction byte is added to the sprite frame, so it shows the team
colour (`0x11a6a9c`).

<small>Read by `0x15ce080` (case 0x3c); used by `0x11a6a9c`.</small>

## 0x3d Training Port {#0x3d}

Item type 109 (`ITEM_TYPE_FISHGOTCHI_TANK`): Training Port (5530). A fish being trained.

The data is read into a sub-object that the client creates only when the foreground's item type is 109.
If the tile's foreground isn't a Training Port, **nothing is read** and the rest of the world is parsed
from the wrong offset.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | size | the fish's size, passed with the fish id when the fish is drawn swimming in the port (as the pounds value of a Fish Tank fish) |
| u8 | ? | not traced |
| u8 | done | 1 = training finished: the timer stops and the fish swims differently |
| u32 | fish | the fish's item id; 0 = empty port (the client redraws the fish when it changes between 0 and not 0) |
| u32 | ? | not traced |
| u32 | remaining | counts down by `rate` per second |
| u32 | progress | goes up once each time `remaining` runs out (one step per `rate` units) |
| u32 | ? | when it changes and isn't 0, the client rebuilds the fish (probably its level or look) |
| u32 | rate | units per second (see above) |
| u32 | target | when `progress` passes it, `done` is set |
| u8 | paused | 1 = the timer doesn't run |

<small>Read by `0x15ce080` (case 0x3d); timer in `0x15d0b24`; fish drawing `0x1844e18`, `0x1845364`; packet 0x05 handler in `0x1373e20`.</small>

## 0x3e Item Sucker (MAGPLANT) {#0x3e}

Item type 111 (`ITEM_TYPE_ITEM_SUCKER`): MAGPLANT 5000, Gaia's Beacon, Unstable Tesseract. It collects one
kind of item.

The first four fields go into a sub-object the client creates only when the foreground's item type is
111. Otherwise **nothing is read** for them.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | item | the item it collects; drawn as an icon on the block; 0 = not set |
| u32 | count | how many it holds; the block blinks when `count` reaches capacity − 25 |
| u8 | ? | not traced |
| u8 | look | picks one of two frames for the "has an item" overlay (probably on/off) |
| u32 | capacity | only from the server: the maximum count. The client writes the item's own limit here when it saves |

<small>Read by `0x15ce080` (case 0x3e); drawn in `0x11a9ee4`; world list in `0x15af7b8`.</small>

## 0x3f Robot {#0x3f}

Item type 113 (`ITEM_TYPE_ROBOT`): ShockBot, SpikeBot, ShooterBot, FlameBot, SearBot (all levels). The
bot's program, a list of command blocks.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | n | number of commands |
| n × entry | commands | see below |
| u32 | ? | not traced (the client has no timer for this type) |
| u32 | state | 1 or more: the bot is drawn with its active frame (+2) |

Each entry, in order:

| Bytes | Meaning |
|---|---|
| u32 | the command block's item id. The robot (`0x1943d38`) turns each into a move: the item's flags (item+0x64) pick the command kind ("Adding Command", "Adding Mirror Command") |
| u8 | not traced |
| u32 | not traced |
| u32 | not traced |
| u16 len + bytes | a string, not traced |

<small>Read by `0x15ce080` (case 0x3f); robots built in `0x1943950`/`0x1943d38`; frame in `0x11a6a9c`.</small>

## 0x40 Lucky Token {#0x40}

Item type 115 (`ITEM_TYPE_LUCKY_TICKET`): Lucky Token and the Year of the … Lucky Tokens.

| Bytes | Field | Meaning |
|---|---|---|
| u16 len + bytes | text | not traced (probably the owner's name or a message) |

<small>Read by `0x15ce080` (case 0x40, same code as the end of 0x0b).</small>

## 0x41 (no data) {#0x41}

Not a case in the 5.60 parser, so the type byte is followed by nothing. The client gives this type to a new
tile extra when the item's "has extra" flag (item+0x65 bit 1) is set but its item type maps to no other
extra type.

<small>Default in `0x15ce080`; set in `0x15aef40`.</small>

## 0x42 GrowScan 9000 {#0x42}

Item type 116 (`ITEM_TYPE_STATS_BLOCK`): GrowScan 9000.

| Bytes | Field | Meaning |
|---|---|---|
| u8 | flags | not traced |

<small>Read by `0x15ce080` (case 0x42, the same byte as the end of type 0x01).</small>

## 0x43 Containment Field Power Node {#0x43}

Item type 117 (`ITEM_TYPE_FIELD_NODE`): Containment Field Power Node.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | value | not traced |
| u32 | n | number of values |
| n × u32 | list | not traced (probably the linked nodes) |

<small>Read by `0x15ce080` (case 0x43).</small>

## 0x44 Spirit Board {#0x44}

Item type 118 (`ITEM_TYPE_OUIJA_BOARD`): Spirit Board, Dark Spirit Board.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | value | not traced |
| u16 len + bytes | text 1 | not traced |
| u16 len + bytes | text 2 | not traced |
| u32 | n | number of values |
| n × u32 | list | not traced |

<small>Read by `0x15ce080` (case 0x44).</small>

## 0x45 Tesseract Manipulator {#0x45}

Item type 123 (`ITEM_TYPE_AUTO_ACTION_BREAK`): Tesseract Manipulator. It breaks blocks by itself.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | fuel | probably the gems it has left: with 0 an extra "empty" overlay frame is drawn on the block |
| u32 | ? | not traced |
| u32 | target | the item it works on; drawn as an icon on the block, 0 = not set |
| u32 | on | only if world version > 7: not 0 = running, the block animates |

<small>Read by `0x15ce080` (case 0x45, shared with 0x46); drawn in `0x11a9ee4`.</small>

## 0x46 Heart of Gaia {#0x46}

Item type 124 (`ITEM_TYPE_AUTO_ACTION_HARVEST`): Heart of Gaia. It harvests trees by itself.

Same layout and meanings as [0x45](#0x45).

<small>Read by `0x15ce080` (case 0x46).</small>

## 0x47 Techno-Organic Engine {#0x47}

Item type 125 (`ITEM_TYPE_AUTO_ACTION_HARVEST_SUCK`): Techno-Organic Engine. It harvests and collects.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | fuel | as in [0x45](#0x45) |
| u32 | ? | not traced |
| u32 | target | the item it works on |
| u32 | on | only if world version > 7: not 0 = running |
| u32 | item | storage sub-object: the item it holds (only read if the foreground's item type is 125, like [0x3e](#0x3e)) |
| u32 | count | storage: how many |
| u8 | ? | storage: not traced |
| u8 | look | storage: frame choice |
| u32 | offset | added to `target` to get the icon drawn on the block (probably 1 = show the target's seed) |
| u32 | ? | not traced |

If the foreground isn't item type 125, the four storage fields are **not read** and the parse goes out of step.

<small>Read by `0x15ce080` (case 0x47); drawn in `0x11a9ee4`.</small>

## 0x48 Storm Cloud {#0x48}

Item type 126 (`ITEM_TYPE_LIGHTNING_CLOUD`): Storm Cloud.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | ? | not traced (0 when placed) |
| u32 | ? | not traced (1 when placed) |
| u32 | ? | not traced (0 when placed) |

<small>Read by `0x15ce080` (case 0x48); defaults from `0x15d1014`.</small>

## 0x49 Phased block {#0x49}

Item type 127 (`ITEM_TYPE_PHASED_BLOCK`): Cracked Stone Slab, Dunking Bucket.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | value | not traced |

<small>Read by `0x15ce080` (case 0x49, same code as 0x28/0x29/0x4e/0x4f).</small>

## 0x4a Safe Vault {#0x4a}

Item type 130 (`ITEM_TYPE_PASSWORD_STORAGE`): Safe Vault.

**From the server: no data.** In the client's own save format (`fromServer` false) it holds three u16-length
strings. The server keeps the password and contents to itself.

<small>Read by `0x15ce080` (case 0x4a).</small>

## 0x4b Angelic Counting Cloud {#0x4b}

Item type 131 (`ITEM_TYPE_PHASED_BLOCK_2` in the client's name table): Angelic Counting Cloud (9346).

| Bytes | Field | Meaning |
|---|---|---|
| u32 | number | added to the sprite frame, so it picks the digit the cloud shows |
| u16 len + bytes | text | not traced |

<small>Read by `0x15ce080` (case 0x4b); frame in `0x11a6a9c`.</small>

## 0x4c PvE NPC {#0x4c}

Item type 133 (`ITEM_TYPE_PVE_NPC`). No item in the current items.dat has this type. The data is read
into a 0x370-byte PvE object that the client creates only when the foreground's item type is 133;
otherwise **nothing is read**.

Three entries (probably the NPC's three forms, see [PVE_NPC (0x29)](/packets/29-pve-npc)), each:

| Bytes | Meaning |
|---|---|
| 25 × 4 bytes | stats. Values 1, 2, 3, 8, 11, 13, 21 and 22 (counting from 0) are floats; 5, 6, 10, 14, 19 and 24 are read as 0/1 flags; the rest are ints. Meanings not traced |
| u32 n | number of pairs |
| n × (u32, u32) | pairs, not traced |

<small>Read by `0x15ce080` (case 0x4c), entries from `0x14b7680`.</small>

## 0x4d Infinity Weather Machine {#0x4d}

Item type 134 (`ITEM_TYPE_INFINITY_WEATHER_MACHINE`): Infinity Weather Machine.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | value | not traced (probably the time per weather) |
| u32 | n | number of values |
| n × u32 | list | probably the weathers it cycles through |

The block animates while its weather is the world's current weather (as the other weather machines do).

<small>Read by `0x15ce080` (case 0x4d, the end of 0x2c's code); frame in `0x11a6a9c`.</small>

## 0x4e Completionist {#0x4e}

Item type 137 (`ITEM_TYPE_COMPLETIONIST`). No item in the current items.dat has this type.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | value | not traced |

<small>Read by `0x15ce080` (case 0x4e).</small>

## 0x4f Feeding block {#0x4f}

Item type 140 (`ITEM_TYPE_FEEDING_BLOCK`): Pineapple Guzzler.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | value | not traced (probably how much it has been fed) |

<small>Read by `0x15ce080` (case 0x4f).</small>

## 0x50 Kranken's block {#0x50}

Item type 141 (`ITEM_TYPE_KRANKENS_BLOCK`): Kranken's Galactic Block and Krankens Pattern 1–10.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | value | not traced (0 when placed) |
| u32 | color | the block is drawn tinted with this colour (packed RGBA, `0xffffffff` = no tint, the default) |

<small>Read by `0x15ce080` (case 0x50); drawn in `0x11a9ee4`.</small>

## 0x51 Friends Entrance {#0x51}

Item type 142 (`ITEM_TYPE_FRIENDS_ENTRANCE`): Friends Entrance.

| Bytes | Field | Meaning |
|---|---|---|
| u32 | ? | not traced (0 when placed) |
| u32 | ? | not traced (1 when placed) |

<small>Read by `0x15ce080` (case 0x51).</small>

## 0x52 (no data) {#0x52}

Accepted by the parser (only types above 0x52 log "Bad type of %d detected in tileextra") but there is no
case for it, so nothing follows the type byte.

<small>Default in `0x15ce080`.</small>
