# onShowCaptcha

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Shows a captcha. The name starts with a lower-case `o`; the client matches names exactly, so `OnShowCaptcha` won't work.

| # | Type | Meaning |
|---|---|---|
| 1 | string | dialog text in the usual `key\|value` line format (see [Dialogs](/guide/dialogs)) |

The client looks only at the first line, split on `|`:

- If its first field is `add_puzzle_captcha`, the client builds a puzzle captcha (`PuzzleParent`) from fields 1-4 of that line.
  Field 3 is handed to a `Downloader` component, so it is probably the puzzle image to fetch; the meaning of the other three
  wasn't traced.
- Otherwise the whole text is shown as an ordinary dialog by the generic dialog builder (`0x16c3088`, the one that handles
  `add_text_input`, `button_quick_exit` and so on).

An empty string does nothing.

```text
add_puzzle_captcha|<f1>|<f2>|<f3: image>|<f4>|
```

### Decompiled handler

```c
// v[n] = argument n
void onShowCaptcha(GameLogic *self, VariantList *v) {
    TextScanner t(v[1].s);                                   // lines
    if (t.lines.empty()) return;
    auto f = t.GetLine(0).Split('|');
    if (f[0] == "add_puzzle_captcha")
        AddPuzzleCaptcha(f);                                 // 0x137dd78 → 0x16c4528(GUI, &f[1], &f[2], &f[3], &f[4])
    else
        BuildDialog(GetEntityByName(GetGUIRoot(), "GUI"), v[1].s);   // 0x16c3088
}
```

<small>Handler: `0x13714d8` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x137dd78`, `0x16c4528`, `0x16c3088`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "onShowCaptcha", "..." });
```
