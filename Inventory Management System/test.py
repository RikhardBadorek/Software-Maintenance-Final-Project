import unittest
from billing import billManager
import os
import sqlite3
from tkinter import Tk

class TestBillManager(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.bill_manager = billManager(self.root)
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    # 3 Unit tests

    def test_calc_addition(self):
        self.bill_manager.var_cal_input.set(" 100+30 ")
        self.bill_manager.perform_cal()
        self.assertEqual(self.bill_manager.var_cal_input.get(), "130")

    def test_calc_multiplication(self):
        self.bill_manager.var_cal_input.set("10*5")
        self.bill_manager.perform_cal()
        self.assertEqual(self.bill_manager.var_cal_input.get(), "50")

    def test_new_feature(self):
        self.bill_manager.cart_list =[[ "1", "shirt", "100", "2", "50" ]]
        
        self.bill_manager.var_discount.set("10")
        self.bill_manager.bill_update()

        self.assertEqual(self.bill_manager.bill_amnt, 200.0)
        self.assertEqual(self.bill_manager.discount, 20.0)
        self.assertEqual(self.bill_manager.net_pay, 180.0)

    # 2 integration tests

    def test_db_integration(self):
        db_path = "ims.db"
        self.assertTrue(os.path.exists(db_path), "Database file is missing")
        
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cur.fetchall()
            
        self.assertTrue(len(tables) > 0, "no tables found in the database")

    def test_receipt_text_integration(self):
        self.bill_manager.bill_amnt = 100
        self.bill_manager.discount = 10
        self.bill_manager.net_pay = 90
        
        self.bill_manager.bill_bottom() 
        
        receipt_text = self.bill_manager.txt_bill_area.get('1.0', 'end')
        
        self.assertIn("Rs.100", receipt_text)
        self.assertIn("Rs.90", receipt_text)

    # regression test

    def test_empty_discount(self):
        self.bill_manager.cart_list =[[ "1", "watch", "1000", "3", "50" ]]
        
        self.bill_manager.var_discount.set("")
        self.bill_manager.bill_update()

        self.assertEqual(self.bill_manager.discount, 0.0)
        self.assertEqual(self.bill_manager.net_pay, 3000.0)

if __name__ == '__main__':
    unittest.main()

