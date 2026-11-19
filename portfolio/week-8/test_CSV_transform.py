# Roll B – Data Processing: funktsioonide testimine
# Kontrollime, kas transform.py funktsioonid töötavad roll A
# salvestatud müügi- ja kliendiandmetega (sales.csv ja customers.csv).
# Testime andmete puhastamist, nädalapõhiseid kokkuvõtteid,
# KPI-de arvutamist ning müügi- ja kliendiandmete ühendamist.
# Eesmärk on veenduda, et rollide A ja B koodid töötavad koos.

import pandas as pd

from transform import (
    clean_data,
    calculate_weekly_aggregates,
    calculate_kpis,
    merge_datasets
)

# Loeme roll A salvestatud andmed
df_sales = pd.read_csv("portfolio/week-8/sales.csv")
df_customers = pd.read_csv("portfolio/week-8/customers.csv")

# Käivitame roll B funktsioonid
df_clean = clean_data(df_sales)
df_weekly = calculate_weekly_aggregates(df_clean)
kpis = calculate_kpis(df_clean)
df_merged = merge_datasets(df_clean, df_customers)

# Kuvame tulemused
print("Puhastatud müügiridu:", len(df_clean))
print("Nädalate arv:", len(df_weekly))
print("KPI-d:", kpis)
print("Ühendatud ridu:", len(df_merged))
