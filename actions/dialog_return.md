# action|dialog_return

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|dialog_return
dialog_name|{}
```

## Fields

| Field | Meaning |
|---|---|
| `dialog_name` | The name from the dialog's `end_dialog|<name>|...` line. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Server

gurotopia: [`include/action/dialog_return.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/dialog_return.cpp).

Reply: Depends on the dialog; gurotopia's handlers are in `include/action/dialog_return/`.

## Notes

After `dialog_name`, the client adds every `embed_data` as `key|value`, every text input as `name|value`, checkboxes as `name|0` or `name|1`, and `buttonClicked|<id>` for the button pressed. The `end_dialog` OK button adds no `buttonClicked` line (except for a few built-in dialogs), and Cancel sends nothing; see [Dialog elements](/guide/dialog-elements). Example:

```text
action|dialog_return
dialog_name|drop_item
itemID|2|
count|5
```

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|dialog_return\ndialog_name|drop_item\n");
```

<small>Client function: `0x16690ac, 0x169000c, 0x1693460` in libgrowtopia.so 5.60.</small>
