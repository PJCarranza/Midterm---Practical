# crear entorno virtual
python3 -m venv venv
# activar entorno virtual
venv/Scripts/activate
# instalar librerias
pip install "fastapi[standard]" sqlmodel bcrypt python-dotenv
#Iniciar
fastapi env
