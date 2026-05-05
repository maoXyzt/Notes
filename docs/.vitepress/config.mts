import path from 'node:path'
import { defineConfig } from 'vitepress'
import mathjax3 from 'markdown-it-mathjax3'

import { themeConfig } from './theme/themeConfig'
import { docsConfig } from './docs'
import { head } from './head'

const mdExtension = '.md'
const H1_INJECT_EXCLUDES = new Set(['index', 'atlas', 'toc'])

function fileNameToTitle(relativePath: string): string {
  const baseName = path.basename(relativePath, mdExtension)
  return decodeURIComponent(baseName)
}

function injectFilenameH1(md: any) {
  md.core.ruler.before('normalize', 'inject_filename_h1', (state: any) => {
    const relPath: string | undefined = state.env?.relativePath || state.env?.path
    if (!relPath) return

    const filename = path.basename(relPath, path.extname(relPath))
    if (H1_INJECT_EXCLUDES.has(filename)) return

    const src: string = state.src
    let injectAt = 0

    if (src.startsWith('---\n') || src.startsWith('---\r\n')) {
      const fmEnd = src.slice(4).match(/\r?\n---(\r?\n|$)/)
      if (fmEnd && typeof fmEnd.index === 'number') {
        injectAt = 4 + fmEnd.index + fmEnd[0].length
      }
    }

    const rest = src.slice(injectAt).replace(/^\s*\n/, '')
    if (/^#\s+/.test(rest)) return

    state.src = src.slice(0, injectAt) + `# ${filename}\n\n` + src.slice(injectAt)
  })
}

// Ref: https://blog.csdn.net/weixin_43837483/article/details/132517579
const customElements = [
  'mjx-container',
  'mjx-assistive-mml',
  'math',
  'maction',
  'maligngroup',
  'malignmark',
  'menclose',
  'merror',
  'mfenced',
  'mfrac',
  'mi',
  'mlongdiv',
  'mmultiscripts',
  'mn',
  'mo',
  'mover',
  'mpadded',
  'mphantom',
  'mroot',
  'mrow',
  'ms',
  'mscarries',
  'mscarry',
  'mscarries',
  'msgroup',
  'mstack',
  'mlongdiv',
  'msline',
  'mstack',
  'mspace',
  'msqrt',
  'msrow',
  'mstack',
  'mstack',
  'mstyle',
  'msub',
  'msup',
  'msubsup',
  'mtable',
  'mtd',
  'mtext',
  'mtr',
  'munder',
  'munderover',
  'semantics',
  'math',
  'mi',
  'mn',
  'mo',
  'ms',
  'mspace',
  'mtext',
  'menclose',
  'merror',
  'mfenced',
  'mfrac',
  'mpadded',
  'mphantom',
  'mroot',
  'mrow',
  'msqrt',
  'mstyle',
  'mmultiscripts',
  'mover',
  'mprescripts',
  'msub',
  'msubsup',
  'msup',
  'munder',
  'munderover',
  'none',
  'maligngroup',
  'malignmark',
  'mtable',
  'mtd',
  'mtr',
  'mlongdiv',
  'mscarries',
  'mscarry',
  'msgroup',
  'msline',
  'msrow',
  'mstack',
  'maction',
  'semantics',
  'annotation',
  'annotation-xml',
];

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
      md.use(injectFilenameH1);
    },
  },
  transformPageData: (pageData) => {
    if (pageData.title?.trim()) {
      return
    }

    pageData.title = fileNameToTitle(pageData.relativePath)
  },
  vue: {
    template: {
      compilerOptions: {
        isCustomElement: (tag) => customElements.includes(tag),
      },
    },
  },
  vite: {
    server: {
      strictPort: false,
    }
  }
})
