import os


user_accounts = {}

admin_username = "admin"
admin_password = "adminpass"

game_library = {

    "Donkey Kong": {"quantity": 3, "cost": 2},

    "Super Mario Bros": {"quantity": 5, "cost": 3},

    "Tetris": {"quantity": 2, "cost": 1},

    # Add more games as needed

}


#number of spaces between panels
#i wanted to use a clear screen but i was afraid it might cause issues on a different device
spaces = 10

#specialized input handling function
def GetInput(max, message="Enter choice (leave blank to cancel): ", min=1):
	while True:
		try:
			choice = int(input(message))
			
			if choice < min or choice > max:
				input("Out of bounds.")
				return 0
				
			return choice
			
		except ValueError:
			return "error"
			
#for vertical spacing
def Spaces(amount, clear=True):
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')



#for panel headers
def Header(message):
	print("-----", end="")
	print(message, end="")
	print("-----")

#entry creation in account dictionary
def CreateAccount(name, password, balance, points):
	user_accounts[name] = {"name": name, "pw": password, "balance": balance, "points": points, "games": []}


#returns true if the credentials are matching and correct
def check_credentials(username, password):
	try:
		if user_accounts[username]["pw"] == password:
			return True
			
		else:
			input("Password entered is incorrect.\nPress Enter to continue.")
			return False
			
	except KeyError:
		input("Username not found.\nPress Enter to continue.")
		return False

def Login():
	while True:
		Spaces(spaces)
		Header("Log in")
		username = input("Username: ")
		pw = input("Password: ")
		
		if check_credentials(username, pw):
			input("Successfully logged in!\nPress Enter to continue.")
			logged_in_menu(username)
			return
			
		else:
			return
			
			
def display_available_games():
	Spaces(spaces)
	Header("Available Games")	
	for game in game_library:
		print(f"- {game}")
		print(f"   Copies: {game_library[game]['quantity']}")
		print(f"   Price: ${game_library[game]['cost']}\n")	
		
	input("")


def rent_game(username):
	Spaces(spaces)
	Header("Rent Game")
	for game in game_library:
		print(f"- {game}")
		
	select = input("\nEnter the name of the game you want to rent: ")
	
	if select in game_library:
		
		if game_library[select]['quantity'] <= 0:
			input("This game currently has no available copies.\nPlease ask the administrator to upload more copies or wait for\nrented copies to be returned.\nPress Enter to continue.")
			return
		
		Spaces(spaces)
		Header(select)
		print(f"Copies: {game_library[select]['quantity']}")
		print(f"Price: ${game_library[select]['cost']}\n")
		
		print("1 Rent")
		print("2 Redeem")
		
		choice = GetInput(2)
		
		if choice == "error":
			input("Operation cancelled.\nPress Enter to continue.")
			return
			
		if choice == 1:
			if user_accounts[username]['balance'] >= game_library[select]['cost']:
				user_accounts[username]['balance'] -= game_library[select]['cost']
				point = int(game_library[select]['cost']/2)
				user_accounts[username]['points'] += point 
				user_accounts[username]['games'].append(select)
				game_library[select]['quantity'] -= 1
				input(f"Game rented. You gained {point} points from this transaction.\nPress Enter to continue.")
			else:
				input("Not enough balance.\nPress Enter to continue.")
		if choice == 2:
			if user_accounts[username]['points'] >= 3:
				user_accounts[username]['games'].append(select)
				game_library[select]['quantity'] -= 1
				user_accounts[username]['points']-=3
				input(f"Game redeemed. Thank you for your patronage!\nPress Enter to continue.")
			else:
				input("Not enough points.\nPress Enter to continue.")
	else:
		input("Game not found.\nPress Enter to continue.")


def top_up_account(username):
	Spaces(spaces)
	Header("Top Up")
	amount = GetInput(9999999, "Enter the amount you wish to top up: ")
	
	if amount == "error":
		input("Invalid input.\nPress Enter to continue.")
		return
	
	if amount == 0:
		return
	
	user_accounts[username]['balance'] += amount
	input(f"Successfully topped up ${amount}!\nPress Enter to continue.")

def display_inventory(username):
	Spaces(spaces)
	Header("Balance and Points")
	print(f"Balance: ${user_accounts[username]['balance']}")
	print(f"Points:  {user_accounts[username]['points']}")
	input("\nPress Enter to continue...")

def display_games_inventory(username):
	Spaces(spaces)
	Header("Rented Games")
	
	if len(user_accounts[username]['games']) <= 0:
		input("No rented games.\nPress Enter to continue.")
		
	else:	
		for game in user_accounts[username]['games']:
			print(f"- {game}")
			
		input("Press Enter to continue.")


def return_game(username):
	Spaces(spaces)
	Header("Return Game")
	if len(user_accounts[username]['games']) <= 0:
		input("No rented games.\nPress Enter to continue.")
		
	else:	
		for game in user_accounts[username]['games']:
			print(f"- {game}")
			
		select = input("Enter the name of the game you want to return: ")
		
		if select in user_accounts[username]['games']:
			user_accounts[username]['games'].remove(select)
			game_library[select]['quantity'] += 1
			input("Game returned.\nPress Enter to continue.")
			
		else:
			input("Game not found.\nPress Enter to continue.")
			

def logged_in_menu(username):
	while True:
		Spaces(spaces)
		Header("User Menu")
		print("1 View All Games")
		print("2 Rent Games")
		print("3 Return Games")
		print("4 Points and Balance")
		print("5 View Rented Games")
		print("6 Top Up")
		print("7 Log Out")
		
		choice = GetInput(7, "Enter choice: ")
		
		if choice == "error":
			input("Invalid input.\nPress Enter to continue.")
			continue
			
		if choice == 1:
			display_available_games()
			
		if choice == 2:
			rent_game(username)
			
		if choice == 3:
			return_game(username)
			
		if choice == 4:
			display_inventory(username)
			
		if choice == 5:
			display_games_inventory(username)
			
		if choice == 6:
			top_up_account(username)
			
		if choice == 7:
			input("Logging out...")
			return

def EditGame():
	Spaces(spaces)
	Header("Edit Game")
	
	name = input("Game title: ")
	
	if name in game_library:
		price = GetInput(9999999, "New price: ", 0)
		if price == "error":
			input("Invalid input.\nPress Enter to continue.")
			return
		game_library[name]['cost'] = price
		
		copies = GetInput(9999999, "New amount: ", 0)
		if copies == "error":
			input("Invalid input.\nPress Enter to continue.")
			return
		game_library[name]['quantity'] = copies
		input("Game updated!\nPress Enter to continue.")
		

def AddGame():
	Spaces(spaces)
	Header("Add Game")
	name = input("Game title: ")
	
	if name in game_library:
		input("Game already exists.\nPress Enter to continue.")
		return
	
	price = GetInput(9999999, "Price: ")
	if price == "error":
		input("Invalid input.\nPress Enter to continue.")
		return
	
	copies = GetInput(9999999, "Copies: ")
	if copies == "error":
		input("Invalid input.\nPress Enter to continue.")
		return
	
	game_library[name] = {'quantity': copies, 'cost': price}

	input("Game added to library.\nPress Enter to continue.")
	
	

def admin_menu():
	while True:
		Spaces(spaces)
		Header("Admin Menu")
		
		print("1 Add Game")
		print("2 Edit Game Details")
		print("3 View Games")
		print("4 Log Out\n")
		
		choice = GetInput(4, "Enter choice: ")
			
		if choice == "error":
			input("Invalid input.\nPress Enter to continue.")
				
		if choice == 1:
			AddGame()
				
		if choice == 2:
			EditGame()
			
		if choice == 3:
			display_available_games()
			
		if choice == 4:
			input("Logging you out, Administrator.\nPress Enter to continue.")
			return

def admin_login():
	Spaces(spaces)
	Header("Admin Login")
	name = input("Username: ")
	pw = input("Password: ")
	
	if name == admin_username and pw == admin_password:
		input("\nWelcome, Administrator!\nPress Enter to continue.")
		admin_menu()
		
	else:
		input("The credentials you entered are incorrect.\nPress Enter to continue.")

def register_user():
	while True:
		Spaces(spaces)
		Header("Sign up")
		username = input("Username: ")
		
		if username in user_accounts:
			input("Username is taken.\nPress Enter to continue.")
			continue
			
		pw = input("Password: ")
		input("Account created!\nPress Enter to continue.")
		CreateAccount(username, pw, 0, 0)
		return
			

def main():
	while True:

		Header("Main Menu")
		print("1 Sign up")
		print("2 Log in")
		print("3 Log in as Administrator\n")
		
		choice = GetInput(3)
		
		if choice == "error":
			print("Exiting...")
			return
			
		if choice == 1:
			register_user()
			
		if choice == 2:
			Login()
			
		if choice == 3:
			admin_login()
			
		
		Spaces(spaces)




if __name__ == "__main__":

	main()