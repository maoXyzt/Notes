import type { HeadConfig } from 'vitepress'
import constants from './constants'

export const head: HeadConfig[] = [
  ['link', { rel: 'icon', href: `${constants.base_url}favicon.ico` }],
  [
    'script',
    {},
    `
    window._hmt = window._hmt || [];
    (function() {
      var hm = document.createElement("script");
      hm.src = "https://hm.baidu.com/hm.js?91e91f9b5d7694a3c392c2e570906a78";
      var s = document.getElementsByTagName("script")[0];
      s.parentNode.insertBefore(hm, s);
    })();
    `,
  ],
]
