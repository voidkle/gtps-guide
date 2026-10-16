Refreshes the `PlayerInfo` UI model (your name, level and similar on the world screen).
Registered by `WorldUIController::OnActivate` (`0x1c604a4`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

No arguments. The client fires it itself when your avatar spawns; a call from the server only causes a refresh.

<small>Handler: lambda `0x1c62694` → `0x19240ac` in the 5.60 arm64 client.</small>

<!-- args: -->
