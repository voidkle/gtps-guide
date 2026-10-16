Asks the app store for current in-app purchase prices. No arguments. "Houston" is the client's name for its
store/IAP service (app+0xd10).

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

The request is made only on platforms 0, 1, 2 and 4; the Android build always reports 4 (`0x14213cc`),
so on Android it always runs. The store answers asynchronously; nothing is sent to the game server.

### Decompiled handler

```c
// lambda registered for "OnRequestHoustonPricing" in 0x1ba1ec8
void operator()(VariantList *const &) {            // 0x1ba8240
    int p = GetPlatformID();                         // 0x14213cc, returns 4 on Android
    if (p != 2 && p != 0 && p != 4 && p != 1) return;
    Houston_RequestPrices(&GetApp()->houston);       // app+0xd10, 0x1d91a3c: houston->store (+0x120) vtable +0x18 with a callback
}
```

<small>Handler: `0x1ba8240` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x14213cc`, `0x1d91a3c`.</small>

<!-- args: -->
