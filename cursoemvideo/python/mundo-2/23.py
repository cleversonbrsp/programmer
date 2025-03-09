num = int(input('Digite um numero: '))
u = num // 1 % 10
d = num // 10 % 10
c = num // 100 % 10
m = num // 1000 % 10
print('A unidade do numero digitado é {}'.format(u))
print('A dezena do numero digitado é {}'.format(d))
print('A centena do numero digitado é {}'.format(c))
print('A milhar do numero digitado é {}'.format(m))

#resolvido de forma matemática.
#o numero digitado é dividido e tiro o modulo por 10 entregando o resto do valor.