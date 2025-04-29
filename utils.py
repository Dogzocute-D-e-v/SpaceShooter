import os

SPECIAL_ABILITY_DURATION = 5  # seconds

def save_score(score):
    try:
        with open("score.txt", "w") as f:
            f.write(str(score))
    except Exception as e:
        print(f"Error saving score: {e}")

def load_score():
    if not os.path.exists("score.txt"):
        return 0
    try:
        with open("score.txt", "r") as f:
            return int(f.read())
    except Exception as e:
        print(f"Error loading score: {e}")
        return 0

def get_special_ability():
    return {
        "nuke": False,
        "shield": False,
        "rapid_fire": False,
        "active": None,
        "timer": 0
    }

def activate_ability(ability_state, name):
    ability_state["active"] = name
    ability_state["timer"] = SPECIAL_ABILITY_DURATION
    if name == "nuke":
        ability_state["nuke"] = True
    elif name == "shield":
        ability_state["shield"] = True
    elif name == "rapid_fire":
        ability_state["rapid_fire"] = True

def update_ability_timer(ability_state, dt):
    if ability_state["active"]:
        ability_state["timer"] -= dt
        if ability_state["timer"] <= 0:
            ability_state["nuke"] = False
            ability_state["shield"] = False
            ability_state["rapid_fire"] = False
            ability_state["active"] = None
            ability_state["timer"] = 0