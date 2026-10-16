Sets the player's pearl count shown in the UI (`PlayerInfo` +0x38) and notifies its listeners. Whether the
counter is visible is set with [ShowPearlCurrency](./ShowPearlCurrency) / [HidePearlCurrency](./HidePearlCurrency).

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | int | pearls |

### Decompiled handler

```c
void operator()(VariantList *const &vl) {                        // 0x1ba8d68
    SetPearls(&this->owner->appContext->playerInfo, vl->GetInt(0));   // 0x19238ec
}
```

<small>Handler: `0x1ba8d68` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x19238ec`.</small>

<!-- args: int -->
