import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

read_columns = ["year", "month", "day", "Precip", "TMAX", "TMIN"]
write_columns = ["year", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "annual"]

def read_file(names:list):
    """
    Receives a list of names of csv files, read them, and returns 
    a dictionary with the loaded files as pandas DataFrames 
    """
    csv_files = {}
    for name in names:
        csv_file = os.path.join("..", "dados", f"{name}.csv")
        csv_files[name] = pd.read_csv(csv_file, names=read_columns, header=None)
    return csv_files

def calculate_indices(df:pd.DataFrame):
    """
    Calculates climate indices for each month and the annual period.
    Returns a dictionary with the indices
    """
    indices = {}
    
    # Making groups for easier calculation per months and year
    monthly_groups = df.groupby(["year", "month"])
    annual_groups = df.groupby("year")

    for (year, month), group in monthly_groups:
        TXx = group["TMAX"].max()
        TX10P = (group["TMAX"] < np.percentile(group["TMAX"], 10)).mean() * 100
        TX90P = (group["TMAX"] > np.percentile(group["TMAX"], 90)).mean() * 100
        TNn = group["TMIN"].min()
        TN10P = (group["TMIN"] < np.percentile(group["TMIN"], 10)).mean() * 100
        TN90P = (group["TMIN"] > np.percentile(group["TMIN"], 90)).mean() * 100

        if year not in indices:
            indices[year] = {}

        indices[year][month] = {
            "TXx": TXx,
            "TX10P": TX10P,
            "TX90P": TX90P,
            "TNn": TNn,
            "TN10P": TN10P,
            "TN90P": TN90P
        }

    for year, group in annual_groups:
        TXx = group["TMAX"].max()
        TX10P = (group["TMAX"] < np.percentile(group["TMAX"], 10)).mean()*100
        TX90P = (group["TMAX"] > np.percentile(group["TMAX"], 90)).mean()*100
        TNn = group["TMIN"].min()
        TN10P = (group["TMIN"] < np.percentile(group["TMIN"], 10)).mean()*100
        TN90P = (group["TMIN"] > np.percentile(group["TMIN"], 90)).mean()*100

        if year not in indices:
            indices[year] = {}

        indices[year]["annual"] = {
            "TXx": TXx,
            "TX10P": TX10P,
            "TX90P": TX90P,
            "TNn": TNn,
            "TN10P": TN10P,
            "TN90P": TN90P
        }

    return indices

def write_indices(indices:dict, name:str):
    """
    For each index is created a csv file, wich contains the year, 
    the value of the index for each month, and the annual value"
    """
    # Creates a 'indices' folder if it doesn't exist
    output_dir = "indices"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save each index to a separete CSV file
    for index_name in ["TXx", "TX10P", "TX90P", "TNn", "TN10P", "TN90P"]:
        data = []
        for year, months in indices.items():
            row = ([year] + [months.get(m, {}).get(index_name, np.nan) for m in range(1, 13)] + 
                    [months.get("annual", {}).get(index_name, np.nan)])
            data.append(row)

        df_output = pd.DataFrame(data, columns=write_columns)
        df_output = df_output.round(2)
        #Save the file in the 'indices' directory
        df_output.to_csv(os.path.join(output_dir, f"{name}_{index_name}.csv"), index=False, sep=",")

def plot_indices(df:pd.DataFrame, name:str, index:str):
    """
    Generates charts about the indices and save these charts in a PDF
    """
    output_dir = "indices"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_path = os.path.join(output_dir, f"{name}_decadal_{index}.pdf")

    with PdfPages(pdf_path) as pdf:
        start_year = df["year"].min()
        end_year = df["year"].max() + 1

        decades = list(range(start_year, end_year + 1, 10))

        plt.figure(figsize=(10, len(decades) * 2)) 

        for i, start in enumerate(decades[:-1]):
            end = start + 9
            subset = df[(df["year"] >= start) & (df["year"] <= end)]

            if subset.empty:
                continue 

            plt.subplot(len(decades), 1, i + 1)
            plt.plot(subset["year"] + (subset["month"] - 1) / 12, subset[f"{index}"], color="blue", linewidth=0.8)

            # Yellow lines to mark years
            for year in range(start, end + 1):
                plt.axvline(year, color="yellow", linestyle="-", linewidth=1)

            plt.xlim(start, end + 1)
            plt.ylim(df[f"{index}"].min(), df[f"{index}"].max())

            plt.title(f"Station: {name}, {start} ~ {end}, {index} (°C)", fontsize=10)
            plt.xticks(range(start, end + 2, 1)) 
            plt.yticks([10, 30]) 
            plt.grid(False) 

        plt.tight_layout()
        pdf.savefig()
        plt.close()

def main():
    csv_files = read_file(["SAOSIMAO"])

    for name, df in csv_files.items():
        indices = calculate_indices(df)
        write_indices(indices, name)
        for index in ["TMIN", "TMAX", "Precip"]:
            plot_indices(df, name, index)
    

if __name__ == "__main__":
    main()