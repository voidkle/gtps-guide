# OnZoomCamera

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Animates the world camera's zoom (the scale of GameLogic's entity) to a value.

| # | Type | Meaning |
|---|---|---|
| 1 | float | target zoom. **10000** means "the default zoom", described below. Missing = 0 |
| 2 | uint | animation time in ms. Missing = 0 |

The default zoom (`0x135de10`) is 1.0 on screens of 300 dpi or less, 2.0 above that, 4.0 if the screen is
wider than 1600 px, and 0.8 on a 320×240 screen. With 10000, when the player has the `rememberZoom` option on,
the client uses the saved zoom (`zoomSave`) instead, but never less than half the default.

If the current zoom is below half the default, it is first snapped up to that.

### Decompiled handler

```c
void OnZoomCamera(GameLogic *self, VariantList *args) {
    float zoom = arg1.f;
    uint ms = arg2.u;
    if (zoom == 10000.0f) {
        zoom = DefaultZoom();                                       // 0x135de10
        if (GetApp()->config.Get("rememberZoom").u != 0             // app+0x9c0
            && GetApp()->config.Get("rememberZoom").f != 0) {
            zoom = GetApp()->GetVar("zoomSave")->f;
            if (zoom < DefaultZoom() * 0.5f) zoom = DefaultZoom() * 0.5f;
        }
    }
    vec2 s = GetScale(self->entity);                                // self+0x20
    if (s.x < DefaultZoom() * 0.5f) SetScale(self->entity, ...);    // snap up
    AnimateScale(-1.0f, zoom, self->entity, ms, 1, 1);              // 0x1dc71c8
}
```

<small>Handler: `0x135dec8` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x135de10`, `0x1dc71c8`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnZoomCamera"` |
| 1 | float | zoom (10000) |
| 2 | uint | duration (1000) |

gurotopia: `include/gamePacket/tile_activate.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnZoomCamera", 1.0f, 1u });
```
