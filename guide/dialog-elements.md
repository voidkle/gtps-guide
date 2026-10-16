# Dialog elements

This page lists every element the 5.60 client's dialog parser (`0x16b7560`) understands, in the order it checks
them. [OnDialogRequest](/functions/OnDialogRequest) passes its text to that parser. It also describes what the
client sends back in `action|dialog_return`. Everything here comes from the decompiled client. Where a field's
meaning is a guess from how the value is used, the table says "probably".

## How the text is read

- The text is split into lines at `\n`, and each line into fields at `|`. Field 0 is the element name. The
  tables below number the fields from 1.
- An unknown element name is skipped silently.
- An element with too few fields logs `Error with <element> parms` and is skipped. "Min" in the tables is the
  smallest number of fields, counting the name, that the parser accepts.
- Text fields get the color from `set_default_color` put in front of them, and `<CR>` in them becomes a line break.
- Size fields compare exactly against `big`; anything else is small. Alignment fields compare exactly against
  `center`; anything else, `left` and `right` included, is left-aligned.
- Most elements take one more optional field at the end, written **opts** below. It is a list of
  `key:value` pairs separated by `;`. When it has `featureEnableFlag:<n>`, the element is only added if feature
  `n` is on (the flags come from [OnSetFeatureEnableFlags](/functions/OnSetFeatureEnableFlags)). Some builders read
  other keys from the same list: the label builder reads `additionalPosX`, `additionalPosY`, `frameSize` and
  `iconFrame`.

## Elements checked by length first

The parser first compares a few names by their length and raw bytes, before the general list.

| Element | Min | Fields | Notes |
|---|---|---|---|
| `add_rating_item` | 3 | name, settings | A star-rating row. The settings are `key:value;…`, with keys `maxRating`, `defaultRating`, `selectedIcons`, `unSelectedIcons`, `touchPadding` and `alignment`. Sends back `rating_item\|<name>\|<value>`. Its error message calls it `add_rating_control`. |
| `add_image` | 4 | file, a, b, [scale], [opts] | An image (`dialogImage`). a and b are floats, probably the size. scale defaults to 1.0. |
| `add_label` | 4 | size, text, align, (unused), [opts] | A text line. |
| `add_inline_label` | 4 | size, text, align, int, [opts] | Probably a label that stays on the current row, with an icon (the int). |
| `add_label_with_icon` | 5 | size, text, align, item id, [opts] | A label with an item icon on the left. |
| `add_label_with_counter` | 4 | size, text, align, input name, [opts] | A label that counts the characters in the text input named by field 4 (builder `0x1699aa8` reads `inputName`). |
| `add_seed_color_icons` | 2 | int, [opts] | Probably the color icons for the seed with that item id. |
| `add_dual_layer_icon_label` | 8 | size, text, align, icon 1, icon 2, float, float, [opts] | Two icons drawn on top of each other. A non-zero 7th field turns on an option. |
| `add_searchable_item_list` | 3 | name, items, … | A list with a search box (`SearchableListEntity`). Clicking an entry sends `buttonClicked\|searchableItemListButton_…`. |

## Labels, text and progress

| Element | Min | Fields | Notes |
|---|---|---|---|
| `add_label_with_icon_button` | 6 | size, text, align, item id, string (probably the button name), [flags, default `noflags`], [string], [opts] | A clickable label. |
| `add_label_with_icon_button_list` | 7 | size, text, align, list 1, list 2, list 3, … | A list of priced entries (builder `0x16b3530`), shown with "Cost: … World Lock(s)" and "(Quantity: …)". The lists are comma-separated item ids (`itemID_transID`, `itemID_iconID`). |
| `add_label_with_ele_icon` | 6 | size, text, align, item id, int, [opts] | A label with an icon. The 5th field probably picks the element. |
| `add_achieve` | 5 | title, text, align, achievement id, [opts] | An achievement row. |
| `add_achieve_button` | 5 | title, text, align, achievement id, [string], [opts] | The same row as a button. |
| `add_achieve_custom`, `add_achieve_custom_btn` | 8 | title, text, align, int, string, int, int, [opts] | Custom achievement row, plain or clickable. |
| `add_player_info`, `add_player_info_small` | 5 | name, level, current, max, [opts] | Shows "Level N" with "(current/max)" or "(MAX!)". |
| `add_fish_info` | 5 | text, int, int, int, [opts] | The same layout, used for fish. |
| `add_progress_bar` | 5 | text, string, string, int, int, [string], [int], [opts] | A progress bar. |
| `add_textured_progress_bar` | 13 | text, int, int, string, int, int, layout, float, float, float, int, int, float, [background], [string] | A bar drawn from textures. The layout (field 7) is `fixed`, `relative`, `pre_icon` or `iconlist`. The background defaults to `barBG`. |
| `add_textured_progress_bar_with_icon` | 15 | as above, plus an icon | Same layout keywords as above. |
| `add_textbox` | 3 | text, align, [opts] | Wrapped text. |
| `add_smalltext` | 3 | text, align, [opts] | The same, in a smaller font. |
| `add_custom_textbox` | 4 | text, font size (float), align, [opts] | |
| `add_clock` | 4 | text, size, align, [opts] | |
| `add_smalltext_forced`, `add_smalltext_forced_alpha` | 3 | text, align, [opts] / two strings | One of the two takes text, align and opts; the other takes two plain strings and uses `TextBoxRender` with a `fontScale`. Which is which wasn't settled. |

## Pickers

| Element | Min | Fields | What happens |
|---|---|---|---|
| `add_player_picker` | 3 | name, label, [opts] | Opens a "Select a player" menu. The choice is sent at once, as `<name>\|<int>` (probably the player's netID), in the `dialog_return`. |
| `add_item_picker` | 4 | name, label, text, [opts] | Opens the item picker. Picking an item sends `dialog_return` at once with `<name>\|<item id>`. |
| `add_confirm_item_picker` | 5 | name, label, text, confirm text, [opts] | The same, with a confirmation step (`ConfirmMsg`). |

## Buttons

Buttons are named `_button_<name>`. Clicking one closes the dialog and sends `dialog_return` with `buttonClicked|<name>`.

| Element | Min | Fields | Notes |
|---|---|---|---|
| `text_scaling_string` | 2 | text | Sets the sample text that button widths are scaled to (probably). |
| `add_community_button` | 4 | name, label, string, [opts] | |
| `add_button` | 4 | name, label, flags, (unused), (unused), [notify], [opts] | The plain button. If `flags` contains `off`, the button is drawn at 30% alpha and probably can't be clicked. A non-zero `notify` (field 6) adds a notification badge (`NotificationOverlay`). gurotopia sends `add_button\|name\|text\|noflags\|0\|0\|`. |
| `add_iap_button` | 5 | four strings | An in-app purchase button (`_button_iap_…`). |
| `add_adwatch_button` | 3 | three strings | A "watch an ad" button. Its error message says `add_custom_button`. |
| `add_inner_image_label_button` | 4 | name, label, string, float, int, int, int, [opts] | |
| `add_friend_image_label_button` | 10 | name, label, …, int, int, int, string, string, [opts] | Uses `game/tiles_page14.rttex`. |
| `add_small_font_button` | 4 | name, label, flags, [opts] | |
| `add_cmmnty_toptoday_bttn`, `add_cmmnty_toptotal_bttn`, `add_cmmnty_toprated_bttn` | 6 | name, label, three strings, [opts] | Community hub buttons. |
| `add_url_button` | 6 | name, label, flags, url, url prompt, [opts] | Clicking it asks "Launch" / "Cancel", then opens the url, instead of sending `dialog_return`. A url of `OPENWORLD`, `OPENSTORE`, `OPENSURVEY` or `OPENCOMMUNITY` does that action instead. `OPENSURVEY` sends `action\|survey`. |
| `add_image_button` | 6 | name, image, three strings, [float / opts] | Layout keyword `imageslayout`. |
| `add_embedded_url_button` | 6 | like `add_url_button` | Also sets `embedded_url = 1` on the button, so the url probably opens inside the game. |
| `add_button_with_icon` | 6 | name, label, frame, item id, text, [notify], [opts] | An item tile. frame is for example `staticBlueFrame`, `staticGreyFrame` or `staticPurpleFrame`. A label of `END_LIST` or `END_ROW` ends the list or the row of tiles. |
| `add_custom_button` | 2 | name, settings | A button styled by `key:value;…` keys: `textLabel`, `middle_colour`, `border_colour`, `alignment`, `iconAlignment`, `margin_rself`, `urlPrompt`, `link_to_rating_item`. |

## Inputs

| Element | Min | Fields | Sends back |
|---|---|---|---|
| `add_checkicon` | 7 | name, label, frame, item id, text, checked (`1`), [opts] | `<name>\|0` or `<name>\|1`. `min_checks` and `max_checks` limit how many can be ticked. |
| `add_checkbox` | 3 | name, label, state, [`useLabel`], [opts] | `<name>\|0` or `<name>\|1`. The parser compares the state with `0`; `1` starts ticked. |
| `dud_checkbox` | 3 | same as `add_checkbox` | Nothing; a checkbox drawn for show. |
| `add_text_input` | 5 | name, label, default text, max length, [opts] | `<name>\|<text>`. |
| `add_text_box_input` | 6 | name, (unused), default text, max length, lines (probably), [opts] | `<name>\|<text>`, multi-line. Line breaks are sent as `<CR>`. |
| `add_text_input_password` | 5 | name, label, default text, max length, (unused), [opts] | `<name>\|<text>`, typed hidden. |

The first text input in a dialog gets the keyboard focus.

## Dialog-level commands

| Element | Fields | Effect |
|---|---|---|
| `embed_data` | key, value, … | Not drawn. Every field is appended to the dialog's hidden data followed by `\|`, and the line ends with a newline, so `embed_data\|itemID\|2` comes back as `itemID\|2\|`. |
| `end_dialog` | name, cancel label, OK label | Sets the dialog name (`returnName`) and adds the buttons. An empty label leaves its button out. Fewer than 4 fields logs `Error with end_dialog parms`. It also sets `labelXMult` to 1.5 if nothing set it before. |
| `add_spacer` | `small` or `big` | Vertical space. |
| `add_layout_spacer` | layout | Spacing for a layout such as `imageslayout`. |
| `disable_resize` | – | Keeps the panel from resizing to its content (probably). |
| `set_default_color` | color code, for example `` `o `` | Put in front of every later text field. |
| `set_border_color` | `r,g,b,a` | The panel border color. With fewer than 4 numbers it is left as it was. |
| `set_bg_color` | `r,g,b,a` | The panel background color. |
| `set_survey_enabled` | `0` or `1` | Shows the survey button (`_button_survey`, `has_survey`). |
| `max_checks`, `min_checks` | number | Limits for `add_checkicon`. |
| `add_quick_exit` | – | An X button (`interface/cross.rttex`) in the corner. It closes the dialog without sending anything. |
| `set_labelXMult` | float (default 1.5) | Label width multiplier. |
| `add_custom_label` | text, settings | A free-placed label (`alignment` key). |
| `add_entity_animation` | settings | Animation keys: `ic_animation`, `startDelay`, `interpolationType` (e.g. `INTERPOLATE_LINEAR`), `finishType` (e.g. `ON_FINISH_DIE`), `set_value_on_finish`. |
| `add_custom_image` | settings | A free-placed image. |
| `add_custom_break` | – | Starts a new row below the tallest item of the current row. |
| `add_custom_margin` | `x:<n>;y:<n>` | Moves the placement point. |
| `set_custom_spacing` | `x:<n>;y:<n>` | Spacing between custom items. |
| `set_custom_start` | `x:<n>` | The x that rows start at. |
| `start_custom_tabs`, `end_custom_tabs` | – | Puts the next elements in a `DialogTabs` container, and leaves it. |
| `add_custom_spacer` | `x:<n>;y:<n>` | Moves the placement point by a multiple of the last item's size. |
| `add_popup_name` | name | Stored as the dialog's `PopupName`. |
| `reset_placement_x` | – | Probably moves the placement point back to the row start. |

## What the client sends back

When a button closes the dialog (`0x1693460`), the client builds the answer (`0x169000c`) and sends it as a text message (type 2):

```text
action|dialog_return
dialog_name|<end_dialog name>
<embed_data lines>
buttonClicked|<button name>        <- only for a button made by an element
<one line per input, in the order they were added>
```

- **Buttons from elements** (`_button_<name>`) add `buttonClicked|<name>`, or `buttonClicked|<name>|params_…`
  when the button has `params`. A button that has a `url` doesn't send anything.
- **The end_dialog OK button** sends the answer without a `buttonClicked` line. The client adds
  `buttonClicked|button_ok` only for a few built-in dialog names: `check_ring`, `crime_edit`, `give_ring`,
  `prezgob`, `surgery`, `mpsuperhero` and `dialog_growpedia`.
- **The end_dialog Cancel button** just closes the dialog. Only `give_ring`, `check_ring` and `mpsuperhero`
  send an answer on cancel, with `buttonClicked|button_cancel`.
- **`add_quick_exit`** closes the dialog without an answer.
- **Inputs**, one line each:
  - text inputs: `name|text`, with `|` in the text replaced by `[`;
  - multi-line inputs: the same, with line breaks sent as `<CR>`;
  - checkboxes and checkicons: `name|0` or `name|1`;
  - ratings: `rating_item|name|value`;
  - the captcha slider: `captcha_answer|<value>|CaptchaID|<id>`.
- **The chat filter.** When the client's local chat filter is on and a text input trips it, the client adds
  `\n|[FT##]|1` to the end of the message.
- **Double clicks.** A second button press in the same tick is ignored. The client logs "You seem clicked
  buttons twice in a tick…".
