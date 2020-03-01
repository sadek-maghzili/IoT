# Rapport du projet IOT « Station Météo »

1. Choix technologiques

__Introduction__

Dans le cadre du projet d'IoT, nous avions à réaliser une station météo connectée, nous avons 
choisi de réaliser notre station pour l'agriculture. Notre station météorologique permet donc 
de renseigner des données spécifiques à l’environnement d’un champ de tomate (plante qui a besoin 
de beacoup de soleil, d'eau et de lumière) tel que l’humidité du sol, la luminosité ou encore la 
température extérieure. Cela permettra aux professionnels de l’agro-alimentaire d’améliorer leur 
rendement, gagner du temps et donc de la productivité.

Notre technologie d’IoT (Internet Of Things) doit être capable de récolter des informations
sur son environnement à l'aide de ses capteurs et les transmettre de manière autonome et sans
fil pour pouvoir être traité et afficher. Pour cela, des choix appropriés de technologies sont 
nécessaires en fonction du système que l’on souhaite concevoir.

Dans notre cas, nous avons opté pour un module Sigfox pour faire la liaison entre les capteurs et 
le serveur. En effet, les messages Sigfox sont limités en taille (12 bytes au maximum) toutes les 
10 minutes et nombre (140 par jour), ce qui est amplement suffisant pour des relevés de température 
et d'humidité. De plus, cela permet d'être plus efficace que le WiFi dans les zones de campagnes les 
plus reculé.

__Schéma de la solution__

![alt text][schema_sol]

[schema_sol]: https://github.com/sadek-maghzili/IoT/blob/master/Schema%20solution.png "Schéma de la solution"

__Schéma électronique__

![alt text][schema_elec]

[schema_elec]: https://github.com/sadek-maghzili/IoT/blob/master/Sch%C3%A9ma%20%C3%A9lectronique.png "Schéma électronique"

2. How to...


3. Usages potentiels

Cette technologie à de nombreux usages potentiels, à grande échelle comme à petite échelle. Tout 
d’abord à __grande échelle__ :

Les agriculteurs de demain aurons accès un flux de donnée régulier sur l’état de leur produit en 
temps réel. L’étude des sols leur permettrons d’anticiper une mauvaise croissance ou quelconque 
anomalie et de vite réagir face à une situation de façon très localisé. De ce fait, non seulement 
ce contrôle réduit les pertes et par conséquent le gâchis mais permet de fructifier considérablement 
sa production.

A présent à __petite échelle__ :
Dans une société visant à manger mieux avec des produits de meilleure qualité, être plus éco-responsable 
et moins dépendant des produits de grande surface dont la provenance et leur surproduction sont des problèmes. 
Notre système d’alertes permettrait à des personnes sans connaissances agricoles particulières de faire pousser 
leurs propres légumes simplement. En effet, nous avons pensé à mettre différentes alertes indiquant les besoins 
en eaux ou en compléments nutritifs à la terre en mesurant le tôt d’oxygène par exemple. 

Une société auto-suffisante, plus vert, limitant considérablement notre empreinte carbone.


