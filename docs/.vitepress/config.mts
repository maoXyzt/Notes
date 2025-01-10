import { defineConfig } from 'vitepress'
import mathjax3 from 'markdown-it-mathjax3';

import structure from '../structure.json';

const customElements = ['mjx-container'];

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "YANG's Notes",
  description: "My notes collections.",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Table of Contents', link: '/toc' }
    ],
    sidebar: structure,
    socialLinks: [
      { icon: 'github', link: 'https://github.com/maoXyzt/Notes' }
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
      pattern: 'https://github.com/maoXyzt/Notes/blob/master/docs/:path',
      text: 'View this page on GitHub'
    },
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2019-present YANG',
    },
  },
  lastUpdated: true,  // show the last Updated time
  base: '/Notes/',
  srcDir: '.',
  markdown: {
    math: true,
    config: (md) => {
      md.use(mathjax3);
    },
  },
  vue: {
    template: {
      compilerOptions: {
        isCustomElement: (tag) => customElements.includes(tag),
      },
    },
  },
})
