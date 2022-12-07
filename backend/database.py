import streamlit as st
import mysql.connector
import random

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "inventory_management_system"
)
c = mydb.cursor()

from reload import reload
def check_login(email, password):
    # print(email)
    values = email
    c.execute("SELECT * FROM login WHERE email_id = %s", (values,))
    passws = c.fetchall()
    for passw in passws:
        if passw[1] == password:
            reload("home")
            break
        else:
            st.error("Incorrect credentials, please try again.")

def add_login(fn, ln, email, password):
    values = email
    c.execute("SELECT * FROM login WHERE email_id = %s", (values,))
    x = c.fetchall()
    if x != []:
        print(x)
        st.error("User already exists :/")
    else:
        c.execute("INSERT INTO login (email_id, pass) VALUES (%s,%s)", (email, password))
        vid = random.randint(10000, 99999)
        c.execute("INSERT INTO vendor (fname, lname, vendor_id, email_id) VALUES (%s, %s, %s, %s) ", (fn, ln, vid, email))
        st.success("Successfully Added User")
    # else:
    #     st.error("User already exists :/")
    

def update_password(mail, old_pass, new_pass):
    c.execute("UPDATE login SET pass = %s WHERE email_id = %s AND pass = %s", (new_pass, mail, old_pass))
    if c.rowcount is not None:
        st.success("Password updated successfully!")

def view_stock():
    c.execute("SELECT * FROM stock")
    data = c.fetchall()
    return data

def add_stock(pid, pdate, mdate, qty):
    c.execute("INSERT INTO stock VALUES (%s, %s, %s, %s)", (pid, pdate, mdate, qty))
    st.success("Values inserted")

def prod_not_in_stock():
    c.execute("SELECT product.product_id FROM product WHERE product.product_id NOT IN (SELECT stock.pid FROM stock)")
    data = c.fetchall()
    return data

def prod_in_stock():
    c.execute("SELECT product.product_id FROM product WHERE product.product_id IN (SELECT stock.pid FROM stock)")
    data = c.fetchall()
    return data

def get_product(pid):
    c.execute("SELECT * FROM product WHERE product.product_id = {}".format(pid))
    data = c.fetchall()
    print(data)
    return data

def get_stock(pid):
    c.execute("SELECT * FROM stock WHERE stock.pid = {}".format(pid))
    data = c.fetchall()
    print(data)
    return data

def update_stock(pid, pdate, mdate, qty):
    c.execute("UPDATE stock SET purchase_date = %s, mfg_date = %s, pqty = %s WHERE pid = %s", (pdate, mdate, qty, pid))
    st.success("Stock updated successfully")

def remove_stock(pid):
    c.execute("DELETE FROM stock WHERE stock.pid = {}".format(pid))
    st.success("Product Deleted successfully")

def view_product():
    c.execute("SELECT * FROM product")
    data = c.fetchall()
    return data

def add_product(pid, pname, cp, mfg, mrp):
    c.execute("INSERT INTO product VALUES (%s, %s, %s, %s, %s)", (pid, pname, cp, mfg, mrp))
    st.success("Inserted Product")

def get_product_names():
    c.execute("SELECT product.product_name FROM product")
    data = c.fetchall()
    return data

def get_product_id(pname):
    value = pname
    c.execute("SELECT product.product_id FROM product WHERE product_name = %s", (value,))
    data = c.fetchall()
    return data[0][0]

def get_prod_mrp(pid):
    value = pid
    c.execute("SELECT product.mrp FROM product WHERE product.product_id = %s", (value,))
    data = c.fetchall()
    return data[0][0]

def update_prod_price(pid, cp):
    c.execute("UPDATE product SET product.cost_price = %s WHERE product.product_id = %s", (cp, pid))
    st.success("Cost price updated")

def view_customer():
    c.execute("SELECT * FROM customer")
    data = c.fetchall()
    return data

def add_customer(cid, pn, mail, cname, sno, sname, pin):
    c.execute("INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s)", (cid, pn, mail, cname, sno, sname, pin))
    st.success("Inserted Customer")

def get_customer(cid):
    c.execute("SELECT * FROM customer WHERE customer.cust_id = {}".format(cid))
    data = c.fetchall()
    print(data)
    return data

def get_cust_names():
    c.execute("SELECT customer.cust_name FROM customer")
    data = c.fetchall()
    return data

def get_cust_ids(cname):
    value = cname
    c.execute("SELECT customer.cust_id FROM customer WHERE customer.cust_name = %s", (value,))
    data = c.fetchall()
    return data

def update_customer(cid, phno, email, cname, stno, stname, pin):
    c.execute("UPDATE customer SET phone_no = %s, cust_email_id = %s, cust_name = %s, str_no = %s, str_name = %s, pincode = %s WHERE cust_id = %s", (phno, email, cname, stno, stname, pin, cid))
    st.success("Successfully Updated Customer")

def view_invoice():
    c.execute("SELECT * FROM invoice")
    data = c.fetchall()
    return data

def get_vendor_id(mail):
    print(mail)
    c.execute("SELECT DISTINCT vendor.vendor_id FROM vendor WHERE vendor.email_id = %s", (mail, ))
    data = c.fetchall()
    print("data", data[0][0])
    return data[0][0]

def add_invoice(pid, ino, idate, sp, pqty, dis, phno, vid):
    c.execute("INSERT INTO invoice VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (pid, ino, idate, sp, pqty, dis, phno, vid))
    c.execute("SELECT customer.cust_id FROM customer WHERE customer.phone_no = %s", (phno,))
    cid = c.fetchall()[0][0]
    c.execute("SELECT DISTINCT vendor.fname, vendor.lname, vendor.vendor_id, vendor.email_id FROM vendor WHERE vendor.vendor_id = %s", (vid,))
    d = c.fetchall()
    fn, ln, vid0, mail = d[0][0], d[0][1], d[0][2], d[0][3]
    c.execute("INSERT INTO vendor VALUES (%s, %s, %s, %s, %s, %s)", (fn, ln, vid0, mail, pid, cid))
    c.execute("CALL insert_invoice(%s,%s)", (pqty, pid))
    st.success("Invoice inserted successfully")

def get_invoice(iid):
    c.execute("SELECT * FROM invoice WHERE invoice.invoice_no = {}".format(iid))
    data = c.fetchall()
    return data

def get_phnos():
    c.execute("SELECT customer.phone_no FROM customer")
    data = c.fetchall()
    return data