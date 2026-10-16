# OnDataConfig

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets two permission flags on a player. Judging by what reads them, they are probably moderator and developer
level. Their names aren't in the client.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | ≠ 0 sets flag 1 (avatar+0x161) |
| 2 | uint | ≠ 0 sets flag 2 (avatar+0x162) |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

What the flags do (as far as traced):

- **Invisible players** ([OnInvis](/functions/OnInvis)). If your own avatar has flag 2, you see every invisible
  player. With flag 1 you see invisible players who don't have flag 2.
- **[OnTriggerCrashlyticsNFE](/functions/OnTriggerCrashlyticsNFE)** only runs when your own avatar has flag 2.

### Decompiled handler

```c
void NetAvatar::OnDataConfig(NetAvatar *a, VariantList *vl) {
    a->dataConfig1 = vl[1].u != 0;                                 // avatar+0x161
    a->dataConfig2 = vl[2].u != 0;                                 // avatar+0x162
}
```

<small>Handler: `0x12f7510` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; readers: `0x12ff0b4`, `0x1372aa8`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnDataConfig", 1u, 1u }, pPeer->netid);
```
