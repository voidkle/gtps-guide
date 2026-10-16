# OnParticleEffect

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Plays a particle effect at a position in the world. The [0x11 SEND_PARTICLE_EFFECT](/packets/11-send-particle-effect)
game packet is turned into this same call.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | particle effect id; only ids below 396 are played |
| 2 | vec2 | position in pixels |
| 3 | float | passed to the spawner as its third value. Many effects use it as a direction in degrees (they spray within ±20° of it). Missing = 0 |
| 4 | float | an effect-specific value: for some effects a strength around 0–1 (above 0.1 switches to a full 360° spray), for others an id that is matched. Missing = 0 |

Nothing happens without a world renderer (GameLogic+0xe0).

### Decompiled handler

```c
void OnParticleEffect(GameLogic *self, VariantList *args) {
    uint id = arg1.u;
    vec2 pos = arg2.vec2;
    if (self->worldRenderer && id < 396)
        SpawnParticles(pos.x, pos.y, arg3.f, arg4.f, 0,
                       &self->worldRenderer->particles, id, 0);     // 0x190d050, renderer+0x178
}
```

<small>Handler: `0x136f7e8` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x190d050`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnParticleEffect"` |
| 1 | uint | effect id |
| 2 | vec2 | position in pixels |
| 3 | float | 0 |
| 4 | float | 0 |

gurotopia: `include/database/peer.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnParticleEffect", 1u, CL_Vec2f{x, y}, 1.0f, 1.0f });
```
