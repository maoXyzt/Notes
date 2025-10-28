import type { DefaultTheme as DefaultThemeType } from 'vitepress'

import constants from '../constants'
import structure from '../../structure.json'

// https://vitepress.dev/reference/default-theme-config
export const themeConfig: DefaultThemeType.Config = {
  // https://vitepress.dev/reference/default-theme-config
  logo: `${constants.base_url}icon.png`,
  siteTitle: "YANG's Notes",
  nav: [
    { text: '🏠 主页', link: '/' },
    { text: '📚 目录', link: '/toc' },
    // { text: '📝 最新', link: '/toc#最新更新' },
    // { text: '🔍 搜索', link: '/toc#搜索' }
  ],
  sidebar: structure,
  socialLinks: [
    { icon: 'github', link: constants.github },
    // { icon: 'twitter', link: 'https://twitter.com/your_twitter' },
    // { icon: 'linkedin', link: 'https://linkedin.com/in/your_profile' }
  ],
  search: {
    provider: 'local',
    options: {
      _render(src, env, md) {
        const html = md.render(src, env)
        if (env.frontmatter?.title)
          return md.render(`# ${env.frontmatter.title}`) + html
        return html
      },
      translations: {
        button: {
          buttonText: '🔍 搜索',
          buttonAriaLabel: '搜索文档',
        },
        modal: {
          noResultsText: '😔 无法找到相关结果',
          resetButtonTitle: '清除查询结果',
          footer: {
            selectText: '选择',
            navigateText: '切换',
            closeText: '关闭',
          },
        },
      },
    },
  },
  editLink: {
    pattern: `${constants.github}/blob/master/docs/:path`,
    text: '✏️ 在 GitHub 上编辑此页'
  },
  lastUpdated: {
    text: '📅 最后更新',
    formatOptions: {
      dateStyle: 'short',
      timeStyle: 'medium'
    }
  },
  docFooter: {
    prev: '⬅️ 上一页',
    next: '➡️ 下一页'
  },
  outline: {
    level: [2, 3],
    label: '📋 页面大纲'
  },
  footer: {
    message: 'Released under the MIT License.',
    copyright: 'Copyright © 2019-present YANG',
  },
  // 添加更多自定义配置
  outlineTitle: '页面导航',
  returnToTopLabel: '返回顶部',
  sidebarMenuLabel: '菜单',
  darkModeSwitchLabel: '主题',
  lightModeSwitchTitle: '切换到浅色模式',
  darkModeSwitchTitle: '切换到深色模式',
}
