Sets the world's current weather (it overrides the base weather while non-zero; 0 shows the base weather again). The
renderer redraws and `audio/terraform.wav` plays, except in the cases below.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | weather id (stored as 16 bits at world+0x1ac); 0 = back to the base weather |

Without a world and renderer the client logs "Can't set base weather, no map loaded" (the same text as
[OnSetBaseWeather](./OnSetBaseWeather)).

- If the weather shown doesn't change, it only redraws (with the sound) when the old weather is 28, 29, 34, 41, 42 or 82.
- If it changes, it redraws with the sound unless the base weather is 0 and the change is from 0 to 4 or from 4 to 0.

### Decompiled handler

```c
// v[n] = argument n
void OnSetCurrentWeather(GameLogic *self, VariantList *v) {
    if (!self->world || !self->worldRenderer) { LogMsg("Can't set base weather, no map loaded"); return; }
    uint id = v[1].GetUINT();
    ushort before = ShownWeather(self->world);                  // 0x15e1048
    self->world->currentWeather = id;                           // world+0x1ac
    if (before == ShownWeather(self->world)) {
        if (before is 28, 29, 34, 41, 42 or 82) { RefreshWeather(self->worldRenderer); PlaySound("audio/terraform.wav"); }
    } else if (!((before == 0 && id == 4) || (before == 4 && id == 0)) || self->world->baseWeather != 0) {
        RefreshWeather(self->worldRenderer);                    // 0x11a2f70
        PlaySound("audio/terraform.wav");
    }
}
```

<small>Handler: `0x1370a20` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x15e1048`, `0x11a2f70`.</small>

<!-- args: uint -->
