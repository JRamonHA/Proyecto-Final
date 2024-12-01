import io
import pandas as pd
import plotly.express as px
from shiny import App, Inputs, reactive, render, ui
from shinywidgets import render_widget, output_widget
import faicons
import funciones as func


f = func.cargar_anio("2010")
esol = pd.read_parquet(f)
nombres = list(esol.columns)
years = func.years


app_ui = ui.page_navbar(
    ui.nav_spacer(),
    ui.nav_panel(
        "Visualizador",
        ui.navset_card_underline(
            ui.nav_panel("Anual", output_widget("plot_anual")),
            ui.nav_panel("Mensual", output_widget("plot_mensual")),
            title="Meteorología",
        ),
    ),
    ui.nav_panel(
        "Datos",
        ui.card(
            ui.card_header(
                ui.span(ui.output_text("file_title"),
                    class_="me-auto"),
                ui.download_link("download_data", "Descargar archivo", icon=faicons.icon_svg("download"),
                    class_="btn btn-primary btn-sm"),
                class_="d-flex justify-content-between align-items-center"
            ),
            ui.output_data_frame("data"),
        ),
    ),
    sidebar=ui.sidebar(
        ui.input_select("year", "Año", choices=list(years), selected="2010"),
        ui.input_select("variable", "Variable", choices=nombres)
    ),
    id="tabs",
    title="Explorador ESOLMET",
    fillable=True,
)


def server(input: Inputs):
    @reactive.calc()
    def cargar_esol() -> pd.DataFrame:
        year_selected = input.year()
        f = func.cargar_anio(year_selected)
        esol = pd.read_parquet(f)
        return esol

    @render_widget
    def plot_anual():
        esol = cargar_esol()
        var = input.variable()

        df = esol.reset_index()
        fig = px.line(
            df,
            x='TIMESTAMP',
            y=var,
            title=f"{var} - {input.year()}",
            labels={'TIMESTAMP': 'Fecha', var: var},
        )

        maximos = esol[var].resample('D').max()  
        maximos_idx = maximos.index  
        maximos_valor = maximos.values  

        fig.add_scatter(
                x=maximos_idx, 
                y=maximos_valor, 
                mode='markers', 
                name="Máximos diarios", 
                marker=dict(color='red', size=6)
        )

        return fig

    @render_widget
    def plot_mensual():
        esol = cargar_esol()
        var = input.variable()

        df = esol.resample('ME').agg({var: ['mean', 'std']}).reset_index()
        df.columns = ['TIMESTAMP', 'mean', 'std']

        fig = px.line(
            df,
            x='TIMESTAMP',
            y='mean',
            title=f"{var} - {input.year()}",
            labels={'TIMESTAMP': 'Fecha', 'mean': f"{var}"}
        )

        if var not in ['Ib', 'Ig']:
            fig.add_scatter(
                x=df['TIMESTAMP'],
                y=df['std'],
                mode='lines',
                name="Desviación estándar",
                line=dict(dash='dot', color='red')
            )
        return fig

    @render.data_frame
    def data():
        df = cargar_esol().reset_index().rename(columns={"TIMESTAMP": "Fecha"})
        return df

    @render.text
    def file_title():
        return f"ESOLMET_{input.year()}.csv"

    @render.download(filename=lambda: f"ESOLMET_{input.year()}.csv")
    def download_data():
        df = cargar_esol().reset_index()
        df = df.rename(columns={"TIMESTAMP": "Fecha"}) 
        with io.StringIO() as buf:
            df.to_csv(buf, index=False)
            yield buf.getvalue().encode()


app = App(app_ui, server)