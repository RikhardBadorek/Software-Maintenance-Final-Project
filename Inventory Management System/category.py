from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os

# Set base path for database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'ims.db')
IMAGE_DIR = os.path.join(BASE_DIR, 'images')

class categoryManager:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ variables -------------
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        # Initialize the UI

        self.setup_ui()
        self.show()

     # Database helper function
    def execute_db_query(self, query, params=(), fetchall=False, fetchone=False):
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute(query, params)
                con.commit()
                if fetchall:
                    return cur.fetchall()
                if fetchone:
                    return cur.fetchone()
                
                con.commit()
                return True
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
            return None
            
    # UI setup function
    def setup_ui(self):
        #--------------- title ---------------------
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        lbl_name=Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,bg="lightyellow",font=("goudy old style",18)).place(x=50,y=170,width=300)
        btn_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)
        #------------ category details -------------
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)
        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)\
        # Refactored the column setup to be more dynamic and maintainable
        columns = {"cid": ("C ID", 90), "name": ("Name", 100)}
        self.CategoryTable=ttk.Treeview(cat_frame, columns=tuple(columns.keys()),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)

        self.CategoryTable["show"]="headings"
        for col_id, (col_text, col_width) in columns.items():
            self.CategoryTable.heading(col_id, text=col_text)
            self.CategoryTable.column(col_id, width=col_width)
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)
        #----------------- images --------------------- # Use Os path to load files
        try:
            self.im1=Image.open(os.path.join(IMAGE_DIR, "cat.jpg"))
            self.im1=self.im1.resize((500,250))
            self.im1=ImageTk.PhotoImage(self.im1)
            self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
            self.lbl_im1.place(x=50,y=220)

            self.im2=Image.open(os.path.join(IMAGE_DIR, "category.jpg"))
            self.im2=self.im2.resize((500,250))
            self.im2=ImageTk.PhotoImage(self.im2)
            self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
            self.lbl_im2.place(x=580,y=220)
        except Exception as ex:
            messagebox.showerror("Error",f"Error loading images: {str(ex)}")
#----------------------------------------------------------------------------------
    def add(self):
        if self.var_name.get()=="":
            messagebox.showerror("Error","Category Name must be required",parent=self.root)
            return
        
        row = self.execute_db_query("Select * from category where name=?",(self.var_name.get(),),fetchone=True)
        if row is not None:
            messagebox.showerror("Error","Category already present",parent=self.root)
            return
        
        success = self.execute_db_query("insert into category (name) values (?)",(self.var_name.get(),))
        if success:
            messagebox.showinfo("Success","Category added successfully",parent=self.root)
            self.clear()

    def show(self):
        rows = self.execute_db_query("select * from category", fetchall=True)
        if rows is not None:
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        
    def clear(self):
        self.var_name.set("")
        self.var_cat_id.set("")
        self.show()

    def get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        if row:
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])
    
    def delete(self):
        if self.var_cat_id.get()=="":
            messagebox.showerror("Error","Category name must be required",parent=self.root)
            return
        
        row = self.execute_db_query("Select * from category where cid=?",(self.var_cat_id.get(),),fetchone=True)
        if row is None:
            messagebox.showerror("Error","Invalid Category Name",parent=self.root)
            return
        
        op = messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
        if op:
            success = self.execute_db_query("delete from category where cid=?",(self.var_cat_id.get(),))
            if success:
                messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                self.clear()

if __name__=="__main__":
    root=Tk()
    obj=categoryManager(root)
    root.mainloop()