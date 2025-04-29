# Estoque da Loja
![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![mysql](https://img.shields.io/badge/MySQL-4B7B9F?style=for-the-badge&logo=mysql&logoColor=white)

![imagem da home page](static/images/estoque-home-page.png)

## Sobre 📝
Projeto full-stack feito para facilitar a contagem de produtos do estoque de uma loja de cama, mesa, banho e plásticos. Aqui você pode ver os produtos, adicionar um novo, excluir e editar.

### Frontend
- Construído com a tecnologia Jinja embutida ao Flask

### Backend
- API contruída com o framework Flask e para o banco de dados foi usado o framework MySQLAlchemy para ligar a um servidor mysqlite.

## Instalação 🚀
```bash
# Clonando repositório
$ git clone https://github.com/lnr273/estoque-da-loja.git

# Instalando dependências
$ pip install -r dependencies.txt 
```

## Rodando 🤖
No terminal do IDLE, rode:
```
python app.py
```
O site estará acessível em: [http://localhost:5000/](http://localhost:5000/) 

## Rotas 🛣️
A API concede os seguintes endpoint:
```
GET / Página inicial com tabela dos produtos do banco de dados

GET /add Página para formulário de adição de produto

GET /edit Página para formulário de edição de produto

GET /delete Remove produto do banco de dados com parâmetro da url

GET /search Pesquisa produtos do banco de dados por id, nome e categoria

POST /add Adiciona os valores do formulário ao banco de dados

POST /edit Atualiza os valores do banco de dados para os novos vindos do formulário
```

## Próximos passos
- Adicionar página com mais detalhes sobre o produto, como foto e descrição detalhada.
- Controle de estoque: movimentação dos produtos, notificar produtos com baixa quantidade.