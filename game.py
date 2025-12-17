# game.py

# --- The Game State ---
# We use a dictionary to store information about the player.
# This is a simple way to keep track of variables.
player_state = {
    "current_room": "start",
    "has_key": False,
    "has_sword": False  # NEW: Track if the player has the sword
}

# --- The Game World ---
# A dictionary to represent the rooms in our game.
# Each room has a description and exits (choices).
rooms = {
    "start": {
        "description": "You are in a dimly lit room. There is a wooden door to your right and a dark hallway ahead.",
        "exits": {
            "right": "locked_room",
            "ahead": "monster_room"
        }
    },
    "locked_room": {
        # NEW: Updated description to mention the sword.
        "description": "You are in a small study. A heavy, iron-bound door is locked. On the desk, you see a shiny key. Hanging on the wall is a rusty sword.",
        "exits": {
            "back": "start"
        }
    },
    "monster_room": {
        # NEW: Updated description to hint at a solution.
        "description": "A giant, sleepy monster blocks the path! It looks like it might wake up if you get closer. There seems to be a path behind it.",
        "exits": {
            "back": "start",
            "forward": "garden" # NEW: A new exit is revealed
        }
    },
    # NEW: A new room to discover!
    "garden": {
        "description": "You've found a secret garden! It's beautiful. At the center is a fountain with a treasure chest inside.",
        "exits": {
            "back": "monster_room",
            "open": "treasure_room" # The goal is now here
        }
    },
    "treasure_room": {
        "description": "You've found the treasure room! Gold and jewels are piled everywhere. You win!",
        "exits": {} # No exits, it's the end of the game
    }
}

# --- Game Functions ---
def show_room():
    """Displays the current room's description and available exits."""
    current_room_data = rooms[player_state["current_room"]]
    print("\n" + "="*40)
    print(current_room_data["description"])
    
    # Show the player their inventory
    print("\n--- Inventory ---")
    if player_state["has_key"]:
        print("- a shiny key")
    if player_state["has_sword"]:
        print("- a rusty sword")
    if not player_state["has_key"] and not player_state["has_sword"]:
        print("- empty")
    print("------------------")
    
    # Show the player their options
    exits = list(current_room_data["exits"].keys())
    if exits:
        print("You can go:", " or ".join(exits))
    else:
        print("There are no exits.")
    print("You can also type 'quit' to exit the game.") # NEW: Added quit hint

def handle_choice(choice):
    """Processes the player's choice and updates the game state."""
    current_room_data = rooms[player_state["current_room"]]
    
    # NEW: Handle the quit command
    if choice == "quit":
        print("Thanks for playing!")
        exit() # This command stops the program

    # Check if the choice is a valid exit
    if choice in current_room_data["exits"]:
        next_room = current_room_data["exits"][choice]
        
        # Special logic for the monster room
        if player_state["current_room"] == "monster_room" and choice == "forward":
            if player_state["has_sword"]:
                print("You bravely hold up the sword. The monster sees it, whimpers, and scurries away, clearing the path!")
            else:
                print("The monster roars and blocks your way! You cannot get past without something to defend yourself.")
                return # Stop here, don't change rooms

        # Special logic for the treasure room
        if next_room == "treasure_room" and not player_state["has_key"]:
            print("The treasure chest is locked. You need a key.")
            return # Stop here, don't change rooms

        # Special logic for getting the sword and key
        if player_state["current_room"] == "locked_room":
            if not player_state["has_sword"]:
                print("You take the rusty sword from the wall.")
                player_state["has_sword"] = True
            if not player_state["has_key"]:
                print("You pick up the shiny key from the desk.")
                player_state["has_key"] = True

        player_state["current_room"] = next_room
    else:
        print("Invalid choice. Please try again.")

# --- The Main Game Loop ---
def main_game_loop():
    """The main loop that runs the game."""
    print("Welcome to the Text Adventure!")
    
    while player_state["current_room"] != "treasure_room":
        show_room()
        
        # Get input from the player
        player_choice = input("> ").lower().strip() # .lower() makes it case-insensitive, .strip() removes extra spaces
        
        handle_choice(player_choice)
    
    # Game Over message
    show_room() # Show the final treasure room description
    print("\n*** Congratulations! You've completed the adventure! ***")

# --- Start the Game ---
if __name__ == "__main__":
    main_game_loop()