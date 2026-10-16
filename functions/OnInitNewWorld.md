# OnInitNewWorld

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Switches the client's screen to the world view. No arguments. The client runs this itself, without
arguments, at the end of handling [SEND_MAP_DATA (0x04)](/packets/04-send-map-data); GameLogic has no
handler of its own for it, only this listener. A server can send it too, but there's no reason to.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

It creates a new `WorldContext` from the shared app context (screen controller +0x60), creates a
`WorldScreen` for it, and makes that the current screen (`0x1b72ee4`).

### Decompiled handler

```c
void operator()(VariantList *const &) { ScreenFlow_OnInitNewWorld(this->owner); }   // 0x1ba85ac

void ScreenFlow_OnInitNewWorld(ScreenFlow *self) {                 // 0x1ba3a98
    auto ctx    = std::make_shared<WorldContext>(self->appContext);  // 0x1ba9e20, self+0x60
    auto screen = std::make_shared<WorldScreen>(ctx);               // 0x1ba9f74
    SetScreen(self, screen);                                       // 0x1b72ee4
}
```

<small>Handler: `0x1ba85ac` → `0x1ba3a98` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; class names from the `make_shared` RTTI (`0x29206c0`, `0x2920710`).</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnInitNewWorld" });
```
