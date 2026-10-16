# 0x21 PET_BATTLE

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="tip" text="both" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x137415c`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Runs a battle-pet fight. The client keeps a list of battles, each with two sides (side 0 and side 1). Each side has a player (or a tile), an active pet and a bench pet, and up to ten status effects. `tileX` is the battle id. `buildRange` says what happened; the server sends the outcome of every move, and the client only animates it. Nothing happens if you're not in a world, and sub-commands 2 to 13 are ignored for a battle id the client doesn't know.

| Field | Used as |
|---|---|
| `tileX` | battle id |
| `buildRange` | the sub-command, 0 to 13 (10 does nothing) |
| `netID` | the side, 0 or 1 (for 0: a player's netID) |
| `targetNetID` | the other side, or a status effect id (5) |
| `tileY` | an ability/pet item id, an amount or a mode, depending on the sub-command |
| `itemID` | a result, a hit-point value or a cooldown |
| `particleID` | read as a float and converted to an int: a cooldown in ms, a duration or effect flags |
| `extraDataLength` | the battle state (sub-command 1) |

### Sub-commands
`buildRange` selects what happens:

| Value | Effect | Fields used |
|---|---|---|
| 0 | Sets which battle pet player `netID` shows: `tileY` is a battle-pet item id. The avatar's look code (`0x1098f88`) draws that item wherever the player wears a **Battle Leash** (item 3552). [0x2a](./2a-pvpcard-battle) sub-command 99 sets the same field. | `netID`, `tileY` |
| 1 | Creates or replaces battle `tileX` from the extra data (layout below). | `tileX`, extra data |
| 2 | Ends the battle: both players leave it; for your own battle, the battle UI closes, the music stops and the camera returns. | `tileX` |
| 3 | Swaps side `netID`'s active and bench pets (only if `tileY` is the bench pet's id). Shows ``` `3Swap`` ``` ("Swap" in color 3). The new active pet's ability cooldowns are raised to at least `itemID` ms. `particleID` is the side's new **swap cooldown** in ms (see below). | `netID`, `tileY`, `itemID`, `particleID` |
| 4 | Side `netID`'s **active** pet uses ability `tileY` on side `targetNetID` (animation below). | `netID`, `targetNetID`, `tileY`, `itemID`, `particleID` |
| 13 | Same as 4 for the **bench** pet. | same |
| 5 | `tileY` = 1: add status effect `targetNetID` to side `netID`, with the low byte of `itemID` and value `particleID`; effect 0x36 adds `particleID` seconds to the side's cooldowns, and effects 6, 12, 13 and 29 raise them to `particleID`. Any other `tileY`: remove status effect `targetNetID` from side `netID`. | `netID`, `targetNetID`, `tileY`, `itemID`, `particleID` |
| 6 | Side `netID`'s **active** pet takes a hit: its HP becomes `itemID`, and `tileY` shows as a damage number (yellow if `particleID` has bit 2, red otherwise; a sound when `tileY` ≥ 900). Other bits of `particleID`: 1 draws a beam from the other side, 4 a second beam effect, 8 orbiting particles for status effect 0x20. | `netID`, `tileY`, `itemID`, `particleID` |
| 8 | Same as 6 for the **bench** pet. | same |
| 7 | Side `netID`'s **active** pet is healed: HP becomes `itemID` (a fainted pet gets back up) and `tileY` shows as a green number. | `netID`, `tileY`, `itemID` |
| 9 | Same as 7 for the **bench** pet. | same |
| 11 | Battle tutorial/hint state for your own battle: `tileY` 0 hides it, 41-45 show hint screens. | `tileY` |
| 12 | Celebration on side `targetNetID`'s pet: `tileY` 0 = confetti and `audio/cumbia_horns.wav`, 1 = splash and `audio/squish.wav`. | `targetNetID`, `tileY` |

For 4 and 13, ability `tileY` is looked up in the battle-pet table (`sub_14d1d34`). Its name becomes the side's "last move" text, and the matching ability slot's cooldown is set to `particleID` (the other slots to at least 1 or 2 seconds). `itemID % 100` picks the hit style (2-5, each with its own text and sound: `audio/mlaunch.wav`, `audio/trampoline.wav`, `audio/tip_start.wav`, `audio/sungate.wav`). For pet 1400, `itemID / 100` picks "Punch!" (`audio/swoosh.wav`, `audio/punch_organic.wav`), "Build!" (`audio/tile_created.wav`) or "Grow!" (`audio/choir.wav`).

### Extra data
Sub-command 1 reads the battle state (`sub_1821830`). Strings are `u16 length` + bytes.

| Type | Meaning |
|---|---|
| `u32` | skipped: the reader starts at offset 4 and nothing reads these bytes |
| *then, for side 0 and then side 1:* | |
| string | side name |
| `i32` `u8` `u8` | the player's netID, or -1 and the x, y of a tile (the battle is dropped if the player isn't in the world) |
| `u32` | the side's swap cooldown in ms (side+0x3878) |
| string, `i32` hp, `i32` max hp | active pet: name and hit points |
| 3 × (`i32` pet id, `i32` cooldown) | its three abilities (battle-pet item ids; the first is the pet you see) and their cooldowns, interleaved: id1, cd1, id2, cd2, id3, cd3 |
| string, `i32`, `i32`, 3 × (`i32`, `i32`) | bench pet, same layout |
| 10 × (`u32` id, `u8` stacks, `u32` time) | status effects (id 0 = empty slot): the effect id, its stack count, and its remaining time in ms |

### Cooldowns and status effects

Every frame the battle update (`0x1822ad8`) counts down, by the frame time in ms and never below 0:
- each status effect's remaining time;
- each pet's three ability cooldowns, and the side's swap cooldown, at a rate set by the side's status
  effects: twice as fast while effect 0x16 (with non-zero stacks) is on, half as fast with 0x17; both
  together cancel out.

During your own battle the four quick-access slots become the battle buttons (`0x13d78b4`). Slots 1-3 show
the active pet's abilities with their cooldowns in whole seconds. Slot 4 is the swap button, drawn with item
482 (Big Old Sideways Arrow), and shows the swap cooldown. Using an ability (4 and 13) raises the swap
cooldown to at least 2000 ms and clears the selected slot.

Effect 0x10 makes a display factor of the active pet (side+0xd0) ease towards
1 + 0.2 × ⌊stacks / 3⌋, and 0x19 (non-zero stacks) adds 0.3. That factor is probably the pet's size; the
bench pet's stays at 1.

### Decompiled handler

```c
void PetBattle(GameLogic *self, packet *pkt)              // 0x137b680
{
    Battle *b = FindBattle(pkt->tileX);                   // sub_18221c4: global list of 0x7180-byte battles
    if (!self->world) return;
    switch (pkt->buildRange) {
    case 0: {
        NetAvatar *p = GetAvatar(pkt->netID); if (!p) return;
        p->battlePetShown = pkt->tileY;                   // avatar+0x3588, drawn on the Battle Leash
        RefreshPetDisplay(&p->pets);                      // sub_1098f88(avatar+0x330)
        return;
    }
    case 1:  if (pkt->extraDataLength) LoadBattle(pkt->tileX, GetExtra(pkt));   // sub_18216d0 -> sub_1821830
             return;
    case 2:  if (b) EndBattle(b); return;                 // sub_18220d4
    }
    if (!b || !b->active) return;
    int  side = pkt->netID, other = pkt->targetNetID;
    int  ms   = (int)pkt->particleID;
    switch (pkt->buildRange) {
    case 3:  SwapPets(b, side, pkt->tileY, pkt->itemID, ms); break;                     // sub_1826fbc "`3Swap``"
    case 4:  UseAbility(b, side, other, pkt->tileY, pkt->itemID, ms, /*pet*/0); break;   // sub_182784c
    case 13: UseAbility(b, side, other, pkt->tileY, pkt->itemID, ms, /*pet*/1); break;
    case 5:
        if (pkt->tileY == 1) AddStatus(b, side, other, (uint8_t)pkt->itemID, ms);       // sub_1828d34
        else                 RemoveStatus(b, side, other);                               // sub_1829074
        break;
    case 6:  PetHit (b, side, pkt->tileY, pkt->itemID, /*pet*/0, ms); break;             // sub_1827360
    case 8:  PetHit (b, side, pkt->tileY, pkt->itemID, /*pet*/1, ms); break;
    case 7:  PetHeal(b, side, pkt->tileY, pkt->itemID, /*pet*/0); break;                 // sub_18277bc
    case 9:  PetHeal(b, side, pkt->tileY, pkt->itemID, /*pet*/1); break;
    case 11: SetBattleHint(b, pkt->tileY); break;                                        // sub_18223d0
    case 12: Celebrate(b, pkt->tileY, side, other); break;                               // sub_182a66c
    }
}

void PetHeal(Battle *b, int side, int amount, int hp, int pet)       // sub_18277bc
{
    if (side > 1) return;
    Pet *p = &b->side[side].pet[pet];
    if (p->hp < 1) p->state = 2;                          // back up
    p->hp = hp;
    SpawnParticles(p->x, p->y - 16, ..., (float)amount, 0xac);   // the green number
}

void PetHit(Battle *b, int side, int amount, int hp, int pet, int flags)   // sub_1827360
{
    if (side > 1) return;
    Pet *p = &b->side[side].pet[pet];
    p->hp = hp;
    SpawnParticles(p->x, p->y - 16, ..., 0x0b);
    if (amount >= 900) PlaySound(...);                    // big hit
    SpawnParticles(p->x, p->y - 16, (flags & 2) ? yellow : red, (float)amount, (flags & 2) ? 0xad : 0xab);
    if (flags & 1) Beam(0xaf, from other side, to p);
    if (flags & 4) Beam(0x6e, from other side, to p);
    if (flags & 8) for each stack of status 0x20 on the other side: orbit particle 0x2b around p;
}

void RemoveStatus(Battle *b, int side, int id)            // sub_1829074
{
    for (int i = 0; i < 10; i++)
        if (b->side[side].status[i].id == id) b->side[side].status[i].id = 0;
}

void AddStatus(Battle *b, int side, int id, uint8_t a, int value)   // sub_1828d34
{
    if (id == 0x36) for (cd : b->side[side].cooldowns) if (cd > 0) cd += value * 1000;
    slot = the slot already holding id, else the first empty one (none free: return);
    slot->id = id; slot->a = a; slot->value = value;
    if (id is 6, 12, 13 or 29) for (cd : b->side[side].cooldowns) cd = max(cd, value);
}
```

<small>Handler: `0x137b680` (called from the switch at `0x137415c`) in the 5.60 arm64 client; callees read: `0x18221c4`, `0x18216d0`, `0x1821830`, `0x18220d4`, `0x1826fbc`, `0x182784c`, `0x1828d34`, `0x1829074`, `0x1827360`, `0x18277bc`, `0x18223d0`, `0x182a66c`; battle update `0x1822ad8`, battle buttons `0x13d78b4`, look code `0x1098f88`.</small>



### What the client sends

During a pet battle the four quick-inventory slots become the battle buttons (`0x13d7d7c`). Tapping one sends
(sender `0x1382f78`):

| Field | Value |
|---|---|
| `type` | 0x21 |
| `buildRange` | 10 (choose a move) |
| `netID` | your netID |
| `tileX` | the battle id (battle+8; the same id the server uses in `tileX`) |
| `tileY` | the button: 1, 2, 3 = the active pet's abilities, 4 = swap pets |
| everything else | 0 |

Sent reliable, no extra data. It's only sent while you're in a battle (avatar+0x3294 ≥ 0 and the battle has a
side for you), when the button differs from your side's current choice, and for button 4 only if your side has
a bench pet (side+0x314). The client stores the choice, animates the button (`0x1dc379c`) and plays `audio/click.wav`. The
server probably answers with the move's result (sub-commands 3, 4, 13 above). Outside a battle the slots select items as
usual and nothing is sent.

<small>Sender: `0x1382f78`; caller `0x13d7d7c` (battle buttons).</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `buildRange (4th type byte)` | an argument |

## Official client

**Received:** handled at `0x137415c` in the incoming switch (`0x1373e20`).

**Sent:** Helper `0x1382f78`.
