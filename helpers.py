# some helper functions will be defined here
import requests

# The URL to fetch dishes from
URL = "https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup"

# categories to extract
CATEGORIES_TO_EXTRACT = ["Pizzas", "Drinks", "Desserts"]

# internal function
def generate_dish_item(item):
    dish_item = {}
    dish_item["id"] = item["dishId"]
    dish_item["name"] = item["dishName"]
    dish_item["description"] = item["dishDescription"]
    dish_item["price"] = item["dishPrice"]

    return dish_item

# internal function
def generate_dishes_dict(dish_list):
    dishes_dict = {}

    for dish in dish_list:
        dishes_dict[int(dish["dishId"])] = generate_dish_item(dish)

    return dishes_dict


# the method to fetch and build the data in appropriate structure
def build_data():
    # a GET request is sent to the URL
    response = requests.get(URL)
    data = {}
    raw_json = response.json()

    for category in raw_json["Data"]["categoriesList"]:
        if category["categoryName"] in CATEGORIES_TO_EXTRACT:
            dishes_dict = generate_dishes_dict(category["dishList"])
            data[category["categoryName"].lower()] = dishes_dict

    return data
