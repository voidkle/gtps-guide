# OnLocalPlayerSpawned

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Refreshes the `PlayerInfo` UI model (your name, level and similar on the world screen).
Registered by `WorldUIController::OnActivate` (`0x1c604a4`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

No arguments. The client fires it itself when your avatar spawns; a call from the server only causes a refresh.

<small>Handler: lambda `0x1c62694` → `0x19240ac` in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnLocalPlayerSpawned" });
```
