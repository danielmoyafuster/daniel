import streamlit as st
import pandas as pd

# Ruta del archivo Excel con las canciones y enlaces
file_path = "FONOTECA_RADIO_UMH_SPOTIFY_SAMPLES.xlsx"

# Cargar los datos desde el archivo Excel
@st.cache_data
def cargar_datos():
    return pd.read_excel(file_path)

data = cargar_datos()

# Configurar la aplicación
logo_url = "https://radio.umh.es/files/2023/07/FOTO-PERFIL-RADIO.png"
st.image(logo_url, width=200)
st.title("📻 Radio UMH - 🎵 Fonoteca Interactiva")
st.markdown("Busca canciones, explora álbumes y abre enlaces completos a las canciones disponibles.")

# Barra de búsqueda
query = st.text_input("🔍 Busca por título, autor o nombre del CD:")

# Filtrar las canciones según la búsqueda
filtered_data = data
if query:
    filtered_data = filtered_data[
        data["Título"].str.contains(query, case=False, na=False) |
        data["AUTOR"].str.contains(query, case=False, na=False) |
        data["NOMBRE CD"].str.contains(query, case=False, na=False)
    ]

# Agregar un filtro por género (si está disponible en los datos)
if "Género" in data.columns:
    genero = st.selectbox("Filtrar por género:", ["Todos"] + sorted(data["Género"].dropna().unique().tolist()))
    if genero != "Todos":
        filtered_data = filtered_data[filtered_data["Género"] == genero]

# Mostrar los resultados en una tabla con estilos
if not filtered_data.empty:
    # Agregar enlaces clicables en la columna de URLs
    def convertir_url_enlace(url):
        return f'<a href="{url}" target="_blank">Abrir en Spotify</a>' if pd.notna(url) and url != "No encontrado" else "🔗 No disponible"

    filtered_data.loc[:, "Enlace Spotify"] = filtered_data["Spotify URL"].apply(convertir_url_enlace)
    st.write(f"🎧 Resultados encontrados: {len(filtered_data)}")

    # Aplicar estilos con pandas Styler
    def aplicar_estilo(df):
        return df.style.set_properties(
            **{
                'text-align': 'left',  # Alinear texto a la izquierda
            }
        ).set_table_styles(
            [
                {'selector': 'th', 'props': [('text-align', 'left')]}
            ]
        )

    # Eliminar el índice manualmente antes de aplicar el estilo
    filtered_data.reset_index(drop=True, inplace=True)
    styled_table = aplicar_estilo(
        filtered_data[["Nº", "AUTOR", "NOMBRE CD", "Título", "Enlace Spotify"]]
    )
    st.write(styled_table.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("❌ No se encontraron resultados.")

# Botón para descargar resultados filtrados
if not filtered_data.empty:
    st.download_button(
        label="📥 Descargar resultados",
        data=filtered_data.to_csv(index=False),
        file_name="resultados_fonoteca.csv",
        mime="text/csv"
    )