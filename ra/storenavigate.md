**Format correction:** `selection|` is optional (`action|storenavigate\nitem|main\n` exists).

Opens a store tab or item directly.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `item` | the store tab (`main`, `locks`, `token`, ...) |
| `selection` | optional: the entry to highlight |

Fixed messages the client sends:

| Where | Text after `action\|storenavigate\n` |
|---|---|
| world UI gems panel (`world_ui.gems_panel_click`), store pop-up | `item\|main\nselection\|gems_bundle06\n` |
| inventory **Increase Backpack** (item 9412) | `item\|locks\nselection\|upgrade_backpack\n` |
| fashion show **Buy tickets** | `item\|main\nselection\|fashion_show_ticket\n` |
| store pop-up (`0x1773c00`) | `item\|token\nselection\|megaphone\n`, or `item\|main\n` |

Dynamic ones: the store's Back button (with `proto` ≥ 88) sends the parent tab and the last selection; dialog
`OPENSTORE/<item>/<selection>` links and url-prompt buttons send the parts of the link.

<small>Builders: `0x1c61b4c`, `0x13940cc`, `0x1ce4990`, `0x1773c00`, `0x175dcdc`, `0x1693460`, `0x16a2f7c`.</small>
