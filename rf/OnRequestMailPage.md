Fills the mailbox with a page of mails.
Registered by `MailBoxController::OnActivate` (`0x1d0e0ec`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | int | 0: no mail; the client logs "No messages for load" and stops |
| 2 | string | the mails, **MessagePack**-encoded (not JSON), below |
| 3 | int | stored on the mailbox (model+0x30), probably the page number |
| 4 | int | stored on the mailbox (model+0x34), probably the number of pages |

Argument 2 is a MessagePack array `[mails, int, int]` (`0x147c380`, `0x14801f8`); the first int is stored at
model+0x50. Each mail is an array of up to 13 values (`0x148036c`, `0x14808a4` … `0x1480c24`); trailing values may
be left out:

| # | Type | Meaning |
|---|---|---|
| 0, 1, 2 | int | not traced (one is probably the mail id the claim action uses) |
| 3, 4, 5 | string | probably the title, description and body (localization keys) |
| 6 | string | the rewards as JSON: `{"<item id>": count, ...}` (keys are read with `atoi`) |
| 7 | int | not traced |
| 8 | int64 | probably a time |
| 9 | int | not traced |
| 10, 11, 12 | string | `titleparams`, `descparams`, `messagebodyparams`: values put into the texts (the client logs them when `proto` > 218) |

Integers must be MessagePack integers (positive or negative); strings may be `str` or `bin`.

<small>Handler: lambda `0x1d0ff0c` → `0x1d0ea8c` (registered by `0x1d0e0ec`) in the 5.60 arm64 client; callees read: `0x147c380`, `0x14801f8`, `0x148036c`, `0x14808a4`, `0x148095c`, `0x1480a7c`, `0x1480b6c`, `0x1480c24`.</small>

<!-- args: int,string,int,int -->
