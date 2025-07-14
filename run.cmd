@echo off

echo Ouverture de Microsoft Edge...
start microsoft-edge:http://127.0.0.1:5000/


echo Activation de l'environnement virtuel...
call .venv\Scripts\activate

echo Lancement de l'application...
python app.py


