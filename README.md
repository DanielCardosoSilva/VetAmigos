# VetAmigos — Sistema de Gestão Veterinária

O VetAmigos é uma aplicação desenvolvida em Python, destinada à gestão das operações de uma clínica veterinária.

O projeto permite gerir funcionários, clientes, animais, consultas, vacinação, medicamentos, receitas médicas, faturação e relatórios, centralizando a informação numa base de dados SQLite.

Foi desenvolvido com uma interface de linha de comandos (CLI) e uma arquitetura modular baseada no padrão MVC (Model–View–Controller), complementada pelas camadas de serviços e repositórios.



# Objetivos

Digitalizar e simplificar os processos administrativos e clínicos.

Centralizar os dados de clientes, animais e consultas.

Facilitar o acompanhamento do histórico clínico dos animais.

Controlar o acesso às funcionalidades através de perfis de funcionários.

Aplicar boas práticas de programação orientada a objetos, separação de responsabilidades e testes unitários.


# Funcionalidades


## Gestão de funcionários

Registo inicial do proprietário da clínica.

Autenticação através de nome de utilizador e palavra-passe.

Registo de novos funcionários.

Listagem de funcionários.

Desativação e reativação de contas.

Controlo de permissões de acordo com o perfil.


O sistema contempla três tipos de funcionários:

Proprietário: Administração e gestão da clínica

Médico Veterinário: Consultas, vacinação, medicamentos e receitas

Recepcionista: Clientes, animais, agendamentos e faturação



## Gestão de clientes

Registo e listagem de clientes.

Associação através do NIF.

Validação de dados introduzidos.

Verificação de telefone com exatamente 9 dígitos.

Verificação da presença de @ no email.



## Gestão de animais

Registo de animais associados aos respetivos clientes.

Armazenamento de informações como nome, espécie, data de nascimento e peso.

Consulta dos animais registados.

Atualização do peso após uma consulta clínica.



## Gestão de consultas

Agendamento de consultas para animais registados.

Associação de um médico veterinário.

Registo do motivo da consulta.

Consulta do histórico clínico.

Cancelamento de consultas.

Conclusão de consultas pelo veterinário responsável.

Na conclusão de uma consulta, o médico veterinário pode registar: Diagnóstico, tratamento, sumário clínico, custo e peso observado.

Quando o peso observado é diferente do peso atual do animal, o sistema atualiza o respetivo registo.



## Gestão de vacinação

Registo de vacinas administradas.

Associação das vacinas aos animais.

Registo da data de administração e da próxima dose.

Consulta de informações de vacinação.



## Gestão de medicamentos e receitas

Registo e consulta de medicamentos.

Controlo de quantidades disponíveis.

Emissão de receitas médicas associadas a consultas.

Associação de medicamentos às receitas.

Registo da quantidade prescrita e da posologia.



## Faturação e relatórios

Gestão de faturas associadas às consultas.

Registo de valores e estados de pagamento.

Consulta de informações financeiras.

Consulta de relatórios de gestão.





# Instalação e execução

## 1. Requisitos

É necessário ter o Python 3 instalado.

## Para confirmar a instalação:

```bash
python --version
```


## 2. Clonar o repositório

```bash
git clone https://github.com/DanielCardosoSilva/VetAmigos.git
```

## Entrar na pasta do projeto:

```bash
cd VetAmigos
```

## 3. Executar a aplicação

```bash
python main.py
```


Na primeira execução, o sistema inicializa a base de dados SQLite e permite criar a conta inicial de proprietário, caso ainda não exista.

Após o registo, é possível iniciar sessão e aceder às funcionalidades disponíveis para o respetivo perfil.


# Testes unitários

O projeto utiliza a biblioteca unittest do Python.

Para testar as camadas isoladamente, são utilizados objetos MagicMock, que simulam dependências como repositórios e serviços sem exigir operações reais na base de dados.


## Na raiz do projeto:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Executar um ficheiro de testes específico


## Por exemplo:

```bash
python -m unittest tests.test_consulta -v
```


Os testes permitem verificar regras de negócio, validações, chamadas entre componentes e o comportamento esperado das operações.



# Desenvolvimento

Projeto: VetAmigos — Sistema de Gestão Veterinária

Equipa: Alexandre Petarli, Daniel Silva, David Branco e Regina Silva

Finalidade: Projeto académico de desenvolvimento de software, com aplicação de programação orientada a objetos, arquitetura MVC, persistência de dados e testes unitários.
