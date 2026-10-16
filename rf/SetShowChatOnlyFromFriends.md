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

<!-- args: uint -->
