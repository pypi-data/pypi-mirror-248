from chomp.data_manager import (
    add_food_diary_entry,
    get_food,
    FoodNotFoundException,
)
from chomp.food import Food


def eat(food_name, weight=None, percent=1):
    # determine if user provided straight colorie count
    # instead of food name
    try:
        # see if a number was provided instead of a food name
        cal = int(food_name)
        print(f"You ate {cal} calories!!")
        nutri_facts = {"calories": cal}
        food = Food("calories", "None", nutri_facts)
        add_food_diary_entry(food.to_dict())
        return
    except ValueError:
        pass

    # from here on out, we assume that food_name really
    # represents the name of a food
    if abs(percent - 1) < 0.001:
        print(f"You ate {food_name}")
    else:
        print(f"You ate {100 * percent:.1f}% of {food_name}")

    try:
        food = get_food(food_name)
        if weight:
            food_weight = food.get_nutritional_fact("weight")
            percent = weight / food_weight
        food = food * percent
        cal = round(food.get_nutritional_fact("calories"))
        print(f"You ate {cal} calories!!")
        add_food_diary_entry(food.to_dict())
    except FoodNotFoundException:
        print(f"Cannot find {food_name}!")
