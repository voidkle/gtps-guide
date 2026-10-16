# ToggleScreenshotMode

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Toggles the screenshot mode: flips the app variable `hide_ui` between 0 and 1 and switches the screen mode to 2 (UI hidden) or back to 0 (`0x10843b0`). `ToggleScreenshotMode` and `OnPlayerScreenShotMode` do the same thing.
Registered by `WorldUIController::OnActivate` (`0x1c604a4`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

No arguments. Logs the function name.

<small>Handler: lambda `0x1c62aac` → `0x1c617b0` in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "ToggleScreenshotMode" });
```
