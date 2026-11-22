"""Rules for cleaning ingredient names.

Used by project_Rakel.ipynb (to clean the ingredient lists of the recipes) and by
reviews.ipynb (to find the same clean ingredient names in the review texts), so both
use exactly the same rules. See step 7 in project_Rakel.ipynb for how the rules were made.
"""
import re

# Step 1: names where removing a word would change the ingredient, so they are fixed first
KEEP = {
    "dry mustard": "mustard powder", "dried mustard": "mustard powder", "ground mustard": "mustard powder",
    "dry milk": "milk powder", "powdered milk": "milk powder", "nonfat dry milk": "milk powder",
    "lean ground meat": "ground meat", "ground meat": "ground meat",
    "1% fat cottage cheese": "cottage cheese",
}

# Step 1: describing words, brand names and phrases that do not change what the ingredient is
PHRASES = ["extra virgin", "extra-virgin", "low sodium", "reduced sodium", "low fat", "fat free",
           "reduced fat", "all-purpose", "all purpose", "freshly ground", "fresh ground",
           "old fashioned", "old-fashioned", "whole grain", "whole-grain", "head of", "ear of", "ears of",
           # brand names (not kept where the brand is the product: velveeta, cool whip, bisquick, jell-o)
           "campbell's", "kraft", "nestle", "toll house", "pillsbury", "hidden valley", "jimmy dean",
           "hellmann's", "hellmanns", "philadelphia", "heinz", "lea & perrins", "betty crocker", "hormel",
           "lipton", "knorr", "mccormick's", "mccormick", "kikkoman's", "kikkoman", "swanson", "old el paso"]
WORDS = {"fresh", "freshly", "minced", "chopped", "diced", "sliced", "grated", "shredded", "crushed",
         "large", "small", "medium", "unsalted", "salted", "ground", "finely", "coarsely", "boneless",
         "skinless", "lean", "extra", "virgin", "granulated", "kosher", "plain", "pure", "cooked",
         "uncooked", "frozen", "canned", "softened", "melted", "beaten", "peeled", "pitted", "boiling",
         "cold", "warm", "lukewarm", "packed", "light", "dark", "sharp", "mild", "organic", "baby",
         "low-fat", "fat-free", "nonfat", "non-fat", "reduced-fat", "low-sodium", "reduced-sodium",
         "whole", "raw", "dried", "dry",
         "semi-sweet", "semisweet", "unsweetened", "miniature", "mini", "rolled", "quick-cooking", "quick",
         "creamy", "chunky", "crunchy", "smooth", "slivered", "coarse", "cracked", "unbleached", "bleached",
         "wide", "fillet", "fillets", "original", "jumbo"}


# sizes and percentages like 8-inch, 9", 95%, 10-minute (but not 7-up, v8, a.1.)
SIZE = re.compile(r'^\d+(%|"|-inch|-minute)$')


def remove_describing_words(name):
    if name in KEEP:
        return KEEP[name]
    # "lemon, juice of" -> "lemon juice", "limes, zest of" -> "lime zest"
    m = re.match(r"^(\w+?)s?, (juice|zest|rind|juice and zest|juice and rind) of$", name)
    if m:
        fruit, part = m.groups()
        parts = {"juice": "juice", "zest": "zest", "rind": "zest"}
        return "; ".join(f"{fruit} {parts[p]}" for p in part.split(" and "))
    for phrase in PHRASES:
        name = re.sub(rf"\b{re.escape(phrase)}(?!\w)", " ", name)
    words = [w for w in name.split() if w not in WORDS and not SIZE.match(w)]
    return " ".join(words) if words else name      # never remove everything


# Step 2: plural -> singular, only if the singular form exists in the data
def to_singular(name, known_names):
    if name.endswith("'s"):                        # m&m's, not a plural
        return name
    if name.endswith("leaves"):                    # thyme leaves -> thyme leaf
        return name[:-6] + "leaf"
    for plural, singular in [("ies", "y"), ("oes", "o"), ("ches", "ch"), ("ves", "f"), ("s", "")]:
        if name.endswith(plural) and not name.endswith("ss"):
            candidate = name[: -len(plural)] + singular
            if candidate in known_names:
                return candidate
    return name


# Step 3: synonyms; "; " splits one name into two ingredients
SYNONYMS = {
    "garlic clove": "garlic",
    "clove garlic": "garlic",
    "black pepper": "pepper",
    "salt and pepper": "salt; pepper",
    "salt & pepper": "salt; pepper",
    "salt and black pepper": "salt; pepper",
    "salt & black pepper": "salt; pepper",
    "sea salt": "salt",
    "table salt": "salt",
    "white sugar": "sugar",
    "confectioners' sugar": "powdered sugar",
    "icing sugar": "powdered sugar",
    "vanilla extract": "vanilla",
    "oil": "vegetable oil",
    "cooking oil": "vegetable oil",
    "salad oil": "vegetable oil",
    "scallion": "green onion",
    "spring onion": "green onion",
    "catsup": "ketchup",
    "chicken breast half": "chicken breast",
    # found when we read through the clean names
    "cayenne": "cayenne pepper",
    "jalapeno pepper": "jalapeno",
    "celery rib": "celery",
    "celery stalk": "celery",
    "dill weed": "dill",
    "basil leaf": "basil",
    "oregano leaf": "oregano",
    "oregano leaves": "oregano",
    "parsley leaf": "parsley",
    "parsley leaves": "parsley",
    "parsley flakes": "parsley",
    "spinach leaf": "spinach",
    "spinach leaves": "spinach",
    "cocoa powder": "cocoa",
    "whipping cream": "heavy cream",
    "heavy whipping cream": "heavy cream",
    "half-and-half cream": "half-and-half",
    "condensed cream of mushroom soup": "cream of mushroom soup",
    "condensed cream of chicken soup": "cream of chicken soup",
    "condensed cream of celery soup": "cream of celery soup",
    "condensed cream of tomato soup": "cream of tomato soup",
    "elbow macaroni": "macaroni",
    "feta": "feta cheese",
    "cheddar": "cheddar cheese",
    "parmesan": "parmesan cheese",
    "mozzarella": "mozzarella cheese",
    "taco seasoning mix": "taco seasoning",
    "hot water": "water",
    "ice water": "water",
    "kernel corn": "corn",
    "corn kernel": "corn",
    "apple cider vinegar": "cider vinegar",
    "chicken bouillon cube": "chicken bouillon",
    "chicken bouillon granules": "chicken bouillon",
    "beef bouillon cube": "beef bouillon",
    "beef bouillon granules": "beef bouillon",
    "bicarbonate of soda": "baking soda",
    "italian seasoned breadcrumbs": "italian breadcrumbs",
    "italian style breadcrumbs": "italian breadcrumbs",
    "pecan half": "pecans",
    "pecan halves": "pecans",
    "rotel": "rotel tomatoes",
    "ro-tel tomatoes": "rotel tomatoes",
    "chocolate chip": "chocolate chips",
    "powdered milk": "milk powder",
    "grain mustard": "mustard",
    "gingerroot": "ginger",
    "milk ricotta cheese": "ricotta cheese",
}

# Step 3: leaves of herbs count as the herb (thyme leaf -> thyme), except leaves that are an ingredient themselves
LEAF_NAMES = {"bay leaf", "curry leaf", "banana leaf", "kaffir lime leaf", "lime leaf", "grape leaf"}

# Not food: kitchen equipment that some recipes list as an ingredient
NOT_FOOD = {"aluminum foil", "reynolds wrap foil", "wooden skewer", "bamboo skewer", "toothpick", "paraffin wax",
            "parchment paper", "wax paper", "plastic wrap", "oven cooking bag", "jar", "tall slender 4 cup container"}


# For the reviews: every way an ingredient can be written in a review -> its clean name
def review_forms(vocabulary):
    """Map written forms to clean names: the clean name itself, its plural, and the synonyms
    (with their plurals) that lead to it. E.g. 'tomatoes' -> 'tomato', 'scallions' -> 'green onion'."""
    def plurals(name):
        forms = {name, name + "s", name + "es"}
        if name.endswith("y"):
            forms.add(name[:-1] + "ies")
        if name.endswith("leaf"):
            forms.add(name[:-4] + "leaves")
        return forms

    forms = {}
    for name in sorted(vocabulary):                    # sorted, so the result is the same in every run
        for form in plurals(name):
            forms.setdefault(form, name)
    for synonym, name in sorted({**SYNONYMS, **REVIEW_SYNONYMS}.items()):
        if name in vocabulary:                         # only synonyms that lead to one clean name
            for form in plurals(synonym):
                forms.setdefault(form, name)
    return forms


# written forms that only occur in the reviews (not in the ingredient lists)
REVIEW_SYNONYMS = {
    "corn starch": "cornstarch",
    "cloves of garlic": "garlic",
    "clove of garlic": "garlic",
}
