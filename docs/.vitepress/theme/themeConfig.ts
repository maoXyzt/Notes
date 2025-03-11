import type { DefaultTheme as DefaultThemeType } from 'vitepress'

import constants from '../constants'
import structure from '../../structure.json'

// https://vitepress.dev/reference/default-theme-config
export const themeConfig: DefaultThemeType.Config = {
  // https://vitepress.dev/reference/default-theme-config
  logo: `${constants.base_url}icon.png`,
  siteTitle: "YANG's Notes",
  nav: [
    { text: '主页', link: '/' },
    { text: '目录', link: '/toc' }
  ],
  sidebar: structure,
  socialLinks: [
    { icon: 'github', link: constants.github },
  ],
  search: {
    provider: 'local',
    options: {
      // _render(src, env, md) {
      //   const html = md.render(src, env)
      //   if (env.frontmatter?.title)
      //     return md.render(`# ${env.frontmatter.title}`) + html
      //   return html
      // },
      translations: {
        button: {
          buttonText: '搜索',
          buttonAriaLabel: '搜索文档',
        },
        modal: {
          noResultsText: '无法找到相关结果',
          resetButtonTitle: '清除查询结果',
          footer: {
            selectText: '选择',
            navigateText: '切换',
          },
        },
      },
    },
  },
  editLink: {
    pattern: `${constants.github}/blob/master/docs/:path`,
    text: 'View this page on GitHub'
  },
  footer: {
    message: 'Released under the MIT License.',
    copyright: 'Copyright © 2019-present YANG',
  },
}
