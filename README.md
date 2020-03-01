# Rapport du projet IOT « Station Météo »

1. Choix technologiques

Dans le cadre du projet d'IoT, nous avions à réaliser une station météo connectée, nous avons 
choisi de réaliser notre station pour l'agriculture. Notre station météorologique permet donc 
de renseigner des données spécifiques à l’environnement d’un champ de tomate tel que l’humidité 
du sol, la luminosité ou encore la température extérieure. Cela permettra aux professionnels 
de l’agro-alimentaire d’améliorer leur rendement, gagner du temps et donc de la productivité.

Notre technologie d’IoT (Internet Of Things) doit être capable de récolter des informations
sur son environnement à l'aide de ses capteurs et les transmettre de manière autonome et sans
fil pour pouvoir être traité et afficher. Pour cela, des choix appropriés de technologies sont 
nécessaires en fonction du système que l’on souhaite concevoir.

Dans notre cas, nous avons opté pour un module Sigfox pour faire la liaison entre les capteurs et 
le serveur. En effet, les messages Sigfox sont limités en taille (12 bytes au maximum) toutes les 
10 minutes et nombre (140 par jour), ce qui est amplement suffisant pour des relevés de température 
et d'humidité. De plus, cela permet d'être plus efficace que le WiFi dans les zones de campagnes les 
plus reculé.

