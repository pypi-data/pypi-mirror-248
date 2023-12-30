# Flask JobManager

Biblioteca de gerenciamento de tarefas, ao definir uma tarefa sera catalogado em uma lista de tarefas e poderar ser visto em uma pagina web.

a biblioteca ta em teste e abertas a contribuições.

## Como implementar
a definição da secret_key é importante para o uso, na falta da definição da variavel JOB_MANAGER_PASSWORD_KEY a secret_key sera usada como senha para acessar os jobs

```python
app = Flask(__name__)
jm = JobManager(app)
```
ou

```python
app = Flask(__name__)
jm = JobManager()
jm.init_app(app)
```

## Como criar uma task

```python

# definição da tarefa
def teste():
    ...

processo1 = jm.tasks.new(
    "teste1",
    teste,
    group="Ola Mundo",
    description="uma task de teste para visualização",
)
processo2 = jm.tasks.new(
    "teste2",
    teste,
    description="uma task de teste para visualização",
)
processo3 = jm.tasks.new(
    "teste3",
    teste,
    description="uma task de teste para visualização",
)
processo4 = jm.tasks.new(
    "teste4",
    teste,
)

```

## Declaração com parametros e decorador
```python
#decoração sem argumentos
@job_manager.tasks.decorate()
def ola_mundo():
    """Função que imprime ola mundo"""
    print("ola mundo")

#declaração com argumentos
@job_manager.tasks.decorate(kwargs={"texto": "ola"})
def imprimir(texto):
    print(texto)

#chamada individual
imprimir("ola mundo")
```

## Tela de gerenciamento
![Captura de tela de 2023-11-18 21-18-13](https://github.com/feiticeiro-tec/flask-JobManager/assets/53744463/075de845-2621-4b35-8f5f-b03064e6ce18)
