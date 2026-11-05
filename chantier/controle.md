# Contrôle des chiffres

Méthode : `chantier/controle/controle.py`, écrit sans relire `analyse.py`, recalcule depuis `donnees/` (doublons retirés, libellés `chat` corrigés, client inscrit après le 30 juin et lignes de commande postérieures écartés). Le script de l'analyste n'a été consulté qu'après mes résultats, pour expliquer les écarts.

## Chiffres cités et recalculés

| Chiffre cité | Recalculé | Écart | Fichier |
|---|---|---|---|
| Échantillon 1 984 clients | 1 984 | 0 | dossier, strategie |
| Abonnés partis 197 / 1 293 (15,2 %) | 197 / 1 293 (15,2 %) | 0 | dossier, présentation, strategie |
| Ponctuels sans commande 443 / 691 (64,1 %) | 443 / 691 (64,1 %) | 0 | dossier, présentation |
| Chats 114 / 481 (23,7 %), chiens 83 / 812 (10,2 %) | identique | 0 | dossier, présentation |
| Chats abonnés avec saumon 253 / 81 (32,0 %), sans 228 / 33 (14,5 %) | 253 / 81, 228 / 33 (P026, P027, P034 : croquettes et sachets chat saumon ; avec l'huile de saumon P021 : 82 / 257 = 31,9 %, écart nul sur la conclusion) | 0 | dossier, strategie |
| Motifs abonnés partis : 166 connus, 59 / 27 / 25 / 23 (35,5 %) | identique | 0 | dossier, présentation, strategie |
| Motifs ponctuels : prix 117 sur 356 | identique | 0 | dossier, strategie |
| Abonnés partis sans motif : 31 (dossier) | 31 | 0 | dossier |
| Abonnés partis sans motif : diapositive 4 (118 au premier passage, corrigé en 31) | 31 | 0 après correction | présentation |
| CA des partis 153 607 € (19,0 %) | 153 607 € (19,0 %) | 0 | dossier |
| CA de l'échantillon 810 464 € | 810 373 € | 0,01 % | dossier |
| CA abonnés partis 81 821 € (12,0 %) | 81 821 € (12,0 %) | 0 | dossier |
| CA moyen abonné parti 415 €, resté 550 € | 415 €, 550 € | 0 | dossier, strategie |
| CA moyen « 162 € » des segments 4 et 5 | 162 € pour les ponctuels partis (443) ; 182 € pour tous les ponctuels | libellé | dossier (corrigé : « ponctuel sans commande »), strategie (libellé inchangé) |
| Nouveaux abonnés 29 / 111 (26,1 %), avant 168 / 1 182 (14,2 %) | identique | 0 | dossier, présentation, strategie |
| Livraison décalée : 310 clients, 62 partis (20,0 %), sans 13,7 % ; 2 décalages 33,3 % sur 18 | 310 / 62, 135 / 983, 6 / 18 | 0 | dossier, présentation, strategie |
| Ponctuels avec retard 87, 81 sans commande (93,1 %), sans retard 59,9 % | 87 / 81, 362 / 604 | 0 | dossier, présentation, strategie |
| Ponctuels 2 tickets ou plus : 41, 35 (85 %) | 41, 35 (85,4 %) | 0 | strategie |
| Note 1-3 : 17,0 %, 4-5 : 14,0 % | 28 / 165, 60 / 430 | 0 | dossier, strategie |
| Cumul de signaux 12,2 / 17,3 / 15,5 % | identique (définition : décalage, retard, ticket ≥ 1, note ≤ 3) | 0 | dossier, strategie |
| Département 29 : 0,83 retard par client, 36 clients, moyenne 0,40 | 0,86, 35 clients, 0,40 | 3,6 % | strategie (dossier : plus de chiffre précis, corrigé) |
| Remboursements croquettes 0,22 % (juillet 2025), 1,23 % (juin 2026) | 0,22 %, 1,23 % | 0 | dossier, strategie |
| 15 doublons, 691 / 1 293 | 15 doublons clients | 0 | dossier |

## Business case

Recalculé indépendamment : H6 = 172, 248, 82 ; départs attendus 55,1 / 49,6 / 21,4 (total 126,1) ; gains prudent 3 029 / 2 728 / 1 178 = 6 935 € ; central 6 057 / 5 456 / 2 357 = 13 870 € ; coûts 2 064 + 1 984 + 492 = 4 540 €, plus 1 500 € fixes = 6 040 € ; soldes 895 € et 7 830 €. Tout concorde, dossier, stratégie et présentation compris (diapositive 8 : 895 € et 7 830 €, gain 6 935 € et 13 870 €, coûts 6 040 €).
Hypothèses H2, H4 et H5 : estimations d'agence, écrites comme telles, non vérifiables dans les données. Le solde prudent de 895 € est à peine positif ; la diapositive 8 titre « Le plan couvre ses coûts », ce qui est vrai en prudent à 895 € près seulement, et ne dit pas que le résultat repose sur H2.

## Second passage (après corrections du rédacteur et du designer)

- Présentation : « 118 » a disparu, la diapositive 4 dit 31 sans motif. Tous les autres chiffres des 10 diapositives concordent avec le recalcul (15,2 %, 23,7 / 10,2 %, 59 / 25 / 31 / 117 sur 356, 20,0 / 13,7 %, 26,1 % (29 / 111), 14,2 % (168 / 1 182), 64,1 %, 93,1 / 59,9 %, 895 / 7 830 €, 6 935 / 13 870 €, 6 040 €). « Presque deux fois » (1,84) et « deux fois plus » (2,3) tiennent. Note « plafond » sur les gains ajoutée.
- Dossier : 162 € correctement libellé, département 29 sans chiffre faux, 31 sans motif juste, business case recalculé à l'identique.
- Reste dans `strategie.md` (stratège, hors de mon périmètre), sans effet sur un chiffre clé : département 29 à 0,83 sur 36 clients (juste : 0,86 sur 35, ligne 40) ; « leur CA moyen (162 €) » appliqué aux segments 4 et 5 sans préciser « ponctuels sans commande » (ligne 51). Dans `chiffres.md` : « signalux » (lignes 252-254) et département 29 (analyste).
- Réserve de fond, non numérique : le solde prudent (895 €) repose sur H2, H4 et H5, estimations d'agence non vérifiables ; la diapositive 8 le dit (« de justesse »).
- `tableau-de-bord.html` n'entre pas dans ma mission : non contrôlé.

Aucun écart de plus de 2 % sur un chiffre clé dans les livrables à lire par le comité.

## Troisième passage

`controle.py` réexécuté sur les fichiers actuels (dossier.md, presentation.html et strategie.md relus en entier). Tous les résultats sont identiques aux passages précédents : 197 / 1 293, 443 / 691, 114 / 481, 83 / 812, 81 / 253 et 33 / 228, 166 motifs connus (59, 27, 25, 23) et 31 sans motif, 29 / 111 et 168 / 1 182, 62 / 310 et 135 / 983, 81 / 87 et 362 / 604, 153 607 €, 81 821 €, 415 € et 550 €, business case 6 935 € / 13 870 € de gain, 6 040 € de coûts, soldes 895 € et 7 830 €. Aucun « 118 » ni « signalux » dans les trois fichiers contrôlés.

Écarts restants, aucun sur un chiffre clé :
- `strategie.md` ligne 40 : département 29 à 0,83 retard par client sur 36 clients ; recalcul 0,86 sur 35 (3,6 %). Le dossier ne cite plus ce chiffre. À corriger par le stratège.
- `strategie.md` ligne 51 : « leur CA moyen (162 €) » sans préciser qu'il s'agit des ponctuels sans commande (les 691 ponctuels font 182 €). Libellé à corriger par le stratège.
- CA de l'échantillon : 810 464 € cité, 810 373 € recalculé (0,01 %).

Non contrôlé : `tableau-de-bord.html` (hors mission). H2, H4 et H5 restent des estimations d'agence que les données ne permettent pas de vérifier.

VERDICT : OK
