from pathlib import Path
import zipfile, textwrap, os, math
from PIL import Image, ImageDraw

base = Path("/mnt/data/dreamhouse_fashion_project")
assets = base / "assets"
assets.mkdir(parents=True, exist_ok=True)

# Create original small GIF art assets that Turtle can load directly.
def make_icon(filename, kind, bg, accent, detail):
    im = Image.new("RGBA", (120, 120), (255, 255, 255, 0))
    d = ImageDraw.Draw(im)
    # soft circular backing
    d.ellipse((8, 8, 112, 112), fill=bg, outline=accent, width=4)
    if kind == "dress":
        d.polygon([(48, 30), (72, 30), (78, 45), (97, 88), (23, 88), (42, 45)], fill=detail, outline=accent)
        d.rectangle((46, 24, 74, 38), fill=detail, outline=accent, width=3)
        d.line((40, 48, 80, 48), fill=accent, width=3)
        d.ellipse((55, 53, 65, 63), fill=(255,255,255,220))
    elif kind == "shoes":
        d.ellipse((23, 45, 58, 78), fill=detail, outline=accent, width=3)
        d.ellipse((57, 57, 98, 87), fill=detail, outline=accent, width=3)
        d.line((31, 73, 52, 73), fill=accent, width=4)
        d.line((68, 82, 91, 82), fill=accent, width=4)
    elif kind == "bag":
        d.rounded_rectangle((30, 43, 90, 88), radius=9, fill=detail, outline=accent, width=4)
        d.arc((42, 24, 78, 60), 180, 360, fill=accent, width=5)
        d.ellipse((56, 58, 64, 66), fill=(255,255,255,230))
    elif kind == "crown":
        d.polygon([(27, 76), (20, 40), (43, 57), (60, 25), (77, 57), (100, 40), (93, 76)], fill=detail, outline=accent)
        d.rectangle((27, 76, 93, 88), fill=detail, outline=accent, width=3)
        for x in (34, 60, 86):
            d.ellipse((x-4, 52, x+4, 60), fill=(255,255,255,240))
    elif kind == "glasses":
        d.ellipse((23, 42, 55, 72), outline=accent, width=6)
        d.ellipse((65, 42, 97, 72), outline=accent, width=6)
        d.line((55, 55, 65, 55), fill=accent, width=6)
        d.line((20, 48, 11, 42), fill=accent, width=4)
        d.line((100, 48, 109, 42), fill=accent, width=4)
    elif kind == "jacket":
        d.polygon([(39, 30), (52, 37), (60, 48), (68, 37), (81, 30), (96, 85), (75, 85), (73, 57), (72, 92), (48, 92), (47, 57), (45, 85), (24, 85)], fill=detail, outline=accent)
        d.line((60, 48, 60, 91), fill=accent, width=3)
    im.convert("RGB").save(assets / filename, "GIF")

make_icon("dress.gif", "dress", (255,226,242), (174,61,134), (255,112,180))
make_icon("shoes.gif", "shoes", (230,240,255), (67,104,190), (255,196,95))
make_icon("bag.gif", "bag", (255,239,205), (167,99,40), (186,126,255))
make_icon("crown.gif", "crown", (255,249,200), (179,126,0), (255,211,65))
make_icon("glasses.gif", "glasses", (224,255,240), (30,135,104), (255,255,255))
make_icon("jacket.gif", "jacket", (240,225,255), (115,67,174), (139,103,255))

code = r'''"""
DREAMHOUSE FASHION RESCUE 👗✨
A beginner-friendly interactive Turtle game.

HOW TO PLAY:
1. Run this file in PyCharm.
2. Click the pink buttons with your mouse.
3. Choose a fashion collection and collect items.
4. Dress your mannequin, earn Style Stars, and launch the fashion show!

The GIF pictures are in the assets folder. Keep the assets folder beside this file.
"""

import random
import turtle
from pathlib import Path

# -------------------- GAME SETTINGS --------------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.title("Dreamhouse Fashion Rescue ✨")
screen.bgcolor("#fff0f7")
screen.tracer(False)

ASSET_FOLDER = Path(__file__).resolve().parent / "assets"

# Collections are dictionaries: each one has a name, colour, and item choices.
COLLECTIONS = {
    "Dream Princess": {
        "color": "#f35ca8",
        "items": ["Sparkle Dress", "Crystal Crown", "Glitter Shoes", "Pearl Bag"],
    },
    "Pop Star": {
        "color": "#9a68f2",
        "items": ["Star Jacket", "Shimmer Glasses", "Stage Shoes", "Music Bag"],
    },
    "Beach Day": {
        "color": "#22b8b0",
        "items": ["Sunny Dress", "Shell Crown", "Sandals", "Beach Bag"],
    },
}

ITEM_ART = {
    "Sparkle Dress": "dress.gif",
    "Sunny Dress": "dress.gif",
    "Crystal Crown": "crown.gif",
    "Shell Crown": "crown.gif",
    "Glitter Shoes": "shoes.gif",
    "Stage Shoes": "shoes.gif",
    "Sandals": "shoes.gif",
    "Pearl Bag": "bag.gif",
    "Music Bag": "bag.gif",
    "Beach Bag": "bag.gif",
    "Star Jacket": "jacket.gif",
    "Shimmer Glasses": "glasses.gif",
}

# -------------------- GAME STATE --------------------
style_stars = 0
chosen_collection = None
wardrobe = []
outfit = {"clothing": None, "shoes": None, "accessory": None}
show_started = False

# -------------------- TURTLE HELPERS --------------------
pen = turtle.Turtle(visible=False)
pen.speed(0)
pen.penup()

# Clickable button records: (x1, y1, x2, y2, label, action)
buttons = []


def write_at(x, y, message, size=14, color="#66345a", align="center", bold=False):
    """Write a message at a screen position."""
    pen.penup()
    pen.goto(x, y)
    pen.color(color)
    style = "bold" if bold else "normal"
    pen.write(message, align=align, font=("Arial", size, style))


def draw_box(x, y, width, height, fill, outline="#df72b2", radius=14):
    """Draw a rounded-looking panel using a rectangle with soft colours."""
    pen.penup()
    pen.goto(x - width / 2, y - height / 2)
    pen.color(outline, fill)
    pen.pensize(2)
    pen.pendown()
    pen.begin_fill()
    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)
    pen.end_fill()
    pen.penup()


def add_button(x, y, width, height, label, action, fill="#f35ca8"):
    """Draw a button and save its click area."""
    draw_box(x, y, width, height, fill, outline="#ffffff")
    write_at(x, y - 8, label, 12, "#ffffff", bold=True)
    buttons.append((x - width / 2, y - height / 2,
                    x + width / 2, y + height / 2, action))


def load_item_shape(item_name):
    """Load an item picture as a Turtle shape when possible."""
    filename = ITEM_ART.get(item_name)
    if not filename:
        return None
    path = ASSET_FOLDER / filename
    if not path.exists():
        return None
    shape_name = f"fashion_{filename}"
    try:
        screen.register_shape(shape_name, str(path))
        return shape_name
    except turtle.TurtleGraphicsError:
        return None


def clear_scene():
    """Clear the drawings and buttons, but keep the window open."""
    global buttons
    pen.clear()
    buttons = []
    for item_turtle in screen.turtles():
        if item_turtle is not pen:
            item_turtle.hideturtle()
            item_turtle.clear()
    screen.tracer(False)


def draw_background():
    """Draw the Dreamhouse shop backdrop."""
    screen.bgcolor("#fff0f7")
    draw_box(-300, 220, 350, 120, "#ffe0f0", "#ffffff")
    write_at(-300, 244, "DREAMHOUSE", 24, "#c52c86", bold=True)
    write_at(-300, 210, "FASHION RESCUE STUDIO", 12, "#8b4b7c")
    # sparkle decorations
    for x, y in [(-430, 285), (-180, 275), (100, 285), (430, 270), (-455, -280), (440, -280)]:
        write_at(x, y, "✦", 20, "#f6b900")
    # dressing room mirror
    draw_box(250, 20, 260, 390, "#ffffff", "#d58ac0")
    draw_box(250, 20, 225, 350, "#e8f7ff", "#e9a3cd")
    write_at(250, 183, "YOUR LOOK", 13, "#8b4b7c", bold=True)


def draw_mannequin():
    """Draw a simple mannequin with Turtle lines and shapes."""
    # head
    pen.penup()
    pen.goto(220, 90)
    pen.dot(58, "#ffd6bd")
    # hair
    pen.goto(220, 112)
    pen.dot(64, "#75452d")
    pen.goto(220, 88)
    pen.dot(48, "#ffd6bd")
    # neck and body
    pen.goto(220, 62)
    pen.pensize(13)
    pen.color("#ffd6bd")
    pen.setheading(270)
    pen.pendown()
    pen.forward(28)
    pen.penup()
    # arms
    pen.goto(220, 30)
    pen.pensize(10)
    pen.color("#ffd6bd")
    pen.setheading(200)
    pen.pendown()
    pen.forward(58)
    pen.penup()
    pen.goto(220, 30)
    pen.setheading(340)
    pen.pendown()
    pen.forward(58)
    pen.penup()
    # body / starter outfit
    pen.goto(220, 36)
    pen.color("#f5a1ce")
    pen.setheading(0)
    pen.pensize(3)
    pen.pendown()
    pen.begin_fill()
    pen.goto(250, 10)
    pen.goto(275, -75)
    pen.goto(165, -75)
    pen.goto(190, 10)
    pen.goto(220, 36)
    pen.end_fill()
    pen.penup()
    # legs
    for x in (202, 238):
        pen.goto(x, -75)
        pen.color("#ffd6bd")
        pen.pensize(10)
        pen.setheading(270)
        pen.pendown()
        pen.forward(82)
        pen.penup()
    write_at(220, -178, "STYLE ICON", 10, "#c52c86", bold=True)


def draw_item_picture(item_name, x, y, scale=1.0):
    """Show a GIF item picture, with a text label below it."""
    shape = load_item_shape(item_name)
    if shape:
        art = turtle.Turtle(visible=False)
        art.penup()
        art.shape(shape)
        art.goto(x, y)
        art.shapesize(scale, scale)
        art.showturtle()
    write_at(x, y - 58, item_name, 9, "#66345a")


def show_home(message="Choose a button to begin your fashion rescue!"):
    """Draw the main game screen."""
    clear_scene()
    draw_background()
    draw_mannequin()
    write_at(-300, 130, "Style Stars: " + str(style_stars), 16, "#9a4d87", bold=True)
    write_at(-300, 95, message, 11, "#66345a")
    write_at(-300, 55, "COLLECTIONS", 13, "#c52c86", bold=True)
    add_button(-395, 10, 130, 40, "Dream Princess", ("collection", "Dream Princess"), "#f35ca8")
    add_button(-245, 10, 130, 40, "Pop Star", ("collection", "Pop Star"), "#9a68f2")
    add_button(-95, 10, 130, 40, "Beach Day", ("collection", "Beach Day"), "#22b8b0")
    add_button(-300, -70, 130, 40, "Fashion Challenge", ("challenge",), "#ff9d3d")
    add_button(-300, -125, 130, 40, "Open Wardrobe", ("wardrobe",), "#8c6cf0")
    add_button(-300, -180, 130, 40, "Fashion Show!", ("show",), "#d943a2")
    screen.update()


def choose_collection(name):
    """Choose a style collection and add its items to the wardrobe."""
    global chosen_collection, style_stars
    chosen_collection = name
    for item in COLLECTIONS[name]["items"]:
        if item not in wardrobe:
            wardrobe.append(item)
    style_stars += 1
    show_home(f"{name} collection unlocked! +1 Style Star ✨")


def run_challenge():
    """Ask a fashion emergency question and reward a good answer."""
    global style_stars
    clear_scene()
    draw_background()
    draw_mannequin()
    write_at(-300, 140, "FASHION EMERGENCY! 🚨", 19, "#c52c86", bold=True)
    write_at(-300, 95, "A dress has a tear just before the fashion show.", 12)
    write_at(-300, 65, "What is your best fashion rescue?", 12)
    add_button(-300, 10, 340, 48, "A. Cancel the show", ("challenge_answer", "A"), "#f080a0")
    add_button(-300, -55, 340, 48, "B. Patch it with a creative design", ("challenge_answer", "B"), "#29b89b")
    add_button(-300, -125, 150, 40, "Back Home", ("home",), "#9a68f2")
    screen.update()


def answer_challenge(answer):
    """Reward a creative fashion solution."""
    global style_stars
    if answer == "B":
        style_stars += 2
        show_home("Amazing rescue! +2 Style Stars 🌟")
    else:
        show_home("Try a creative fix next time! You can retry the challenge.")


def show_wardrobe():
    """Display collected fashion items and outfit choices."""
    clear_scene()
    draw_background()
    write_at(-300, 150, "YOUR FASHION WARDROBE 👛", 18, "#c52c86", bold=True)
    write_at(-300, 115, f"Collected items: {len(wardrobe)}", 12)
    if not wardrobe:
        write_at(-300, 70, "Choose a collection on the home screen first!", 11)
    else:
        # display up to 6 items in a neat grid
        for index, item in enumerate(wardrobe[:6]):
            col = index % 3
            row = index // 3
            x = -420 + col * 120
            y = 45 - row * 135
            draw_item_picture(item, x, y, 0.65)
    add_button(-300, -205, 150, 40, "Back Home", ("home",), "#9a68f2")
    add_button(-110, -205, 150, 40, "Build Outfit", ("build",), "#f35ca8")
    screen.update()


def build_outfit_screen():
    """Let the player choose clothing, shoes, and one accessory."""
    clear_scene()
    draw_background()
    write_at(-300, 155, "BUILD YOUR LOOK ✨", 18, "#c52c86", bold=True)
    write_at(-300, 118, "Click an item category, then pick an item.", 11)
    add_button(-400, 70, 125, 38, "Clothing", ("category", "clothing"), "#f35ca8")
    add_button(-260, 70, 125, 38, "Shoes", ("category", "shoes"), "#9a68f2")
    add_button(-120, 70, 125, 38, "Accessory", ("category", "accessory"), "#22b8b0")
    # current outfit summary
    for i, category in enumerate(("clothing", "shoes", "accessory")):
        value = outfit[category] or "Not chosen yet"
        write_at(-300, 20 - i * 28, f"{category.title()}: {value}", 11)
    draw_mannequin()
    add_button(-300, -160, 150, 40, "Back to Wardrobe", ("wardrobe",), "#9a68f2")
    add_button(-100, -160, 150, 40, "Save Outfit", ("save_outfit",), "#f35ca8")
    screen.update()


def choose_item_category(category):
    """Show the available items for the chosen outfit category."""
    clear_scene()
    draw_background()
    write_at(-300, 145, f"CHOOSE {category.upper()} 👗", 18, "#c52c86", bold=True)
    if category == "clothing":
        possible = [item for item in wardrobe if "Dress" in item or "Jacket" in item]
    elif category == "shoes":
        possible = [item for item in wardrobe if "Shoes" in item or "Sandals" in item]
    else:
        possible = [item for item in wardrobe if any(word in item for word in ("Crown", "Bag", "Glasses"))]
    if not possible:
        write_at(-300, 80, "Unlock a collection first to get items!", 12)
    else:
        for i, item in enumerate(possible[:4]):
            x = -410 + i * 100
            draw_item_picture(item, x, 55, 0.65)
            add_button(x, -35, 90, 32, "Choose", ("pick_item", category, item), "#f35ca8")
    add_button(-300, -160, 150, 40, "Back to Outfit", ("build",), "#9a68f2")
    screen.update()


def pick_item(category, item):
    """Put a selected item into the current outfit."""
    outfit[category] = item
    build_outfit_screen()


def save_outfit():
    """Save the look and award a star for a complete outfit."""
    global style_stars
    if all(outfit[category] for category in ("clothing", "shoes", "accessory")):
        style_stars += 3
        show_home("Outfit saved! +3 Style Stars. You are runway ready! 💖")
    else:
        build_outfit_screen()
        write_at(-300, -115, "Choose clothing, shoes AND an accessory first!", 10, "#c52c86")


def fashion_show():
    """Celebrate the player's saved outfit."""
    clear_scene()
    draw_background()
    draw_mannequin()
    write_at(-300, 140, "✨ DREAMHOUSE FASHION SHOW ✨", 18, "#c52c86", bold=True)
    write_at(-300, 105, f"Collection: {chosen_collection or 'Not chosen yet'}", 12)
    write_at(-300, 75, f"Clothing: {outfit['clothing'] or 'Not selected'}", 11)
    write_at(-300, 45, f"Shoes: {outfit['shoes'] or 'Not selected'}", 11)
    write_at(-300, 15, f"Accessory: {outfit['accessory'] or 'Not selected'}", 11)
    write_at(-300, -35, f"Total Style Stars: {style_stars} 🌟", 14, "#c52c86", bold=True)
    if all(outfit[category] for category in ("clothing", "shoes", "accessory")):
        write_at(-300, -75, "You completed a full runway look! 🎉", 12, "#14866d", bold=True)
    else:
        write_at(-300, -75, "Build a complete look to earn 3 more stars!", 11)
    add_button(-300, -155, 150, 40, "Back Home", ("home",), "#9a68f2")
    screen.update()


def on_click(x, y):
    """Run the action for the button the player clicked."""
    for x1, y1, x2, y2, action in buttons[:]:
        if x1 <= x <= x2 and y1 <= y <= y2:
            kind = action[0]
            if kind == "collection":
                choose_collection(action[1])
            elif kind == "challenge":
                run_challenge()
            elif kind == "challenge_answer":
                answer_challenge(action[1])
            elif kind == "wardrobe":
                show_wardrobe()
            elif kind == "build":
                build_outfit_screen()
            elif kind == "category":
                choose_item_category(action[1])
            elif kind == "pick_item":
                pick_item(action[1], action[2])
            elif kind == "save_outfit":
                save_outfit()
            elif kind == "show":
                fashion_show()
            elif kind == "home":
                show_home()
            return


def main():
    """Start the interactive fashion game."""
    show_home()
    screen.onclick(on_click)
    screen.listen()
    screen.mainloop()


if __name__ == "__main__":
    main()
'''
(base / "dreamhouse_fashion_rescue.py").write_text(code, encoding="utf-8")

readme = """# Dreamhouse Fashion Rescue 👗✨

## Run it in PyCharm
1. Extract the ZIP file.
2. Open the extracted `dreamhouse_fashion_project` folder in PyCharm.
3. Make sure `dreamhouse_fashion_rescue.py` and the `assets` folder are beside each other.
4. Right-click `dreamhouse_fashion_rescue.py` and choose **Run**.
5. A Turtle graphics window opens. Click the coloured buttons with your mouse.

## What is included?
- Interactive Turtle screen with clickable buttons.
- Original GIF item pictures stored in `assets/`.
- Three fashion collections.
- A fashion rescue challenge.
- Wardrobe and outfit builder.
- Style Stars and a final fashion show.

## If you get an error
- Do not move the `assets` folder away from the Python file.
- Run the `.py` file, not the README.
- The game uses Python's built-in `turtle` module. PyCharm must be running on a computer that supports graphical windows.
"""
(base / "README.txt").write_text(readme, encoding="utf-8")

zip_path = Path("/mnt/data/dreamhouse_fashion_rescue_project.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in base.rglob("*"):
        zf.write(p, p.relative_to(base.parent))

print(f"Created project: {zip_path}")
print("Files:")
for p in sorted(base.rglob("*")):
    print(p.relative_to(base.parent))


