if archivo is not None:
    df = pd.read_csv(archivo)
    
    st.subheader("Variables numéricas disponibles")
    vars_numericas = df.select_dtypes(include='number').columns.tolist()

    if len(vars_numericas) < 2:
        st.error("El archivo debe contener al menos dos columnas numéricas")
        st.stop()

    st.write(vars_numericas)

    var_x = st.selectbox("Selecciona la primera variable", vars_numericas)
    var_y = st.selectbox("Selecciona la segunda variable", vars_numericas)

    if var_x != var_y:
        correlacion = df[var_x].corr(df[var_y], method='pearson')

        st.metric(
            label=f"Correlación entre {var_x} y {var_y}",
            value=round(correlacion, 3)
        )

        if abs(correlacion) >= 0.7:
            interpretacion = "Correlación fuerte"
        elif abs(correlacion) >= 0.4:
            interpretacion = "Correlación moderada"
        elif abs(correlacion) >= 0.2:
            interpretacion = "Correlación débil"
        else:
            interpretacion = "Correlación nula o inexistente"

        st.info(f"Interpretación: {interpretacion}")

    else:
        st.error("Seleccione dos variables diferentes")
else:
    st.error("Sube un archivo CSV")
