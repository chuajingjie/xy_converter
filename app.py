import streamlit as st
import pandas as pd
from pyproj import Transformer
from io import BytesIO

# Set page title
st.title("SVY21 to Latitude/Longitude Converter")

# Upload file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Define transformer
transformer = Transformer.from_crs("EPSG:3414", "EPSG:4326", always_xy=True)

# Define conversion function
def convert_coords(row):
    x, y = row["Traffic_Light.Junction_X"], row["Traffic_Light.Junction_Y"]

    if x == 0 or y == 0:
        return pd.Series([0, 0], index=["lat", "lon"])

    lon, lat = transformer.transform(x, y)
    return pd.Series([lat, lon], index=["lat", "lon"])

# If a file is uploaded
if uploaded_file is not None:
    # Read the file
    df = pd.read_csv(uploaded_file)

    # Apply coordinate conversion
    df[["lat", "lon"]] = df.apply(convert_coords, axis=1)

    # Select the columns you want
    output_df = df[["Site_ID", "lat", "lon"]]

    # Show the result
    st.subheader("Converted Data")
    st.dataframe(output_df)

    # Create a download button
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(output_df)

    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='converted_coordinates.csv',
        mime='text/csv',
    )
