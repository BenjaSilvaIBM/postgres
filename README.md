# pasos para hacer la demo de postgres con pgbench

# Paso 1: instalar postgres
sudo dnf install postgresql-server postgresql-contrib -y

# Paso 2: utiliza
/usr/bin/postgresql-setup --initdb

# Paso 3: modifica el pg_hba.conf
nano vi /var/lib/pgsql/data/pg_hba.conf

IPv4 local connections:

host    all             all             0.0.0.0/0            md5
#host    all             all             127.0.0.1/32            ident

# Paso 3.5: cambiar la config
nano /var/lib/pgsql/data/postgresql.conf

# Paso 4: cambiar y descomentar
listen_addresses = '*'

# Paso 5: cambiar la contraseña del usuario consola postgres (min. 8 caracteres)
sudo passwd postgres

# Paso 6: cambiar la contraseña del usuario db postgres
sudo -i -u postgres
psql
ALTER USER postgres WITH PASSWORD 'nueva_contraseña_segura';
exit
exit

# Paso 7: reinicia PostgreSQL
sudo systemctl restart postresql

# Paso 8: importa y descomprime la dvdrental
wget https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip
unzip dvdrental.zip

# Paso 9: 
cp dvdrental.tar /var/lib/pgsql/
chown postgres:postgres /var/lib/pgsql/dvdrental.tar

# Paso 10: entra a postgres como user
sudo -i -u postgres

# Paso 11: crea una nueva database llamada dvdrental
createdb dvdrental

# Paso 12: restaura el backup dentro de la dvdrental database y sales
pg_restore -U postgres -d dvdrental dvdrental.tar
\q

# Paso 13: configura el firewalld (si es que tiene)
sudo firewall-cmd --permanent --add-port=5432/tcp
sudo firewall-cmd --reload

# Paso 14: configura el SELinux
sudo setsebool -P httpd_can_network_connect_db 1

# Paso 15: inicia y habilita el postgresql
sudo systemctl start postgresql
sudo systemctl enable postgresql




