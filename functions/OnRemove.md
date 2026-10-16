# OnRemove

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Removes a player from the world. The player is found by the `netID|` field of argument 1. If that player is
your own avatar, the client forgets its local player.

| # | Type | Meaning |
|---|---|---|
| 1 | string | `netID|<n>\n` |
| 2 | string | `pId|<userID>\n`; only checked when the server's `proto` (from the login settings) is above 206 |

With `proto` > 206 the player is removed only if `pId` equals the `userID` it was spawned with
([OnSpawn](./OnSpawn)); a missing or different `pId` keeps the player. With a lower `proto` the netID alone decides.
Either way the team-battle top-3 list is recomputed.

### Decompiled handler

```c
void OnRemove(GameLogic *self, VariantList *args) {
    int netID, pId;
    GetInt(arg1.str, "netID|", &netID);
    NetAvatar *a = NetObjects()->Get(netID);
    if (a) {
        if (GetApp()->proto > 206) {                       // app+0xc08
            NetAvatar *p = dynamic_cast<NetAvatar *>(a);
            if (!p) goto done;
            pId = 0;
            GetInt(arg2.str, "pId|", &pId);
            if (pId != p->userID) goto done;               // avatar+0x12c
        }
        a->Remove();                                       // vtable+0x40
    }
done:
    if (a == self->localPlayer) self->localPlayer = NULL;  // +0x1a8
    UpdateBattleTop3(&self->battle);                       // 0x14db3ec, self+0x318
}
```

<small>Handler: `0x136ba44` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x157f82c`, `0x1342f40`, `0x14db3ec`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnRemove"` |
| 1 | string | netID|<n>\n |
| 2 | string | pId|<user id>\n |

A player left the world.

gurotopia: `include/action/quit_to_exit.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnRemove", "...", "..." });
```
