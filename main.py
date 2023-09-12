import psycopg2



def create_table():
    
        cur.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR (30) NOT NULL,
                    last_name VARCHAR (30) NOT NULL,
                    email VARCHAR (60) NOT NULL UNIQUE);
                        ''')
        cur.execute('''
                CREATE TABLE IF NOT EXISTS phone_numbers(
                    client_id INTEGER NOT NULL REFERENCES clients (id),
                    number VARCHAR (30) UNIQUE);
                    ''')
        conn.commit()



def add_new_client (name, last_name, email):
    
        cur.execute('''
            INSERT INTO clients (name, last_name, email)
                VALUES (%s, %s, %s);''', (name, last_name, email))
        
        conn.commit()
        print(f'Добавлен клиент: {name} {last_name}') 

def add_phone_number(name, last_name, phone_number):
        cur.execute('''
            SELECT id FROM clients
             WHERE name = %s AND last_name =%s;''',(name, last_name))
        client_id = cur.fetchone()
        cur.execute('''
            INSERT INTO phone_numbers (client_id, number)
                VALUES (%s, %s);''',(client_id,phone_number))
        conn.commit()        
        print (f'Добавлен номер телефона для клиента {name} {last_name}')


def add_changes(client_id, name, last_name, email):
        cur.execute('''
            UPDATE clients 
               SET name= %s, last_name =%s, email = %s
             WHERE id = %s;''',(name, last_name,email, client_id))
        conn.commit
        cur.execute('''
            SELECT * FROM clients
            WHERE id = %s;''', (client_id))
        res = cur.fetchall()
        return res

def delete_phone_number(client_id, number):
      cur.execute('''
            DELETE FROM phone_numbers
             WHERE number = %s AND client_id = %s;''',(number, client_id))
      conn.commit()
      print(f'номер телефона {number} удален у клиента с id {client_id}')

def delete_client(name, last_name):
       cur.execute('''
            DELETE FROM phone_numbers
            WHERE client_id IN (SELECT id FROM clients
                                WHERE name =%s AND last_name =%s);''',(name, last_name))
       conn.commit()
       cur.execute('''
            DELETE FROM clients
            WHERE name = %s AND last_name = %s;''',(name, last_name))
       conn.commit()
       print (f'Данные о клиенте {name} {last_name} удалены')

def find_client(name ='%', last_name = '%', email = '%', phone_number= '%'):
       cur.execute('''
            SELECT c.name, c.last_name, c.email, pn.number FROM clients c
                   JOIN phone_numbers pn 
                   ON pn.client_id = c.id
             WHERE c.name LIKE %s AND c.last_name LIKE %s AND c.email LIKE %s AND pn.number LIKE %s;''', (name, last_name, email, phone_number,))
       conn.commit()
       print(cur.fetchall())
                  



if __name__ == '__main__':
    conn = psycopg2.connect(database = 'clients_data_base', user = 'postgres', password = '')
    with conn.cursor() as cur:
        # # создаем таблицы
        # table_creation  = create_table() 

        # # заполняем таблицы
        # new_clients = [('Brian', 'Molko', 'molko@gmail.ru'), ('Mike', 'Shinoda', 'mike@gmail.com'), ('Chester', 'Benington', 'chester@gmail.com')]
        # for one_client in new_clients:
        #     add_new_client(*one_client) 
        # new_phone_numbers = [('Brian', 'Molko', '111111'),('Mike', 'Shinoda', '222222'), ('Chester', 'Benington', '333333')]
        # for one_number in new_phone_numbers:
        #        add_phone_number(*one_number)

        # # изменяем данные
        # add_changes('1', 'Brian', 'Molko', 'brianmolko@gmail.com' )
    
        # # удаляем номер телефона
        # delete_number = delete_phone_number('2', '222222')

        # # удаляем клиента
        # del_client = delete_client('Mike', 'Shinoda')

        # # ищем клиента
        # find = find_client('Brian','Molko')
        

        
    conn.close()
