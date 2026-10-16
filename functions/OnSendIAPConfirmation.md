# OnSendIAPConfirmation

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Confirms an in-app purchase order: the client deletes the saved key `order_<id>` from its settings database and saves
`save.dat` ("Save save.dat failed!" is logged on error). The client keeps unconfirmed orders under those keys, probably so
it can report them again.

| # | Type | Meaning |
|---|---|---|
| 1 | int | the order id |

### Decompiled handler

```c
// v[n] = argument n
void OnSendIAPConfirmation(GameLogic *self, VariantList *v) {
    int id = v[1].GetINT32();
    GetApp()->sharedDB.DeleteVar("order_" + std::to_string(id));     // 0x16e1fd0 → 0x1e4e770, app+0x9c0
    SaveSaveDat(GetApp());                                            // 0x10814a4
}
```

<small>Handler: `0x1370928` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x16e1fd0`, `0x1e4e770`, `0x10814a4`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSendIAPConfirmation", 1 });
```
