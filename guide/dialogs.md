# Dialogs

[OnDialogRequest](/functions/OnDialogRequest) carries one element per line, `|`-separated. gurotopia
builds them with `create_dialog` (`include/tools/create_dialog.cpp`):

```text
set_default_color|`o
add_label_with_icon|big|`wDrop Dirt``|left|2|
add_textbox|How many to drop?|left|
add_text_input|count||5|5|
embed_data|itemID|2
end_dialog|drop_item|Cancel|OK|
```

| Element | Fields |
|---|---|
| `add_label` | size (`big` or small), text, align (`center` or left) |
| `add_label_with_icon` | size, text, align, icon item id |
| `add_textbox`, `add_smalltext` | text, align |
| `add_text_input` | name, label, default value, max length |
| `add_checkbox` | name, label, 0/1 |
| `add_button` | name, label, flags (`off` greys it out), 0, 0 |
| `add_custom_button` | name, `key:value;…` style settings |
| `add_image_button` | name, image, … |
| `embed_data` | key, value: sent back unchanged |
| `add_spacer` | small / big |
| `end_dialog` | dialog name, cancel label, OK label (an empty label hides that button) |

Most elements take one more field at the end: options as `key:value;…`, for example
`featureEnableFlag:<n>`. The 5.60 client parses about 80 elements. [Dialog elements](/guide/dialog-elements)
lists all of them, with their fields and what each sends back.

Text colors are `` `x `` codes (`` `w `` white, `` `2 `` green, `` `4 `` red, …), and ` `` ` resets.

## Answering

The client answers with [action|dialog_return](/actions/dialog_return):

```text
action|dialog_return
dialog_name|drop_item
itemID|2|
count|5
```

- every `embed_data` as `key|value|`
- `buttonClicked|<name>` when the player pressed a button added by an element (`add_button` and the others)
- every text input as `name|value` (`|` in the text becomes `[`), checkboxes as `name|0` or `name|1`

The `end_dialog` OK button sends the answer **without** a `buttonClicked` line (the example above is one), and
its Cancel button sends nothing. The details, including pickers and ratings, are under
[What the client sends back](/guide/dialog-elements#what-the-client-sends-back).

gurotopia routes it by `dialog_name` to `include/action/dialog_return/`.
