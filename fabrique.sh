#!/usr/bin/env bash
# La fabrique : lance les agents de l'équipe, chacun avec son rôle, sur le dossier chantier/.
#
# Usage :
#   ./fabrique.sh                 toute la chaîne, du plan au bilan
#   ./fabrique.sh analyste        un seul agent (plan, analyste, stratege, redacteur,
#                                 designer, relecteur, controleur, bilan)
#
# Variables :
#   CLI=agy | vibe | claude       l'agent en ligne de commande à utiliser (agy par défaut)
#   MARQUE=branding/agence.md     la charte à appliquer (celle du client par défaut)
#   REPASSES=2                    nombre maximum de corrections après un refus
#   DEMANDE=chantier/demande.md   la demande du client à traiter

set -uo pipefail
cd "$(dirname "$0")"

CLI="${CLI:-agy}"
MARQUE="${MARQUE:-branding/client-pattes-papilles.md}"
REPASSES="${REPASSES:-2}"
DEMANDE="${DEMANDE:-chantier/demande.md}"
LOGS="chantier/logs"
mkdir -p "$LOGS" chantier/livrables chantier/analyse chantier/controle
touch chantier/journal.md

# Couleurs du terminal, pour suivre qui travaille
bold=$(tput bold 2>/dev/null || true); reset=$(tput sgr0 2>/dev/null || true)

say() { echo "${bold}[$(date +%H:%M:%S)] $*${reset}"; }

# Lance un agent en mode non interactif. $1 = rôle, $2 = fichier de rôle, $3 = consigne en plus
run_agent() {
  local role="$1" fiche="$2" extra="${3:-}"
  local prompt="Tu es l'agent « ${role} » de la fabrique.
Lis d'abord AGENTS.md, puis ta fiche de rôle ${fiche}, et suis-les strictement.
La demande du client à traiter est dans ${DEMANDE}.
Charte à appliquer pour cette mission : ${MARQUE}.
${extra}
Travaille jusqu'au bout sans poser de question : si une information manque, note-le dans chantier/journal.md et continue."
  local log="$LOGS/$(date +%H%M%S)-${role}.log"
  say "▶ ${role} démarre (journal : ${log})"
  case "$CLI" in
    agy)    agy -p "$prompt" --dangerously-skip-permissions >"$log" 2>&1 ;;
    vibe)   vibe -p "$prompt" --auto-approve --trust >"$log" 2>&1 ;;
    claude) claude -p "$prompt" --dangerously-skip-permissions >"$log" 2>&1 ;;
    *)      echo "CLI inconnu : $CLI (agy, vibe ou claude)"; exit 1 ;;
  esac
  local code=$?
  if [ $code -eq 0 ]; then say "✔ ${role} a terminé"; else say "✖ ${role} s'est arrêté (code ${code}), voir ${log}"; fi
  return $code
}

# Lit le verdict d'un agent bloquant : 0 si OK, 1 sinon
verdict_ok() { [ -f "$1" ] && tail -n 3 "$1" | grep -q "VERDICT : OK"; }

etape() {
  case "$1" in
    plan)       run_agent chef-de-projet agents/chef-de-projet.md "Ta mission du jour : la mission de lancement (étape plan)." ;;
    analyste)   run_agent analyste agents/analyste.md ;;
    stratege)   run_agent stratege agents/stratege.md ;;
    redacteur)  run_agent redacteur agents/redacteur.md ;;
    designer)   run_agent designer agents/designer.md ;;
    relecteur)  run_agent relecteur agents/relecteur.md ;;
    controleur) run_agent controleur agents/controleur.md ;;
    bilan)      run_agent chef-de-projet agents/chef-de-projet.md "Ta mission du jour : la mission de clôture (étape bilan)." ;;
    *) echo "Étape inconnue : $1"; exit 1 ;;
  esac
}

if [ $# -gt 0 ]; then
  for e in "$@"; do etape "$e"; done
  exit 0
fi

say "Fabrique lancée avec ${CLI}, charte ${MARQUE}"
etape plan
etape analyste
etape stratege

# Le rédacteur et le designer travaillent en parallèle : chacun ses fichiers
etape redacteur & p1=$!
etape designer  & p2=$!
wait $p1 $p2

# Les deux contrôles bloquants tournent eux aussi en parallèle
for ((i = 0; i <= REPASSES; i++)); do
  etape relecteur & p1=$!
  etape controleur & p2=$!
  wait $p1 $p2
  if verdict_ok chantier/relecture.md && verdict_ok chantier/controle.md; then
    say "Les deux contrôles sont au vert"
    break
  fi
  if [ $i -eq "$REPASSES" ]; then
    say "Toujours refusé après ${REPASSES} repasses : un humain doit trancher (voir relecture.md et controle.md)"
    break
  fi
  say "Refusé, repasse $((i + 1)) sur ${REPASSES}"
  etape redacteur
  etape designer
done

etape bilan
say "Terminé. Livrables dans chantier/livrables/, bilan dans chantier/bilan.md"
