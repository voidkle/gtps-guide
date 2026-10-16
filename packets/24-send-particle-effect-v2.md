# 0x24 SEND_PARTICLE_EFFECT_V2

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1374d60`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

The client turns the packet into a call to its own `OnParticleEffectV2` function, after `itemID` milliseconds.
The `OnParticleEffectV2` handler (`0x136f90c`) then adds the effect when a world renderer exists. It works like [0x11](/packets/11-send-particle-effect) without the `proto` check: argument 0 always comes from `netID`.

| Field | Used as |
|---|---|
| `netID` | argument 0 of `OnParticleEffectV2`: the effect id, passed to the effect system (`0x1912570`); ids ≥ 1819 (0x71b) are ignored |
| `posX`, `posY` | where the effect plays, in pixels (argument 1) |
| `particleID` | float argument 2, stored in the new effect (effect+0x78) |
| `speedX` | float argument 3: non-zero sets the effect system's last flag (`0x1912570`'s 5th argument) |
| `itemID` | delay in milliseconds before the effect runs |

### Decompiled handler

```c
case 0x24: // SEND_PARTICLE_EFFECT_V2
    // FUN_0137814c: same shape as the 0x11 helper, different function name
    VariantList args;
    args[0] = pkt->netID;        // int
    args[1] = vec2{ pkt->posX, pkt->posY };
    args[2] = pkt->particleID;   // float (offset 0x28)
    args[3] = pkt->speedX;       // float
    CallFunctionDelayed(GetApp()->gameRoot, /*delayMS*/ pkt->itemID, "OnParticleEffectV2", args);
    break;
```

<small>Handler: inline in the switch at `0x1374d60`, then `0x137814c`.</small>

## Official client

**Received:** handled at `0x1374d60` in the incoming switch (`0x1373e20`).
