#language:pt

Funcionalidade: Cadastro de publicações no sistema

Contexto:
  Dado que a URL da API é "https://jsonplaceholder.typicode.com/posts/"
    E defino o parâmetro Content Type do cabeçalho como "application/json"
    E defino o parâmetro Accept do cabeçalho como "application/json"

Cenário: Criar uma publicação
  Quando defino a "<coluna>" e o "<valor>" como segue

    | coluna   | valor               |
    | title    | título teste        |
    | body     | conteúdo publicação |
    | userId   | 1                   |

    E faço a requisição "POST"
  Então o código da resposta deve ser "201"

Cenário: Ler uma publicação
  Quando informo que o ID da publicação que quero ler é o "1"
	E faço a requisição "GET"
  Então o código da resposta deve ser "200"
	E o conteúdo do BODY não deve estar vazio

Cenário: Atualizar uma publicação
  Quando defino a "<coluna>" e o "<valor>" como segue

    | coluna   | valor                          |
    | id       | 1                              |
    | title    | título atualizado              |
    | body     | conteúdo publicação atualizado |
    | userId   | 1                              |

    E faço a requisição "PUT"
  Então o código da resposta deve ser "200"

Cenário: Apagar uma publicação
  Quando informo que o ID da publicação que quero apagar é o "1"
	E faço a requisição "DELETE"
  Então o código da resposta deve ser "200"
	E o conteúdo do BODY deve estar vazio
