from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import asyncio

app = FastAPI()
lock = asyncio.Lock()


contador_id = 36
produtos_df = pd.DataFrame(
    {
        "id": list(range(1, contador_id)),
        "codigo": [451, 789, 123, 567, 890, 234, 678, 901, 345, 765,
            432, 876, 109, 543, 210, 654, 987, 321, 753, 951,
            852, 159, 486, 753, 369, 147, 258, 963, 145, 785,
            236, 985, 175, 305, 407],
        "nome": ["Arroz", "Feijão", "Macarrão", "Óleo de Soja", "Sal", "Açúcar", "Café", "Leite", "Pão de Forma", "Queijo Prato",
            "Presunto", "Peito de Frango", "Peixe Tilápia", "Maçã", "Banana", "Laranja", "Alface", "Tomate", "Cebola",
            "Batata", "Cenoura", "Sabão em Pó", "Shampoo", "Detergente", "Refrigerante", "Suco de Laranja", "Água Mineral",
            "Vinho Tinto", "Cerveja", "Iogurte", "Manteiga", "Ovos (Dúzia)", "Parafuso", "Controle", "Tangerina" ],
        "categoria": ["Grão", "Grão", "Massa", "Óleo", "Tempero", "Tempero", "Bebida", "Laticínio", "Padaria", "Frio",
            "Frio", "Frio", "Frio", "Fruta", "Fruta", "Fruta", "Hortifruti", "Hortifruti", "Hortifruti",
            "Hortifruti", "Hortifruti", "Limpeza", "Higiene", "Limpeza", "Bebida", "Bebida", "Bebida",
            "Bebida", "Bebida", "Laticínio", "Laticínio", "Frio", "Mercearia", "Eletrônico", "Fruta"],
        "preco": [50.00, 2.00, 25.50, 8.90, 4.20, 7.50, 2.10, 5.00, 14.80, 4.50, 
            6.70, 15.00, 12.30, 18.00, 22.00, 6.00, 3.50, 4.00, 3.00, 8.00, 
            5.50, 4.80, 3.90, 19.90, 23.40, 2.80, 8.50, 10.00, 2.50, 45.00, 
            3.80, 6.20, 9.00, 16.00, 3.70]
    }
)

class Produto(BaseModel):
    codigo: int
    nome: str
    categoria: str
    preco: float

@app.get("/produtos")
def listar_produto():
    return produtos_df.to_dict(orient = "records")

@app.get("/produtos/{id}")
def obter_produto(id: int):
    filtro = produtos_df["id"] == id
    produto = produtos_df[filtro]
    if produto.empty:
        raise HTTPException(status_code=404, detail=f"Produto id:{id}, não encontrado")
    
    return produto.to_dict(orient="records")[0]

@app.post("/produtos")
async def criar_produto(produto: Produto):
    async with lock:
        global produtos_df, contador_id

        novo_produto = {
            "id": contador_id,
            "codigo": produto.codigo,
            "nome": produto.nome,
            "categoria": produto.categoria,
            "preco": produto.preco
        }

        produtos_df = produtos_df._append(novo_produto, ignore_index=True)
        contador_id = contador_id+1

        produtos_df.to_csv('produtos.csv', index=False)
        return {
            "mensagem": "Produto criado com sucesso!",
            "produto": novo_produto
        }

@app.put("/produtos/{id}")
async def atualizar_produto(id: int, produto: Produto):
    async with lock:
        global produtos_df
        produto_antigo_idx = produtos_df.index[produtos_df["id"] == id]
        if produto_antigo_idx.empty:
            raise HTTPException(status_code=404, detail=f"Produto id:{id}, não encontrado")
        
        produtos_df.loc[produto_antigo_idx, ["codigo", "nome", "categoria", "preco"]] = [produto.codigo, produto.nome, produto.categoria, produto.preco]
        
        produtos_df.to_csv('produtos.csv', index=False)
        return {
            "mensagem": f"Produto {id} atualizado com sucesso!",
            "produto": produtos_df.loc[produto_antigo_idx].to_dict(orient="records")[0]
        }

@app.delete("/produtos/{id}")
async def apagar_produto(id: int):
    async with lock:
        global produtos_df
        produto_apagar_idx = produtos_df.index[produtos_df["id"] == id]
        if produto_apagar_idx.empty:
            raise HTTPException(status_code=404, detail=f"Produto id:{id}, não encontrado")
        produtos_df = produtos_df.drop(produto_apagar_idx).reset_index(drop = True)
        
        produtos_df.to_csv('produtos.csv', index=False)
        return { "mensagem":  f"Produto com {id} apagado com sucesso!"}

@app.get("/maior-preco")
def maior_preco():
    id_maior_preco = produtos_df['preco'].idxmax()

    nome_maior_preco = produtos_df.loc[id_maior_preco]['nome']
    valor_maior_preco = produtos_df.loc[id_maior_preco]['preco']

    return f"Produto mais caro: {nome_maior_preco}\nValor do produto: {valor_maior_preco}\n"

@app.get("/menor-preco")
def menor_preco():
    id_menor_preco = produtos_df['preco'].idxmin()

    nome_menor_preco = produtos_df.loc[id_menor_preco]['nome']
    valor_menor_preco = produtos_df.loc[id_menor_preco]['preco']

    return f"Produto mais barato: {nome_menor_preco}\nValor do produto: {valor_menor_preco}\n"

@app.get("/media-precos")
def media_precos():
    media = produtos_df['preco'].mean()
    return f"A média dos preços é {round(media, 2)}\n"
    

@app.get("/produtos-acima-media")
def produtos_acima_media():
    media = produtos_df['preco'].mean()

    produtos_acima_media = produtos_df[produtos_df['preco'] >= media]
    output_string= f''

    for objeto in produtos_acima_media.to_dict('records'):
        output_string += (f"Produto: {objeto['nome']}, Preço: {objeto['preco']}\n")

    return output_string

@app.get("/produtos-abaixo-media")
def produtos_abaixo_media():
    media = produtos_df['preco'].mean()

    produtos_abaixo_media = produtos_df[produtos_df['preco'] < media]
    output_string= f''

    for objeto in produtos_abaixo_media.to_dict('records'):
        output_string += (f"Produto: {objeto['nome']}, Preço: {objeto['preco']}\n")

    return output_string