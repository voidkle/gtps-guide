Shows or hides the countdown timer in the game menu (`GameMenu` → `TimerLabel`, displayed as `m:ss`) and sets the text next to
it (`ExtraText`). Ignored when there is no GUI or the argument list is missing.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | seconds to count down from (the timer runs for #1 × 1000 + 1000 ms) |
| 2 | int, optional | 0 = hide the timer instead; missing or non-zero = start it |
| 3 | string, optional | text for `ExtraText`; read only when #2 is present. Empty or missing hides the text |

The name is registered twice in the dispatcher, with the same handler.

### Decompiled handler

```c
// v[n] = argument n
void OnSetMissionTimer(GameLogic *self, VariantList *v) {
    Entity *gui = GetGUIRoot();
    if (!v || !gui) return;
    uint secs = v[1].GetUINT();
    std::string text;
    if (v[2].type == 0)           StartTimer(gui, secs);                 // 0x16f9388
    else {
        text = v[3].s;
        if (v[2].i != 0)          StartTimer(gui, secs);
        else                      ShowTimer(gui, false);                 // 0x16f9538
    }
    SetTimerText(gui, text);                                             // 0x16f9658: "ExtraText", hidden if empty
}

// 0x16f9388
void StartTimer(Entity *gui, int secs) {
    g_timerStart = GetTick(); g_timerLength = secs * 1000 + 1000;
    UpdateTimerLabel(gui, g_timerLength);                                // 0x16f8f4c: "TimerLabel", "m:ss"
    ShowTimer(gui, true);
}
```

<small>Handler: `0x1371bb0` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x16f9388`, `0x16f9538`, `0x16f9658`, `0x16f8f4c`.</small>

<!-- args: uint,int,string -->
