# OnInvis

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Makes a player invisible or visible again.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | ≠ 0 = invisible |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

Stored at avatar+0x160. Another player who is invisible isn't drawn for you, with two exceptions that come from
the two flags of [OnDataConfig](/functions/OnDataConfig) (`0x12ff0b4`):

- you have flag 2: you see every invisible player;
- you have flag 1 and the invisible player doesn't have flag 2: you see them.

### Decompiled handler

```c
void NetAvatar::OnInvis(NetAvatar *a, VariantList *vl) {
    a->invisible = vl[1].u != 0;                                   // avatar+0x160
}

// drawing check, 0x12ff0b4 (for other players)
if (other->invisible) {
    NetAvatar *me = GetGameLogic()->GetLocalAvatar();              // 0x1373e18
    bool show = me && (me->dataConfig2 || (me->dataConfig1 && !other->dataConfig2));
    if (!show) return;                                             // not drawn
}
```

<small>Handler: `0x12f74cc` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; reader: `0x12ff0b4`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnInvis", 1u }, pPeer->netid);
```
