# La fabrique Pattes & Papilles

AI Week · jeudi 5 novembre 2026 · à distance

Aujourd'hui, votre agence ne travaille pas seule : elle pilote une équipe de sept agents IA. Chacun a un rôle écrit dans un fichier, tous partagent un dossier de chantier, deux d'entre eux peuvent bloquer la livraison. À la fin de la journée, une seule commande reconstruit tout votre livrable : diagnostic, tableau de bord, messages aux abonnés, business case, dossier et présentation.

C'est une version miniature de l'usine que Marius vous a montrée ce matin.

## Démarrer (9 h 20 · 15 minutes)

1. Connectez-vous à GitHub (créez un compte gratuit si besoin).
2. Sur cette page, bouton vert **Use this template**, puis **Open in a codespace**. Une équipe = un dépôt, chaque membre ouvre son propre Codespace sur le dépôt de l'équipe.
3. Attendez la fin de l'installation (2 à 3 minutes), puis ouvrez un terminal : menu ☰, **Terminal**, **New Terminal**.
4. Branchez **un** des deux agents :

| Agent | Connexion | Compte |
|---|---|---|
| **Antigravity CLI** (Google) | tapez `agy`, suivez le lien affiché, connectez-vous, puis `/quit` | compte Google gratuit |
| **Mistral Vibe** | créez une clé sur [console.mistral.ai](https://console.mistral.ai) (offre Experiment, gratuite), puis `vibe --setup` | compte Mistral gratuit |

5. Vérifiez : `agy -p "Dis bonjour en une phrase"` ou `vibe -p "Dis bonjour en une phrase"`.

Vous préférez le terminal de votre propre ordinateur ? C'est possible en SSH, voir la fin de `outils/antiseche-terminal.md`.

Le quota gratuit est limité : si un agent répond « quota » ou « 429 », passez à l'autre (`CLI=vibe ./fabrique.sh …`).

## Ce qu'il y a dans le dépôt

```
AGENTS.md                 les règles de l'usine, lues par chaque agent
agents/                   une fiche par rôle : chef de projet, analyste, stratège,
                          rédacteur, designer, relecteur, contrôleur
skills/redaction-humaine/ la skill d'écriture humaine construite en début de semaine
branding/                 la charte du client, et celle de votre agence (à remplir)
donnees/                  les données clients et leur dictionnaire
corpus/                   les documents de la marque
chantier/                 le dossier partagé où les agents travaillent
fabrique.sh               le chef d'orchestre
outils/                   l'antisèche du terminal, l'affichage des livrables
```

Le trajet d'une demande :

```
demande.md ─► chef de projet (plan)
                 │
                 ▼
             analyste ─► stratège ─┬─► rédacteur ─┐
                                   └─► designer  ─┤      en parallèle
                                                  ▼
                              relecteur ┬ contrôleur      bloquants, en parallèle
                                        │
                     refusé ? le rédacteur et le designer corrigent (2 fois au plus)
                                        ▼
                              chef de projet (bilan) ─► vous validez
```

## Atelier 0 · Le terminal sans peur (9 h 35 · 30 min)

Jusqu'ici, vous avez utilisé l'IA dans des fenêtres : ChatGPT, NotebookLM, Make. Pour qu'une équipe d'agents travaille seule, il faut descendre d'un étage, là où elle tourne vraiment : un serveur Linux, piloté depuis un terminal. Pas besoin de devenir développeur. Il suffit de douze commandes et de quatre réflexes, rassemblés dans `outils/antiseche-terminal.md`.

Chasse au trésor, à faire dans le terminal sans l'aide d'aucune IA :

1. Où êtes-vous ? (`pwd`) Qu'y a-t-il autour de vous ? (`ls`, puis `tree -L 1`)
2. Combien de clients compte `donnees/customers.csv` ? Attention, la première ligne est l'en-tête.
3. Affichez les 5 premières lignes de `donnees/abonnes_support.csv`. Comment s'appelle le chien de Damien ?
4. Combien de produits contiennent du saumon ? (`grep -i saumon donnees/products.csv`, puis ajoutez ` | wc -l`)
5. Ouvrez `AGENTS.md` avec `nano`, ajoutez votre prénom en dernière ligne, enregistrez, sortez. Vérifiez avec `tail -3 AGENTS.md`.
6. Bonus : ouvrez une session `tmux`, détachez-vous, revenez. Vous venez de faire ce que fait une usine d'agents toute la journée.

**Livrable** : les quatre réponses, dans le chat de l'équipe.

## Atelier 1 · Votre équipe d'agents (10 h 05 · 35 min)

1. Lisez `AGENTS.md` et deux fiches de rôle au choix.
2. Lancez un seul agent pour voir comment il travaille : `./fabrique.sh plan`. Ouvrez `chantier/plan.md`.
3. Adaptez l'usine à votre agence : ajoutez dans `AGENTS.md` trois règles tirées de la bataille des supports d'hier (ce qui a fait céder votre agent, ce qui l'a protégé).
4. Ajoutez ou modifiez un rôle. Exemples : un agent « juriste » qui vérifie le RGPD des messages, un agent « veille » qui lit les avis clients, un agent « avocat du diable » qui attaque le business case.

**Livrable** : votre `AGENTS.md` et vos fiches de rôle, commités (onglet Source Control, message, Commit, Sync).

## Atelier 2 · L'analyste et le stratège (10 h 40 · 1 h)

1. `./fabrique.sh analyste` : l'agent écrit et exécute du Python sur vos données. Suivez son travail dans un second terminal : `tail -f chantier/logs/*analyste.log`.
2. Ouvrez le tableau de bord : `./outils/voir.sh`, onglet **Ports**, globe à côté du port 8000, puis `livrables/tableau-de-bord.html`.
3. Vérifiez un chiffre vous-mêmes, dans `chantier/analyse/chiffres.md` puis dans les données. Faux ? Corrigez la fiche `agents/analyste.md`, pas le résultat, et relancez.
4. `./fabrique.sh stratege` : segments, plan d'action, business case, recommandation par abonné.

**Livrable** : un tableau de bord dont vous avez vérifié trois chiffres à la main.

## Atelier 3 · Toute la chaîne (11 h 40 · 45 min)

1. Ouvrez une session qui survivra à la pause : `tmux new -s fabrique`, puis `./fabrique.sh` lance toute l'équipe, du plan au bilan. `Ctrl+B` puis `D` pour vous détacher, `tmux attach -t fabrique` pour revenir.
2. Pendant qu'elle tourne, regardez `chantier/journal.md` se remplir.
3. Lisez `chantier/relecture.md` et `chantier/controle.md` : qu'est-ce qui a été refusé ? Le refus était-il juste ?
4. Lisez trois messages de `chantier/livrables/messages-abonnes.md` comme si vous étiez Nadia. Les enverriez-vous ?

**Livrable** : `chantier/bilan.md`, et votre avis d'humain écrit à la fin.

## Atelier 4 · Votre marque (après-midi · 1 h 15)

Le matin, la fabrique a travaillé aux couleurs du client. L'après-midi, elle passe à celles de votre agence.

1. Remplissez `branding/agence.md` : nom, couleurs, polices, ton. Vous pouvez demander trois pistes à un agent, mais c'est vous qui tranchez.
2. Relancez la mise en forme avec votre charte : `MARQUE=branding/agence.md ./fabrique.sh redacteur designer relecteur`.
3. Comparez les deux versions de la présentation. Gardez la meilleure base pour l'oral de demain.

**Livrable** : `chantier/livrables/dossier.md` et `chantier/livrables/presentation.html` aux couleurs de votre agence.

## Les règles du jeu

- Vous êtes les seuls décideurs. Un agent propose, un humain valide, et le bilan dit qui a fait quoi.
- On corrige les règles (`AGENTS.md`, fiches de rôle), pas les livrables à la main. C'est ce qui rend la fabrique réutilisable.
- Un chiffre qui ne vient pas de `donnees/` n'existe pas.
- Commitez souvent : si un agent casse quelque chose, on revient en arrière.
- La fabrique lance les agents sans leur demander la permission avant chaque commande : c'est ce qui les rend autonomes, et c'est aussi un risque. Un fichier piégé dans `donnees/` ou `corpus/` pourrait leur faire exécuter n'importe quoi. Faites-la tourner uniquement dans le Codespace, jamais sur votre ordinateur, et n'y mettez ni mot de passe ni clé autre que celle de l'agent.
