"""Seed file to make sample data for db"""

from models import User, Post, db, defaultImage
from app import app


#create all tables
db. drop_all()
db.create_all()


u1 = User(first_name='Arlo', last_name='Chung', image_URL='https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRJITJfzHfn8PlB2-Ib5-BRFAnsKDVPGmu8NfEfBZtqrXgyT0ucyWBsX1RxyaewJKzUKUxSG3Li9EMWSz4')
u2 = User(first_name='Tiger', last_name='Woods', image_URL='https://people.com/thmb/hHSAu0xge-G0C-lIQXoOy0LKz1M=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(716x479:718x481)/tiger-woods-2000-8f8344b29c26417ca9018f14fc2ca944.jpg')
u3 = User(first_name='Rory', last_name='Mcilroy', image_URL='https://www.telegraph.co.uk/content/dam/golf/2023/06/22/TELEMMGLPICT000340288681_16874632816550_trans_NvBQzQNjv4Bq_NJ62v2ZFDvrR1Z2dUS5zCutLnR8HK5Rupmihr5J0I4.jpeg')
u4 = User(first_name='Michael', last_name='Scott', image_URL='https://jeprades.github.io/michael-scott-tribute/images/michael-scott-header.png')

p1 = Post(title="My First Post", content="Hey all! I'm making my first post! I'm a bit nervous so be nice! :)", user_id='1')
p2 = Post(title="How I Manage", content="How I manage, by Michael Scott....", user_id='4')
p3 = Post(title="The Goat", content="So I think this Tiger guy is pretty good. Some say he's the GOAT", user_id='2')
p4 = Post(title="Business 101", content="Business by Michael Scott. Over 1 billion sold. The business man...", user_id='4')
p5 = Post(title="My Favourite Snacks", content="I basically like everything. Woof woof!", user_id='1')
p6 = Post(title="The Master is Rigged!", content="Pretty sure it's rigged. How does Patrick Reed win but not me!?", user_id='3')
p7 = Post(title="Woof Woof!", content="Woof woof woof!!!", user_id='1')



db.session.add_all([u1,u2,u3,u4])
db.session.add_all([p1,p2,p3,p4,p5,p6,p7])
db.session.commit()


