# Projet 9 : Développez une application Web en utilisant Django


## But du projet :

Création d'un site web permettant de demander et de poster des critiques sur articles ou des livres.  

## Etape 1 : Initialisation du projet

Cliquer sur le bouton vert "<> Code" puis sur Download ZIP.
Extraire l'ensemble des éléments dans le dossier dans lequel vous voulez stockez les datas qui seront téléchargées.


## Etape 2 : Création de l'environnement virtuel

Se placer dans le dossier où l'on a extrait l'ensemble des documents grâce à la commande ``cd``  
Exemple :
```
cd home/magali/OpenClassrooms/Formation/Projet_9
```


Dans le terminal de commande, executer la commande suivante :
```
python3 -m venv env
```


Activez l'environnement virtuel
```
source env/bin/activate
```
> Pour les utilisateurs de Windows, la commande est la suivante : 
> ``` env\Scripts\activate.bat ```

## Etape 5 : Télécharger les packages nécessaires au bon fonctionnement du programme

Dans le terminal, taper la commande suivante :
```
pip install -r requierements.txt
```

## Etape 6 :  Mise en route du serveur
 

Pour lancer le serveur, ouvrez le terminal de commande :   
Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   

```
cd home/magali/OpenClassrooms/Formation/Projet_9/LitREVU
```


Dans le terminal de commande, executer la commande suivante :
```
python3 manage.py runserver
```

Le terminal de commande affiche le message suivant :
```System check identified no issues (0 silenced).
May 03, 2024 - 06:10:48
Django version 5.0, using settings 'LitREVU.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Vous avez alors deux possibilités : cliquez directement sur le lien dans le terminal,  
ou tapez [http://127.0.0.1:8000/](http://127.0.0.1:8000/) dans votre navigateur

## Etape 7 :  Utilisation du site

Créez-vous un compte ou connectez-vous avec les identifiants d'un utilisateur existant :  
username : florineg  
password : S3cret!  
  
Bonne navigation ! 
