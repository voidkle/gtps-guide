Plays an effect from the newer particle system (the one with up to 128 live emitters, ids up to 1818) at a position. It does
nothing until the world renderer exists. [SEND_PARTICLE_EFFECT_V2 (0x24)](/packets/24-send-particle-effect-v2) is a shortcut
that turns into this call.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | effect id; ignored if above 1818 |
| 2 | vec2 | position in pixels |
| 3 | float | stored on the new emitter (emitter+0x78) after it starts; probably a size or angle, it depends on the effect |
| 4 | float | non-zero sets a flag passed to the emitter start (probably "don't play its sound" or "one-shot"; not traced) |

If the effect id is in the client's list of disabled effects (a hash set the spawn function checks first), no emitter
starts. Otherwise the client takes a free emitter, or reuses the one with the lowest value at +0x7c when all 128 are busy.

### Decompiled handler

```c
// v[n] = argument n (variant n of the packet; variant 0 is the name)
void OnParticleEffectV2(GameLogic *self, VariantList *v) {
    uint  id  = v[1].GetUINT();
    vec2  pos = v[2].GetVector2();
    float f4  = v[4].GetFloat();
    if (!self->worldRenderer || id > 1818) return;              // self+0xe0
    int slot = SpawnEffect(&self->worldRenderer->effects /*+0x178*/, id, &pos, f4 != 0);   // 0x1912570
    float f3 = v[3].GetFloat();
    self->worldRenderer->emitters[slot].f_78 = f3;              // emitters at renderer+0x1e0, 0x340 bytes each
}
```

<small>Handler: `0x136f90c` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1912570`.</small>

<!-- args: uint,vec2,float,float -->
