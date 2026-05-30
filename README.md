# TCP File Transfer and Chat

Aplicação cliente-servidor desenvolvida em Python para comunicação via TCP, oferecendo funcionalidades de chat em tempo real e transferência segura de arquivos.

## Funcionalidades

* Chat entre clientes conectados ao servidor
* Download de arquivos hospedados no servidor
* Transferência de arquivos em chunks
* Validação de integridade utilizando SHA-256
* Proteção contra ataques de Path Traversal
* Arquitetura orientada a objetos
* Comunicação baseada em protocolo próprio
* Processamento concorrente utilizando threads
* Logs de conexão e transferência

## Arquitetura

O sistema é dividido em dois componentes principais:

### Servidor

Responsável por:

* Aceitar conexões TCP
* Gerenciar clientes conectados
* Realizar broadcast de mensagens de chat
* Processar solicitações de download
* Validar acesso aos arquivos
* Enviar metadados e conteúdo dos arquivos

### Cliente

Responsável por:

* Enviar mensagens de chat
* Solicitar downloads
* Receber arquivos
* Validar integridade após transferência
* Exibir mensagens recebidas

## Protocolo de Comunicação

A comunicação utiliza cabeçalhos JSON contendo metadados da mensagem.

Exemplo:

```json
{
  "command": "DOWNLOAD",
  "payload_size": 1024,
  "filename": "arquivo.pdf",
  "filesize": 5242880,
  "sha256": "..."
}
```

### Comandos Suportados

| Comando  | Descrição                |
| -------- | ------------------------ |
| CHAT     | Envio de mensagens       |
| DOWNLOAD | Solicitação de arquivo   |
| FILE     | Transferência de arquivo |
| ERROR    | Retorno de erro          |
| EXIT     | Encerramento da conexão  |

## Segurança

### Validação de Caminho

Todos os arquivos solicitados passam por validação para impedir acesso fora do diretório configurado.

### Integridade

Após a transferência, o cliente calcula o SHA-256 do arquivo recebido e compara com o hash enviado pelo servidor.

## Execução

### Iniciar o servidor

```bash
python server.py
```

### Iniciar um cliente

```bash
python client.py
```

## Exemplo de Uso

```text
================================
1 - Chat
2 - Download
3 - Sair
================================
```

### Chat

```text
1
Diga: Olá pessoal
```

### Download

```text
2
Arquivo: exemplo.pdf
```

## Estrutura do Projeto

```text
project/
├── client.py
├── server.py
├── protocol/
├── services/
├── domain/
├── configuration/
├── utils/
└── threads/
```

## Tecnologias

* Python 3
* Socket TCP
* Threading
* JSON
* SHA-256

## Objetivos Educacionais

Este projeto foi desenvolvido com foco em:

* Programação de redes
* Protocolos de aplicação
* Concorrência com threads
* Transferência segura de arquivos
* Boas práticas de arquitetura em Python
* Segurança básica em aplicações TCP
