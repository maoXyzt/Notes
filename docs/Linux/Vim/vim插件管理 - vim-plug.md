# vim 插件管理: vim-plug

## 1 - vim-plug

### 1.1 安装 vim-plug

自动安装：在 `~/.vimrc` 中添加以下内容（在 `plug#begin()` 之前）

```bash
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif
```

Note that `--sync` flag is used to block the execution until the installer finishes.

### 1.2 添加插件

Example:

```bash
" Specify a directory for plugins
" - For Neovim: stdpath('data') . '/plugged'
" - Avoid using standard Vim directory names like 'plugin'
call plug#begin('~/.vim/plugged')

" Make sure you use single quotes

" Shorthand notation; fetches https://github.com/junegunn/vim-easy-align
Plug 'junegunn/vim-easy-align'

" Any valid git URL is allowed
Plug 'https://github.com/junegunn/vim-github-dashboard.git'

" Multiple Plug commands can be written in a single line using | separators
Plug 'SirVer/ultisnips' | Plug 'honza/vim-snippets'

" On-demand loading
Plug 'scrooloose/nerdtree', { 'on':  'NERDTreeToggle' }
Plug 'tpope/vim-fireplace', { 'for': 'clojure' }

" Using a non-default branch
Plug 'rdnetto/YCM-Generator', { 'branch': 'stable' }

" Using a tagged release; wildcard allowed (requires git 1.9.2 or above)
Plug 'fatih/vim-go', { 'tag': '*' }

" Plugin options
Plug 'nsf/gocode', { 'tag': 'v.20150303', 'rtp': 'vim' }

" Plugin outside ~/.vim/plugged with post-update hook
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }

" Unmanaged plugin (manually installed and updated)
Plug '~/my-prototype-plugin'

" Initialize plugin system
call plug#end()
```

### 1.3 安装插件

进入 vim，使用如下命令:

* `:PlugInstall`: Install plugins
* `:PlugUpdate`: Update plugins
* `:PlugClean[!]`: Remove unlisted plugins (bang version will clean without prompt)
* `:PlugUpgrade`: Upgrade vim-plug itself

## 2 - 推荐插件

```bash
"主题"
Plug 'altercation/vim-colors-solarized'
"注释与反注释"
Plug 'tpope/vim-commentary'
Plug 'tpope/vim-surround'
Plug 'scrooloose/nerdtree'
Plug 'jistr/vim-nerdtree-tabs'
Plug 'kien/rainbow_parentheses.vim'
Plug 'easymotion/vim-easymotion'  "快速跳转"
"状态栏"
Plug 'vim-airline/vim-airline'
Plug 'Yggdroot/indentLine'    "缩进指示线"
Plug 'davidhalter/jedi-vim'   "python自动补全"
```

## 3 - 其他 vim 配置

```bash
"关闭vi兼容
set nocompatible

"map <leader> key
let mapleader=","

"显示行号
set number
"将换行自动缩进设置成4个空格
set shiftwidth=4
"表示一个tab键相当于4个空格键
set tabstop=4
set softtabstop=4
set expandtab
set hlsearch
"把当前行的对齐格式应用到下一行
set autoindent
" 隐藏滚动条"
set guioptions-=r
set guioptions-=L
set guioptions-=b
"开启语法高亮"
syntax on
syntax enable
"solarized主题设置在终端下的设置"
set background=dark
colorscheme solarized
"设置不折行"
set nowrap
"显示匹配的括号"
set showmatch
"文件编码"
set fenc=utf-8
set encoding=utf-8
```
