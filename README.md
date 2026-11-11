# 02805 Projekt — Food.com opskriftsnetværk

Noder = opskrifter. Kant hvis to opskrifter deler ≥ 2 ingredienser og har Jaccard ≥ 0,2
(ingredienser i > 10 % af opskrifterne tæller ikke med).

Data: Kaggle `shuyangli94/food-com-recipes-and-user-interactions`, hentes automatisk med `kagglehub` i første celle. Data ligger ikke i git.

## Notebooks

1. `project_Rakel.ipynb`: preprocessing, opskriftsnetværket og communities. Gemmer de rensede data i `data/` (tager ca. 10 min).
2. `reviews.ipynb`: anmeldelserne (ændringer og substitutioner). Indlæser data fra `data/`.

`data/` ligger ikke i git. Kør `project_Rakel.ipynb` én gang (og igen, hvis preprocessingen ændres), før `reviews.ipynb`.

## Første gang

```bash
git clone <repo-url>
cd <repo>
pip install nbstripout networkx pandas scikit-learn matplotlib igraph kagglehub
nbstripout --install --attributes .gitattributes   # fjerner output fra notebooks ved commit
```

## Arbejdsgang

```bash
git pull                      # altid før du starter
# ... arbejd ...
git add .
git commit -m "Kort beskrivelse"
git pull                      # hent din makkers ændringer
git push
```

Regler for at undgå konflikter i notebooks:
- Arbejd helst i hver sin notebook (fx `analysis_communities.ipynb`, `analysis_reviews.ipynb`), og flyt færdig kode ind i `Project.ipynb`.
- Commit og push ofte, i små bidder.
- Aftal hvem der redigerer `Project.ipynb`, hvis I begge skal i den samme dag.
- Ingen API-tokens eller cookies i koden.
