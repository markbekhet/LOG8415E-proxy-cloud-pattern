source ~/venv/bin/activate
cd proxy
python main.py random_hit "SELECT * FROM actor" >> ~/test_proxy.txt 
python main.py direct_hit "INSERT INTO actor VALUES (201,'SYLVESTER','Stalone','2006-02-15 04:34:33')" >> ~/test_proxy.txt
python main.py customized_hit "SELECT * FROM actor" >> ~/test_proxy.txt
python main.py direct_hit "INSERT INTO actor VALUES (202,'Kevin','Hart','2006-02-15 04:34:33')" >> ~/test_proxy.txt
python main.py random_hit "SELECT * FROM actor" >> ~/test_proxy.txt
python main.py direct_hit "INSERT INTO actor VALUES (203,'Dwayne','Jhonson','2006-02-15 04:34:33')" >> ~/test_proxy.txt
python main.py customized hit "SELECT * FROM actor" >> ~/test_proxy.txt
python main.py direct_hit "INSERT INTO actor VALUES (204,'Bradly','Cooper','2006-02-15 04:34:33')" >> ~/test_proxy.txt
python main.py customized_hit "SELECT * FROM actor"
deactivate