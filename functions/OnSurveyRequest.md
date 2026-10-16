# OnSurveyRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Opens the survey menu, built from argument 1 with the normal dialog builder, like
[OnDailyRewardRequest](./OnDailyRewardRequest). If the survey menu is already open, the client logs
"To replace content" and keeps the open one; the new text is not used.

| # | Type | Meaning |
|---|---|---|
| 1 | string | dialog text (the OnDialogRequest format) |

Before building, the client runs its own `HideWorldUI` function and sets the local avatar to state 2
(`0x12eca8c`). The menu is a child of the `WorldSpecificGUI` entity.

### Decompiled handler

```c
void OnSurveyRequest(GameLogic *self, VariantList *args) {
    Entity *gui = FindEntity(GetEntityRoot(), "WorldSpecificGUI");
    OpenSurveyMenu(gui, arg1.str);                        // 0x177f7a8
}

Entity *OpenSurveyMenu(Entity *gui, std::string text) {   // 0x177f7a8
    if (g_survey.open) { Log("To replace content"); return g_survey.entity; }
    CallFunction(GameLogic(), "HideWorldUI");
    if (NetAvatar *me = GameLogic()->GetLocalPlayer()) me->SetState(2);
    return g_survey.Build(gui, text);                     // 0x177f988
}
```

<small>Handler: `0x136e680` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x177f7a8`, `0x177f988`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSurveyRequest", "..." });
```
