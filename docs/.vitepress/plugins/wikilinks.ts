import fs from 'node:fs'
import path from 'node:path'

const MD_EXT = '.md'
const SKIP_DIRS = new Set(['.vitepress', 'node_modules'])
const EXCLUDED_SLUGS = new Set(['index'])

// NOTE: 索引在模块加载时构建一次。新增 / 重命名 md 文件需要重启 vitepress dev server。
export function buildWikilinkIndex(srcDir: string): Map<string, string> {
  const bySlug = new Map<string, string>()

  const walk = (dir: string) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name.startsWith('.') && entry.name !== '.') {
        if (entry.isDirectory()) continue
      }
      if (entry.isDirectory()) {
        if (SKIP_DIRS.has(entry.name)) continue
        walk(path.join(dir, entry.name))
        continue
      }
      if (!entry.isFile() || !entry.name.endsWith(MD_EXT)) continue

      const slug = entry.name.slice(0, -MD_EXT.length)
      if (EXCLUDED_SLUGS.has(slug)) continue

      const rel = path.relative(srcDir, path.join(dir, entry.name))
      const existing = bySlug.get(slug)
      if (existing && existing !== rel) {
        throw new Error(
          `[wikilinks] Ambiguous basename "${slug}": both "${existing}" and "${rel}" exist. Rename one.`,
        )
      }
      bySlug.set(slug, rel)
    }
  }

  walk(srcDir)
  return bySlug
}

function toHref(relPath: string): string {
  const withoutExt = relPath.slice(0, -MD_EXT.length)
  return '/' + withoutExt.split(path.sep).join('/')
}

export function wikilinks(index: Map<string, string>) {
  return (md: any) => {
    md.inline.ruler.before('link', 'wikilink', (state: any, silent: boolean) => {
      const src: string = state.src
      const start: number = state.pos

      if (src.charCodeAt(start) !== 0x5b /* [ */) return false
      if (src.charCodeAt(start + 1) !== 0x5b) return false

      const end = src.indexOf(']]', start + 2)
      if (end === -1) return false

      const inner = src.slice(start + 2, end)
      if (inner.includes('[[') || inner.includes(']]')) return false

      const pipeIdx = inner.indexOf('|')
      const rawTarget = pipeIdx === -1 ? inner : inner.slice(0, pipeIdx)
      const rawAlias = pipeIdx === -1 ? '' : inner.slice(pipeIdx + 1)
      const target = rawTarget.trim()
      const alias = rawAlias.trim()

      const file = state.env?.relativePath || state.env?.path || '<unknown>'

      if (!target) {
        throw new Error(`[wikilinks] Empty wikilink [[]] in ${file}`)
      }

      const rel = index.get(target)
      if (!rel) {
        throw new Error(`[wikilinks] Unresolved wikilink [[${target}]] in ${file}`)
      }

      if (silent) {
        state.pos = end + 2
        return true
      }

      const href = toHref(rel)
      const display = alias || target

      const open = state.push('link_open', 'a', 1)
      open.attrs = [
        ['href', href],
        ['class', 'wikilink'],
      ]

      const text = state.push('text', '', 0)
      text.content = display

      state.push('link_close', 'a', -1)

      state.pos = end + 2
      return true
    })
  }
}
