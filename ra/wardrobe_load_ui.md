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
