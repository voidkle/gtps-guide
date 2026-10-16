# ShowWorldUI

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Shows the world screen's UI again after [HideWorldUI](./HideWorldUI) (if the main UI exists) and re-applies the current screen mode, see [ApplyScreenMode](./ApplyScreenMode).
Registered by `WorldUIController::OnActivate` (`0x1c604a4`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

No arguments. Logs `ShowWorldUI`.

<small>Handler: lambda `0x1c627f0` → `0x1c612ec` in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "ShowWorldUI" });
```
