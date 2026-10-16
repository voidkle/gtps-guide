Shows the World of the Day coin: it sets a flag on the game logic (+0x4d1 = 1) that the world renderer checks (in `0x11a9ee4`).
No arguments.

### Decompiled handler

```c
void ShowWOTDCoin(GameLogic *self, VariantList *v) {
    self->showWOTDCoin = 1;      // +0x4d1
}
```

<small>Handler: `0x137205c` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: -->
