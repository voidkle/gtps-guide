Opens the daily-reward menu. The menu is built from argument 1 with the normal dialog builder, the same one
[OnDialogRequest](./OnDialogRequest) uses, plus a few things only this menu understands. Nothing happens if
the menu is already open.

| # | Type | Meaning |
|---|---|---|
| 1 | string | dialog text (`add_label|…`, `add_button|…`, … as in OnDialogRequest) |

Before building, the client runs its own `HideWorldUI` function and sets the local avatar to state 2
(`0x12eca8c`, probably "busy in a menu").

What this menu adds (`0x167b02c`):

- **`add_countdown|<text>|enable`.** Shows `<text>` in a `countdown` label at about 4/5 of the menu's height.
  With an empty text the label probably falls back to `SMASH PINATAS`, the string the label code holds. The
  third field decides whether the claim button is set up: only the exact word `enable` does it.
- **`_button_claimbutton`, `_button_resetclaim`.** Buttons with these names get the menu's own
  `OnButtonSelected` handling. Other buttons work as in any dialog.

### Decompiled handler

```c
void OnDailyRewardRequest(GameLogic *self, VariantList *args) {
    Entity *gui = FindEntity(GetEntityRoot(), "GUI");
    OpenDailyRewardMenu(gui, arg1.str);                  // 0x167ae58
}

Entity *OpenDailyRewardMenu(Entity *gui, std::string text) {   // 0x167ae58
    if (g_dailyMenu.open) return g_dailyMenu.entity;
    CallFunction(GameLogic(), "HideWorldUI");
    if (NetAvatar *me = GameLogic()->GetLocalPlayer()) me->SetState(2);   // 0x12eca8c
    return g_dailyMenu.Build(gui, text);                 // 0x167b02c: dialog builder 0x16c3088 + add_countdown
}
```

<small>Handler: `0x136da70` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x167ae58`, `0x167b02c`, `0x167b6d4`, `0x167ba58`, `0x16c3088`.</small>

<!-- args: string -->
