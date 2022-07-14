installer python 3
installer django, django_tables2


pip3 install django
pip3 install django_tables2
pip3 install mysqlclient
pip3 install numpy
pip3 install pandas
pip3 install tabula # pour transformer les donnees des pdf en csv
pip3 install pymysql   


installer MySQL
Changer mot de passe root de mysql
créer la bdd app_gestion_django

installer mysqlclient

python3 manage.py runserver 127.0.0.1:8000
python manage.py runserver


30/12/2021:
Mise à jour de pip
Mise à jour de django, django_tables2, mysql

Acces au site: http://127.0.0.1:8000/gestion_operations/


MySQL:
show databases;
use app_gestion_django;
show tables;



python manage.py makemigrations
python manage.py migrate


python -Wa manage.py test


avec zsh de mort ça marchait plus pour mysql, j'ai du faire tourner ça:
export PATH=${PATH}:/usr/local/mysql/bin/

--------------

# Pour mettre à jour les données

- Utiliser l'application Tabula pour sélectionner les zones des relevés de compte à utiliser
- Utiliser le notebook "Utiliser les relevés CE"
- Il y a une cellule ou je dis que j'utilise ça ... (le nom du fichier commence par tabula)
- Vérifier que c'est bon avec l'affichage de la table finale
- Si ça marche, relancer le serveur django et envoyer le fichier
- Utiliser le dropdown de recherche de fichier, le sélecteur en mode recherche ne fonctionne pas