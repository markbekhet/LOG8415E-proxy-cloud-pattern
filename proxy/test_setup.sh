source ~/venv/bin/activate
cd proxy
python main.py "SELECT * FROM actor" >> ~/test_proxy.txt 
python main.py "INSERT INTO actor VALUES (201,'SYLVESTER','Stalone','2006-02-15 04:34:33')" >> ~/test_proxy.txt
python main.py "SELECT * FROM actor" >> ~/test_proxy.txt
python main.py "INSERT INTO actor VALUES (202,'Kevin','Hart','2006-02-15 04:34:33')" >> ~/test_proxy.txt
python main.py "SELECT * FROM actor" >> ~/test_proxy.txt
python main.py "INSERT INTO actor VALUES (203,'Dwayne','Jhonson','2006-02-15 04:34:33')" >> ~/test_proxy.txt
python main.py "SELECT * FROM actor" >> ~/test_proxy.txt
python main.py "INSERT INTO actor VALUES (204,'Bradly','Cooper','2006-02-15 04:34:33')" >> ~/test_proxy.txt
python main.py "SELECT * FROM actor"
deactivate