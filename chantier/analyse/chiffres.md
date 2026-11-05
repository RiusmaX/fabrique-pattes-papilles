# Chiffres clés : churn Pattes & Papilles

Source unique de tous les chiffres du dossier, de la présentation et des messages. Généré par `chantier/analyse/analyse.py`, à partir de `donnees/`.

## À lire avant d'utiliser un chiffre

- Échantillon de 1984 clients en portefeuille au 30 juin 2026, pas la base de 18 000 clients actifs. La part d'abonnés y est plus forte (dictionnaire, point 3). Ne pas multiplier ces chiffres pour parler de toute la base.
- Une seule fenêtre de départ : du 1er juillet au 30 septembre 2026 (3 mois). Il n'existe pas de série mensuelle de départs dans les données. Les « churn par mois » ci-dessous sont groupés par mois de dernière commande.
- Le mot « churn » ne veut pas dire la même chose pour les deux formules. Abonné : a résilié. Achat ponctuel : n'a rien commandé sur la période. Les deux taux ne se comparent pas et ne s'additionnent pas sans le dire.
- Corrélation n'est pas cause. Un signal qui précède un départ n'en est pas forcément la raison.
- Les montants sont en euros TTC.

## Nettoyage appliqué

- 15 lignes en double supprimées (2000 lignes lues, 1985 clients uniques)
- 7 libellés de canal corrigés (Facebook, Paid Social → paid_social) ; 5 espèces « chat » → cat
- 1 client exclu : dernière commande datée après la photo du 2026-06-30 (incohérent)
- 4 animaux de plus de 20 ans et 1 poids à 0 kg : laissés tels quels, ces colonnes ne servent pas aux calculs de départ
- 2 lignes de commande postérieures au 2026-06-30 écartées (le dictionnaire annonce des commandes jusqu'à cette date)

## 1. Churn global (colonne `churned`, `customers.csv`)

| Mesure | Valeur | Calcul |
|---|---:|---|
| Clients analysés | 1984 | lignes uniques de `customers.csv` après nettoyage |
| Partis, tous clients | 640 (32.3 %) | somme de `churned` / clients |
| Abonnés | 1293 | `plan` = subscription |
| Abonnés partis | 197 (15.2 %) | résiliations 1er juillet au 30 septembre 2026 |
| Achats ponctuels | 691 | `plan` = one_off |
| Ponctuels sans commande sur la période | 443 (64.1 %) | pas de commande du 1er juillet au 30 septembre 2026 |

## 2. Churn par mois de dernière commande (`last_order_date`)

| Mois | Tous : clients | Tous : churn | Abonnés : clients | Abonnés : churn | Ponctuels : clients | Ponctuels : churn |
|---|---:|---:|---:|---:|---:|---:|
| 2025-10 | 1 | 100.0 % | 0 | n/a | 1 | 100.0 % |
| 2025-12 | 8 | 100.0 % | 0 | n/a | 8 | 100.0 % |
| 2026-01 | 64 | 92.2 % | 0 | n/a | 64 | 92.2 % |
| 2026-02 | 73 | 83.6 % | 0 | n/a | 73 | 83.6 % |
| 2026-03 | 87 | 69.0 % | 0 | n/a | 87 | 69.0 % |
| 2026-04 | 149 | 60.4 % | 15 | 46.7 % | 134 | 61.9 % |
| 2026-05 | 420 | 30.2 % | 276 | 17.0 % | 144 | 55.6 % |
| 2026-06 | 1182 | 19.8 % | 1002 | 14.3 % | 180 | 50.6 % |

### Avant et après le 1er mars 2026 (hausse de prix de 5 %)

| Tous clients | Clients | Partis | Churn |
|---|---:|---:|---:|
| dernière commande avant le 1er mars 2026 | 146 | 129 | 88.4 % |
| dernière commande le 1er mars 2026 ou après | 1838 | 511 | 27.8 % |

| Abonnés | Clients | Partis | Churn |
|---|---:|---:|---:|
| dernière commande le 1er mars 2026 ou après | 1293 | 197 | 15.2 % |

| Ponctuels | Clients | Partis | Churn |
|---|---:|---:|---:|
| dernière commande avant le 1er mars 2026 | 146 | 129 | 88.4 % |
| dernière commande le 1er mars 2026 ou après | 545 | 314 | 57.6 % |

Lecture : chez les ponctuels, plus la dernière commande est ancienne, plus le « départ » est mécanique (pas de commande sur 3 mois de plus). Cette partie du tableau ne mesure pas l'effet de la hausse de prix. Chez les abonnés, les dernières commandes d'avant mars sont très peu nombreuses (voir effectifs) : on ne conclut rien sur elles.

Abonnés dont la dernière commande date d'avant le 1er mars 2026 : 0. Un abonné actif commande au moins tous les 6 semaines : la comparaison avant/après par date de dernière commande est donc impossible pour eux.

### Abonnés selon la date d'inscription (`signup_date`)

| Cohorte | Clients | Partis | Churn |
|---|---:|---:|---:|
| inscrits avant le 1er mars 2026 | 1182 | 168 | 14.2 % |
| inscrits le 1er mars 2026 ou après | 111 | 29 | 26.1 % |

## 3. Churn par segment

### Abonnés, par canal d'acquisition (`acquisition_channel`)

| Canal | Clients | Partis | Churn |
|---|---:|---:|---:|
| organic_search | 241 | 41 | 17.0 % |
| paid_search | 238 | 38 | 16.0 % |
| paid_social | 366 | 56 | 15.3 % |
| referral | 250 | 34 | 13.6 % |
| influencer | 88 | 13 | 14.8 % |
| direct | 110 | 15 | 13.6 % |

### Ponctuels, par canal d'acquisition (`acquisition_channel`)

| Canal | Clients | Partis | Churn |
|---|---:|---:|---:|
| organic_search | 75 | 44 | 58.7 % |
| paid_search | 130 | 84 | 64.6 % |
| paid_social | 284 | 187 | 65.8 % |
| referral | 64 | 29 | 45.3 % |
| influencer | 94 | 70 | 74.5 % |
| direct | 44 | 29 | 65.9 % |

### Abonnés, par espèce (`pet_species`)

| Espèce | Clients | Partis | Churn |
|---|---:|---:|---:|
| dog | 812 | 83 | 10.2 % |
| cat | 481 | 114 | 23.7 % |

### Ponctuels, par espèce (`pet_species`)

| Espèce | Clients | Partis | Churn |
|---|---:|---:|---:|
| dog | 343 | 229 | 66.8 % |
| cat | 348 | 214 | 61.5 % |

### Abonnés, par formule (`delivery_weeks`, rythme de livraison)

| Rythme | Clients | Partis | Churn |
|---|---:|---:|---:|
| toutes les 4 semaines | 372 | 48 | 12.9 % |
| toutes les 5 semaines | 549 | 93 | 16.9 % |
| toutes les 6 semaines | 372 | 56 | 15.1 % |

Les ponctuels n'ont pas de formule (colonne vide, non comptée comme zéro).

### Abonnés, par remise de bienvenue (`welcome_discount_pct`)

| Remise | Clients | Partis | Churn |
|---|---:|---:|---:|
| 0 % | 457 | 69 | 15.1 % |
| 20 % | 624 | 86 | 13.8 % |
| 30 % | 212 | 42 | 19.8 % |

### Ponctuels, par remise de bienvenue (`welcome_discount_pct`)

| Remise | Clients | Partis | Churn |
|---|---:|---:|---:|
| 0 % | 156 | 97 | 62.2 % |
| 20 % | 277 | 157 | 56.7 % |
| 30 % | 258 | 189 | 73.3 % |

### Remise de bienvenue selon le canal (abonnés, part des clients du canal)

| Canal | 0 % | 20 % | 30 % |
|---|---:|---:|---:|
| organic_search | 73 % | 24 % | 3 % |
| paid_search | 45 % | 49 % | 7 % |
| paid_social | 18 % | 43 % | 39 % |
| referral | 7 % | 93 % | 0 % |
| influencer | 14 % | 34 % | 52 % |
| direct | 73 % | 27 % | 0 % |

Remise et canal vont ensemble (parrainage et créateurs donnent 20 ou 30 %) : on ne peut pas dire laquelle des deux pèse sur le départ sans analyse plus poussée.

### Abonnés, par sensibilité déclarée (`sensitivity`)

| Sensibilité | Clients | Partis | Churn |
|---|---:|---:|---:|
| none | 774 | 122 | 15.8 % |
| digestive | 233 | 20 | 8.6 % |
| skin | 107 | 24 | 22.4 % |
| overweight | 179 | 31 | 17.3 % |

### Abonnés chats : achat de produits au saumon depuis le 4 mai 2026

| Abonnés chats | Clients | Partis | Churn |
|---|---:|---:|---:|
| a acheté du saumon depuis le 4 mai | 253 | 81 | 32.0 % |
| n'a pas acheté de saumon depuis le 4 mai | 228 | 33 | 14.5 % |

Lecture : l'écart est très net, mais il ne prouve pas que le saumon cause le départ. Les produits au saumon du catalogue existent depuis 2021 (`launch_date`) et les données ne repèrent pas la « nouvelle recette » du 4 mai : « saumon » désigne ici tout produit chat au saumon (croquettes ou sachets). Les motifs déclarés vont dans le même sens (voir section 5 : « animal refuse » en tête chez les abonnés). À confirmer avec le service qualité avant toute conclusion.

Abonnés chats, par sensibilité déclarée :

| Sensibilité | Clients | Partis | Churn |
|---|---:|---:|---:|
| none | 252 | 75 | 29.8 % |
| digestive | 80 | 4 | 5.0 % |
| skin | 43 | 13 | 30.2 % |
| overweight | 106 | 22 | 20.8 % |

## 4. Signaux qui précèdent un départ

Colonnes `skipped_deliveries_90d` (abonnés seulement), `late_deliveries_12m`, `support_tickets_12m`, `last_review_score`.

### Abonnés, livraisons décalées sur 90 jours

| Livraisons décalées | Clients | Partis | Churn |
|---|---:|---:|---:|
| 0 | 983 | 135 | 13.7 % |
| 1 | 292 | 56 | 19.2 % |
| 2 | 18 | 6 | 33.3 % |

### Abonnés, colis en retard sur 12 mois

| Retards | Clients | Partis | Churn |
|---|---:|---:|---:|
| 0 | 743 | 116 | 15.6 % |
| 1 | 423 | 58 | 13.7 % |
| 2 | 100 | 21 | 21.0 % |
| 3 ou plus | 27 | 2 | 7.4 % |

### Ponctuels, colis en retard sur 12 mois

| Retards | Clients | Partis | Churn |
|---|---:|---:|---:|
| 0 | 604 | 362 | 59.9 % |
| 1 | 87 | 81 | 93.1 % |

### Abonnés, tickets au service client sur 12 mois

| Tickets | Clients | Partis | Churn |
|---|---:|---:|---:|
| 0 | 816 | 117 | 14.3 % |
| 1 | 319 | 50 | 15.7 % |
| 2 | 115 | 21 | 18.3 % |
| 3 ou plus | 43 | 9 | 20.9 % |

### Ponctuels, tickets au service client sur 12 mois

| Tickets | Clients | Partis | Churn |
|---|---:|---:|---:|
| 0 | 543 | 328 | 60.4 % |
| 1 | 107 | 80 | 74.8 % |
| 2 | 27 | 23 | 85.2 % |
| 3 ou plus | 14 | 12 | 85.7 % |

### Abonnés, note du dernier avis (« aucun avis » = colonne vide, jamais comptée comme une note)

| Dernier avis | Clients | Partis | Churn |
|---|---:|---:|---:|
| aucun avis | 698 | 109 | 15.6 % |
| 1 sur 5 | 6 | 1 | 16.7 % |
| 2 sur 5 | 30 | 6 | 20.0 % |
| 3 sur 5 | 129 | 21 | 16.3 % |
| 4 sur 5 | 220 | 31 | 14.1 % |
| 5 sur 5 | 210 | 29 | 13.8 % |

### Ponctuels, note du dernier avis

| Dernier avis | Clients | Partis | Churn |
|---|---:|---:|---:|
| aucun avis | 407 | 254 | 62.4 % |
| 1 sur 5 | 2 | 2 | 100.0 % |
| 2 sur 5 | 19 | 16 | 84.2 % |
| 3 sur 5 | 63 | 53 | 84.1 % |
| 4 sur 5 | 102 | 74 | 72.5 % |
| 5 sur 5 | 98 | 44 | 44.9 % |

Regroupement abonnés : note de 1 à 3 → 17.0 % de churn (165 clients) ; note de 4 ou 5 → 14.0 % (430 clients).

### Abonnés, cumul de signaux (livraison décalée, retard, ticket, note de 1 à 3)

| Signaux cumulés | Clients | Partis | Churn |
|---|---:|---:|---:|
| 0 signal | 417 | 51 | 12.2 % |
| 1 signal | 394 | 68 | 17.3 % |
| 2 signalux | 349 | 54 | 15.5 % |
| 3 signalux | 122 | 21 | 17.2 % |
| 4 signalux | 11 | 3 | 27.3 % |

## 5. Raisons de départ déclarées (`churn_reason`)

- Clients partis : 640, dont 522 avec un motif connu et 118 sans motif (colonne vide, ne pas lire comme « autre »).
- Clients restés avec un motif renseigné : 0 (attendu : 0).

| Motif | Partis | Part des motifs connus |
|---|---:|---:|
| Prix (`price`) | 142 | 27.2 % |
| Autre (`other`) | 94 | 18.0 % |
| Livraison (`delivery_issues`) | 86 | 16.5 % |
| Concurrent (`switched_competitor`) | 85 | 16.3 % |
| Animal refuse (`pet_refused_food`) | 75 | 14.4 % |
| Trop de stock (`too_much_stock`) | 23 | 4.4 % |
| Régime vétérinaire (`moved_to_vet_diet`) | 9 | 1.7 % |
| Animal décédé (`pet_deceased`) | 8 | 1.5 % |

Motifs des abonnés partis (166 motifs connus sur 197 partis) : Animal refuse 59, Livraison 27, Prix 25, Trop de stock 23, Concurrent 13, Autre 9, Régime vétérinaire 8, Animal décédé 2.

Motifs des ponctuels partis (356 motifs connus sur 443 partis) : Prix 117, Autre 85, Concurrent 72, Livraison 59, Animal refuse 16, Animal décédé 6, Régime vétérinaire 1.

## 6. Chiffre d'affaires perdu (12 mois précédant le 30 juin 2026)

Définition : somme de `line_total_eur` (remboursements déduits) des commandes du 1er juillet 2025 au 30 juin 2026 des clients partis (`orders.csv`). C'est le CA annuel que ces clients représentaient, pas un CA futur garanti. Pour un ponctuel « parti », c'est une absence de commande, pas une résiliation : le CA n'est pas forcément perdu.
3 clients n'ont aucune commande sur ces 12 mois (leur CA vaut 0, ils sont comptés).

| Mesure | Valeur | Calcul |
|---|---:|---|
| CA 12 mois, tous clients de l'échantillon | 810 464 € | somme de `line_total_eur` |
| CA 12 mois des clients partis | 153 607 € (19.0 % du CA) | clients avec `churned` = 1 |
| dont abonnés partis | 81 821 € (12.0 % du CA des abonnés) | `plan` = subscription, `churned` = 1 |
| dont ponctuels sans commande | 71 787 € | `plan` = one_off, `churned` = 1 |
| CA 12 mois moyen d'un abonné parti | 415 € | moyenne sur 197 abonnés |
| CA 12 mois moyen d'un abonné resté | 550 € | moyenne sur 1096 abonnés |
| CA 12 mois moyen d'un ponctuel sans commande | 162 € | moyenne sur 443 clients |

Ces montants valent pour l'échantillon de presque 2 000 clients, pas pour les 18 000 clients actifs. Aucune extrapolation n'est faite ici : la part d'abonnés de l'échantillon est plus forte que celle de la base.

### CA 12 mois des partis, par motif (tous clients partis)

| Motif | Partis | CA 12 mois |
|---|---:|---:|
| Prix | 142 | 28 563 € |
| Motif inconnu | 118 | 25 201 € |
| Livraison | 86 | 21 995 € |
| Animal refuse | 75 | 21 437 € |
| Concurrent | 85 | 20 722 € |
| Autre | 94 | 18 551 € |
| Trop de stock | 23 | 8 093 € |
| Régime vétérinaire | 9 | 6 715 € |
| Animal décédé | 8 | 2 329 € |

## 7. Repères complémentaires

### Remboursements de croquettes (`orders.csv`, lignes avec quantité négative / lignes de croquettes)

| Mois | Lignes de croquettes | Remboursées | Part |
|---|---:|---:|---:|
| 2025-07 | 893 | 2 | 0.22 % |
| 2025-08 | 937 | 0 | 0.00 % |
| 2025-09 | 935 | 0 | 0.00 % |
| 2025-10 | 972 | 0 | 0.00 % |
| 2025-11 | 989 | 1 | 0.10 % |
| 2025-12 | 1017 | 0 | 0.00 % |
| 2026-01 | 1117 | 1 | 0.09 % |
| 2026-02 | 1066 | 0 | 0.00 % |
| 2026-03 | 1170 | 5 | 0.43 % |
| 2026-04 | 1171 | 10 | 0.85 % |
| 2026-05 | 1232 | 12 | 0.97 % |
| 2026-06 | 1218 | 15 | 1.23 % |

Les volumes sont faibles (quelques dizaines de lignes). Les données ne disent pas la cause des remboursements ni le transporteur : le lien avec le changement de transporteur du 2 mars ou la recette au saumon du 4 mai ne peut pas être établi ici.

### Départements (au moins 30 clients) : retards de livraison moyens sur 12 mois

| Département | Clients | Retards par client | Churn |
|---|---:|---:|---:|
| 29 | 36 | 0.83 | 36.1 % |
| 92 | 63 | 0.56 | 23.8 % |
| 33 | 88 | 0.52 | 30.7 % |
| 59 | 50 | 0.48 | 28.0 % |
| 13 | 63 | 0.48 | 27.0 % |

Moyenne de l'échantillon : 0.40 retard par client. Écarts à lire avec prudence vu les petits effectifs.

### Fichier `abonnes_support.csv` (les 20 clients à risque)

- 20 clients : 10 abonnés et 10 achats ponctuels.
- Sensibilités déclarées : aucune 17, peau 2, surpoids 1.

## Graphiques produits

Dans `chantier/analyse/` : `01-churn-plan-et-mois.png`, `02-churn-canal.png`, `03-churn-profil.png`, `04-signaux.png`, `05-motifs.png`, `06-ca-perdu.png`.

## Ce que les données ne permettent pas de dire

- L'effet causal de la hausse de prix du 1er mars, du transporteur du 2 mars ou de la recette saumon du 4 mai : une seule fenêtre de départ, pas de date de résiliation, pas de transporteur par commande.
- Le churn de la base entière : l'échantillon surreprésente les abonnés.
- Un modèle prédictif : non demandé ici.
