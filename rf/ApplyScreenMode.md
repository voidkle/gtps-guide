Re-applies the client's current screen mode (app+0xbd8) to the world UI, choosing which parts are hidden (the `full-hide`, `ftue-hide` and `petbattle-hide` classes). Mode 0 is the normal UI; 1, 2 and 3 hide more of it (2 is the screenshot mode).
Registered by `WorldUIController::OnActivate` (`0x1c604a4`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

No arguments; the mode is not taken from the call.

<small>Handler: lambda `0x1c62974` → `0x1c612ec` in the 5.60 arm64 client.</small>

<!-- args: -->
