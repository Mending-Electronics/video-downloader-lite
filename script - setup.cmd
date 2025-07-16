@echo off
echo Création de l'environnement virtuel...
python -m venv .venv

echo Activation de l'environnement...
call .venv\Scripts\activate

echo Installation des dépendances...
pip install -r requirements.txt

echo Tout est prêt !
pause
