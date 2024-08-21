# documentation: https://docs.streamlit.io/get-started/fundamentals/main-concepts
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈Data Exploration Dashboard")

uploaded_file = st.file_uploader("📌Upload a CSV file to start", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # Standardize column names
    
    st.subheader("Data Preview")
    st.write(df.head())
    
    st.subheader("Data Summary")

    # Create two columns for data types and missing values
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Data Types:**")
        st.write(df.dtypes)

    with col2:
        st.write("**Missing Values:**")
        missing_values = df.isnull().sum()
        st.write(missing_values)

    # Show basic statistical summary
    st.write("**Statistical Summary:**")
    st.write(df.describe())
    
    st.subheader("Filter Data (Optional)")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", ["No Filter"] + columns)
    
    if selected_column != "No Filter":
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox(f"Select value for {selected_column}", unique_values)
        filtered_df = df[df[selected_column] == selected_value]
        st.subheader(f"Filtered Data based on '{selected_column}' = '{selected_value}'")
        st.write(filtered_df)
    else:
        filtered_df = df
    
    st.subheader("Plot Data")
    # Initialize with None to ensure nothing is selected by default
    x_column = st.selectbox("Select x-axis column", ["None"] + columns)
    y_column = st.selectbox("Select y-axis column", ["None"] + columns)
    
    if x_column != "None" and y_column != "None":
        x_dtype = filtered_df[x_column].dtype
        y_dtype = filtered_df[y_column].dtype

        # Automatically determine the plot type
        if pd.api.types.is_numeric_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
            plot_type = "Scatter Plot"
        elif pd.api.types.is_categorical_dtype(x_dtype) or pd.api.types.is_object_dtype(x_dtype):
            plot_type = "Bar Chart"
        elif pd.api.types.is_datetime64_any_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
            plot_type = "Line Chart"
        else:
            plot_type = "Not Supported"
        
        st.subheader(f"Automatically Selected Plot: {plot_type}")
        
        if plot_type == "Scatter Plot":
            fig = px.scatter(filtered_df, x=x_column, y=y_column)
            st.plotly_chart(fig)
        elif plot_type == "Line Chart":
            fig = px.line(filtered_df, x=x_column, y=y_column)
            st.plotly_chart(fig)
        elif plot_type == "Bar Chart":
            fig = px.bar(filtered_df, x=x_column, y=y_column)
            st.plotly_chart(fig)
        else:
            st.write("No suitable plot type found for the selected columns🥲")
    else:
        st.write("ℹ️Please select both x-axis and y-axis columns to plot.")
else:
    st.write("Waiting for file upload...")
