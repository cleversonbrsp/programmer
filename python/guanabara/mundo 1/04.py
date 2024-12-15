##############################################
# faça um programa que leia algo pelo teclado
# e mostre na tela o seu tipo primitivo e todas
# as informações possíveis sobre ele.
##############################################

# PS: Todo valor é do tipo str (string) caso nao seja convertido no codigo.
# Aqui estamos trabalhando com métodos e o "a.etc..." é um objeto e todo objeto
# tem caracteristicas e, realiza funcionalidades, pois eles possuiem atributos
# e metodos que no nosso caso, como existem parenteses em cada um deles,
# estamos trabalhando metodos e todo objeto string tem esses metodos "isupper, islower, isalnum...)".

# Minha logica:
# - Adionar uma variável para armazenar um valor que o usuário fornecerá;
# - O script interpreta essa variável e mostra os resultados na tela.

a = input('Digite algo: ')
print('O tipo primitivo desse valor é .', type(a))
print('O valor digitado possui apenas espaços? ', a.isspace())
print('É um numero? ', a.isnumeric())
print('É alfabetico? ', a.isalpha())
print('É alfanumerico? ', a.isalnumc())
print('Esta em maiusculas? ', a.isupper())


