import pandas as pd
import streamlit as st

st.title("CSV analyzer")
st.write("Upload a CSV, filter its rows, and download the results.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        if data.empty:
            st.warning("The CSV has headers but no data rows.")
        else:
            st.subheader("Preview")
            st.dataframe(data.head(), hide_index=True)

            numeric_columns = data.select_dtypes(include="number").columns.tolist()

            if not numeric_columns:
                st.info("No numeric columns found. Check that numeric values are formatted as numbers.")
            else:
                column = st.selectbox(
                    "Choose a numeric column to filter",
                    numeric_columns,
                )

                values = data[column].dropna()

                if values.empty:
                    st.warning(f"The column '{column}' has no numeric values.")
                else:
                    minimum_value = float(values.min())

                    minimum = st.number_input(
                        f"Minimum {column}",
                        value=minimum_value,
                    )

                    filtered_data = data[data[column] >= minimum]

                    st.subheader("Filtered results")
                    st.write(f"Rows shown: {len(filtered_data)}")
                    st.dataframe(filtered_data, hide_index=True)

                    if not filtered_data.empty:
                        st.subheader(f"{column} chart")
                        st.bar_chart(filtered_data, y=column)

                    csv_bytes = filtered_data.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Download filtered CSV",
                        data=csv_bytes,
                        file_name="filtered_data.csv",
                        mime="text/csv",
                    )

    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty.")
    except pd.errors.ParserError:
        st.error("Could not read this file as a valid CSV.")
    except UnicodeDecodeError:
        st.error("Could not decode the file. Save it as UTF-8 CSV and try again.")

