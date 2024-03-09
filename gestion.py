from unicodedata import name
from Data.database_handler_MySql import DatabaseHandler

database_handler = DatabaseHandler("bank_iav_db")

def consulter_information(user_id):
    print("--- Votre Information Personnel ---")
    user = database_handler.get_user(user_id)
    if user:
        id,nom, prenom, username, email, password ,role= user
        print(f"Nom: {nom}")
        print(f"Prénom: {prenom}")
        print(f"Nom d'utilisateur: {username}")
        print(f"Email: {email}")
        print(f"role: {role}") 
    menu_de_base(user_id)

def consulter_solde(user_id):
	print("-------------------------------------")
	print("Choisissez le compte")
	print("1. Compte épargne")
	print("2. Compte chèque")
	choix = int(input())
	if choix == 1:
		éparne = database_handler.get_epargne(user_id)
		if éparne:		
			id_compte, type, solde, id_user ,rib= éparne
			print(f"type: {type}")
			print(f"RIB : {rib}")
			print(f"solde: {solde} Dh")

	if choix == 2:
		database_handler.get_chèque(user_id)
		chèque = database_handler.get_chèque(user_id)
		if chèque:		
			id_compte, type, solde, id_user ,rib= chèque
			print(f"type: {type}")
			print(f"RIB : {rib}")
			print(f"solde:{solde} Dh")
	menu_de_base(user_id)

def afficher_beneficier(user_id):
	print("---afficher les beneficier---")
	beneficiers = database_handler.get_beneficier(user_id)
	for beneficiary in beneficiers:
	    beneficiary_id, name, email, phone,rib,user_Id,account_id = beneficiary
	    print("Name:", name)
	    print("Email:", email)
	    print("Phone:", phone)
	    print("rib:", rib)
	    print("------------------------------------")

def effectuer_virement(user_id):
	print("-------------------------------------")
	print("Choisir un beneficier !")
	beneficiers = database_handler.get_beneficier(user_id)
	i = 0
	for beneficier in beneficiers:
		beneficiary_id, name, email, phone,rib,user_Id,account_id = beneficier
		print(i+1,"- beneficier :", i+1, name)
		i+=1
	choix = int(input())
	montant = int(input("entre le montant : "))
	accountid_recepteur = beneficiers[choix-1][6]
	accountid_emeteur =  database_handler.get_account_id(user_id)
	is_solde_sufisant = database_handler.verif_solde(user_Id,montant)
	if is_solde_sufisant :
		i = 3
		while (i>0):
			password = input("entre le mot de passe : ")
			if database_handler.get_password_by_id(user_id) == password: 
				is_incremented =database_handler.increment_solde(accountid_recepteur,montant)
				is_decremented = database_handler.decrement_solde(user_id,montant)
				#add to transactions 
				if is_incremented and is_decremented:
					type_transaction = "virement"
					database_handler.ajouter_transaction(type_transaction,montant,accountid_emeteur,accountid_recepteur)
					print("**********Le virement a été bien effectuer****************")
					break
			else:
				print("mot de pass incorrect , il vous rest ", i-1 , "tentative")
				i-=1
	else :
		print("ce montant ",montant," est plus grand de votre solde ")
	menu_de_base(user_id)

def taux_interet():
	tauxs = database_handler.get_taux_interet()
	for taux in tauxs:
	    id, type_compte, taux1 = taux
	    print(type_compte , " : ",taux1)
	    print("------------------------------------")

def affiche_clients():
	print("---afficher les beneficier---")
	clients = database_handler.get_clients()
	i = 1 
	for client in clients:
	    id, name, prename, user_name,email,password,role = client
	    print(i,". client_",i)
	    print("Name : ", name)
	    print("prename : ", prename)
	    print("Username : ", user_name)
	    print("Email : ", email)
	    print("password : ", password)
	    print("role : ", role) 
	    print("------------------------------------")
	    print("")
	    i+=1
	choix = int(input("choisir un client : "))
	if(choix <= i):
		userid = clients[choix-1][0]
		cheque = database_handler.get_chèque(userid)
		epargne = database_handler.get_epargne(userid)
		id_compte, type, solde, id_user ,rib= epargne
		print(f"type: {type}")
		print(f"RIB : {rib}")
		print(f"solde: {solde} Dh")
		print("------------------------------------")
		id_compte1, type1, solde1, id_user1 ,rib1= cheque
		print(f"type: {type1}")
		print(f"RIB : {rib1}")
		print(f"solde: {solde1} Dh")
		return
	else : 
		print("utilisateur introuvable ")
		return 

def rechercher_client():
	print("-------------------------------------")
	username = input("rechercher par username  : ")
	user = database_handler.get_user_by_username(username)
	if user is not None : 
		id, name, prename, user_name,email,password,role = user
		print("Name : ", name)
		print("prename : ", prename)
		print("Username : ", user_name)
		print("Email : ", email)
		print("password : ", password)
		print("role : ", role) 
		print("------------------------------------")
		return
	else : 
		print("username introuvable")
		rechercher_client()

def ajouter_client():
	print("----------------creation d'utilisateur ---------------------")
	nom = input("nom : ")
	prenom = input("prenom : ")
	username = input("Username : ")
	email = input("email : ")
	password = input("Password : ")
	database_handler.create_user(nom,prenom,username,email, password)
	user_id = database_handler.get_id_user(username)
	print("------------------creation de compte -------------------")
	print("1. compte epargne")
	print("2. compte chéque")
	choix = input("choisir type de compte : ")
	solde = int(input("solde : "))
	rib = input("RIB : ")
	if choix == 1 : 
		type_compte = "épargne"
	elif choix == 2 :
		type_compte = "chèque"
	else : 
		return
	database_handler.create_account(type_compte,solde,userid,rib)

def afficher_transaction():
	transactions = database_handler.get_transaction()
	print("transaction")
	print("ID | Type Transaction | Montant | Date Transaction | ID Compte Emetteur | ID Compte Recepteur")
	print("-" * 100)
	for row in transactions:
	    print("{:<3}| {:<17}| {:<8}| {:<17}| {:<19}| {:<19}".format(*row))
	    print("-" * 100)

	print("")
	print("")
	return 



def menu_de_base(user_id):
	while True:
	    role = database_handler.check_role(user_id)
	    if role == "admin":
		    print("-------------------------------------")
		    print("Bienveenue sur le espace admin !")
		    print("Choisissez une option")
		    print("1. Afficher tous les client")
		    print("2. rechercher un client")
		    print("3. ajouter client")
		    print("4. afficher transactions")
		    print("5. deconnecter")
		    choix = int(input())
		    if choix == 1:
		        affiche_clients()
		    elif choix == 2:
		    	rechercher_client()
		    elif choix == 3:
			    ajouter_client() 
		    elif choix == 4:
			    afficher_transaction()
		    elif choix == 5:
		    	print("---deconnection---")
		    	return
		
	    elif role == "client":
		    print("-------------------------------------")
		    print("Bienveenue sur le menu principale !")
		    print("Choisissez une option")
		    print("1. consulter_information")
		    print("2. consulter solde")
		    print("3. afficher beneficier")
		    print("4. effectuer un virement")
		    print("5. taux d'interets")
		    print("6. deconnecter")
		    choix = int(input())
		    if choix == 1:
		        consulter_information(user_id)
		    elif choix == 2:
		    	consulter_solde(user_id)
		    elif choix == 3:
			    afficher_beneficier(user_id) 
		    elif choix == 4:
		        effectuer_virement(user_id)
		    elif choix == 5:
		        taux_interet() 
		    elif choix == 6:
		    	print("---deconnection---")
		    return
	    else:
	        print("Rôle utilisateur non reconnu.")
	        return

def main(user_id):
	try:
		menu_de_base(user_id)
	except KeyboardInterrupt:
		print("Fin du programme")
		quit()
	except ValueError:
		print("Enter un nombre")
		menu_de_base(user_id)

# if __name__ == '__main__':
# 	main(magasin="magasin_1")