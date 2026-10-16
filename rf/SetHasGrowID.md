Tells the client whether the player has a GrowID, and if so saves the login so the next start can log in
with it. The name has no `On` prefix.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | non-zero = has a GrowID (GameLogic+0x29c). With 0 nothing else happens |
| 2 | string | the GrowID name, saved as `tankid_name` |
| 3 | string | the password, saved as `tankid_password` (`0x1084f18`; obfuscated with key 0x16062 on non-Android platforms, Android takes another path). gurotopia sends an empty string |

With argument 1 non-zero the client also sets `tankid_checkbox` = 1 (remember the login).

### Decompiled handler

```c
void SetHasGrowID(GameLogic *self, VariantList *args) {
    self->hasGrowID = arg1.u != 0;                                 // +0x29c
    if (!arg1.u) return;
    GetApp()->GetVar("tankid_name")->Set(arg2.str);
    GetApp()->SavePassword("tankid_password", arg3.str);           // 0x1084f18
    GetApp()->GetVar("tankid_checkbox")->SetUint(1);
}
```

<small>Handler: `0x136edf8` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1084f18`, `0x1e68358`.</small>

<!-- args: uint,string,string -->
