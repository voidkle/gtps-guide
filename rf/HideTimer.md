Hides the mission timer (`GameMenu` → `TimerLabel`). The countdown keeps its values; see [OnSetMissionTimer](./OnSetMissionTimer).
Takes no arguments, but the handler does nothing if the argument list pointer is null (it never is for a server call).

### Decompiled handler

```c
void HideTimer(GameLogic *self, VariantList *v) {
    if (v && GetGUIRoot()) ShowTimer(GetGUIRoot(), false);      // 0x16f9538
}
```

<small>Handler: `0x1372018` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x16f9538`.</small>

<!-- args: -->
