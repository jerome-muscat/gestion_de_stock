import tkinter as tk
import tkinter.ttk as ttk
from Categorie import *
from Produit import *
import tkinter.messagebox as messagebox

root = tk.Tk()
root.geometry("1000x700")
root.title("Gestion de stock")
categorie = Categorie('localhost', 'root', 'root', 'boutique')
produit = Produit('localhost', 'root', 'root', 'boutique')

resultat = produit.lecture()

def affich_nom(resultat, treeview, produit):
    for row in resultat:
        req = f"id = {row[5]}"

        categorie = produit.lectureCondition(req)
        nom_categorie = ""
        for lettre in str(categorie):
            if lettre not in "(),'{[]}":
                nom_categorie += lettre
        treeview.insert('', 'end', text=row[0], values=(row[1], row[2], nom_categorie, row[3], row[4], "Modifier", "Effacer"))

def clique_colonne_produit(event):
    region = treeview.identify_region(event.x, event.y)
    if region == "cell":
        item_id = treeview.identify_row(event.y)
        column_id = treeview.identify_column(event.x)

        if column_id == "#6":
            # Clic sur la colonne "modifier"
            modifier_produit(item_id)
            
        elif column_id == "#7":
            # Clic sur la colonne "effacer"
            effacer_produit(item_id)

def validation(item_id, name_entry, description_entry, price_entry, quantity_entry, modif_window):
    reponse = messagebox.askyesno("Modifier", "Voulez-vous vraiment modifier ce produit ?")
    if reponse:        
        id_produit = treeview.item(item_id, "text")
        values = [
                name_entry.get(),
                description_entry.get('1.0', 'end-1c'),
                treeview.item(item_id, "values")[2],
                price_entry.get(),
                quantity_entry.get(),
                "Modifier",
                "Effacer"
            ]
        verif = False

        try:    
            produit.maj("nom", f'"{values[0]}"', f"id = {id_produit}")
            produit.maj("description", f'"{values[1]}"', f"id = {id_produit}")
            produit.maj("prix", values[3], f"id = {id_produit}")
            produit.maj("quantite", values[4], f"id = {id_produit}")
            messagebox.showinfo("Etat modification", "Modification effectuée avec succès !")
            verif = True
            
        except:
            messagebox.showinfo("Etat modification", "Modification echouée !") 
        
        if verif:
            treeview.item(item_id, values=values)
            modif_window.destroy()

def ajout_valid(name_entry, description_entry, categorie_entry, price_entry, quantity_entry, modif_window):
    reponse = messagebox.askyesno("Ajout", "Voulez-vous vraiment ajouter ce produit ?")
    if reponse:
        values = [
                name_entry.get(),
                description_entry.get('1.0', 'end-1c'),
                categorie_entry.get(),
                price_entry.get(),
                quantity_entry.get(),
                "Modifier",
                "Effacer"
            ]
        
        verif = False

        id_category = categorie.lectureCondition_id(values[2])

        try:
            produit.ajout(values[0], values[1], values[3], values[4], id_category)
            messagebox.showinfo("Etat ajout", "Ajout effectué avec succès !")
            verif = True
            
        except:
            messagebox.showinfo("Etat ajout", "Ajout echoué !")
        
        if verif:
            treeview.insert("", "end", values=values)
            modif_window.destroy()

def modifier_produit(item_id):
    modif_window = tk.Toplevel(root)
    modif_window.title("Modifier la ligne")
    modif_window.geometry("800x400")

    name_label = tk.Label(modif_window, text="Entrez le nom du produit:")
    description_label = tk.Label(modif_window, text="Entrez la description du produit:")
    price_label = tk.Label(modif_window, text="Entrez le prix du produit:")
    quantity_label = tk.Label(modif_window, text="Entrez la quantité du produit:")

    name_var = tk.StringVar(value=treeview.item(item_id, "values")[0])
    description_var = tk.StringVar(value=treeview.item(item_id, "values")[1])
    price_var = tk.StringVar(value=treeview.item(item_id, "values")[3])
    quantity_var = tk.StringVar(value=treeview.item(item_id, "values")[4])

    name_entry = tk.Entry(modif_window, textvariable=name_var, width=100)
    description_entry = tk.Text(modif_window, height=5, width=90)
    description_entry.insert(tk.END, description_var.get())
    price_entry = tk.Entry(modif_window, textvariable=price_var, width=100)
    quantity_entry = tk.Entry(modif_window, textvariable=quantity_var, width=100)

    name_label.pack()
    name_entry.pack()

    description_label.pack()
    description_entry.pack()

    price_label.pack()
    price_entry.pack()
    
    quantity_label.pack()
    quantity_entry.pack()
    
    valider_button = tk.Button(modif_window, text="Valider", command= lambda: validation(item_id, name_entry, description_entry, price_entry, quantity_entry, modif_window))
    valider_button.pack()

def effacer_produit(item_id):
    reponse = messagebox.askyesno("Effacer", "Voulez-vous vraiment effacer cet enregistrement ?")
    if reponse:
        id_produit = treeview.item(item_id, "text")
        verif = False

        try:
            produit.supr(f"id = {id_produit}")
            messagebox.showinfo("Etat suppression", "Suppression effectuée avec succès !")
            verif = True

        except:
            messagebox.showinfo("Etat suppression", "Suppression echouée !")
            
        if verif:
            treeview.delete(item_id)

def ajout():
    modif_window = tk.Toplevel(root)
    modif_window.title("Modifier la ligne")
    modif_window.geometry("800x400")
    
    name_label = tk.Label(modif_window, text="Entrez le nom du produit:")
    description_label = tk.Label(modif_window, text="Entrez la description du produit:")
    categorie_label = tk.Label(modif_window, text="Entrez la catégorie du produit:")
    price_label = tk.Label(modif_window, text="Entrez le prix du produit:")
    quantity_label = tk.Label(modif_window, text="Entrez la quantité du produit:")

    name_entry = tk.Entry(modif_window, width=100)
    description_entry = tk.Text(modif_window, height=5, width=90)
    categorie_entry = tk.Entry(modif_window, width=100)
    price_entry = tk.Entry(modif_window, width=100)
    quantity_entry = tk.Entry(modif_window, width=100)

    name_label.pack()
    name_entry.pack()

    description_label.pack()
    description_entry.pack()

    categorie_label.pack()
    categorie_entry.pack()

    price_label.pack()
    price_entry.pack()
    
    quantity_label.pack()
    quantity_entry.pack()
        
    valider_button = tk.Button(modif_window, text="Valider", command=lambda: ajout_valid(name_entry, description_entry, categorie_entry, price_entry, quantity_entry, modif_window))
    valider_button.pack()  

def validation_modif_categorie(item_id, name_entry, modif_window):
    reponse = messagebox.askyesno("Modifier", "Voulez-vous vraiment modifier ce produit ?")
    if reponse:
        values = [
                name_entry.get(),
                "Modifier",
                "Effacer"
            ]
        id_categorie = treeview_categorie.item(item_id, "text")
        verif = False

        try:
            categorie.maj("nom", f'"{values[0]}"', f"id = {id_categorie}")
            messagebox.showinfo("Etat modification", "Modification effectuée avec succès !")
            
            verif = True
                     
        except:
            messagebox.showinfo("Etat modification", "Modification echouée !") 

        if verif:
            modif_window.destroy()
            treeview_categorie.item(item_id, values=values)   

def modifier_categorie(item_id):
    modif_window = tk.Toplevel(root)
    modif_window.title("Modifier la ligne")
    modif_window.geometry("800x400")

    name_label = tk.Label(modif_window, text="Entrez le nom du produit:")

    name_var = tk.StringVar(value=treeview_categorie.item(item_id, "values")[0])

    name_entry = tk.Entry(modif_window, textvariable=name_var, width=100)

    name_label.pack()
    name_entry.pack()
        
    valider_button = tk.Button(modif_window, text="Valider", command=lambda: validation_modif_categorie(item_id, name_entry, modif_window))
    valider_button.pack()

def effacer_categorie(item_id):
    reponse = messagebox.askyesno("Effacer", "Voulez-vous vraiment effacer cet enregistrement ?")
    if reponse:
        
        id_categorie = treeview_categorie.item(item_id, "text")

        try:
            produit.supr(f"id_categorie = {id_categorie}")
            categorie.supr(f"id = {id_categorie}")
            messagebox.showinfo("Etat suppression", "Suppression effectuée avec succès !")
            treeview_categorie.delete(item_id)

        except:
            messagebox.showinfo("Etat suppression", "Suppression echouée !")

def clique_colonne_categorie(event):
    region = treeview_categorie.identify_region(event.x, event.y)
    if region == "cell":
        item_id = treeview_categorie.identify_row(event.y)
        column_id = treeview_categorie.identify_column(event.x)

        if column_id == "#2":
            # Clic sur la colonne "modifier"
            modifier_categorie(item_id)

        elif column_id == "#3":
            # Clic sur la colonne "effacer"
            effacer_categorie(item_id)

def ajout_categorie(categorie):
    global treeview_categorie
    modif_window = tk.Toplevel(root)
    modif_window.title("Modifier la ligne")
    modif_window.geometry("800x400")

    categorie = categorie.lecture()

    treeview_categorie = ttk.Treeview(modif_window, height=len(categorie))
    treeview_categorie.pack()
    treeview_categorie['columns'] = ('name', 'modifier', 'effacer')
    treeview_categorie.heading('#0', text='ID')
    treeview_categorie.column('#0', width=60)
    treeview_categorie.heading('name', text='Name')
    treeview_categorie.heading('modifier', text='Modifier')
    treeview_categorie.column('modifier', width=60)
    treeview_categorie.heading('effacer', text='Effacer')
    treeview_categorie.column('effacer', width=60)
    treeview_categorie.bind("<Button-1>", clique_colonne_categorie)

    nom_label = tk.Label(modif_window, text="Entrez le nom de la catégorie:")
    nom_entry = tk.Entry(modif_window, width=100)

    ajout_button = tk.Button(modif_window, text="Valider", command=lambda: ajout())


    nom_label.pack()
    nom_entry.pack()
    ajout_button.pack()
    
    for row in categorie:
        nom_categorie = ""
        for lettre in str(row[1]):
            if lettre not in "(),'{[]}":
                nom_categorie += lettre
        treeview_categorie.insert('', 'end', text=row[0], values=(nom_categorie, "Modifier", "Effacer"))

frame = tk.Frame(root)
frame.pack(pady=10)

treeview = ttk.Treeview(frame, height=len(resultat))
treeview.pack(side=tk.LEFT)
treeview['columns'] = ('name', 'description', 'categorie', 'price', 'quantity', 'modifier', 'effacer')
treeview.heading('#0', text='ID')
treeview.column('#0', width=60)
treeview.heading('name', text='Name')
treeview.column('name', width=200)
treeview.heading('description', text='Description')
treeview.column('description', width=300)
treeview.heading('categorie', text='Categorie')
treeview.column('categorie', width=90)
treeview.heading('price', text='Price')
treeview.column('price', width=60, anchor=tk.CENTER)
treeview.heading('quantity', text='Quantity')
treeview.column('quantity', width=60)
treeview.heading('modifier', text='Modifier')
treeview.column('modifier', width=60)
treeview.heading('effacer', text='Effacer')
treeview.column('effacer', width=60)
treeview.bind("<Button-1>", clique_colonne_produit)

affich_nom(resultat, treeview, categorie)

ajout_button = tk.Button(root, text="Ajouter un produit", command=lambda: ajout())
ajout_button.pack()

ajout_button = tk.Button(root, text="Ajouter/supprimer une catégorie", command=lambda: ajout_categorie(categorie))
ajout_button.pack()

root.mainloop()