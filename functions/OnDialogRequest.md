# OnDialogRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Opens a dialog built from the text in argument 1, one element per line (see [Dialog elements](/guide/dialog-elements)).
It runs only while you are in a world: the world screen (`0x1bff3ec`) registers it as a listener on GameLogic's
functions, so it needs the header `netID` to be -1, like the other global functions.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the dialog text: lines of `element\|field\|field…`, separated by `\n` |

If a menu is already open, the call is dropped. "Already open" means a `ControllerDialog`, the `PauseMenu` or
a `PuzzleParent` (the check is `0x137d330`). The client logs `Dialog already opened. Ignore dialog {}.`, then logs
the name of every child of the GUI root. A server that sends two dialogs back to back loses the second one, so
wait for the `dialog_return` first, or close the first dialog (it closes when the player presses a button).

Otherwise `0x16c3088` builds the dialog on the GUI root:

- It runs GameLogic's `HideWorldUI` function, which hides the in-world HUD (`0x16fc408`).
- It sizes the panel from the screen. When the text contains `add_text_input` and `0x14213b0` returns true
  (probably "this device uses an on-screen keyboard"), the panel's height is computed another way.
- It draws a white box (`game/gui_box_white.rttex`, border color `0xccb887ff`).
- It parses the lines (`0x16b7560`, see [Dialog elements](/guide/dialog-elements)), opens the keyboard for the first text input (`0x1dd27f0`),
  adds the survey button if `set_survey_enabled` asked for it, and plays `audio/dialog_open.wav`.

The answer, `action|dialog_return`, is built when the player presses a button. The
[Dialog elements](/guide/dialog-elements#what-the-client-sends-back) page describes it.

### Decompiled handler

```c
// lambda 0x1c0822c -> 0x1c008b8; arg1 = the first argument
void OnDialogRequest(WorldScreen *self, Variant *arg1) {
    GetGameLogic();
    if (IsAnyMenuOpen()) {                                    // 0x137d330: ControllerDialog / PauseMenu / PuzzleParent
        LogError(fmt("Dialog already opened. Ignore dialog {}.", arg1->s));   // 0x1da5798
        for (Entity *e : GetGUIRoot()->children) LogError(e->name);
        return;
    }
    Entity *gui = FindEntity(GetGUIRoot(), "GUI");            // 0x1808f78, 0x1dbca54
    BuildDialog(gui, arg1->s);                                // 0x16c3088 -> parser 0x16b7560
}
```

<small>Handler: `0x1c0822c` → `0x1c008b8`, registered by the world screen (`0x1bff3ec`, through `0x1be9ae8`) in the 5.60 arm64 client; callees read: `0x137d330`, `0x16c3088`, `0x16b7560`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnDialogRequest"` |
| 1 | string | dialog text |

See [Dialogs](/guide/dialogs). The client answers with `action|dialog_return`.

gurotopia: `include/tools/create_dialog.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnDialogRequest", "..." });
```
