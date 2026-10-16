# 0x14 SET_CHARACTER_STATE

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="tip" text="confirmed" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's character state: state bits, physics values and a few visual parameters. gurotopia sends it
with every `OnSetClothing`. For your own avatar it also sets your extra build and punch range. The physics
values are kept in a scrambled form in memory (each one stored twice with a random offset), which is the
client's protection against memory editing.

| Field | Used as |
|---|---|
| `netID` | the player; ignored if they aren't in the world |
| `objectType` (byte 1) | punch effect id (avatar+0x18c) |
| `jumpCount` (byte 2) | your own avatar only: extra reach in tiles = value − 0x80 (so gurotopia's 0x80 = none) for every item **except** the Fist: placing blocks, tools, consumables |
| `buildRange` (byte 3) | your own avatar only: extra reach in tiles = value − 0x80 when using the **Fist** (item 18, also used when nothing is selected) |
| `flags` | stored as the avatar's flags; when bit 10 (`0x400`) changes, the avatar's look is rebuilt |
| `itemID` | character state bits (invisible, halo, frozen, ...; see gurotopia's list in `SetClothing.cpp`) |
| `float_var` | a physics value, raised to 0.01 if ≤ 0 and capped by a client maximum (gurotopia: 125, "water speed") |
| `posX`, `posY`, `speedX`, `speedY` | four physics values (gurotopia: 1200, 200, 250, 1000). `speedX` is raised to just above 0 if it's ≤ 0 and capped like `float_var` |
| `targetNetID` | stored on the avatar (avatar+0x184). The look code (`0x109abe4`) copies it into the avatar's look with 0 replaced by 0xff, next to `tileX` (gurotopia's hair colour) and `tileY` (0 replaced by -1). Probably a third colour; the drawing code that uses it wasn't followed |
| `tileX`, `tileY` | stored on the avatar (avatar+0x17c); gurotopia puts the hair color in `tileX` |

Despite the field names, byte 3 is the punch range and byte 2 the build range. The tile-click code
(`0x13a70f8`) picks the reach with `selected == 18 /* Fist */ ? 0x1373de8() : 0x1373e00()`, and both return
`(bonus + 2) × 32` pixels: the base reach is 2 tiles around you. Both values come back to the server in every
[PING_REPLY](./15-ping-reply).

### Decompiled handler

```c
case 0x14: {
    NetAvatar *p = GetAvatar(pkt->netID);
    if (p) NetAvatar_SetCharacterState(p, pkt);              // 0x13131f8
}

void NetAvatar_SetCharacterState(NetAvatar *a, packet *pkt)
{
    u32 old = a->flags;
    a->flags = pkt->flags;
    a->stateBits = pkt->itemID;                               // avatar+0x170
    if ((old ^ pkt->flags) & 0x400) a->look.Rebuild(a);        // 0x1098f88

    a->phys.speedX = Scramble(pkt->speedX);                   // stored as value + k/2 and value + k
    a->phys.speedY = Scramble(pkt->speedY);
    a->phys.posX   = Scramble(pkt->posX);
    a->phys.posY   = Scramble(pkt->posY);
    a->phys.floatVar = pkt->float_var;
    a->punchEffect = pkt->objectType;
    a->tile        = { pkt->tileX, pkt->tileY };
    a->field_184   = pkt->targetNetID;

    if (!a->controller) {                                     // this is you
        self->fistRange  = pkt->buildRange - 0x80;            // self+0x2f4, reach with the Fist
        self->buildRange = pkt->jumpCount  - 0x80;            // self+0x2f8, reach with anything else
    }
    if (a->phys.speedX <= 0) a->phys.speedX = 0.01;
    if (a->phys.floatVar <= 0) a->phys.floatVar = 0.01;
    a->phys.speedX   = min(a->phys.speedX,   PHYS_MAX);       // a scrambled global
    a->phys.floatVar = min(a->phys.floatVar, PHYS_MAX);
    // in worlds of type 0x19 it also moves an object linked to the avatar (avatar+0xbc) to the avatar
}
```

<small>Handler: `0x1374ba0` (switch case) → `0x13131f8` in the 5.60 arm64 client; callees read: `0x13131f8`; range users `0x1373de8`, `0x1373e00`, `0x13a70f8`.</small>

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `type bytes 2-4` | `0x8080` + punch effect id |
| `netID` | the player |
| `float_var` | 125 (water speed) |
| `itemID` | character state bits (invisible, frozen, halo, ...) |
| `pos / speed` | movement constants |
| `tileX` | hair color |

## gurotopia

`include/onVariant/SetClothing.cpp`, sent with every `OnSetClothing`.

## Official client

**Received:** handled at `0x1374ba0` in the incoming switch (`0x1373e20`).
