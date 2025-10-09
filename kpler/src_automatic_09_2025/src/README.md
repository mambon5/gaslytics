
Aquí definim uns programes de python que creen la base de dades de mysql i carreguen les taules amb els csv descarregats a `data`.


# Crear base dades mysql, usuari i donar permisos:

```
CREATE DATABASE kpler CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'kpler_user'@'localhost' IDENTIFIED BY 'StrongPassword123';

GRANT ALL PRIVILEGES ON kpler.* TO 'kpler_user'@'localhost';
FLUSH PRIVILEGES;

```

# posar contrasenyes

A un fitxer d'ambient .env i instalar `pip install python-dotenv` en el virtual environment.

També hem d'instalar `pip3 install sqlalchemy`, `pip3 install pymysql`