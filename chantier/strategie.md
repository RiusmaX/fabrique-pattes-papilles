# Stratégie anti-churn Pattes & Papilles

Tous les chiffres viennent de `chantier/analyse/chiffres.md` (section indiquée entre parenthèses), sauf mention contraire. Ils décrivent l'échantillon de 1984 clients au 30 juin 2026, pas les 18 000 clients actifs. Un signal qui précède un départ n'en est pas forcément la cause.

## Ce que le diagnostic permet de décider

Chez les abonnés, 197 clients sur 1293 sont partis entre le 1er juillet et le 30 septembre 2026 (15,2 %, section 1). Les chats partent plus que les chiens : 23,7 % contre 10,2 % (section 3). Le premier motif déclaré par les abonnés partis n'est pas le prix mais l'animal qui refuse la nourriture : 59 motifs sur 166 connus, soit 35,5 % (section 5). Le prix pèse 25 motifs sur 166 chez eux. Il domine seulement chez les achats ponctuels (117 motifs sur 356).

Les achats ponctuels ne se comparent pas aux abonnés : 443 sur 691 n'ont rien commandé sur la période (64,1 %), ce qui n'est pas une résiliation (section 1). Le plan les traite à part.

## Segments à risque

Les segments se recoupent : un abonné chat qui prend du saumon peut aussi avoir eu une livraison décalée. Leurs tailles ne s'additionnent pas.

| Segment | Taille | Signal | Action proposée |
|---|---|---|---|
| 1. Abonnés chats qui ont acheté du saumon depuis le 4 mai | 253 clients, 81 partis (32,0 %), contre 14,5 % pour les abonnés chats sans saumon (section 3) | Un produit chat au saumon dans les commandes depuis le 4 mai. Le lien de cause n'est pas prouvé : le catalogue saumon existe depuis 2021 et les données ne repèrent pas la nouvelle formule. | Écrire au client pour demander comment le chat accueille la croquette, et proposer d'échanger la prochaine livraison contre une autre recette du catalogue. Ne pas conclure sur la recette avant la décision d'Élise Garnier. |
| 2. Abonnés dont une livraison a été décalée | 310 clients (292 avec 1 décalage, 18 avec 2), 62 partis, soit 20,0 %, contre 13,7 % sans décalage (section 4) | `skipped_deliveries_90d` supérieur ou égal à 1. Avec 2 décalages, 33,3 % (18 clients : effectif très petit). | Contacter le client avant la livraison suivante, proposer d'ajuster le rythme (4, 5 ou 6 semaines existent déjà) plutôt que de le laisser résilier. |
| 3. Nouveaux abonnés | 111 clients inscrits depuis le 1er mars 2026, 29 partis, soit 26,1 %, contre 14,2 % pour les inscrits avant (section 2) | Date d'inscription récente, une ou deux commandes. | Message de suivi un mois après la première livraison : ça se passe bien, la quantité convient-elle, le rythme convient-il. Le baromètre cite « trop de croquettes reçues » (22 % des clients agacés) et « abonnement difficile à modifier » (18 %). |
| 4. Achats ponctuels ayant eu un colis en retard | 87 clients, 81 sans commande, soit 93,1 %, contre 59,9 % sans retard (section 4) | `late_deliveries_12m` égal à 1. Aussi : 41 ponctuels avec 2 tickets ou plus, 35 sans commande (85 %). | Contact humain du service client qui reconnaît le retard, avant toute offre. Un client ponctuel mécontent de la livraison ne revient pas de lui-même. |
| 5. Achats ponctuels réguliers | 691 ponctuels (section 1) ; la taille du sous-groupe « réguliers » n'est pas calculée dans `chiffres.md` | Plusieurs commandes sans abonnement (exemple dans les 20 : un client à 16 commandes). Critère à chiffrer par l'analyste. | Proposer l'abonnement du catalogue, qui donne 10 % sur les croquettes et les pâtées. Aucune autre remise. |

Un signal qui ne sert pas de critère : la note du dernier avis chez les abonnés (17,0 % de churn pour les notes de 1 à 3, 14,0 % pour 4 ou 5, section 4). L'écart est faible. Le cumul de signaux n'est pas monotone non plus (12,2 % avec 0 signal, 17,3 % avec 1, 15,5 % avec 2), donc on ne bâtit pas un score sur lui.

## Plan d'action

### Semaine 1

1. Faire valider les 20 messages par Lucie Prigent, qui relit tout ce qui touche aux données clients.
2. Appeler en priorité les deux abonnés dont la livraison est annoncée le 6 novembre et qui ont un historique de retards ou de contacts (Caroline et Raphaël, voir `recommandations.md`).
3. Demander à Élise Garnier les ventes par référence et les remboursements de la recette au saumon. Les remboursements de croquettes passent de 0,22 % des lignes en juillet 2025 à 1,23 % en juin 2026 (section 7) : le volume est faible, la cause inconnue.
4. Trancher les gestes commerciaux (voir « Questions ouvertes »). D'ici là, aucun message ne promet autre chose que le catalogue.

### Premier mois

1. Envoyer les 20 messages après relecture.
2. Poser une règle de contact : tout abonné qui décale une livraison ou subit un retard reçoit un message du service client avant la livraison suivante.
3. Contacter les abonnés chats du segment 1 : question sur la croquette, échange possible.
4. Programmer le message de suivi à 30 jours pour chaque nouvel abonné (segment 3).
5. Transmettre à la responsable logistique le constat sur les retards avant la renégociation du contrat en décembre. Dans l'échantillon, le département 29 compte 0,83 retard par client contre 0,40 en moyenne (36 clients, à lire avec prudence, section 7). Cette action est une proposition : la demande est silencieuse sur le périmètre logistique.

### Premier trimestre

1. Mesurer avec un groupe témoin : sur les segments 1 à 3, une moitié des clients est contactée, l'autre non. C'est la seule façon de connaître la part de départs évités, que ce document ne peut que supposer.
2. Proposer l'abonnement aux ponctuels réguliers (segment 5).
3. Prévenir les abonnés avant tout changement de prix ou de recette. Un client du baromètre le dit : « J'aimerais être prévenue avant une hausse de prix, pas la découvrir sur mon relevé. »
4. Refaire l'analyse avec des dates de résiliation. Les données actuelles n'ont qu'une fenêtre de départ, donc aucune évolution mensuelle.

## Business case

Le calcul porte sur les trois segments d'abonnés (1, 2 et 3), à l'échelle de l'échantillon. Les segments 4 et 5 ne sont pas chiffrés : leur « churn » est une absence de commande, et leur CA moyen (162 €, section 6) ne se compare pas à celui d'un abonné.

### Hypothèses

| N° | Hypothèse | Valeur | D'où elle vient |
|---|---|---|---|
| H1 | Le taux de départ du trimestre à venir égale celui observé sur le profil | 32,0 % (segment 1), 20,0 % (segment 2), 26,1 % (segment 3) | Données : `chiffres.md`, sections 2 à 4. |
| H2 | Part des départs évités par l'action | 10 % (prudent), 20 % (central) | Choix de l'agence. Aucune mesure n'existe dans les données. À corriger après le test avec groupe témoin. |
| H3 | Valeur d'un abonné conservé | 550 € de CA sur 12 mois | Données : CA moyen d'un abonné resté (`chiffres.md`, section 6). C'est du chiffre d'affaires TTC, pas de la marge : la marge n'est pas fournie. |
| H4 | Coût unitaire par abonné concerné | 12 € (segment 1), 8 € (segment 2), 6 € (segment 3) | Estimation de l'agence : temps du service client et coût d'un échange de livraison. Aucun coût n'est dans les données. À valider par la finance. |
| H5 | Coûts fixes du plan | 1 500 € | Estimation de l'agence : relecture, paramétrage des alertes, suivi du test. À valider par la finance. |
| H6 | Abonnés encore concernés | 172, 248 et 82 | Données : taille du segment moins les partis (253 − 81, 310 − 62, 111 − 29). |

Le coût d'acquisition de 66 € cité par le comité (compte rendu du 15 septembre 2026) n'entre pas dans le calcul : remplacer un abonné perdu coûterait en plus ce montant, ce qui rend l'estimation prudente.

### Calcul

Départs attendus = abonnés concernés (H6) × taux de départ (H1). Départs évités = départs attendus × H2. Gain = départs évités × 550 €. Coût = abonnés concernés × coût unitaire (H4).

| Segment | Départs attendus | Évités (prudent) | Évités (central) | Gain prudent | Gain central | Coût |
|---|---:|---:|---:|---:|---:|---:|
| 1. Chats au saumon | 55,1 | 5,5 | 11,0 | 3 029 € | 6 057 € | 2 064 € |
| 2. Livraison décalée | 49,6 | 5,0 | 9,9 | 2 728 € | 5 456 € | 1 984 € |
| 3. Nouveaux abonnés | 21,4 | 2,1 | 4,3 | 1 178 € | 2 357 € | 492 € |
| Total des trois segments | 126,1 | 12,6 | 25,2 | 6 935 € | 13 870 € | 4 540 € |

| Scénario | Gain en CA | Coûts (4 540 € + 1 500 € fixes) | Solde |
|---|---:|---:|---:|
| Prudent | 6 935 € | 6 040 € | 895 € |
| Central | 13 870 € | 6 040 € | 7 830 € |

Trois limites à lire avant de présenter ces chiffres. Les segments se recoupent : un client compté deux fois gonfle le gain, donc le total est un maximum. Le gain est du CA, la marge n'est pas connue. L'échantillon compte 1984 clients, la base 18 000 : on ne multiplie pas ce résultat, parce que la part d'abonnés de l'échantillon est plus forte que celle de la base.

Dans le scénario prudent, le plan est à peine rentable. Il tient surtout par le scénario central, qui repose sur H2, l'hypothèse la moins solide. C'est la raison du groupe témoin au premier trimestre.

## Questions ouvertes

1. Budget : aucune enveloppe pour le plan. Le seul montant cité par le comité (150 k€) concerne la visibilité dans les IA, un autre sujet. Les coûts H4 et H5 sont des ordres de grandeur d'agence.
2. Gestes commerciaux : le comité n'a décidé aucune remise. Les messages ne proposent que le catalogue : produits aux prix du catalogue, remise abonné de 10 %, ajustement du rythme. Tout produit offert ou geste de compensation est marqué « à valider » dans `recommandations.md`.
3. Prix : la hausse du 1er mars est maintenue. Le plan n'agit pas sur le prix. Les données montrent qu'il pèse peu chez les abonnés partis (25 motifs sur 166).
4. Recette saumon : le plan la traite comme un signal à vérifier, pas comme une cause. Élise Garnier tranche.
5. Date de validité des offres : la charte cite le 30 novembre en exemple. Aucune date n'est confirmée pour l'envoi.
