# OnOpenTapjoyTV

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Asks the ad manager to show a video ad for a placement name. In 5.60 the ad library is IronSource; the name "Tapjoy" is
left over from the library used before. If the ad can't be shown, the client reports `IronSource_Show_Failed` to its analytics
(UbiServices).

| # | Type | Meaning |
|---|---|---|
| 1 | string | ad placement name |

### Decompiled handler

```c
// v[n] = argument n
void OnOpenTapjoyTV(GameLogic *self, VariantList *v) {
    ShowAd(&GetApp()->ads /*app+0xe38*/, v[1].s, 0);     // 0x1e3cf90 → app+0xcb0 → 0x1f23f88
}
```

<small>Handler: `0x1371744` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1e3cf90`, `0x1f23f88`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnOpenTapjoyTV", "..." });
```
