# Diploma_Ilia_G_17
For start postgres on docker 
sudo docker run --rm --name postgres -p 5432:5432 \
     -e POSTGRES_PASSWORD=P@ssw0rd \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_DB=db \
     -d postgres \
     -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data 

For PGAdmin
sudo docker run -p 5050:80 \
    -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" \
    -e "PGADMIN_DEFAULT_PASSWORD=SuperSecret" \
    -d dpage/pgadmin4
