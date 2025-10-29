import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


def plot_annual_data(csv_path, index, file_name, title_img, caption_img, embed_mode=False):
    data_base = pd.read_csv(csv_path)
    data_base.columns = ["year", "prec", "tmax", "tmin", "tmean"]
    data_base[index] = data_base[index].replace(-99.9, None)
    data_base["date"] = pd.to_datetime(data_base["year"].astype(str) + "-01-01")

    sns.set_style("white")
    fig, ax = plt.subplots(figsize=(12, 2))
    cmap = sns.color_palette("RdBu_r", as_cmap=True)

    scatter = ax.scatter(
        data_base["date"],
        [1] * len(data_base),
        c=data_base[index],
        cmap=cmap,
        marker="s",
        s=200
    )

    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_yticks([])
    ax.set_title(title_img, fontsize=14, fontweight="bold")
    ax.set_xlabel("")
    ax.grid(False)
    
    fig.colorbar(scatter, ax=ax, label=f"Temperatura ({index})")
    fig.text(0.9, 0.02, caption_img, fontsize=10, ha="right")

    if embed_mode:
        return fig
    else:
        fig.savefig(file_name, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)
        return None


def plot_quarterly_data(csv_path, index, file_name, title_img, caption_img, embed_mode=False):
    data_base = pd.read_csv(csv_path)
    data_base.columns = ["year", "quarter", "prec", "tmax", "tmin", "tmean"]
    data_base[index] = data_base[index].replace(-99.9, None)

    sns.set_style(style="white")
    fig, ax = plt.subplots(figsize=(14, 4))
    cmap = sns.color_palette("RdBu_r", as_cmap=True)

    scatter = ax.scatter( 
        data_base["year"],
        data_base["quarter"],
        c=data_base[index],
        cmap=cmap,
        marker="s",
        s=200
    )

    ax.tick_params(axis='x', rotation=90)
    ax.set_yticks([1, 2, 3, 4], labels=["T1", "T2", "T3", "T4"])
    ax.set_title(title_img, fontsize=14, fontweight="bold")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Trimestre")
    ax.grid(False)
    fig.colorbar(scatter, ax=ax, label=f"Temperatura ({index})")
    fig.text(0.95, 0.02, caption_img, fontsize=10, ha="right")

    fig.tight_layout()

    if embed_mode:
        return fig
    else:
        fig.savefig(file_name, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)
        return None


def plot_monthly_data(csv_path, index, file_name, title_img, caption_img, embed_mode=False):
    data_base = pd.read_csv(csv_path)
    data_base.columns = ["year", "month", "prec", "tmax", "tmin", "tmean"]
    data_base[index] = data_base[index].replace(-99.9, None)

    sns.set_style(style="white")
    fig, ax = plt.subplots(figsize=(14, 5))
    cmap = sns.color_palette("RdBu_r", as_cmap=True)

    scatter = ax.scatter(
        data_base["year"],
        data_base["month"],
        c=data_base[index],
        cmap=cmap,
        marker="s",
        s=150
    )

    ax.invert_yaxis() 
    ax.tick_params(axis='x', rotation=90)
    ax.set_yticks(range(1, 13), labels=[
        "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
        "Jul", "Ago", "Set", "Out", "Nov", "Dez"
    ])
    ax.set_title(title_img, fontsize=14, fontweight="bold")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Mês")
    ax.grid(False) 
    fig.colorbar(scatter, ax=ax, label=f"Temperatura ({index})") 
    fig.text(0.95, 0.02, caption_img, fontsize=10, ha="right") 

    fig.tight_layout()

    if embed_mode:
        return fig
    else:
        fig.savefig(file_name, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)
        return None
