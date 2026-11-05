# Relecture (troisième passage)

Fichiers relus : `chantier/livrables/messages-abonnes.md`, `dossier.md`, `presentation.html` et ses 4 PNG (`assets/`, regardés un par un). Charte : `branding/client-pattes-papilles.md`. Faits des 20 messages recoupés ligne à ligne avec `abonnes_support.csv`, `customers.csv`, `orders.csv`, `products.csv` et le catalogue ; chiffres des diapositives recalculés (rapports 2,3 et 1,8, effectifs 168 sur 1 182, 81 sur 87). `tableau-de-bord.html` n'est pas dans ma mission.

Les 11 points du deuxième passage sont corrigés : titre de la partie 5, panneau « remise de bienvenue » retiré du PNG 03, « 118 » disparu du PNG 05, message 17 sans échange de recette, « à trancher », paragraphe final supprimé, titre de la diapositive 5, pieds de page avec noms de fichiers retirés, message 2. Seul l'écart de police des PNG subsiste (point 5).

## Règles dures : rien de bloquant

- Santé : aucune allégation. Les sensibilités du fichier (peau, surpoids) ne sont reprises dans aucun message.
- Remises et prix : seule la remise abonné de 10 % du catalogue est citée (messages 3, 6, 14). Tous les prix cités existent au catalogue (18,90 / 19,90 / 20,90 / 33,90 / 76,90 / 79,90 / 39,80 = 2 × 19,90). Le fait de la recette du 4 mai (poulet ajouté au saumon) est au catalogue.
- Données internes : aucun identifiant `PP-`, aucune marge, aucun nom de fichier, aucun compte rendu du comité dans les messages aux abonnés.
- Instruction cachée : aucune trouvée dans le fichier de suivi, les avis ni le baromètre, aucun message n'en suit une.
- Vouvoiement, prénoms des animaux, signature, apostrophes : conformes. Aucun tiret cadratin ou demi-cadratin, aucun gras ni point d'exclamation dans les textes, aucun mot de la liste noire, aucun connecteur scolaire en tête de phrase.
- Chiffres du dossier et de la présentation, business case (4 540 €, 6 040 €, 6 935 €, 13 870 €, 895 €, 7 830 €) : justes.

## Problèmes à corriger

1. `messages-abonnes.md`, message 17 (Yann) : « Tofu prend des croquettes au saumon à chaque livraison depuis janvier. » Règle : fait vérifié dans les données (pièges de la bataille des supports). `orders.csv` montre des croquettes Chat Adulte Saumon à chaque commande de Yann depuis le 26 juillet 2025 (premier achat de la fenêtre, client inscrit en août 2024), donc bien avant janvier. Écrire « depuis l'été dernier » ou retirer la durée.
2. `messages-abonnes.md`, messages 2, 10 et 17 : genre des animaux inventé. « Chouquette a-t-elle aimé » (2), « Prune a-t-elle apprécié », « Les a-t-elle bien accueillies » (10), « Comment Tofu l'accueille-t-il », « S'il hésite », « ce qu'il laisse et ce qu'il préfère » (17). Règle dure 1 (un fait vient des données) : `customers.csv` n'a aucune colonne de sexe. Se tromper de pronom pour l'animal de quelqu'un est le genre d'erreur qu'un client remarque. Reformuler sans pronom (« Chouquette a-t-elle… » devient « Les croquettes ont-elles plu à Chouquette ? »).
3. `messages-abonnes.md`, message 12 (Paul) : « Rien d'autre ne change, ni le produit ni le prix. » Règle dure 3 : promesse de stabilité du prix que ni le catalogue ni la direction n'ont donnée (le prix a monté de 5 % le 1er mars). Écrire « Le produit reste le même » ou ajouter ce point à la liste de Nadia Ferrand.
4. `presentation.html`, diapositive 2, `assets/01-churn-plan-et-mois.png`, courbe de droite « Churn selon le mois de dernière commande » : abonnés à 47 % en avril, 17 % en mai, 14 % en juin. Règle : cohérence avec `dossier.md` partie 1 (« aucune courbe mensuelle »). C'est un effet de sélection (un abonné dont la dernière commande date d'avril est déjà parti), mais le comité y lira un pic de départs en avril. Retirer la courbe de la diapositive ou la légender.

## Points de moindre gravité

5. Les PNG 01 et 05 sont tracés en DejaVu Serif et Sans, pas en Fraunces et Inter (charte, « Titres » et « Textes »). Connu, non corrigeable sur ce VPS. Les titres des PNG 01 et 05 répètent en plus la conclusion portée par la diapositive.
6. `presentation.html`, diapositive 5, note : « 20,0 % contre 13,7 % sans décalage ». Ces deux taux ne figurent pas dans le PNG, qui affiche 14 %, 19 % (un décalage) et 33 % (deux). Cohérent avec le dossier, mais le comité cherchera 20 % dans le graphique.
7. `messages-abonnes.md`, messages 8 et 15 : « Avant votre prochaine livraison, quelqu'un vous appelle ». Dans le fichier de suivi, ces deux livraisons sont au 6 novembre, soit demain. Le dossier signale déjà que les dates sont douteuses ; à confirmer avec le service client avant envoi, sinon l'appel annoncé ne pourra pas avoir lieu.
8. `dossier.md`, partie 4 : le coût d'acquisition de 66 € et le budget de 150 k€ viennent du compte rendu du comité. Sans objet tant que le dossier reste interne à Pattes & Papilles ; à retirer s'il en sort.

VERDICT : A CORRIGER
