# OnPinchMod

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Changes the camera zoom by an amount, as a pinch gesture would. The result is set at once (no animation)
and saved in the `zoomSave` option.

| # | Type | Meaning |
|---|---|---|
| 1 | float | zoom change; multiplied by 3 and by the GUI scale (`scale2d.x` of the root entity). Missing = 0 |

The new zoom is the current zoom plus that amount, kept within limits. The upper limit is 8.8. The lower
limit is half the default zoom for normal players; a moderator or super-moderator (avatar+0x161 / +0x162)
can go down to 0.16, or 0.1 on a 320×240 screen.

### Decompiled handler

```c
void OnPinchMod(GameLogic *self, VariantList *args) {
    float d = arg1.f;
    vec2 s2d = GetApp()->gameLogicEntity->entity->GetVar("scale2d")->vec2;   // app+0xfd8
    AddZoom(d * s2d.x * 3.0f, self, true);                           // 0x1381858
}

void AddZoom(float d, GameLogic *self, bool now) {                   // 0x1381858
    float min = TinyScreen() ? 0.1f : 0.16f;
    NetAvatar *me = self->localPlayer;
    if (!me || (!me->mod && !me->superMod)) min = DefaultZoom() * 0.5f;
    float z = clamp(*self->zoom + d, min, 8.8f);                     // self+0xf0
    if (now) SetScale(self->entity, z); else AnimateScale(-1, z, self->entity, 400, 1, 2);
    GetApp()->GetVar("zoomSave")->SetFloat(z);
}
```

<small>Handler: `0x136e904` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1381858`, `0x135de10`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnPinchMod", 1.0f });
```
