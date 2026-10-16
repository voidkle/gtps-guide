The server's answer to "claim all" in the mailbox.
Registered by `MailBoxController::OnActivate` (`0x1d0e0ec`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | int | 1 = success; anything else = failed |

On failure the client logs "Fail to claim all reward." and closes the mailbox.

<small>Handler: lambda `0x1d1009c` in the 5.60 arm64 client.</small>

<!-- args: int -->
