// https://vitepress.dev/guide/custom-theme
import { h } from 'vue'
import type { Theme, EnhanceAppContext } from 'vitepress'
import { inBrowser } from 'vitepress'
import DefaultTheme from 'vitepress/theme'

import './style.css'


export default {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      // https://vitepress.dev/guide/extending-default-theme#layout-slots
    })
  },
  enhanceApp({ app, router, siteData }: EnhanceAppContext) {
    // ...
    if (inBrowser) {
      router.onBeforeRouteChange = (to) => {
        // 百度统计
        // @ts-ignore: ts(2304)
        if (typeof _hmt !== 'undefined') {
          // @ts-ignore: ts(2304)
          _hmt.push(['_trackPageview', to])
          // @ts-ignore: ts(2304)
        } else if (typeof window._hmt !== 'undefined') {
          // @ts-ignore: ts(2304)
          window._hmt.push(['_trackPageview', to])
        }
      }
    }
  }
} satisfies Theme
