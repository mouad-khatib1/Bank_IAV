import mysql.connector
import os
from datetime import date


class DatabaseHandler():
    def __init__(self, database_name : str):
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="PasswordA77.",
            database=database_name
        )
        self.cur = self.con.cursor()

    def create_user(self, nom: str,prenom : str,username : str,email : str, password : str,role = "client"):
        query = "INSERT INTO utilisateur (nom,Prénom,user_name,Adresse_email, Mot_de_passe,role) VALUES (%s, %s,%s,%s,%s,%s)"
        self.cur.execute(query, (nom, prenom,username,email,password,role))
        self.con.commit()
    
    def create_account(self,type_compte,solde,user_id,rib): 
        query = "INSERT INTO compte (Type_de_compte,Solde,ID_utilisateur,RIB) VALUES (%s, %s,%s,%s)"
        self.cur.execute(query, (type_compte, solde,user_id,rib))
        self.con.commit()

    def get_password(self, username: str):
        query = "SELECT Mot_de_passe FROM utilisateur WHERE user_name = %s"
        self.cur.execute(query, (username,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_password_by_id(self, user_id: str):
        query = "SELECT Mot_de_passe FROM utilisateur WHERE ID_utilisateur = %s"
        self.cur.execute(query, (user_id,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def change_password(self, magasin: str, new_password):
        query = "UPDATE utilisateur SET password = %s, nbPasswordChange = nbPasswordChange + 1 WHERE magasin = %s"
        self.cur.execute(query, (new_password, magasin))
        self.con.commit()

    def get_id_user(self, username):
        query = "SELECT ID_utilisateur FROM utilisateur WHERE user_name = %s"
        self.cur.execute(query, (username,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def user_exist_whith(self, username: str):
        query = "SELECT * FROM utilisateur WHERE user_name = %s"
        self.cur.execute(query, (username,))
        result = self.cur.fetchone()
        return result is not None

    def take_id(self):
        query = 'SELECT MAX(ID_utilisateur) FROM utilisateur'
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def get_epargne(self, user_id: int):
        epargne = "épargne"
        query = "SELECT * FROM compte WHERE ID_utilisateur = %s and Type_de_compte= 'epargne' "
        self.cur.execute(query, (user_id,))
        result = self.cur.fetchone()
        return result 

    def get_chèque(self, user_id: int):
        query = "SELECT * FROM compte WHERE ID_utilisateur = %s and Type_de_compte= 'chèque' "
        self.cur.execute(query, (user_id,))
        result = self.cur.fetchone()
        return result 
  
    def get_user(self, user_id: int):
        query = "SELECT * FROM utilisateur WHERE ID_utilisateur = %s"
        self.cur.execute(query, (user_id,))
        result = self.cur.fetchone()
        return result
    def get_user_by_username(self, user_name: str):
        query = "SELECT * FROM utilisateur WHERE user_name = %s"
        self.cur.execute(query, (user_name,))
        result = self.cur.fetchone()
        if result is not None:
            return result  
        else:
            return None  


    def check_role(self, user_id):
        query = "SELECT role FROM utilisateur WHERE ID_utilisateur = %s"
        self.cur.execute(query, (user_id,))
        result = self.cur.fetchone()
        if result:
            return result[0]  
        else:
            return Non

    def get_beneficier(self,user_id):
        query = "SELECT * FROM beneficiary WHERE user_id = %s "
        self.cur.execute(query, (user_id,))
        result = self.cur.fetchall()
        return result
    
    def get_account_id(self,user_id):
        query = "SELECT ID_compte FROM compte WHERE ID_utilisateur = %s and Type_de_compte ='chèque'"
        self.cur.execute(query, (user_id,))
        result = self.cur.fetchone() 
        if result is not None:
            return int(result[0]) 
        else:
            return None


    def verif_solde(self, user_id, montant):
        query = "SELECT Solde FROM compte WHERE ID_utilisateur = %s and Type_de_compte ='chèque'"
        self.cur.execute(query, (user_id,))
        result = self.cur.fetchone() 
        if result:
            solde = result[0] 
            return solde > montant
        else:
            return False

    def increment_solde(self, account_id, montant):
        query = "UPDATE compte SET Solde = Solde + %s WHERE ID_compte = %s and Type_de_compte = 'chèque'"
        try:
            self.cur.execute(query, (montant, account_id))
            self.con.commit()
            if self.cur.rowcount > 0:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print("Error:", err)
            return False

    def decrement_solde(self, user_id, montant):
        query = "UPDATE compte SET Solde = Solde - %s WHERE ID_utilisateur = %s and Type_de_compte = 'chèque'"
        try:
            self.cur.execute(query, (montant, user_id))
            self.con.commit()
            if self.cur.rowcount > 0:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print("Error:", err)
            return False
    
    def ajouter_transaction(self,type_transaction,montant,id_emeteur,id_recepteur):
        try:
            query = "INSERT INTO transaction (Type_transaction,Montant,Date_transaction,ID_compte_emeteur, ID_compte_recepteur) VALUES (%s, %s,%s,%s,%s)"
            today_date_string = date.today().strftime('%Y-%m-%d')
            self.cur.execute(query, (type_transaction, montant,today_date_string,id_emeteur,id_recepteur))
            self.con.commit()
            print("Transaction added successfully!")
        except Exception as e:
            print("An error occurred:", e)

    def get_taux_interet(self):
        query = "SELECT * FROM taux_interet"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def get_clients(self):
        query = "select * FROM utilisateur"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def get_transaction(self):
        query = "select * FROM transaction"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result       




