import random
from datetime import date
from typing import List, Set

# Define seasonal months. The overlaps are intentional.
winter = {12, 1, 2, 3}
spring = {3, 4, 5}
summer = {6, 7, 8, 9}
fall = {8, 9, 10, 11}


NUM_MEALS = 2
NUM_PEOPLE = 4


# Get the current month.
def month():
    return date.today().month


class Ingredient:
    """Represent an ingredient and its serving size."""

    def __init__(self, name: str, serving: float, serving_units: str):
        self.name: str = name
        self.serving: float = serving
        self.serving_units: str = serving_units

    def with_serving(self, serving: float) -> "Ingredient":
        return Ingredient(self.name, serving, self.serving_units)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return other.name == self.name
        elif isinstance(other, IngredientGrp):
            return any(self == option for option in other.options)
        return False

    def __lt__(self, other):
        if isinstance(other, Ingredient):
            return self.name < other.name
        raise ValueError(f"Cannot compare Ingredient to {type(other)}")

    def __str__(self):
        return f"{self.name} [{self.serving:.3} {self.serving_units}]"


class IngredientGrp:
    """Represent a grouping of ingredients (including one), and a preference."""

    def __init__(self, *options: Ingredient, pref: float = 1):
        self.options: List[Ingredient] = list(options)
        self.pref: float = pref

    def select(self) -> Ingredient:
        return random.choice(self.options)

    def __hash__(self):
        return hash(self.options)


chickpeas = Ingredient("chickpeas", 5, "oz")
beans = Ingredient("beans", 5, "oz")
lentils = Ingredient("lentils", 1/3, "cup")
tofu = Ingredient("tofu", 3.5, "oz")
walnuts = Ingredient("walnuts", 1, "oz")
peanuts = Ingredient("peanuts", 1, "oz")
pine_nuts = Ingredient("pine nuts", 1, "oz")
chia_seeds = Ingredient("chia seeds", 1, "oz")
sf_seeds = Ingredient("sunflower seeds", 1, "oz")
pumpkin_seeds = Ingredient("pumpkin seeds", 1, "oz")
meat_balls = Ingredient("'meat' balls", 1, "serving")

spinach = Ingredient("spinach", 1, "cup")
broccoli = Ingredient("broccoli", 1, "cup")
brussel_sprouts = Ingredient("brussel sprouts", 1, "cup")
artichoke_hearts = Ingredient("artichoke hearts", 1/3, "can")
green_beans = Ingredient("green beans", 1, "cup")
peas = Ingredient("peas", 0.5, "cup")
chard = Ingredient("chard", 1, "cup")
carrots = Ingredient("carrot", 1, "carrot")
beets = Ingredient("beets", 1, "beet")
radishes = Ingredient("radishes", 2.5, "radish")
zucs = Ingredient("zuc", 1/2, "zuc")
tomatoes = Ingredient("tomato", 1.5, "tomato")
asparagus = Ingredient("asparagus", 1/3, "bunch")
squash = Ingredient("squash", 4, "oz")
bok_choy = Ingredient("bok choy", 1/3, "bunch")
cabbage = Ingredient("cabbage", 1/4, "head")
cauliflower = Ingredient("cauliflower", 1/4, "head")
celery = Ingredient("celery", 2, "stalks")
cucumber = Ingredient("cucumber", 1/4, "cucumber")
corn = Ingredient("corn", 1/2, "ear")

potatoes = Ingredient("potatoes", 1, "medium potato")
rice = Ingredient("rice", 1/6, "cups")
bread = Ingredient("bread", 1/10, "loaf")
tortilla = Ingredient("tortilla", 1, "tortilla")
pasta = Ingredient("pasta", 2, "oz")
quinoa = Ingredient("quinoa", 1/4, "cups")
couscous = Ingredient("couscous", 1/3, "cups")
bulgar = Ingredient("bulgar", 1/3, "cups")
barley = Ingredient("barley", 1/2, "cups")
millet = Ingredient("millet", 1/3, "cups")
sweet_potatoes = Ingredient("sweet potatoes", 2/3, "potato")
pizza_crust = Ingredient("pizza crust", 1/8, "crust")

peppers = Ingredient("peppers", 1/2, "pepper")
onions = Ingredient("onions", 1/4, "onion")
leek = Ingredient("leek", 1/4, "leek")
mushrooms = Ingredient("mushrooms", 2.5, "oz")
chives = Ingredient("chives", 30, "g")
apples = Ingredient("apples", 1/2, "apple")
raisins = Ingredient("raisins", 1/4, "cup")
cheese = Ingredient("cheese", 1.5, "oz")

# Define categories of ingredients and some modifiers that vary by season.
proteins = [
    IngredientGrp(chickpeas, beans, lentils, pref=4),
    IngredientGrp(tofu, pref=3),
    IngredientGrp(walnuts, peanuts, pref=2 if month() in winter else 1),
    IngredientGrp(pine_nuts, chia_seeds),
    IngredientGrp(sf_seeds, pumpkin_seeds, pref=2 if month() in fall | winter else 0.5),
    IngredientGrp(meat_balls),
]

nutrients = [
    IngredientGrp(spinach, pref=7 if month() in summer else 5),
    IngredientGrp(broccoli, brussel_sprouts, artichoke_hearts),
    IngredientGrp(green_beans),
    IngredientGrp(peas, pref=5 if month() in winter | spring else 3),
    IngredientGrp(chard, pref=5 if month() in summer else 1),
    IngredientGrp(carrots, beets, pref=5 if month() in summer else 2),
    IngredientGrp(radishes, pref=2 if month() in summer else 0.2),
    IngredientGrp(zucs),
    IngredientGrp(tomatoes, pref=4 if month() in summer & fall else 1),
    IngredientGrp(asparagus),
    IngredientGrp(squash, pref=2 if month() in fall else 0.2),
    IngredientGrp(bok_choy),
    IngredientGrp(cabbage, pref=3 if month() in winter & spring else 1),
    IngredientGrp(cauliflower),
    IngredientGrp(celery),
    IngredientGrp(cucumber, pref=2 if month() in summer else 0.5),
    IngredientGrp(corn, pref=2 if month() in summer else 1),
]

carbs = [
    IngredientGrp(potatoes, pref=2 if month() in summer else 1),
    IngredientGrp(rice, pref=5),
    IngredientGrp(bread, pref=3),
    IngredientGrp(tortilla, pref=2),
    IngredientGrp(pasta, pref=5),
    IngredientGrp(quinoa, pref=3),
    IngredientGrp(couscous),
    IngredientGrp(bulgar),
    IngredientGrp(barley),
    IngredientGrp(millet),
    IngredientGrp(sweet_potatoes, pref=2 if month() in summer else 1),
    IngredientGrp(pizza_crust),
]

flare = [
    IngredientGrp(peppers),
    IngredientGrp(onions, pref=3),
    IngredientGrp(leek),
    IngredientGrp(mushrooms, pref=2 if month() in winter else 1),
    IngredientGrp(chives, pref=3 if month() in spring else 0.2),
    IngredientGrp(apples, pref=2 if month() in fall else 0.2),
    IngredientGrp(raisins, pref=1.2 if month() in fall | winter else 0.1),
    IngredientGrp(cheese, pref=2)
]


class Selection:
    def __init__(self, ingredient_grp: IngredientGrp, servings: float):
        self.ingredient_grp = ingredient_grp
        self.servings = servings

    def select(self):
        ingredient = self.ingredient_grp.select()
        return ingredient.with_serving(self.servings*ingredient.serving)

    def __hash__(self):
        return hash(self.ingredient_grp)


def get_weighted_selection(options: List[IngredientGrp], n=1):
    """Get a weighted selection based on mods, without replacement."""

    # Make a list of weights based on the mods.
    weights = [option.pref for option in options]
    results = []
    for _ in range(n):
        # Remove selected options from the list to ensure no duplicates.
        if results:
            options, weights = zip(
                *[(opt, w) for opt, w in zip(options, weights) if opt not in results]
            )

        # Get a random selection.
        results += random.choices(options, weights=weights)

    return [Selection(result, servings=NUM_MEALS*NUM_PEOPLE/n) for result in results]


def select_meal() -> Set[Ingredient]:
    """Select a meal."""
    # Choose 2 proteins or 2 nutrients, and 1 of the other.
    maybe_extra = [proteins, nutrients]
    random.shuffle(maybe_extra)

    extra, norm = maybe_extra

    # Flip a coin to choose some flare.
    add_flare = random.choice([True, True, False])

    # Make the selections.
    num_extra = 3 if extra is nutrients else 2
    num_norm = 2 if norm is nutrients else 1
    selection = get_weighted_selection(extra, n=num_extra)
    selection += get_weighted_selection(norm, n=num_norm) 
    selection += get_weighted_selection(carbs)
    if add_flare:
        selection += get_weighted_selection(flare)

    # Make choices on the options in each group.
    return {item.select() for item in selection}


def get_sort_key(item):
    """We want to show things in the order of proteins, nutrients, carbs, flare."""
    type_order = [proteins, nutrients, carbs, flare]
    for k, category in enumerate(type_order):
        if item in category:
            return k, item


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
    ingredients = '\n'.join(str(item) for item in sorted(meal, key=get_sort_key))
    print(f"Meal {i+1} ({tries} tries):\n{ingredients}")
    print()

grocery_list_str = "\n".join(
    f"{item.with_serving(item.serving*cnt)}" + (f"(used in {cnt} meals)" if cnt > 1 else "")
    for item, cnt in sorted(
        used_ingredients.items(),
        key=lambda key_value_pair: get_sort_key(key_value_pair[0]),
    )
)
print(f"\nGrocery list:\n{grocery_list_str}")
