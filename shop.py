def loadDataBase(filename, products):
    for line in open(filename, "r", encoding="utf8").readlines()[1:]:
        reading = line.strip().split(";")
        products.update({reading[0]: (reading[1], reading[2], float(reading[3]), float(reading[4].strip("%")) / 100)})

    return products


def registerPurchase(products):
    code = None
    single_purchase = []

    while True:
        user_input = input("Code? ").split()

        if len(user_input) == 0:
            break

        amount = 1 if len(user_input) == 1 else int(user_input[1])

        code = user_input[0]

        if code in products:
            name, section, price, tax = products[code]
            final_price = round(price * (1 + tax) * amount, 2)
            print(name, amount, final_price)
            for i in range(0, amount):
                single_purchase.append(code)

    return single_purchase


def bill(products, purchases):
    while True:  # Verificação
        try:
            bill_number = int(input("Numero compra? "))
            break
        except (ValueError, IndexError):
            continue

    total_bruto = total_iva = total_liquido = 0
    sections = []
    amount = {}

    for code in purchases[bill_number]:
        name, section, price, tax = products[code]
        total_bruto += price
        total_iva += price * tax
        total_liquido += price * (1 + tax)

        def printItem(amount):
            for key in amount:
                name, section, price, tax = products[key]
                tax_percentage = int(tax * 100)
                total_price = round(price * (1 + tax) * amount[key], 2)
                print("{:>4} {:<30} ({:>2}%) {:>10}".format(amount[key], name, tax_percentage, total_price))
            return

        if len(sections) == 0:
            sections.append(section)
            print(section)

        elif section not in sections:
            sections.append(section)
            printItem(amount)
            amount = {}
            print(section)

        amount.update({code: purchases[bill_number].count(code)})

    printItem(amount)

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
