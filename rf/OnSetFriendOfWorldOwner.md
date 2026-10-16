Marks whether a player is a friend of the world's owner. Only the exact value 1 counts.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | 1 = friend of the owner, anything else = not |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

Stored at avatar+0x3698; where it is used wasn't traced.

### Decompiled handler

```c
void NetAvatar::OnSetFriendOfWorldOwner(NetAvatar *a, VariantList *vl) {
    a->friendOfOwner = vl[1].u == 1;                               // avatar+0x3698
}
```

<small>Handler: `0x12f79a8` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client.</small>

<!-- args: uint -->
