# OnFTUECameraLock

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Locks or unlocks the camera for the first-time tutorial (FTUE) and gives it a position. The values are kept
in one of two slots on GameLogic. Slot 0 is applied to the world camera at once if a world is being drawn.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | non-zero = lock the camera |
| 2 | vec2 | camera position; each part is rounded to the nearest whole number |
| 3 | vec2 | stored next to the position (slot +0x0c); meaning not traced |
| 4 | uint | slot: 0 = the active camera (GameLogic+0x100); non-zero = a second slot (GameLogic+0x114), probably applied later. Missing = 0 |

Each slot is `{u8 locked, u8 set = 1, vec2 position, vec2 argument 3}`.

### Decompiled handler

```c
void OnFTUECameraLock(GameLogic *self, VariantList *args) {
    uint lock = arg1.u;
    vec2 pos  = { (int)(arg2.x + 0.5f), (int)(arg2.y + 0.5f) };
    vec2 v3   = arg3.vec2;
    CamLock *slot = (arg4.u == 0) ? &self->camLock : &self->camLock2;   // +0x100 / +0x114
    slot->locked = lock != 0;  slot->set = 1;
    slot->pos = pos;  slot->v3 = v3;
    if (arg4.u == 0 && self->worldRenderer) {                            // +0xe0
        Camera *c = self->worldRenderer->overrideCam ? self->worldRenderer->overrideCam
                                                     : &self->worldRenderer->cam;   // +0xf8 / +0x98
        c->locked = lock != 0;                                           // +0x48
        c->pos = slot->pos;                                              // +0x20
    }
}
```

<small>Handler: `0x136d694` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnFTUECameraLock", 1u, CL_Vec2f{x, y}, CL_Vec2f{x, y}, 1u });
```
