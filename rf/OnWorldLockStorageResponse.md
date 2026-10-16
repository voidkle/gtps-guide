Fills the World Lock storage screen.
Registered by `WorldLockStorageController::OnActivate` (`0x1d7cb38`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

| # | Type | Meaning |
|---|---|---|
| 1 | string | **MessagePack**-encoded data, below |

Argument 1 is a MessagePack array (`0x1481940`, `0x1481a90`):

| # | Type | Meaning |
|---|---|---|
| 0 | array | the entries, each `[int, int, int, string]` (meanings not traced; the string is shown) |
| 1 | int64 | probably a start time |
| 2 | int64 | not traced |
| 3 | int64 | probably a duration: the client stores element 1 + element 3 as an end time |
| 4 | int | stored on the model (+0x1c) |

The list is rebuilt from the entries and the screen refreshed.

<small>Handler: lambda `0x1d7d84c` → `0x1d7d39c` in the 5.60 arm64 client; callees read: `0x1481940`, `0x1481a90`, `0x1481bf8`, `0x1482214`.</small>

<!-- args: string -->
