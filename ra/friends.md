**Format correction:** two forms: `action|friends\ndelay|<ms>\n` and `action|friends\nlocation|pausemenu\n`.

Opens the friends list (the server answers with a dialog).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `delay` | `0` from the world UI friends button; `500` from the community hub's Back button when no tab was open |
| `location` | `pausemenu` from the pause menu's **FriendsMenu** button (no `delay` line) |

- The world UI button does nothing while the options or pause menu is open
  ("Options menu already active, not showing friends menu").

<small>Builders: `0x1c60de0` (world UI, via `0x1c621d4`), `0x1663bb4` (community hub Back), `0x17289bc` (pause menu).</small>
