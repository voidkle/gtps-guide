The answer to a dialog from [OnDialogRequest](/functions/OnDialogRequest). The full format (embed_data, inputs,
checkboxes, `buttonClicked`, captcha and rating lines, `[FT##]`) is on [Dialog elements](/guide/dialog-elements#what-the-client-sends-back).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `dialog_name` | the `end_dialog` name |

- A second button press in the same tick is ignored ("You seem clicked buttons twice in a tick...").
- The same click handler (`0x1693460`) also turns special buttons into other messages: `OPENWORLD` links join a world,
  `OPENSTORE` sends [storenavigate](./storenavigate), `OPENCOMMUNITY` sends [communitytabs](./communitytabs), and
  `OPENSURVEY` sends `action|survey\n` (an action not otherwise listed here).

<small>Builders: `0x16690ac`, `0x169000c`; click handler `0x1693460`.</small>
