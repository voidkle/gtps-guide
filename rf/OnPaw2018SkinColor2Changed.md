Unlocks (or locks) extra skin colour 2 from the 2018 "Paw" promotion (the name comes from the function; what Paw was isn't in the code). The flag (GameLogic+0x3b1) is read by the skin colour picker
("Select a skin color:").

| # | Type | Meaning |
|---|---|---|
| 1 | int | 1 = unlocked; any other value = locked |

### Decompiled handler

```c
// v[n] = argument n
void OnPaw2018SkinColor2Changed(GameLogic *self, VariantList *v) {
    self->pawSkinColor2 = v[1].GetINT32() == 1;      // +0x3b1, read by 0x1bc580c
}
```

<small>Handler: `0x1371014` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: int -->
