# OnGetDeeplinkData

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Opens a page of the login site from a deep link while the login web page is showing.
Registered by `ConnectionScreenController::OnActivate` (`0x1b6d8c4`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the deep link without its scheme (for example `//host/path?query`); `https:` is put in front of it |

- Only used while the connection screen is in its web-login state (+0x40c == 1, see
  [Login on the official servers](/guide/official-login)). Otherwise ignored.
- The client splits `https:` + argument 1 into its parts (`0x1e54158`) and loads `https://<loginurl>` followed by
  the link's path in the login web view (`0x17bf664`), then refreshes the screen (`0x1b6e504`). Probably used to
  resume a login that was started in an external browser.

### Decompiled handler

```c
void OnGetDeeplinkData(ConnectionScreen *self, VariantList *v) {      // lambda 0x1b79f90 -> 0x1b7499c
    if (self->state != 1) return;                                   // +0x40c: web login
    Url u = ParseUrl("https:" + v[1].s);                            // 0x1e54158
    WebView()->Load("https://" + App()->loginurl + u.path, self->webViewId, 1);   // 0x17bf664, app+0x478
    self->Refresh();                                                // 0x1b6e504
}
```

<small>Handler: lambda `0x1b79f90` → `0x1b7499c` (registered by `0x1b6d8c4`) in the 5.60 arm64 client; callees read: `0x1e54158`, `0x17bf664`, `0x1b6e504`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnGetDeeplinkData", "..." });
```
