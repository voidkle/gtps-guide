# OnChangeSkin

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Changes a player's skin colour.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | skin colour (same value as argument 4 of [OnSetClothing](/functions/OnSetClothing)) |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

The app variable `skinColor` is set too, for whichever player it's sent for. The draw colour (avatar+0x88) is
recomputed the same way as in OnSetClothing: item *pants + 1*'s colour field if the player wears pants,
otherwise the skin colour.

### Decompiled handler

```c
void NetAvatar::OnChangeSkin(NetAvatar *a, VariantList *vl) {
    a->look.skinColor = vl[1].u;                                   // 0x14ce8e0
    GetApp()->GetVar("skinColor")->SetUINT(a->look.skinColor);
    ItemInfo *it = GetItem(a->shownCloth[2] + 1);                  // avatar+0x290
    a->drawColor = (it && a->shownCloth[2]) ? it->f_b8 : a->look.skinColor;   // avatar+0x88
}
```

<small>Handler: `0x12f6680` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x14ce8e0`, `0x14ce834`, `0x1564a48`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnChangeSkin", 1u }, pPeer->netid);
```
