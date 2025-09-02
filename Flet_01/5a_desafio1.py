import flet as ft

def main(page: ft.Page):
    """
    Tela de criação de perfil com card, edição e exclusão de usuário.
    """

    page.title = "Criação de Perfil"
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Campos de entrada
    campo_nome = ft.TextField(label="Nome", width=300)
    campo_email = ft.TextField(label="E-mail", width=300)
    campo_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    campo_hobby = ft.Dropdown(
        label="Selecione seu hobby",
        width=300,
        options=[
            ft.dropdown.Option("🎮 Jogos"),
            ft.dropdown.Option("📚 Leitura"),
            ft.dropdown.Option("🎵 Música"),
            ft.dropdown.Option("⚽ Esportes"),
            ft.dropdown.Option("💻 Programação"),
        ]
    )

    # Card do usuário (inicialmente vazio)
    card_usuario = ft.Container()

    # Função para criar card
    def criar_card(nome, email, hobby):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("👤 Perfil Criado", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"📛 Nome: {nome}", size=16),
                        ft.Text(f"📧 Email: {email}", size=16),
                        ft.Text(f"🎯 Hobby: {hobby}", size=16),
                        ft.Row(
                            [
                                ft.ElevatedButton("✏️ Editar", on_click=lambda e: editar_perfil(nome, email, hobby)),
                                ft.ElevatedButton("🗑️ Excluir", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=excluir_perfil),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=15
            )
        )

    # Criar perfil
    def criar_perfil(e):
        nome = campo_nome.value
        email = campo_email.value
        senha = campo_senha.value
        hobby = campo_hobby.value

        if nome and email and senha and hobby:
            card_usuario.content = criar_card(nome, email, hobby)
        else:
            card_usuario.content = ft.Text(
                "⚠️ Preencha todos os campos antes de criar o perfil!",
                size=16, color=ft.Colors.RED
            )
        page.update()

    # Editar perfil
    def editar_perfil(nome, email, hobby):
        campo_nome.value = nome
        campo_email.value = email
        campo_hobby.value = hobby
        campo_senha.value = ""  # senha não volta por segurança
        card_usuario.content = ft.Text("✏️ Edite os dados no formulário acima e clique em 'Criar Perfil' novamente.", size=16, color=ft.Colors.BLUE)
        page.update()

    # Excluir perfil
    def excluir_perfil(e):
        campo_nome.value = ""
        campo_email.value = ""
        campo_senha.value = ""
        campo_hobby.value = None
        card_usuario.content = ft.Text("❌ Usuário excluído.", size=16, color=ft.Colors.RED)
        page.update()

    # Botão de criar perfil
    botao_criar = ft.ElevatedButton(
        "Criar Perfil", on_click=criar_perfil,
        bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE
    )

    # Layout principal
    layout = ft.Column(
        controls=[
            ft.Text("👤 Criação de Perfil", size=24, weight=ft.FontWeight.BOLD),
            campo_nome,
            campo_email,
            campo_senha,
            campo_hobby,
            botao_criar,
            card_usuario,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

    page.add(layout)

ft.app(target=main)
