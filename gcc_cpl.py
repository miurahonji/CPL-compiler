#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re, sys

#################################### STARTING LEX ####################################
reserved = {
	'begin': 'BEGIN',
	'end': 'END',
	'content': 'CONTENT',
	'newspaper': 'NEWSPAPER',
	'title': 'TITLE',
	'date': 'DATE',
	'abstract': 'ABSTRACT',
	'text': 'TEXT',
	'source': 'SOURCE',
	'image': 'IMAGE',
	'author': 'AUTHOR',
	'structure': 'STRUCTURE',
	'format': 'FORMAT',
	'item': 'ITEM',
}

special = {
	'jpg': 'PHOTO_EXT',
	'png': 'PHOTO_EXT',
	'col': 'COL',
	'border': 'BORDER',
}

tokens = reserved.values()
tokens.extend(set(special.values()))
tokens.extend((
	'LPAREN','RPAREN',
	'COLON','URL',
	'LBRACK', 'RBRACK',
	'LBRACE', 'RBRACE',
	'PIPE','EQUAL','NAME','WORD',
	'POINT','INDENT_COLON',
	'SESSION_EQUAL',
	'BAR','NUMBER','COMMA','QUOTE',
	'DQUOTE','DASH',
	))

# Tokens
# Blocks marks
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LBRACK  = r'\['
t_RBRACK  = r'\]'
t_BAR = r'/'

t_COLON = r':'
t_POINT = r'\.'
t_PIPE = r'\|'
t_EQUAL = r'='
t_COMMA = r','
t_QUOTE = r"'"
t_DQUOTE = r'"|”'
t_DASH = r'-'

t_URL = r'http://[^\t \n]*'
t_ignore_COMMENT = r'//.*'

# Ignored characters
t_ignore = " \t"

def t_NUMBER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print "Integer value too large", t.value
		t.value = 0
	return t

def t_newline(t):
	r'\n+(?!\s*[:=])'
	t.lexer.lineno += t.value.count("\n")

def t_INDENT_COLON(t):
	r'\n\s*:'
	t.lexer.lineno += t.value.count('\n')
	t.value = ':'
	t.lineno = t.lexer.lineno
	return t

def t_SESSION_EQUAL(t):
	r'\n\s*='
	t.lexer.lineno += t.value.count('\n')
	t.value = '='
	t.lineno = t.lexer.lineno
	return t

def t_NAME(t):
	r'(?!http://[^\t \n]*)\w+(?=\s*[\{\.])'
	p = re.compile(r'[a-zA-Z][a-zA-Z0-9_]*', re.U)
	test = p.split(t.value)
	if len(test) == 2 and test[0] == '' and test[1] == '':
		t.type = special.get(t.value, 'NAME')
		t.type = reserved.get(t.value, t.type)
	else:
		t.type = special.get(t.value, 'WORD')
		t.type = reserved.get(t.value, t.type)
	return t

def t_WORD(t):
	r'(?!http://[^\t \n]*)\w+(?!\s*[\{\.])'
	t.type = special.get(t.value, 'WORD')
	t.type = reserved.get(t.value, t.type)
	return t

def t_error(t):
	print "Illegal character '%s' on" % t.value[0].encode('utf-8'), t
	t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex(reflags=re.U)

#################################### FINISHED LEX ####################################


################################### STARTING PARSE ###################################
def p_statement_nBegin(t):
	'''statement : BEGIN nContent nStructure END'''
	t[0] = '''<HTML>
	<HEAD><meta http-equiv="content-type" content="text/html; charset=utf-8" />
	 <TITLE> Untitled </TITLE>
	 <link rel="stylesheet" type="text/css" href="style/style.css" media="screen" />
	 </HEAD>''' + t[2] + '''</HTML>'''
	#TODO: Complete this function

#### CONTENT DEFINES ####
def p_nContent(t):
	'''nContent : CONTENT LBRACE nNewspaper blocks RBRACE'''
	t[0] = '<BODY>' + t[3] + '</BODY>'
	#TODO: Complete this function

def p_nNewspaper(t):
	'''nNewspaper : NEWSPAPER LBRACE nNewspaper_block RBRACE'''
	t[0] = t[3]
	#TODO: Complete this function

def p_nNewspaper_block(t):
	'''nNewspaper_block : nn_block nTitle nn_block'''
	t[0] = '<h1>' '</h1>'
	#TODO: Complete this function

def p_nn_block(t):
	'''nn_block : nDate
				| empty'''
	if (t[1]):
		t[0] = '<h3>' + t[1] + '</h3>'
		
	#TODO: Complete this function

def p_blocks(t):
	'''blocks : blocks block
				| block
				| empty'''
	#TODO: Complete this function

def p_block(t):
	'''block : NAME LBRACE cblock RBRACE'''
	#TODO: Complete this function
	#TODO: Verify if cblock have nTitle and nAbstract

def p_cblock(t):
	'''cblock : cblock ccblock 
				| ccblock'''
	#TODO: Complete this function

def p_ccblock(t):
	'''ccblock :  nTitle
				| nDate
				| nAbstract
				| nImage
				| nSource
				| nAuthor
				| nText
				'''
	#TODO: Complete this function

def p_nTitle(t):
	'''nTitle : TITLE COLON noWikiText'''
	#TODO: Complete this function

def p_nDate(t):
	'''nDate : DATE COLON noWikiText'''
	t[0] = t[3]
	#TODO: Complete this function

def p_nAbstract(t):
	'''nAbstract : ABSTRACT COLON noWikiText'''
	#TODO: Complete this function

def p_nImage(t):
	'''nImage : IMAGE COLON POINT BAR noWikiText POINT PHOTO_EXT'''
	#TODO: Complete this function

def p_nSource(t):
	'''nSource : SOURCE COLON noWikiText
				| SOURCE COLON URL'''
	#TODO: Complete this function

def p_nAuthor(t):
	'''nAuthor : AUTHOR COLON noWikiText'''
	#TODO: Complete this function

def p_nText(t):
	'''nText : TEXT COLON wikiText'''
	#TODO: Complete this function

def p_wText(t):
	'''wText : NAME
				| WORD
				| POINT
				| COLON
				| LPAREN
				| RPAREN
				| BAR
				| NUMBER
				| COMMA
				| QUOTE
				| DQUOTE
				| DASH
				| link
				| session
				| indent
				'''
	#TODO: Complete this function

def p_wikiText(t):
	'''wikiText : wikiText wText
				| wText'''
	#TODO: Complete this function

def p_noWText(t):
	'''noWText : NAME
				| WORD
				| POINT
				| COLON
				| LPAREN
				| RPAREN
				| BAR
				| NUMBER
				| COMMA
				| QUOTE
				| DQUOTE
				| DASH
				'''
	#TODO: Complete this function

def p_noWikiText(t):
	'''noWikiText : noWikiText noWText
				| noWText'''
	#TODO: Complete this function

def p_link(t):
	'''link : LBRACK URL PIPE noWikiText RBRACK'''
	t[0] = '<a href="' + t[2] +  '"></a>'
	#TODO: Complete this function

def p_session(t):
	'''session : SESSION_EQUAL nSession EQUAL'''
	#TODO: Complete this function

def p_nSession(t):
	'''nSession : EQUAL nSession EQUAL
				| wikiText'''
	#TODO: Complete this function

def p_indent(t):
	'''indent : INDENT_COLON nIndent'''
	#TODO: Complete this function

def p_nIndent(t):
	'''nIndent : COLON nIndent
				| wikiText'''
	#TODO: Complete this function

#### STRUCTURE DEFINE ####
def p_nStructure(t):
	'''nStructure : STRUCTURE LBRACE nFormat nItems RBRACE'''
	#TODO: Complete this function

def p_nFormat(t):
	'''nFormat : FORMAT LBRACE nCol nBorder RBRACE'''
	#TODO: Complete this function

def p_nCol(t):
	'''nCol : COL COLON NUMBER'''
	#TODO: Complete this function

def p_nBorder(t):
	'''nBorder : BORDER COLON NUMBER'''
	#TODO: Complete this function

def p_nItems(t):
	'''nItems : nItems nItem
				| nItem '''
	#TODO: Complete this function

def p_nItem(t):
	'''nItem : ITEM LBRACK range RBRACK LBRACE define_item RBRACE'''
	#TODO: Complete this function

def p_range(t):
	'''range : NUMBER COLON NUMBER
				| NUMBER'''
	#TODO: Complete this function

def p_define_item(t):
	'''define_item : define_item ditem
					| ditem'''
	#TODO: Complete this function

def p_ditem(t):
	'''ditem : NAME POINT TITLE
				| NAME POINT ABSTRACT
				| NAME POINT IMAGE
				| NAME POINT SOURCE
				| NAME POINT DATE
				| NAME POINT AUTHOR
				| NAME POINT TEXT'''
	#TODO: Complete this function

def p_error(t):
	print "Syntax error at '%s'" % t.value

def p_empty(t):
	'''empty :'''
	pass


import ply.yacc as yacc
if __name__ == '__main__':
	# Parsing options
	debug = False
	f = 'exemplo.cpl'
	while len(sys.argv) > 1:
		op = sys.argv.pop(1).strip()
		if op == '--debug':
			debug = True
		elif op == '-f':
			if len(sys.argv) < 2:
				print 'Usage %s -f filename' % sys.argv[0]
				sys.exit(1)
			f = sys.argv.pop(1)

	# To debug lexic
	if debug:
		lexer = lex.lex(reflags=re.U)
		lexer.input(open(f).read().decode('utf-8'))
		while True:
			tok = lexer.token()
			if not tok: break
			print tok

	# Execute parse
	yacc.yacc()
	result = yacc.parse(open(f).read().decode('utf-8'))
	print result
################################### FINISHED PARSE ###################################
