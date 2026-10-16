# action|store

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|store
location|{}
```

## Fields

| Field | Meaning |
|---|---|
| `location` | Where the menu was opened from: `gem`, `bottommenu`, `pausemenu`, ... |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** `location` has three values: `gem`, `bottommenu` and `pausemenu`.

Opens the store. The server answers with [OnStoreRequest](/functions/OnStoreRequest).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `location` | `gem`: the gems counter in the world UI; `bottommenu`: the inventory bar's **STORE** button; `pausemenu`: **mainStore** in the pause menu |

- `gem` and `bottommenu` aren't sent while another menu is open.

<small>Builders: `0x1c6120c` (gems, via `0x1c622d4`), `0x16f774c` (item bar), `0x17289bc` (pause menu).</small>

## Server

gurotopia: [`include/action/store.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/store.cpp).

Reply: `OnStoreRequest` with the store page.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|store\nlocation|gem\n");
```

<small>Client function: `0x1c6120c, 0x16f774c, 0x17289bc` in libgrowtopia.so 5.60.</small>
