# OnHitVFX

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the hit effect a player's punches show (the player in the CALL_FUNCTION header's `netID`), chosen by an
item id. Probably sent when the player equips a weapon with its own hit effect.

| # | Type | Meaning |
|---|---|---|
| 1 | int | item id whose hit effect to use |

The client picks the effect like this (`0x10dfcb4`); the effect lasts 3000 ms unless noted:

| Item | Effect |
|---|---|
| 10442 Winter Light Launcher | effect 599 |
| 10578 Mystic Battle Lance | effect 619, 8000 ms |
| 10800 Cactus Cannon | effect 732 |
| 11312 Spider Sniper | effect 955 |
| 14154 Confetti Popper | effect 1798 |
| any other item | from the item's data: if it names an effect file (item+0x6d8) with a length (item+0x6f0 > 0), that file is loaded and the length is used; otherwise the effect id at item+0x6d0, if > 0 |

### Decompiled handler

```c
void NetAvatar::OnHitVFX(VariantList *args) {          // 0x12f92bc
    SetHitEffect(&this->renderer, args->GetInt(0));     // 0x10dfcb4
}

void SetHitEffect(AvatarRenderer *r, int item) {        // 0x10dfcb4, simplified
    r->hitFx = 0; r->hitFxMS = 3000;
    switch (item) {
    case 10442: r->hitFx = 599; break;
    case 10578: r->hitFx = 619; r->hitFxMS = 8000; break;
    case 10800: r->hitFx = 732; break;
    case 11312: r->hitFx = 955; break;
    case 14154: r->hitFx = 1798; break;
    default: {
        ItemInfo *it = GetItem(item);
        if (!it->hitFxFile.empty() && it->hitFxMS > 0) {   // +0x6d8, +0x6f0
            LoadHitEffectFile(r, it->hitFxFile);            // shared resource cache
            r->hitFxMS = it->hitFxMS; r->hitFx = 0;
        } else if (it->hitFx > 0) r->hitFx = it->hitFx;    // +0x6d0
    }}
    // then releases or prepares the previous/new effect resources
}
```

<small>Handler: `0x12f92bc` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x10dfcb4`, `0x1563ef8`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnHitVFX", 1 }, pPeer->netid);
```
