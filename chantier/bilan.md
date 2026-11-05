# Bilan de mission : plan anti-churn Pattes & Papilles

**Statut : non livrable en l'état.** Le contrôleur dit `VERDICT : OK` (troisième passage), le relecteur dit `VERDICT : A CORRIGER` (troisième passage). Le plan fait des deux contrôles des points bloquants. Rien ne part chez Nadia Ferrand avant la correction des 4 points ci-dessous.

## Ce qui est livré

Chemins relatifs à `chantier/`.

| Demande du client | Fichier | État |
|---|---|---|
| 1. Diagnostic chiffré | `analyse/chiffres.md`, `analyse/analyse.py`, 6 PNG dans `analyse/` | Fait. Chiffres recalculés par le contrôleur, 0 écart sur un chiffre clé. Reste « signalux » (3 occurrences) et le panneau remise de bienvenue dans les PNG d'origine. |
| 2. Tableau de bord | `livrables/tableau-de-bord.html` | Écrit, **ni contrôlé ni relu** (hors mission des deux contrôleurs). |
| 3. Messages aux 20 abonnés à risque | `livrables/messages-abonnes.md` (base : `recommandations.md`) | Écrit, 2 passages de corrections. **4 erreurs ouvertes** (ci-dessous). |
| 4. Business case | `strategie.md`, partie 4 de `livrables/dossier.md` | Recalculé : gain 6 935 € (prudent) et 13 870 € (central), coûts 6 040 €, soldes 895 € et 7 830 €. Repose sur H2, H4, H5, estimations d'agence. |
| 5. Présentation, 10 diapositives | `livrables/presentation.html`, `livrables/assets/` (4 PNG) | Écrite, 3 passages. 1 point ouvert (courbe mensuelle, diapo 2). |
| Dossier remis au client | `livrables/dossier.md` | Écrit, 6 parties, chiffres contrôlés. |
| Contrôle, relecture | `controle.md`, `controle/controle.py`, `relecture.md` | Faits. |

## Refusé par le relecteur (troisième passage) et pourquoi

1. **Message 17 (Yann), `messages-abonnes.md` ligne 257** : « depuis janvier » est faux. `orders.csv` montre du saumon à chaque commande depuis le 26 juillet 2025. Toujours présent dans le fichier.
2. **Messages 2, 10, 17** : genre inventé des animaux (« a-t-elle », « il »). `customers.csv` n'a pas de colonne de sexe. À reformuler sans pronom.
3. **Message 12 (Paul), ligne 184** : « ni le produit ni le prix » promet une stabilité du prix que personne n'a décidée (hausse de 5 % le 1er mars). Toujours présent.
4. **Diapositive 2, PNG 01** : la courbe « churn selon le mois de dernière commande » (47 % en avril, 14 % en juin) est un effet de sélection, mais le comité y lira un pic en avril. À retirer ou à légender.

Points mineurs relevés : PNG tracés en polices de repli (Fraunces et Inter absentes du VPS) ; diapo 5, les 20,0 % et 13,7 % du texte ne figurent pas dans le PNG ; messages 8 et 15 annoncent un appel « avant la prochaine livraison » alors que le fichier de suivi date ces livraisons du 6 novembre ; 66 € de coût d'acquisition et 150 k€ viennent du comité, à retirer si le dossier sort de chez le client.

## Écarts du contrôleur, sans effet sur un chiffre clé

- `strategie.md` ligne 40 : département 29 à 0,83 sur 36 clients, recalcul 0,86 sur 35.
- `strategie.md` ligne 51 : 162 € à libeller « ponctuels sans commande » (182 € pour les 691 ponctuels).
- CA de l'échantillon : 810 464 € cité, 810 373 € recalculé (0,01 %).

## Reste à faire par un humain

- **Valider côté client** : Lucie Prigent (les 20 messages, données clients), Nadia Ferrand, Élise Garnier (recette saumon), finance. Aucune validation n'est enregistrée ; la diapositive 10 le dit.
- **Décisions manquantes** : budget du plan, gestes commerciaux (messages 5 et 15 sans proposition), date de validité des offres, périmètre logistique, prix.
- **Valider H2, H4, H5** (10 et 20 % de départs évités, coûts unitaires, 1 500 € fixes). Le solde prudent de 895 € en dépend entièrement.
- **Confirmer les dates de livraison** avec le service client avant d'envoyer les messages 8 et 15 ; `next_delivery` est incohérent avec les dernières commandes.
- **Taille du segment 5** (ponctuels réguliers) non calculée.
- **Polices** : régénérer les PNG avec Fraunces et Inter depuis une machine qui les a.
- **Hors cadre** : le tableau de bord n'a eu ni contrôle des chiffres ni relecture.
- **Pas d'extrapolation** à la base de 18 000 clients (échantillon biaisé vers les abonnés). Effets causaux de la hausse de prix, du transporteur et de la recette saumon non établis.

## Correction nécessaire avant livraison

Le rédacteur corrige les points 1 à 3 dans `messages-abonnes.md`, le designer le point 4 dans `presentation.html`. Ensuite, nouveau passage du relecteur, puis un contrôle du tableau de bord. Il n'y a pas eu de passage de correction après 09:00 : c'est la raison de l'état actuel.

## Trois leçons

1. **Règle pour `agents/redacteur.md`** : tout fait temporel d'un message (« depuis… », « à chaque livraison ») se vérifie dans `orders.csv` avant écriture, et un animal n'a pas de pronom tant que les données ne donnent pas son sexe. Le même défaut est revenu sur trois passages.
2. **Règle pour `AGENTS.md`** : chaque livrable passe par le contrôleur ou le relecteur, tableau de bord compris. Le plan ne l'avait attribué à personne.
3. **Règle pour `agents/analyste.md` et `agents/stratege.md`** : un correctif demandé sur un fichier se fait par son propriétaire dans le même tour. `chiffres.md` et `strategie.md` portent encore des écarts signalés trois fois, parce que le contrôleur n'a pas le droit d'écrire chez les autres. Ajouter aussi une passe de correction obligatoire après un `A CORRIGER`, avec le relecteur en dernier.
