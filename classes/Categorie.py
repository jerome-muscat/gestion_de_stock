import mysql.connector

class Categorie:
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

    def ajout(self, nom):
        self.connect()
        ajout_req = f'insert into categorie (nom) \
            \nvalues ("{nom}")'
       
        self.cursor.execute(ajout_req)
        self.bd.commit()
        self.close()

    def lecture(self):
        self.connect()
        lecture_req = f"select * from categorie"
        self.cursor.execute(lecture_req)
        resultat = self.cursor.fetchall()
        self.close()
        return resultat

    def lectureCondition(self, condition):
        self.connect()
        if type(condition) == str:
            lecture_cond_req = f"select nom from categorie where {condition}"
            self.cursor.execute(lecture_cond_req)
            resultat = self.cursor.fetchall()
            self.close()
            return resultat
        else:
            print("Erreur, condition pas en str")

    def lectureCondition_id(self, condition):
        self.connect()
        lecture_cond_req = f'select id from categorie where nom = "{condition}"'
        self.cursor.execute(lecture_cond_req)
        resultat = self.cursor.fetchone()[0]
        print(resultat)
        self.close()
        return resultat

    def maj(self, champ, nouvelle_valeur, condition):
        self.connect()
        if type(champ) != str:
            print("Le format du champ n'est pas en str")
        
        elif type(condition) != str:
            print("Le format de condition n'est pas en str")
        
        else:
            maj_req = f"update categorie set {champ} = {nouvelle_valeur} where {condition}"
            self.cursor.execute(maj_req)
            self.bd.commit()
            self.close()

    def supr(self, condition):
        self.connect()
        if type(condition) == str:
            supr_req = f"delete from categorie where {condition}"
            self.cursor.execute(supr_req)
            self.bd.commit()
            self.close()
            
        else:
            print("Le format de condition, n'est pas en str")