import mysql.connector
import pandas as pd
import plotly.express as px
import streamlit as st

# Fungsi untuk menghubungkan ke database MySQL dan mengambil data promosi
def fetch_promotion_data():
    conn = mysql.connector.connect(
        host = "kubela.id",
        port = "3306",
        database = "aw",
        username = "davis2024irwan",
        password = "wh451n9m@ch1n3"
    )
    query = """
    SELECT EnglishPromotionType, COUNT(*) as PromotionCount
    FROM dimpromotion
    GROUP BY EnglishPromotionType
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fungsi untuk membuat donut chart menggunakan Plotly
def create_donut_chart(df, color_theme):
    fig = px.pie(
        df,
        names='EnglishPromotionType',
        values='PromotionCount',
        hole=0.4,
        color_discrete_sequence=color_theme
    )
    fig.update_layout(xaxis_tickangle=45)
    st.subheader('Distribusi Jenis Promosi')
    st.markdown('Menampilkan distribusi dari berbagai jenis promosi yang paling umum dan tidak umum digunakan')
    st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk mengambil dan menampilkan scatter plot data harga produk vs subkategori produk
def fetch_and_display_product_data(color_theme):
    conn = mysql.connector.connect(
        host = "kubela.id",
        port = "3306",
        database = "aw",
        username = "davis2024irwan",
        password = "wh451n9m@ch1n3"
    )
    query = """
        SELECT ps.EnglishProductSubcategoryName, p.ListPrice
        FROM dimproductsubcategory ps
        INNER JOIN dimproduct p ON ps.ProductSubcategoryKey = p.ProductSubcategoryKey
    """
    df = pd.read_sql(query, con=conn)
    conn.close()

    fig = px.scatter(
        df,
        x='EnglishProductSubcategoryName',
        y='ListPrice',
        labels={'EnglishProductSubcategoryName': 'Subkategori Produk', 'ListPrice': 'Harga Daftar'},
        color='EnglishProductSubcategoryName',
        color_discrete_sequence=color_theme
    )
    fig.update_layout(xaxis_tickangle=45)
    st.subheader('Harga Produk vs Subkategori Produk')
    st.markdown('Menampilkan hubungan antara harga produk dan subkategori produk')
    st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk mengambil dan menampilkan scatter plot distribusi pendapatan tahunan pelanggan
def fetch_and_display_income_distribution(color_theme):
    conn = mysql.connector.connect(
        host = "kubela.id",
        port = "3306",
        database = "aw",
        username = "davis2024irwan",
        password = "wh451n9m@ch1n3"
    )
    query = "SELECT CustomerKey, YearlyIncome FROM dimcustomer WHERE YearlyIncome IS NOT NULL"
    df = pd.read_sql(query, con=conn)
    conn.close()

    fig = px.scatter(
        df,
        x='CustomerKey',
        y='YearlyIncome',
        labels={'CustomerKey': 'CustomerKey', 'YearlyIncome': 'Pendapatan Tahunan'},
        color='YearlyIncome',
        color_continuous_scale=color_theme
    )
    fig.update_layout(xaxis_tickangle=45)
    st.subheader('Distribusi Pendapatan Tahunan Pelanggan')
    st.markdown('Menampilkan distribusi pendapatan tahunan pelanggan')
    st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk mengambil dan menampilkan perbandingan total penjualan berdasarkan wilayah penjualan
def fetch_and_display_sales_comparison(color_theme, chart_type):
    conn = mysql.connector.connect(
        host = "kubela.id",
        port = "3306",
        database = "aw",
        username = "davis2024irwan",
        password = "wh451n9m@ch1n3"
    )
    
    if chart_type == 'Comparison':
        query = """
        SELECT 
            ds.SalesTerritoryRegion,
            SUM(fs.SalesAmount) as TotalSales
        FROM factinternetsales fs
        JOIN dimsalesterritory ds ON fs.SalesTerritoryKey = ds.SalesTerritoryKey
        GROUP BY ds.SalesTerritoryRegion
        """
        df = pd.read_sql(query, conn)
        conn.close()

        fig = px.bar(
            df,
            x='SalesTerritoryRegion',
            y='TotalSales',
            labels={'SalesTerritoryRegion': 'Sales Territory Region', 'TotalSales': 'Total Sales Amount'},
            color='SalesTerritoryRegion',
            color_discrete_sequence=color_theme
        )
        st.subheader('Total Penjualan Internet berdasarkan Wilayah Penjualan')
        st.markdown('Menampilkan total penjualan internet untuk setiap wilayah')
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == 'Distribution':
        query = "SELECT CustomerKey, YearlyIncome FROM dimcustomer WHERE YearlyIncome IS NOT NULL"
        df = pd.read_sql(query, conn)
        conn.close()

        fig = px.scatter(
            df,
            x='CustomerKey',
            y='YearlyIncome',
            labels={'CustomerKey': 'CustomerKey', 'YearlyIncome': 'Pendapatan Tahunan'},
            color='YearlyIncome',
            color_continuous_scale=color_theme
        )
        st.subheader('Distribusi Pendapatan Tahunan Pelanggan')
        st.markdown('Menampilkan distribusi pendapatan tahunan pelanggan')
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == 'Composition':
        query = """
        SELECT EnglishPromotionType, COUNT(*) as PromotionCount
        FROM dimpromotion
        GROUP BY EnglishPromotionType
        """
        df = pd.read_sql(query, conn)
        conn.close()

        fig = px.pie(
            df,
            names='EnglishPromotionType',
            values='PromotionCount',
            hole=0.4,
            color_discrete_sequence=color_theme
        )
        fig.update_layout(xaxis_tickangle=45)
        st.subheader('Distribusi Jenis Promosi')
        st.markdown('Menampilkan distribusi dari berbagai jenis promosi yang paling umum dan tidak umum digunakan')
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == 'Relationship':
        query = """
            SELECT ps.EnglishProductSubcategoryName, p.ListPrice
            FROM dimproductsubcategory ps
            INNER JOIN dimproduct p ON ps.ProductSubcategoryKey = p.ProductSubcategoryKey
        """
        df = pd.read_sql(query, conn)
        conn.close()

        fig = px.scatter(
            df,
            x='EnglishProductSubcategoryName',
            y='ListPrice',
            labels={'EnglishProductSubcategoryName': 'Subkategori Produk', 'ListPrice': 'Harga Daftar'},
            color='EnglishProductSubcategoryName',
            color_discrete_sequence=color_theme
        )
        fig.update_layout(xaxis_tickangle=45)
        st.subheader('Harga Produk vs Subkategori Produk')
        st.markdown('Menampilkan hubungan antara harga produk dan subkategori produk')
        st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk memuat dan menampilkan data IMDb
def load_and_display_imdb_data(color_theme):
    df = pd.read_csv('imdb_warnerbross.csv')

    # Pilihan visualisasi IMDb
    imdb_chart_type = st.sidebar.selectbox(
        "Pilih Jenis Chart",
        ('Comparison', 'Distribution', 'Composition', 'Relationship')
    )

    if imdb_chart_type == 'Comparison':
        st.title('Perbandingan Anggaran Film')
        st.markdown('Membandingkan anggaran produksi dari beberapa film untuk melihat perbedaan investasi antara film-film tersebut.')
        data_to_visualize_budget = df[['Name', 'Budget']].sort_values(by='Budget', ascending=False).head(10)
        fig_budget = px.bar(data_to_visualize_budget, x='Name', y='Budget', title='Anggaran Produksi Film',
                            labels={'Name': 'Film', 'Budget': 'Anggaran Produksi'},
                            color='Name', color_discrete_sequence=color_theme)
        fig_budget.update_layout(xaxis_title='Film', yaxis_title='Anggaran Produksi')
        st.plotly_chart(fig_budget, use_container_width=True)

    elif imdb_chart_type == 'Distribution':
        st.title('Pengaruh Tahun Rilis dengan Rating Film')
        st.markdown('Visualisasi scatter plot untuk mengeksplorasi pengaruh tahun rilis terhadap rating film.')
        data_to_visualize_rating = df[['Year', 'Rating']]
        fig_rating = px.scatter(data_to_visualize_rating, x='Year', y='Rating', title='Pengaruh Tahun Rilis dengan Rating Film',
                                labels={'Year': 'Tahun Rilis', 'Rating': 'Rating'},
                                color='Year', color_continuous_scale=color_theme)
        fig_rating.update_layout(xaxis_title='Tahun Rilis', yaxis_title='Rating')
        st.plotly_chart(fig_rating, use_container_width=True)

    elif imdb_chart_type == 'Composition':
        st.title('Komposisi Pendapatan Kotor Global Film')
        st.markdown('Visualisasi menggunakan donut chart untuk komposisi pendapatan kotor global film')
        column_to_visualize = 'Gross_World'
        bins = [0, 1000000, 10000000, 100000000, df[column_to_visualize].max()]
        labels = ['Very Low', 'Low', 'Moderate', 'High']
        df['Gross_Category'] = pd.cut(df[column_to_visualize], bins=bins, labels=labels, right=False)
        gross_counts = df['Gross_Category'].value_counts()
        fig_gross = px.pie(gross_counts, values=gross_counts.values, names=gross_counts.index,
                           title=f'Komposisi {column_to_visualize}',
                           hole=0.4, color_discrete_sequence=color_theme)
        fig_gross.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_gross, use_container_width=True)

    elif imdb_chart_type == 'Relationship':
        st.title('Hubungan antara Budget dan Rating Film')
        st.markdown('Visualisasi scatter plot untuk mengeksplorasi hubungan antara anggaran produksi dan rating film')
        data_to_visualize = df[['Budget', 'Rating']]
        fig_budget_rating = px.scatter(data_to_visualize, x='Budget', y='Rating', hover_name=df['Name'],
                                       title='Hubungan antara Budget dan Rating Film',
                                       labels={'Budget': 'Budget (in USD)', 'Rating': 'Rating'},
                                       color='Budget', color_continuous_scale=color_theme)
        fig_budget_rating.update_layout(xaxis_title='Budget (in USD)', yaxis_title='Rating')
        st.plotly_chart(fig_budget_rating, use_container_width=True)


def main():
    st.sidebar.title('Pengaturan Dashboard')

    # Pilih tema warna
    color_theme = st.sidebar.selectbox(
        "Pilih Tema Warna",
        ('Pastel', 'Viridis', 'Greens', 'Blues', 'Plasma')
    )

    # Map the selected theme to Plotly color scales
    if color_theme == 'Pastel':
        color_theme = px.colors.qualitative.Pastel
    elif color_theme == 'Viridis':
        color_theme = px.colors.sequential.Viridis
    elif color_theme == 'Greens':
        color_theme = px.colors.sequential.Greens
    elif color_theme == 'Blues':
        color_theme = px.colors.sequential.Blues
    elif color_theme == 'Plasma':
        color_theme = px.colors.sequential.Plasma

    # Pilih tab yang diinginkan
    tab = st.sidebar.radio(
        "Pilih Visualisasi",
        ('Data AdventureWork', 'Data IMDb')
    )

    if tab == 'Data AdventureWork':
        # Pilih jenis visualisasi untuk AdventureWorks
        chart_type = st.sidebar.selectbox(
            "Pilih Jenis Chart",
            ('Comparison', 'Distribution', 'Composition', 'Relationship')
        )

        if chart_type == 'Comparison':
            fetch_and_display_sales_comparison(color_theme, chart_type)
        elif chart_type == 'Distribution':
            fetch_and_display_income_distribution(color_theme)
        elif chart_type == 'Composition':
            promotion_data = fetch_promotion_data()
            create_donut_chart(promotion_data, color_theme)
        elif chart_type == 'Relationship':
            fetch_and_display_product_data(color_theme)

    elif tab == 'Data IMDb':
        load_and_display_imdb_data(color_theme)

if __name__ == "__main__":
    main()
