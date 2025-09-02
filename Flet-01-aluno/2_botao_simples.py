import flet as ft

def main(page: ft.Page):
    page.title = "Meu Primeiro Botão"
    page.padding = 20

    # Criando um texto que será modificado pelo botão
    mensagem = ft.Text(
        value="Clique no botão ai meu parceiro!",
        size=20,
        text_align=ft.TextAlign.CENTER
    )

    def botao_clicado(evento):
        """
        Esta função será executada sempre que o botão for clicado.
        """
        # Mudando o texto da mensagem
        mensagem.value = "🎉 Parabéns! Meu bom!"
        mensagem.color = ft.Colors.GREEN

        page.update()

    # Criando nosso botão
    meu_botao = ft.ElevatedButton(
        text="Clique em mim!",  # Texto do botão
        on_click=botao_clicado,  # Função que será executada ao clicar
        width=200,
        height=50,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE
    )

    # Adicionando os elementos à página
    page.add(mensagem)
    page.add(meu_botao)

ft.app(target=main)
