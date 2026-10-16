Stores a zodiac mode number on the game logic (+0x140). No reader was found with a direct search, so its effect wasn't
traced; it is probably which zodiac sign or event is active.

| # | Type | Meaning |
|---|---|---|
| 1 | int | zodiac mode |

### Decompiled handler

```c
// v[n] = argument n
void OnReceivedZodiacMode(GameLogic *self, VariantList *v) {
    self->zodiacMode = v[1].GetINT32();     // +0x140
}
```

<small>Handler: `0x1371b60` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: int -->
