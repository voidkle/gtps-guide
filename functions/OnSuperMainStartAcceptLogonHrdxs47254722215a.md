# OnSuperMainStartAcceptLogonHrdxs47254722215a

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Login accepted. The server sends the data file hashes, the CDN location, a list of apps to check for, and a
settings string. The client checks its local `items.dat` and `player_tribute.dat`, asks for new copies if
they differ, applies the settings, and continues into the game.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | hash of `items.dat` (proton's `HashString` over the file, `0x1e69d5c`) |
| 2 | string | CDN host (GameLogic+0x520) |
| 3 | string | CDN path (GameLogic+0x538) |
| 4 | string | space-separated Android package names to check; only used if it's a string. See [the app check](#the-app-check) |
| 5 | string | settings, `key=value` entries separated by `\|`; see [the settings](#the-settings) |
| 6 | uint | hash of `player_tribute.dat`; 0 = skip the tribute check (gurotopia doesn't send it) |

### After connecting

What happens next depends on the logon mode from [OnSendToServer](./OnSendToServer) argument 5 (app+0x9a0 → +0xc0, 0 on the first connection):

- **Logon mode ≥ 2:** the client skips the file checks and sends at once
  ```text
  action|enter_game
  invitedWorld|<empty>
  crossplaySetting|<value of 0x1083658>
  ```
- **Logon mode &lt; 2:**
  1. Hashes its `items.dat`. Equal to argument 1: logs `Loading items data.`, loads it, and starts a thread
     (`0x1ba76a8`) that loads the rest of the base data and then sends `action|enter_game`
     ("EnterGame: Loading base data", "EnterGame: Entering game.."). Different: logs
     `Need to refresh items data. Request it.` and sends `action|refresh_item_data\n`.
  2. If argument 6 isn't 0: hashes `player_tribute.dat`. Equal: loads it (using `proto`). Different:
     sends `action|refresh_player_tribute_data\n`.
  3. Loads `Profanity_Filter_Update.dat`.

### The app check

If argument 4 is a string, the client splits it on spaces and asks Android whether each package is installed
(`is_app_installed`, through JNI, `0x1422e88`). Then it sends a game packet
[APP_CHECK_RESPONSE (0x18)](/packets/18-app-check-response):

| Field | Value |
|---|---|
| `netID` | the 1-based position in the list of the **last** installed package; -1 if none is installed |
| `itemID` | sum of `HashString(name)` over the packages that are **not** installed |

All other header fields are 0. A server that knows the list can compute the expected `itemID` for "none
installed" and compare.

### The settings

Argument 5 is split on `|`, each entry on `=`. Before reading it the client sets `proto` to 15 and the menu
music to `audio/mp3/about_theme.mp3`. Recognized keys:

| Key | Effect |
|---|---|
| `use_beta_files` (no value) | app+0xbe5 = 1, logs "Using beta files" |
| `use_mod_beta_files` (no value) | app+0xbe8 = 1, logs "Using test server media..." |
| `choosemusic` | menu music file (app+0xbf0) |
| `game_theme` | sets the UI theme (`0x17f7c40`) |
| `proto` | the protocol number (app+0xc08), used by many handlers to pick old or new formats. If it's > 136 and the client hasn't done it before, the saved setting `enable_msg_icon` is set to 1 once |
| `active_holiday` | GameLogic+0x38c |
| `wing_week_day` | GameLogic+0x390 |
| `server_tick` | the server's clock (GameLogic+0x394, `strtoul` base 0); the client's own tick at that moment goes to +0x398 |
| `clash_active` | `1` = on (GameLogic+0x39c) |
| `drop_lavacheck_faster` | `1` = on (GameLogic+0xb8) |
| `isPayingUser` | `1` = on; saved as the `isPayingUser` setting |
| `usingIgnoreSeal` | `1` = on (app+0xcca) |
| `enableInventoryTab` | `1` = on (app+0x999) |
| `usingTransmutationIcon` | `1` = on (app+0xccb) |
| `usingStoreNavigation` | `1` = on (app+0xcc9) |
| `exclusiveInventoryTabs` | passed to `0x1ba713c` |
| `enableInventoryTabExculseMobile` (sic) | `1` = on (app+0xcc8) |
| `bigBackpack` | `1` = on (GameLogic+0x4d0) |
| `eventButtons` | JSON for the event buttons (`0x1ba74ac`) |
| `seed_diary_hash` | compared with the hash of the local seed diary; if they differ, the saved setting `seed_diary_hash_dirty` is set to 1 (see [OnSendSeedDiaryData](./OnSendSeedDiaryData)) |
| `m_clientBits` | only with `proto` ≥ 203: bit 12 → app flag 0x1000, bit 11 → app flag 0x800 |

Boolean keys are on only when the value starts with `1`. Unknown keys are ignored; keys are case-sensitive.
On Android (platform 4), if the saved setting `forceIAPsync` exists, it's removed, app+0xe10 is set and the
store purchases are re-synced (`0x1d935d8`). Finally a few GameLogic fields are reset (+0x418…+0x430, +0x3a4).

### Decompiled handler

```c
void operator()(VariantList *const &vl) { ScreenFlow_OnSuperMain(this->owner, vl); }   // 0x1ba8524

void ScreenFlow_OnSuperMain(ScreenFlow *self, VariantList *args) {     // 0x1ba4ab4, condensed
    uint itemsHash = args->GetUInt(0), tributeHash = args->GetUInt(5);
    int proto = 0;
    if (args->type(4) == STRING)
        for (auto &e : Split(args->GetString(4), "|")) { auto kv = Split(e, "="); if (kv.size() > 1 && kv[0] == "proto") proto = atoi(kv[1]); }
    ProcessConnection(self, itemsHash, tributeHash, args->GetString(1), args->GetString(2), proto);  // 0x1ba6598
    GetApp()->client->f_a5 = 1;
    if (args->type(3) == STRING) {                                     // app check
        int last = -1, sum = 0, i = 0;
        std::string list = args->GetString(3);
        for (std::string name; !(name = PopToken(list, " ")).empty(); ) {
            i++;
            if (IsAppInstalled(name)) last = i; else sum += HashString(name);
        }
        GameHeader h = {}; h.type = 0x18; h.netID = last; h.itemID = sum;
        SendGamePacket(4, &h, 0x38, NULL, peer, 1);
    }
    GetApp()->useBeta = GetApp()->useModBeta = 0;
    GetApp()->menuMusic = "audio/mp3/about_theme.mp3";
    SetProto(GetApp(), 15);                                            // 0x108457c
    if (args->type(4) == STRING)
        for (auto &e : Split(args->GetString(4), "|")) {
            if (e == "use_beta_files")     { Log("Using beta files"); GetApp()->useBeta = 1; }
            if (e == "use_mod_beta_files") { Log("Using test server media..."); GetApp()->useModBeta = 1; }
            auto kv = Split(e, "=");
            if (kv.size() < 2) continue;
            ApplySetting(kv[0], kv[1]);                                // the table above
        }
    ...
}

void ProcessConnection(ScreenFlow *self, uint itemsHash, uint tributeHash,
                       string host, string path, int proto) {         // 0x1ba6598
    Log("Processing connection...");
    GameLogic()->cdnHost = host; GameLogic()->cdnPath = path;          // +0x520, +0x538
    if (GetApp()->client->logonMode >= 2) {
        SendText(2, "action|enter_game\ninvitedWorld|" + std::string() + "\ncrossplaySetting|" + CrossplaySetting() + "\n");
        return;
    }
    uint32_t h = HashFile("items.dat");
    PlayerTribute()->hash = tributeHash;
    LoadProfanityFilter("Profanity_Filter_Update.dat");
    if (h == itemsHash) { Log("Loading items data."); LoadItems(); StartEnterGameThread(self); Log("Loading items data done."); }
    else { Log("Need to refresh items data. Request it."); SendText(2, "action|refresh_item_data\n"); ShowLoading(); }
    if (tributeHash) {
        if (HashFile("player_tribute.dat") == tributeHash) LoadTribute(proto);
        else { SendText(2, "action|refresh_player_tribute_data\n"); ShowLoading(); }
    }
}
```

<small>Handler: `0x1ba8524` → `0x1ba4ab4`, `0x1ba6598` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x1422e88`, `0x1e69d5c`, `0x157ee8c`, `0x157f060`, `0x108457c`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnSuperMainStartAcceptLogonHrdxs47254722215a"` |
| 1 | uint | items.dat hash |
| 2 | string | CDN host |
| 3 | string | CDN path |
| 4 | string | blocked app list |
| 5 | string | settings: proto|...|active_holiday|...|eventButtons=... |

Login accepted. The client answers with `action|enter_game` (and `refresh_item_data` if its items.dat hash differs).

gurotopia: `include/action/tankIDName.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnSuperMainStartAcceptLogonHrdxs47254722215a", 1u, "...", "...", "...", "...", 1u });
```
