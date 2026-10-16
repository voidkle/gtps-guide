# OnOverrideGDPRFromServer

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Does nothing in the 5.60 client. The name is registered (so the call isn't logged as unknown), but the
handler is an empty function and no other dispatcher handles it. gurotopia sends it with four ints at login;
they're ignored.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| – | – | any arguments are ignored |

### Decompiled handler

```c
void operator()(VariantList *const &) {   // 0x1ba902c
    return;
}
```

<small>Handler: `0x1ba902c` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnOverrideGDPRFromServer"` |
| 1 | int |  |
| 2 | int |  |
| 3 | int |  |
| 4 | int |  |

gurotopia: `include/action/tankIDName.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnOverrideGDPRFromServer" });
```
