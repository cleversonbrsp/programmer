# Ala 12  - Condições Aninhadas

# Escreva um programa para aprovar o emprestimo bancario para a compra de uma casa.
# O programa vai perguntar o valor da casa, o salario do comprador e em quantos anos ele vai pagar.
# Calcule o valor da prestação mensal, sabendo que ela não pode exceder 30% do salário ou então o empréstimo será negado.

casa = float(input('Qual o valor da casa? R$ '))
salario = float (input('Qual o seu salário? R$ '))
anos = input('Em quantos anos você pretende pagar? ')

if float(salario) * 0.3 > float(casa) / (int(anos) * 12):
    print('Emprestimo aprovado!')
    print('O valor da casa é de R$ {:.2f}'.format(float(casa)))
    print('O valor do salário é de R$ {:.2f}'.format(float(salario)))
    print('O valor da prestação mensal é de R$ {:.2f}'.format(float(casa) / (int(anos) * 12)))
    print('O valor da prestação mensal não excede 30% do seu salário.')
else:
    print('Emprestimo negado!')
    print('O valor da casa é de R$ {:.2f}'.format(float(casa)))
    print('O valor do salário é de R$ {:.2f}'.format(float(salario)))
    print('O valor da prestação mensal é de R$ {:.2f}'.format(float(casa) / (int(anos) * 12)))
    print('O valor da prestação mensal não excede 30% do seu salário.')


