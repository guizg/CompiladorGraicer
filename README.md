# CompiladorGraicer
Repositório para o compilador da matéria Lógica da Computação

Diagrama Sintático atual:

![diagrama](https://github.com/guizg/CompiladorGraicer/blob/h9/ds.jpg)

Program = SubDec|FuncDec

SubDec = “sub”, “identifier”, “(“, { | (“identifier”, “as”, Type)}, “)”, “\n”, { | ( Statement, “\n”)}, “end”, “sub”;

FuncDec = “function”, “identifier”, “(“, { | (“identifier”, “as”, Type)}, “)”, “as”, Type, “\n”, { | ( Statement, “\n”)}, “end”, “function”;

RelExpression = Expression, {“=” | ”>” | ”<”}, Expression;

Expression = Term, {(“+” |  “-” | ”or”),Term | ;

Term = Factor, {(“*” | ”/” | ”and”), Factor} | ;

Factor = “number” | {“boolean” | (”identifier”,{| {“(“{(| RelExpression, {| “,”})}}}) | {(“+” | ”-” | ”not”), Factor} | “(“, RelExpression, “)” | ”input”;

Statement = | (“identifier”, “=”, RelExpression) | (“print”, RelExpression) | (“dim”, “identifier”, “as”, Type) | (“if”, RelExpression, “then”, “\n”, {| (Statement, “\n”), {| (“else”, “\n”, {| (Statement, “\n”)}}, “end”, “if”) | (“call”, “identifier”, “(“, {| {RelExpression, {| “,”}});
