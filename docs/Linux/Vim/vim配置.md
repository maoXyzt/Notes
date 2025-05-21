# Vim 配置

## 1. 配置内容

`~/.vimrc` 文件:

```vim
set nocompatible


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => vim-plug
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" Specify a directory for plugins
" - For Neovim: stdpath('data') . '/plugged'
" - Avoid using standard Vim directory names like 'plugin'
" - Install with `:PlugInstall`
" Initialize plugin system
call plug#begin('~/.vim/plugged')
  Plug 'Yggdroot/indentLine'    "缩进指示线
  Plug 'kien/rainbow_parentheses.vim'
  "+ movements
  Plug 'tpope/vim-surround'
  Plug 'easymotion/vim-easymotion'
  "+ statusline
  Plug 'itchyny/lightline.vim'
  "+ theme: everforest
  Plug 'sainnhe/everforest'
  "+ python
  Plug 'vim-scripts/indentpython.vim'
  "+ toml
  Plug 'cespare/vim-toml', { 'branch': 'main' }
call plug#end()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => General
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let mapleader = ","
let g:mapleader = ","
" Sets how many lines of history VIM has to remember
set history=700
" Enable filetype plugins
filetype plugin on
filetype indent on
" Set to auto read when a file is changed from the outside
set autoread


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => VIM user interface
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Set 3 lines to the cursor - when moving vertically using j/k
set so=3
" Turn on the WiLd menu
set wildmenu
" Ignore compiled files
set wildignore=*.o,*~,*.pyc
" 显示行号
set number

" 隐藏滚动条
set guioptions-=r
set guioptions-=L
set guioptions-=b

" 文件编码/终端编码均设置默认为utf-8，编码中文乱码问题
set fileencoding=utf-8
set fileencodings=ucs-bom,utf-8,gbk,cp936,gb2312,gb18030,big5,euc-jp,euc-kr,latin1
set termencoding=utf-8
" 将工作目录自动切换到当前打开文件目录下
set autochdir

set list
set listchars=eol:↵,trail:~,tab:>-,nbsp:␣

" search configs
set ignorecase smartcase                  " 搜索时忽略大小写
set nowrapscan                            " 禁止在搜索到文件两端时重新搜索
set incsearch                             " 输入搜索内容时就显示搜索结果
set hlsearch                              " 搜索时高亮显示被找到的文本
set showmatch                             " 插入括号时，短暂地跳转到匹配的对应括号
set matchtime=2                           " 短暂跳转到匹配括号的时间

" Don't redraw while executing macros (good performance config)
set lazyredraw

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=
set tm=500


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Text, tab and indent related
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 将换行自动缩进设置成4个空格；
set shiftwidth=4
" 表示一个tab键相当于4个空格键
set tabstop=4
set softtabstop=4
set expandtab
" Be smart when using tabs ;)
set smarttab
" 把当前行的对齐格式应用到下一行
"set autoindent
set smartindent     " 智能自动缩进

" Linebreak on 500 characters
set lbr
set tw=500
"set nowrap          " 设置不折行
"
set ai "Auto indent
set si "Smart indent
set wrap "Wrap lines


""""""""""""""""""""""""""""""
" => Visual mode related
""""""""""""""""""""""""""""""
" Visual mode pressing * or # searches for the current selection
" Super useful! From an idea by Michael Naumann
vnoremap <silent> * :call VisualSelection('f')<CR>
vnoremap <silent> # :call VisualSelection('b')<CR>


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Moving around, tabs, windows and buffers
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Treat long lines as break lines (useful when moving around in them)
map j gj
map k gk

" Map <Space> to / (search) and Ctrl-<Space> to ? (backwards search)
map <space> /
map <c-space> ?

" Disable highlight when <leader><cr> is pressed
map <silent> <leader><cr> :noh<cr>

" Smart way to move between windows
map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

" Close the current buffer
map <leader>bd :Bclose<cr>

" Close all the buffers
map <leader>ba :1,1000 bd!<cr>

" Useful mappings for managing tabs
map <leader>tn :tabnew<cr>
map <leader>to :tabonly<cr>
map <leader>tc :tabclose<cr>
map <leader>tm :tabmove

" Opens a new tab with the current buffer's path
" Super useful when editing files in the same directory
map <leader>te :tabedit <c-r>=expand("%:p:h")<cr>/

" Switch CWD to the directory of the open buffer
map <leader>cd :cd %:p:h<cr>:pwd<cr>

" Specify the behavior when switching between buffers
try
  set switchbuf=useopen,usetab,newtab
  set stal=2
catch
endtry

" Return to last edit position when opening files (You want this!)
autocmd BufReadPost *
  \ if line("'\"") > 0 && line("'\"") <= line("$") |
  \   exe "normal! g`\"" |
  \ endif
" Remember info about open buffers on close
set viminfo^=%


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Colors and Fonts
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" enable syntax highlight
syntax on
syntax enable
" theme config
if has('termguicolors')
  set termguicolors
endif
set t_Co=256
set background=dark
colorscheme everforest
set laststatus=2                        " 显示状态栏(默认值为 1, 无法显示状态栏)
set ruler                               " 打开状态栏标尺 Always show current position
set cursorline                          " 突出显示当前行
let g:lightline = {
  \ 'colorscheme': 'everforest',
  \ }
let g:everforest_background = 'soft'        " The background contrast used in this color scheme. 'hard'|'medium'|'soft'`
let g:everforest_better_performance = 1     " For better performance of everforest theme

" Set cursor shape and color
" 1 -> blinking block           闪烁的方块
" 2 -> solid block              不闪烁的方块
" 3 -> blinking underscore      闪烁的下划线
" 4 -> solid underscore         不闪烁的下划线
" 5 -> blinking vertical bar    闪烁的竖线
" 6 -> solid vertical bar       不闪烁的竖线
if &term =~ "xterm"
  " INSERT mode
  let &t_SI = "\<Esc>[5 q" . "\<Esc>]12;green\x7"
  " REPLACE mode
  let &t_SR = "\<Esc>[4 q" . "\<Esc>]12;white\x7"
  " NORMAL mode
  let &t_EI = "\<Esc>[2 q" . "\<Esc>]12;white\x7"
endif
```

## 2. 配置说明

### 2.1 插件

使用 vim-plug 管理插件，参考: [vim-plug](./vim插件管理%20-%20vim-plug.md)

### 2.2 通用配置

* 关闭 vi 兼容模式 (`set nocompatible`)
* 设置 leader 键为 `,`
* 启用 filetype 插件
* ...

### 2.3 VIM UI

* 显示行号
* 配置默认文件编码为 utf-8
* 配置空白字符的显示 (`set listchars=eol:↵,trail:~,tab:>-,nbsp:␣`)
* 搜索功能的相关配置

### 2.4 文本、标签和缩进相关

* 配置 tab 键缩进为4个空格
* ...

### 2.5 Visual mode 相关

* 用 `*` 和 `#` 搜索当前内容 (下一个/上一个)

### 2.6 移动、标签、窗口和缓冲区相关

* 对于长行时，用 `j` 和 `k` 移动时考虑折行后的移动
* 用 `<space>` 和 `Ctrl-<space>` 开启前向搜索/后向搜索
* 用 `Ctrl-j/k/h/l` 在窗口间移动
* ...
* 配置打开文件时，返回上次编辑的位置
* ...

### 2.7 颜色和字体相关

* 配置主题 (`everforest`)
* 显示状态栏
* 显示状态栏标尺
* 突出显示当前行
* 配置光标样式
* ...

## 3. filetype 插件

使用 filetype 插件，按文件类型适用某些配置。

参考: [VIM 的 FileType Plugins 配置](./vim的filetype%20plugins配置.md)
