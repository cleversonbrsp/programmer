def calcular_valor_hora(salario_mensal, dias_trabalhados, horas_diarias):
    # Calcula o total de horas trabalhadas no mês
    horas_totais = dias_trabalhados * horas_diarias

    # Calcula o valor da hora
    valor_hora = salario_mensal / horas_totais

    return valor_hora


def main():
    # Solicita ao usuário o salário mensal, dias trabalhados e horas diárias
    salario_mensal = float(input("Digite o salário mensal: R$ "))
    dias_trabalhados = int(input("Digite o número de dias trabalhados no mês: "))
    horas_diarias = int(input("Digite o número de horas diárias trabalhadas: "))

    # Calcula o valor da hora
    valor_hora = calcular_valor_hora(salario_mensal, dias_trabalhados, horas_diarias)

    # Formata o valor da hora para o modelo desejado
    valor_formatado = "R$ {:,.2f}".format(valor_hora).replace(',', ';').replace('.', ',').replace(';', '.')

    # Exibe o resultado
    print("O valor da hora de trabalho é:", valor_formatado)


if __name__ == "__main__":
    main()
