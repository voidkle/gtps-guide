Lays out the Options screen again (sliders, check boxes, the left/right UI offset controls), for example after the screen size or UI scale changed.
Registered by `OptionsScreen::OnActivate` (`0x1bb75b0`) as a listener on GameLogic's functions (through `0x1be9ae8`), so the header `netID` must be -1. The listener exists only while that screen or controller is active; at other times the call does nothing.

No arguments are read. It reads the UI scale and the saved settings the screen shows (`SfxVolSlider`,
`MusicVolSlider`, `GraphicDetailSlider`, `check_chatTimestamp`, `left_uis_offset`, `right_uis_offset`,
`check_addJump`, `ResolutionSettings`, the skin and role pickers, ...) and repositions those controls.

<small>Handler: lambda `0x1bc877c` → `0x1bc700c` (registered by `0x1bb75b0`) in the 5.60 arm64 client.</small>

<!-- args: -->
