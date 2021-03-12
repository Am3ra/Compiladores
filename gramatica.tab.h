/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     IF = 258,
     VAR = 259,
     FLOAT = 260,
     INT = 261,
     ELSE = 262,
     PROGRAM = 263,
     PRINT = 264,
     PLUS = 265,
     MINUS = 266,
     TIMES = 267,
     DIVIDE = 268,
     LPAREN = 269,
     RPAREN = 270,
     SCOLON = 271,
     LBRACKET = 272,
     RBRACKET = 273,
     COMMA = 274,
     COLON = 275,
     ASSIGN = 276,
     NE = 277,
     LT = 278,
     GT = 279,
     CTEF = 280,
     CTEI = 281,
     ID = 282,
     CTESTRING = 283
   };
#endif
/* Tokens.  */
#define IF 258
#define VAR 259
#define FLOAT 260
#define INT 261
#define ELSE 262
#define PROGRAM 263
#define PRINT 264
#define PLUS 265
#define MINUS 266
#define TIMES 267
#define DIVIDE 268
#define LPAREN 269
#define RPAREN 270
#define SCOLON 271
#define LBRACKET 272
#define RBRACKET 273
#define COMMA 274
#define COLON 275
#define ASSIGN 276
#define NE 277
#define LT 278
#define GT 279
#define CTEF 280
#define CTEI 281
#define ID 282
#define CTESTRING 283




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;

