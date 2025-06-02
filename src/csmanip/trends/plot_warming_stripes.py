import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


def plot_annual_data(csv_path, index, file_name, title_img, caption_img):
    data_base = pd.read_csv(csv_path)
    data_base.columns = ["year", "prec", "tmax", "tmin", "tmean"]
    data_base[index] = data_base[index].replace(-99.9, None)
    data_base["date"] = pd.to_datetime(data_base["year"].astype(str) + "-01-01")

    sns.set_style("white")
    plt.figure(figsize=(12, 2))
    cmap = sns.color_palette("RdBu_r", as_cmap=True)

    scatter = plt.scatter(
        data_base["date"],
        [1] * len(data_base),
        c=data_base[index],
        cmap=cmap,
        marker="s",
        s=200
    )

    plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    plt.yticks([])
    plt.title(title_img, fontsize=14, fontweight="bold")
    plt.xlabel("")
    plt.grid(False)
    plt.colorbar(scatter, label=f"Temperatura ({index})")
    plt.figtext(0.9, 0.02, caption_img, fontsize=10, ha="right")
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    plt.show()


def plot_quarterly_data(csv_path, index, file_name, title_img, caption_img):
    data_base = pd.read_csv(csv_path)
    data_base.columns = ["year", "quarter", "prec", "tmax", "tmin", "tmean"]
    data_base[index] = data_base[index].replace(-99.9, None)

    sns.set_style(style="white")
    plt.figure(figsize=(14, 4))
    cmap = sns.color_palette("RdBu_r", as_cmap=True)

    scatter = plt.scatter(
        data_base["year"],
        data_base["quarter"],
        c=data_base[index],
        cmap=cmap,
        marker="s",
        s=200
    )

    plt.xticks(rotation=90)
    plt.yticks([1, 2, 3, 4], labels=["T1", "T2", "T3", "T4"])
    plt.title(title_img, fontsize=14, fontweight="bold")
    plt.xlabel("Ano")
    plt.ylabel("Trimestre")
    plt.grid(False)
    plt.colorbar(scatter, label=f"Temperatura ({index})")
    plt.figtext(0.95, 0.02, caption_img, fontsize=10, ha="right")

    plt.tight_layout()
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    plt.show()


def plot_monthly_data(csv_path, index, file_name, title_img, caption_img):
    data_base = pd.read_csv(csv_path)
    data_base.columns = ["year", "month", "prec", "tmax", "tmin", "tmean"]
    data_base[index] = data_base[index].replace(-99.9, None)

    sns.set_style(style="white")
    plt.figure(figsize=(14, 5))
    cmap = sns.color_palette("RdBu_r", as_cmap=True)

    scatter = plt.scatter(
        data_base["year"],
        data_base["month"],
        c=data_base[index],
        cmap=cmap,
        marker="s",
        s=150
    )

    plt.gca().invert_yaxis()
    plt.xticks(rotation=90)
    plt.yticks(range(1, 13), labels=[
        "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
        "Jul", "Ago", "Set", "Out", "Nov", "Dez"
    ])
    plt.title(title_img, fontsize=14, fontweight="bold")
    plt.xlabel("Ano")
    plt.ylabel("Mês")
    plt.grid(False)
    plt.colorbar(scatter, label=f"Temperatura ({index})")
    plt.figtext(0.95, 0.02, caption_img, fontsize=10, ha="right")

    plt.tight_layout()
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    plt.show()
