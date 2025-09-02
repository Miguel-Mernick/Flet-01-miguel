import flet as ft

def main(page: ft.Page):
    """
    Aplicativo multi-página moderno e interativo desenvolvido com Flet.
    """

    page.title = "Meu App Moderno"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.GREY_50

    # Estado global
    pagina_atual = "home"
    dados_usuario = {
        "nome": "Estudante Flet",
        "nivel": "Iniciante",
        "pontos": 150,
        "configuracoes": {
            "modo_escuro": False,
            "notificacoes": True,
            "som": True
        }
    }

    # ---------------- Funções de navegação ---------------- #
    def mudar_pagina(nova_pagina):
        nonlocal pagina_atual
        if pagina_atual == nova_pagina:
            return  # Evita atualizações desnecessárias
        print(f"Mudando de página: {pagina_atual} -> {nova_pagina}")  # Log para depuração
        pagina_atual = nova_pagina

        # Esconde todas
        for conteudo in [conteudo_home, conteudo_perfil, conteudo_config, conteudo_sobre]:
            conteudo.visible = False

        # Mostra selecionada
        if nova_pagina == "home":
            conteudo_home.visible = True
        elif nova_pagina == "perfil":
            conteudo_perfil.visible = True
        elif nova_pagina == "config":
            conteudo_config.visible = True
        elif nova_pagina == "sobre":
            conteudo_sobre.visible = True

        atualizar_barra_navegacao()
        page.update()

    # Funções de clique
    def ir_para_home(e): mudar_pagina("home")
    def ir_para_perfil(e): mudar_pagina("perfil")
    def ir_para_config(e): mudar_pagina("config")
    def ir_para_sobre(e): mudar_pagina("sobre")

    # ---------------- Cabeçalho ---------------- #
    cabecalho = ft.Container(
        content=ft.Text("Meu App Moderno", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        bgcolor=ft.Colors.BLUE,
        padding=ft.padding.symmetric(vertical=25),
        alignment=ft.alignment.center
    )

    # ---------------- Barra de navegação ---------------- #
    def criar_item_navegacao(icone, label, pagina_nome, on_click_func):
        return ft.GestureDetector(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(icone, size=26, color=ft.Colors.GREY_600),
                        ft.Text(label, size=12, color=ft.Colors.GREY_600)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                ),
                padding=ft.padding.symmetric(vertical=10, horizontal=18),
                border_radius=12,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
            ),
            on_tap=on_click_func
        )

    item_home = criar_item_navegacao(ft.Icons.HOME, "Início", "home", ir_para_home)
    item_perfil = criar_item_navegacao(ft.Icons.PERSON, "Perfil", "perfil", ir_para_perfil)
    item_config = criar_item_navegacao(ft.Icons.SETTINGS, "Config", "config", ir_para_config)
    item_sobre = criar_item_navegacao(ft.Icons.INFO, "Sobre", "sobre", ir_para_sobre)

    def atualizar_barra_navegacao():
        for item, nome in [(item_home, "home"), (item_perfil, "perfil"), (item_config, "config"), (item_sobre, "sobre")]:
            container = item.content
            icone = container.content.controls[0]
            texto = container.content.controls[1]
            if pagina_atual == nome:
                container.bgcolor = ft.Colors.BLUE_50
                container.border = ft.border.all(2, ft.Colors.BLUE_300)
                icone.color = ft.Colors.BLUE
                texto.color = ft.Colors.BLUE
                texto.weight = ft.FontWeight.BOLD
            else:
                container.bgcolor = ft.Colors.TRANSPARENT
                container.border = None
                icone.color = ft.Colors.GREY_600
                texto.color = ft.Colors.GREY_600
                texto.weight = ft.FontWeight.NORMAL

    barra_navegacao = ft.Container(
        content=ft.Row(
            controls=[item_home, item_perfil, item_config, item_sobre],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor=ft.Colors.WHITE,
        padding=ft.padding.only(top=12, bottom=25),
        border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.GREY_300)),
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, -2)),
        height=80
    )

    # ---------------- Páginas ---------------- #
    # HOME
    conteudo_home = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.HOME, size=80, color=ft.Colors.BLUE),
                ft.Text("Bem-vindo ao App! 🎉", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Explore as páginas usando a barra inferior", size=16, color=ft.Colors.GREY_700),
                ft.Container(height=20),
                ft.Text("🎯 Toque nos ícones para navegar!", size=14, color=ft.Colors.BLUE_600)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=40,
        visible=True
    )

    # PERFIL
    texto_pontos = ft.Text(f"Pontos: {dados_usuario['pontos']} ⭐", size=16)
    def adicionar_pontos(e):
        dados_usuario["pontos"] += 10
        texto_pontos.value = f"Pontos: {dados_usuario['pontos']} ⭐"
        page.update()

    conteudo_perfil = ft.Container(
        content=ft.Column(
            controls=[
                ft.CircleAvatar(content=ft.Icon(ft.Icons.PERSON, size=50, color=ft.Colors.WHITE), bgcolor=ft.Colors.BLUE, radius=60),
                ft.Text(dados_usuario["nome"], size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Nível: {dados_usuario['nivel']}", size=16, color=ft.Colors.BLUE_600),
                texto_pontos,
                ft.Container(height=20),
                ft.ElevatedButton("Ganhar Pontos! 🎯", on_click=adicionar_pontos, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=40,
        visible=False
    )

    # CONFIG
    def alternar_modo_escuro(e): dados_usuario["configuracoes"]["modo_escuro"] = e.control.value
    def alternar_notificacoes(e): dados_usuario["configuracoes"]["notificacoes"] = e.control.value
    def alternar_som(e): dados_usuario["configuracoes"]["som"] = e.control.value

    conteudo_config = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.SETTINGS, size=60, color=ft.Colors.BLUE),
                ft.Text("Configurações ⚙️", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                ft.Switch("Modo escuro", value=dados_usuario["configuracoes"]["modo_escuro"], on_change=alternar_modo_escuro),
                ft.Switch("Notificações", value=dados_usuario["configuracoes"]["notificacoes"], on_change=alternar_notificacoes),
                ft.Switch("Som", value=dados_usuario["configuracoes"]["som"], on_change=alternar_som),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=40,
        visible=False
    )

    # SOBRE
    conteudo_sobre = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.INFO, size=60, color=ft.Colors.BLUE),
                ft.Text("Sobre o App ℹ️", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                ft.Text("Versão: 1.0.0", size=16),
                ft.Text("Desenvolvido com Flet", size=16),
                ft.Text("Python + Interface Mobile", size=16),
                ft.Container(height=20),
                ft.Text("Este app demonstra navegação entre páginas, gerenciamento de estado e interface completa!", size=14, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY_600)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=40,
        visible=False
    )

    # ---------------- Montagem da página ---------------- #
    stack_paginas = ft.Stack(controls=[conteudo_home, conteudo_perfil, conteudo_config, conteudo_sobre])

    page.add(
        ft.Column(
            controls=[
                cabecalho,
                ft.Container(content=stack_paginas, expand=True),
                barra_navegacao
            ],
            spacing=0,
            expand=True
        )
    )

ft.app(target=main)
