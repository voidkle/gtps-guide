# OnShowDialogMessage

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Shows a text in the in-game message panel (probably the NPC / story message box), then moves the console to make room.
The text isn't refreshed if it's empty or the same as the text already shown.

| # | Type | Meaning |
|---|---|---|
| 1 | string | read and passed on, but the panel function ignores it (probably a title or speaker) |
| 2 | string | the message text |

### Decompiled handler

```c
// v[n] = argument n
void OnShowDialogMessage(GameLogic *self, VariantList *v) {
    if (!v || !GetGUIRoot()) return;
    ShowDialogMessage(GetGUIRoot(), &v[1].s, &v[2].s);   // 0x177b518 drops #1: MessagePanel::SetText(0x17168ac(), v[2].s) (0x1b58ef0)
    RepositionConsole();                                  // 0x168725c
}
```

<small>Handler: `0x1371cc0` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x177b518`, `0x1b58ef0`, `0x168725c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnShowDialogMessage", "...", "..." });
```
