Hides the world screen's UI (adds the `full-hide` style class), probably for cut-scenes.
Registered by `WorldUIController::OnActivate` (`0x1c604a4`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

No arguments. Logs `HideWorldUI`.

<small>Handler: lambda `0x1c6255c` → `0x1c60314` in the 5.60 arm64 client.</small>

<!-- args: -->
