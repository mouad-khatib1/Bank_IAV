from unicodedata import name
from Data.database_handler import DatabaseHandler

database_handler = DatabaseHandler("stock.db")

def new_product(magasin):
    print("---nouveau produits---")
    name = input("nom : ")
    quantité = input("quantité : ")
    database_handler.new_product(name, quantité, magasin)
    print("produit ajouter")

def add_stok(magasin):
	print("---rajouter---")
	produit = input("produit : ")
	quantité = int(input("quantité : "))
	qt = database_handler.take_stock(produit, magasin)
	qt = int(qt)
	quantité += qt
	database_handler.mod_stock(produit, quantité, magasin)
	print(f"Le stock a bien été modifié, maintenant, il y a {quantité} {produit}")
	
def delete(magasin):
	print("---suprimer---")
	produit = input("produit : ")
	verif = input("press entrer pour confirmer sinon press une autre touche puis entrer")
	if verif == "":
		database_handler.delete(produit, magasin)
		print("Le produit a bien été suprimer")
	
def del_stock(magasin):
	print("---elever---")
	produit = input("produit : ")
	print("combien de produit (press entrer pour 1)")
	quantité = input(">>> ")
	if quantité == "":
		quantité = 1
	else:
		quantité = int(quantité)
	qt = database_handler.take_stock(produit, magasin)

	qt = int(qt)
	qt -= quantité
	database_handler.mod_stock(produit, qt, magasin)
	print(f"Le stock a bien été modifié, maintenant, il y a {qt} {produit}")


def menu_de_base(magasin):
	while True:
		print("-------------------------------------")
		print("Bienveenue sur le menu principale !")
		print("Choisissez une option")
		print("1. Nouveau produit")
		print("2. Rajouter du stok")
		print("3. Enlever du stock")
		print("4. Suprimer un produit")
		print("5. Se deconnecter")
		choix = int(input())

		if choix == 1:
			new_product(magasin)
		if choix == 2:
			add_stok(magasin)
		if choix == 3:
			del_stock(magasin)
		if choix == 4:
			delete(magasin)
		if choix == 5:
			print("---deconnection---")
			return

def main(magasin):
	try:
		menu_de_base(magasin)
	except KeyboardInterrupt:
		print("Fin du programme")
		quit()
	except ValueError:
		print("Enter un nombre")
		menu_de_base(magasin)

if __name__ == '__main__':
	main(magasin="magasin_1")