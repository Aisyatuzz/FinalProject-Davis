import mysql.connector
import pandas as pd
import plotly.express as px
import streamlit as st

# Fungsi untuk menghubungkan ke database MySQL dan mengambil data promosi
def fetch_promotion_data():
    conn = mysql.connector.connect(
        host = st.secrets["connections"]["mydb"]["host"],
        port = st.secrets["connections"]["mydb"]["port"],
        database = st.secrets["connections"]["mydb"]["database"],
        user = st.secrets["connections"]["mydb"]["username"],
        password = st.secrets["connections"]["mydb"]["password"]
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
    st.markdown('Visualisasi ini digunakan untuk menampilkan distribusi dari berbagai jenis promosi yang paling umum dan tidak umum digunakan, dapat dilihat bahwa volume discount merupakan jenis promosi yang paling banyak digunakan yaitu sebesar 31.3% ')
    st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk mengambil dan menampilkan scatter plot data harga produk vs subkategori produk
def fetch_and_display_product_data(color_theme):
    conn = mysql.connector.connect(
        host = st.secrets["connections"]["mydb"]["host"],
        port = st.secrets["connections"]["mydb"]["port"],
        database = st.secrets["connections"]["mydb"]["database"],
        user = st.secrets["connections"]["mydb"]["username"],
        password = st.secrets["connections"]["mydb"]["password"]
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
    st.markdown('Visualiasi ini digunakan untuk menampilkan hubungan antara harga produk dan subkategori produk, dapat dilihat bahwa terdapat variasi yang signifikan dalam harga produk tergantung pada subkategori produk. Subkategori seperti "Road Bikes" dan "Mountain Bikes" memiliki variasi harga yang sangat luas dan harga yang tinggi, sementara subkategori lainnya memiliki rentang harga yang lebih sempit dan lebih rendah')
    st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk mengambil dan menampilkan scatter plot distribusi pendapatan tahunan pelanggan
def fetch_and_display_income_distribution(color_theme):
    conn = mysql.connector.connect(
        host = st.secrets["connections"]["mydb"]["host"],
        port = st.secrets["connections"]["mydb"]["port"],
        database = st.secrets["connections"]["mydb"]["database"],
        user = st.secrets["connections"]["mydb"]["username"],
        password = st.secrets["connections"]["mydb"]["password"]
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
    st.markdown('Visualisasi ini digunakan untuk menampilkan distribusi pendapatan tahunan pelanggan, dapat dilihat bahwa pendapatan tahunan pelanggan tersebar merata dalam beberapa interval yang berbeda dan mayoritas pendapatan tahunan pelanggan berada dalam kisaran 50k hingga 150k')
    st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk mengambil dan menampilkan perbandingan total penjualan berdasarkan wilayah penjualan
def fetch_and_display_sales_comparison(color_theme, chart_type):
    conn = mysql.connector.connect(
        host = st.secrets["connections"]["mydb"]["host"],
        port = st.secrets["connections"]["mydb"]["port"],
        database = st.secrets["connections"]["mydb"]["database"],
        user = st.secrets["connections"]["mydb"]["username"],
        password = st.secrets["connections"]["mydb"]["password"]
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
        st.markdown('Visualisasi ini digunakan untuk menampilkan total penjualan internet pada setiap wilayah, dapat dilihat bahwa negara Australia merupakan negara dengan total penjualan internet terbanyak, sedangkan Central merupakan negara dengan total penjualan internet paling sedikit')
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
        st.markdown('Visualisasi ini digunakan untuk membandingkan anggaran produksi dari beberapa film untuk melihat perbedaan investasi antara film-film tersebut, dapat dilihat bahwa film "Barbie" memiliki anggaran produksi tertinggi yaitu 125M dibanding anggaran produksi film lainnya')
        data_to_visualize_budget = df[['Name', 'Budget']].sort_values(by='Budget', ascending=False).head(10)
        fig_budget = px.bar(data_to_visualize_budget, x='Name', y='Budget', title='Anggaran Produksi Film',
                            labels={'Name': 'Film', 'Budget': 'Anggaran Produksi'},
                            color='Name', color_discrete_sequence=color_theme)
        fig_budget.update_layout(xaxis_title='Film', yaxis_title='Anggaran Produksi')
        st.plotly_chart(fig_budget, use_container_width=True)

    elif imdb_chart_type == 'Distribution':
        st.title('Pengaruh Tahun Rilis dengan Rating Film')
        st.markdown('Visualisasi ini digunakan untuk mengeksplorasi pengaruh tahun rilis terhadap rating film, dapat dilihat bahwa semua kategori rating memiliki titik-titik yang tersebar secara merata di sepanjang rentang tahun yang ditampilkan dan menunjukkan bahwa tahun rilis tidak secara langsung mempengaruhi rating film')
        data_to_visualize_rating = df[['Year', 'Rating']]
        fig_rating = px.scatter(data_to_visualize_rating, x='Year', y='Rating', title='Pengaruh Tahun Rilis dengan Rating Film',
                                labels={'Year': 'Tahun Rilis', 'Rating': 'Rating'},
                                color='Year', color_continuous_scale=color_theme)
        fig_rating.update_layout(xaxis_title='Tahun Rilis', yaxis_title='Rating')
        st.plotly_chart(fig_rating, use_container_width=True)

    elif imdb_chart_type == 'Composition':
        st.title('Komposisi Pendapatan Kotor Global Film')
        st.markdown('Visualisasi ini digunakan untuk mengetahui komposisi pendapatan kotor global film, dapat dilihat bahwa mayoritas film memiliki pendapatan kotor global yang sangat rendah (Very Low). Hanya sebagian kecil film yang memiliki pendapatan dalam kategori Moderate atau High, dan tidak ada film yang masuk dalam kategori Low. Hal ini menunjukkan bahwa sebagian besar film tidak menghasilkan pendapatan yang signifikan secara global')
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
        st.markdown('Visualisasi ini digunakan untuk mengeksplorasi hubungan antara anggaran produksi dan rating film, dapat dilihat bahwa terdapat variasi anggaran produksi di berbagai kategori rating film, tetapi film dengan rating PG-13 cenderung memiliki anggaran produksi yang lebih tinggi dibandingkan dengan kategori rating lainnya')
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
