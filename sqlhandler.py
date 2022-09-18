import sqlite3
  
# database name to be passed as parameter
conn = sqlite3.connect('USER.db')
  
# delete student record from database
conn.execute("DELETE from Student where unix='B113058'")
conn.commit()
print("Total number of rows deleted :", conn.total_changes)
  
cursor = conn.execute("SELECT * FROM Student")
for row in cursor:
   print(row)
  
conn.close()