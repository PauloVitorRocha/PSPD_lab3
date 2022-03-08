Inicialmente precisamos subir o broker para realizar a troca de mensagens atraves do comando:
```
sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
```
Para rodar o sender use o comando dentro da pasta rabbitMQ:
```
python3 sender.py listaDeMaquinas tamanhoDoVetor
```
Ex.:
```
python3 sender.py maq1,maq2 100
```

Para rodar o receiver
```
python3 receiver.py nomeMaquina
```
Ex.:
```
python3 receiver.py maq1
```
