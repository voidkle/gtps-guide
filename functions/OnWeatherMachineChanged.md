# OnWeatherMachineChanged

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Tells the client that a weather machine tile's settings changed, so it re-applies them to the current
background. Ignored when no world is loaded or the index is outside the world.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | int | tile index, `x + y × width` |

The tile's extra data must be a `WeatherMachineData` with a non-empty settings string (extra+8), and the
world's current background (renderer+0x100) must be a configurable one (`Background_ConfigRenderObject`);
then the string is applied to the background (`0xf1f850`). The settings string itself arrives with the tile
data, not in this call.

### Decompiled handler

```c
void operator()(VariantList *const &vl) {                       // 0x1ba91a4
    WorldTiles *t = GetWorldTiles();                            // 0x1626f30
    if (!t) return;
    int i = vl->GetInt(0);
    if (i < 0 || i >= t->count) return;
    GameLogic()->OnWeatherMachineTile(&t->tiles[i]);            // 0x13834b4, tiles are 0xf0 bytes
}

void GameLogic::OnWeatherMachineTile(Tile *tile) {              // 0x13834b4
    auto *wm = dynamic_cast<WeatherMachineData *>(tile->extra); // tile+0xe8
    if (!wm || wm->settings.empty()) return;
    if (auto *bg = dynamic_cast<Background_ConfigRenderObject *>(this->renderer->background))   // +0xe0 → +0x100
        bg->ApplySettings(wm->settings);                        // 0xf1f850
}
```

<small>Handler: `0x1ba91a4` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x13834b4`, `0xf1f850`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnWeatherMachineChanged", 1 });
```
