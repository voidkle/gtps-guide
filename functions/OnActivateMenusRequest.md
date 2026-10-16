# OnActivateMenusRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Does nothing in the 5.60 client: the registered handler is a bare `ret`. The name is still registered, so
sending it is harmless.

No arguments are read.

### Decompiled handler

```c
void OnActivateMenusRequest(GameLogic *self, VariantList *args) { }
```

<small>Handler: `0x135d128` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnActivateMenusRequest" });
```
