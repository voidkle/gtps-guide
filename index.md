---
layout: home

hero:
  name: GTPS Protocol
  text: Every Growtopia packet, one page each
  tagline: How the client and a private server talk over ENet, and how to talk to the server yourself.
  actions:
    - theme: brand
      text: Introduction
      link: /guide/introduction
    - theme: alt
      text: Talk to the server
      link: /guide/talk-to-server

features:
  - title: 87 client actions
    details: Every action|... message the 5.60 client sends, with its exact fields and what gurotopia replies.
    link: /actions/join_request
  - title: Game packets
    details: All game packet types with the header fields each one uses, from 0x00 STATE to 0x2e.
    link: /packets/00-state
  - title: Server functions
    details: OnSpawn, OnSendToServer, OnDialogRequest and the rest, with their arguments.
    link: /functions/OnSendToServer
---
