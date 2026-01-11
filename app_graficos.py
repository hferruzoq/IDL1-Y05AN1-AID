import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# CONFIGURACIÓN INICIAL
# ------------------------------
st.set_page_config(
    page_title="Visualización de Ventas",
    layout="wide"
)

st.title("📊 Visualización de Ventas - Tiendas de Conveniencia")

# ------------------------------
# CARGA DE ARCHIVO
# ------------------------------
archivo = st.file_uploader(
    "Sube el archivo CSV",
    type=["csv"]
)

# ------------------------------
# PROCESAMIENTO DEL ARCHIVO
# ------------------------------
if archivo is not None:
    try:
        df = pd.read_csv(archivo)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

    st.subheader("📄 Vista previa de los datos")
    st.dataframe(df.head())

    # ------------------------------
    # VALIDACIÓN DE COLUMNAS PARA VENTAS
    # ------------------------------
    columnas_necesarias = {'producto', 'turno', 'tienda', 'venta_total'}

    if columnas_necesarias.issubset(df.columns):
        st.subheader("📈 Análisis de Ventas")

        # Ventas por producto
        st.markdown("### Ventas totales por producto")
        ventas_producto = df.groupby('producto')['venta_total'].sum()

        fig1 = plt.figure()
        ventas_producto.plot(kind='bar')
        plt.xticks(rotation=45)
        plt.ylabel("Venta total")
        st.pyplot(fig1)

        # Ventas por turno
        st.markdown("### Ventas totales por turno")
        ventas_turno = df.groupby('turno')['venta_total'].sum()

        fig2 = plt.figure()
        ventas_turno.plot(kind='bar')
        plt.ylabel("Venta total")
        st.pyplot(fig2)

        # Ventas por tienda
        st.markdown("### Ventas totales por tienda")
        ventas_tienda = df.groupby('tienda')['venta_total'].sum()

        fig3 = plt.figure()
        ventas_tienda.plot(kind='bar')
        plt.ylabel("Venta total")
        st.pyplot(fig3)

    else:
        st.warning(
            "Para el análisis de ventas, el CSV debe contener las columnas: "
            f"{', '.join(columnas_necesarias)}"
        )

    # ------------------------------
    # CORRELACIÓN DE PEARSON
    # ------------------------------
    st.divider()
    st.subheader("🔗 Correlación de Pearson")

    vars_numericas = df.select_dtypes(include='number').columns.tolist()

    if len(vars_numericas) < 2:
        st.error("El archivo debe contener al menos dos columnas numéricas.")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        var_x = st.selectbox(
            "Selecciona la primera variable",
            vars_numericas
        )

    with col2:
        var_y = st.selectbox(
            "Selecciona la segunda variable",
            vars_numericas
        )

    if var_x != var_y:
        correlacion = df[var_x].corr(df[var_y], method='pearson')

        st.metric(
            label=f"Correlación entre {var_x} y {var_y}",
            value=round(correlacion, 3)
        )

        # Interpretación automática
        if abs(correlacion) >= 0.7:
            interpretacion = "Correlación fuerte"
            st.warning(interpretacion)
        elif abs(correlacion) >= 0.4:
            interpretacion = "Correlación moderada"
            st.info(interpretacion)
        elif abs(correlacion) >= 0.2:
            interpretacion = "Correlación débil"
            st.success(interpretacion)
        else:
            interpretacion = "Correlación nula o inexistente"
            st.write(interpretacion)

    else:
        st.error("Selecciona dos variables diferentes.")

# ------------------------------
# MENSAJE INICIAL
# ------------------------------
else:
    st.info("⬆️ Sube un archivo CSV para comenzar el análisis")
