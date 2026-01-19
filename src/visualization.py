import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def plot_global_trends(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="year", y="tb_deaths")
    plt.title("Global TB Deaths Over Time")
    plt.ylabel("Deaths")
    plt.xlabel("Year")
    plt.tight_layout()
    plt.show()

def animated_tb_map(df):
    fig = px.choropleth(
        df,
        locations="country",
        locationmode="country names",
        color="tb_incidence",
        animation_frame="year",
        title="Global TB Incidence Over Time",
        color_continuous_scale="Reds"
    )
    fig.show()
