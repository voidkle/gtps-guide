Login finished: ask the server to put you in the game (it answers with the world menu and the rest of
[What the server sends after enter_game](/guide/login#what-the-server-sends-after-enter-game)).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|enter_game\n`, or with logon mode ≥ 2: `action\|enter_game\ninvitedWorld\|\ncrossplaySetting\|<n>\n` |

- Normal path: after [OnSuperMainStartAcceptLogon…](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a), a loader thread
  (`0x1ba7aac`) loads the base data (items, auction panel, seed diary) and sends it once no file download is pending.
- Beta mode (`use_beta_files`) skips the file updates and sends it straight away.
- Logon mode ≥ 2 (a redirect from [OnSendToServer](/functions/OnSendToServer)) sends the long form at once (`0x1ba6598`).

<small>Builders: `0x1ba7aac`, `0x1ba6598`; called from `0x1ba790c`, `0x1bad8d8`, `0x1ba4ab4`.</small>
