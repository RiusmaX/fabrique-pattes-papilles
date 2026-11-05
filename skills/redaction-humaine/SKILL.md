---
name: redaction-humaine
description: Rédiger et réécrire des textes avec un style humain naturel et indétectable, sans marqueurs d'IA générative. Utiliser cette compétence dès que l'utilisateur demande un texte naturel, "human-like", sans trace d'IA, un article, un billet de blog, une documentation, un courrier ou une réécriture fluide qui échappe aux tics algorithmiques et aux détecteurs d'IA.
---

# Rédaction Humaine

Cette compétence applique des règles typographiques, syntaxiques, lexicales et structurelles strictes pour produire des textes indiscernables d'une rédaction humaine soignée et éliminer tous les marqueurs d'IA générative.

## 1. Typographie et mise en forme (Zéro trace visuelle)

1. **Interdiction des tirets d'incise anglo-saxons** : Ne jamais utiliser le tiret cadratin (U+2014) ni le demi-cadratin (U+2013) pour isoler une incise. Utiliser des virgules, des parenthèses ou scinder en deux phrases.
2. **Casse française stricte dans les titres** : Seule la première lettre du titre et les noms propres prennent une majuscule. Ne jamais appliquer le *Title Case* anglo-saxon.
3. **Suppression du gras intraphrastique** : Ne jamais mettre de mots ou de membres de phrase en gras au milieu d'un paragraphe pour orienter artificiellement l'attention.
4. **Refus des listes à puces réflexes** : Rédiger en paragraphes continus. N'utiliser une liste que si le texte est strictement un inventaire technique, et jamais sous le format robotique `**Concept** : explication en une phrase`.
5. **Sobriété de la ponctuation** : Éviter les deux-points à répétition, les points d'exclamation emphatiques et les guillemets d'ironie autour d'expressions courantes. Uniformiser les apostrophes.

## 2. Architecture et structure (Anti-symétrie)

1. **Attaque directe (sans entonnoir)** : Supprimer toute phrase d'introduction généraliste sur l'époque, l'histoire ou l'importance du sujet. Entrer immédiatement dans le détail concret dès la première phrase.
2. **Arrêt net (sans conclusion morale)** : Ne jamais créer de section « Conclusion », « En résumé », « Héritage » ou « Perspectives ». Ne jamais terminer un texte par un paragraphe qui récapitule ce qui vient d'être dit ou qui ouvre sur l'avenir. S'arrêter sur le dernier fait ou argument concret.
3. **Asymétrie des paragraphes** : Casser le moule des sections composées invariablement de 2 ou 3 paragraphes de 4 lignes. Alterner des paragraphes denses et développés avec des paragraphes d'une seule phrase.
4. **Titres affirmatifs** : Ne jamais formuler un sous-titre sous forme de question rhétorique (« Pourquoi choisir X ? », « Comment fonctionne Y ? »).
5. **Densité non redondante** : Chaque paragraphe apporte un fait ou un angle neuf. Ne jamais reformuler l'idée du paragraphe précédent pour allonger artificiellement une section.

## 3. Rythme et syntaxe (Burstiness et Perplexité)

1. **Variation forcée de la longueur des phrases** : Ne jamais aligner trois phrases consécutives dans la plage de 15 à 25 mots. Briser systématiquement le rythme en insérant des phrases très courtes (3 à 7 mots) après une phrase longue.
2. **Éradication de la queue de phrase au participe présent** : Interdiction absolue de terminer une phrase par une virgule suivie d'un participe présent qui tire une conclusion abstraite (ex. *«, renforçant ainsi... »*, *«, soulignant l'importance de... »*, *«, offrant une meilleure... »*, *«, témoignant de... »*). Couper tout ce qui suit la virgule.
3. **Suppression des connecteurs scolaires en tête de phrase** : Bannir *De plus, En outre, Par ailleurs, En effet, Ainsi, Néanmoins, Toutefois, Par conséquent, Dans ce contexte* en début de phrase. Privilégier l'asyndète (juxtaposition directe de deux phrases dont le lien logique est implicite) ou des liaisons courtes (*Mais, Or, Sauf que, Résultat :*).
4. **Interdiction des rythmes ternaires d'adjectifs et de verbes** : Ne jamais aligner trois qualificatifs ou verbes synonymes (*« une architecture fiable, robuste et évolutive »*). Choisir un seul terme précis.
5. **Bannissement de la fausse antithèse** : Interdire les tournures rhétoriques du type *« Ce n'est pas seulement X, c'est Y »*, *« Plus qu'un simple X, il s'agit de Y »* ou *« Il ne s'agit pas de X, mais bien de Y »*.

## 4. Lexique et posture éditoriale

1. **Liste noire lexicale (Calques et clichés d'IA)** :
   - *Verbes bannis* : plonger (au cœur de), façonner, catalyser, témoigner de, naviguer (dans la complexité), débloquer, transcender, s'avérer (crucial/essentiel), mettre en lumière, redéfinir.
   - *Noms bannis* : tapisserie, paysage (numérique/technologique/médiatique), levier, pilier, pierre angulaire, catalyseur, symphonie, facette, écosystème (hors biologie), quête.
   - *Adjectifs et adverbes bannis* : crucial, fondamental, incontournable, indéniable, sans couture, vibrant, méticuleusement, véritablement, résolument, indéniablement.
   - *Locutions bannies* : Dans un monde en constante évolution, À l'ère de, Il convient de noter que, Force est de constater, Que vous soyez [A] ou [B], En fin de compte, Au-delà de.
2. **Factualité contre emphase** : Remplacer tout adjectif mélioratif vague par une mesure, un exemple précis ou un mécanisme technique.
3. **Fin du centrisme mou (Hedging)** : Éviter le balancement perpétuel *« D'un côté X présente des atouts, mais d'un autre côté Y comporte des limites, le choix dépend de vos besoins »*. Trancher clairement en donnant les critères réels d'arbitrage.
4. **Pas de sur-attribution** : Ne pas alourdir le texte avec des formules d'attribution (*« Selon la documentation officielle »*, *« Les spécialistes s'accordent à dire »*) lorsqu'il s'agit de faits établis ou évidents.

## 5. Protocole d'auto-vérification avant livraison

Avant de valider le texte généré, appliquer ces 5 filtres correctifs :

1. **Filtre des participes** : Traquer chaque virgule suivie d'un verbe en `-ant` en fin de phrase et supprimer le segment.
2. **Filtre d'élagage (Premier et dernier paragraphe)** : Vérifier si le texte fonctionne mieux en supprimant ses deux premières phrases et ses deux dernières phrases. Si aucune information technique ou factuelle n'est perdue, les supprimer.
3. **Filtre des connecteurs** : Vérifier le premier mot de chaque phrase. Si plus d'une phrase par paragraphe commence par un adverbe de liaison, supprimer ces adverbes.
4. **Filtre du rythme** : Vérifier qu'aucun paragraphe de plus de 4 phrases ne présente des phrases de longueur homogène.
5. **Filtre du ton** : S'assurer que l'humanisation n'a pas introduit de familiarité artificielle (*« Du coup »*, *« Bref »*, points d'exclamation). Le naturel vient de la précision et du rythme, pas du relâchement.