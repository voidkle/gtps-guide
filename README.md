# Growtopia protocol guide

How a Growtopia client and server talk to each other: the transport, every message type, every game packet, every
action the client sends and every function a server can call on it, with the byte layouts, what the client does with
each one, and how to answer. Written so you can build a private server from it, or write a client that talks to one.

**Read it online:** https://voidkle.github.io/gtps-guide/

## What's in it

| Section | Contents |
|---|---|
| Guide | transport (ENet), message types, the 56-byte game packet header, variant lists, login (private servers and the official flow), world data, tile extras, `items.dat`, text commands, dialogs, how to talk to a server, a relay, how to decode a Wireshark capture, and how the client was analyzed |
| Message types | the 11 message types |
| Actions | the 87 `action\|...` messages the client sends, with the exact text and when it is sent |
| Game packets | the 47 game packet types, field by field |
| Server functions | the 215 functions a server can call on the client (`OnSpawn`, `OnConsoleMessage`, `OnDialogRequest`, ...) with their arguments |

Most pages come from the **5.60 Android client** (`libgrowtopia.so`), read function by function, and from the two
open source servers gurotopia and GrowServer. Each page says where a statement comes from; guesses are marked as such
("probably", "wasn't traced"). Fields that only exist to recognize the official client (device ids, integrity values)
are described as what they are, not how they are made.

## Build it locally

You need Node.js and Python 3.

```sh
npm install
npm run dev      # live preview at http://localhost:5173
npm run build    # static site in .vitepress/dist
```

`npm run build` first runs `gen.py`, which writes the `actions/`, `packets/`, `functions/` and `messages/` pages. The
tables come from `gen.py`; the explanations are hand-written fragments in `ra/` (actions), `rx/` (packets), `rf/`
(functions) and `rm/` (messages) that `gen.py` pastes into the pages. **Edit the fragments or `gen.py`, not the
generated pages**, or your changes are overwritten.

`scripts/deploy-branch.sh` builds the site and publishes it to the `gh-pages` branch.

## Layout

```text
guide/       hand-written guide pages
rx/ rf/ ra/ rm/   fragments for packet, function, action and message pages
gen.py       builds the generated pages and the sidebar
examples/    hello.cpp, the smallest client that logs in and joins a world
.vitepress/  site config
```

## License

See [LICENSE-DOCS.md](LICENSE-DOCS.md): free to read and use, free to redistribute **unmodified** and free of charge,
no selling and no modified versions without permission. It covers the documentation only, not any software.

This guide is not affiliated with or endorsed by Ubisoft or Growtopia. Growtopia is a trademark of its owner.
