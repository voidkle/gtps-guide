**Format correction:** `location` has three values: `gem`, `bottommenu` and `pausemenu`.

Opens the store. The server answers with [OnStoreRequest](/functions/OnStoreRequest).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `location` | `gem`: the gems counter in the world UI; `bottommenu`: the inventory bar's **STORE** button; `pausemenu`: **mainStore** in the pause menu |

- `gem` and `bottommenu` aren't sent while another menu is open.

<small>Builders: `0x1c6120c` (gems, via `0x1c622d4`), `0x16f774c` (item bar), `0x17289bc` (pause menu).</small>
