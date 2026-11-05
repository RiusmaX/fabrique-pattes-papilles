                                                                                              LE CAS · AI WEEK

LE CAS · DONNÉES


Dictionnaire des données
     Données simulées de Pattes & Papilles, marque fictive. Elles ne sont pas propres, comme
     un vrai export : regardez-les avant de calculer.



Ce que contiennent les fichiers
1.     La photo : les variables décrivent chaque client au 30 juin 2026.

2.     Le départ : la colonne churned dit ce qui s'est passé ensuite, du 1er juillet au 30 septembre 2026.
       C'est ce qu'un modèle doit prévoir à partir de la photo.

3.     L'échantillon : 2 000 lignes tirées au hasard parmi les clients en portefeuille au 30 juin
       (abonnement en cours, ou dernière commande depuis moins de six mois). Ce n'est pas la base des
       18 000 clients actifs à douze mois : la part d'abonnés y est plus forte.

4.     Les commandes : 23 184 lignes, soit 12 673 commandes, du 1er juillet 2025 au 30 juin 2026, pour
       les clients de l'échantillon.

5.     Le format : CSV (comma-separated values, valeurs séparées par des virgules), point décimal,
       encodage UTF-8 (celui qui garde les accents). Pour le tableur, ouvrez plutôt le classeur, qui reprend
       les quatre tables.


customers.csv
Colonne                         Type      Sens
customer_id                     texte     Identifiant du client (PP- et six chiffres).
first_name                      texte     Prénom (fictif).
signup_date                     date      Date de la première commande, au format AAAA-MM-JJ.
acquisition_channel             texte     Canal de la première visite : organic_search (référencement
                                          naturel), paid_social (publicité Meta : Facebook et Instagram),
                                          paid_search (publicité Google), referral (parrainage), influencer
                                          (code d'un créateur de contenu), direct (adresse tapée, bouche-à-
                                          oreille).
welcome_discount_pct            entier    Remise de bienvenue sur la première commande : 0, 20
                                          (parrainage, code BIENVENUE20 ou code de créateur) ou 30 (code
                                          BIENVENUE30 ou code de créateur).
department                      texte     Département de livraison (01, 2A, 75…). À lire comme du texte.
household_income_band           texte     Revenu mensuel net du foyer, en euros, estimé par un courtier en
                                          données (fichier acheté en 2025). Vide : client non apparié.
pet_name                        texte     Prénom de l'animal.
pet_species                     texte     dog ou cat.
pet_age_years                   décimal   Âge de l'animal au 30 juin 2026, en années.
pet_weight_kg                   décimal   Poids déclaré dans le quiz, en kilos.
pet_sterilized                  texte     yes ou no.

Sergent.dev · Formation                                                                                    Page 1 / 4
                                                                                            LE CAS · AI WEEK

Colonne                   Type      Sens
activity_level            texte     low, normal ou high (déclaré dans le quiz).
sensitivity               texte     none, digestive, skin ou overweight (déclaré dans le quiz).
plan                      texte     subscription : abonnement en cours au 30 juin 2026 ; one_off :
                                    sans abonnement.
delivery_weeks            entier    Rythme de l'abonnement, en semaines (4, 5 ou 6). Vide sans
                                    abonnement.
orders_count              entier    Nombre de commandes depuis l'inscription, jusqu'au 30 juin
                                    2026 : toute la vie du client, quand orders.csv ne garde que douze
                                    mois.
total_spent_eur           décimal   Total dépensé depuis l'inscription, en euros toutes taxes
                                    comprises (TTC), remises déduites, hors remboursements.
avg_basket_eur            décimal   total_spent_eur divisé par orders_count.
last_order_date           date      Date de la dernière commande avant le 30 juin 2026 inclus.
skipped_deliveries_90d    entier    Livraisons décalées par l'abonné dans les 90 jours avant le 30 juin.
                                    Vide sans abonnement.
late_deliveries_12m       entier    Colis livrés en retard sur les douze mois avant le 30 juin.
support_tickets_12m       entier    Demandes au service client sur les douze mois avant le 30 juin.
last_review_score         entier    Note du dernier avis déposé, de 1 à 5. Vide : aucun avis.
newsletter_optin          texte     yes ou no : inscrit à la newsletter.
email_open_rate_90d       décimal   Part des e-mails marketing ouverts sur 90 jours, de 0 à 1. Vide :
                                    pas inscrit à la newsletter.
churn_reason              texte     Motif donné par le client quand il part (enquête de départ ou
                                    service client) : price, too_much_stock, pet_refused_food,
                                    delivery_issues, switched_competitor, pet_deceased,
                                    moved_to_vet_diet, other. Vide : pas de motif connu.
churned                   entier    1 si l'abonné a résilié entre le 1er juillet et le 30 septembre 2026,
                                    ou si le client sans abonnement n'a rien commandé sur cette
                                    période ; 0 sinon.




orders.csv
Colonne                   Type      Sens
order_id                  entier    Numéro de commande. Une commande compte une ou plusieurs
                                    lignes.
order_date                date      Date de la commande.
customer_id               texte     Le client (voir customers.csv).
product_id                texte     La référence (voir products.csv).
quantity                  entier    Quantité. Négative : remboursement d'un article, qui reprend le
                                    numéro de la commande d'origine.
unit_price_eur            décimal   Prix catalogue TTC à la date de la commande.
discount_eur              décimal   Remise de la ligne : bienvenue (première commande) ou remise
                                    abonné de 10 %.
line_total_eur            décimal   quantity × unit_price_eur - discount_eur.
order_type                texte     subscription (livraison d'abonnement) ou one_off.
batch_id                  texte     Numéro de lot des croquettes : L, année et mois de fabrication,
                                    série (L2605-14 : mai 2026, série 14). Vide pour les autres produits.

Sergent.dev · Formation                                                                                     Page 2 / 4
                                                                                            LE CAS · AI WEEK




products.csv
Colonne                   Type      Sens
product_id                texte     La référence.
name                      texte     Le nom affiché sur le site.
species                   texte     dog, cat ou both.
category                  texte     kibble (croquettes), wet (pâtée, sachet), treat (friandise),
                                    supplement, accessory.
recipe                    texte     Protéine principale.
life_stage                texte     puppy, kitten, adult, senior ou all.
pack_size                 texte     Contenance affichée.
pack_kg                   décimal   Kilos de nourriture. Vide : produit vendu au volume ou à la pièce.
price_eur                 décimal   Prix TTC au 30 juin 2026 (hausse de 5 % le 1er mars 2026).
subscription_eligible     texte     yes : remise abonné de 10 % possible.
launch_date               date      Mise en vente.




marketing_monthly.csv
Colonne                   Type      Sens
month                     texte     Mois, au format AAAA-MM.
channel                   texte     Les canaux de customers.csv.
spend_eur                 entier    Dépenses du mois : achat d'espace, rémunération des créateurs,
                                    récompenses de parrainage. 0 pour les canaux sans dépense.
impressions               entier    Affichages des publicités. Vide pour les canaux sans publicité.
clicks                    entier    Clics vers le site. Vide pour les canaux sans publicité.
new_customers             entier    Nouveaux clients du mois venus par ce canal, pour toute
                                    l'entreprise (pas seulement l'échantillon).




Sergent.dev · Formation                                                                                  Page 3 / 4
                                                                                        LE CAS · AI WEEK


Rappels de base
Pour celles et ceux qui ont besoin de se remettre les notions en tête avant les travaux pratiques (TP) du
lundi.


     Taux de départ (churn en anglais) : la part des clients partis sur une période. Ici, trois
     mois : 120 départs sur 400 clients, c'est 30 %.

     Photo et fenêtre : on décrit les clients à une date, puis on regarde qui part ensuite. Une
     colonne connue seulement après la photo ne doit pas entrer dans un modèle : c'est une
     fuite de données, et le modèle paraît parfait sans rien prévoir.

     Entraînement et test : le modèle apprend sur 70 % des clients ; on le juge sur les 30 %
     qu'il n'a jamais vus.

     Précision et rappel : le modèle désigne 100 clients à risque, 70 partent vraiment : la
     précision est de 70 %. S'il y avait 200 partants en tout, il en a trouvé 70 : le rappel est de
     35 %.

     AUC (area under the curve, l'aire sous la courbe ROC) : la probabilité que le modèle place
     plus haut un partant qu'un fidèle, tous deux tirés au hasard. 0,5 vaut pile ou face, 1 est
     parfait. Au-delà de 0,95 sur des données clients, cherchez la fuite.

     RFM (récence, fréquence, montant) : jours depuis la dernière commande, nombre de
     commandes, dépense. On note chaque client de 1 à 5 sur chaque axe, puis on regroupe.

     Coût d'acquisition client (CAC) : les dépenses d'un canal divisées par les nouveaux
     clients qu'il a amenés.

     Valeur vie client (LTV, lifetime value) : la marge qu'un client rapporte tant qu'il reste.
     Approximation : dépense annuelle × marge brute × durée de vie, et la durée de vie vaut
     environ 1 ÷ le taux de départ annuel (25 % de départs par an : quatre ans).



Avant de confier un fichier à une intelligence artificielle (IA)
1.     Le fichier clients contient des prénoms et une estimation de revenu : même fictifs, traitez-les
       comme des données personnelles.

2.     Joignez ce dictionnaire au fichier : l'assistant se trompe moins quand il connaît le sens des
       colonnes.

3.     Demandez-lui le code qu'il exécute et relisez-le. Recalculez au tableur au moins un chiffre clé.


Sergent.dev · Formation                                                                           Page 4 / 4
