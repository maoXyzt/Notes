import { defineConfig } from 'vitepress'
import mathjax3 from 'markdown-it-mathjax3'

import { themeConfig } from './theme/themeConfig'
import { docsConfig } from './docs'
import { head } from './head'

const customElements = ['mjx-container'];

// https://vitepress.dev/reference/site-config
export default defineConfig({
  /* Docs Config */
  ...docsConfig,
  /* Head Config */
  head,
  /* Theme Config */
  themeConfig,
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
  vite: {
    // ...
  }
})
