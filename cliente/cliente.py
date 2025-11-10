import httpx

BASE_URL = "http://127.0.0.1:8000"

def criar_produto(produto):
    resp = httpx.post(
        f"{BASE_URL}/produtos",
        json = {"codigo": produto.get("codigo"), "nome": produto.get("nome"), "categoria": produto.get("categoria"), "preco" : produto.get("preco")}
    )
    print("TESTANDOOOOOOOOO")
    print(resp.json())
    return resp

def listar_produtos():
    resp = httpx.get(f"{BASE_URL}/produtos")
    print(resp.json())

def obter_produto(id):
    resp = httpx.get(f"{BASE_URL}/produtos/{id}")
    print(resp.json())

def atualizar_produto(id, produto):
    resp = httpx.put(
        f"{BASE_URL}/produtos/{id}",
        json = {"codigo": produto.get("codigo"), "nome": produto.get("nome"), "categoria": produto.get("categoria"), "preco": produto.get("preco")}
    )
    print(resp.json())

def apagar_produto(id):
    resp = httpx.delete(f"{BASE_URL}/produtos/{id}")
    return resp.json()

def maior_preco():
    resp = httpx.get(f"{BASE_URL}/maior-preco")
    print(resp.json())

def menor_preco():
    resp = httpx.get(f"{BASE_URL}/menor-preco")
    print(resp.json())

def media_precos():
    resp = httpx.get(f"{BASE_URL}/media-precos")
    print(resp.json())

def produtos_acima_media():
    resp = httpx.get(f"{BASE_URL}/produtos-acima-media")
    print(resp.json())

def produtos_abaixo_media():
    resp = httpx.get(f"{BASE_URL}/produtos-abaixo-media")
    print(resp.json())


produto_teste = {
    "codigo": 0,
    "nome": "Banana",
    "categoria": "Fruta",
    "preco": 10
}

produto_atualizar = {
    "codigo": 25,
    "nome": "Cerveja",
    "categoria": "Bebida",
    "preco": 9
}

#criar_produto(produto_teste)
#listar_produtos()
#obter_produto(2)
#atualizar_produto(1, produto_atualizar)
#listar_produtos()
#tualizar_produto(2, produto_teste)
##listar_produtos()
#apagar_produto(3)
#obter_produto(3)
maior_preco()
menor_preco()
media_precos()
produtos_acima_media()
produtos_abaixo_media()