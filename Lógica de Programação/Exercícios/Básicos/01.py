###########################################
# Crie uma função que receba 
# dois números e retorne o maior deles.
###########################################

# lógica: receber n1, receber n2. se n1 for maior que n2, exibir n1, senao exibir n2.

n1 = int(input('Digite um numero inteiro: '))
n2 = int(input('Digite mais um numero inteiro para eu comparar: '))

if n1 > n2:
    print('{} é maior que {}'.format(n1,n2))
else:
    print('{} é maior que {}'.format(n2,n1))

