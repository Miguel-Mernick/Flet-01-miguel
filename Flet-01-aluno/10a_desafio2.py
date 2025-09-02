import flet as ft

def main(page: ft.Page):
    """
    Desafio 2 - Criar um app que simule uma lista de tarefas.
    """

    # Campo de texto para digitar a tarefa
    campo_tarefa = ft.TextField(label="Digite uma tarefa", width=300)

    # Lista onde as tarefas vão aparecer
    lista_tarefas = ft.Column()

    # Função para adicionar tarefas
    def adicionar_tarefa(e):
        if campo_tarefa.value.strip() != "":
            # Cria um item de tarefa
            tarefa = ft.Row(
                controls=[
                    ft.Checkbox(label=campo_tarefa.value),  # Caixa de seleção
                ]
            )
            lista_tarefas.controls.append(tarefa)
            campo_tarefa.value = ""  # Limpa o campo
            page.update()

    # Botão de adicionar
    botao_add = ft.ElevatedButton("Adicionar", on_click=adicionar_tarefa)

    # Layout
    page.add(
        ft.Text("📝 Lista de Tarefas", size=22, weight=ft.FontWeight.BOLD),
        ft.Row([campo_tarefa, botao_add]),
        lista_tarefas
    )

# Iniciando o app
ft.app(target=main)