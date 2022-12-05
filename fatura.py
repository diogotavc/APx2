def fatura(produtos, compra):
    """Imprime a fatura de uma dada compra."""
    while True:
        try:
            # para o user, a lista de compras começa no 1, mas para o código começa no 0
            n = int(input("Numero compra? ")) - 1
            fatura = compra[n]
            break
        # após a seleção se for introuzido um caracter errado ou um número inválido(que faça "estourar" a lista), continua
        except (ValueError, IndexError):
            continue
    # a variável code é uma variável 'cobaia', é usada para loops, tendo significados diferentes
    seccoes = []

    # vai por numa lista 'seccoes' as secções usadas
    for code in fatura.keys():
        seccoes.append(produtos[code][1])
    # remove secções duplicadas
    seccoes = sorted(list(set(seccoes)))
    liquido = 0
    bruto = 0
    totaliva = 0
    dictsec = {}
    # para cada secção usada nas compras
    for seccao in seccoes:
        # para cada linha do dicionário produtos
        for code in produtos:
            # se a secção da linha selecionada for igual à secção atual das compras
            # E se o código atual está na lista de compras, adiciona um dicionário que tem como key a secção e como
            # values os códigos que existem nas compras, na respetiva secção
            if produtos[code][1] == seccao and code in fatura.keys():
                dictsec.setdefault(seccao, []).append(code)     # setdefault cria uma key se ela não existir...

    # para cada secção, dá print à secção
    for code in dictsec.keys():
        print(code)
        # para a lista de códigos da secção atual
        for var in dictsec.values():
            # para cada código da lista anteroirmente referida
            for exp in var:
                # se o código está na lista da secção atual
                if exp in dictsec[code]:
                    iva = int(produtos[exp][3] * 100)       # buscar o IVA do produto atual e representá-lo como pedido
                    preco = fatura[exp] * produtos[exp][2] * (1 + iva / 100) #  calcular o preço líquido do item
                    liquido += preco    # adicionar o preço líquido do ‘item’ a uma variável para obter o preço total
                    totaliva += fatura[exp] * produtos[exp][2] * iva / 100  # adicionar o preço do IVA do item a uma variável que representa o valor do IVA total
                    bruto += fatura[exp] * produtos[exp][2]     #adicionar o peso bruto do item a uma variável que representa o preço bruto total
                    # um print com a quantidade, nome, IVA e o preco do ‘item’,
                    # respeitando a quantidade e arrendondado para 2 casas decimais, respetivamente e formatado
                    print("{:>4} {:<31} ({:>2}%) {:>11}".format(fatura[exp], produtos[exp][0], iva, round(preco, 2)))
    # print que mostra o total bruto, o total do IVA e total líquido, arredondado para 2 casas decimais e formatado
    print(" {:>41} {:>11}\n {:>41} {:>11}\n {:>41} {:>11}".format("Total bruto:", round(bruto, 2), "Total IVA:", round(totaliva, 2), "Total Liquido:", round(liquido, 2)))