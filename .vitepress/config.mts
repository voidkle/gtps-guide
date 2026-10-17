import { defineConfig } from 'vitepress'
import sidebar from './sidebar.json' // @note written by docs/gen.py

export default defineConfig({
  title: 'GTPS Protocol',
  description: 'Growtopia client ↔ server packets, documented from gurotopia, GrowServer and the 5.60 client',
  base: process.env.BASE || '/', // the Pages workflow sets BASE=/gtps-guide/
  cleanUrls: true,
  srcExclude: ['README.md', 'LICENSE-DOCS.md', 'rx/**', 'rf/**', 'ra/**', 'rm/**'], // @note write-ups that gen.py pastes into the packet, function and action pages
  themeConfig: {
    nav: [
      { text: 'Guide', link: '/guide/introduction' },
      { text: 'Talk to the server', link: '/guide/talk-to-server' },
    ],
    search: { provider: 'local' },
    outline: [2, 3],
    sidebar: [
      {
        text: 'Guide',
        items: [
          { text: 'Introduction', link: '/guide/introduction' },
          { text: 'Transport (ENet)', link: '/guide/transport' },
          { text: 'Message types', link: '/guide/message-types' },
          { text: 'Game packet header', link: '/guide/game-packet' },
          { text: 'Variant lists', link: '/guide/variant-list' },
          { text: 'Login', link: '/guide/login' },
          { text: 'Login on the official servers', link: '/guide/official-login' },
          { text: 'World data', link: '/guide/world-data' },
          { text: 'Tile extras', link: '/guide/tile-extras' },
          { text: 'items.dat', link: '/guide/items-dat' },
          { text: 'Text commands from the server', link: '/guide/server-text' },
          { text: 'Dialogs', link: '/guide/dialogs' },
          { text: 'Dialog elements', link: '/guide/dialog-elements' },
          { text: 'Talk to the server', link: '/guide/talk-to-server' },
          { text: 'Relay', link: '/guide/relay' },
          { text: 'Capturing the real game', link: '/guide/capture' },
          { text: 'How the client was analyzed', link: '/guide/client-analysis' },
        ],
      },
      { text: 'Message types', collapsed: true, items: sidebar.messages },
      { text: 'Actions (client → server)', collapsed: false, items: sidebar.actions },
      { text: 'Game packets', collapsed: true, items: sidebar.packets },
      { text: 'Server functions', collapsed: true, items: sidebar.functions },
    ],
  },
})
