# OnHelpRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Opens the help menu (`HelpMenuContainer`, under `WorldSpecificGUI`), built from argument 1 with the generic
dialog builder like other menu requests (`0x16d211c`). If the help menu isn't open and another menu or
dialog is open (the pause menu excepted), the client logs "Ignoring dialog request" and does nothing. If the
help menu is already open, it is rebuilt with the new text.

| # | Type | Meaning |
|---|---|---|
| 1 | string | dialog text (the OnDialogRequest format) |

### Decompiled handler

```c
void OnHelpRequest(GameLogic *self, VariantList *args) {
    if (!FindEntity(GetEntityRoot(), "HelpMenu") && IsAnyMenuOpen()
        && !FindEntity(GetEntityRoot(), "PauseMenu")) {
        Log("Ignoring dialog request");
        return;
    }
    BuildHelpMenu(FindEntity(GetEntityRoot(), "WorldSpecificGUI"), arg1.str);   // 0x16d211c
}
```

<small>Handler: `0x136ea28` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x137d330`, `0x16d211c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnHelpRequest", "..." });
```
