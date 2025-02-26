import type { DefaultTheme as DefaultThemeType } from 'vitepress'

import constants from '../constants'
import structure from '../../structure.json'

// https://vitepress.dev/reference/default-theme-config
export const themeConfig: DefaultThemeType.Config = {
  // https://vitepress.dev/reference/default-theme-config
  logo: `${constants.base_url}icon.png`,
  siteTitle: 'AnimoXtend',
  nav: [
    { text: 'Home', link: '/' },
    { text: 'Table of Contents', link: '/toc' }
  ],
  sidebar: structure,
  socialLinks: [
    { icon: 'github', link: constants.github },
  ],
  search: {
    provider: 'local',
    options: {
      _render(src, env, md) {
        const html = md.render(src, env)
        if (env.frontmatter?.title)
          return md.render(`# ${env.frontmatter.title}`) + html
        return html
      }
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
