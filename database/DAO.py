from database.DB_connect import DBConnect
from model.state import State


class DAO():
    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        select ID
        from state s 
        """
        result = []
        cursor.execute(query)
        for row in cursor:
            result.append(row["ID"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllShapes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct shape
            from sighting s 
        """
        result = []
        cursor.execute(query)
        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(stato):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct s.city 
            from sighting s
            where s.state = %s
        """
        result = []
        cursor.execute(query, (stato, ))
        for row in cursor:
            result.append(row["city"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(stato, forma):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select s1.city as c1, s2.city as c2, count(s1.shape) as peso
            from sighting s1, sighting s2
            where s1.state = %s and s1.state = s2.state
                and s1.id != s2.id and s1.city != s2.city
                and year(s1.`datetime`) = year(s2.`datetime`)
                and s1.shape = %s and s1.shape = s2.shape
            group by s1.city, s2.city
        """
        result = []
        cursor.execute(query, (stato, forma, ))
        for row in cursor:
            result.append((row["c1"], row["c2"], row["peso"]))
        cursor.close()
        conn.close()
        return result






