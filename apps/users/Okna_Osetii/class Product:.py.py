class Order:
    def __init__(self, product, price, quantity):
        if price < 0 or quantity <= 0:
            raise ValueError("Ввели неверное значение цены или количества")
        self.product, self.price, self.quantity = product, price, quantity

    def total(self):
        return self.price * self.quantity

class OrderView:
    def show(self, order):
        print(order.product, order.quantity, order.total())
class OrderRepository:
    def save(self, order):
        with open("orders.txt", "a", encoding="utf-8") as f:
            f.write(f"{order.product};{order.quantity};{order.total()}\n")
class OrderNotifier:
    def send(self, order):
        print("Уведомление о заказе:", order.product)
order = Order("Куртка", 12000, 2)
OrderView().show(order)
OrderRepository().save(order)
OrderNotifier().send(order)