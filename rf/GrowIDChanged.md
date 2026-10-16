Updates the saved GrowID name after a rename. It works like [SetHasGrowID](./SetHasGrowID) without the
password.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | non-zero = has a GrowID (GameLogic+0x29c). With 0 the name isn't saved |
| 2 | string | the new name, saved as `tankid_name` |

### Decompiled handler

```c
void GrowIDChanged(GameLogic *self, VariantList *args) {
    self->hasGrowID = arg1.u != 0;
    if (arg1.u) GetApp()->GetVar("tankid_name")->Set(arg2.str);
}
```

<small>Handler: `0x136f124` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: uint,string -->
