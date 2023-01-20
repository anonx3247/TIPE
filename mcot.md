# Comment livrer le plus de colis en le moins de temps?

#### Anas Lecaillon (MP)

## Ancrage au thème (24/50)

La livraison est une activité posant de nombreux problèmes: planification, organisation du traffic, adaptation aux différentes zones d'habitation,
ayant tous rapport avec la ville.

## Motivation du Choix (49/50)

Étant automobiliste, je passe une bonne part de mon temps sur les routes. Ainsi, le fonctionnement des programmes de navigation GPS, que j'utilise 
quotidiennement, m'intéressent: De même, j'effectue des commandes sur internet, que je me fais livrer régulièrement ce qui motive ma curiosité sur
les méthodes mises en oeuvre.

## Positionnements thématiques et mots-clés

- **Thématiques**: Informatique (*Informatique Pratique*), Mathématiques (*Autres Domaines*), Mathématiques (*Probabilités*)
- **Mots-clés** (*Francais*): Livraison, Problème du voyageur, Recherche de trajectoire, Graphes, Statistiques
- **Mots-clés** (*English*): Delivery, Travelling Salesman, Pathfinding, Graphs, Statistics

## Bibliographie Commentée (519/650)

La livraison, est avant tout une question logistique. Pour livrer des colis, le nombre de colis par livreur, le nombre de livreurs par région géographique,
ainsi que le choix de répartition des colis aux différents livreurs et l'ordre de visite des adresses, sont tous des paramètres de grande importance, étant tous
plus ou moins résolus aujourd'hui. La navigation, par exemple, ne profite pas de beaucoup d'innovation, les algorithmes de navigation comme Djikstra et A* ayant été
développés il y a un certain temps sont assez matures, et la plupart des innovations se trouvent dans des algorithmes hybrides [1].

L'étude et l'exploitation des circuits routiers ont été sensiblement facilités par le travail de Geoff Boeing [2]. Ceci, avec la théorie des graphes, facilite aussi l'élaboration
de programmes implémantant les algorithmes comme A* ou Djikstra sur les réseaux routiers. Cela permet également l'étude statstique des caractéristiques de ces réseaux: la proportion de voies a sens
unique, la connexité du graphe, et le degré infini moyen, qui permettent de caractériser la propensité a être facilement navigable d'une ville. C'est d'ailleurs la raison
principale de la création par Boeing de la librairie *OSMNX* qui permet de télécharger, sous forme de graphe, les réseaux routiers, depuis les bases de données *OpenStreetMap*.

Lorsque la livraison est envisagée, il y a une part certes, qui est dédiée à la navigation, mais il y a des problèmes logistiques plus importants. L'un d'eux, est le
problème du voyageur, consistant dans le choix de l'ordre de visite des adresses pour un livreur. Ce problème a de nombreuses solutions avec des algorithmes classiques,
notamment génétiques [4]; cependant d'autres méthodes ont été essayées, utilisant des réseaux de neurones, et d'autre méthodes d'intelligence artificielle, même si l'avantage
de telles méthodes reste peu probant, et leur implémentation présente de nombreuses difficultés [5].

Ces problèmes, sont les mêmes que pour les algorithmes classiques: la complexité. Un algorithme naif pouvant donner une solution optimale possède une complexité de $O(n!)$,
et peut simplement être ramenée à $O(2^n n^2)$ [4]. C'est pourquoi la plupart de l'étude de cette question est aujourd'hui centrée sur des méthodes heuristiques, qui donnent
des solutions suboptimales, de bonne qualité neanmoins, en un temps polynomial [4]. Sur cette dernière étude, comme dit plus haut, les réseaux de neurones peinent à rendre une meilleure performance
que ces algorithmes pour les solutions optimales [5].

Le second problème qui existe est celui de la répartition. Lorsqu'une entreprise a beaucoup de colis à livrer, elle envoie souvent des stocks dans des grands entrepots,
puis ils sont répartis à des *sattelites* qui eux répartissent les colis à des livreurs individuels. La question de comment organiser la répartition des livreurs,
et des sattélites est large et complexe et est appelée le problème de Routage de véhicules à deux échelons [3]. Car l'on doit répartir des véhicules entre le premier échelon: les entrepots
et le deuxième: les sattelites.

Ces questions, logistiques, d'optimisation et de répartition ou de sélection d'ordre (pour le cas du problème du voyageur) ne sont pas qu'applicables à la livraison,
ils trouvent leur utilité dans de nombreux domaines, et ainsi les études menées sont souvent théoriques [3].

## Problématique retenue (44/50)

Au vu de la problématique de la navigation, et des stratégies qu'un organisme de livraison peut être amené à employer pour livrer ses colis,
nous étudiérons *comment l'on peut optimiser la livraision, pour livrer le plus de colis possible, en le moins de temps.*


## Objectifs du TIPE (100/100)

Les objectifs de se travail sont: d'une part, de créer un système informatique qui, donnée une liste d'adresses pour livrer des colis, permet de répartir
ces adresses parmi des livreurs, de choisir l'ordre de visite des adresses, et de determiner les trajets que doivent prendre ses livreurs, afin de minimiser le
temps de livraison et de maximiser le nombre de colis livrés; d'autre part, ce travail comparera divers algorithmes pour résoudre ce problème. Enfin
une étude statistique seras faite pour évaluer l'importance de différents paramètres sur la livraison: densité de livreurs, caractéristiques de la ville, et densité des adresses
de livraison.

## Liste de références bibliographiques (5/10)

1. Cho, Hsun-Jung, and Chien-Lun Lan. ‘Hybrid Shortest Path Algorithm for Vehicle Navigation’. *The Journal of Supercomputing*, vol. 49, no. 2, Aug. 2009, pp. 234–247, https://doi.org10.1007/s11227-008-0236-7.
2. Boeing, Geoff. ‘OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks’. *Computers, Environment and Urban Systems*, l. 65, 2017, pp. 126–139, https://doi.org10.1016/j.compenvurbsys.2017.05.004.
3. Sluijk, Natasja, et al. Two-Echelon Vehicle Routing Problems: A Literature Review’. *European Journal of Operational Research*, vol. 304, no. 3, 2023, pp. 865–886, https://doi.org10.1016/j.ejor.2022.02.022.
4. Larrañaga, P., et al. ‘Genetic Algorithms for the Travelling Salesman Problem: A Review of Representations and Operators’.*Artificial Intelligence Review*, vol. 13, no. 2, Apr. 1999, pp. 129–170, https://doi.org10.1023/A:1006529012972.
5. Potvin, Jean-Yves. ‘State-of-the-Art Survey - The Traveling Salesman Problem: A Neural Network Perspective’. *INFORMS J. Comput.*, vol. 5, 1993, pp. 328–348, https://doi.org/10.1287/ijoc.5.4.328
