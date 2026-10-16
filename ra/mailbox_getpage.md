The mailbox asks for a page of messages (on open and "next page").

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `pageIndex` | the page (≥ -1) |

- Marks a request as pending and refreshes the list view.

<small>Builder: `0x1d0e738`; called from `0x1d0e0ec` (`MailBoxController::OnActivate`), `0x1d11350`.</small>
