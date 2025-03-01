// https://vitepress.dev/guide/custom-theme
import { h } from 'vue'
import type { Theme, EnhanceAppContext } from 'vitepress'
import { inBrowser, useData, useRoute } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import giscusTalk from 'vitepress-plugin-comment-with-giscus';

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
  },
  setup() {
    // Get frontmatter and route
    const { frontmatter } = useData();
    const route = useRoute();
    // giscus配置
    giscusTalk({
      repo: 'maoXyzt/Notes',
      repoId: 'MDEwOlJlcG9zaXRvcnkxNzY0Njk3NTM=',
      category: 'Announcements',
      categoryId: 'DIC_kwDOCoS2-c4CndeH',
      mapping: 'pathname',
      inputPosition: 'bottom',
      lang: 'zh-CN',
      },
      {
        frontmatter, route
      },
      //默认值为true，表示已启用，此参数可以忽略；
      //如果为false，则表示未启用
      //您可以使用“comment:true”序言在页面上单独启用它
      true
    );
  }
} satisfies Theme
