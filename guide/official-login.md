# Login on the official servers

This page follows what the 5.60 Android client does when it logs in to the official servers, step by step. Everything comes from the client's own code (`libgrowtopia.so` and its Java side), not from watching the
official servers. For what gurotopia and GrowServer accept, see [Login](/guide/login).

## Overview

```text
client                      growtopia1/2.com            login site (loginurl)          ENet servers
  |                               |                             |                           |
  |-- POST server_data.php ------>|                             |                           |
  |<-- server|port|loginurl|... --|                             |                           |
  |                                                             |                           |
  |-- saved token?  yes: POST <checktoken>  (refreshToken) ---->|                           |
  |                 no:  WebView POST /player/login/dashboard -->|  (player signs in)        |
  |<-- JSON {status:"success", token, accountType, accountAge} -|                           |
  |                                                                                         |
  |-- ENet connect server:port, send  protocol|ltoken|platformID|...  -----> login server   |
  |<-- OnSendToServer(port, token, user, "ip|doorID|uuid", lmode, growid) ------------------|
  |-- DISCONNECT, connect ip:port, send  tankIDName|...|user|token|UUIDToken|doorID|aat --> game server
  |<-- OnSuperMainStartAcceptLogon…  ->  action|enter_game  ->  world menu                  |
```

The connection screen keeps a state number through all of this (`+0x40c`): 0 getting the server address,
1 web login, 2 captcha, 3 connecting to the login server, 4 handed over to a game server. Each change is also
reported to the client's analytics (`0x1b6fbc0`).

## 1. server_data.php

The client asks a web server where to connect. While waiting it shows "Getting `` `wserver address`` ``...".

| | |
|---|---|
| URL | `https://www.growtopia1.com/growtopia/server_data.php`; the retry uses `www.growtopia2.com` and adds "(using alternate)" to the text |
| Method | POST, form-encoded, through the client's CURL wrapper. Redirects to a non-HTTPS URL are refused |
| Body | `version=5.6&protocol=227&platform=<n>` |

| Field | Value |
|---|---|
| `version` | the game version as a float, `5.6` (`0x107fe6c`) |
| `protocol` | the protocol number, `227` in 5.60. The ENet login messages send the same number |
| `platform` | the platform number (`0x14213cc`). The ENet login sends the same number as `platformID` |

The reply is `key|value` lines. The client reads these keys, so a line it doesn't know about is ignored
(`RTENDMARKERBS1001` and `type2`, for example):

| Key | Used as |
|---|---|
| `error` | `error\|<code>\|<message>`: the message is shown and logged. Code `1000` means the client is too old: it reads `url` and shows an **Update Growtopia** button (or **Download Latest Version** on some platforms), and the login stops |
| `url` | the download link for `error\|1000` |
| `server` | the login server's address |
| `port` | its ENet port |
| `type` | stored at app+0xbe0 when connecting; what it changes wasn't traced |
| `maint` | if it isn't empty, the text is shown and the login stops there (maintenance) |
| `loginurl` | the host of the login site, used in step 2 |
| `endpoint` | the login page's path, default `/player/login/dashboard` |
| `checktoken` | the path for checking a saved token, default `player/growid/checktoken` |
| `beta_server`, `beta_port`, `beta_maint`, `beta_type`, `beta_loginurl` | used in place of the normal values when the client is in beta mode (see [OnSetBetaMode](/functions/OnSetBetaMode)); `beta2_*` and `beta3_*` work the same way for two more beta flags |
| `meta` | stored in the app and sent back as `meta\|` in the login message (step 4) |

If the HTTP status isn't 200, the client tries again up to 4 times. Each retry switches between
growtopia1 and growtopia2 and logs "Get web front, retry login". After that it shows "`` `4During login request an error occurred: fail to login. Please try to login again.`` ``".
Network errors show "`` `4Unable to connect to the network.`` ``".

A developer setting (a server override, app+0xa28) skips the request and loads a built-in reply that points
to `localhost:16999` instead.

<small>Request: `0x1b6ea04`; reply parser: `0x1b700fc`; retry on error: `0x1b7f95c`.</small>

## 2. The login site

Next the client needs a **token** from the login site, `https://<loginurl>`. All of its requests also send a
fixed `valKey` query parameter that is built into the client. Its value isn't given here.

**With a saved token**: when the client has a token from an earlier login and a saved GrowID name (the
`tankid_name` setting), it checks the token instead of showing the login page. It logs "Validate token." and POSTs
`refreshToken=<saved token>&clientData=<login message>` to `https://<loginurl>/<checktoken>?valKey=…`.

**Otherwise**: it logs "Request login token." and opens a WebView that POSTs `clientData` to
`https://<loginurl>/player/login/dashboard?valKey=…`. The player signs in on that page, with a GrowID,
Google, Apple or Ubisoft Connect, and a **Cancel** button under the page stops the login.

`clientData` is the same text as the ENet login message from step 4, built by the same function
(`0x180145c`) and URL-encoded. That way the site knows the device and game version before the game server
does.

### How the page hands the token back

The WebView exposes a JavaScript object named `NativeApp` to the page:

| Method | What the client does |
|---|---|
| `NativeApp.nativeSignIn(x)` | starts the platform's own sign-in (Google on Android). The result goes to `https://<loginurl>/google/native/callback?code=<code>&token=<token>`, opened in the same WebView ("Send native token.") |
| `NativeApp.onloginselection(x)`, `NativeApp.onnameselection(x)` | passed to the native code as script calls (`nativeOnScriptCall`) |
| `NativeApp.pageContent(text)` | hands the page's text to the native code |
| `NativeApp.openInBrowser(url)` | opens the link in the system browser. Links with `target="_blank"` do the same |

The answer is JSON. For the dashboard it is read from the page text (`pageContent`); for `checktoken` it is the
response body. The client reads it as follows (`0x1b99a54`):

| `status` | What happens |
|---|---|
| `success` | reads `token`, `accountType` and `accountAge`, closes the WebView and continues to step 3 |
| `failed` | shows `message` in red, if there is one |
| `close` | shows "`` `4You don't have permission to continue playing` ``" |
| `unlinked` | reads `accountType` and starts that account type's linking flow (not traced further) |
| anything else | "`` `4During login request an error occurred: fail to get validation status. Please try to login again.`` ``" |

`status` and `token` must both be strings, or the client shows "…fail to get validation response…". The
`accountType` strings the client knows are `growtopia`, `apple`, `google` and `ubiconnect` (`0x1b9e04c`).
`accountAge` is one of the client's age types: None, Kid, Teenage, Adult, AdultNotVerified.

What the client does with a good answer (`0x1b72ab0`):

1. It keeps the token, which becomes the `ltoken` in step 3, and the account type.
2. It applies the age type. Depending on it, the client turns on friends-only chat and switches off some
   features (probably the limits for younger players). For one age type it first shows an adult-verification
   notice, once.
3. It closes the WebView and connects (step 3).

The token is saved to the `Token` setting, with the account type in `LoginAccountType`, only after the login
server has accepted it and sent `OnSendToServer`. That saved token is what the next launch checks.

If a deep link opens the app during the web login (for example after signing in through the system browser),
the client opens `https://<loginurl>/<path from the link>` in the WebView ([OnGetDeeplinkData](#5-game-messages-during-login)).

## 3. ENet: the login server

The client shows "Located `` `wserver`` ``, connecting..." ("`` `5beta server`` ``" and so on in beta mode), sets the logon
mode to 0 and connects to `server:port` with [ENet](/guide/transport). After the server's [HELLO](/messages/1-server-hello) it sends one
[GENERIC_TEXT](/messages/2-generic-text) message (`0x1805e08`):

```text
protocol|227
ltoken|<token from step 2>
platformID|<platform>
rcdl|<redeem code>          only when the app was opened with a redeem-code link
adc|<0 or 1>                the AppleConsent setting
```

The login server answers in one of these ways:

- [OnSendToServer](/functions/OnSendToServer)`(port, token, user id, "ip|doorID|uuid", logon mode, growid)`:
  the token was accepted. The client disconnects (sending a [DISCONNECT (0x1a)](/packets/1a-disconnect)) and connects to
  `ip:port` (step 4).
- `action|logon_fail` ([GAME_MESSAGE](/messages/3-game-message)): with logon mode 0 the client disconnects. Otherwise it disconnects and
  reconnects after 2 seconds.
- One of the text commands in [Game messages during login](#5-game-messages-during-login).

## 4. ENet: the game server

The client connects to the address from `OnSendToServer` and, after HELLO, sends the full login message
(`0x18009d0`). It is the same text that went to the login site as `clientData`, with the redirect values at the end.
Fields are in this order, each as `key|value\n`:

| Field | What it is |
|---|---|
| `tr` | first, only when present (not traced) |
| `tankIDName`, `tankIDPass` | the saved GrowID name and password; sent only when the "remember" setting (`tankid_checkbox`) is on |
| `requestedName` | the saved `name` setting (the name a new player asked for) |
| `f` | the swear-filter setting |
| `protocol` | 227 |
| `game_version` | 5.6 |
| `fz` | an integrity value |
| `cbits` | client setting bits |
| `hash2` | a device hash |
| `vid`, `aid`, `gid` | device and advertising ids (probably vendor, Android and Google ad ids) |
| `meta` | the `meta` from server_data.php |
| `rid` | an id the client creates once and saves (`rid` setting) |
| `platformID` | the platform number |
| `deviceVersion` | the device's OS version (probably) |
| `country` | the country code |
| `hash` | a device hash |
| `mac` | the device's MAC address, or a placeholder |
| `user`, `token`, `doorID` | from `OnSendToServer` |
| `wk` | a device key (probably) |
| `fhash` | an integrity hash |
| `GDPR` | the consent value (app+0xc2c) |
| `player_age` | the age value (app+0xc30) |
| `assign_button_inverted` | a controls setting |
| `category` | the saved `last_Category` setting |
| `totalPlaytime` | the saved total play time |
| `klv` | a checksum the server uses to detect modified clients |
| `lmode` | the logon mode from `OnSendToServer` |
| `reconnect` | `1`, when this is a reconnect |
| `FCMToken` | the Firebase push token |

After a redirect, the builder then appends (`0x18009d0`):

| Field | Value |
|---|---|
| `reconnect` | `1`, if the connection is flagged as a reconnect |
| `lmode` | the logon mode from `OnSendToServer` argument 5 |
| `user` | the user id from argument 3 |
| `token` | the token from argument 2, if it isn't 0 |
| `UUIDToken` | the third part of argument 4 |
| `doorID` | the second part of argument 4 |
| `aat` | a value from the login account (probably the account age type from step 2) |

The integrity values (`fz`, `hash`, `hash2`, `fhash`, `klv`, `wk`, `rid` and the device ids) are only described
here, not how they are made. They exist so the official servers can recognise their own client.

The game server then sends
[OnSuperMainStartAcceptLogonHrdxs47254722215a](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a).
The client checks its items.dat and player_tribute.dat hashes, downloads newer files from the CDN it was given,
and answers with [action|enter_game](/actions/enter_game). With logon mode 2 or more it skips the file checks and sends
`enter_game` straight away. From there it is the same as on a private server; see
[What the server sends after enter_game](/guide/login#what-the-server-sends-after-enter-game).

## 5. Game messages during login

While the connection screen is up, [GAME_MESSAGE (3)](/messages/3-game-message) texts from the server reach it
through `GameTextMessage` (`0x1b737ac`). The connection screen also handles `OnSendToServer`, `OnReconnect`
("Reconnect requested.") and `OnGetDeeplinkData` (`0x1b6d8c4`).

| `action\|` | What the client does |
|---|---|
| `request_token` | starts the whole login again from step 1, at most 3 times ("Get request_token, retry login"). After that: "…fail to login…" and a **Retry login** button |
| `request_captcha` | reads `url\|` and `silentRequest\|`. Without `silentRequest\|1` it opens `url` in the WebView. With it, it loads `url&showCaptcha=false` in the background. If that JSON says `success` the login starts again. If it says `showcaptcha` the page is shown. On some platforms the client also shows "`` `2Please solve the captcha and press continue login button.`` ``" and a **Continue login** button |
| `set_url` | reads `url\|` and `label\|` and shows a button with that label that opens the link |

`action|log`, `logoff`, `play_sfx`, `play_music`, `add_notification` and `logon_fail` are handled before this,
in every screen (`0x1372d28`).

## Errors the player sees

| Text | When |
|---|---|
| the `maint` text | server_data.php has a `maint` value |
| the `error` message, with an update button for code 1000 | server_data.php has an `error` line |
| "`` `4Unable to connect to the network.`` ``" | the HTTP request failed |
| "`` `4During login request an error occurred: fail to login. Please try to login again.`` ``" | server_data.php failed 4 times, or `request_token` came more than 3 times |
| "`` `4During login request an error occurred: fail to get validation response. Please try to login again.`` ``" | the login site's JSON couldn't be read, or `status`/`token` was missing |
| "`` `4During login request an error occurred: fail to get validation status. Please try to login again.`` ``" | unknown `status` |
| "`` `4During login request error occurred: can't parse page content. Please try to login again.`` ``" | the page text couldn't be read |
| the `message` in red | `status` is `failed` |
| "`` `4You don't have permission to continue playing` ``" | `status` is `close` |

<small>Connection screen (`ConnectionScreenController`): server address `0x1b6ea04`, reply `0x1b700fc`, token request
`0x1b71f50`, token check `0x1b723cc`, token received `0x1b72ab0`, native sign-in `0x1b73228`, connect `0x1b6e778`,
game messages `0x1b737ac`; login-site JSON `0x1b99a54`; WebView bridge `com.rtsoft.growtopia.WebViewManager`.</small>
