# OnRequestReadMailMsg

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Registered for the mailbox by `MailBoxController::OnActivate` (`0x1d0e0ec`, header `netID` -1), but the handler is
empty: the client accepts the call and does nothing.

<small>Handler: lambda `0x1d1001c` (a bare `ret`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnRequestReadMailMsg" });
```
