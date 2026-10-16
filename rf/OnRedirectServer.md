Moves the client to another server address and reconnects there. Unlike [OnSendToServer](./OnSendToServer)
it goes through the connection screen: the client logs out of the current server and the
`ConnectionScreenController` connects to the stored address.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | string | host (app context +0x428) |
| 2 | int | port (app context +0x440) |
| 3 | string | stored at app context +0x448; how the connection screen uses it wasn't traced |

Steps: store the three values, run GameLogic's [OnLogout](./OnLogout) handler (`0x136b858`) with an empty
argument list, then switch to a new `ConnectionScreenController`.

### Decompiled handler

```c
void operator()(VariantList *const &vl) { ScreenFlow_OnRedirectServer(this->owner, vl); }   // 0x1ba8630

void ScreenFlow_OnRedirectServer(ScreenFlow *self, VariantList *args) {   // 0x1ba3c80
    AppContext *c = self->appContext;                                   // self+0x60
    c->redirectHost = args->GetString(0);                               // +0x428
    c->redirectPort = args->GetInt(1);                                  // +0x440
    c->redirectArg3 = args->GetString(2);                               // +0x448
    VariantList empty;
    GameLogic()->OnLogout(&empty);                                      // 0x136b858
    SetScreen(self, std::make_shared<ConnectionScreenController>(self->appContext));   // 0x1ba9a3c
}
```

<small>Handler: `0x1ba8630` → `0x1ba3c80` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x136b858`, `0x1ba9a3c`, `0x1b72ee4`.</small>

<!-- args: string,int,string -->
