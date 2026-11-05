#!/usr/bin/env bash
# Installe tout ce qu'il faut à la création du Codespace
set -e
pip install --quiet -r requirements.txt
# Antigravity CLI (Google), gratuit avec un compte Google
curl -fsSL https://antigravity.google/cli/install.sh | bash || echo "Installation d'agy à refaire à la main"
# Mistral Vibe, gratuit avec une clé API de l'offre Experiment
pip install --quiet mistral-vibe || echo "Installation de Vibe à refaire à la main"
grep -q 'local/bin' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo "Fabrique prête. Lisez le README."
