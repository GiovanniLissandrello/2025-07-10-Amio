from database.DB_connect import DBConnect
from model.arco import Arco
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select category_id, category_name from categories c "

        cursor.execute(query)

        for row in cursor:
            results.append((row["category_id"],row["category_name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(id_category):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select  p.product_id, p.product_name , p.brand_id , p.category_id , p.model_year , p.list_price 
                    from categories c, products p
                    where c.category_id = p.category_id 
                    and c.category_id = %s"""

        cursor.execute(query, (id_category,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArchi(id_category, start, end, dizionario):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.product_id as id1, t1.num_vendite1, t2.product_id as id2, t2.num_vendite2, (t1.num_vendite1 + t2.num_vendite2) as peso
                    from (select p.product_name, p.product_id, count(*) as num_vendite1
                    from categories c, products p,  orders o, order_items oi 
                    where c.category_id = p.category_id 
                    and c.category_id = %s
                    and p.product_id  = oi.product_id 
                    and oi.order_id = o.order_id 
                    and o.order_date BETWEEN %s and %s
                    group by p.product_name) t1,
                    (select p.product_name, p.product_id, count(*) as num_vendite2
                    from categories c, products p,  orders o, order_items oi 
                    where c.category_id = p.category_id 
                    and c.category_id = %s
                    and p.product_id  = oi.product_id 
                    and oi.order_id = o.order_id 
                    and o.order_date BETWEEN %s and %s
                    group by p.product_name) t2
                    where t1.num_vendite1 >= t2.num_vendite2 
                    and t1.product_id != t2.product_id """

        cursor.execute(query, (id_category, start, end, id_category, start, end,))

        for row in cursor:
            results.append(Arco(dizionario.get(row["id1"]),dizionario.get(row["id2"]), row["peso"]))

        cursor.close()
        conn.close()
        return results

