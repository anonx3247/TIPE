# Algorithmes

## A priori personnel

### Premier algorithme:

1. $L:$ tableau des positions des destinations
2. Trouver le $p$  plus proche parmi $L \backslash \{\text{destinations deja rencontrees}\}$
3. bouger vers $p$ 
4. Repeter jusqu'a ce que $L \backslash \{\text{destinations deja rencontrees}\} = \varnothing$

### Deuxieme algorithme:

1. Tracer des splines polynomiales cubiques reliant les points de la manière la plus fluide possible en faisant des équations paramétriques $x(t)$ et $y(t)$.
2. Générer un trajet qui colle au mieux a cette courbe

#### Pourquoi des splines?

Le choix de splines au lieu d'un seul polynome de degré égal au nombre de points, et pour deux raisons:

1. Le plus haut le degré, le plus complexe le calcul, et le pire que seras la vitesse de calcul de l'algorithme, des polynomes de même degré font que la compléxité est linéaire par rapport au nombre de points
2. Lorsque le degré augmente, l'interpolation n'augmente pas nécéssairement en qualité, en particulier lorsque les points sont proches, et que le résultat est une grande dérivée en ses points qui par conséquent a l'effet parasite d'augmenter les distances entre les points les plus proches pour qu'elles deviennent les plus grandes, avec des splines nous controlons précisément les dérivées en touts les points, et ainsi pouvons assurer une interpolation qui est quasi-linéaire entre deux points consécutifs, tout en étant fluide et dérivable en tout point de l'agregat des splines.

#### Méthode d'interpolation

Nous faison le suivant sur le $x$  et le $y$  indépendamment:

Soient $p_1, p_2, \cdots, p_n$, $n$  points de coordonées respectives:
$$
p_1(x_1, y_1), p_2(x_2, y_2), \cdots, p_n(x_n, y_n)
$$

Dans tout ce qui suit, $p$, $p_k$, $P$, ou $P_k$  corespondent non pas aux points directement mais font référence a $x$ ou a $y$ car le travail fait sur eux est le même, ainsi $p$ corespondrait a $x$ ou $y$ $P$ a $X$ ou $Y$ et ainsi de suite.

La solution finale est de la forme d'un système d'équations paramétriques en $t  ∈\mathbb{R}_+$ sur $p$

Nous notons des $t_k$ tous éspacés uniformément sur $[0, t_n]$

Nous allons former $n$ splines polynomiales cubiques notées $P_k$.

$$
\begin{cases}
P_k: [t_{k-1}, t_k] \to [p_{k-1}, p_k] \\
t \mapsto a_kt^3+b_kt^2+c_kt+d_k
\end{cases}
$$

Pour s'assurer que ces polynomes passent par les points on impose les conditions suivantes sur chaqu'un

$$
\begin{cases}
P_k(t) = a_kt^3+b_kt^2+c_kt+d_k \\
P_k(t_{k-1}) = p_{k-1} \\
P_k(t_k) = p_k \\
P_k'(t_{k-1}) = P_{k-1}'(t_{k-1}) \\
\end{cases}
$$

La deriniere condition peut aussi s'écrire de la façon suivante:
$$
3a_k (t_{k-1})^2 + 2b_k (t_{k-1}) + c_k = 3a_{k-1} (t_{k-1})^2 + 2b_{k-1} (t_{k-1}) + c_{k-1}
$$

On peut aussi ajouter une condition sur la dérivée en $t_k$: pour qu'elle soit la même qu'une droite entre $p_k$ et $p_{k+1}$

$$
P_k'(t_k) = mt_k / m = \frac{p_{k+1}-p_k}{t_{k+1}-t_k}
$$

ce qui revient a:
$$
3a_k t_k^2 + 2b_k t_k + c_k = m t_k
$$

Le système final est alors:

$$
\begin{cases}
P_k(t) = a_kt^3+b_kt^2+c_kt+d_k \\
p_{k-1} = a_k t_{k-1}^3 + b_k t_{k-1}^2 + c_k t_{k-1} + d_k \\
p_k = a_k t_k^3 + b_k t_k^2 + c_k t_k + d_k \\
3a_k (t_{k-1})^2 + 2b_k (t_{k-1}) + c_k = 3a_{k-1} (t_{k-1})^2 + 2b_{k-1} (t_{k-1}) + c_{k-1} \\
3a_k t_k^2 + 2b_k t_k + c_k = m t_k / m = \frac{p_{k+1}-p_k}{t_{k+1}-t_k}
\end{cases}
$$

Cela revient donc a résoudre l'équation matricielle $AX=B$ avec $A,X,$ et $B$:

$$
A = \left(
\begin{matrix}
t_{k-1}^3 & t_{k-1}^2 & t_{k-1} & 1 \\
t_k^3 & t_k^2 & t_k & 1 \\
3t_{k-1}^2 & 2t_{k-1} & 1 & 0 \\
3t_k^2 & 2t_k & 1 & 0
\end{matrix}
\right), X = \left(
\begin{matrix}
a_k \\ b_k \\ c_k \\ d_k
\end{matrix}
\right), B =
\left(
\begin{matrix}
p_{k-1} \\
p_k \\
P'_{k-1}(t_{k-1})\\
m t_k
\end{matrix}
\right)
$$

On défini alors des fonctions de $t$ pour $x$ et $y$ pour créer une equation paramétrique. Ses fonctions sont de la forme suivante (ici de nouveau $p$ corespond soit a $x$ soit a $y$:

$$
p(t) = \begin{cases}
P_1(t) \text{ si } 0 \le t \le t_1 \\
P_2(t) \text{ si } t_1 \le t \le t_2 \\
\vdots \\
P_k(t) \text{ si } t_{k-1} \le t \le t_k \\
\vdots \\
P_n(t) \text{ si } t_{n-1} \le t \le t_n \\
\end{cases}
$$

On aboutiras alors a une solution finale du type:

$$
 ∀ 1 \le k \le n
\begin{cases}
x(t) = X_k(t) \text{ si } t_{k-1} \le t \le t_k \\
y(t) = Y_k(t) \text{ si } t_{k-1} \le t \le t_k \\
\end{cases}
$$

Cette équation paramétrique passe bien par tous les points de manière fluide car les dérivées en les points sont égales (donc fluide) et les équations $x(t), y(t)$ passent par tous les $x_k, y_k$ pour une même valeur de $t=t_k$

#### Comment choisir les $t_k$?

En réalité il faudrait faire le travail précédent avec différent choix pour les $t_k$, ce choix revient au choix de l'ordre de visite des points.

### Algorithme du plus proche en $p$.

Disons que nous sommes au point $k$

1. trouver les $p$ points les plus proches de $k$ qui n'ont pas déjà été visités

2. identifier la direction générale des $p$ points par la somme des vecteurs de déplacement

3. trouver le premier point n'allant pas dans la direction des points

4. ceci est le prochain point

## Recherche dans l'industrie

## Tentatives d'application

## Comparaison avec algorithmes complets
