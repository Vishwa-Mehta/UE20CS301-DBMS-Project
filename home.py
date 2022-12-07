import streamlit as st
from backend.database import *
import pandas as pd
import random

st.title("Welcome to ListAll")
def main():
    menu = ["View Stock", "Add item to stock", "Update Stock", "Remove Stock", "View Products", "Add Product", "Update Product Price", "View Customers", "Add Customer", "Update Customer", "View Invoice", "Add Invoice", "Change Password"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View Stock":
        st.subheader("Current Stock:")
        data = view_stock()
        df = pd.DataFrame(data, columns = ['pid', 'purchase_date', 'mfg_date', 'pqty'])
        st.dataframe(df)

    elif choice == "Add item to stock":
        st.subheader("Add New Product to Current Stock:")
        list_of_products = [i[0] for i in prod_not_in_stock()]
        prod = st.selectbox("Products that can be added to stock", list_of_products)
        result = get_product(prod)
        if result:
            pid = st.text_input("Product ID:", result[0][0])
            pname = st.text_input("Product Name:", result[0][1])
            pur_date = st.text_input("Purchase Date(YYYY-MM-DD):")
            mfg_date = st.text_input("Manufacturing Date(YYYY-MM-DD):")
            qty = st.text_input("Product Quantity:")
            if st.button("Add"):
                add_stock(pid, pur_date, mfg_date, qty)
        with st.expander("View Updated table"):
            data = view_stock()
            df = pd.DataFrame(data, columns = ['pid', 'purchase_date', 'mfg_date', 'pqty'])
            st.dataframe(df)

    elif choice == "Update Stock":
        st.subheader("Update Stock:")
        list_of_products = [i[0] for i in prod_in_stock()]
        prod = st.selectbox("Products that can be updated in stock", list_of_products)
        result = get_stock(prod)
        res = get_product(prod)
        # print(result[0])
        if result:
            # print(type(result[0][1]), type(result[0][2]))
            pid = result[0][0]
            pdate = result[0][1]
            mdate = result[0][2]
            pqty = result[0][3]
            col1, col2= st.columns(2)
            with col1:
                pid0 = st.text_input("Product ID:", pid, disabled = True)
                new_pdate = st.text_input("Purchase Date(YYYY-MM-DD):", pdate)
            with col2:
                pname = st.text_input("Product Name:", res[0][1], disabled = True)
                new_mdate = st.text_input("Manufacturing Date(YYYY-MM-DD):", mdate)
            new_pqty = st.text_input("Product Quantity:", pqty)
            if st.button("Update"):
                update_stock(pid0, new_pdate, new_mdate, new_pqty)
        with st.expander("View Updated table"):
            data = view_stock()
            df = pd.DataFrame(data, columns = ['pid', 'purchase_date', 'mfg_date', 'pqty'])
            st.dataframe(df)
    
    elif choice == "Remove Stock":
        st.subheader("Remove Stock:")
        list_of_products = [i[0] for i in prod_in_stock()]
        prod = st.selectbox("Products that can be added to stock", list_of_products)
        result = get_product(prod)
        if result:
            pid = result[0][0]
            if st.button("Remove "+str(result[0][1])):
                remove_stock(pid)
        with st.expander("View Updated table"):
            data = view_stock()
            df = pd.DataFrame(data, columns = ['pid', 'purchase_date', 'mfg_date', 'pqty'])
            st.dataframe(df)

    elif choice == "View Products":
        st.subheader("Products:")
        data = view_product()
        df = pd.DataFrame(data, columns = ['product_id', 'product_name', 'cost_price', 'manufacturer', 'mrp'])
        st.dataframe(df)

    elif choice == "Add Product":
        st.subheader("Enter product details:")
        gen_pid = random.randint(10000, 99999)
        d = get_product(gen_pid)
        if not d:
            print(gen_pid)
            pid = st.text_input("Product ID:", gen_pid, disabled = True)
        else:
            st.error("Please reload the page.")
        pname = st.text_input("Product Name:")
        cp = st.text_input("Cost Price:")
        mfg = st.text_input("Manufacturer Name:")
        mrp = st.text_input("MRP:")
        if st.button("Add"):
            add_product(pid, pname, cp, mfg, mrp)
        with st.expander("View Updated table"):
            data = view_product()
            df = pd.DataFrame(data, columns = ['product_id', 'product_name', 'cost_price', 'manufacturer', 'mrp'])
            st.dataframe(df)

    elif choice == "Update Product Price":
        st.subheader("Update Product:")
        list_of_products = [i[0] for i in get_product_names()]
        pname = st.selectbox("Product Name:", list_of_products)
        prod = get_product_id(pname)
        result = get_product(prod)
        # print(result[0])
        if result:
            # print(type(result[0][1]), type(result[0][2]))
            pid = result[0][0]
            pname = result[0][1]
            cp = result[0][2]
            mfg = result[0][3]
            mrp = result[0][4]
            col1, col2= st.columns(2)
            with col1:
                pid0 = st.text_input("Product ID:", pid, disabled = True)
                pname0 = st.text_input("Name:", pname, disabled = True)
                mrp0 = st.text_input("MRP:", mrp, disabled = True)
            with col2:
                new_cp = st.text_input("Cost Price:", cp)
                mfg0 = st.text_input("Manufacturer Name:", mfg, disabled = True)
            if st.button("Update"):
                update_prod_price(pid0, new_cp)
            with st.expander("View Updated table"):
                data = view_product()
                df = pd.DataFrame(data, columns = ['product_id', 'product_name', 'cost_price', 'manufacturer', 'mrp'])
                st.dataframe(df)

    elif choice == "View Customers":
        st.subheader("Customers:")
        data = view_customer()
        df = pd.DataFrame(data, columns = ['cust_id', 'phone_no', 'cust_email_id', 'cust_name', 'str_no', 'str_name', 'pincode'])
        st.dataframe(df)
    
    elif choice == "Add Customer":
        st.subheader("Enter customer details:")
        gen_cid = random.randint(10000, 99999)
        d = get_customer(gen_cid)
        if not d:
            print(gen_cid)
            cid = st.text_input("Customer ID:", gen_cid, disabled = True)
        else:
            st.error("Please reload the page.")
        cname = st.text_input("Customer Name:")
        pn = st.text_input("Phone Number:")
        mail = st.text_input("Email ID:")
        col1, col2, col3 = st.columns(3)
        with col1:
            sno = st.text_input("Street Number:")
        with col2:
            sname = st.text_input("Street Name:")
        with col3:
            pin = st.text_input("Pincode:")
        
        if st.button("Add"):
            add_customer(cid, pn, mail, cname, sno, sname, pin)
        
        with st.expander("View Updated table"):
            data = view_customer()
            df = pd.DataFrame(data, columns = ['cust_id', 'phone_no', 'cust_email_id', 'cust_name', 'str_no', 'str_name', 'pincode'])
            st.dataframe(df)

    elif choice == "Update Customer":
        st.subheader("Update Customer:")
        list_of_cnames = [i[0] for i in get_cust_names()]
        # print(list_of_cnames)
        cname = st.selectbox("Select customer to be updated", list_of_cnames)
        # print(cname)
        cid = get_cust_ids(cname)
        # print(cid[0][0])
        result = get_customer(cid[0][0])
        # print(result[0])
        if result:
            cid = result[0][0]
            phno = result[0][1]
            email = result[0][2]
            cname = result[0][3]
            stno = result[0][4]
            stname = result[0][5]
            pin = result[0][6]
            cid0 = st.text_input("Customer ID:", cid, disabled = True)
            new_phno = st.text_input("Phone Number", phno)
            new_email = st.text_input("Email ID:", email)
            new_cname = st.text_input("Name:", cname)
            new_stno = st.text_input("Street Number:", stno)
            new_stname = st.text_input("Street Name:", stname)
            new_pin = st.text_input("Pincode:", pin)
            if st.button("Update"):
                update_customer(cid0, new_phno, new_email, new_cname, new_stno, new_stname, new_pin)
        with st.expander("View Updated table"):
            data = view_customer()
            df = pd.DataFrame(data, columns = ['cust_id', 'phone_no', 'cust_email_id', 'cust_name', 'str_no', 'str_name', 'pincode'])
            st.dataframe(df)

    elif choice == "View Invoice":
        st.subheader("Invoice:")
        data = view_invoice()
        df = pd.DataFrame(data, columns = ['prod_id', 'invoice_no', 'invoice_date', 'selling_price', 'prod_qty', 'discount', 'phone_no', 'vendor_id'])
        st.dataframe(df)

    elif choice == "Add Invoice":
        st.subheader("Add Invoice:")
        list_of_products = [i[1] for i in view_product()]
        prod = st.selectbox("Product Name:", list_of_products)
        pid = get_product_id(prod)
        gen_iid = random.randint(10000, 99999)
        d = get_invoice(gen_iid)
        if not d:
            print(gen_iid)
            iid = st.text_input("Invoice ID:", gen_iid, disabled = True)
        else:
            st.error("Please reload the page.")
        idate = st.text_input("Invoice Date (YYYY-MM-DD):")
        dis = st.text_input("Discount Given(%):")
        mrp = get_prod_mrp(pid)
        if dis:
            dis = float(dis) * 0.01
            sp = mrp - (mrp * dis)
            sp0 = st.text_input("Selling Price:", sp, disabled = True)
        pqty = st.text_input("Product Quantity:")
        list_of_phnos = [i[0] for i in get_phnos()]
        pno = st.selectbox("Customer Phone Number:", list_of_phnos)
        mail = st.text_input("Vendor Email ID:")
        # vid = 0
        if mail:
            vid = get_vendor_id(mail)
            # pass
        # phno = get_cus_phone(pno)
        if st.button("Add Invoice"):
            add_invoice(pid, iid, idate, sp0, pqty, dis, pno, vid)
        with st.expander("View Updated Invoice"):
            data = view_invoice()
            df = pd.DataFrame(data, columns = ['prod_id', 'invoice_no', 'invoice_date', 'selling_price', 'prod_qty', 'discount', 'phone_no', 'vendor_id'])
            st.dataframe(df)


    elif choice == "Change Password":
        st.subheader("Enter New Credentials Below:")
        email = st.text_input("Email:")
        old_pass = st.text_input("Old Password:", type = "password")
        new_pass = st.text_input("New Password:", type = "password")
        if st.button("Change Password"):
            update_password(email, old_pass, new_pass)
    
    else:
        st.subheader("Home Page")
if __name__ == '__main__':
    main()