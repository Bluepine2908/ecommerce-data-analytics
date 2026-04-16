import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    return pd.read_csv("Updated_sales.csv")

def clean_data(sales_data):
    sales_data = sales_data.dropna(subset=["Order ID"])

    # For changing non numeric values to Null values and then dropping the null values
    sales_data["Quantity Ordered"] = pd.to_numeric(sales_data["Quantity Ordered"], errors="coerce")
    sales_data = sales_data.dropna(subset=["Quantity Ordered"])
    return sales_data

def set_dtype(sales_data):
    sales_data["Order ID"] = sales_data["Order ID"].astype(str)
    sales_data["Product"] = sales_data["Product"].astype(str)
    sales_data["Quantity Ordered"] = sales_data["Quantity Ordered"].astype(int)
    sales_data["Price Each"] = sales_data["Price Each"].astype(float)
    sales_data["Order Date"] = pd.to_datetime(sales_data["Order Date"], format="%m/%d/%y %H:%M")
    sales_data["Purchase Address"] = sales_data["Purchase Address"].astype(str)
    return sales_data

def add_column(sales_data):
    sales_data["Sales"] = sales_data["Quantity Ordered"] * sales_data["Price Each"]
    return sales_data

def monthly_revenue_graph(sales_data):
    sales_data["Month"] = sales_data["Order Date"].dt.month
    monthly_sales = sales_data.groupby("Month")
    month_rev = monthly_sales["Sales"].sum()

    month_names = {
        1 : "Jan",
        2 : "Feb",
        3 : "Mar",
        4 : "Apr",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "Aug",
        9 : "Sept",
        10 : "Oct",
        11 : "Nov",
        12 : "Dec"
    }
    month_rev_x = [month_names[month] for month in month_rev.index]
    month_rev_y = np.array(month_rev.values)

    plt.title("Monthly Revenue Distribution", fontweight = "bold")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.bar(month_rev_x, month_rev_y)
    plt.tight_layout()
    return plt.show()

def product_rev_vs_product_count(sales_data):
    product_group = sales_data.groupby("Product")
    product_rev = product_group["Sales"].sum()
    product_mon = product_group["Product"].count()

    product_rev_x = product_rev.index
    product_mon_x = product_mon.index
    product_rev_y = np.array(product_rev.values)
    product_mon_y = np.array(product_mon.values)

    figure, axes = plt.subplots(1,2, sharey = True)
    axes[0].barh(product_rev_x, product_rev_y)
    axes[0].set_title("Revenue by Product")
    axes[1].barh(product_mon_x, product_mon_y)
    axes[1].set_title("Quantity Sold by Product")

    plt.tight_layout()
    return plt.show()

def most_order_time(sales_data):
    sales_data["Time"] = sales_data["Order Date"].dt.hour
    hourly_purchase_grp = sales_data.groupby("Time")
    hourly_purchase = hourly_purchase_grp["Order Date"].count()
    hourly_purchase_x = np.array(hourly_purchase.index)
    hourly_purchase_y = np.array(hourly_purchase.values)

    plt.plot(hourly_purchase_x, hourly_purchase_y)
    plt.title("Number of Orders by Hours of Day")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number Of Orders")

    plt.tight_layout()
    return plt.show()

def city_revenue(sales_data):
    sales_data["City Name"] = sales_data["Purchase Address"].str.split(",").str[1].str.strip()
    city_rev = sales_data.groupby("City Name")["Sales"].sum()

    max_city_name = city_rev.idxmax()
    max_city_value = city_rev.max()
    print(f"The city with maximum revenue {max_city_name} and the revenue is {max_city_value}$")

    city_rev_x = city_rev.index
    city_rev_y = np.array(city_rev.values)

    plt.bar(city_rev_x, city_rev_y)
    plt.title("Revenue of City")
    plt.xlabel("City")
    plt.ylabel("Revenue")

    plt.tight_layout()
    return plt.show()

def top_ordered_together(sales_data):
    def combine_products(x):
        return ",".join(x)
    grp_id = sales_data.groupby("Order ID")["Product"].apply(combine_products)
    grp_id = grp_id[grp_id.str.contains(",")]
    top_products = grp_id.value_counts().head()

    top_products_name = top_products.idxmax()
    top_products_value = top_products.max()
    print(f"The product bought together the most are {top_products_name} with the amount of people buying it together being {top_products_value}.")

    top_products_x = top_products.index
    top_products_y = np.array(top_products.values)

    plt.barh(top_products_x, top_products_y)
    plt.title("Top Products Ordered Together")
    plt.xlabel("Product Combination")
    plt.ylabel("Number of Orders")

    plt.tight_layout()
    return plt.show()
        
    
def main():
    sales_data = load_data()
    sales_data = clean_data(sales_data)
    sales_data = set_dtype(sales_data)
    sales_data = add_column(sales_data)


    monthly_revenue_graph(sales_data)
    product_rev_vs_product_count(sales_data)
    most_order_time(sales_data)
    city_revenue(sales_data)
    top_ordered_together(sales_data)
    

if __name__ == "__main__":
    main()
