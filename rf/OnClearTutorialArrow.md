Removes the tutorial arrow with the given name (see [OnTutorialArrow](./OnTutorialArrow)). Nothing happens if
there is none.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the arrow's name |

### Decompiled handler

```c
void OnClearTutorialArrow(GameLogic *self, VariantList *args) {
    self->tutorial->Remove(arg1.str);     // 0x1150764: erase the first arrow whose name matches
}
```

<small>Handler: `0x136d9ac` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1150764`.</small>

<!-- args: string -->
