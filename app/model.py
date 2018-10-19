import sys
# sys.path.append('/home/foooooodie')

from app import db
from datetime import datetime
from flask_login import UserMixin

class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    
    def __repr__(self):
        return '<Category, id: %r, name: %r>' %(self.id, self.name)

class Food(db.Model):
    __tablename__ = 'Food'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    area = db.Column(db.Integer)
    price = db.Column(db.Float)
    maker_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    description = db.Column(db.String(3000))
    available_amount = db.Column(db.Integer)
    score = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'))
    image = db.Column(db.String(3000))
    
    def __repr__(self):
        return '<Food, id: %r, name: %r, area: %r, price: %r, maker_id: %r, description: %r, available_amount: %r, score: %r, category_id: %r, image: %r>' % (self.id, self.name, self.area, self.price, self.maker_id, self.description, self.available_amount, self.score, self.category_id, self.image)

class Friend(db.Model):
    __tablename__ = 'Friend'
    muser_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key = True)
    fuser_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key = True)
    
    def __repr__(self):
        return '<muser_id: %r, fuser_id: %r>' % (self.muser_id, self.fuser_id)
    
    


class Ingredient(db.Model):
    __tablename__ = 'Ingredient'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    
    def __repr__(self):
        return '<Ingredient, id: %r, name: %r>' %(self.id, self.name)

class Ingredient_Food(db.Model):
    __tablename__ = 'Ingredient_Food'
    ingre_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'), primary_key = True)
    ingre_amount = db.Column(db.Integer)
    food_id = db.Column(db.Integer, db.ForeignKey('Food.id'), primary_key = True)
    
    def __repr__(self):
        return '<Ingredient_Food, ingre_id: %r, ingre_amount: %r, food_id: %r>' %(self.ingre_id, self.ingre_amount, self.food_id)

class Orders(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key = True)
    seller_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    food_id = db.Column(db.Integer)
    food_amount = db.Column(db.Integer)
    food_score = db.Column(db.Float)
    note = db.Column(db.String(3000), default = "Write Pick up Time and Place Here")
    time = db.Column(db.DateTime(), default = datetime.now)
    seller_score = db.Column(db.Float)
    buyer_score = db.Column(db.Float)
    total_price = db.Column(db.Float)
    
    def __repr__(self):
        return '<Orders, id: %r, seller_id: %r, buyer_id: %r, food_id: %r, food_amount: %r, food_score: %r, note: %r, time: %r, seller_score: %r, buyer_score: %r, total_price: %r>' %(self.id, self.seller_id, self.buyer_id, self.food_id, self.food_amount, self.food_score, self.note, self.time, self.seller_score, self.buyer_score, self.total_price)

class Suborder(db.Model):
    __tablename__ = 'Suborder'
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('Food.id'))
    order_amount = db.Column(db.Integer)
    food_score = db.Column(db.Float)
    sub_price = db.Column(db.Float)
    
    def __repr__(self):
        return '<Suborder, id: %r, order_id: %r, food_id: %r, order_amount: %r, food_score: %r, sub_price: %r>' %(self.id, self.order_id, self.food_id, self.order_amount, self.food_score, self.sub_price)

class Preference(db.Model):
    __tablename__ = 'Preference'
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'), primary_key = True)
        
    def __repr__(self):
        return '<Preference, user_id: %r, category_id: %r>' %(self.user_id, self.category_id)

class Search_History(db.Model):
    __tablename__ = 'Search_History'
    user_id = db.Column(db.Integer, primary_key = True)
    search_1  = db.Column(db.String(300))
    search_2  = db.Column(db.String(300))
    search_3  = db.Column(db.String(300))
    
    def __repr__(self):
        return '<Search_History, user_id: %r, search_1: %r, search_2: %r, search_3: %r>' %(self.user_id, self.search_1, self.search_2, self.search_3)

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone_number  = db.Column(db.Integer, unique=True)
    address  = db.Column(db.String(100))
    gender = db.Column(db.Integer) # 0 or 1
    birth_year = db.Column(db.Integer)
    selling_score = db.Column(db.Float, default = 0)
    purchasing_score = db.Column(db.Float, default = 0)
    zipcode = db.Column(db.Integer)
    
    is_active = db.Column(db.Boolean, default = True)
    is_authenticated = db.Column(db.Boolean, default = True)
    is_anonymous = db.Column(db.Boolean, default = True)
    
    search_1 = db.Column(db.String(300))
    search_2 = db.Column(db.String(300))
    search_3 = db.Column(db.String(300))
    
    image = db.Column(db.String(300), default = "https://cdn.dribbble.com/users/22122/screenshots/1302117/foodie_d.png")
    
    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User, id: %r, name: %r, password_hash: %r, email: %r, phone_number: %r, address: %r, gender: %r, birth_year: %r, selling_score: %r, purchasing_score: %r, zipcode: %r, search_1: %r, search_2: %r, search_3: %r, image: %r>' %(self.id, self.name, self.password_hash, self.email, self.phone_number, self.address, self.gender, self.birth_year, self.selling_score, self.purchasing_score, self.zipcode, self.search_1, self.search_2, self.search_3, self.image)

#-------TEST---------
def Suborder_test():
    all_i = db.session.query(Suborder).all()
    for i in all_i:
        print(i)

def Order_test():
    all_i = db.session.query(Orders).all()
    for i in all_i:
        print(i)

def Ingre_Food_test():
    all_i = db.session.query(Ingredient_Food).all()
    for i in all_i:
        print(i)

def Ingre_test():
    all_i = db.session.query(Ingredient).all()
    for i in all_i:
        print(i)

def Food_test():
    all_f = db.session.query(Food).all()
    for f in all_f:
        print(f)

def Category_test():
    all_c = db.session.query(Category).all()
    for c in all_c:
        print(c)
    
    print("-----------------")
    new_c = Category(category_name = 'pasta')
    db.session.add(new_c)
    db.session.commit()
    print("-----------------")
    all_c = db.session.query(Category).all()
    for c in all_c:
        print(c)

def Preference_test():
    all_p = db.session.query(Preference).all()
    for p in all_p:
        print(p)
    print("-----------------")

    p = Preference(8, 7)
    db.session.add(p)
    db.session.commit()

    all_p = db.session.query(Preference).all()
    for p in all_p:
        print(p)

def User_test():
    all_users = db.session.query(User).all()
    for user in all_users:
        print(user)

def Search_History_test():
    all_hist = db.session.query(Search_History).all()
    for hist in all_hist:
        print(hist)
        
def Friend_test():
    all_friend_pair = db.session.query(Friend).all()
    for pair in all_friend_pair:
        print(hist)


if __name__ == '__main__':
    # print("nothing")
    db.create_all()
    # Suborder_test()
    # Order_test()
    # Ingre_Food_test()
    # Ingre_test()
    # Food_test()
    # Category_test()
    # Preference_test()
    User_test()