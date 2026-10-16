# action|communitytabs

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|communitytabs
type|{}
```

## Fields

| Field | Meaning |
|---|---|
| `type` | Which tab or type was picked. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** optional extra lines: `category|<cat>\n` and `selection|<sel>\n` (from dialog links).

The community hub tabs.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `type` | the tab: a button whose name contains `community_` or `community_worlds_` sends its own name; Back sends the last tab |
| `category` | optional, from an `OPENCOMMUNITY/<type>/<category>` dialog link (`cat`) |
| `selection` | optional, from dialog links and `gazette_` buttons |

<small>Builders: `0x1668ca8` (hub buttons), `0x1663bb4` (Back), `0x1693460` (dialog `OPENCOMMUNITY` links and gazette buttons).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|communitytabs\ntype|0\n");
```

<small>Client function: `0x1663bb4` in libgrowtopia.so 5.60.</small>
