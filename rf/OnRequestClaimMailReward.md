The server's answer to claiming one mail's reward. Two listeners on GameLogic's functions (through `0x1be9ae8`),
both needing header `netID` -1, each only while its screen is open: the mailbox (`MailBoxController::OnActivate`,
`0x1d0e0ec`) and a single opened mail (`MailMessageController::OnShow`, `0x1d15d90`).

| # | Type | Meaning |
|---|---|---|
| 1 | int | 0 = failed, anything else = success |

- Mailbox: on 0 logs "Fail to claim reward." and closes the mailbox; on success nothing happens here.
- Opened mail: on 0 logs "Fail to claim reward." and calls the mail's callback (+0x380); on success closes the mail.

<small>Handlers: lambda `0x1d0ff94` → `0x1d0f9bc` and lambda `0x1d1662c` → `0x1d16398` in the 5.60 arm64 client.</small>

<!-- args: int -->
