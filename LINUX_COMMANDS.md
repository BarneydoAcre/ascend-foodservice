# CloudSys

## LINUX Initialization 
```
sudo apt-get update
```
```
sudo apt-get upgrade
```


## Commands for POSTGRES CONFIGURATION
```
sudo apt install postgresql postgresql-contrib
```
### Para criar o banco sem desvincular o usuário root rodar ->
```
sudo -u postgres createdb nome_do_banco
```
### Para alterar a senha default da conexão POSTGRES ->
```
sudo passwd postgres
```
```
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'nova_senha'"
```

