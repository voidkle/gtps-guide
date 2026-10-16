# Talk to the server

You don't need the Growtopia app to play on your server. Anything that speaks ENet with the three
Growtopia changes can log in and send the same packets the app does. This page builds the smallest
such client, `docs/examples/hello.cpp`. It logs in, joins a world, says hello in chat and prints
every packet the server sends.

## Build and run

From the repository root, with gurotopia running (`./main.out`):

```bash
g++ -std=c++20 -Iinclude docs/examples/hello.cpp -Linclude/enet/lib -lenet -lcrypto -o hello
./hello myname mypassword START 127.0.0.1 17091
```

A new GrowID is created on first login. Output from a real run:

```text
<- SERVER_HELLO, sending login
<- OnSendToServer
<- OnOverrideGDPRFromServer
<- OnSuperMainStartAcceptLogonHrdxs47254722215a
<- OnConsoleMessage Welcome back, `wclienttest``. No friends are online.
...
<- game packet 0x04 (48160 bytes)
<- OnEmoticonDataChanged
<- OnSpawn
<- OnSetPos
<- OnConsoleMessage World `wSTART`` entered.  There are `w0`` other people here, `w1`` online.
<- OnSetClothing
<- game packet 0x14 (60 bytes)
<- OnCountryState
<- OnTalkBubble
<- OnConsoleMessage CP:0_PL:0_OID:_CT:[W]_ `6<`wclienttest``>`` `$`$hello from hello.cpp````
```

## How it works

1. **Set up ENet** with the [three Growtopia changes](/guide/transport), then connect.
2. **On [SERVER_HELLO](/messages/1-server-hello)**, send the [ltoken login](/guide/login):
   `protocol|225\nltoken|<base64("growId=NAME&password=PASS")>\n` as message type 2.
3. **On [OnSendToServer](/functions/OnSendToServer)**, send the `tankIDName|...` message with
   `user|<argument 3>`. gurotopia wants at least 41 `|`-separated fields, so the example pads it.
4. **On [OnSuperMainStartAcceptLogon…](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a)**, send
   [action|enter_game](/actions/enter_game) and [action|join_request](/actions/join_request).
5. **On your own [OnSpawn](/functions/OnSpawn)** (the one with `type|local`), you're in the world. Send
   anything, for example [action|input](/actions/input).

## The code

<<< @/examples/hello.cpp

## Doing more

Every packet page ends with a **Send it yourself** line you can paste into this client. For example:

| To | Send |
|---|---|
| Move one tile right | [STATE 0x00](/packets/00-state) with your new `pos` (pixels) |
| Punch a tile | [TILE_CHANGE_REQUEST 0x03](/packets/03-tile-change-request) with `itemID` 18 |
| Place a block | 0x03 with the block's item id |
| Pick up a drop | [ITEM_ACTIVATE_OBJECT_REQUEST 0x0b](/packets/0b-item-activate-object-request) with the object uid |
| Wear an item | [ITEM_ACTIVATE_REQUEST 0x0a](/packets/0a-item-activate-request) |
| Drop or trash | [action\|drop](/actions/drop), then answer the [dialog](/guide/dialogs) |
| Change world | [action\|quit_to_exit](/actions/quit_to_exit), then [action\|join_request](/actions/join_request) |

For a complete client, see `client/main.cpp` in the repository. It's the player manager: it runs
several players at once, reads the world ([World data](/guide/world-data)), tracks inventory and drops,
answers dialogs, and has a browser UI.

## Other servers

The packets are the same on any Growtopia server, but the login differs. Pointed at GrowServer, this
client gets `Invalid login metadata, try again?`, because GrowServer wants a session token from its
login website ([Login](/guide/login)).
