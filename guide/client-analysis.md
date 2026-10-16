# How the client was analyzed

The client-side information on this site (the action list, the login fields, the function names and the
game packets the client sends) comes from static analysis of `libgrowtopia.so` from Growtopia 5.60
(build 426, arm64). The game's own functions have no symbol names.

## Method

1. **Strings → functions.** Disassemble `.text` with `llvm-objdump`, find every `ADRP`+`ADD` or `ADR`
   that computes an address inside `.rodata`, and group those references by function. The function
   boundaries come from the `.eh_frame` unwind records. A function that references `action|drop\n|itemID|`
   followed by `\n` builds that message, and the order of its string references gives the field order.
2. **The send function.** `0x157ee8c` is called with `(4, header, 0x38, extra, peer, 1)`: message type 4,
   a 56-byte header, reliable. It drops packets over 1,000,000 bytes, and appends `extra` only when
   header byte 12 has bit 3 set (S_EXTENDED).
3. **Game packet types.** For each call to the send function (and to the four helpers that wrap it),
   read the byte constant stored at offset 0 of the header just before the call.
4. **Game packets the client receives.** The incoming handler (`0x1373e20`) reads the type byte, sends
   anything above `0x2d` to a do-nothing default (`0x1376388`), and otherwise jumps through a table of
   46 16-bit offsets at `0x7fae44`. 34 types have their own handler, so the official server sends them.
   The other 12 (`0x02`, `0x07`, `0x0a`, `0x0b`, `0x15`, `0x17`, `0x18`, `0x19`, `0x1a`, `0x1e`,
   `0x2b`, `0x2c`) go to the default: the client ignores them, and most are types it only sends.
   The switch and every handler it reaches were then decompiled with Ghidra 12.1.4 (see below). The
   **What the client does with it** section on each packet page is written from that decompiled code:
   the fields it reads, the sub-commands it branches on, the strings and sounds it uses, and a
   cleaned-up copy of the handler.
5. **Packet names.** A static initializer (`0x108ea9c`) registers the client's own names for the types,
   `NET_GAME_PACKET_STATE` through `NET_GAME_PACKET_ON_STEP_ON_TILE_MOD` (0x2e). The packet pages use
   them. They differ from GrowServer's list from 0x19 on, for example 0x28 `FTUE_SET_ITEM_TO_QUICK_INVENTORY`
   and 0x2d `SET_EXTRA_MODS`. 0x08-0x0a aren't in the table; their names come from the servers.
6. **Server functions.** Three functions register a handler per name: `0x135e25c` (GameLogic, global
   functions), `0x12ecb2c` (NetAvatar, functions about one player) and `0x1ba1ec8` (login and menu screens,
   `std::function` lambdas added as extra listeners on GameLogic's functions). The world screen
   (`0x1bff3ec`) adds `OnDialogRequest` and `OnDialogRequestRML` the same way, and 19 more screens and
   controllers add their own names through `0x1be9ae8` while they are open (mail, auctions, dungeons, wardrobe...).
   That gives 215 names. Each
   handler was decompiled, and each function page's **What the client does with it** section is written
   from it. Handlers get a list of the arguments only: the client copies variants 1–6 into a new list,
   so the first argument is the handler's slot 0. Global functions run only when the header `netID` is
   -1; player functions run on the avatar with that `netID`.
7. **`proto`.** Many handlers check `app+0xc08`, the `proto|` value from the
   [OnSuperMainStartAcceptLogon…](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a) settings
   (default 15), to choose between old and new formats. Function pages say which value they need.

## Decompiling with Ghidra

Two settings matter, and without them Ghidra seems to time out on everything:

- **Image base 0.** Ghidra loads an arm64 `.so` at `0x100000`, so the addresses on this site (which come from
  `llvm-objdump`, base 0) point 1 MiB into the wrong code. Rebase the program to 0
  (`currentProgram.setImageBase(toAddr(0), true)`) before using any address from here.
- **Function bounds from `.eh_frame`.** Ghidra's own analysis merges and splits many functions. Recreating
  every function from the 86,682 `.eh_frame` ranges gives correct bodies, so tail calls end where they
  should.

With both, the whole 12 KB switch decompiles in about 45 seconds and most handlers in under one, with
the timeout off (`decompileFunction(f, 0, monitor)`).

The pseudo-C on the packet pages is cleaned up by hand: helper functions get descriptive names (`GetTile`,
`PlaySound`, ...), `std::string` and stack-protector code is left out, and string literals that Ghidra
drops from inlined `std::string::append` calls are filled back in from the `.rodata` references. Functions
nobody has named keep their address (`sub_14c86b8`).

## Confidence

| Badge | Meaning |
|---|---|
| <Badge type="tip" text="confirmed" /> | gurotopia sends or handles it, and the client code agrees |
| <Badge type="warning" text="inferred" /> | only seen in the client; the meaning is a reasonable guess |
| <Badge type="danger" text="unknown" /> | the client sends it, but what it means isn't known yet |

## Known gaps

- **Short names.** `OnSpawn`, `OnRemove`, `OnSetPos`, `OnSetBux` and `OnKilled` aren't in `.rodata`. Names
  of up to 22 characters fit libc++'s short-string buffer, so the compiler writes them with immediate
  `mov`/`str` instructions (case 0x04 builds `OnInitNewWorld` this way). A search for the text won't find them.
- **Meanings of stored values.** Some handlers only store a value (a cosmetic's state, a flag). Where nothing
  that reads it was found, the page says so instead of guessing.

The best way to settle the open questions is to log what the Windows app sends to your server while
playing, through a [relay](/guide/relay) or by printing in `receive()`.
