from django.shortcuts import render
import random
import time

def main(request):
    '''
    displaying the main restaurant page
    '''
    return render(request, "restaurant/main.html")

def order(request):
    '''
    showing the ordering page with popcorn options
    '''
    specials = ["Buttered Popcorn", "Caramel Popcorn", "Cheddar Popcorn", "Cookie Batter Popcorn"]
    daily_special = random.choice(specials)
    context = {"daily_special": daily_special}
    return render(request, "restaurant/order.html", context)

def confirmation(request):
    '''
    processing the customer's order based on order form and showing the confirmation page
    '''
    if request.method == "POST":
        order_items = []
        total_price = 0  # total price of the food before start of order

        selected_items = request.POST.getlist("items")  # getting selected popcorn flavors from form
        extras = request.POST.getlist("extras")  # getting selected extras from form
        special_instructions = request.POST.get("instructions", "").strip()  # getting instructions from form

        # processing ordered popcorn flavors
        for item in selected_items:
            item_name, price = item.rsplit(",", 1)  # splitting name and price
            order_items.append(item_name)  # adding item name to order
            total_price += float(price)  # adding price to total

        # processing extras options
        for extra in extras:
            extra_name, extra_price = extra.rsplit(",", 1)
            order_items.append(extra_name)  # adding extra option to order
            total_price += float(extra_price)  # adding extra option price to total

        # generating a random ready time between 30 mins and an hour 
        minutes = random.randint(30, 60)
        now_time = time.time()
        calc_time = now_time + (minutes * 60)
        ready_time = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(calc_time))

        context = {
            "order_items": order_items,
            "total_price": f"{total_price:.2f}",  # making the total price round to two decimal places
            "ready_time": ready_time,
            "customer_name": request.POST.get("name"),
            "customer_phone": request.POST.get("phone"),
            "customer_email": request.POST.get("email"),
            "special_instructions": special_instructions,  
        }
        return render(request, "restaurant/confirmation.html", context)

