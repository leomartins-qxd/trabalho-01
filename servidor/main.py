from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import asyncio

app = FastAPI()
lock = asyncio.Lock()


produtos_df = pd.read_csv('produtos.csv')
contador_id = int(produtos_df['id'].max())+1

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
