Updates the first-time-user ("FTUE") task button: the current tutorial task, its text and progress.
Registered by `EventsDataController::OnActivate` (`0x1c50d04`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

The arguments depend on the client's `EnableNewFTUE` setting (GameplayFeaturesConfig, `0x1444df4`).

Old FTUE (`EnableNewFTUE` off):

| # | Type | Meaning |
|---|---|---|
| 1 | int | 1 sets a flag on the button (probably "task complete") |
| 2 | int | probably the progress value |
| 3 | int | the task number |
| 4 | string | the task, `|`-separated, at least 5 fields: title, description, a number, two more strings, and optionally a 6th field, the state (`atoi`) (`0x197bf90`). Empty: the task stays as it is |
| 5 | string | passed to the task code with argument 4 (`0x197b504`) |
| 6 | string | `a|b`: `a` != 0 probably hides the progress counter; `b` is read as a number |

New FTUE (`EnableNewFTUE` on):

| # | Type | Meaning |
|---|---|---|
| 1 | string | the task data, read by the new FTUE manager (`0x197c164`) |

- The button is created on first use (`0x1c52b80`, text "Call me!"). When every task is done it shows
  "Congratulations!" / "You have completed all tasks!".
- Title and description go into the UI model. When the task is finished, or its state is -1, the counter is set to
  100 and the progress state to 2.
- The saved setting `IsFTUEHintEnabled` decides whether the hint is shown.

The meanings of arguments 1, 2 and 6 weren't traced past the values they set.

<small>Handler: lambda `0x1c54db0` → `0x1c52008` (registered by `0x1c50d04`) in the 5.60 arm64 client; callees read: `0x1444df4`, `0x197bf90`, `0x197c164`, `0x1c52b80`, `0x1c53164`.</small>

<!-- args: int,int,int,string,string,string -->
