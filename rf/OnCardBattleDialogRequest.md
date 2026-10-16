Opens the card-battle dialog. It first closes whatever else is open, then builds the dialog from argument 1
with the normal dialog builder. An earlier card-battle dialog that is still open is closed first.

| # | Type | Meaning |
|---|---|---|
| 1 | string | dialog text (the OnDialogRequest format) |

What it closes, in order:

- a generic dialog, if any menu is open (`0x137d330` → `0x168f370`);
- the pause menu (`PauseMenu`);
- the store (`StoreMenu`);
- the community hub (`CommunityHubMenu`).

What the card-battle dialog adds (`0x18338ec`):

- It remembers the button named `_button_passturn`.
- It reads the dialog's embedded data, the `embed_data` lines. If that contains `action|0`, it starts a
  timer from the current tick (`0x1833dcc`), probably the countdown that passes your turn automatically.

### Decompiled handler

```c
void OnCardBattleDialogRequest(GameLogic *self, VariantList *args) {
    if (IsAnyMenuOpen()) CloseGenericDialog(0, 0, 0);                    // 0x168f370
    if (IsPauseMenuOpen() && FindEntity(GetEntityRoot(), "PauseMenu")) CloseMenu(...);   // 0x16fdcb0, 0x1728644
    if (IsStoreOpen()) CloseStore();                                     // 0x1759a34, 0x1759ae8
    if (FindEntity(GetEntityRoot(), "CommunityHubMenu")) CloseCommunityHub();   // 0x16640a0
    Entity *gui = FindEntity(GetEntityRoot(), "GUI");
    OpenCardBattleDialog(gui, arg1.str);                                 // 0x1833f00 -> 0x18338ec
}
```

<small>Handler: `0x136dce0` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1833f00`, `0x18338ec`, `0x16c3088`, `0x168f370`.</small>

<!-- args: string -->
