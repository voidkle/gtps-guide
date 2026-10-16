# OnRequestClaimRewardsMany

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

The server's answer to "claim all" in the mailbox.
Registered by `MailBoxController::OnActivate` (`0x1d0e0ec`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | int | 1 = success; anything else = failed |

On failure the client logs "Fail to claim all reward." and closes the mailbox.

<small>Handler: lambda `0x1d1009c` in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnRequestClaimRewardsMany", 1 });
```
