The client's own route for text commands from the server. A [GAME_MESSAGE (type 3)](/messages/3-game-message)
whose action the client doesn't handle itself is passed on as this function (see
[Text commands from the server](/guide/server-text#everything-else-gametextmessage)). It is a normal GameLogic
function, so a server can also call it directly with CALL_FUNCTION (header `netID` -1); the effect is the same.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the action name, for example `set_url` |
| 2 | string | the whole text message (`action|...\n...`) |

Two screens listen to it, each only while it is active:

- Connection screen (`ConnectionScreenController::OnActivate`, `0x1b6d8c4`; handler `0x1b737ac`): handles
  `set_url`, `request_token` and `request_captcha`. See [Login on the official servers](/guide/official-login).
- World menu (`WorldSelectScreen::OnShow`, `0x1c10eb8`; handler `0x1c174e0`): handles `world_validated`, the answer
  to [validate_world](/actions/validate_world).

### Decompiled handler

```c
void GameTextMessage_Connection(ConnectionScreen *self, VariantList *v) {   // 0x1b737ac
    std::string action = v[1].s, text = v[2].s;
    if (action == "set_url")         { /* reads url| and label| from text */ ... }
    else if (action == "request_token")   { /* "Get request_token, retry login" */ ... }
    else if (action == "request_captcha") { ... }
}
```

<small>Handlers: lambdas `0x1b79f08` → `0x1b737ac` and `0x1c17f14` → `0x1c174e0` in the 5.60 arm64 client.</small>

<!-- args: string,string -->
