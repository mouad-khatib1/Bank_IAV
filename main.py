from Data.database_handler_MySql import DatabaseHandler
from getpass import getpass
import gestion

database_handler = DatabaseHandler("bank_iav_db")

def register():
	print("---Register---")
	nom = input("nom : ")
	prenom = input("prenom : ")
	username = input("Username : ")
	email = input("email : ")
	password = input("Password : ")

	database_handler.create_user(nom,prenom,username,email, password)
	menu_connected(username)

def login():
	print("---login---")
	username = input("Username : ")
	password = input("Password : ")

	if database_handler.user_exist_whith(username) and database_handler.get_password(username) == password:
		print("login")
		menu_connected(username)
	else:
		print("Nom d'utilisateur / Mot de passe incorect")


def changer_mdp(username: str):
	new_password = input("Veillez entre le nouveau mot de passe : ")
	new_password_confirmed = input("Veillez confirmer votre mot de passe : ")

	if new_password == new_password_confirmed:
		database_handler.change_password(username, new_password)
		print("Votre mot de passe a bien été modifié")
	else:
		print("Les mots de passe ne corresponde pas")

def menu_connected(username: str):
	print("*************Bienvenu a votre compte bancaire*******************************")
	id = database_handler.get_id_user(username)
	gestion.main(id)

def menu_not_connected():
	while True:
		print("Bienveenue sur le espace Bank_IAV, veuiller vous connecter")
		print("Choisissez une option")
		print("1. Login")
		print("2. S'enregistrer")
		choix = int(input())
		if choix == 1:
			login()
		if choix == 2:
			register()

def main():
	try:
		menu_not_connected()
	except KeyboardInterrupt:
		print("Fin du programme")
		quit()
	except ValueError:
		print("Enter un nombre")
		menu_not_connected()


main()