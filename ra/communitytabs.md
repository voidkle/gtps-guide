**Format correction:** optional extra lines: `category|<cat>\n` and `selection|<sel>\n` (from dialog links).

The community hub tabs.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `type` | the tab: a button whose name contains `community_` or `community_worlds_` sends its own name; Back sends the last tab |
| `category` | optional, from an `OPENCOMMUNITY/<type>/<category>` dialog link (`cat`) |
| `selection` | optional, from dialog links and `gazette_` buttons |

<small>Builders: `0x1668ca8` (hub buttons), `0x1663bb4` (Back), `0x1693460` (dialog `OPENCOMMUNITY` links and gazette buttons).</small>
