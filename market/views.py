from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from market.models import Car, Order, Payment


def show_cars(request: HttpRequest) -> HttpResponse:
    user_id = request.session.get("user_id", None)
    if user_id is None:
        return HttpResponseRedirect("/login")
    context = {
        "cars": Car.objects.all()
    }
    return render(request, "cars.html", context)


def audi_purchase(request: HttpRequest, id_: int) -> HttpResponse:
    car = Car.objects.filter(id=id_).first()

    if request.method == "POST":
        order = Order.objects.create(
            car=car,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
        )

        payment = Payment.objects.create(
            order=order,
            amount=order.car.price,
        )
        return HttpResponseRedirect(f"/payment/{payment.id}")

    return render(request, "purchase_form.html", {"car": car})


def payment(request: HttpRequest, id_: int) -> HttpResponse:
    payment = Payment.objects.get(pk=id_)
    car = Car.objects.filter(id=payment.order.car.id).first()

    if request.method == "POST":
        credit_card = request.POST.get("credit_card", "")
        assert len(credit_card) > 0
        payment.credit_card = credit_card
        """
        Хдесь мы передали параметр update_fields, чтобы 
        запрос в базу данных был проще. Но это не обязательно.
        Так стоит делать, если есть вероятность, что объект
        может быть изменён где-то ещё.
        """
        payment.save(update_fields=["credit_card"])
        return HttpResponseRedirect(f"/")

    return render(request, "purchase_form2.html", {"car": car})
