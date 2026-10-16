# Login

This page covers what a private server needs: server_data.php and the ENet login that gurotopia and
GrowServer accept. The official servers add a web login in between: a token from the login site, an
`ltoken` message to a login server, then a redirect to a game server. That flow, as the 5.60 client runs it, is
on [Login on the official servers](/guide/official-login).

## 1. server_data.php (HTTPS)

Before ENet, the client posts to `https://www.growtopia1.com/growtopia/server_data.php` (falling back to
`www.growtopia2.com`) and reads:

```text
server|192.168.1.10
port|17091
type|1
type2|1
#maint|Server under maintenance. Please try again later.
loginurl|login-gurotopia.vercel.app
meta|gurotopia
RTENDMARKERBS1001
```

The 5.60 client also understands `beta_server`, `beta_port`, `beta_loginurl`, `beta_type` and
`beta_maint` (plus `beta2_*` and `beta3_*`), which it uses after a server has put it in beta mode with
`OnSetBetaMode`.

::: warning The official Android app
Recent Android versions of the app only accept a certificate signed by a real authority for
`www.growtopia1.com`, so they never get past this step on a private server. Your own client
([Talk to the server](/guide/talk-to-server)) skips HTTPS entirely: it already knows the address.
:::

## 2. ENet login, gurotopia

`include/action/protocol.cpp` and `include/action/tankIDName.cpp`:

1. Server → [SERVER_HELLO](/messages/1-server-hello).
2. Client → [GENERIC_TEXT](/messages/2-generic-text):
   ```text
   protocol|225
   ltoken|<base64 of "growId=NAME&password=PASS">
   ```
   A GrowID that doesn't exist yet is created with that password (`peer::load()`).
3. Server → [OnSendToServer](/functions/OnSendToServer)`(port, 0, user_id, "ip|0|0", 1, growid)`.
4. Client → GENERIC_TEXT starting with `tankIDName|NAME`, containing `protocol|` (non-zero) and
   `user|<user_id from step 3>`. gurotopia schedules a disconnect if the message has fewer than 41
   `|`-separated fields. The official client reconnects first; gurotopia also accepts it on the same
   connection.
5. Server → `OnOverrideGDPRFromServer`, [OnSuperMainStartAcceptLogon…](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a).
6. Client → [action|enter_game](/actions/enter_game).
7. Client → [action|join_request](/actions/join_request).

## 2. ENet login, GrowServer

`src/game/server/game-server.ts` and `src/game/player/auth.ts`:

1. Server → SERVER_HELLO.
2. Client → text with `ltoken|<base64(url-encoded _token=SESSION&...)>`. `SESSION` must be a session
   token from GrowServer's own login website; a GrowID and password alone aren't accepted.
3. Server → OnSendToServer with a one-time transfer token (valid 60 s), then disconnects.
4. Client reconnects and sends `tankIDName|`, `token|<transfer token>`, `user|<player id>`.
5. Server → OnSuperMainStartAcceptLogon….

## The client's login messages (5.60)

The **ltoken message** (client function `0x1805e08`):

```text
protocol|{}
ltoken|{}
platformID|{}
rcdl|{}
adc|{}            (only with Apple consent)
```

The **full login message** (`0x180145c`), fields in order:

```text
tankIDName|  tankIDPass|  requestedName|  f|  protocol|  game_version|  fz|  cbits|  hash2|  vid|
aid|  gid|  meta|  rid|  platformID|  deviceVersion|  country|  hash|  mac|  user|  token|  doorID|
wk|  fhash|  GDPR|  player_age|  category|  totalPlaytime|  klv|  lmode|  reconnect|1  FCMToken|
```

`tr|` comes first when present. `user|` and `token|` echo what the server sent in OnSendToServer.
gurotopia reads only `tankIDName`, `protocol`, `country` and `user`.

## What the server sends after enter_game

Captured from gurotopia with [hello.cpp](/guide/talk-to-server):

```text
<- OnSendToServer
<- OnOverrideGDPRFromServer
<- OnSuperMainStartAcceptLogonHrdxs47254722215a
<- OnConsoleMessage Welcome back, `wclienttest``. No friends are online.
<- OnConsoleMessage
<- OnConsoleMessage `5Personal Settings active:`` `#Can customize profile``
<- game packet 0x09 (79 bytes)            SEND_INVENTORY_STATE
<- OnSetBux
<- SetHasGrowID
<- OnTodaysDate
<- OnRequestWorldSelectMenu
<- OnConsoleMessage Where would you like to go? (`w1`` online)
<- OnDialogRequest                        the gazette
<- game packet 0x16 (60 bytes)            PING_REQUEST
<- OnSetFeatureEnableFlags
```
