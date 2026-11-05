#!/usr/bin/env bash
# Sert les livrables sur le port 8000 : ouvrez l'onglet « Ports » de Codespaces et cliquez sur le globe
cd "$(dirname "$0")/../chantier" && python3 -m http.server 8000
