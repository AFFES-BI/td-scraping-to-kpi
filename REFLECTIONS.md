# Réflexions — TD3

## 1. Erreur silencieuse vs erreur bruyante (CM3)
`rp.read()` renvoie « tout est interdit » quand le proxy bloque la requête, sans aucune erreur. Le script croit alors que le site interdit le scraping alors que c'est un simple problème réseau : le contrôle a l'air d'avoir marché, mais sa réponse est fausse. Or tout l'intérêt du contrôle est de pouvoir prouver *pourquoi* on a le droit (ou non) d'agir (provenance, CM3). Un plantage bruyant se corrige tout de suite ; un échec silencieux contamine la décision et la preuve sans qu'on le sache. J'ai testé `rp.parse()` : sur Wikipédia, `robots.txt` autorise `/wiki/Le_Mans` (True).

## 2. France Travail vs échantillon jobspy
France Travail publie des données ouvertes sous licence de réutilisation : on a le droit de les republier. Les annonces récupérées via jobspy viennent d'Indeed/LinkedIn, dont les conditions d'utilisation interdisent la redistribution : les republier expose à un risque juridique (et envers les entreprises/personnes citées). Un dépôt privé ne change pas le droit (la copie est toujours non autorisée) mais réduit fortement l'exposition, car personne d'extérieur ne peut télécharger les annonces. Public/privé compte donc pour la diffusion, pas pour la licence.

## 3. Pourquoi un LLM pour texte → compétences, pas pour le suivi de candidatures (CM5)
Un texte d'annonce est libre, varié, parfois en français, parfois en anglais : transformer ça en liste structurée est de l'interprétation, exactement ce qu'un LLM sait faire et où une erreur reste tolérable. Ma liste de candidatures réellement envoyées est un fait que je connais déjà : il n'y a rien à deviner, et une approximation serait une erreur grave. Un tableau/une base suffit, de façon déterministe et fiable.

## 4. Incohérence de format prédite et constatée
Prédiction (écrite avant d'ouvrir le fichier) : une même compétence écrite avec une casse différente (« Python » / « python »). Constat : oui, dans mon `extracted.json` — « Computer vision » / « computer vision », « Generative AI » / « generative AI », « Image technology » / « image technology ». Les deux premières annonces sont quasi identiques (même poste, deux entreprises) et le modèle a pourtant écrit différemment. Conséquence mesurable : dans `top_skills`, « generative AI » (2) et « Generative AI » (1) sont comptés séparément au lieu d'un seul « Generative AI » (3).
Autres limites vues en relisant : l'annonce n°3 donne 24 « compétences » dont beaucoup ne sont pas des outils (« test cases », « automation solutions », « hardware components »), et les annonces n°8 et n°10 renvoient une liste vide car les 1500 premiers caractères (seuls envoyés au modèle) ne contiennent que la présentation de l'entreprise — vide ≠ « aucune compétence demandée ».

## 5. Passe de critique = human-in-the-loop (CM5)
Je n'avais pas de camarade pour l'échange : je me suis relu moi-même, ce qui est plus faible (voir limites). Cela doit se faire sur `extracted.json` car c'est là qu'on voit, annonce par annonce, ce que le modèle a lu et sorti ; `kpi.json` est déjà agrégé (des pourcentages et des totaux), les erreurs y sont noyées et invérifiables.

## 6. Mon `TARGET_SKILL` et lequel des deux KPI croire (CM2)
Choix avant de voir le chiffre : **AI** — pour un comité de programme, c'est la thématique transversale à faire monter (et mon échantillon est orienté IA, donc ce choix est aussi biaisé). Résultats : `python` = 8,3 % (1/12) ; `AI` = 41,7 % (5/12). Je ne ferais confiance à aucun des deux pour dire « il faut enseigner X » : 12 annonces ne représentent rien, la sélection des annonces (recherche orientée IA/ingénieur) prédétermine le résultat, et un « Python » raté ou une casse différente change le chiffre. Le KPI par défaut sous-évalue sans doute Python (l'annonce n°3 est la seule qui le cite dans les 1500 caractères lus). C'est une *construction* choisie, pas un fait neutre (CM2). J'ai vérifié que la recherche par sous-chaîne « ai » ne produit pas de faux positifs ici, mais cette méthode est fragile (elle matcherait « maintenance »).

## 7. Que peut-on reconstituer depuis `kpi.json` ? (CM3/CM6)
Non : il ne contient ni titre, ni entreprise, ni URL, ni texte d'annonce — seulement un pourcentage, des totaux, 10 noms de compétences avec leur fréquence et une moyenne. C'est un choix délibéré dans `compute_kpi()` : la fonction ne recopie dans la sortie que des agrégats, jamais les champs `title` / `company` présents dans `extracted.json`. Un nom de compétence rare (compté 1 fois) pourrait toutefois trahir une annonce très spécifique : l'agrégation protège, mais pas parfaitement avec un petit échantillon.

## 8. À qui s'adresse le dashboard ?
En l'état : à moi, pas à un comité. La page affiche seulement la carte du KPI et le graphique des compétences, sans titre ni explication : quelqu'un d'extérieur ne saurait pas que l'échantillon ne compte que 12 annonces ni d'où viennent les chiffres. Pour un vrai comité, il faudrait une phrase du type « Exercice étudiant : 12 annonces, compétences extraites par un LLM local, échantillon trop petit pour décider d'un programme », ainsi que la normalisation des compétences et la source des annonces.

## 9. Second KPI
KPI 2 : part des annonces citant un fournisseur cloud (AWS, Azure, GCP, S3, SageMaker…), avec recherche par mots entiers et insensible à la casse : **2/12 = 16,7 %** (DevOps, Desktop Support). Comparé au KPI 1 (une seule compétence, recherche par sous-chaîne), il regroupe une *famille* de compétences et est donc moins sensible aux variations d'écriture, ce qui le rend plus solide ; mais avec 12 annonces, aucun des deux ne devrait seul piloter une décision réelle.
