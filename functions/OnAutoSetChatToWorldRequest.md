# OnAutoSetChatToWorldRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Switches the chat window to its world tab. It sets a global flag (0x2adc2ac = 1) and selects tab 1 of the
chat's `TabComponent`, which sits inside the `TabContainer` entity.

No arguments are read.

### Decompiled handler

```c
void OnAutoSetChatToWorldRequest(GameLogic *self) {
    g_autoChatToWorld = 1;                                       // 0x2adc2ac
    Entity *c = FindEntity(GetEntityRoot(), "TabContainer");
    if (c) {
        TabComponent *t = dynamic_cast<TabComponent *>(c->GetComponent("TabComponent"));
        if (t) t->selected = 1;                                  // +0x88
    }
}
```

<small>Handler: `0x135d130` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnAutoSetChatToWorldRequest" });
```
