# Roll C: Visualization + Saving
print("Python töötab!")
# Impordime Pandase teegi andmete töötlemiseks ja analüüsimiseks
import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Loome Supabase ühenduse
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Toome müügiandmed Supabase'ist
response = supabase.table("sales").select("*").execute()

# Muudame andmed Pandase DataFrame'iks
df = pd.DataFrame(response.data)



# Defineerime funktsiooni müügiandmete puhastamiseks
def clean_data(df):
    # Proovime andmeid puhastada
    try:
        # Loome andmetest koopia, et algsed andmed ei muutuks
        df_clean = df.copy()

        # Eemaldame duplikaadid
        df_clean = df_clean.drop_duplicates()

        # Teisendame kuupäeva õigesse formaati
        df_clean['sale_date'] = pd.to_datetime(
            df_clean['sale_date'], errors='coerce'
        )

        # Eemaldame read, kus puudub kuupäev või hind.
        # Puuduva customer_id-ga müügiread jätame alles, sest need võivad siiski olla kehtivad müügitehingud.
        df_clean = df_clean.dropna(
            subset=['sale_date', 'total_price']
        )

        # Tagastame puhastatud DataFrame'i
        return df_clean

    # Püüame kinni tekkinud vead ja kuvame veateate
    except Exception as e:
        print(f"Viga andmete puhastamisel: {e}")
        raise


# Defineerime funktsiooni nädalapõhise müügikokkuvõtte arvutamiseks
def calculate_weekly_aggregates(df):
    # Proovime arvutada nädalapõhise kokkuvõtte
    try:
        # Grupeerime andmed nädalate kaupa ning arvutame tulu, tellimuste arvu ja keskmise ostuväärtuse
        weekly = df.resample('W', on='sale_date').agg(
            total_revenue=('total_price', 'sum'),
            order_count=('total_price', 'count'),
            avg_order_value=('total_price', 'mean')
        )

        # Muudame indeksi tavaliseks veeruks ja tagastame nädalapõhise kokkuvõttetabeli
        return weekly.reset_index()
    
    # Püüame kinni tekkinud vead ja kuvame veateate
    except Exception as e:
        print(f"Viga nädalapõhise kokkuvõtte arvutamisel: {e}")
        raise


# Defineerime funktsiooni KPI-de arvutamiseks
def calculate_kpis(df):
    # Proovime arvutada KPI-d
    try:
        # Arvutame KPI-d: kogukäive, unikaalsete klientide arv ja keskmise tellimuse väärtus
        kpis = {
            'total_revenue': round(float(df['total_price'].sum()), 2),
            'unique_customers': int(df['customer_id'].nunique()),
            'avg_order_value': round(float(df['total_price'].mean()), 2)
        }

        # Tagastame KPI-de väärtused
        return kpis

    # Püüame kinni tekkinud vead ja kuvame veateate
    except Exception as e:
        print(f"Viga KPI-de arvutamisel: {e}")
        raise


# Defineerime funktsiooni müügi-ja kliendiandmete ühendamiseks
def merge_datasets(df_sales, df_customers):
    # Proovime ühendada müügi- ja kliendiandmed
    try:   
        # Ühendame müügi- ja kliendiandmed nii, et säiliks kõik müügiread
        df_merged = pd.merge(
            df_sales,
            df_customers,
            on='customer_id',
            how='left'
        )

        # Tagastame ühendatud DataFrame'i 
        return df_merged

    # Püüame kinni tekkinud vead ja kuvame veateate
    except Exception as e:
        print(f"Viga andmete ühendamisel: {e}")
        raise

# Impordime Matplotlibi teegi andmete visualiseerimiseks
import matplotlib.pyplot as plt

# Defineerime funktsiooni nädalapõhise müügigraafiku loomiseks
def create_weekly_chart(df_weekly):
    # Proovime luua nädalapõhise müügigraafiku
    try:
        # Loome graafiku ja määrame selle suuruse
        plt.figure(figsize=(12, 6))

        # Loome joondiagrammi nädalase kogukäibe kuvamiseks
        plt.plot(
            df_weekly['sale_date'],
            df_weekly['total_revenue'],
            marker='o',
            label='Nädala kogukäive'
        )

        # Lisame graafikule pealkirja ja telgede nimetused
        plt.title('Nädalapõhine müügikäive')
        plt.xlabel('Nädal')
        plt.ylabel('Kogukäive (€)')

        # Lisame legendi ja ruudustiku
        plt.legend()
        plt.grid(True)

        # Muudame kuupäevad graafikul paremini loetavaks
        plt.xticks(rotation=45)

        # Kohandame graafiku paigutust
        plt.tight_layout()

        # Kuvame graafiku
        plt.show()

    # Püüame kinni tekkinud vead ja kuvame veateate
    except Exception as e:
        print(f"Viga nädalapõhise graafiku loomisel: {e}")
        raise

    # Puhastame Supabase'ist saadud andmed
df_clean = clean_data(df)

# Kontrollime andmeid
print("Supabase andmed edukalt laaditud!")
print(df.head())

print(df.columns.tolist())
print(df.head())

print("Ridade arv:", len(df_clean))

# 2. Arvutame KPI-d
kpis = calculate_kpis(df_clean)

print("\nMüügi KPI-d:")
for key, value in kpis.items():
    print(f"{key}: {value}")

# 3. Arvutame nädalapõhise kokkuvõtte
df_weekly = calculate_weekly_aggregates(df_clean)

# 4. Kuvame nädalapõhise tabeli
print("\nNädalapõhine müügikokkuvõte:")
print(df_weekly.to_string(index=False))

import plotly.graph_objects as go

# 5. Loome graafiku
create_weekly_chart(df_weekly)

def create_kpi_summary(kpis):
    try:
        # Koostame KPI-de tabeli
        fig = go.Figure(data=[
            go.Table(
                header=dict(
                    values=['KPI', 'Väärtus'],
                    fill_color='lightblue',
                    align='center',
                    font=dict(size=14)
                ),
                cells=dict(
                    values=[
                        ['Kogukäive (€)', 'Unikaalsed kliendid',
                         'Keskmine ostuväärtus (€)'],
                        [
                            kpis['total_revenue'],
                            kpis['unique_customers'],
                            kpis['avg_order_value']
                        ]
                    ],
                    align='center',
                    font=dict(size=13)
                )
            )
        ])

        fig.update_layout(
            title='Müügi peamised KPI-d',
            height=300
        )

        # Kuvame KPI tabeli
        fig.show()

        return fig

    except Exception as e:
        print(f"Viga KPI kokkuvõtte loomisel: {e}")
        raise


# Defineerime funktsiooni tulemuste eksportimiseks
def export_results(df, output_dir):
    try:
        # Loome output kausta, kui seda pole olemas
        os.makedirs(output_dir, exist_ok=True)

        # Loome ajatempliga failinimede jaoks ajatempli
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Salvestame DataFrame CSV-failina
        csv_path = os.path.join(
            output_dir,
            f"sales_results_{timestamp}.csv"
        )

        df.to_csv(
            csv_path,
            index=False,
            encoding='utf-8-sig'
        )

        print(f"CSV fail salvestatud: {csv_path}")

        # Arvutame KPI-d
        kpis = calculate_kpis(df)

        # Loome KPI kokkuvõtte
        kpi_fig = create_kpi_summary(kpis)

        # Salvestame KPI tabeli HTML-failina
        kpi_path = os.path.join(
            output_dir,
            f"kpi_summary_{timestamp}.html"
        )

        kpi_fig.write_html(kpi_path)

        print(f"KPI HTML salvestatud: {kpi_path}")

        # Arvutame nädalapõhised müügiandmed
        df_weekly = calculate_weekly_aggregates(df)

        # Loome nädalapõhise graafiku
        weekly_fig = go.Figure()

        weekly_fig.add_trace(
            go.Scatter(
                x=df_weekly['sale_date'],
                y=df_weekly['total_revenue'],
                mode='lines+markers',
                name='Nädala kogukäive'
            )
        )

        weekly_fig.update_layout(
            title='Nädalapõhine müügikäive',
            xaxis_title='Nädal',
            yaxis_title='Kogukäive (€)',
            template='plotly_white'
        )

        # Salvestame graafiku HTML-failina
        chart_path = os.path.join(
            output_dir,
            f"weekly_sales_chart_{timestamp}.html"
        )

        weekly_fig.write_html(chart_path)

        print(f"Nädalag graafik salvestatud: {chart_path}")

        print("\nKõik tulemused edukalt eksporditud!")

    except Exception as e:
        print(f"Viga tulemuste eksportimisel: {e}")
        raise

# Arvutame KPI-d
kpis = calculate_kpis(df_clean)

# Kuvame KPI kokkuvõtte
create_kpi_summary(kpis)

# Ekspordime kõik tulemused output kausta
export_results(df_clean, "output")

print("\nRoll B andmetöötlus lõpetatud!")