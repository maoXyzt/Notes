# 安装Neovim

> [Windows 10 系统下 Neovim 安装与配置 - jdhao's digital space](https://jdhao.github.io/2018/11/16/neovim_configuration_windows-zh/#fn:1)

## 安装

### 安装 Neovim

根据指示，下载安装包:

> [neovim/INSTALL.md](https://github.com/neovim/neovim/blob/master/INSTALL.md#install-from-download)

为了确保在命令行可以使用 `nvim` 这个命令打开 Neovim，将安装路径添加到`PATH`中。

> [install-from-package](https://github.com/neovim/neovim/wiki/Installing-Neovim#install-from-package)

### 安装 `vim-plug`

> [junegunn/vim-plug](https://github.com/junegunn/vim-plug#neovim)

```bash
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
```

### 安装 `python3-provider` 和 `nodejs-provider`

```bash
pip3 install --user --upgrade neovim
npm install -g neovim
```

安装后自检，执行:

```
:checkhealth
```

## 配置

Neovim 使用了和 Vim 不同的配置文件名称以及配置文件存放位置。
根据 Neovim 官方文档，Neovim 的配置文件应该命名为 `init.vim`，并且应该放在 ~/AppData/Local/nvim 目录下。

具体环境中，打开 Neovim，使用 `:echo stdpath('config')` 可以查看该目录的具体位置。

参考配置文件:

```vim
call plug#begin('~/.config/nvim/plugged')
  " surround
  Plug 'tpope/vim-surround'
  " easymotion
  Plug 'easymotion/vim-easymotion'

  if !exists('g:vscode')
    " * ordinary Neovim *
    " dashboard
    Plug 'glepnir/dashboard-nvim'
    " Shorthand notation; fetches https://github.com/junegunn/vim-easy-align
    Plug 'junegunn/vim-easy-align'
    Plug 'tpope/vim-vinegar'
    " file navigation
    Plug 'preservim/nerdtree', { 'on': 'NERDTreeToggle' }
    Plug 'Xuyuanp/nerdtree-git-plugin'
    Plug 'vim-airline/vim-airline'
    " fuzzy file finder
    Plug 'kien/ctrlp.vim'
    Plug 'atweiden/vim-dragvisuals'
    Plug 'gavocanov/foldsearches.vim'
    " fuzzy search
    Plug 'nvim-lua/plenary.nvim'
    Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
    Plug 'nvim-telescope/telescope.nvim'
    " coc.nvim
    Plug 'neoclide/coc.nvim', {'branch': 'release'}
    " git tool
    Plug 'tpope/vim-fugitive'
    " Visual content can move
    Plug 'atweiden/vim-dragvisuals'
    " Vim global plugin for persistent Visual seletions
    "Plug 'galli-a/persistentvisuals'
    " syntax check/linter
    Plug 'vim-syntastic/syntastic'
    " vim-commentary
    Plug 'scrooloose/nerdcommenter'
    " surround
    Plug 'tpope/vim-surround'
    " easymotion
    Plug 'easymotion/vim-easymotion'
    " emmet
    "Plug 'mattn/emmet-vim'
    Plug 'jiangmiao/auto-pairs'
  endif
call plug#end()

let mapleader = ","

" 文件编码
set fenc=utf-8
set encoding=utf-8

let g:python_host_prog = 0
let g:python3_host_prog = '/usr/bin/python3'
let g:loaded_perl_provider = 0
let g:loaded_ruby_provider = 0

if !exists('g:vscode')
  let g:dashboard_default_executive = 'telescope'
  let g:NERDSpaceDelims = 1

  " 开启语法高亮
  syntax on
  syntax enable

  " 显示行号
  set number
  " set relativenumber
  " 将换行自动缩进设置成4个空格；
  set shiftwidth=4
  " 表示一个tab键相当于4个空格键
  set tabstop=4
  set softtabstop=4
  set expandtab
  " 把当前行的对齐格式应用到下一行
  set autoindent
  set shiftwidth=4            " width for autoindents
  " 隐藏滚动条
  set guioptions-=r
  set guioptions-=L
  set guioptions-=b
  set scrolloff=1
  set sidescrolloff=2
  " 显示匹配的括号
  set showmatch

  " 设置不折行
  set nowrap
  set ignorecase              " case insensitive
  set smartcase
  set hlsearch                " highlight search
  set incsearch               " incremental search
  set wildmode=longest,list   " get bash-like tab completions
  " set cc=120                  " set an 80 column border for good coding style
  set cursorline              " highlight current cursorline
  " set lazyredraw

  " coc.nvim
  let g:coc_global_extensions = [
    \ 'coc-diagnostic',
    \ 'coc-explorer',
    \ 'coc-gitignore',
    \ 'coc-html',
    \ 'coc-json',
    \ 'coc-lists',
    \ 'coc-snippets',
    \ 'coc-syntax',
    \ 'coc-tasks',
    \ 'coc-translator',
    \ 'coc-vimlsp',
    \ 'coc-yaml',
    \ 'coc-yank']
endif

" tab complete
inoremap <expr> <TAB> pumvisible() ? "<C-y>" : "<TAB>"


" Neovide only
if exists("g:neovide")
    " Put anything you want to happen only in Neovide here
    set guifont=FiraCode\ NF,FiraCode\ Nerd\ Font\ Mono,Fira\ Code,Consolas,Courier\ New,monospace:h11
    let g:neovide_transparency = 0.8
    let g:neovide_remember_window_size = v:true
    let g:neovide_cursor_vfx_mode = "pixiedust"
endif
```

## 安装桌面端

推荐使用 Neovide 作为 Neovim 的桌面端，它是一个基于 Rust 编写的 Neovim 桌面端，可以在 Windows、Linux 和 MacOS 上运行。

下载安装包，并安装：

> [Release · neovide/neovide](https://github.com/neovide/neovide/releases)
