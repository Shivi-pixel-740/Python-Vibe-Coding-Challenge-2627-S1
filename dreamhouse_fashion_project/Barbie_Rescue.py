
import turtle
import random
from pathlib import Path

# ==========================================
# DREAMHOUSE FASHION VENDING MACHINE
# ==========================================

screen = turtle.Screen()
screen.title("Dreamhouse Fashion Vending Machine")
screen.setup(1000, 760)
screen.bgcolor("#fff0f7")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

BASE = Path(__file__).resolve().parent
ASSETS = BASE / "assets"

PINK = "#f062a6"
DARK_PINK = "#c52c86"
LIGHT_PINK = "#ffd6e9"
PURPLE = "#cdb4f5"
MINT = "#b8e0d2"
GOLD = "#ffd166"
WHITE = "#ffffff"
DARK = "#66334f"

buttons = []
sprites = []

coins = 12
style_stars = 0
collection_index = 0
current_category = "Clothing"
last_item = None
message = "Welcome! Choose a collection and start shopping!"

outfit = {
    "Clothing": None,
    "Shoes": None,
    "Accessory": None
}

# Item format: name, category, picture filename
collections = {
    "Dreamhouse Glam": [
        ("Pink Party Dress", "Clothing", "dress.gif"),
        ("Sparkle Jacket", "Clothing", "jacket.gif"),
        ("Pink Heels", "Shoes", "shoes.gif"),
        ("Glitter Boots", "Shoes", "shoes.gif"),
        ("Royal Crown", "Accessory", "crown.gif"),
        ("Star Glasses", "Accessory", "glasses.gif"),
        ("Heart Handbag", "Accessory", "bag.gif")
    ],
    "Beach Party": [
        ("Summer Dress", "Clothing", "dress.gif"),
        ("Beach Jacket", "Clothing", "jacket.gif"),
        ("Beach Sandals", "Shoes", "shoes.gif"),
        ("Sunny Crown", "Accessory", "crown.gif"),
        ("Beach Sunglasses", "Accessory", "glasses.gif"),
        ("Beach Bag", "Accessory", "bag.gif")
    ],
    "Rockstar": [
        ("Concert Dress", "Clothing", "dress.gif"),
        ("Rockstar Jacket", "Clothing", "jacket.gif"),
        ("Star Boots", "Shoes", "shoes.gif"),
        ("Rockstar Crown", "Accessory", "crown.gif"),
        ("Stage Glasses", "Accessory", "glasses.gif"),
        ("Guitar Bag", "Accessory", "bag.gif")
    ]
}

collection_names = list(collections.keys())
wardrobe = []
seen_items = set()

# Register pictures that exist in the assets folder.
pictures = {}

for filename in {
    item[2]
    for items in collections.values()
    for item in items
}:
    path = ASSETS / filename
    if path.exists():
        try:
            screen.register_shape(str(path))
            pictures[filename] = str(path)
        except turtle.TurtleGraphicsError:
            pass


# ==========================================
# DRAWING HELPERS
# ==========================================

def write_at(x, y, text, size=13, color=DARK,
             align="left"):
    pen.goto(x, y)
    pen.color(color)
    pen.write(
        str(text),
        align=align,
        font=("Arial", size, "bold")
    )


def rectangle(x, y, width, height, color,
              outline=None):
    pen.goto(x, y)
    pen.setheading(0)
    pen.color(outline or color)
    pen.pendown()
    pen.begin_fill()
    pen.fillcolor(color)

    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)

    pen.end_fill()
    pen.penup()


def button(x, y, width, height, label, action,
           color=LIGHT_PINK, text_size=11):
    rectangle(x, y, width, height, color, WHITE)

    write_at(
        x + width / 2,
        y + height / 2 - text_size / 2,
        label,
        text_size,
        DARK,
        "center"
    )

    buttons.append((
        x, y, x + width, y + height, action
    ))


def picture(filename, x, y):
    if filename not in pictures:
        return

    sprite = turtle.Turtle()
    sprite.hideturtle()
    sprite.penup()
    sprite.shape(pictures[filename])
    sprite.goto(x, y)
    sprite.showturtle()
    sprites.append(sprite)


def clear_scene():
    pen.clear()
    buttons.clear()

    for sprite in sprites:
        sprite.hideturtle()
        sprite.clear()

    sprites.clear()


def show_message(text):
    global message
    message = text


def current_collection():
    return collection_names[collection_index]


def collection_items(category=None):
    items = collections[current_collection()]

    if category is None:
        return items

    return [
        item for item in items
        if item[1] == category
    ]


# ==========================================
# HOME: THE VENDING MACHINE
# ==========================================

def home():
    clear_scene()
    screen.bgcolor("#fff0f7")

    write_at(
        0, 315,
        "DREAMHOUSE FASHION",
        25, DARK_PINK, "center"
    )
    write_at(
        0, 280,
        "THE MAGIC VENDING MACHINE",
        15, "#9b59b6", "center"
    )

    # Collection selector
    button(
        -380, 220, 190, 42,
        "< Previous Style",
        ("previous_collection",),
        PURPLE
    )

    button(
        -175, 220, 350, 42,
        current_collection(),
        ("collection_info",),
        LIGHT_PINK,
        13
    )

    button(
        205, 220, 190, 42,
        "Next Style >",
        ("next_collection",),
        PURPLE
    )

    # Main vending machine body
    rectangle(-430, -260, 470, 440, PINK, DARK_PINK)
    rectangle(-410, 40, 430, 120, "#fffaff", WHITE)

    write_at(
        -195, 130, "FASHION DROP!",
        15, DARK_PINK, "center"
    )

    if last_item:
        write_at(
            -195, 95, last_item[0],
            13, DARK_PINK, "center"
        )
        picture(last_item[2], -195, 60)
    else:
        write_at(
            -195, 83, "Your next look is waiting...",
            12, DARK, "center"
        )

    write_at(
        -195, -10,
        "SELECT WHAT TO DISPENSE",
        11, WHITE, "center"
    )

    # Item category controls
    button(
        -405, -70, 190, 42,
        "Dresses & Jackets",
        ("category", "Clothing"),
        "#ffe0ef"
    )

    button(
        -195, -70, 190, 42,
        "Shoes",
        ("category", "Shoes"),
        "#e4d7ff"
    )

    button(
        -405, -125, 190, 42,
        "Bags & Accessories",
        ("category", "Accessory"),
        "#d5f5e8"
    )

    button(
        -195, -125, 190, 42,
        "SURPRISE DROP!",
        ("vend",),
        GOLD,
        12
    )

    rectangle(-405, -230, 420, 65, "#fffaff", WHITE)
    write_at(
        -195, -188,
        f"YOUR COINS: {coins}  |  COST: 2",
        14, DARK_PINK, "center"
    )

    # Player information panel
    rectangle(65, -260, 365, 440, "#fffaff", PINK)

    write_at(
        245, 145, "YOUR DREAM LOOK",
        17, DARK_PINK, "center"
    )

    y = 95

    for category, item in outfit.items():
        name = item[0] if item else "Not chosen"

        write_at(
            95, y,
            f"{category}:",
            11, "#9b59b6"
        )
        write_at(
            95, y - 22,
            name,
            11, DARK
        )
        y -= 65

    write_at(
        245, -110,
        f"Style Stars: {style_stars}",
        15, DARK_PINK, "center"
    )

    button(
        95, -165, 140, 42,
        "My Wardrobe",
        ("wardrobe",),
        PURPLE
    )

    button(
        255, -165, 140, 42,
        "Style Challenge",
        ("challenge",),
        GOLD
    )

    button(
        95, -220, 140, 42,
        "Save My Look",
        ("save",),
        MINT
    )

    button(
        255, -220, 140, 42,
        "Runway Show",
        ("runway",),
        LIGHT_PINK
    )

    # Status message
    write_at(
        0, -320, message,
        11, DARK_PINK, "center"
    )

    screen.update()


# ==========================================
# COLLECTIONS
# ==========================================

def change_collection(direction):
    global collection_index

    collection_index = (
        collection_index + direction
    ) % len(collection_names)

    show_message(
        "New collection: " + current_collection()
    )
    home()


# ==========================================
# VENDING MACHINE
# ==========================================

def vend_item(category=None):
    global coins, last_item

    if coins < 2:
        show_message(
            "Not enough coins! Complete a challenge to earn more."
        )
        home()
        return

    choices = collection_items(category)

    if not choices:
        show_message("No items in this category!")
        home()
        return

    coins -= 2
    item = random.choice(choices)
    last_item = item

    name, item_category, filename = item

    if name not in seen_items:
        wardrobe.append(item)
        seen_items.add(name)

        show_message(
            "SURPRISE! You got " + name + "!"
        )
    else:
        # Duplicate drops give a small refund.
        coins += 1
        show_message(
            "Duplicate item! You got 1 coin back."
        )

    home()


# ==========================================
# WARDROBE
# ==========================================

def show_wardrobe():
    clear_scene()

    write_at(
        0, 300, "YOUR FASHION CLOSET",
        23, DARK_PINK, "center"
    )

    write_at(
        0, 265,
        "Click an item to wear it in that category.",
        12, DARK, "center"
    )

    if not wardrobe:
        write_at(
            0, 100,
            "Your closet is empty!",
            17, DARK_PINK, "center"
        )
        write_at(
            0, 65,
            "Visit the vending machine to collect items.",
            12, DARK, "center"
        )

    # Display up to 12 items per page.
    visible_items = wardrobe[:12]

    for index, item in enumerate(visible_items):
        row = index // 3
        col = index % 3

        x = -350 + col * 250
        y = 165 - row * 105

        rectangle(x, y - 65, 220, 85, "#fffaff", PINK)

        write_at(
            x + 110, y - 5,
            item[0][:25],
            10, DARK_PINK, "center"
        )

        picture(item[2], x + 110, y - 40)

        button(
            x + 25, y - 92, 170, 27,
            "WEAR THIS",
            ("wear", index),
            LIGHT_PINK,
            10
        )

    write_at(
        -350, -265,
        f"Collected: {len(wardrobe)} items",
        12, DARK_PINK
    )

    button(
        170, -300, 220, 45,
        "Back to Vending Machine",
        ("home",),
        PURPLE
    )

    screen.update()


def wear_item(index):
    item = wardrobe[index]
    name, category, filename = item

    outfit[category] = item

    show_message("You are now wearing " + name + "!")
    home()


# ==========================================
# STYLE CHALLENGES
# ==========================================

def challenge_screen():
    clear_scene()

    write_at(
        0, 260, "FASHION EMERGENCY!",
        24, DARK_PINK, "center"
    )

    challenges = [
        (
            "Which item completes a royal look?",
            ["Crown", "Beach Bag", "Sneakers"],
            "Crown"
        ),
        (
            "What is best for a sunny beach day?",
            ["Winter Jacket", "Beach Sandals", "Snow Boots"],
            "Beach Sandals"
        ),
        (
            "Which item adds sparkle to a look?",
            ["Star Glasses", "Rain Boots", "Plain Scarf"],
            "Star Glasses"
        ),
        (
            "What helps finish a stylish outfit?",
            ["A matching accessory", "Nothing at all", "A school book"],
            "A matching accessory"
        )
    ]

    question = random.choice(challenges)

    write_at(
        0, 190, question[0],
        14, DARK, "center"
    )

    for index, answer in enumerate(question[1]):
        button(
            -180, 105 - index * 70,
            360, 48,
            answer,
            ("answer", answer, question[2]),
            GOLD if index == 0 else LIGHT_PINK
        )

    button(
        -120, -160, 240, 45,
        "Back Home",
        ("home",),
        PURPLE
    )

    screen.update()


def answer_challenge(answer, correct_answer):
    global coins, style_stars

    if answer == correct_answer:
        coins += 3
        style_stars += 1

        show_message(
            "Correct! +3 coins and +1 Style Star!"
        )
    else:
        show_message(
            "Not quite! Try another fashion challenge."
        )

    home()


# ==========================================
# SAVE OUTFIT AND RUNWAY
# ==========================================

def save_outfit():
    global style_stars

    if all(outfit.values()):
        style_stars += 3

        show_message(
            "Complete look saved! +3 Style Stars!"
        )
    else:
        show_message(
            "Choose clothing, shoes AND an accessory first!"
        )

    home()


def runway_show():
    clear_scene()

    write_at(
        0, 285, "DREAMHOUSE RUNWAY",
        25, DARK_PINK, "center"
    )

    write_at(
        0, 245, "YOUR FASHION MOMENT",
        14, "#9b59b6", "center"
    )

    # Draw a simple runway.
    rectangle(-150, -180, 300, 360, "#ffe0ef", WHITE)

    write_at(
        0, 140, "YOUR LOOK",
        15, DARK_PINK, "center"
    )

    y = 90

    for category, item in outfit.items():
        name = item[0] if item else "Not selected"

        write_at(
            0, y, category + ": " + name,
            11, DARK, "center"
        )
        y -= 35

        if item:
            picture(item[2], 0, y + 5)
            y -= 35

    if all(outfit.values()):
        write_at(
            0, -215,
            "RUNWAY READY!",
            16, DARK_PINK, "center"
        )
    else:
        write_at(
            0, -215,
            "Finish your outfit for the full look!",
            11, DARK_PINK, "center"
        )

    write_at(
        0, -250,
        f"Style Stars: {style_stars}",
        13, DARK, "center"
    )

    button(
        -130, -315, 260, 45,
        "Back to Vending Machine",
        ("home",),
        PURPLE
    )

    screen.update()


# ==========================================
# MOUSE CONTROLS
# ==========================================

def on_click(x, y):
    for x1, y1, x2, y2, action in buttons[:]:
        if x1 <= x <= x2 and y1 <= y <= y2:
            kind = action[0]

            if kind == "previous_collection":
                change_collection(-1)

            elif kind == "next_collection":
                change_collection(1)

            elif kind == "collection_info":
                show_message(
                    "Collection: " + current_collection()
                )
                home()

            elif kind == "category":
                vend_item(action[1])

            elif kind == "vend":
                vend_item()

            elif kind == "wardrobe":
                show_wardrobe()

            elif kind == "wear":
                wear_item(action[1])

            elif kind == "challenge":
                challenge_screen()

            elif kind == "answer":
                answer_challenge(action[1], action[2])

            elif kind == "save":
                save_outfit()

            elif kind == "runway":
                runway_show()

            elif kind == "home":
                home()

            return


# ==========================================
# START GAME
# ==========================================

def main():
    screen.onclick(on_click)
    home()
    screen.mainloop()


if __name__ == "__main__":
    main()

