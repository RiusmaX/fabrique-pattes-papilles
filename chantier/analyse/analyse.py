"""Analyse du churn Pattes & Papilles.

Lit donnees/, nettoie, calcule, écrit chiffres.md, les PNG et le tableau de bord HTML.
Usage : python3 -I chantier/analyse/analyse.py   (depuis la racine du projet)
"""
import base64
import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "donnees"
OUT = ROOT / "chantier" / "analyse"
LIV = ROOT / "chantier" / "livrables"
LIV.mkdir(parents=True, exist_ok=True)

# Charte Pattes & Papilles
SAPIN, TERRA, CREME, MOUTARDE, GRIS = "#1E4636", "#D9734E", "#FBF5EC", "#E8B04B", "#9A9A92"
available = {f.name for f in font_manager.fontManager.ttflist}
FONT_T = "Fraunces" if "Fraunces" in available else "DejaVu Serif"
FONT_B = "Inter" if "Inter" in available else "DejaVu Sans"
plt.rcParams.update({
    "figure.facecolor": CREME, "axes.facecolor": CREME, "savefig.facecolor": CREME,
    "font.family": FONT_B, "axes.edgecolor": GRIS, "axes.labelcolor": SAPIN,
    "xtick.color": SAPIN, "ytick.color": SAPIN, "text.color": SAPIN,
    "axes.spines.top": False, "axes.spines.right": False,
})

PHOTO = "2026-06-30"
HAUSSE = "2026-03-01"

# ---------------------------------------------------------------- nettoyage
journal_nettoyage = []
raw = pd.read_csv(DATA / "customers.csv", dtype={"department": str})
cust = raw.drop_duplicates().copy()
journal_nettoyage.append(f"{len(raw) - len(cust)} lignes en double supprimées ({len(raw)} lignes lues, {len(cust)} clients uniques)")
assert cust.customer_id.is_unique

canal_map = {"Facebook": "paid_social", "Paid Social": "paid_social"}
n_canal = cust.acquisition_channel.isin(canal_map).sum()
cust["acquisition_channel"] = cust.acquisition_channel.replace(canal_map)
n_chat = (cust.pet_species == "chat").sum()
cust["pet_species"] = cust.pet_species.replace({"chat": "cat"})
journal_nettoyage.append(f"{n_canal} libellés de canal corrigés (Facebook, Paid Social → paid_social) ; {n_chat} espèces « chat » → cat")

futur = cust.last_order_date > PHOTO
journal_nettoyage.append(f"{futur.sum()} client exclu : dernière commande datée après la photo du {PHOTO} (incohérent)")
cust = cust[~futur].copy()

n_age = (cust.pet_age_years > 20).sum()
n_poids = (cust.pet_weight_kg <= 0).sum()
journal_nettoyage.append(
    f"{n_age} animaux de plus de 20 ans et {n_poids} poids à 0 kg : laissés tels quels, ces colonnes ne servent pas aux calculs de départ")

orders_raw = pd.read_csv(DATA / "orders.csv")
orders = orders_raw[orders_raw.order_date <= PHOTO].copy()
journal_nettoyage.append(f"{len(orders_raw) - len(orders)} lignes de commande postérieures au {PHOTO} écartées (le dictionnaire annonce des commandes jusqu'à cette date)")
orders = orders[orders.customer_id.isin(cust.customer_id)]

cust["last_month"] = cust.last_order_date.str[:7]
cust["after_march"] = cust.last_order_date >= HAUSSE
N = len(cust)
sub = cust[cust.plan == "subscription"].copy()
one = cust[cust.plan == "one_off"].copy()


def rate(df):
    return df.churned.mean() * 100


def by(df, col, order=None):
    g = df.groupby(col, dropna=False).churned.agg(["size", "sum", "mean"])
    g["pct"] = g["mean"] * 100
    g = g.rename(columns={"size": "n", "sum": "partis"})
    if order is not None:
        g = g.reindex(order)
    return g[["n", "partis", "pct"]]


def eur(x):
    return f"{x:,.0f} €".replace(",", " ")


V = {}  # valeurs clés réutilisées dans le HTML
L = []  # lignes de chiffres.md


def table(g, label):
    L.append(f"| {label} | Clients | Partis | Churn |")
    L.append("|---|---:|---:|---:|")
    for k, r in g.dropna().iterrows():
        L.append(f"| {k} | {int(r.n)} | {int(r.partis)} | {r.pct:.1f} % |")
    L.append("")


# ---------------------------------------------------------------- 1. churn global
V["n"] = N
V["churn_all"] = rate(cust)
V["partis_all"] = int(cust.churned.sum())
V["churn_sub"], V["n_sub"], V["partis_sub"] = rate(sub), len(sub), int(sub.churned.sum())
V["churn_one"], V["n_one"], V["partis_one"] = rate(one), len(one), int(one.churned.sum())

L += [
    "# Chiffres clés : churn Pattes & Papilles",
    "",
    "Source unique de tous les chiffres du dossier, de la présentation et des messages. Généré par `chantier/analyse/analyse.py`, à partir de `donnees/`.",
    "",
    "## À lire avant d'utiliser un chiffre",
    "",
    f"- Échantillon de {N} clients en portefeuille au 30 juin 2026, pas la base de 18 000 clients actifs. La part d'abonnés y est plus forte (dictionnaire, point 3). Ne pas multiplier ces chiffres pour parler de toute la base.",
    "- Une seule fenêtre de départ : du 1er juillet au 30 septembre 2026 (3 mois). Il n'existe pas de série mensuelle de départs dans les données. Les « churn par mois » ci-dessous sont groupés par mois de dernière commande.",
    "- Le mot « churn » ne veut pas dire la même chose pour les deux formules. Abonné : a résilié. Achat ponctuel : n'a rien commandé sur la période. Les deux taux ne se comparent pas et ne s'additionnent pas sans le dire.",
    "- Corrélation n'est pas cause. Un signal qui précède un départ n'en est pas forcément la raison.",
    "- Les montants sont en euros TTC.",
    "",
    "## Nettoyage appliqué",
    "",
]
L += [f"- {x}" for x in journal_nettoyage]
L += [
    "",
    "## 1. Churn global (colonne `churned`, `customers.csv`)",
    "",
    "| Mesure | Valeur | Calcul |",
    "|---|---:|---|",
    f"| Clients analysés | {N} | lignes uniques de `customers.csv` après nettoyage |",
    f"| Partis, tous clients | {V['partis_all']} ({V['churn_all']:.1f} %) | somme de `churned` / clients |",
    f"| Abonnés | {V['n_sub']} | `plan` = subscription |",
    f"| Abonnés partis | {V['partis_sub']} ({V['churn_sub']:.1f} %) | résiliations 1er juillet au 30 septembre 2026 |",
    f"| Achats ponctuels | {V['n_one']} | `plan` = one_off |",
    f"| Ponctuels sans commande sur la période | {V['partis_one']} ({V['churn_one']:.1f} %) | pas de commande du 1er juillet au 30 septembre 2026 |",
    "",
]

# ---------------------------------------------------------------- 2. par mois de dernière commande
L += ["## 2. Churn par mois de dernière commande (`last_order_date`)", ""]
mois = sorted(cust.last_month.unique())
g_all = by(cust, "last_month")
g_sub = by(sub, "last_month")
g_one = by(one, "last_month")
L.append("| Mois | Tous : clients | Tous : churn | Abonnés : clients | Abonnés : churn | Ponctuels : clients | Ponctuels : churn |")
L.append("|---|---:|---:|---:|---:|---:|---:|")
for m in mois:
    a, s, o = g_all.loc[m], g_sub.reindex([m]).iloc[0], g_one.reindex([m]).iloc[0]
    fs = f"{s.pct:.1f} %" if s.n == s.n else "n/a"
    fo = f"{o.pct:.1f} %" if o.n == o.n else "n/a"
    L.append(f"| {m} | {int(a.n)} | {a.pct:.1f} % | {int(s.n) if s.n == s.n else 0} | {fs} | {int(o.n) if o.n == o.n else 0} | {fo} |")
L.append("")

L += ["### Avant et après le 1er mars 2026 (hausse de prix de 5 %)", ""]
ba = by(cust, "after_march").rename(index={False: "dernière commande avant le 1er mars 2026", True: "dernière commande le 1er mars 2026 ou après"})
table(ba, "Tous clients")
ba_s = by(sub, "after_march").rename(index={False: "dernière commande avant le 1er mars 2026", True: "dernière commande le 1er mars 2026 ou après"})
table(ba_s, "Abonnés")
ba_o = by(one, "after_march").rename(index={False: "dernière commande avant le 1er mars 2026", True: "dernière commande le 1er mars 2026 ou après"})
table(ba_o, "Ponctuels")
L += [
    "Lecture : chez les ponctuels, plus la dernière commande est ancienne, plus le « départ » est mécanique (pas de commande sur 3 mois de plus). Cette partie du tableau ne mesure pas l'effet de la hausse de prix. Chez les abonnés, les dernières commandes d'avant mars sont très peu nombreuses (voir effectifs) : on ne conclut rien sur elles.",
    "",
]
V["sub_before_n"] = int(((sub.last_order_date < HAUSSE)).sum())
L.append(f"Abonnés dont la dernière commande date d'avant le 1er mars 2026 : {V['sub_before_n']}. Un abonné actif commande au moins tous les 6 semaines : la comparaison avant/après par date de dernière commande est donc impossible pour eux.")
L.append("")

# cohorte d'inscription (abonnés)
sub["cohorte"] = (sub.signup_date >= HAUSSE).map({False: "inscrits avant le 1er mars 2026", True: "inscrits le 1er mars 2026 ou après"})
co = by(sub, "cohorte")
L += ["### Abonnés selon la date d'inscription (`signup_date`)", ""]
table(co, "Cohorte")
V["co_avant"] = co.loc["inscrits avant le 1er mars 2026"]
V["co_apres"] = co.loc["inscrits le 1er mars 2026 ou après"]

# ---------------------------------------------------------------- 3. segments
ch_order = ["organic_search", "paid_search", "paid_social", "referral", "influencer", "direct"]
ch_lbl = {"organic_search": "Référencement\nnaturel", "paid_search": "Publicité\nGoogle", "paid_social": "Publicité\nMeta",
          "referral": "Parrainage", "influencer": "Créateurs", "direct": "Direct"}
L += ["## 3. Churn par segment", ""]
for nom, df in (("Abonnés", sub), ("Ponctuels", one)):
    L.append(f"### {nom}, par canal d'acquisition (`acquisition_channel`)")
    L.append("")
    table(by(df, "acquisition_channel", ch_order), "Canal")
ch_s = by(sub, "acquisition_channel", ch_order)
V["ch_s"] = ch_s

for nom, df in (("Abonnés", sub), ("Ponctuels", one)):
    L.append(f"### {nom}, par espèce (`pet_species`)")
    L.append("")
    table(by(df, "pet_species", ["dog", "cat"]), "Espèce")
sp_s = by(sub, "pet_species", ["dog", "cat"])
V["sp_s"] = sp_s

L.append("### Abonnés, par formule (`delivery_weeks`, rythme de livraison)")
L.append("")
fo_s = by(sub, "delivery_weeks", [4.0, 5.0, 6.0])
fo_s.index = ["toutes les 4 semaines", "toutes les 5 semaines", "toutes les 6 semaines"]
table(fo_s, "Rythme")
V["fo_s"] = fo_s
L.append("Les ponctuels n'ont pas de formule (colonne vide, non comptée comme zéro).")
L.append("")

for nom, df in (("Abonnés", sub), ("Ponctuels", one)):
    L.append(f"### {nom}, par remise de bienvenue (`welcome_discount_pct`)")
    L.append("")
    g = by(df, "welcome_discount_pct", [0, 20, 30])
    g.index = ["0 %", "20 %", "30 %"]
    table(g, "Remise")
re_s = by(sub, "welcome_discount_pct", [0, 20, 30])
re_s.index = ["0 %", "20 %", "30 %"]
V["re_s"] = re_s

# Remise et canal : la remise est-elle un simple reflet du canal ?
x = pd.crosstab(sub.acquisition_channel, sub.welcome_discount_pct, normalize="index") * 100
L.append("### Remise de bienvenue selon le canal (abonnés, part des clients du canal)")
L.append("")
L.append("| Canal | 0 % | 20 % | 30 % |")
L.append("|---|---:|---:|---:|")
for k in ch_order:
    L.append(f"| {k} | {x.loc[k].get(0, 0):.0f} % | {x.loc[k].get(20, 0):.0f} % | {x.loc[k].get(30, 0):.0f} % |")
L.append("")
L.append("Remise et canal vont ensemble (parrainage et créateurs donnent 20 ou 30 %) : on ne peut pas dire laquelle des deux pèse sur le départ sans analyse plus poussée.")
L.append("")

L.append("### Abonnés, par sensibilité déclarée (`sensitivity`)")
L.append("")
table(by(sub, "sensitivity", ["none", "digestive", "skin", "overweight"]), "Sensibilité")


# chats abonnés selon achat de saumon depuis le 4 mai 2026 (lancement de la recette chat au saumon)
L += ["### Abonnés chats : achat de produits au saumon depuis le 4 mai 2026", ""]
prod0 = pd.read_csv(DATA / "products.csv")
oo = orders.merge(prod0[["product_id", "species", "recipe", "category"]], on="product_id")
oo = oo[(oo.quantity > 0) & (oo.species.isin(["cat", "both"])) & (oo.category.isin(["kibble", "wet"]))]
oo_s = oo[(oo.recipe == "salmon") & (oo.order_date >= "2026-05-04")]
chats = sub[sub.pet_species == "cat"].copy()
chats["saumon"] = chats.customer_id.isin(oo_s.customer_id).map({True: "a acheté du saumon depuis le 4 mai", False: "n'a pas acheté de saumon depuis le 4 mai"})
sa = by(chats, "saumon")
table(sa, "Abonnés chats")
sa_oui = sa.loc["a acheté du saumon depuis le 4 mai"]
sa_non = sa.loc["n'a pas acheté de saumon depuis le 4 mai"]
V["sa_oui"], V["sa_non"] = sa_oui, sa_non
V["sa"] = sa
dogs = sub[sub.pet_species == "dog"]
L.append("Lecture : l'écart est très net, mais il ne prouve pas que le saumon cause le départ. Les produits au saumon du catalogue existent depuis 2021 (`launch_date`) et les données ne repèrent pas la « nouvelle recette » du 4 mai : « saumon » désigne ici tout produit chat au saumon (croquettes ou sachets). Les motifs déclarés vont dans le même sens (voir section 5 : « animal refuse » en tête chez les abonnés). À confirmer avec le service qualité avant toute conclusion.")
L.append("")
chats_c = by(chats, "sensitivity", ["none", "digestive", "skin", "overweight"])
L.append("Abonnés chats, par sensibilité déclarée :")
L.append("")
table(chats_c, "Sensibilité")

# ---------------------------------------------------------------- 4. signaux
L += ["## 4. Signaux qui précèdent un départ", ""]
L.append("Colonnes `skipped_deliveries_90d` (abonnés seulement), `late_deliveries_12m`, `support_tickets_12m`, `last_review_score`.")
L.append("")

sk = by(sub, "skipped_deliveries_90d", [0.0, 1.0, 2.0])
sk.index = ["0", "1", "2"]
L.append("### Abonnés, livraisons décalées sur 90 jours")
L.append("")
table(sk, "Livraisons décalées")

def bucket(s, top):
    return s.clip(upper=top).astype(int).astype(str).replace({str(top): f"{top} ou plus"})

sub["late_b"] = bucket(sub.late_deliveries_12m, 3)
one["late_b"] = bucket(one.late_deliveries_12m, 3)
lt = by(sub, "late_b", ["0", "1", "2", "3 ou plus"])
L.append("### Abonnés, colis en retard sur 12 mois")
L.append("")
table(lt, "Retards")
L.append("### Ponctuels, colis en retard sur 12 mois")
L.append("")
table(by(one, "late_b", ["0", "1", "2", "3 ou plus"]), "Retards")

sub["tk_b"] = bucket(sub.support_tickets_12m, 3)
one["tk_b"] = bucket(one.support_tickets_12m, 3)
tk = by(sub, "tk_b", ["0", "1", "2", "3 ou plus"])
L.append("### Abonnés, tickets au service client sur 12 mois")
L.append("")
table(tk, "Tickets")
L.append("### Ponctuels, tickets au service client sur 12 mois")
L.append("")
table(by(one, "tk_b", ["0", "1", "2", "3 ou plus"]), "Tickets")

sub["rev"] = sub.last_review_score.map(lambda v: "aucun avis" if pd.isna(v) else f"{int(v)} sur 5")
one["rev"] = one.last_review_score.map(lambda v: "aucun avis" if pd.isna(v) else f"{int(v)} sur 5")
rev_order = ["aucun avis", "1 sur 5", "2 sur 5", "3 sur 5", "4 sur 5", "5 sur 5"]
rv = by(sub, "rev", rev_order)
L.append("### Abonnés, note du dernier avis (« aucun avis » = colonne vide, jamais comptée comme une note)")
L.append("")
table(rv, "Dernier avis")
L.append("### Ponctuels, note du dernier avis")
L.append("")
table(by(one, "rev", rev_order), "Dernier avis")
V["sk"], V["lt"], V["tk"], V["rv"] = sk, lt, tk, rv

# note basse = 1 à 3
bas = sub[sub.last_review_score.between(1, 3)]
haut = sub[sub.last_review_score.between(4, 5)]
V["bas"], V["haut"] = rate(bas), rate(haut)
V["bas_n"], V["haut_n"] = len(bas), len(haut)
L.append(f"Regroupement abonnés : note de 1 à 3 → {V['bas']:.1f} % de churn ({V['bas_n']} clients) ; note de 4 ou 5 → {V['haut']:.1f} % ({V['haut_n']} clients).")
L.append("")

# cumul de signaux
sub["nb_signaux"] = ((sub.skipped_deliveries_90d >= 1).astype(int) + (sub.late_deliveries_12m >= 1).astype(int)
                     + (sub.support_tickets_12m >= 1).astype(int) + sub.last_review_score.between(1, 3).astype(int))
cum = by(sub, "nb_signaux", [0, 1, 2, 3, 4])
cum.index = [f"{i} signal" + ("" if i < 2 else "ux") for i in cum.index]
L.append("### Abonnés, cumul de signaux (livraison décalée, retard, ticket, note de 1 à 3)")
L.append("")
table(cum.dropna(), "Signaux cumulés")
V["cum"] = cum

# ---------------------------------------------------------------- 5. motifs
L += ["## 5. Raisons de départ déclarées (`churn_reason`)", ""]
partis = cust[cust.churned == 1]
hors = cust[(cust.churned == 0) & cust.churn_reason.notna()]
L.append(f"- Clients partis : {len(partis)}, dont {int(partis.churn_reason.notna().sum())} avec un motif connu et {int(partis.churn_reason.isna().sum())} sans motif (colonne vide, ne pas lire comme « autre »).")
L.append(f"- Clients restés avec un motif renseigné : {len(hors)} (attendu : 0).")
L.append("")
lbl_reason = {"price": "Prix", "other": "Autre", "delivery_issues": "Livraison", "switched_competitor": "Concurrent",
              "pet_refused_food": "Animal refuse", "too_much_stock": "Trop de stock", "moved_to_vet_diet": "Régime vétérinaire",
              "pet_deceased": "Animal décédé"}
mr = partis.churn_reason.value_counts()
nk = int(mr.sum())
L.append("| Motif | Partis | Part des motifs connus |")
L.append("|---|---:|---:|")
for k, v in mr.items():
    L.append(f"| {lbl_reason[k]} (`{k}`) | {v} | {v / nk * 100:.1f} % |")
L.append("")
V["mr"], V["nk"], V["n_partis_nomotif"] = mr, nk, int(partis.churn_reason.isna().sum())
for nom, df in (("abonnés", sub), ("ponctuels", one)):
    p = df[df.churned == 1]
    c = p.churn_reason.value_counts()
    L.append(f"Motifs des {nom} partis ({int(c.sum())} motifs connus sur {len(p)} partis) : " + ", ".join(f"{lbl_reason[k]} {v}" for k, v in c.items()) + ".")
    L.append("")
V["mr_sub"] = sub[sub.churned == 1].churn_reason.value_counts()
V["mr_one"] = one[one.churned == 1].churn_reason.value_counts()
V["refus_sub_pct"] = V["mr_sub"].get("pet_refused_food", 0) / V["mr_sub"].sum() * 100
V["price_one_pct"] = V["mr_one"].get("price", 0) / V["mr_one"].sum() * 100
V["nk_sub"], V["nk_one"] = int(V["mr_sub"].sum()), int(V["mr_one"].sum())
# "prix + concurrent" : seulement ce que le client dit
V["price_pct"] = mr.get("price", 0) / nk * 100
V["deliv_pct"] = mr.get("delivery_issues", 0) / nk * 100
V["comp_pct"] = mr.get("switched_competitor", 0) / nk * 100
V["refus_pct"] = mr.get("pet_refused_food", 0) / nk * 100

# ---------------------------------------------------------------- 6. CA perdu
L += ["## 6. Chiffre d'affaires perdu (12 mois précédant le 30 juin 2026)", ""]
ca = orders.groupby("customer_id").line_total_eur.sum()
ncmd = orders.groupby("customer_id").order_id.nunique()
cust["ca12"] = cust.customer_id.map(ca).fillna(0.0)
cust["cmd12"] = cust.customer_id.map(ncmd).fillna(0)
sub["ca12"] = sub.customer_id.map(ca).fillna(0.0)
one["ca12"] = one.customer_id.map(ca).fillna(0.0)
sans_cmd = int((cust.cmd12 == 0).sum())
V["ca_tot"] = cust.ca12.sum()
V["ca_perdu"] = cust.loc[cust.churned == 1, "ca12"].sum()
V["ca_perdu_sub"] = sub.loc[sub.churned == 1, "ca12"].sum()
V["ca_perdu_one"] = one.loc[one.churned == 1, "ca12"].sum()
V["ca_moy_sub_parti"] = sub.loc[sub.churned == 1, "ca12"].mean()
V["ca_moy_sub_reste"] = sub.loc[sub.churned == 0, "ca12"].mean()
V["ca_moy_one_parti"] = one.loc[one.churned == 1, "ca12"].mean()
V["pct_ca_perdu"] = V["ca_perdu"] / V["ca_tot"] * 100
V["pct_ca_perdu_sub"] = V["ca_perdu_sub"] / sub.ca12.sum() * 100
L += [
    "Définition : somme de `line_total_eur` (remboursements déduits) des commandes du 1er juillet 2025 au 30 juin 2026 des clients partis (`orders.csv`). C'est le CA annuel que ces clients représentaient, pas un CA futur garanti. Pour un ponctuel « parti », c'est une absence de commande, pas une résiliation : le CA n'est pas forcément perdu.",
    f"{sans_cmd} clients n'ont aucune commande sur ces 12 mois (leur CA vaut 0, ils sont comptés).",
    "",
    "| Mesure | Valeur | Calcul |",
    "|---|---:|---|",
    f"| CA 12 mois, tous clients de l'échantillon | {eur(V['ca_tot'])} | somme de `line_total_eur` |",
    f"| CA 12 mois des clients partis | {eur(V['ca_perdu'])} ({V['pct_ca_perdu']:.1f} % du CA) | clients avec `churned` = 1 |",
    f"| dont abonnés partis | {eur(V['ca_perdu_sub'])} ({V['pct_ca_perdu_sub']:.1f} % du CA des abonnés) | `plan` = subscription, `churned` = 1 |",
    f"| dont ponctuels sans commande | {eur(V['ca_perdu_one'])} | `plan` = one_off, `churned` = 1 |",
    f"| CA 12 mois moyen d'un abonné parti | {eur(V['ca_moy_sub_parti'])} | moyenne sur {V['partis_sub']} abonnés |",
    f"| CA 12 mois moyen d'un abonné resté | {eur(V['ca_moy_sub_reste'])} | moyenne sur {V['n_sub'] - V['partis_sub']} abonnés |",
    f"| CA 12 mois moyen d'un ponctuel sans commande | {eur(V['ca_moy_one_parti'])} | moyenne sur {V['partis_one']} clients |",
    "",
    "Ces montants valent pour l'échantillon de presque 2 000 clients, pas pour les 18 000 clients actifs. Aucune extrapolation n'est faite ici : la part d'abonnés de l'échantillon est plus forte que celle de la base.",
    "",
]

# CA perdu par motif (abonnés + ponctuels)
cr = cust[cust.churned == 1].copy()
cr["motif"] = cr.churn_reason.map(lbl_reason).fillna("Motif inconnu")
ca_mot = cr.groupby("motif").agg(clients=("ca12", "size"), ca=("ca12", "sum")).sort_values("ca", ascending=False)
L.append("### CA 12 mois des partis, par motif (tous clients partis)")
L.append("")
L.append("| Motif | Partis | CA 12 mois |")
L.append("|---|---:|---:|")
for k, r in ca_mot.iterrows():
    L.append(f"| {k} | {int(r.clients)} | {eur(r.ca)} |")
L.append("")
V["ca_mot"] = ca_mot

# ---------------------------------------------------------------- 7. autres repères
L += ["## 7. Repères complémentaires", ""]
# remboursements de croquettes par mois
prod = pd.read_csv(DATA / "products.csv")
ok = orders.merge(prod[["product_id", "category"]], on="product_id")
ok = ok[ok.category == "kibble"].copy()
ok["m"] = ok.order_date.str[:7]
ok["ref"] = ok.quantity < 0
rf = ok.groupby("m").agg(lignes=("ref", "size"), remb=("ref", "sum"))
rf["pct"] = rf.remb / rf.lignes * 100
L.append("### Remboursements de croquettes (`orders.csv`, lignes avec quantité négative / lignes de croquettes)")
L.append("")
L.append("| Mois | Lignes de croquettes | Remboursées | Part |")
L.append("|---|---:|---:|---:|")
for m, r in rf.iterrows():
    L.append(f"| {m} | {int(r.lignes)} | {int(r.remb)} | {r.pct:.2f} % |")
L.append("")
V["rf_fev"], V["rf_juin"] = rf.loc["2026-02", "pct"], rf.loc["2026-06", "pct"]
L.append("Les volumes sont faibles (quelques dizaines de lignes). Les données ne disent pas la cause des remboursements ni le transporteur : le lien avec le changement de transporteur du 2 mars ou la recette au saumon du 4 mai ne peut pas être établi ici.")
L.append("")

# retards par département
dep = cust.groupby("department").agg(n=("churned", "size"), retard=("late_deliveries_12m", "mean"), churn=("churned", "mean"))
dep = dep[dep.n >= 30].sort_values("retard", ascending=False)
L.append("### Départements (au moins 30 clients) : retards de livraison moyens sur 12 mois")
L.append("")
L.append("| Département | Clients | Retards par client | Churn |")
L.append("|---|---:|---:|---:|")
for k, r in dep.head(5).iterrows():
    L.append(f"| {k} | {int(r.n)} | {r.retard:.2f} | {r['churn'] * 100:.1f} % |")
L.append("")
L.append(f"Moyenne de l'échantillon : {cust.late_deliveries_12m.mean():.2f} retard par client. Écarts à lire avec prudence vu les petits effectifs.")
L.append("")

# abonnés à risque du fichier support
sup = pd.read_csv(DATA / "abonnes_support.csv")
sup_plan = sup.plan.value_counts()
L.append("### Fichier `abonnes_support.csv` (les 20 clients à risque)")
L.append("")
L.append(f"- {len(sup)} clients : {sup_plan.get('abonnement', 0)} abonnés et {sup_plan.get('achat ponctuel', 0)} achats ponctuels.")
L.append(f"- Sensibilités déclarées : " + ", ".join(f"{k} {v}" for k, v in sup.sensitivity.value_counts().items()) + ".")
V["sup_sub"], V["sup_one"] = sup_plan.get("abonnement", 0), sup_plan.get("achat ponctuel", 0)
L.append("")

# ---------------------------------------------------------------- graphiques
def finish(fig, name, titre, sous=None):
    fig.subplots_adjust(top=0.84, bottom=0.2)
    fig.suptitle(titre, fontfamily=FONT_T, fontweight="bold", fontsize=15, color=SAPIN, x=0.02, ha="left", y=0.98)
    if sous:
        fig.text(0.02, 0.01, sous, fontsize=8, color=GRIS, ha="left", va="bottom")
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight")
    plt.close(fig)


def bars(ax, labels, vals, ns, hi=None, ref=None, fmt="{:.0f} %"):
    cols = [TERRA if (hi is not None and i == hi) else SAPIN for i in range(len(vals))]
    ax.bar(range(len(vals)), vals, color=cols, width=0.65)
    for i, (v, n) in enumerate(zip(vals, ns)):
        ax.text(i, v + max(vals) * 0.02, fmt.format(v), ha="center", fontsize=9, fontweight="bold", color=SAPIN)
        ax.text(i, -max(vals) * 0.02, f"n={int(n)}", ha="center", va="top", fontsize=7.5, color=GRIS)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.tick_params(axis="x", pad=14)
    ax.set_ylim(0, max(vals) * 1.18)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    if ref is not None:
        ax.axhline(ref, color=MOUTARDE, lw=1.6, ls="--")


# 1. deux départs qui ne se ressemblent pas : plan + mois de dernière commande
fig, axs = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw={"width_ratios": [1, 2.2]})
bars(axs[0], ["Abonnés\n(ont résilié)", "Achats ponctuels\n(sans commande)"], [V["churn_sub"], V["churn_one"]],
     [V["n_sub"], V["n_one"]], hi=0)
axs[0].set_title("Churn sur 3 mois", fontsize=10, color=SAPIN, loc="left")
mm = [m for m in mois if m >= "2026-01"]
for df, col, nom in ((sub, TERRA, "Abonnés"), (one, SAPIN, "Ponctuels")):
    g = by(df, "last_month").reindex(mm)
    g = g[g.n >= 10]
    xs = [mm.index(m) for m in g.index]
    axs[1].plot(xs, g.pct, marker="o", color=col, lw=2.2, label=nom)
    for x_, y_ in zip(xs, g.pct):
        axs[1].text(x_, y_ + 3, f"{y_:.0f} %", ha="center", fontsize=8, color=col)
axs[1].set_xticks(range(len(mm)))
axs[1].set_xticklabels(mm, fontsize=8.5)
axs[1].set_ylim(0, 105)
axs[1].set_title("Churn selon le mois de dernière commande (mois de 10 clients ou plus)", fontsize=10, color=SAPIN, loc="left")
axs[1].legend(frameon=False, fontsize=9, loc="upper right")
axs[1].set_yticks([])
axs[1].spines["left"].set_visible(False)
finish(fig, "01-churn-plan-et-mois.png",
       f"Un abonné sur {round(100 / V['churn_sub'])} part en 3 mois ; chez les ponctuels, {V['churn_one']:.0f} % ne recommandent rien",
       "Source : customers.csv, 30 juin 2026, départs du 1er juillet au 30 septembre. Définitions différentes selon la formule.")

# 2. canal
fig, ax = plt.subplots(figsize=(9, 4.6))
vals = ch_s.pct.values
hi = int(vals.argmax())
bars(ax, [ch_lbl[c] for c in ch_order], vals, ch_s.n.values, hi=hi, ref=V["churn_sub"])
finish(fig, "02-churn-canal.png",
       f"Chez les abonnés, le canal pèse peu : de {vals.min():.0f} % à {vals.max():.0f} % de churn selon l'origine",
       "Source : customers.csv, abonnés uniquement. Lecture : écart de canal fiable seulement avec un effectif suffisant (n indiqué).")

# 3. espèce, saumon, remise
fig, axs = plt.subplots(1, 3, figsize=(12, 4.4))
bars(axs[0], ["Chien", "Chat"], sp_s.pct.values, sp_s.n.values, hi=int(sp_s.pct.values.argmax()), ref=V["churn_sub"])
axs[0].set_title("Abonnés selon l'espèce", fontsize=10, loc="left")
bars(axs[1], ["Pas de saumon\ndepuis le 4 mai", "Saumon acheté\ndepuis le 4 mai"], [V["sa_non"].pct, V["sa_oui"].pct],
     [V["sa_non"].n, V["sa_oui"].n], hi=1, ref=sp_s.pct.loc["cat"])
axs[1].set_title("Abonnés chats selon le saumon", fontsize=10, loc="left")
bars(axs[2], list(re_s.index), re_s.pct.values, re_s.n.values, hi=int(re_s.pct.values.argmax()), ref=V["churn_sub"])
axs[2].set_title("Abonnés selon la remise de bienvenue", fontsize=10, loc="left")
finish(fig, "03-churn-profil.png",
       f"Les abonnés chats partent {str(round(sp_s.pct.loc['cat'] / sp_s.pct.loc['dog'], 1)).replace('.', ',')} fois plus que les chiens, et {V['sa_oui'].pct:.0f} % de ceux qui ont pris du saumon",
       "Source : customers.csv et orders.csv, abonnés. Pointillé : moyenne du groupe. Saumon non démontré comme cause : voir chiffres.md.")

# 4. signaux
fig, axs = plt.subplots(1, 4, figsize=(14, 4.4))
bars(axs[0], ["0", "1", "2"], sk.pct.values, sk.n.values, hi=int(sk.pct.values.argmax()), ref=V["churn_sub"])
axs[0].set_title("Livraisons décalées (90 j)", fontsize=10, loc="left")
bars(axs[1], ["0", "1", "2", "3+"], lt.pct.values, lt.n.values, hi=int(lt.pct.values.argmax()), ref=V["churn_sub"])
axs[1].set_title("Colis en retard (12 mois)", fontsize=10, loc="left")
bars(axs[2], ["0", "1", "2", "3+"], tk.pct.values, tk.n.values, hi=int(tk.pct.values.argmax()), ref=V["churn_sub"])
axs[2].set_title("Tickets service client (12 mois)", fontsize=10, loc="left")
rv2 = rv.dropna()
bars(axs[3], ["aucun", "1", "2", "3", "4", "5"][: len(rv2)], rv2.pct.values, rv2.n.values, hi=None, ref=V["churn_sub"])
axs[3].set_title("Note du dernier avis", fontsize=10, loc="left")
finish(fig, "04-signaux.png",
       f"Livraisons décalées et tickets annoncent un départ ; les retards de colis, pas de façon nette",
       "Source : customers.csv, abonnés, signaux avant le 30 juin. Pointillé : moyenne des abonnés. Petits effectifs à droite de chaque panneau. Un signal annonce, il n'explique pas.")

# 5. motifs, abonnés et ponctuels
fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
for ax, ser, nom in ((axs[0], V["mr_sub"], "Abonnés partis"), (axs[1], V["mr_one"], "Ponctuels sans commande")):
    tot = ser.sum()
    so = ser.sort_values()
    ax.barh([lbl_reason[k] for k in so.index], so.values / tot * 100,
            color=[TERRA if k == ser.index[0] else SAPIN for k in so.index])
    for i, v in enumerate(so.values):
        ax.text(v / tot * 100 + 0.6, i, f"{v / tot * 100:.0f} % ({v})", va="center", fontsize=8.5)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(0, so.max() / tot * 100 * 1.3)
    ax.set_title(f"{nom} ({int(tot)} motifs connus)", fontsize=10, loc="left")
finish(fig, "05-motifs.png",
       f"Abonnés : l'animal refuse la nourriture dans {V['refus_sub_pct']:.0f} % des cas ; ponctuels : le prix dans {V['price_one_pct']:.0f} %",
       f"Source : customers.csv, churn_reason. {V['n_partis_nomotif']} partis sur {V['partis_all']} n'ont aucun motif et ne sont pas comptés.")

# 6. CA perdu
fig, ax = plt.subplots(figsize=(9, 4.6))
cm = ca_mot.sort_values("ca")
cols = [TERRA if k == ca_mot.index[0] else SAPIN for k in cm.index]
ax.barh(cm.index, cm.ca.values, color=cols)
for i, v in enumerate(cm.ca.values):
    ax.text(v + cm.ca.max() * 0.01, i, f"{v:,.0f} €".replace(",", " "), va="center", fontsize=9)
ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.set_xlim(0, cm.ca.max() * 1.2)
finish(fig, "06-ca-perdu.png",
       f"Les départs pèsent {eur(V['ca_perdu'])} de CA annuel, soit {V['pct_ca_perdu']:.0f} % du CA de l'échantillon",
       "Source : orders.csv (juillet 2025 à juin 2026, remboursements déduits), clients partis. Échantillon d'environ 2 000 clients, pas la base entière.")

# ---------------------------------------------------------------- chiffres.md
L += [
    "## Graphiques produits",
    "",
    "Dans `chantier/analyse/` : `01-churn-plan-et-mois.png`, `02-churn-canal.png`, `03-churn-profil.png`, `04-signaux.png`, `05-motifs.png`, `06-ca-perdu.png`.",
    "",
    "## Ce que les données ne permettent pas de dire",
    "",
    "- L'effet causal de la hausse de prix du 1er mars, du transporteur du 2 mars ou de la recette saumon du 4 mai : une seule fenêtre de départ, pas de date de résiliation, pas de transporteur par commande.",
    "- Le churn de la base entière : l'échantillon surreprésente les abonnés.",
    "- Un modèle prédictif : non demandé ici.",
    "",
]
(OUT / "chiffres.md").write_text("\n".join(L), encoding="utf-8")


# ---------------------------------------------------------------- tableau de bord HTML
def b64(name):
    return base64.b64encode((OUT / name).read_bytes()).decode()


sig_max = f"{sk.pct.max():.0f}"
best_tk = tk.pct.idxmax()
sections = [
    ("01-churn-plan-et-mois.png", f"Un abonné sur {round(100 / V['churn_sub'])} part en 3 mois, près de deux ponctuels sur trois ne recommandent rien",
     f"Sur {V['n_sub']} abonnés, {V['partis_sub']} ont résilié entre juillet et septembre ({V['churn_sub']:.1f} %). Sur {V['n_one']} clients sans abonnement, {V['partis_one']} n'ont rien commandé ({V['churn_one']:.1f} %). Les deux mesures ne veulent pas dire la même chose. À droite, les ponctuels dont la dernière commande est ancienne sont mécaniquement les plus nombreux à ne pas revenir."),
    ("02-churn-canal.png", f"Chez les abonnés, le canal change peu le churn : de {ch_s.pct.min():.0f} % à {ch_s.pct.max():.0f} %",
     f"Le canal de la première visite, pour les abonnés. La barre terracotta est le canal qui perd le plus. La ligne pointillée donne la moyenne ({V['churn_sub']:.1f} %). Le n sous chaque barre dit combien de clients se cachent derrière."),
    ("03-churn-profil.png", f"Les chats abonnés partent {str(round(sp_s.pct.loc['cat'] / sp_s.pct.loc['dog'], 1)).replace('.', ',')} fois plus que les chiens",
     f"{sp_s.pct.loc['cat']:.1f} % de churn chez les abonnés chats ({int(sp_s.n.loc['cat'])} clients), {sp_s.pct.loc['dog']:.1f} % chez les chiens ({int(sp_s.n.loc['dog'])}). Parmi les chats, ceux qui ont acheté un produit au saumon depuis le 4 mai partent à {V['sa_oui'].pct:.0f} % ({int(V['sa_oui'].n)} clients), contre {V['sa_non'].pct:.0f} % pour les autres ({int(V['sa_non'].n)}). Ce lien reste à confirmer : les données ne prouvent pas que le saumon soit la cause. La remise de bienvenue suit le canal, donc son effet ne peut pas être isolé."),
    ("04-signaux.png", "Livraisons décalées et tickets : les signaux d'alerte les plus nets",
     f"Pour les abonnés, le churn passe de {sk.pct.iloc[0]:.0f} % sans livraison décalée à {sk.pct.iloc[-1]:.0f} % avec deux (n={int(sk.n.iloc[-1])}), et de {tk.pct.iloc[0]:.0f} % sans ticket à {tk.pct.iloc[-1]:.0f} % avec trois ou plus (n={int(tk.n.iloc[-1])}). Les retards de colis et la note du dernier avis donnent des écarts faibles chez les abonnés. Chez les ponctuels, un colis en retard s'accompagne de {rate(one[one.late_deliveries_12m >= 1]):.0f} % de non-retour (contre {rate(one[one.late_deliveries_12m == 0]):.0f} % sans retard) (voir chiffres.md). Un signal annonce un départ, il n'en donne pas la raison."),
    ("05-motifs.png", f"Chez les abonnés, c'est l'animal qui refuse la nourriture ({V['refus_sub_pct']:.0f} %) ; chez les ponctuels, le prix ({V['price_one_pct']:.0f} %)",
     f"Parmi les {V['nk_sub']} abonnés partis qui ont donné un motif, {V['mr_sub'].get('pet_refused_food', 0)} citent un animal qui refuse la nourriture, {V['mr_sub'].get('delivery_issues', 0)} la livraison et {V['mr_sub'].get('price', 0)} le prix. {V['n_partis_nomotif']} partis (tous formules) n'ont donné aucun motif : on ne les range pas dans « autre »."),
    ("06-ca-perdu.png", f"{eur(V['ca_perdu'])} de CA annuel sont partis avec les clients",
     f"Ce que ces clients avaient commandé sur les 12 mois jusqu'au 30 juin, remboursements déduits. Un abonné parti représentait en moyenne {eur(V['ca_moy_sub_parti'])} par an ({V['partis_sub']} abonnés, soit {eur(V['ca_perdu_sub'])}). Chiffres de l'échantillon, à ne pas multiplier pour toute la base."),
]

tiles = [
    (f"{V['churn_sub']:.1f} %", "des abonnés ont résilié entre juillet et septembre 2026"),
    (f"{sp_s.pct.loc['cat']:.0f} % / {sp_s.pct.loc['dog']:.0f} %", "de churn chez les abonnés chats / chiens"),
    (eur(V["ca_perdu"]), f"de CA annuel chez les {V['partis_all']} clients partis ({V['pct_ca_perdu']:.0f} % du CA de l'échantillon)"),
    (f"{V['refus_sub_pct']:.0f} %", "des abonnés partis (motif connu) citent un animal qui refuse la nourriture"),
]
import re
fr = lambda x: re.sub(r"(\d)\.(\d)", r"\1,\2", x)
sections = [(f, fr(t), fr(p_)) for f, t, p_ in sections]
tiles = [(fr(a), fr(b)) for a, b in tiles]
tiles_html = "".join(f'<div class="tile"><div class="big">{a}</div><p>{b}</p></div>' for a, b in tiles)
sec_html = "".join(
    f'<section><h2>{t}</h2><p>{p}</p><img alt="{t}" src="data:image/png;base64,{b64(f)}"></section>' for f, t, p in sections)
net = "".join(f"<li>{x}.</li>" for x in journal_nettoyage)

html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pattes &amp; Papilles · Diagnostic du churn</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{{--sapin:#1E4636;--terra:#D9734E;--creme:#FBF5EC;--moutarde:#E8B04B}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--creme);color:var(--sapin);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;font-weight:400;line-height:1.55}}
h1,h2,.big,.brand{{font-family:Fraunces,Georgia,"Times New Roman",serif;font-weight:700}}
header{{background:var(--sapin);color:var(--creme);padding:32px 6vw}}
.brand{{font-size:1.1rem;letter-spacing:.02em;margin:0 0 6px}}
header h1{{margin:0;font-size:clamp(1.6rem,3.6vw,2.4rem);line-height:1.2}}
header p{{margin:8px 0 0;max-width:62ch;opacity:.9}}
main{{max-width:1100px;margin:0 auto;padding:28px 5vw 60px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin-bottom:34px}}
.tile{{background:#fff;border-left:6px solid var(--moutarde);border-radius:6px;padding:16px 18px;box-shadow:0 1px 3px rgba(30,70,54,.12)}}
.tile .big{{color:var(--terra);font-size:2rem;line-height:1.1}}
.tile p{{margin:6px 0 0;font-size:.92rem}}
section{{margin:0 0 38px}}
h2{{font-size:1.35rem;margin:0 0 6px;line-height:1.3}}
section p{{margin:0 0 12px;max-width:75ch}}
img{{width:100%;height:auto;border-radius:6px;border:1px solid rgba(30,70,54,.15)}}
.limites{{background:#fff;border-left:6px solid var(--terra);border-radius:6px;padding:16px 20px}}
.limites h2{{margin-top:0}}
.limites li{{margin:4px 0}}
footer{{padding:18px 6vw 30px;color:var(--sapin);font-size:.9rem}}
</style></head><body>
<header>
<p class="brand">Pattes &amp; Papilles</p>
<h1>Diagnostic du churn : qui part, quand, et ce qui l'annonce</h1>
<p>Échantillon de {V['n']} clients en portefeuille au 30 juin 2026, départs observés du 1er juillet au 30 septembre 2026.</p>
</header>
<main>
<div class="tiles">{tiles_html}</div>
{sec_html}
<section class="limites">
<h2>Ce qu'il faut garder en tête</h2>
<ul>
<li>L'échantillon compte {V['n']} clients, pas les 18 000 clients actifs. Il contient plus d'abonnés que la base réelle.</li>
<li>Une seule fenêtre de départ (3 mois) : on ne peut pas isoler l'effet de la hausse de prix du 1er mars, du changement de transporteur du 2 mars ou de la recette au saumon du 4 mai.</li>
<li>Un signal qui précède un départ n'en est pas forcément la cause.</li>
<li>Données nettoyées : {"; ".join(journal_nettoyage[:1])}, libellés corrigés, une ligne incohérente écartée.</li>
</ul>
</section>
</main>
<footer>Bien nourris, bien dans leurs pattes.</footer>
</body></html>
"""
(LIV / "tableau-de-bord.html").write_text(html, encoding="utf-8")
print("OK", len(L), "lignes de chiffres.md")
