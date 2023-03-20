import mysql.connector

class Produit:
    def __init__(self, hote, utilisateur, mdp, bdd):
        self.hote = hote
        self.utilisateur = utilisateur
        self.mdp = mdp
        self.bdd = bdd

    def connect(self):
        self.bd = mysql.connector.connect(
            host = self.hote,
            user = self.utilisateur,
            password = self.mdp,
            database = self.bdd
        )
        self.cursor = self.bd.cursor()

    def close(self):
        self.cursor.close()
        self.bd.close()

    def ajout(self, nom, description, prix, quantite, id_categorie):
        self.connect()
        ajout_req = f'insert into produit (nom, description, prix, quantite, id_categorie) \
            \nvalues ("{nom}", "{description}", {prix}, {quantite}, {id_categorie})'
       
        self.cursor.execute(ajout_req)
        self.bd.commit()
        self.close()

    def lecture(self):
        self.connect()
        lecture_req = f"select * from produit"
        self.cursor.execute(lecture_req)
        resultat = self.cursor.fetchall()
        self.close()
        return resultat

    def lectureCondition(self, condition):
        self.connect()
        if type(condition) == str:
            lecture_cond_req = f"select * from produit where {condition}"
            self.cursor.execute(lecture_cond_req)
            resultat = self.cursor.fetchall()
            self.close()
            return resultat
        else:
            print("Erreur, condition pas en str")

    def maj(self, champ, nouvelle_valeur, condition):
        self.connect()
        maj_req = f"update produit set {champ} = {nouvelle_valeur} where {condition}"
        self.cursor.execute(maj_req)
        self.bd.commit()
        self.close()

    def supr(self, condition):
        self.connect()
        if type(condition) == str:
            supr_req = f"delete from produit where {condition}"
            self.cursor.execute(supr_req)
            self.bd.commit()
            self.close()
            
        else:
            print("Le format de condition, n'est pas en str")
    
    def affich_categorie(self):
        self.connect()
        req = "SELECT c.nom \
                \nFROM produit p\
                \nINNER JOIN categorie c ON p.id_categorie = c.id \
                \nWHERE p.id = %s"
        self.cursor.execute(req)
        resultat = self.cursor.fetchone()[0]
        # print(resultat)
        self.close
        return resultat