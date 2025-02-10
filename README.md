# Projet 9 : Développez une application Web en utilisant Django


## But du projet :

Création d'un site web permettant de demander et de poster des critiques sur articles ou des livres.  

## Etape 1 : Initialisation du projet

Cliquer sur le bouton vert "<> Code" puis sur Download ZIP.
Extraire l'ensemble des éléments dans le dossier dans lequel vous voulez stockez les datas qui seront téléchargées.


## Etape 2 : Télécharger les packages nécessaires au bon fonctionnement du programme

Pour lancer le serveur, ouvrez le terminal de commande :   
Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   

Dans le terminal, placez-vous dans le dossier où vous avez télécharger le code.  


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

Déplacez vous dans le dossier LitREVU

```
cd home/magali/OpenClassrooms/Formation/Projet_9/LitREVU
```
Puis installer les packages nécessaires :  
  
```
pip install -r requierements.txt
```

## Etape 3 :  Mise en route du serveur


Puis exécutez la commande suivante :  

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

## Etape 4 :  Utilisation du site

Créez-vous un compte ou connectez-vous avec les identifiants d'un utilisateur existant :  
username : florineg  
password : S3cret!  
  
Bonne navigation ! 
