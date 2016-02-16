set nowrap
set nocompatible
filetype on
filetype plugin on
filetype plugin indent on
syntax enable
set autoindent
set tabstop=4
set shiftwidth=4
set expandtab
set smarttab
set number

inoremap jj <Esc>
nnoremap JJJJ <Nop>
set incsearch
set hlsearch
nnoremap ; :

autocmd FileType tex setlocal spell spellang=en_us

" Remove trailing whitespace
autocmd BufRead,BufWrite if ! &bin | silent! %s/\s\+$//ge | endif
