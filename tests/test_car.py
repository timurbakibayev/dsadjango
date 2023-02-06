from django.test import TestCase
from market.models import Car, Purchase, Order, Payment


class PurchaseTest(TestCase):
    def setUp(self):
        Car.objects.create(name="Audi A6", price=6_000_000, image="https://some_image.png")
        Car.objects.create(name="Audi A7", price=7_000_000, image="https://some_image.png")
        Car.objects.create(name="Audi A8", price=8_000_000, image="https://some_image.png")

    def test_car_count(self):
        self.assertEqual(Car.objects.all().count(), 3)
        car = Car.objects.get(name="Audi A7")
        assert car.name == "Audi A7"

    def test_cars_left_function(self):
        car = Car.objects.get(name="Audi A6")
        # buy 3 cars
        Purchase.objects.create(car=car, count=3)
        # sell 1 car
        Order.objects.create(car=car)
        # we should have 2 cars left
        self.assertEqual(car.cars_left(), 2)
        car = Car.objects.get(name="Audi A7")
        self.assertEqual(car.cars_left(), 0)

    def test_cars_orders_by_client(self):
        # buy_car/<int:id_>
        car = Car.objects.get(name="Audi A6")
        # buy 3 cars
        Purchase.objects.create(car=car, count=4)
        # sell 1 car
        url = f"/buy_car/{car.id}"
        response_get = self.client.get(url)
        # check that there is name="credit_card" in the form

        response = self.client.post(url, {
            "name": "Timur",
            "email": "timur@gmail.com",
            "phone": "+772828778782",
            # "credit_card": "1234 1234 1234 1234",
        })
        self.assertEqual(response.status_code, 302)
        assert car.cars_left() == 3
        url = response.url
        response_get = self.client.get(url)
        # check that there is name="credit_card" in the form
        self.assertContains(response_get, 'name="credit_card"')
        self.assertContains(response_get, car.image)
        self.assertContains(response_get, car.name)
        response = self.client.post(url, {
            "credit_card": "1234 1234 1234 1234",
        })
        self.assertEqual(response.status_code, 302)

        payment = Payment.objects.all().first()
        assert payment.amount == 6_000_000
        assert payment.credit_card == "1234 1234 1234 1234"

    def test_purchase_order_default_is_one(self):
        car = Car.objects.get(name="Audi A7")
        purchase = Purchase.objects.create(car=car)
        self.assertEqual(purchase.count, 1)
