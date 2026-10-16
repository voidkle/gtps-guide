# OnDisableRemoveIAPScreen

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Closes the store menu if it is open: it slides out, `audio/dialog_close.wav` plays, and the client then calls its own
`ShowWorldUI`. No arguments.

### Decompiled handler

```c
void OnDisableRemoveIAPScreen(GameLogic *self, VariantList *v) {
    CloseStoreMenu();      // tail call to 0x1759ae8: "StoreMenu", "StoreMenuClosing", "audio/dialog_close.wav", "ShowWorldUI"
}
```

<small>Handler: `0x1370578` (dispatcher `0x135e25c`) in the 5.60 arm64 client, a jump to `0x1759ae8`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnDisableRemoveIAPScreen" });
```
