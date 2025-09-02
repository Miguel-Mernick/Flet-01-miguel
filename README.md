# desafio_imc.py
# Aplicativo Flet: Desafio IMC (BMI) - calcula IMC, mostra categoria, sugestões e salva perfis.
# Requisitos: pip install flet
import flet as ft
from typing import Dict

def main(page: ft.Page):
    page.title = "🏋️‍♀️ Desafio IMC"
    page.vertical_alignment = "start"
    page.padding = 20
    page.scroll = "auto"

    # Estado
    perfis_salvos: list[Dict] = []

    # --- UI elements ---
    txt_nome = ft.TextField(label="Nome", width=300)
    txt_peso = ft.TextField(label="Peso (kg)", width=150, keyboard_type="decimal")
    txt_altura = ft.TextField(label="Altura (cm)", width=150, keyboard_type="decimal",
                              hint_text="ex: 170 para 1.70m")
    resultado_text = ft.Text("", size=16, weight="bold")
    categoria_text = ft.Text("", size=16)
    sugestao_text = ft.Text("", size=14)
    barras = ft.ProgressBar(width=300, visible=False)

    # Área de perfis salvos
    lista_perfis = ft.Column()

    # Helper: categoria e cor
    def analisar_imc(imc: float):
        """Retorna (categoria, cor_hex, recomendação_curta)."""
        if imc < 18.5:
            return "Abaixo do peso", "#2196F3", "Considere ganhar peso com alimentação equilibrada."
        elif imc < 25:
            return "Normal", "#4CAF50", "Excelente! Mantenha hábitos saudáveis."
        elif imc < 30:
            return "Sobrepeso", "#FF9800", "Recomenda-se atividade física regular e revisão alimentar."
        elif imc < 35:
            return "Obesidade I", "#FF5722", "Procure orientação profissional (nutrição/atividade)."
        elif imc < 40:
            return "Obesidade II", "#E64A19", "Atenção: acompanhamento médico recomendado."
        else:
            return "Obesidade III", "#B71C1C", "Risco elevado — procure atendimento médico."

    # Valida entradas e converte
    def ler_entradas():
        nome = txt_nome.value.strip()
        try:
            peso = float(txt_peso.value.replace(",", "."))
        except Exception:
            peso = None
        try:
            altura_cm = float(txt_altura.value.replace(",", "."))
        except Exception:
            altura_cm = None
        return nome, peso, altura_cm

    # Função principal de cálculo
    def calcular_imc(e=None):
        nome, peso, altura_cm = ler_entradas()

        # validações
        if not nome:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Informe o nome."), open=True)
            page.update()
            return
        if peso is None or peso <= 0:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Peso inválido."), open=True)
            page.update()
            return
        if altura_cm is None or altura_cm <= 0:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Altura inválida."), open=True)
            page.update()
            return

        altura_m = altura_cm / 100.0
        imc = peso / (altura_m * altura_m)
        imc_2 = round(imc, 2)

        # categoria e cor
        categoria, cor, recomendacao = analisar_imc(imc)

        # peso ideal (intervalo BMI 18.5 - 24.9)
        peso_min = 18.5 * (altura_m * altura_m)
        peso_max = 24.9 * (altura_m * altura_m)

        resultado_text.value = f"IMC: {imc_2:.2f}"
        categoria_text.value = f"{categoria}"
        categoria_text.color = cor
        sugestao_text.value = (
            f"{recomendacao}\nPeso ideal aproximado: {peso_min:.1f} kg — {peso_max:.1f} kg."
        )

        barras.value = min(1.0, imc / 40.0)  # mapeia para progressbar visual (0..1)
        barras.visible = True

        page.snack_bar = ft.SnackBar(ft.Text(f"✔️ IMC calculado: {imc_2:.2f}"), open=True)
        page.update()

    def limpar(e=None):
        txt_nome.value = ""
        txt_peso.value = ""
        txt_altura.value = ""
        resultado_text.value = ""
        categoria_text.value = ""
        sugestao_text.value = ""
        barras.visible = False
        page.update()

    def salvar_perfil(e=None):
        nome, peso, altura_cm = ler_entradas()
        if not nome or peso is None or altura_cm is None:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Preencha nome, peso e altura antes de salvar."), open=True)
            page.update()
            return
        altura_m = altura_cm / 100.0
        imc = peso / (altura_m * altura_m)
        perfil = {
            "nome": nome,
            "peso": peso,
            "altura_cm": altura_cm,
            "imc": round(imc, 2)
        }
        perfis_salvos.append(perfil)
        _atualizar_lista_perfis()
        page.snack_bar = ft.SnackBar(ft.Text(f"💾 Perfil '{nome}' salvo (IMC {perfil['imc']})."), open=True)
        page.update()

    def _atualizar_lista_perfis():
        lista_perfis.controls.clear()
        if not perfis_salvos:
            lista_perfis.controls.append(ft.Text("Nenhum perfil salvo.", italic=True))
        else:
            for i, p in enumerate(perfis_salvos[::-1], start=1):
                linha = ft.Row([
                    ft.Text(f"{p['nome']} — {p['peso']}kg — {p['altura_cm']}cm — IMC {p['imc']}", expand=True),
                    ft.IconButton(ft.icons.DELETE, tooltip="Remover", on_click=lambda e, idx=len(perfis_salvos)-i: _remover_perfil(idx))
                ], alignment="spaceBetween")
                lista_perfis.controls.append(linha)
        page.update()

    def _remover_perfil(idx):
        # idx: índice real na lista perfis_salvos
        try:
            removed = perfis_salvos.pop(idx)
            page.snack_bar = ft.SnackBar(ft.Text(f"🗑️ Perfil '{removed['nome']}' removido."), open=True)
            _atualizar_lista_perfis()
        except Exception:
            pass

    # Atualiza em tempo real quando alteram os campos (opcional)
    def on_input_change(e):
        # tenta calcular só se as três entradas estiverem preenchidas corretamente
        nome, peso, altura_cm = ler_entradas()
        if nome and peso and altura_cm:
            calcular_imc()
        else:
            # mantém respostas anteriores — se quiser limpar automaticamente, descomente:
            # resultado_text.value = ""; categoria_text.value = ""; sugestao_text.value = ""; barras.visible = False
            page.update()

    # conecta eventos de on_change
    txt_nome.on_change = on_input_change
    txt_peso.on_change = on_input_change
    txt_altura.on_change = on_input_change

    # --- Layout ---
    entrada_box = ft.Card(
        content=ft.Container(
            ft.Column([
                ft.Text("Calculadora IMC", size=24, weight="bold"),
                ft.Row([txt_nome], alignment="start"),
                ft.Row([txt_peso, txt_altura], spacing=20),
                ft.Row([
                    ft.ElevatedButton("Calcular", on_click=calcular_imc),
                    ft.ElevatedButton("Limpar", on_click=limpar, bgcolor="#9E9E9E"),
                    ft.ElevatedButton("Salvar Perfil", on_click=salvar_perfil, bgcolor="#03A9F4"),
                ], spacing=10),
            ], tight=True),
            padding=16
        ),
        elevation=4
    )

    resultado_box = ft.Card(
        content=ft.Container(
            ft.Column([
                ft.Text("Resultado", size=18, weight="bold"),
                resultado_text,
                categoria_text,
                barras,
                ft.Divider(),
                sugestao_text
            ]),
            padding=12
        ),
        elevation=2
    )

    perfis_box = ft.Card(
        content=ft.Container(
            ft.Column([
                ft.Text("Perfis salvos", size=18, weight="bold"),
                lista_perfis
            ]),
            padding=12
        ),
        elevation=1
    )

    layout = ft.Row([
        ft.Column([entrada_box, ft.Container(height=10), resultado_box], spacing=10),
        ft.VerticalDivider(),
        ft.Column([perfis_box], width=320)
    ], alignment="start")

    page.add(layout)

    # inicializa lista
    _atualizar_lista_perfis()

if __name__ == "__main__":
    ft.app(target=main)
