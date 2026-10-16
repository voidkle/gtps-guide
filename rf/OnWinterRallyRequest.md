Opens the Winter Rally menu. It works like [OnDailyRewardRequest](./OnDailyRewardRequest), but with its own
menu object. Argument 1 is dialog text for the normal dialog builder, and the menu also understands an
`add_countdown|<text>|enable` line. Nothing happens if the menu is already open.

| # | Type | Meaning |
|---|---|---|
| 1 | string | dialog text (the OnDialogRequest format) |

Before building, the client runs its own `HideWorldUI` function and sets the local avatar to state 2.

### Decompiled handler

```c
void OnWinterRallyRequest(GameLogic *self, VariantList *args) {
    Entity *gui = FindEntity(GetEntityRoot(), "GUI");
    OpenWinterRallyMenu(gui, arg1.str);                  // 0x1794b1c
}

Entity *OpenWinterRallyMenu(Entity *gui, std::string text) {   // 0x1794b1c
    if (g_winterMenu.open) return g_winterMenu.entity;
    CallFunction(GameLogic(), "HideWorldUI");
    if (NetAvatar *me = GameLogic()->GetLocalPlayer()) me->SetState(2);
    return g_winterMenu.Build(gui, text);                // 0x1794cf0: dialog builder 0x16c3088 + add_countdown
}
```

<small>Handler: `0x136dba8` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1794b1c`, `0x1794cf0`, `0x16c3088`.</small>

<!-- args: string -->
