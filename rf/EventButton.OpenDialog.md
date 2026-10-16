Opens one of the client's built-in screens by name. It runs the same code as
[OnDialogRequestRML](./OnDialogRequestRML) (`0x1c00ab0`); the event buttons' `buttonAction` uses it (see
[OnEventButtonDataSet](./OnEventButtonDataSet)). Registered by `WorldScreen::OnShow` (`0x1c00384`) as a listener on
GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1, and only while you are in a world.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the screen name (`show_mailbox_ui`, ...; the list is on [OnDialogRequestRML](./OnDialogRequestRML)) |
| 2 | string | passed to the screen's open function |

- If a menu is already open the call is ignored (`Dialog already opened. Ignore dialog {}.`).
- An unknown name makes the client send `action|<name>\n` (message type 2) to the server instead.

<small>Handler: lambda `0x1c088c4` → `0x1c00ab0` (registered by `0x1c00384`) in the 5.60 arm64 client.</small>

<!-- args: string,string -->
