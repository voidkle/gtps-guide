# action|wardrobe_load_ui

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|wardrobe_load_ui
preset|{}
```

## Fields

| Field | Meaning |
|---|---|
| `preset` | Wardrobe preset slot. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

A preset button on the wardrobe save/load screen (`WardrobeSaveLoad.ButtonClicked`). One builder sends both
`wardrobe_save_ui` and `wardrobe_load_ui`: the format is `action|wardrobe_{}_ui\npreset|{}\n`.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `preset` | the clicked button's `btn_index` attribute (an int) |

- `load` is chosen by the screen's mode (the clicked element's value 1 or 2, `one`/`two` strings in the code); with
  `proto` ≤ 225 the older selection rule is used. Probably: in save mode the current clothes are stored in that preset.
- The screen closes after sending.

<small>Builder: `0x1d68d64` (`WardrobeSaveLoadUiController` lambda).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

The client formats `action|wardrobe_{}_ui` with `save` or `load`.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|wardrobe_load_ui\npreset|0\n");
```

<small>Client function: `0x1d68d64` in libgrowtopia.so 5.60.</small>
