" Vim syntax file
" Language:	Content Publication Language
" Maintainer:	Roberto Miura Honji <miurahonji@gmail.com>
" Last Change:	2009 Oct 29
" Quit when a (custom) syntax file was already loaded
if exists("b:current_syntax")
  finish
endif

" Quit when a (custom) syntax file was already loaded
syn keyword	cplStatement	begin end content newspaper title date abstract text source image author structure format item

syn match	cplComment	display "//[^$]*$"
syn match	cplNoComment display "http:\/\/[^$\/]*"

hi def link cplStatement	Statement
hi def link cplNoComment	ModeMsg
hi def link cplComment		Comment

let b:current_syntax = "cpl"
