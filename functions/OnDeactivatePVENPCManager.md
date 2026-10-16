# OnDeactivatePVENPCManager

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Stops the PvE enemy manager and deletes all its enemies. Like the other PvE calls it only works when the server's `proto` is
999999 or more, and only if the manager is active. No arguments.

### Decompiled handler

```c
void OnDeactivatePVENPCManager(GameLogic *self, VariantList *v) {
    if (self->pve && self->pve->active)           // +0x4d8, +0xb8c
        self->pve->Deactivate();                  // 0x14c0684: proto check, active = 0, delete all enemies and lists
}
```

<small>Handler: `0x13718e0` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x14c0684`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnDeactivatePVENPCManager" });
```
