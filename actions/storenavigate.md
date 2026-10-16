# action|storenavigate

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|storenavigate
item|{}
selection|{}
```

## Fields

| Field | Meaning |
|---|---|
| `item` | Store item or category id. |
| `selection` | Store entry inside `item`. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Server

gurotopia: [`include/action/storenavigate.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/storenavigate.cpp).

Reply: `OnStoreRequest` for that tab.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|storenavigate\nitem|main\nselection|gems_bundle06\n");
```

<small>Client function: `0x16a2f7c, 0x1773c00` in libgrowtopia.so 5.60.</small>
