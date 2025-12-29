preco=float(input('Digite o valor do produto: '))
porcentagem = float(input('Digite a porcentagem de descontos: '))
desconto= preco - (preco * porcentagem / 100)
print('O valor do item R${} com o desconto de {}% será de R${}'.format(preco,porcentagem,desconto))