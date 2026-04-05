
# LAB 1 - Sistema de Chat com Deteção de Dados Pessoais - Rafael Sampaio | 2025157604

## Descrição

Este projeto consiste num sistema de chat multiutilizador como foi pedido pelo professor, com comunicação em tempo real entre clientes e servidor através de sockets TCP. O sistema suporta múltiplas ligações simultâneas através de threading e inclui mecanismos de deteção de dados pessoais, em conformidade com princípios básicos do GDPR.

Além disso, o servidor inclui uma verificação simples de possíveis tentativas de engenharia social, identificando mensagens suspeitas que peçam dados pessoais aos utilizadores.

## Funcionalidades

- Chat multiutilizador em tempo real
- Comunicação cliente-servidor via socket
- Suporte a múltiplos clientes com threading
- Deteção de:
  - e-mails
  - números de telefone
  - endereços IP
  - datas de nascimento
  - cartões de crédito
  - nomes completos (heurística)
- Bloqueio de mensagens com dados pessoais
- Registo de tentativas suspeitas de engenharia social
- Mensagens públicas
- Mensagens privadas entre utilizadores
- Mensagens para grupos
- Logs de ligação, desconexão, bloqueios e suspeitas

## Estrutura do projeto

```bash
Lab01_Rafael/
│
├── server.py
├── client.py
├── detector.py
├── logs/
│   ├── server.log
│   ├── personal_data.log
│   └── suspicious.log
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.10 ou superior

Não é necessária instalação de bibliotecas externas, pois o projeto usa apenas bibliotecas standard do Python:

- `socket`
- `threading`
- `logging`
- `json`
- `re`
- `os`

## Como executar

### 1. Iniciar o servidor

```bash
python server.py
```

O servidor ficará a escutar em:

```bash
127.0.0.1:5555
```

### 2. Iniciar clientes

Em terminais diferentes, executar:

```bash
python client.py
```

## Comandos disponíveis no cliente

### Mensagem pública

Escrever normalmente no terminal:

```text
Olá a todos
```

### Sair do chat

```text
exit
```

### Ver utilizadores online

```text
/users
```

### Mensagem privada

```text
/pm nomeutilizador Olá, esta é uma mensagem privada
```

### Criar grupo

```text
/creategroup grupo1 user2,user3
```

### Enviar mensagem para grupo

```text
/groupmsg grupo1 Olá grupo
```

### Ver grupos

```text
/groups
```

## Deteção de dados pessoais

O sistema bloqueia mensagens que contenham possíveis dados pessoais, como:

- e-mails
- números de telefone
- IPs
- datas de nascimento
- cartões de crédito
- nomes completos

Exemplo de mensagem bloqueada:

```text
O meu email é exemplo@gmail.com
```

O cliente recebe um alerta de bloqueio e o servidor regista o evento em:

```bash
logs/personal_data.log
```

## Deteção de engenharia social

O servidor tenta identificar padrões suspeitos em mensagens, como pedidos de password, e-mail, número de telefone ou outros dados sensíveis.

Essas tentativas são registadas em:

```bash
logs/suspicious.log
```

## Logs

### server.log

Regista:

- arranque do servidor
- ligações e desconexões
- mensagens aceites
- erros

### personal_data.log

Regista:

- mensagens bloqueadas por conterem dados pessoais
- utilizador associado
- tipo de deteção encontrada

### suspicious.log

Regista:

- mensagens suspeitas de engenharia social
- padrões detetados
- utilizador associado
