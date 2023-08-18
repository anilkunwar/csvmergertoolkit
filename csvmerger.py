import streamlit as st
import pandas as pd
import os
import zipfile
import io

# Define the Streamlit app
def main():
    st.title("CSV Merger App")

    # Upload the zip folder
    uploaded_file = st.file_uploader("Upload a zip folder containing data2_*.csv files", type="zip")

    if uploaded_file is not None:
        # Extract the uploaded zip file to a temporary directory
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)

        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Search for subdirectories that contain CSV files
        csv_subdirs = [f for f in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, f))]

        if len(csv_subdirs) > 0:
            dfs = []
            for subdir in csv_subdirs:
                #Uncomment the following if the file starts with letters data2_ before the time integer
                #csv_files = [f for f in os.listdir(os.path.join(temp_dir, subdir)) if f.startswith("data2_") and f.endswith(".csv")]
                csv_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))  # Sort files based on time
                for csv_file in csv_files:
                    df = pd.read_csv(os.path.join(temp_dir, subdir, csv_file), header=None, skiprows=1)
                    
                    # Extract the time from the filename
                    time = int(csv_file.split("_")[1].split(".")[0])
                    df["Time"] = time  # Add a "Time" column with the extracted time
                    
                    dfs.append(df)

            if len(dfs) > 0:
                # Concatenate all dataframes
                merged_df = pd.concat(dfs, ignore_index=True)

                # Set the column names
                column_names = [
                    "flow_solution_loads_1", "flow_solution_loads_2", "flow_solution_loads_3", "flow_solution_loads_4",
                    "pressure", "temperature", "temperature_loads", "velocity:0", "velocity:1", "velocity:2",
                    "GeometryIds", "vtkValidPointMask", "Points:0", "Points:1", "Points:2", "Time"
                ]
                merged_df.columns = column_names

                # Create a download link for the merged CSV file
                st.download_button("Download Merged CSV", data=merged_df.to_csv(index=False).encode(), file_name="merged_data.csv", mime="text/csv")
            else:
                st.warning("No valid CSV files found in the uploaded folder.")
        else:
            st.warning("No subdirectories with CSV files found in the uploaded folder.")

# Run the Streamlit app
if __name__ == "__main__":
    main()

