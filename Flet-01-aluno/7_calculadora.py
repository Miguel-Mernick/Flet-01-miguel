import flet as ft

def main(page: ft.Page):
    """
    Exemplo de calculadora simples (soma de dois números).
    """

    # Campos de entrada
    campo1 = ft.TextField(label="Número 1", width=150)
    campo2 = ft.TextField(label="Número 2", width=150)

    # Resultado
    resultado = ft.Text("Resultado = ?", size=20, weight=ft.FontWeight.BOLD)

    # Função do botão
    def somar(e):
        try:
            n1 = float(campo1.value)
            n2 = float(campo2.value)
            resultado.value = f"Resultado = {n1 + n2}"
            resultado.color = ft.Colors.GREEN
        except:
            resultado.value = "⚠️ Digite números válidos!"
            resultado.color = ft.Colors.RED
        page.update()

    # Botão de soma
    botao_somar = ft.ElevatedButton("Somar", on_click=somar)

    # Layout
    page.add(
        ft.Text("🧮 Calculadora", size=22, weight=ft.FontWeight.BOLD),
        ft.Row([campo1, campo2], alignment=ft.MainAxisAlignment.CENTER),
        botao_somar,
        resultado
    )

# Iniciando o app
ft.app(target=main)