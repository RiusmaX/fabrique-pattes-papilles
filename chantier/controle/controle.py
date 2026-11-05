# Recalcul indépendant des chiffres du dossier, de la présentation et de la stratégie.
import pandas as pd
D = 'donnees/'
c = pd.read_csv(D + 'customers.csv').drop_duplicates()
c = c.drop_duplicates('customer_id')
c['signup_date'] = pd.to_datetime(c.signup_date)
c['last_order_date'] = pd.to_datetime(c.last_order_date)
c['pet_species'] = c.pet_species.replace({'chat': 'cat'})
c = c[c.signup_date <= '2026-06-30']
o = pd.read_csv(D + 'orders.csv').drop_duplicates()
o['order_date'] = pd.to_datetime(o.order_date)
o = o[(o.order_date <= '2026-06-30') & o.customer_id.isin(c.customer_id)]
p = pd.read_csv(D + 'products.csv')

def pr(label, v): print(label, '=>', v)
def rate(df, label):
    pr(label, f"{int(df.churned.sum())}/{len(df)} = {df.churned.mean()*100:.1f} %")

pr('echantillon', len(c))
s = c[c.plan == 'subscription']; one = c[c.plan == 'one_off']
rate(s, 'abonnes'); rate(one, 'ponctuels')
rate(s[s.pet_species == 'cat'], 'abonnes chats'); rate(s[s.pet_species == 'dog'], 'abonnes chiens')

# saumon chat depuis le 4 mai
# produits chat au saumon : croquettes et sachets (espèce cat) ; l'huile de saumon (P021, complément 'both') est testée à part
sal = p[(p.recipe.str.lower().str.contains('salm|saumon', na=False)) & (p.species == 'cat')]
print(sal[['product_id', 'name', 'species', 'category', 'launch_date']].to_string())
buy = set(o[(o.order_date >= '2026-05-04') & o.product_id.isin(sal.product_id)].customer_id)
sc = s[s.pet_species == 'cat']
rate(sc[sc.customer_id.isin(buy)], 'chats abonnes saumon depuis 4 mai')
rate(sc[~sc.customer_id.isin(buy)], 'chats abonnes sans saumon')
# variante : on ajoute l'huile de saumon (P021)
sal2 = p[p.name.str.contains('aumon', case=False) & p.species.isin(['cat', 'both'])]
buy2 = set(o[(o.order_date >= '2026-05-04') & o.product_id.isin(sal2.product_id)].customer_id)
rate(sc[sc.customer_id.isin(buy2)], 'variante avec huile de saumon P021 (positifs)')

# motifs
sp = s[s.churned == 1]
pr('abonnes partis motifs', sp.churn_reason.value_counts(dropna=False).to_dict())
pr('motifs connus abonnes', sp.churn_reason.notna().sum())
op = one[one.churned == 1]
pr('ponctuels motifs', op.churn_reason.value_counts(dropna=False).to_dict())
pr('ponctuels motifs connus', op.churn_reason.notna().sum())

# CA 12 mois
ca = o.groupby('customer_id').line_total_eur.sum()
c['ca'] = c.customer_id.map(ca).fillna(0)
tot = c.ca.sum(); part = c[c.churned == 1].ca.sum()
pr('CA total', round(tot)); pr('CA partis', (round(part), round(part/tot*100, 1)))
s = c[c.plan == 'subscription']
pr('CA abonnes partis', (round(s[s.churned==1].ca.sum()), round(s[s.churned==1].ca.sum()/s.ca.sum()*100, 1)))
pr('CA moyen abonne parti / reste', (round(s[s.churned==1].ca.mean()), round(s[s.churned==0].ca.mean())))
pr('CA moyen ponctuel', round(c[c.plan=='one_off'].ca.mean()))
pr('CA moyen abonne parti/reste (ca>0 seulement)', (round(s[(s.churned==1)&(s.ca>0)].ca.mean()), round(s[(s.churned==0)&(s.ca>0)].ca.mean())))

# nouveaux abonnes
new = s[s.signup_date >= '2026-03-01']; old = s[s.signup_date < '2026-03-01']
rate(new, 'nouveaux abonnes'); rate(old, 'anciens abonnes')
# decalages
rate(s[s.skipped_deliveries_90d >= 1], 'decale>=1'); rate(s[s.skipped_deliveries_90d == 0], 'decale 0')
rate(s[s.skipped_deliveries_90d == 2], 'decale 2')
pr('decale distrib', s.skipped_deliveries_90d.value_counts().to_dict())
# ponctuels retard
one = c[c.plan == 'one_off']
rate(one[one.late_deliveries_12m == 1], 'ponctuels retard=1'); rate(one[one.late_deliveries_12m == 0], 'ponctuels retard=0')
rate(one[one.late_deliveries_12m >= 1], 'ponctuels retard>=1')
rate(one[one.support_tickets_12m >= 2], 'ponctuels tickets>=2')
# avis
rate(s[s.last_review_score.between(1, 3)], 'avis 1-3'); rate(s[s.last_review_score >= 4], 'avis 4-5')
# departement 29
pr('dept29', (c[c.department.astype(str) == '29'].late_deliveries_12m.mean().round(2), (c.department.astype(str) == '29').sum(), c.late_deliveries_12m.mean().round(2)))
# remboursements croquettes
k = o.merge(p[['product_id', 'category']], on='product_id')
k = k[k.category == 'kibble']; k['m'] = k.order_date.dt.strftime('%Y-%m')
r = k.groupby('m').apply(lambda d: (d.quantity < 0).mean() * 100)
pr('remb', (r.get('2025-07'), r.get('2026-06')))
# cumul signaux
sig = (s.skipped_deliveries_90d >= 1).astype(int) + (s.late_deliveries_12m >= 1).astype(int) + (s.support_tickets_12m >= 2).astype(int)
pr('cumul', s.groupby(sig).churned.agg(['sum', 'count', 'mean']).round(3).to_dict())
# business case
for name, n, k_, rt, co in [('seg1', 253, 81, .32, 12), ('seg2', 310, 62, .20, 8), ('seg3', 111, 29, 29/111, 6)]:
    pass
sz = [(253,81,81/253,12),(310,62,62/310,8),(111,29,29/111,6)]
G = {.1: 0, .2: 0}; cost = 0; att = 0
for n, k_, rt, cu in sz:
    base = n - k_; a = base*rt; att += a; cost += base*cu
    for h in G: G[h] += a*h*550
    print('seg', base, round(a, 1), round(a*.1, 1), round(a*.2, 1), round(a*.1*550), round(a*.2*550), round(base*cu))
pr('tot attendus', round(att, 1)); pr('gains', {h: round(v) for h, v in G.items()}); pr('cout', round(cost))
pr('soldes', {h: round(v - cost - 1500) for h, v in G.items()})
pr('gains avec taux arrondis', [round(x) for x in [172*.32*.1*550+248*.2*.1*550+82*.261*.1*550]])

# Complément : cumul de signaux (décalage, retard, ticket >= 1, note <= 3), à comparer au dossier
sig = (s.skipped_deliveries_90d >= 1).astype(int) + (s.late_deliveries_12m >= 1).astype(int) + (s.support_tickets_12m >= 1).astype(int) + (s.last_review_score <= 3).astype(int)
print(s.groupby(sig).churned.agg(['count', 'sum', 'mean']).round(3))
