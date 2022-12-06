def loadDataBase(filename, products):
    for line in open(filename, "r", encoding="utf8").readlines()[1:]:  # Lê o ficheiro por linhas, exceto a primeira
        reading = line.strip().split(";")  # Remove os espaços, e dá split pelos ";"
        products.update({reading[0]: (reading[1], reading[2], float(reading[3]), float(reading[4].strip("%")) / 100)})

    return products


def registerPurchase(products):
    single_purchase = []

    while True:
        user_input = input("Code? ").split()  # Faz split pelos espaços

        if len(user_input) == 0:  # Se a lista tiver length de 0 (nenhum input), dá break
            break

        amount = 1 if len(user_input) == 1 else int(user_input[1])
        # O amount é 1, se o length da lista for 1 (não foi dada uma quantidade específica)
        # O amount é o segundo elemento da lista obtida pelo split

        code = user_input[0]  # O código é o primeiro elemento da lista obtida pelo split

        if code in products:  # Se o código estiver nos produtos:
            name, section, price, tax = products[code]  # Extrai os valores do código
            final_price = round(price * (1 + tax) * amount, 2)  # Calcula o preço final, e arrendonda-o
            print(name, amount, final_price)  # Imprime as informações pedidas
            for i in range(0, amount):
                single_purchase.append(code)  # Dá append do código, consoante a quantidade pedida

    return single_purchase


def bill(products, purchases):
    while True:
        try:
            bill_number = int(input("Numero compra? "))
            break
        except ValueError:  # Se o valor introduzido não for um inteiro, o ciclo repete-se
            continue

    total_bruto = total_iva = total_liquido = 0
    sections = {}

    for code in purchases[bill_number]:  # Iterar pelos códigos dos produtos
        section = products[code][1]  # Extrair a secção de cada código
        if section not in sections:  # Verificar se a secção já existe; Caso não esteja presente:
            sections[section] = []  # Criar uma chave no dicionário das secções
            sections[section].append({code: 1})  # Dar append do código, e da quantidade (1)
        else:  # Caso a secção já esteja presente:
            found = False  # Verificar se o código já está presente ou não
            for index, dict in enumerate(sections[section]):  # Extrair o índice, e o dicionário (código, e quantidade)
                code_in_list = list(dict.items())[0][0]  # O código tem índice 0, no dicionário

                if code == code_in_list:  # Se o código for igual:
                    found = True  # Marcar como encontrado
                    sections[section][index][code_in_list] += 1  # Aumentar a quantidade por 1
                    break

            if not found:
                sections[section].append({code: 1})  # Caso o nome não esteja presente, fazer append do código

    for section in sections:  # Iterar por secções
        print(section)  # Imprimir o nome da secção
        for dict_products in sections[section]:  # Iterar por dicionários (código, quantidade)
            code, quantity = list(dict_products.items())[0]
            name, section, price, tax = products[code]  # Extrair os valores do código
            price = price * quantity  # Calcular o preço baseado na quantidade
            total_bruto += price
            total_iva += price * tax
            total_liquido += price * (1 + tax)
            tax_percentage = int(tax * 100)
            total_price = round(price * (1 + tax), 2)
            print("{:>4} {:<30} ({:>2}%) {:>10}".format(quantity, name, tax_percentage, total_price))

    print(" {:>40} {:>10}\n {:>40} {:>10}\n {:>40} {:>10}".format("Total Bruto:", round(total_bruto, 2), "Total IVA:", round(total_iva, 2), "Total Liquido:", round(total_liquido, 2)))

    return


def main(args):
    products = {'p1': ('Ketchup.', 'Mercearia Salgado', 1.59, 0.23)}

    purchases = {}

    loadDataBase("produtos.txt", products)

    for arg in args:
        loadDataBase(arg, products)

    menu = "(C)ompra (F)atura (S)air ? "

    while True:

        op = input(menu).upper()

        if op == "C":
            purchases[len(purchases) + 1] = registerPurchase(products)

        if op == "F":
            bill(products, purchases)

        if op == "S":
            break

    print("Obrigado!")


import sys

if __name__ == "__main__":
    main(sys.argv[1:])