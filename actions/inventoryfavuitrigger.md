# action|inventoryfavuitrigger

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|inventoryfavuitrigger
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Tapping the **Remove Favorites** entry (item 13720) in the inventory, when the server's `proto` allows favourites.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|inventoryfavuitrigger\n` |

- The same tap handler sends `action|storenavigate\nitem|locks\nselection|upgrade_backpack\n` for the
  **Increase Backpack** entry (item 9412).

<small>Builder: `0x13940cc` (inventory touch handler, set up in `0x13925b8`).</small>

## Server

gurotopia: [`include/action/inventoryfavuitrigger.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/inventoryfavuitrigger.cpp).

Reply: `OnDialogRequest`.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|inventoryfavuitrigger\n");
```

<small>Client function: `0x13940cc` in libgrowtopia.so 5.60.</small>
