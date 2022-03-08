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