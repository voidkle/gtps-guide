Stores one number in the current world's dungeon data (world+0x180 → +8). Ignored when no world is loaded.
What the number means wasn't traced; probably the dungeon's level or floor.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | int | stored at dungeon info +8 |

### Decompiled handler

```c
void operator()(VariantList *const &vl) {                       // 0x1ba8b84
    World *w = GameLogic()->world;                              // +0xd8
    if (!w) return;
    w->dungeonInfo->value = vl->GetInt(0);                      // world+0x180, +8
}
```

<small>Handler: `0x1ba8b84` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client.</small>

<!-- args: int -->
