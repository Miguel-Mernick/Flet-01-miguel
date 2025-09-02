import flet as ft

def main(page: ft.Page):
    """
    Aplicativo de Loja Virtual Mini com funcionalidades de filtro, carrinho e finalização de compra.
    """

    # -----------------------------
    # Configurações da página
    # -----------------------------
    page.title = "🛒 Lojinha do Jegue"
    page.vertical_alignment = "start"
    page.scroll = "auto"
    page.theme_mode = "light"
    page.padding = 20

    # -----------------------------
    # Produtos disponíveis
    # -----------------------------
    produtos = [
        {"nome": "Livro", "preco": 50, "categoria": "Educação"},
        {"nome": "Camiseta", "preco": 80, "categoria": "Roupas"},
        {"nome": "Celular", "preco": 1200, "categoria": "Eletrônicos"},
        {"nome": "Bola", "preco": 60, "categoria": "Brinquedos"},
        {"nome": "Fone de Ouvido", "preco": 200, "categoria": "Eletrônicos"},
        {"nome": "Boneca", "preco": 100, "categoria": "Brinquedos"},
    ]

    # -----------------------------
    # Estado do carrinho
    # -----------------------------
    carrinho = {}

    # -----------------------------
    # Elementos visuais
    # -----------------------------
    lista_produtos = ft.Row(wrap=True, spacing=20, run_spacing=20)
    lista_carrinho = ft.Column(spacing=10)
    contador_carrinho = ft.Text("Carrinho vazio 🛒", size=16, italic=True)

    # Campos de filtro
    filtro_categoria = ft.Dropdown(
        label="Categoria",
        options=[
            ft.dropdown.Option("Todas"),
            ft.dropdown.Option("Educação"),
            ft.dropdown.Option("Roupas"),
            ft.dropdown.Option("Eletrônicos"),
            ft.dropdown.Option("Brinquedos"),
        ],
        value="Todas",
    )

    filtro_preco = ft.TextField(label="Preço máximo", width=150)
    busca_nome = ft.TextField(label="Buscar produto", width=200)

    # -----------------------------
    # Funções
    # -----------------------------
    def atualizar_lista_produtos(e=None):
        lista_produtos.controls.clear()
        cat = filtro_categoria.value
        try:
            preco_max = float(filtro_preco.value) if filtro_preco.value else None
        except ValueError:
            preco_max = None
        busca = busca_nome.value.lower()

        for p in produtos:
            if cat != "Todas" and p["categoria"] != cat:
                continue
            if preco_max and p["preco"] > preco_max:
                continue
            if busca and busca not in p["nome"].lower():
                continue

            card = ft.Card(
                elevation=4,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(p["nome"], size=18, weight="bold"),
                            ft.Text(f"R$ {p['preco']}", color="green", size=16),
                            ft.Text(f"Categoria: {p['categoria']}", size=14, color="grey"),
                            ft.ElevatedButton(
                                "Adicionar ao Carrinho",
                                on_click=lambda e, prod=p: adicionar_carrinho(prod),
                                bgcolor="#007BFF",
                                color="white",
                            ),
                        ],
                        horizontal_alignment="center",
                        spacing=5,
                    ),
                    width=200,
                    padding=15,
                ),
            )
            lista_produtos.controls.append(card)
        page.update()

    def atualizar_carrinho():
        lista_carrinho.controls.clear()
        if not carrinho:
            contador_carrinho.value = "Carrinho vazio 🛒"
        else:
            contador_carrinho.value = f"Itens no carrinho: {sum(carrinho.values())}"
            for nome, qtd in carrinho.items():
                lista_carrinho.controls.append(
                    ft.Row(
                        [
                            ft.Text(f"{nome} x{qtd}", size=16),
                            ft.IconButton(
                                ft.icons.DELETE,
                                on_click=lambda e, prod=nome: remover_carrinho(prod),
                                icon_color="red",
                            ),
                        ],
                        alignment="spaceBetween",
                    )
                )
        page.update()

    def adicionar_carrinho(prod):
        nome = prod["nome"]
        carrinho[nome] = carrinho.get(nome, 0) + 1
        atualizar_carrinho()

    def remover_carrinho(nome):
        if nome in carrinho:
            carrinho[nome] -= 1
            if carrinho[nome] <= 0:
                del carrinho[nome]
        atualizar_carrinho()

    def finalizar_compra(e):
        if carrinho:
            carrinho.clear()
            atualizar_carrinho()
            page.dialog = ft.AlertDialog(
                title=ft.Text("Compra Finalizada 🎉", size=20, weight="bold"),
                content=ft.Text("Obrigado pela sua compra! Seu pedido será processado."),
                actions=[ft.TextButton("Fechar", on_click=lambda e: fechar_dialog())],
            )
            page.dialog.open = True
            page.update()

    def fechar_dialog():
        page.dialog.open = False
        page.update()

    # -----------------------------
    # Layout
    # -----------------------------
    filtros = ft.Row(
        [
            filtro_categoria,
            filtro_preco,
            busca_nome,
            ft.ElevatedButton("Filtrar", on_click=atualizar_lista_produtos),
        ],
        alignment="center",
    )

    page.add(
        ft.Text("🛍️ Loja do Jegue", size=32, weight="bold", color="blue"),
        filtros,
        ft.Divider(),
        ft.Text("Produtos:", size=22, weight="bold"),
        lista_produtos,
        ft.Divider(),
        ft.Text("Carrinho:", size=22, weight="bold"),
        contador_carrinho,
        lista_carrinho,
        ft.ElevatedButton(
            "Finalizar Compra",
            on_click=finalizar_compra,
            bgcolor="green",
            color="white",
            width=200,
        ),
    )

    atualizar_lista_produtos()
    atualizar_carrinho()

ft.app(target=main)
