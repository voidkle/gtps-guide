Shows or hides the Thanksgiving boss bar. It reuses the game menu's timer label: argument 1 starts a countdown,
argument 2 is the boss's health in percent, shown as `Boss Health:<color><percent>%`.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | seconds left on the timer; 0 hides the bar |
| 2 | uint | boss health in percent; 0 hides the bar |

Global function: send it with `netID` -1 in the [CALL_FUNCTION](/packets/01-call-function) header.

- Ignored unless the server's `proto` (from the [login settings](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a), stored at app+0xc08) is above 178.
- If either argument is 0, the `TimerLabel` in `GameMenu` is hidden and its `ExtraText` set to an empty string.
- Otherwise the timer counts down from `(arg1 + 1) × 1000` ms and `ExtraText` becomes
  ``` "Boss Health:" + color + arg2 + "%``" ```. The color is the entry with the smallest threshold ≥ `arg2`:

| Health ≤ | Color |
|---|---|
| 100 | `` `2 `` |
| 80 | `` `9 `` |
| 60 | `` `8 `` |
| 40 | `` `4 `` |
| 20 | `` `4 `` |

### Decompiled handler

```c
void GameLogic::OnUpdateThanksGivingBossUI(GameLogic *self, VariantList *vl) {
    if (GetApp()->proto <= 178) return;                            // 0x117e8cc, app+0xc08
    uint32_t seconds = vl[1].u, health = vl[2].u;
    std::string color;
    for (auto &e : bossHealthColors)                               // 0x29c5040, built at 0x13901e0
        if (health <= e.threshold) color = e.code;
    Entity *menu = GetGameMenu();                                  // 0x1808f78
    if (seconds == 0 || health == 0) {
        ShowTimerLabel(menu, false);                               // 0x16f9538: "GameMenu"/"TimerLabel"
        SetExtraText(menu, "");                                    // 0x16f9658: "ExtraText"
    } else {
        std::string text = "Boss Health:" + color + std::to_string(health) + "%``";
        StartTimerLabel(menu, seconds);                            // 0x16f9388: (seconds*1000 + 1000) ms, shows it
        SetExtraText(menu, text);
    }
}
```

<small>Handler: `0x137244c` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x117e8cc`, `0x16f9388`, `0x16f9538`, `0x16f9658`, table init at `0x13901e0`.</small>

<!-- args: uint,uint -->
