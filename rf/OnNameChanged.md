Changes the name shown above a player (colour codes allowed), and optionally sets their title graphics.

| # | Type | Meaning |
|---|---|---|
| 1 | string | display name, e.g. `` `2Name`` `` |
| 2 | string | optional title data (see below); empty = remove the player's title |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

**Title data** (argument 2) goes into a table of 256 entries, one per player. The client parses one of two
formats, depending on the server's `proto` (login settings, app+0xc08):

- **`proto` below 206:** `texture|x|y`. The texture file is resolved through the app's resource path, and `x`/`y`
  are texture coordinates (`atoi`). The entry is the one for the player's netID. Fewer than three fields: no title.
- **`proto` 206 or higher:** a JSON object. The keys the client reads:
  - `PlayerWorldID`, which picks the entry: probably the player's netID;
  - `TitleTexture`, `TitleTextureCoordinates`, `TitleIconID`;
  - `RenderType`, `RenderScale`, `IsLegendary`, `EnableSmoothing`, `BlendMode`;
  - `WrenchCustomization`, which holds `WrenchIconID`, `WrenchForegroundID` and `WrenchForegroundCanRotate`.

  The value types weren't traced.

Whether parsing worked is stored on the avatar (avatar+0x3661).

**Legend flag.** If the name ends with `` of Legend`` `` the country flag is reset to `lg`. If it doesn't, and the
flag currently is `lg`, the flag is reset to `us`. Both go through the same code as
[OnCountryState](/functions/OnCountryState), which also clears the badge flags.

### Decompiled handler

```c
void NetAvatar::OnNameChanged(NetAvatar *a, VariantList *vl) {
    a->name = vl[1].s;                                             // avatar+0x28
    SetTitle(a, vl[2].s);                                          // 0x131114c
    if (a->name.size() >= 14 && a->name.ends_with(" of Legend``"))
        SetCountryState(a, "lg");                                  // 0x131123c
    else if (a->flagName == "lg")                                  // avatar+0x140
        SetCountryState(a, "us");
}

void SetTitle(NetAvatar *a, const std::string &data) {             // 0x131114c
    Titles *t = Titles::Get();                                     // 0x29b3f68, 256 × 0x60 bytes
    if (data.empty()) { t->Remove(a->netID); a->hasTitle = 0; return; }       // 0x19bf3f0, avatar+0x40
    a->hasTitle = t->Set(data, a->netID);                          // 0x19bede8: proto < 206 → "tex|x|y"
}                                                                  //            else JSON (0x19bf684)
```

<small>Handler: `0x12f64e4` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x131114c`, `0x19bede8`, `0x19beb14`, `0x19bf214`, `0x19bf684`, `0x19bf3f0`, `0x131123c`.</small>

<!-- args: string,string -->
