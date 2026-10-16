# OnRequestNativeAppReview

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Asks the app's platform layer to show the native "rate this app" prompt (probably the Play Store
in-app review). No arguments are read.

Global function: send it with `netID` -1 in the [CALL_FUNCTION](/packets/01-call-function) header.

### Decompiled handler

```c
void GameLogic::OnRequestNativeAppReview(GameLogic *self, VariantList *vl) {
    GetApp()->platform->vfunc_0x10();                              // app+0xcb8
}
```

<small>Handler: `0x1372a88` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnRequestNativeAppReview" });
```
