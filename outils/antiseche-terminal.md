# Antisèche · le terminal sans peur

Un terminal, c'est une conversation écrite avec un ordinateur. Vous tapez une commande, vous appuyez sur Entrée, il répond. Rien de plus.

## Les mots à connaître

| Mot | Ce que c'est | Dans la vraie vie |
|---|---|---|
| **Serveur** | Un ordinateur qui tourne ailleurs, sans écran, et qui ne s'éteint pas | Le site de votre banque, Make, ChatGPT tournent sur des serveurs |
| **Linux** | Le système d'exploitation de presque tous les serveurs du monde | L'équivalent de Windows ou macOS, sans les fenêtres |
| **Codespace** | Un petit serveur Linux que GitHub vous prête, avec un éditeur dans le navigateur | Votre bureau à distance pour la journée |
| **Terminal** | La fenêtre où l'on tape des commandes | La ligne de chat avec la machine |
| **SSH** | Le moyen sécurisé d'ouvrir un terminal sur un serveur à distance | Le badge qui ouvre la porte du bureau |
| **Processus** | Un programme en train de tourner | Un agent qui travaille |
| **tmux** | Un outil qui garde vos programmes en vie quand vous fermez la fenêtre | Laisser l'équipe travailler pendant que vous partez déjeuner |

## Les 12 commandes du jour

| Commande | Ce qu'elle fait | Exemple |
|---|---|---|
| `pwd` | Où suis-je ? | `pwd` |
| `ls` | Qu'y a-t-il ici ? | `ls donnees` |
| `cd` | Aller dans un dossier (`cd ..` pour remonter) | `cd chantier` |
| `tree` | Voir l'arborescence d'un coup d'œil | `tree -L 2` |
| `cat` | Afficher un fichier en entier | `cat AGENTS.md` |
| `head` | Afficher le début d'un fichier | `head -5 donnees/customers.csv` |
| `wc -l` | Compter les lignes | `wc -l donnees/customers.csv` |
| `grep` | Chercher un mot dans des fichiers | `grep -i saumon donnees/products.csv` |
| `nano` | Modifier un fichier dans le terminal (Ctrl+O pour enregistrer, Ctrl+X pour sortir) | `nano branding/agence.md` |
| `cp` | Copier un fichier | `cp agents/relecteur.md agents/juriste.md` |
| `tail -f` | Suivre un fichier qui se remplit en direct (Ctrl+C pour arrêter) | `tail -f chantier/journal.md` |
| `./fabrique.sh` | Lancer votre équipe d'agents | `./fabrique.sh analyste` |

## Les quatre réflexes

- **Tab** complète les noms de fichiers. Tapez `cat AG` puis Tab.
- **Flèche du haut** rappelle la commande précédente.
- **Ctrl+C** arrête ce qui tourne. Ça ne casse rien.
- Une erreur rouge n'est pas une catastrophe : lisez la dernière ligne, elle dit presque toujours ce qui manque.

## Garder la fabrique en vie (tmux)

```
tmux new -s fabrique       ouvre une session qui survit à la fermeture du terminal
./fabrique.sh              lance l'équipe
Ctrl+B puis D              on se détache : l'équipe continue sans vous
tmux attach -t fabrique    on revient voir où elle en est
```

## Se connecter en SSH depuis votre ordinateur (facultatif)

Le Codespace est un vrai serveur : vous pouvez y entrer depuis le terminal de votre propre machine, comme le font les développeurs et les administrateurs système.

1. Installez la ligne de commande GitHub sur votre ordinateur.
   - Windows : ouvrez PowerShell et tapez `winget install GitHub.cli`, puis fermez et rouvrez PowerShell.
   - Mac : téléchargez l'installeur sur [cli.github.com](https://cli.github.com) (ou `brew install gh` si vous avez Homebrew).
2. Connectez-vous : `gh auth login`, puis répondez GitHub.com, HTTPS, Login with a web browser.
3. Entrez dans votre Codespace : `gh codespace ssh`, choisissez-le dans la liste.
4. Vous voilà sur le serveur. `pwd`, `ls`, `tmux attach -t fabrique` : c'est la même machine que dans le navigateur.

Un Codespace s'arrête après 30 minutes sans activité. Pour laisser tourner la fabrique pendant la pause, allez dans les réglages GitHub, rubrique Codespaces, et passez le délai à 120 minutes.
