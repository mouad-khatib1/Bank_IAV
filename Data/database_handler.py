import os
import sqlite3
from unittest import result

class DatabaseHandler():
	def __init__(self, database_name : str):
		self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
		self.con.row_factory = sqlite3.Row

	def new_product(self, produit: str, quantité: str, magasin):
		cursor = self.con.cursor()
		query = f"INSERT INTO {magasin} (produit, quantité) VALUES (?, ?);"
		cursor.execute(query, (produit, quantité,))
		cursor.close()
		self.con.commit()

	def take_stock(self, produit, magasin):
		cursor = self.con.cursor()
		query = f"SELECT quantité FROM {magasin} WHERE produit = ?;"
		cursor.execute(query, (produit,))
		result = cursor.fetchall()
		cursor.close
		return dict(result[0])["quantité"]

	def mod_stock(self, produit: str, quantité : int, magasin):
		cursor = self.con.cursor()
		query = f"UPDATE {magasin} SET quantité = ? WHERE produit = ?;"
		cursor.execute(query, (quantité, produit))
		cursor.close()
		self.con.commit()

	def delete(self, produit, magasin):
		cursor = self.con.cursor()
		query = f"DELETE FROM {magasin} WHERE produit = ?;"
		cursor.execute(query, (produit,))
		cursor.close
		self.con.commit()

	def create_person(self, magasin: str, password: str):
		cursor = self.con.cursor()
		query = f"INSERT INTO Person (magasin, password) VALUES (?, ?);"
		cursor.execute(query, (magasin, password,))
		cursor.close()
		self.con.commit()

	def password_for(self, magasin : str):
		cursor = self.con.cursor()
		query = f"SELECT password FROM Person WHERE magasin = ?;"
		cursor.execute(query, (magasin,))
		result = cursor.fetchall()
		cursor.close
		return dict(result[0])["password"]
	
	def change_password(self, magasin: str, new_password):
		cursor = self.con.cursor()
		query = f"UPDATE Person SET password = ?, nbPasswordChange = nbPasswordChange + 1 WHERE magasin = ?;"
		cursor.execute(query, (new_password, magasin))
		cursor.close()
		self.con.commit()

	def take_id_mag(self, magasin):
		cursor = self.con.cursor()
		query = f"SELECT id FROM Person WHERE magasin = ?;"
		cursor.execute(query, (magasin,))
		result = cursor.fetchall()
		cursor.close
		return dict(result[0])["id"]

	def user_exist_whith(self, magasin: str):
		cursor = self.con.cursor()
		query = f"SELECT * FROM Person WHERE magasin = ?;"
		cursor.execute(query, (magasin,))
		result = cursor.fetchall()
		cursor.close()
		return len(result) == 1

	def create_table(self, magasin):
		cursor = self.con.cursor()
		query = f'''CREATE TABLE {magasin} (
    				produit STRING UNIQUE
                  				   NOT NULL,
    				quantité INTEGER NOT NULL
                   				   DEFAULT (1) 
				);'''
		cursor.execute(query)
		self.con.commit()

	def take_id(self):
		cursor = self.con.cursor()
		query = f'SELECT MAX(id) FROM Person;'
		cursor.execute(query)
		result = list(map(dict, cursor.fetchall()))
		cursor.close()
		return result