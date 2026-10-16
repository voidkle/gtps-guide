Removes every tutorial arrow (see [OnTutorialArrow](./OnTutorialArrow)).

No arguments are read.

### Decompiled handler

```c
void OnClearAllTutorialArrows(GameLogic *self) {
    self->tutorial->Clear();              // 0x11503e4, self+0x1e8
}
```

<small>Handler: `0x136da68` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x11503e4`.</small>

<!-- args: -->
