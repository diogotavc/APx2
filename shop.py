def loadDataBase(filename, products):
    for line in open(filename, "r", encoding="utf8").readlines()[1:]:  # Lê o ficheiro por linhas, exceto a primeira
        reading = line.strip().split(";")  # Remove os espaços, e dá split pelos ";"
        products.update({reading[0]: (reading[1], reading[2], float(reading[3]), float(reading[4].strip("%")) / 100)})

    return products


def registerPurchase(products):
    single_purchase = {}

    while True:
        user_input = input("Code? ").split()  # Faz split pelos espaços

        if len(user_input) == 0:  # Se a lista tiver length de 0 (nenhum input), dá break
            break

        amount = 1 if len(user_input) == 1 else int(user_input[1])
        # O amount é 1, se o length da lista for 1 (não foi dada uma quantidade específica)
        # caso tenha sido dada uma quantidade, o amount é o segundo elemento da lista obtida pelo split

        code = user_input[0]  # O código é o primeiro elemento da lista obtida pelo split

        if code in products:  # Se o código estiver nos produtos:
            name, section, price, tax = products[code]  # Extrai os valores do código
            final_price = round(price * (1 + tax) * amount, 2)  # Calcula o preço final, e arrendonda-o
            print(name, amount, final_price)  # Imprime as informações pedidas
            single_purchase[code] = single_purchase.get(code, 0) + amount  # Adiciona (caso não exista) o código
            # e soma a quantidade (caso o código não esteja presente no dicionário, a quantidade é zero)

    return single_purchase


def bill(products, purchases):
    while True:
        try:
            bill_number = int(input("Numero compra? "))
            bill = purchases[bill_number]
            break
        except ValueError:  # Se o valor introduzido não for um inteiro, o ciclo repete-se
            continue

    total_bruto = total_iva = total_liquido = 0
    sections = {}

    for code, quantity in bill.items():  # Iterar pelos códigos e quantidades dos produtos
        section = products[code][1]  # Extrair a secção de cada código
        if section not in sections:  # Verificar se a secção já existe; Caso não esteja presente:
            sections[section] = []  # Criar uma chave no dicionário das secções
        sections[section].append({code: quantity})  # Dar append do código: quantidade

    for section in sections:  # Iterar por secções
        print(section)  # Imprimir o nome da secção
        for dict_products in sections[section]:  # Iterar pelos códigos, e quantidades
            code, quantity = list(dict_products.items())[0]  # Extrair os valores do código
            name, section, price, tax = products[code]
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