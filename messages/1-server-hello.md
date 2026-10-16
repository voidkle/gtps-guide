# 1 SERVER_HELLO

<Badge type="info" text="message type" /> <Badge type="info" text="server → client" />

Sent by the server as soon as an ENet connection is up. The body is empty; it means "send your login now".

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

The client doesn't read the body. On this message it sends its login text as a
[GENERIC_TEXT (2)](/messages/2-generic-text). When the connection is a redirect (the logon mode from
[OnSendToServer](/functions/OnSendToServer), netclient+0xc0, isn't 0), it first adds
"Logging on `<tankid_name>`..." to the console log (the saved `tankid_name` setting). The text itself is built by the
login object at netclient+0xc8 (its vtable +0x10); the fields are on [Login](/guide/login) and
[Login on the official servers](/guide/official-login).

```c
case 1:
    if (net->logonMode != 0)                                       // net+0xc0
        AddToLog(fmt("Logging on {}...", GetVar("tankid_name")));         // 0x1716724
    std::string text = net->loginBuilder->Build(net);              // (net+0xc8)->vtable[2]
    SendText(2, text, event->peer);                                // 0x157f060
```

<small>Case 1 of the dispatcher `0x114276c`.</small>

## Layout

```text
[u32 1][u8 0]
```

Bytes on the wire:

```text
01 00 00 00 00
```

gurotopia: `include/eventType/connect.cpp`.
