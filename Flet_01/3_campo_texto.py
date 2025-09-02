import flet as ft

def main(page: ft.Page):
    page.title = "Campo de Texto"
    page.padding = ft.padding.only(top=40, left=20, right=20, bottom=20)

    # Criando um campo para o usuário digitar
    campo_nome = ft.TextField(
        label="Digite seu nome aqui",  # Texto de orientação
        width=300,
        border_color=ft.Colors.BLUE
    )

    # Texto que mostrará a resposta
    resposta = ft.Text(
        value="",  # Inicialmente vazio
        size=18,
        text_align=ft.TextAlign.CENTER
    )

    def processar_nome(evento):
        """
        Função que pega o texto digitado pelo usuário e faz algo com ele.
        """
        nome_digitado = campo_nome.value

        if nome_digitado == "" or nome_digitado is None:
            resposta.value = "⚠️ Por favor, digite seu nome!"
            resposta.color = ft.Colors.RED
        elif len(nome_digitado) < 2:
            resposta.value = "⚠️ Nome muito curto!"
            resposta.color = ft.Colors.ORANGE
        else:
            resposta.value = f"✅ Olá, {nome_digitado}! Prazer em conhecê-lo(a)!"
            resposta.color = ft.Colors.GREEN

        page.update()

    # Botão para processar o nome
    botao_ok = ft.ElevatedButton(
        text="Confirmar",
        on_click=processar_nome,
        width=150
    )

    # Adicionando elementos à página
    page.add(
        ft.Text("Vamos nos conhecer!", size=22, weight=ft.FontWeight.BOLD),
        campo_nome,
        botao_ok,
        resposta
    )

ft.app(target=main)
