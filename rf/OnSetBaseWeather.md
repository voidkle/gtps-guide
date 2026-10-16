Sets the world's base weather (the weather shown when no current weather is set). If that changes the weather actually
shown, the world renderer redraws its background.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | weather id (stored as 16 bits at world+0x1a8) |

Without a world and renderer the client logs "Can't set base weather, no map loaded". The weather shown is the current
weather (world+0x1ac, set by [OnSetCurrentWeather](./OnSetCurrentWeather)) when it is non-zero, otherwise the base weather.

### Decompiled handler

```c
// v[n] = argument n
void OnSetBaseWeather(GameLogic *self, VariantList *v) {
    if (!self->world || !self->worldRenderer) { LogMsg("Can't set base weather, no map loaded"); return; }
    uint id = v[1].GetUINT();
    short before = ShownWeather(self->world);       // 0x15e1048: current ? current : base
    self->world->baseWeather = id;                  // world+0x1a8
    if (before != ShownWeather(self->world)) RefreshWeather(self->worldRenderer);   // 0x11a2f70
}
```

<small>Handler: `0x137097c` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x15e1048`, `0x11a2f70`.</small>

<!-- args: uint -->
