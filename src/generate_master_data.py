from pathlib import Path
import csv, random
from faker import Faker

root=Path(__file__).resolve().parents[1]
(root/'data').mkdir(exist_ok=True)
f=Faker('en_IN')
regions=['North','South','East','West']
with open(root/'data/stores.csv','w',newline='',encoding='utf8') as out:
    w=csv.writer(out); w.writerow(['store_id','store_name','region','manager_name'])
    for i in range(1,21): w.writerow([i,f'Store-{i:02d}',regions[(i-1)%4],f.name()])
with open(root/'data/products.csv','w',newline='',encoding='utf8') as out:
    w=csv.writer(out); w.writerow(['product_id','product_name','category','brand','unit_cost'])
    cats=['Electronics','Grocery','Home','Beauty','Sports']
    for i in range(1,101): w.writerow([i,f'Product-{i:03d}',random.choice(cats),random.choice(['Nova','Urban','Prime','Daily']),round(random.uniform(30,1200),2)])
with open(root/'data/customers.csv','w',newline='',encoding='utf8') as out:
    w=csv.writer(out); w.writerow(['customer_id','customer_name','email','city'])
    for i in range(1,1001): w.writerow([i,f.name(),f'{f.user_name()}@example.com',f.city()])
print('Generated stores.csv, products.csv and customers.csv')
