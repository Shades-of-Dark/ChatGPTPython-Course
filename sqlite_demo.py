import sqlite3
from employee import Employee

# CREATE
conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE Table employees (
    first text,
   last text,
  pay integer
  )""")

def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first':emp.first, 'last':emp.last, 'pay':emp.pay})

def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last':lastname})
    return c.fetchall()

def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees WHERE first = :first AND last = :last",
                  {'first': emp.first, 'last': emp.last})

# UPDATE
emp1 = Employee('Vedh', 'Rao', 2000000)
emp2 = Employee('Tom', 'Rao', 5000)


#  READ

insert_emp(emp1)
insert_emp(emp2)

# DELETE
# c.execute("DELETE FROM EMPLOYEES")
update_pay(emp2, 10000000)


remove_emp(emp1)
print(get_emps_by_name("Rao"))
conn.close()
