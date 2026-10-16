# Text commands from the server

A server can send [GAME_MESSAGE (3)](/messages/3-game-message) text to the client, not only receive it.
This page lists every `action|` the 5.60 client reacts to, in the order its handler (`0x1372d28`) checks them.

- The text is `key|value` lines. The first key must be `action`, or the client logs "bad net game message"
  and ignores it.
- The client overwrites the last byte of every text message with a NUL, so end the message with an extra
  `\0` (gurotopia's `send_text()` does).
- If the text contains `OnPersistentNPCMessageInputDependent` anywhere, the client logs "Found tutorial packet".
  That changes nothing else.
- Values are read with the client's text scanner: `key|value`, one per line. A missing key reads as an empty
  string, or 0 for numbers.

```text
[u32 3] action|play_sfx\nfile|audio/gong.wav\ndelayMS|0\n [\0]
```

## log

Prints a line in the console, like [OnConsoleMessage](/functions/OnConsoleMessage).

| Key | Meaning |
|---|---|
| `msg` | the text, with `` `x `` color codes. Emoticon codes are replaced with the emoticons from [OnEmoticonDataChanged](/functions/OnEmoticonDataChanged) |

```c
if (action == "log") {
    std::string text = ReplaceEmoticons(g_emoticons, Get("msg|"));   // 0x1e63e84
    AddToLog(text);                                                     // 0x1716724: the console log
}
```

## logoff

No other keys. The client disconnects its ENet peer (`enet_peer_disconnect(peer, 0)`), and its normal
disconnect handling follows.

## play_sfx

| Key | Meaning |
|---|---|
| `file` | the sound file, e.g. `audio/gong.wav` |
| `delayMS` | wait this many ms before playing it |

The sound is played through the audio queue (`0x1e433d4`, channel type 15).

## play_music

| Key | Meaning |
|---|---|
| `file` | the music file, or `stop` |
| `delayMS` | wait this many ms before starting it |

`file|stop` stops the current music immediately and clears the GUI root's music flag (+0x2f0). Any other
value is queued like `play_sfx`, with type 20 (music).

## add_notification

| Key | Meaning |
|---|---|
| `imageFile` | the picture, e.g. `interface/atomic_button.rttex` |
| `msg` | the text |
| `audioFile` | a sound to play with it (can be empty) |
| `delayMS` | wait this many ms first |

After `delayMS` the client runs [OnAddNotification](/functions/OnAddNotification)`(imageFile, msg, audioFile)`
on the GUI root. After `delayMS + 1000` it also runs `OnAddLog(msg)` there, which adds the text to the log.

```c
RunLater(GetApp()->gui, delayMS,        "OnAddNotification", { image, msg, audio });   // 0x1e443fc
RunLater(GetApp()->gui, delayMS + 1000, "OnAddLog",          { msg });
```

## logon_fail

No other keys. The login was refused.

- **First connection** (logon mode 0, netclient+0xc0): the client sends `action|quit` and disconnects (`0x11424bc`).
- **After a redirect** (logon mode not 0): it disconnects and reconnects after 2 seconds (`0x11433d4`).

See [Login on the official servers](/guide/official-login#_3-enet-the-login-server).

## Everything else: GameTextMessage

Any other action is passed on as GameLogic's `GameTextMessage` function with `{ action name, the whole
text }`. Only two screens listen to it, so these are the only other actions the client handles.

### The connection screen: set_url, request_token, request_captcha

These are only handled while the connection screen is up (during login). They're described on
[Login on the official servers](/guide/official-login#_5-game-messages-during-login).

<small>Listener: `0x1b6d8c4` → `0x1b79f08` → `0x1b737ac`.</small>

### The world menu: world_validated

The answer to [action|validate_world](/actions/validate_world), which the client sends while you type a world
name in the world menu.

| Key | Meaning |
|---|---|
| `available` | `1`: the world doesn't exist yet. `-1`: the name isn't valid. Anything else: the world exists |
| `world_name` | the name it's about |

The client stores the name and the time, then sets the hint text under the name box and the button
(`0x1c13544`):

| Case | Hint text | Button |
|---|---|---|
| empty name | "Enter a unique name to create a new world!" | |
| `start` | "Enter a world name to join friends or create your own!" | |
| `available\|1` | "Hit Enter or click 'Create World' to make this world!" (on other platforms "Press 'Y'…", "Press 'X'…" or "Tap 'Create World'…") | Create World |
| `available\|-1` | "Invalid world name - please try again!" | |
| other, while creating a world (probably, `0x1c15d04`) | "This world already exists. Try another name!" | |
| other | "Hit Enter or click 'Create World' to enter this world!" (or the Y / X / Tap versions) | Enter World |

Afterwards the client compares `world_name` with the name it is waiting for (+0x3e0); probably so an old
answer doesn't change the button for a newer name.

<small>Listener: `0x1c10eb8` → `0x1c17f14` → `0x1c174e0`.</small>

## Where this comes from

<small>Handler: `0x1372d28` (case 3 of the message dispatcher `0x114276c`); text scanner `0x157f12c`, `0x157f82c`.</small>
