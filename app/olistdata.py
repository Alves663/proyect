import pandas as pd
from datashader.utils import lnglat_to_meters as webm


class OlistData(object):

    # percentage_of_rows must be between 0 and 1.
    percentage_of_rows = None

    def __init__(self):
        if self.percentage_of_rows is None:
            self.orders_items = pd.read_csv("data/olist_order_items_dataset.csv")
            self.orders = self.__read_orders()
            self.products = pd.read_csv("data/olist_products_dataset.csv")
            self.orders_payments = pd.read_csv("data/olist_order_payments_dataset.csv")
            self.order_reviews = pd.read_csv('data/olist_order_reviews_dataset.csv')
            self.sellers = self.__read_sellers()
            self.costumer = self.__read_costumer()
            self.geolocation = self.__read_geolocation()
            self.costumer_geolocation = self.__costumer_geolocation()
            self.seller_geolocation = self.__seller_geolocation()
        else:
            self.orders_items = pd.read_csv("data/olist_order_items_dataset.csv").sample(frac=self.percentage_of_rows)
            self.orders = self.__read_orders(frac=self.percentage_of_rows)
            self.products = pd.read_csv("data/olist_products_dataset.csv").sample(frac=self.percentage_of_rows)
            self.orders_payments = pd.read_csv("data/olist_order_payments_dataset.csv").sample(frac=self.percentage_of_rows)
            self.order_reviews = pd.read_csv('data/olist_order_reviews_dataset.csv').sample(frac=self.percentage_of_rows)
            self.sellers = self.__read_sellers(frac=self.percentage_of_rows)
            self.costumer = self.__read_costumer(frac=self.percentage_of_rows)
            self.geolocation = self.__read_geolocation(frac=self.percentage_of_rows)
            self.costumer_geolocation = self.__costumer_geolocation()
            self.seller_geolocation = self.__seller_geolocation()

    @staticmethod
    def __read_orders(frac=None):
        if frac is None:
            orders = pd.read_csv("data/olist_orders_dataset.csv")
        else:
            orders = pd.read_csv("data/olist_orders_dataset.csv").sample(frac=frac)
        orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
        orders["order_approved_at"] = pd.to_datetime(orders["order_approved_at"])
        orders["order_delivered_carrier_date"] = pd.to_datetime(orders["order_delivered_carrier_date"])
        orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
        orders["order_estimated_delivery_date"] = pd.to_datetime(orders["order_estimated_delivery_date"])
        return orders

    @staticmethod
    def __read_sellers(frac=None):
        if frac is None:
            sellers = pd.read_csv("data/olist_sellers_dataset.csv")
        else:
            sellers = pd.read_csv("data/olist_sellers_dataset.csv").sample(frac=frac)
        sellers.rename(columns={"seller_zip_code_prefix": "zip_code",
                                "seller_city": "city", "seller_state": "state"}, inplace=True)
        return sellers

    @staticmethod
    def __read_costumer(frac=None):
        if frac is None:
            costumer = pd.read_csv("data/olist_customers_dataset.csv")
        else:
            costumer = pd.read_csv("data/olist_customers_dataset.csv").sample(frac=frac)
        costumer.rename(columns={"customer_zip_code_prefix": "zip_code",
                                 "customer_city": "city", "customer_state": "state"}, inplace=True)
        return costumer

    @staticmethod
    def __read_geolocation(frac=None):
        if frac is None:
            geolocation = pd.read_csv("data/olist_geolocation_dataset.csv")
        else:
            geolocation = pd.read_csv("data/olist_geolocation_dataset.csv").sample(frac=frac)
        geolocation.rename(columns={"geolocation_zip_code_prefix": "zip_code",
                                    "geolocation_city": "city", "geolocation_state": "state"}, inplace=True)
        # Removing some outliers

        # Brazils most Northern spot is at 5 deg 16′ 27.8″ N latitude.;
        geolocation = geolocation[geolocation.geolocation_lat <= 5.27438888]
        # it’s most Western spot is at 73 deg, 58′ 58.19″W Long.
        geolocation = geolocation[geolocation.geolocation_lng >= -73.98283055]
        # It’s most southern spot is at 33 deg, 45′ 04.21″ S Latitude.
        geolocation = geolocation[geolocation.geolocation_lat >= -33.75116944]
        # It’s most Eastern spot is 34 deg, 47′ 35.33″ W Long.
        geolocation = geolocation[geolocation.geolocation_lng <= -34.79314722]

        x, y = webm(geolocation.geolocation_lng, geolocation.geolocation_lat)
        geolocation['x'] = pd.Series(x)
        geolocation['y'] = pd.Series(y)
        return geolocation

    def __costumer_geolocation(self):
        costumer = self.costumer[["customer_id", 'zip_code', 'city', 'state']]
        return costumer.merge(self.geolocation, on=["zip_code", "city", "state"], how="left")

    def __seller_geolocation(self):
        return self.sellers.merge(self.geolocation, on=["zip_code", "city", "state"], how="left")

    def get_costumer_distribution(self):
        return self.costumer_geolocation.groupby(["zip_code", "city",
                                                  "state", "x", "y"]).count()["customer_id"].reset_index()

    def get_seller_distribution(self):
        return self.seller_geolocation.groupby(["zip_code", "city",
                                                "state", "x", "y"]).count()["seller_id"].reset_index()

    def product_buy_by_costumer(self, year=None, month=None):
        orders_delivered = self.orders[self.orders["order_status"] == "delivered"]
        products = self.products[["product_id", "product_category_name"]]
        orders_items = self.orders_items.merge(products, on=["product_id"])
        orders_delivered_by_costumer = orders_delivered[
            ['order_id', 'customer_id', 'order_status', "order_delivered_customer_date"]]
        orders_items = orders_items.merge(orders_delivered_by_costumer, on=['order_id'])
        orders_items["order_delivered_customer_year"] = orders_items['order_delivered_customer_date'].dt.year
        orders_items["order_delivered_customer_month"] = orders_items['order_delivered_customer_date'].dt.month
        if year is None and month is None:
            return orders_items
        if year is not None and month is not None:
            return orders_items[(orders_items["order_delivered_customer_year"] == year) &
                                (orders_items["order_delivered_customer_month"] == month)]
        if year is not None and month is None:
            return orders_items[orders_items["order_delivered_customer_year"] == year]

        if year is None and month is not None:
            return orders_items[orders_items["order_delivered_customer_month"] == month]

    @staticmethod
    def product_best_sellers(orders_items_costumer, n_top=None):
        top_products = orders_items_costumer.groupby(["product_id"]).sum()["order_item_id"].sort_values(ascending=False)
        top_products_category = orders_items_costumer.groupby(["product_category_name"]).sum()["order_item_id"].sort_values(
            ascending=False)
        return top_products.reset_index().head(n_top), top_products_category.reset_index().head(n_top)

    def top_products_by_costumer(self, orders_items_costumer):
        orders_items_by_costumer = orders_items_costumer.groupby(["product_id", "customer_id"]).sum()[
            "order_item_id"].sort_values(ascending=False).reset_index()
        costumer_location = self.__costumer_geolocation()
        top_products_by_costumer = orders_items_by_costumer.merge(costumer_location, on=["customer_id"])
        return top_products_by_costumer.groupby(["product_id", "zip_code", "city", "state", "x", "y"]).sum()[
            "order_item_id"].sort_values(ascending=False).reset_index()

    def get_incomes(self):
        orders_df = self.orders
        order_items = self.orders_items
        order_reviews = self.order_reviews
        customer = pd.read_csv('data/olist_customers_dataset.csv', dtype={'customer_zip_code_prefix': str})
        # getting the first 3 digits of customer zipcode
        customer['customer_zip_code_prefix_3_digits'] = customer['customer_zip_code_prefix'].str[0:3]
        customer['customer_zip_code_prefix_3_digits'] = customer['customer_zip_code_prefix_3_digits'].astype(int)

        geo = pd.read_csv("data/olist_geolocation_dataset.csv", dtype={'geolocation_zip_code_prefix': str})
        # Removing some outliers
        #Brazils most Northern spot is at 5 deg 16′ 27.8″ N latitude.;
        geo = geo[geo.geolocation_lat <= 5.27438888]
        #it’s most Western spot is at 73 deg, 58′ 58.19″W Long.
        geo = geo[geo.geolocation_lng >= -73.98283055]
        #It’s most southern spot is at 33 deg, 45′ 04.21″ S Latitude.
        geo = geo[geo.geolocation_lat >= -33.75116944]
        #It’s most Eastern spot is 34 deg, 47′ 35.33″ W Long.
        geo = geo[geo.geolocation_lng <= -34.79314722]

        x, y = webm(geo.geolocation_lng, geo.geolocation_lat)
        geo['x'] = pd.Series(x)
        geo['y'] = pd.Series(y)

        geo['geolocation_zip_code_prefix_1_digits'] = geo['geolocation_zip_code_prefix'].str[0:1]
        geo['geolocation_zip_code_prefix_2_digits'] = geo['geolocation_zip_code_prefix'].str[0:2]
        geo['geolocation_zip_code_prefix_3_digits'] = geo['geolocation_zip_code_prefix'].str[0:3]
        geo['geolocation_zip_code_prefix_4_digits'] = geo['geolocation_zip_code_prefix'].str[0:4]

        # transforming the prefixes to int for plotting purposes
        geo['geolocation_zip_code_prefix'] = geo['geolocation_zip_code_prefix'].astype(int)
        geo['geolocation_zip_code_prefix_1_digits'] = geo['geolocation_zip_code_prefix_1_digits'].astype(int)
        geo['geolocation_zip_code_prefix_2_digits'] = geo['geolocation_zip_code_prefix_2_digits'].astype(int)
        geo['geolocation_zip_code_prefix_3_digits'] = geo['geolocation_zip_code_prefix_3_digits'].astype(int)
        geo['geolocation_zip_code_prefix_4_digits'] = geo['geolocation_zip_code_prefix_4_digits'].astype(int)

        brazil_geo = geo.set_index('geolocation_zip_code_prefix_3_digits').copy()

        orders = orders_df.merge(order_items, on='order_id')
        orders = orders.merge(customer, on='customer_id')
        orders = orders.merge(order_reviews, on='order_id')
        gp = orders.groupby('customer_zip_code_prefix_3_digits')['price'].sum().to_frame()
        revenue = brazil_geo.join(gp)

        revenue["revenue"] = revenue.price / 1000
        return revenue







