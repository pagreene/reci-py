import random
from datetime import date

# Define seasonal months. The overlaps are intentional.
winter = {12, 1, 2, 3}
spring = {3, 4, 5}
summer = {6, 7, 8, 9}
fall = {8, 9, 10, 11}


# Get the current month.
def month():
    return date.today().month


# Define categories of ingredients and some modifiers that vary by season.
proteins = [
    "Chickpeas/Beans/Lentils",
    "Tofu",
    "Walnuts/Peanuts",
    "Pine Nut/Chia Seeds",
    "Sunflower seeds/Pumpkin Seeds",
    "'Meat'balls",
]
proteins_mods = {
    "Chickpeas/Beans/Lentils": 4,
    "Tofu": 3,
    "Sunflower seeds/Pumpkin Seeds": 2 if month() in fall | winter else 0.5,
    "Walnuts/Peanuts": 2 if month() in winter else 1,
}

nutrients = [
    "Spinach",
    "Broccoli/Brussel Sprouts/Artichoke Hearts",
    "Green Beans",
    "Peas",
    "Chard",
    "Carrots/Beets",
    "Radishes",
    "Zucs",
    "Tomato",
    "Asparagus",
    "Squash",
    "Bok Choy",
    "Cabbage",
    "Cauliflower",
    "Celery",
    "Cucumber",
    "corn",
]
nutrients_mods = {
    "Spinach": 7 if month() in summer else 5,
    "Peas": 5 if month() in winter | spring else 3,
    "Radishes": 2 if month() in summer else 0.2,
    "Chard": 5 if month() in summer else 1,
    "Tomato": 4 if month() in summer & fall else 1,
    "Carrots/Beets": 5 if month() in summer else 2,
    "Cucumber": 2 if month() in summer else 0.5,
    "corn": 2 if month() in summer else 1,
    "Squash": 2 if month() in fall else 0.1,
}

carbs = [
    "Potatoes",
    "Rice",
    "Bread",
    "Tortilla",
    "Pasta",
    "Quinoa",
    "Couscous",
    "Bulgar",
    "Barley",
    "Millet",
    "Sweet Potatoes",
    "Crust",
]
carbs_mods = {
    "Rice": 5,
    "Pasta": 3,
    "Quinoa": 3,
    "Tortilla": 2,
    "Potatoes": 2 if month() in summer else 1,
    "Sweet Potatoes": 3 if month() in winter else 1,
}

flare = [
    "Peppers",
    "Onions",
    "Leek",
    "Green Onion",
    "Mushrooms",
    "chives",
    "Apples",
    "Raisins",
    "Cheese",
]
flare_mods = {
    "Onions": 3,
    "Mushrooms": 2 if month() in winter else 1,
    "chives": 3 if month() in spring else 0.1,
    "Apples": 1.5 if month() in fall else 1,
    "Raisins": 1.2 if month() in fall | winter else 0.2,
}


def get_weighted_selection(options, mods, n=1):
    """Get a weighted selection based on mods, without replacement."""

    # Make sure I didn't type up any keys wrong.
    assert (opt_set := set(options)) >= (
        key_set := set(mods.keys())
    ), f"Some keys aren't in options: {key_set - opt_set}"

    # Make a list of weights based on the mods.
    weights = [mods.get(option, 1) for option in options]
    results = []
    for _ in range(n):
        # Remove selected options from the list to ensure no duplicates.
        if results:
            options, weights = zip(
                *[(opt, w) for opt, w in zip(options, weights) if opt not in results]
            )

        # Get a random selection.
        results += random.choices(options, weights=weights)

    return results


def select_meal():
    """Select a meal."""
    # Choose 2 proteins or 2 nutrients, and 1 of the other.
    maybe_double = [(proteins, proteins_mods), (nutrients, nutrients_mods)]
    random.shuffle(maybe_double)

    double, single = maybe_double

    # Flip a coin to choose some flare.
    add_flare = random.choice([True, True, False])

    # Make the selections.
    num_extra = 2+(double[0] is nutrients)
    selection = get_weighted_selection(*double, n=num_extra)
    selection += get_weighted_selection(*single, n=1+(single[0] is nutrients)) + get_weighted_selection(
        carbs, carbs_mods
    )
    if add_flare:
        selection += get_weighted_selection(flare, flare_mods)

    # Make choices on the a/b options.
    return {random.choice(item.split("/")) for item in selection}


def get_sort_key(item):
    """We want to show things in the order of proteins, nutrients, carbs, flare."""
    type_order = [proteins, nutrients, carbs, flare]
    for k, category in enumerate(type_order):
        # To handle the case of ingredients split by "/", just make the whole list a string.
        if item in ",".join(category):
            return (k, item)


# Select 3 meals. Just brute-force making the meals use unique ingredients.
used_ingredients = {}
for i in range(3):
    # Keep selecting meals until we get one that has no re-used ingredients.
    tries = 1
    used_once = {item for item, cnt in used_ingredients.items() if cnt == 1}
    used_mult = {item for item, cnt in used_ingredients.items() if cnt > 1}
    while len((meal := select_meal()) & used_once) > 1 or meal & used_mult:
        tries += 1
        continue

    # Record the ingredients used in this meal.
    for item in meal:
        if item not in used_ingredients:
            used_ingredients[item] = 0
        used_ingredients[item] += 1

    # Report the result, neatly sorted.
    ingredients = '\n'.join(sorted(meal, key=get_sort_key))
    print(f"Meal {i+1} ({tries} tries):\n{ingredients}")
    print()

grocery_list_str = "\n".join(
    f"{cnt} {item}"
    for item, cnt in sorted(
        used_ingredients.items(),
        key=lambda key_value_pair: get_sort_key(key_value_pair[0]),
    )
)
print(f"\nGrocery list:\n{grocery_list_str}")
