
## NÄDAL 1 — SQL Põhitõed


## Nädala eesmärk

Nädal 1 eesmärk on uurida UrbanStyle.ltd andmeid SQL-i abil ning saada esmane ülevaade:

- millised tabelid andmebaasis olemas on;
- millised veerud ja andmetüübid tabelites on;
- kui palju kirjeid tabelites on;
- millised väärtused andmetes esinevad;
- kus esineb puuduvaid või ebaloogilisi väärtusi;
- millised leiud võivad olla äriliselt olulised.

Enne analüüsi tegemist on oluline mõista, mida andmed tegelikult sisaldavad ja kas neid saab usaldusväärselt kasutada.

# 1. Ühine Supabase'i keskkond

Week 1 töö jaoks kasutame meeskonna ühist Supabase'i projekti:

**Projekt:** `urbanstyle-marketing-data`

Andmebaasi loomiseks kasutasime UrbanStyle'i ametlikku:

`urbanstyle_schema.sql`

Skeemi põhjal loodi järgmised UrbanStyle'i tabelid:

- `suppliers`
- `products`
- `customers`
- `sales`
- `web_logs`
- `inventory`
- `inventory_movements`
- `promotions`

Andmete importimisel lähtusime tabelite struktuurist.


