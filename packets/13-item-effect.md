# 0x13 ITEM_EFFECT

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x137481c`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

The client turns the packet into a call to its own `OnItemEffect` function, run after `itemID` milliseconds.
`buildRange` is the effect number and becomes argument 0. Effect 7 is special: it carries the extra data as a
string. Every other effect passes the speed and position vectors instead.

| Field | Used as |
|---|---|
| `buildRange` | effect number (argument 0); 7 = with extra data |
| `tileX`, `tileY` | arguments 1 and 2 (ints) |
| `posX`, `posY` | a vec2 argument (4 normally, 3 for effect 7) |
| `speedX`, `speedY` | vec2 argument 3 (not for effect 7) |
| `netID` | for effect 3 only: replaces the x of the position vector, as a float |
| `targetNetID` | argument 5 (int) |
| `itemID` | delay in milliseconds before the effect runs |
| `extraDataLength` | effect 7: length of the string in the extra data |

### Sub-commands

`buildRange` selects how the argument list is built:

| Value | Arguments of `OnItemEffect` | Fields used |
|---|---|---|
| 7 | `7, tileX, tileY, vec2(pos), string(extra data), targetNetID` | `tileX`, `tileY`, `posX`, `posY`, extra data, `targetNetID`, `itemID` |
| 3 | `3, tileX, tileY, vec2(speed), vec2((float)netID, posY), targetNetID` | `tileX`, `tileY`, `speedX`, `speedY`, `netID`, `posY`, `targetNetID`, `itemID` |
| anything else | `effect, tileX, tileY, vec2(speed), vec2(pos), targetNetID` | `tileX`, `tileY`, `speedX`, `speedY`, `posX`, `posY`, `targetNetID`, `itemID` |

### Extra data

Effect 7 only: raw text, `extraDataLength` bytes, no terminator. It is copied into a string argument.

### Decompiled handler

```c
case 0x13: // ITEM_EFFECT  -> FUN_01378320(self, pkt)
    VariantList args;
    if (pkt->buildRange != 7) {
        // FUN_0137c408(self, effect, tileX, tileY, &speed, &pos, targetNetID, delay, netID)
        vec2 pos   = { pkt->posX, pkt->posY };
        vec2 speed = { pkt->speedX, pkt->speedY };
        args[0] = (int)pkt->buildRange;
        args[1] = pkt->tileX;
        args[2] = pkt->tileY;
        args[3] = speed;
        if (pkt->buildRange == 3)
            pos.x = (float)pkt->netID;
        args[4] = pos;
        args[5] = pkt->targetNetID;
        CallFunctionDelayed(GetApp()->gameRoot, pkt->itemID, "OnItemEffect", args);
        return;
    }
    args[0] = 7;
    args[1] = pkt->tileX;
    args[2] = pkt->tileY;
    args[3] = vec2{ pkt->posX, pkt->posY };
    if (pkt->extraDataLength != 0 && GetExtraData(pkt))
        args[4] = std::string(GetExtraData(pkt), pkt->extraDataLength);
    args[5] = pkt->targetNetID;
    CallFunctionDelayed(GetApp()->gameRoot, pkt->itemID, "OnItemEffect", args);
```

<small>Handler: `0x1378320` (tail-called from the switch at `0x137481c`); callees read: `0x137c408`.</small>

## Official client

**Received:** handled at `0x137481c` in the incoming switch (`0x1373e20`).
