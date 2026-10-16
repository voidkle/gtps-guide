# OnMagicCompassTrackingItemIDChanged

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the item the Magic Compass (item 8304) is tracking. The compass's inventory icon draws that item on top of itself;
0 draws nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | tracked item id (0 = none) |

### Decompiled handler

```c
// v[n] = argument n
void OnMagicCompassTrackingItemIDChanged(GameLogic *self, VariantList *v) {
    self->compassItem = v[1].GetUINT();      // +0xb0, read by the inventory icon code (0x11668c0) for item 8304
}
```

<small>Handler: `0x1370d28` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnMagicCompassTrackingItemIDChanged", 1u });
```
