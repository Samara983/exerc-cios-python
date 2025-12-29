alt=float(input('Digite a altura da sua parede:'))
larg=float(input('Largura da sua parede:'))
área=alt*larg
tinta = área/2
print('Sua parede tem a dimensão de {}x{} e sua área é {}'.format(alt,larg,área))
print('para pintar sua parede voce precisará de {}l de tinta'.format(tinta))