# OnBannerBandolier

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the look of a player's Banner Bandolier (the player in the CALL_FUNCTION header's `netID`), stored in its settings (avatar+0x2d18). The client only stores the two numbers; probably the banner pattern and color chosen in the item's settings dialog (not traced).

| # | Type | Meaning |
|---|---|---|
| 1 | uint | stored at settings+4 |
| 2 | uint | stored at settings+0 |

A "has settings" flag (settings+8) is set.

### Decompiled handler

```c
void NetAvatar::OnBannerBandolier(VariantList *args) {   // 0x12f9274
    BannerBandolier *s = &this->bannerBandolier;          // avatar+0x2d18, setter 0x11fc274
    s->v4 = args->GetUInt(0);
    s->v0 = args->GetUInt(1);
    s->set = true;                                        // +8
}
```

<small>Handler: `0x12f9274` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x11fc274`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnBannerBandolier", 1u, 1u }, pPeer->netid);
```
