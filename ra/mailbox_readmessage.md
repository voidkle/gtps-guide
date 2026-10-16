Opening a message in the mailbox (`mailbox.OnMessage`).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `messageID` | the message's id |

- Only sent for an **unread** message **without** rewards; the client marks it read and lowers the unread count.
  Messages with rewards are marked read by [mailbox_claimreward](./mailbox_claimreward). The message view opens either way.

<small>Builder: `0x1d1049c`.</small>
