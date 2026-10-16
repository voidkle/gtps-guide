# 0x22 NPC

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="tip" text="both" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1374780`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Controls the world's NPCs (the client's `ClientNPC` objects: ghosts, beach enemies, XML-defined NPCs and others) and a few NPC effects on players. Each NPC has a one-byte id and a type. `buildRange` is the command, and `jumpCount` is usually the NPC id. Packets with `buildRange` above 11, or arriving when you're not in a world, are ignored.

| Field | Used as |
|---|---|
| `buildRange` | the command (below) |
| `jumpCount` | NPC id (for 5: an amount) |
| `objectType` | NPC type (spawn), a second NPC id (4), or the effect (5) |
| `posX`, `posY` | NPC position in pixels |
| `speedX`, `speedY` | NPC velocity or target |
| `tileX`, `tileY` | passed to the NPC (for 5: `tileX` is the player's netID; for 4: `tileY` = 4 means no particles) |
| `particleID` | a float passed to the NPC (stored at npc+0x28) |
| `extraDataLength` | the NPC list (command 0) |

### Sub-commands
`buildRange` selects what happens:

| Value | Effect | Fields used |
|---|---|---|
| 0 | Replace all NPCs with the list in the extra data. | extra data |
| 1 | Remove NPC `jumpCount`. | `jumpCount` |
| 2 | Spawn NPC `jumpCount` of type `objectType` (or reuse the one with that id/type), at `pos` with `speed`, `tileX`, `tileY`, `particleID`; then pass the command to it. At most about 105 NPCs. Types 8 and 15 on a tile of item type 0x5d start the tile's animation and play `audio/flame_go.wav`; type 3 bursts particle 0xc5. | all of `objectType`, `jumpCount`, `pos`, `speed`, `tileX`, `tileY`, `particleID` |
| 3, 6, 9, 10, 11 | Pass the command to NPC `jumpCount` (its own handler, below). | same |
| 4 | Kill NPCs: those with id `jumpCount` (some types only) and those with id `objectType`; the second kind shows particle 0x2c unless `tileY` is 4. | `jumpCount`, `objectType`, `tileY` |
| 5 | Effect on player `tileX` (not an NPC), selected by `objectType`, below. | `tileX`, `objectType`, `jumpCount` |
| 7 | NPC `jumpCount` dies at `pos` with its type's death effect (ghost type 11: `audio/boo_death.wav`), then is removed. | `jumpCount`, `pos` |
| 8 | Nothing. | |

Command 5, by `objectType`:

| `objectType` | Effect on player `tileX` |
|---|---|
| 1 | particle 0xcc on the player; if it's you and you're in the "swallowed" state (0x1a), the client sends `action\|respawn_spike` (you die) |
| 2 | clears that state (state 0x1d) |
| 3 | sets a scale value to `jumpCount` × 0.1 |
| 4 | the player throws up: `audio/barf.wav`, animation 0x15 with strength `jumpCount` |
| 0 or other | the player is swallowed (state 0x1a, value `jumpCount`): `audio/belch1.wav` |

The basic `ClientNPC` handler (vtable+0x30, `sub_1817a5c`): command 3 and 6 set the NPC's speed/target, `tileX`, `tileY` and `particleID` (6 also moves it to `pos`; a ghost with `tileY` 800 laughs, `audio/boo_evil_laugh.wav`); command 9 plays a hit effect (particle 0x80, or 0x18 for type 9).

### Extra data
Command 0 (`sub_18157c8`): `u8 count`, then per NPC `u8 type` followed by that NPC type's own serialized data (read by the NPC object, vtable+0x10). Types 0x10, 0x11, 0x13 (`BeachEnemyNPC`) and 0x15 (`XmlClientNPC`) have their own classes; every other type is a plain `ClientNPC`.

### Decompiled handler

```c
case 0x22: // NPC
    if (!pkt || !self->world || pkt->buildRange > 11) break;
    uint8_t cmd = pkt->buildRange, id = pkt->jumpCount;
    if ((1 << cmd) & 0xede) {                         // 1,2,3,4,6,7,9,10,11
        vec2 pos = pkt->pos, speed = pkt->speed;
        NPCCommand(pkt->particleID, NPCManager(), cmd, id, pkt->objectType,
                   &pos, &speed, pkt->tileX, pkt->tileY);       // sub_181653c
    } else if (cmd == 0) {
        if (pkt->extraDataLength) { int at = 0; NPC_LoadAll(NPCManager(), GetExtra(pkt), &at); }  // sub_18157c8
    } else if (cmd == 5) {
        NetAvatar *p = GetAvatar(pkt->tileX); if (!p) break;
        switch (pkt->objectType) {
        case 1:
            SpawnParticles(center(p), .., self->renderer + 0x178, 0xcc);
            if (p == self->localPlayer && p->state == 0x1a) SendRespawnSpike(p, 0);  // sub_12f9a18
            break;
        case 2: SetState(&p->anim, 0x1d); break;                     // sub_10d8060
        case 3: p->anim.scale = id * 0.1f; break;                    // sub_10d7e80
        case 4: SetAnim(p, 0x15, (float)id); p->anim.value = id;     // sub_1312e80, sub_10d7ea0
                AvatarSound(p, "audio/barf.wav"); break;
        default: Swallow(&p->anim, id); break;                       // sub_10d7f8c: state 0x1a, "audio/belch1.wav"
        }
    }
    break;

void NPCCommand(float f, NPCList *npcs, int cmd, uint8_t id, uint8_t type,
                vec2 *pos, vec2 *speed, int tileX, int tileY)           // sub_181653c
{
    switch (cmd) {
    case 1: RemoveNPC(npcs, id); return;                              // sub_1816010
    case 7: NPCDies(npcs, id, pos); RemoveNPC(npcs, id); return;      // sub_1816148
    case 4: for (npc : npcs) {
                if ((npc->id == id && sub_14e2be4(npc->type) && npc->type != 11) ||
                    (npc->id == type && sub_156dd98(npc->type))) {
                    npc->type = 0;                                     // dead
                    if (tileY != 4 && npc->id == type) SpawnParticles(npc->pos, 0x2c);
                }
            }
            return;
    case 2: SpawnNPC(f, npcs, type, id, pos, speed, tileX, tileY);   // sub_18159f4
            /* fall through */
    default:
        for (npc : npcs)
            if (npc && npc->type && npc->id == id)
                npc->vtable->OnCommand(f, npc, cmd, type, pos, speed, tileX, tileY);   // vtable+0x30
    }
}
```

<small>Handler: inline in the switch at `0x1374780` (out-of-line part `0x137bd14`) in the 5.60 arm64 client; callees read: `0x1815564`, `0x181653c`, `0x18157c8`, `0x18159f4`, `0x1816010`, `0x1816148`, `0x181f10c`, `0x1817a5c`, `0x10d7f8c`, `0x10d8060`, `0x10d7e80`, `0x10d7ea0`, `0x1312e80`, `0x12f9a18`.</small>



### What the client sends

The client sends 0x22 when you hit an NPC. NPCs check hits in a virtual method (vtable +0x38) that gets the
point that was hit: `ClientNPC` / `BeachEnemyNPC` / `XmlClientNPC` use `0x1818528`, `ThanksgivingWorldBoss`
uses `0x1958d34`. On a hit they call the sender `0x1383008`:

| Field | Value |
|---|---|
| `type` | 0x22 |
| `buildRange` | 8 (hit) |
| `jumpCount` | the NPC id (npc+8) |
| `objectType` | 0 |
| `posX`, `posY` | the point that hit the NPC (see below) |
| `speedX`, `speedY` | the centre of your avatar |
| everything else | 0 |

**Not reliable** (the last argument of the send function is 0), no extra data.

What counts as a hit:

- `ClientNPC` types 9, 14, 18 and 21: the point is within 64 px of the NPC (16 px for type 21). For types 14
  and 18, when your punch effect (avatar+0x18c) is 0xb1 (a beam), the test is instead whether the NPC lies on
  the line from you to the point (±16 px), and `posX`, `posY` are then the NPC's own position. Other types only
  take hits during an event (`0x14e2be4`, not type 11) while you wear the Neutron Power Glove (6086) with the
  Neutron Pack (3714).
- `ThanksgivingWorldBoss`: within 64 px, while it can be hit (npc+0x31).

What sends the point (which punch or projectile code calls the method) wasn't traced.

<small>Sender: `0x1383008`; callers `0x1818528`, `0x1958d34` (NPC vtable slot +0x38).</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `pos` |  |
| `speed` |  |

## Official client

**Received:** handled at `0x1374780` in the incoming switch (`0x1373e20`).

**Sent:** Helper `0x1383008`.
