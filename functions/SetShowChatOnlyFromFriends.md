# SetShowChatOnlyFromFriends

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the player's `onlyFriendsChat` option to the given value. This is the setting that limits chat to
friends; the filtering itself happens elsewhere.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | the new value (0 = off). Missing = 0 |

### Decompiled handler

```c
void SetShowChatOnlyFromFriends(GameLogic *self, VariantList *args) {
    GetApp()->GetVar("onlyFriendsChat")->SetUint(arg1.u);
}
```

<small>Handler: `0x136f2a0` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "SetShowChatOnlyFromFriends", 1u });
```
