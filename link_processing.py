import csv

def collect_information(func):
    def wrapper(*args, **kwargs):
        information = func(*args, **kwargs)
        products_list.append(information)
        return products_list
    return wrapper


@collect_information
def count_sale(product: list):
    sale = float(product[2]) * float(product[-1]) // 100
    new_price = float(product[2]) + int(sale)
    product[1] = str(product[2])
    product[2] = str(new_price)
    return product


products_list = list()

with open("links_for_using.csv", "r", encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    header = next(csv_reader)

    for line in csv_reader:
        product = count_sale(line)


products_list = sorted(products_list)
print(products_list)

with open("products_for_site.csv", "r+", encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    header = next(csv_reader)

    for product in products_list:
        if product not in csv_reader:
            csvfile.write(f"{';'.join(product)}\n")

print(products_list)
