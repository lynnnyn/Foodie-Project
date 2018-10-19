from flask import Flask, request, redirect, url_for, render_template,flash,session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import numpy as np
# import sklearn
from scipy import spatial

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://foooooodie_hzong2:02!E-L!7mN5[@localhost/foooooodie_program'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hahaha_this_is_secret'
app.config['TESTING'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from app.model import *
#----CREATE_NEW_TABLES----
# db.create_all() 

# def Friend_test():
#     all_friend_pair = db.session.query(Friend).all()
#     for pair in all_friend_pair:
#         print(pair)

# Friend_test()


def make_list(input):
    ret = []
    for tuples in input:
        for t in tuples:
            ret.append(t)
    return ret

def process_dict(inputlist, attr):
    outputlist = []
    for i in inputlist:
        dict_list = dict(zip(attr, i))
        outputlist.append(dict_list)
    return outputlist

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    return current_user.name + " are now logged in."
   
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password_candidate = request.form['inputPassword']
        check = request.form.get('remember')
        remember = 0
        if check:
            remember = 1
        print(email, password_candidate, remember)
        user = db.session.query(User).filter_by(email = email, password_hash = password_candidate).first()
        print(user)
        if user:
            login_user(user)
            # return redirect(url_for('test'))
            print("this user exists!")
            print(current_user)
            return redirect(url_for('home'), code = 303)
        else:
            flash("Email or Password is wrong.")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are now logged out.")
    return render_template('login.html')
                
@app.route('/register', methods=['GET', "POST"])
def register():
 sql_all = 'SELECT DISTINCT name FROM Category'
 all_cate = make_list(db.session.execute(sql_all).fetchall())
 
 if request.method == 'POST':
     print("POST")
     # Get from fields
     inputEmail             = request.form['inputEmail']
     inputUsername          = request.form['inputUsername']
     inputPassword          = request.form['inputPassword']
     # ------- PASSWORD CHECK -------------------------------
     #-------- AFTER MID-DEMO -------------------------------
     inputPasswordConfirmed = request.form['inputPasswordConfirmed'] 
     inputPhoneNumber       = request.form['inputPhoneNumber']
     inputAddress           = request.form['inputAddress']
     inputPostcode          = request.form['inputPostcode']
   
     male                   = request.form.get('male')
     female                 = request.form.get('female')
     inputbirthYear         = request.form['birthYear']

     print(inputEmail            )
     print(inputUsername         )
     print(inputPassword         )
     print(inputPasswordConfirmed)
     print(inputPhoneNumber      )
     print(inputAddress          )
     print(inputPostcode         )
     print(male                  )
     print(female                )
     print(inputbirthYear        )
     

     #-------- CHECK EXISTED EMAIL OR PHONE_NUMBER ----------
     #-------- AFTER MID-DEMO -------------------------------
     inputGender = 0
     if male:
         inputGender = 1
     new_user = User(email = inputEmail, name = inputUsername, password_hash = inputPassword, phone_number = inputPhoneNumber, address  = inputAddress, zipcode = inputPostcode, gender = inputGender, birth_year = inputbirthYear) 
     db.session.add(new_user)
     db.session.commit()
     user = db.session.query(User).filter_by(email = inputEmail).first()
     i = 0
     for cate in all_cate:
         i += 1
         if request.form.get(cate):
             new_pref = Preference(user_id = user.id, category_id = i)
             db.session.add(new_pref)
             db.session.commit()
     login_user(user)
     return redirect(url_for('home'), code = 303)

 return render_template('register.html', preferred_cate = all_cate)


attr_food = ('id', 'name', 'area', 'price', 'maker_id', 'description', 'available_amount', 'score', 'category_id','image')
attr_search = ('id','name', 'area', 'price', 'description', 'available_amount', 'score', 'AVG_PRICE', 'AVG_SCORE', 'seller_score','image')
attr_friend = ('id','name','email','phone_number','address','gender','birth_year','selling_score','purchasing_score', 'image')
attr_friendprefer = ('id','name')


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_id = current_user.id
    
    if request.method == "POST":

        inputSearch = request.form["search"]

        curr_user = db.session.query(User).filter(User.id == user_id).first()
        curr_user.search_3 = curr_user.search_2
        curr_user.search_2 = curr_user.search_1
        curr_user.search_1 = inputSearch
        db.session.commit()
        return redirect(url_for('search', search=inputSearch))

    elif request.method == 'GET':

        def make_list(input):
            ret = []
            for tuples in input:
                for t in tuples:
                    ret.append(t)
            return ret

        def make_list_2(input, user_number):
            re = []
            for i in range(user_number):
                re.append([t[1] for t in input if t[0] is i + 1])
            return re

        # user   = 'hzong2'
        user = current_user.name
        print('---------------------------------------------------')
        print(user)
        # print('\u2019')

       
        
        sql_user = 'SELECT gender, birth_year, zipcode FROM User'
        sql_order = 'SELECT id FROM Orders'
        all_users = db.session.execute(sql_user).fetchall()
        all_orders = db.session.execute(sql_order).fetchall()
        user_oder = db.session.execute('SELECT buyer_id, GROUP_CONCAT(id) FROM Orders GROUP BY buyer_id').fetchall()
        user_array = np.array(all_users)
        order = sorted(make_list(all_orders))
        # print(order)
        # print(user_oder)
        user_number = np.shape(user_array)[0]
        p = make_list_2(user_oder, user_number)
        p2 = []
        for i in p:
            if i == []:
                p2.append([])
            elif i != []:
                for j in i:
                    p2.append(j.split(','))

        def order_list(user, order):
            o1 = []
            for i in order:
                if str(i) in user:
                    o1.append(1)
                else:
                    o1.append(0)
            return o1

        px = []

        for i in p2:
            px.append(order_list(i, order))
        order_array = np.array(px)

        # print(px)
        # print(order_array)

        def scale(input):
            out = (input - input.min()) / (input.max() - input.min())
            return out

        user_matrix = np.hstack((scale(user_array), px))

        def similar_user(user_id, user_matrix=user_matrix):
            """
            calculate similarity based on cosine distance
            :param user_id:
            :param user_matrix:
            :return: list of user_id, ranked by similarity
            """
            dis_list = []
            for i in range(len(user_matrix)):
                dis_list.append(1 - spatial.distance.cosine(user_matrix[user_id - 1], user_matrix[i]))
            # print(dis_list)
            recommend_list = [i + 1 for i in np.argsort(-np.array(dis_list)) if i != user_id - 1]
            # recommend_list = [user_id]
            return recommend_list

        # print(similar_user(current_user.id))  # to test similar user

        similar_id = (similar_user(current_user.id)[0],similar_user(current_user.id)[1],similar_user(current_user.id)[2])
        
        sql_nearby = 'SELECT Food.* FROM Food LEFT JOIN User ON Food.area = User.zipcode WHERE Food.available_amount > 0 AND User.name = "%s" LIMIT 9' % user
        
        similar_userid = int(similar_user(current_user.id)[0])
        
        sql_searchhis = 'SELECT User.search_1,User.search_2,User.search_3 FROM User WHERE User.id = %d' %current_user.id
        searchhis_list = db.session.execute(sql_searchhis).fetchall()
        search1 = searchhis_list[0][0]
        search2 = searchhis_list[0][1]
        search3 = searchhis_list[0][2]
        print(search1)

        # sql_prefer = '(SELECT DISTINCT Food.* FROM Food, Food_Category WHERE Food_Category.food_id = Food.id AND Food_Category.category_id IN (SELECT DISTINCT Food_Category.category_id FROM Food_Category, Orders LEFT JOIN User ON Orders.buyer_id = User.id LEFT JOIN Food ON Food.id = Orders.food_id WHERE User.name = "%s" AND Food_Category.food_id = Food.id)) UNION (SELECT DISTINCT Food.* FROM Food,Food_Category WHERE Food.id = Food_Category.food_id AND Food_Category.category_id IN( SELECT DISTINCT Food_Category.category_id FROM Food_Category,User,Preference,Food WHERE Food.available_amount > 0 AND User.id = Preference.user_id AND Food_Category.category_id = Preference.category_id AND User.id = Preference.user_id AND Food_Category.food_id = Food.id AND User.name = "%s" AND User.zipcode = Food.area)) UNION (SELECT DISTINCT Food.* FROM Food,Orders,User WHERE Orders.food_id = Food.id AND User.id = Orders.buyer_id AND User.id = %d AND Food.id NOT IN (SELECT Food.id FROM Food,Orders,User WHERE Orders.food_id = Food.id AND User.id = Orders.buyer_id AND User.name = "%s")) LIMIT 9' %(user,user,similar_userid, user)
        
        sql_prefer = '(SELECT DISTINCT Food.* FROM Food, Food_Category,Orders,User WHERE (Food_Category.food_id = Food.id AND Food_Category.category_id IN (SELECT DISTINCT Food_Category.category_id FROM Food_Category, Orders LEFT JOIN User ON Orders.buyer_id = User.id LEFT JOIN Food ON Food.id = Orders.food_id WHERE User.name = "%s" AND Food_Category.food_id = Food.id)) OR (Food.id = Food_Category.food_id AND Food_Category.category_id IN( SELECT DISTINCT Food_Category.category_id FROM Food_Category,User,Preference,Food WHERE Food.available_amount > 0 AND User.id = Preference.user_id AND Food_Category.category_id = Preference.category_id AND User.id = Preference.user_id AND Food_Category.food_id = Food.id AND User.name = "%s" AND User.zipcode = Food.area)) OR (Orders.food_id = Food.id AND User.id = Orders.buyer_id AND User.id = %d AND Food.id NOT IN (SELECT Food.id FROM Food,Orders,User WHERE Orders.food_id = Food.id AND User.id = Orders.buyer_id AND User.name = "%s")) OR(Food.name LIKE "%%%s%%" OR Food.name LIKE "%%%s%%" OR Food.name LIKE "%%%s%%")) ORDER BY Food.score DESC LIMIT 9' %(user,user,similar_userid, user, search1, search2,search3)

        nearby_list = db.session.execute(sql_nearby).fetchall()
        prefer_list = db.session.execute(sql_prefer).fetchall()
        nearby_l    = process_dict(nearby_list, attr_food)
        prefer_l    = process_dict(prefer_list, attr_food)
        
        
        sql_similaruser  = 'SELECT User.id,User.name,User.email,User.phone_number,User.address,User.gender,User.birth_year,User.selling_score,User.purchasing_score, User.image FROM User WHERE User.id IN %s' % (similar_id,)
        similaruser_list = db.session.execute(sql_similaruser).fetchall()
        similaruser_l    = process_dict(similaruser_list, attr_friend)
        # print(similaruser_l)
        


    # return render_template('home.html', nearby = nearby_l, recommendation = prefer_l,search = {})
    return render_template('home.html', nearby=nearby_l, recommendation=prefer_l, search={},users = similaruser_l)


@app.route('/search',methods=['GET','POST'])
def search():
    user_id = current_user.id
    search_key= 'none'
    if request.method == "GET":
        search_key = request.args["search"]
        sql_search = '(SELECT DISTINCT Food.id, Food.name,Food.area,Food.price,Food.description,Food.available_amount,Food.score,AVG_PRICE,AVG_SCORE,User.selling_score,Food.image FROM Food LEFT JOIN(SELECT Food.name, Food.area ,AVG(Food.price) AS AVG_PRICE,AVG(Food.score) AS AVG_SCORE FROM Food GROUP BY Food.name, Food.area) NEW_FOOD ON Food.name = NEW_FOOD.name AND Food.area = NEW_FOOD.area LEFT JOIN User ON Food.maker_id = User.id LEFT JOIN Food_Category ON Food.id = Food_Category.food_id LEFT JOIN Category ON Food_Category.category_id = Category.id WHERE Food.available_amount > 0 AND (Food.name LIKE "%%%s%%" OR Category.name LIKE "%%%s%%" OR User.name LIKE "%%%s%%" OR Food.area = "%s") ORDER BY Food.score DESC,Food.price,User.selling_score DESC,Food.available_amount DESC)' %(search_key,search_key,search_key,search_key)
        print(sql_search)
        search_list = db.session.execute(sql_search).fetchall()
        search_l = process_dict(search_list, attr_search)
        print("/search:",search_l)
        
        condition = {
            'FoodScore': None, 
            'PriceLow': None, 
            'PriceHigh': None, 
            'SellerScore': None, 
            'SellingAmountLow': None, 
            'SellingAmountHigh': None, 
            'filterPriceLow': '', 
            'filterPriceHigh': '', 
            'filterFoodScoreLow': '', 
            'filterFoodScoreHigh': '', 
            'filterSellerScoreLow': '', 
            'filterSellerScoreHigh': '', 
            'filterAmountLow': '', 
            'filterAmountHigh': ''
        }
        
        return render_template('search.html', search_key=search_key,search_results=search_l, condition = condition)
        # 1. pass searchkey to front end
        #2. render template "search.html"
        
        

    if request.method == "POST":
        print('---------------POST---------------')
        # data = request.form
        search_key = request.form["search"]

        curr_user = db.session.query(User).filter(User.id == user_id).first()
        curr_user.search_3 = curr_user.search_2
        curr_user.search_2 = curr_user.search_1
        curr_user.search_1 = search_key
        db.session.commit()

        
        inputFoodScore = request.form.get("FoodScore")
        inputPriceLow = request.form.get("PriceLow")
        inputPriceHigh = request.form.get("PriceHigh")
        inputSellerScore = request.form.get("SellerScore")
        inputSellingAmountLow = request.form.get("SellingAmountLow")
        inputSellingAmountHigh = request.form.get("SellingAmountHigh")

        inputFilterPriceLow = request.form["filterPriceLow"]
        inputFilterPriceHigh = request.form["filterPriceHigh"]
        inputFilterFoodScoreLow = request.form["filterFoodScoreLow"]
        inputFilterFoodScoreHigh = request.form["filterFoodScoreHigh"]
        inputFilterSellerScoreLow = request.form["filterSellerScoreLow"]
        inputFilterSellerScoreHigh = request.form["filterSellerScoreHigh"]
        inputFilterAmountLow = request.form["filterAmountLow"]
        inputFilterAmountHigh = request.form["filterAmountHigh"]

        condition = {
            "FoodScore": inputFoodScore,
            "PriceLow": inputPriceLow,
            "PriceHigh": inputPriceHigh,
            "SellerScore": inputSellerScore,
            "SellingAmountLow": inputSellingAmountLow,
            "SellingAmountHigh": inputSellingAmountHigh,
            "filterPriceLow": inputFilterPriceLow,
            "filterPriceHigh": inputFilterPriceHigh,
            "filterFoodScoreLow": inputFilterFoodScoreLow,
            "filterFoodScoreHigh": inputFilterFoodScoreHigh,
            "filterSellerScoreLow": inputFilterSellerScoreLow,
            "filterSellerScoreHigh": inputFilterSellerScoreHigh,
            "filterAmountLow": inputFilterAmountLow,
            "filterAmountHigh": inputFilterAmountHigh
        }
        print(condition)
        
        print("search filter ------------------------------>")
        print("search filter ------------------------------>")
        print(search_key)
        print(inputFoodScore)
        print(inputPriceLow)
        print(inputPriceHigh)
        print(inputSellerScore)
        print(inputSellingAmountLow)
        print(inputSellingAmountHigh)
        print(inputFilterPriceLow)
        print(inputFilterPriceHigh)
        print(inputFilterFoodScoreLow)
        print(inputFilterFoodScoreHigh)
        print(inputFilterSellerScoreLow)
        print(inputFilterSellerScoreHigh)
        print(inputFilterAmountLow)
        print(inputFilterAmountHigh)

        food_score_select = ''
        food_price_select = ''
        seller_score_select = ''
        amount_select = ''

        if inputFoodScore:
            food_score_select = 'descent'

        if inputPriceLow:
            food_price_select = 'ascent'
        elif inputPriceHigh:
            food_price_select = 'descent'

        if inputSellerScore:
            seller_score_select = 'descent'

        if inputSellingAmountLow:
            amount_select = 'ascent'
        elif inputFilterAmountHigh:
            amount_select = 'descent'

        result = {
            "search": search_key,
            "Food.score": {
                "select": food_score_select,
                "low": inputFilterFoodScoreLow,
                "high": inputFilterFoodScoreHigh,
            },
            "Food.price": {
                "select": food_price_select,
                "low": inputFilterPriceLow,
                "high": inputFilterPriceHigh,
            },

            "User.selling_score": {
                "select": seller_score_select,
                "low": inputFilterSellerScoreLow,
                "high": inputFilterSellerScoreHigh,
            },
            "Food.available_amount": {
                "select": amount_select,
                "low": inputFilterAmountLow,
                "high": inputFilterAmountHigh,
            }
        }

        

        sort = ''
        where = ''
        for attr in result:
            if attr == 'search':
                continue
            # print('attr',attr)
            # print('result[attr]',result[attr])
            # print(result[attr]['select'])
            if result[attr]['select'] == 'descent':
                sort = sort + attr + ' ' + 'DESC,'
            elif result[attr]['select'] == 'ascent':
                sort = sort + ' ' + attr + ','

            if result[attr]['low'] != '':
                # print('result[attr][low]',result[attr]['low'])
                where = where + ' ' + 'AND' + ' ' + attr + ">" + result[attr]['low']

            if result[attr]['high'] != '':
                # print('result[attr][high]',result[attr]['high'])
                where = where + ' ' + 'AND' + ' ' + attr + "<" + result[attr]['high']

        if sort == '':
            sort = 'Food.score DESC,Food.price,User.selling_score DESC,Food.available_amount DESC,'

        search = result['search']
        sort = sort[:-1]
        # print(search)
        # print(sort)
        # print('where:', where)


        sql_search = '(SELECT DISTINCT Food.id,Food.name,Food.area,Food.price,Food.description,Food.available_amount,Food.score,AVG_PRICE,AVG_SCORE,User.selling_score,Food.image FROM Food LEFT JOIN(SELECT Food.name, Food.area ,AVG(Food.price) AS AVG_PRICE,AVG(Food.score) AS AVG_SCORE FROM Food GROUP BY Food.name, Food.area) NEW_FOOD ON Food.name = NEW_FOOD.name AND Food.area = NEW_FOOD.area LEFT JOIN User ON Food.maker_id = User.id LEFT JOIN Food_Category ON Food.id = Food_Category.food_id LEFT JOIN Category ON Food_Category.category_id = Category.id WHERE Food.available_amount > 0 AND (Food.name LIKE "%%%s%%" OR Category.name LIKE "%%%s%%" OR User.name LIKE "%%%s%%" OR Food.area = "%s") %s ORDER BY %s)' %(search_key,search_key,search_key,search_key,where,sort)
        search_list = db.session.execute(sql_search).fetchall()
        search_l = process_dict(search_list, attr_search)
        print(sql_search)
        print(search_l)

        return render_template('search.html',search_key=search_key, search_results=search_l, condition = condition)



@app.route('/profile', methods=['GET', "POST"])
@login_required
def profile():
    user_name = current_user.name
    attr_food = ('id', 'name', 'area', 'price', 'maker_id', 'description', 'available_amount', 'score', 'category_id', 'image')
    attr_order = ('seller_name', 'seller_phone','order_time', 'food_name','food_amount', 'price', 'note')
    attr_orderid = ('buyer_name', 'buyer_phone','order_time', 'food_name', 'order_id','food_amount', 'price', 'note')
    attr_user = ('name', 'id', 'address', 'phone_number',
        'gender', 'zipcode')
    
    def make_list(input):
        ret = []
        for tuples in input:
            for t in tuples:
                ret.append(t)
        return ret
    
    # def process_dict(inputlist, attr):
    #     outputlist = []
    #     for i in inputlist:
    #         dict_list = dict(zip(attr, i))
    #         outputlist.append(dict_list)
    #     return outputlist
    
    if request.method == 'GET':
        # Get from fields
        # address = request.form['address']
        
        user_id = current_user.id

        sql_user = 'SELECT name FROM Preference, Category WHERE user_id = "%s" AND Category.id = Preference.category_id' % user_id
        sql_all = 'SELECT DISTINCT name FROM Category'
        sql_maker = 'SELECT * FROM `Food` WHERE Food.maker_id = (SELECT User.id FROM User WHERE User.name = "%s") LIMIT 3' % user_name

        use_preference = make_list(db.session.execute(sql_user).fetchall())
        all_preference = make_list(db.session. execute(sql_all).fetchall())
        maker_list     = db.session.execute(sql_maker).fetchall()
        maker_l        = process_dict(maker_list, attr_food)
        # print(maker_l)


        preference_dict = {}
        for category in all_preference:
            if category in use_preference:
                preference_dict[category] = True
            else:
                preference_dict[category] = False
        print(preference_dict)        
        # sql_info = 'SELECT * FROM User WHERE user_id = %d' %user_id
        info_dict = {'name': current_user.name, 'id': current_user.id, 'address': current_user.address, 'phone_number':current_user.phone_number,
        'gender': current_user.gender, 'zipcode': current_user.zipcode, 'image': current_user.image}
        
        # print(info_dict, preference_dict) # test
        # print("----this is info----")
        # print(info_dict)
        
    
        previous_order = db.session.query(Orders, User, Food).filter(Orders.buyer_id == user_id).filter(Orders.food_id == Food.id).filter(Orders.seller_id == User.id).with_entities(User.name ,User.phone_number, Orders.time, Food.name, Orders.food_amount, Orders.total_price, Orders.note).order_by(Orders.time).all()
        
        previous_orderid = db.session.query(Orders, User, Food).filter(Orders.seller_id == user_id).filter(Orders.food_id == Food.id).filter(Orders.buyer_id == User.id).with_entities(User.name ,User.phone_number, Orders.time, Food.name, Orders.id, Orders.food_amount, Orders.total_price, Orders.note).order_by(Orders.time).all()        

        order_list = process_dict(previous_order, attr_order)
        selling_orders = process_dict(previous_orderid, attr_orderid)
    
        # print(len(order_list))
        # for i in range(len(selling_orders)):
        #     print(selling_orders[i])
            
        # selling_orders = []
        return render_template('profile.html', info = info_dict, preferred_cate = preference_dict, maker = maker_l, order_list=order_list, selling_orders=selling_orders)
        
@app.route('/note', methods = ['POST'])
def note():
    new_note = request.form['newNote']
    order_id = request.form['order_id']
    print("new_note: ", new_note)
    print("order_id: ", order_id)
    order = db.session.query(Orders).get(int(order_id))
    order.note = new_note
    db.session.commit()
    return redirect(url_for("profile"))

    
@app.route('/category', methods=['GET', "POST"])
def category():
    def make_list(input):
        ret = []
        for tuples in input:
            for t in tuples:
                ret.append(t)
        return ret    
    if request.method == 'POST':
        print("POST")
        print(request.form)
    # Get from fields
        user_id = current_user.id
        sql_user = 'SELECT name FROM Preference, Category WHERE user_id = "%d" AND Category.id = Preference.category_id' %user_id
        sql_all = 'SELECT DISTINCT name FROM Category'
        use_preference = make_list(db.session.execute(sql_user).fetchall())
        all_preference = make_list(db.session.execute(sql_all).fetchall())
        preference_dict = {}
        for category in all_preference:
            if category in use_preference:
                preference_dict[category] = True
            else:
                preference_dict[category] = False
        current_prefer = {}
        # for category in all_preference:
        #     if request.form[category] == 'true':
        #         current_prefer[category] =  True
        #     elif request.form[category] == 'false':
        #         current_prefer[category] =  False
        
        for category in all_preference:
            # print('cat', request.form.get(category))
            if request.form.get(category) == 'on':
                # print('cat', request.form.get(category))
                # print("here",request.form.get(category))
                current_prefer[category] =  True
            else:
                current_prefer[category] =  False

        print('current prefer', current_prefer)
        print('preference_dict', preference_dict)
        user = db.session.query(User).get(int(user_id))
  
        for category in all_preference:
            if preference_dict[category] is True and current_prefer[category] is False:
                delete_sql = 'SELECT id FROM Category WHERE name = "%s"' %category
                category_id = make_list(db.session.execute(delete_sql).fetchall())[0]
                del_sql = 'DELETE FROM Preference WHERE user_id = %d AND category_id = %d' %(user_id, category_id)

                db.engine.execute(del_sql)

            if preference_dict[category] is False and  current_prefer[category] is True:
                sql = 'SELECT id FROM Category WHERE name = "%s"' %category
                category_id = make_list(db.session.execute(sql).fetchall())[0]
                print('POST CATEGORY')
                print(user_id, category_id)
                new_prefer = Preference(user_id = user_id, category_id = category_id)
                db.session.add(new_prefer)
                db.session.commit()
        
        # return render_template('profile.html', preferred_cate = preference_dict)
        return redirect(url_for("profile"))

@app.route('/description', methods=['POST'])
def description():
    description = request.form["newDescription"]
    food_id = request.form['food_id']
    food = db.session.query(Food).get(int(food_id))
    food.description = description
    db.session.commit()
    return redirect(url_for("foodProfile", food_id = food_id))


@app.route('/myfriends', methods=['POST', 'GET'])
def myfriends():
    user_id = current_user.id
    
    if request.method == 'GET':
        sql_friendlist = 'SELECT User.id,User.name,User.email,User.phone_number,User.address,User.gender,User.birth_year,User.selling_score,User.purchasing_score, User.image FROM User WHERE User.id IN( SELECT DISTINCT Friend.fuser_id FROM Friend,User WHERE Friend.muser_id = User.id  AND Friend.muser_id = "%s")' % user_id
        sql_friendfood = 'SELECT * FROM Food WHERE Food.maker_id IN (SELECT Friend.fuser_id FROM Friend WHERE Friend.muser_id = "%s")' %user_id
        myfriendlist_list = db.session.execute(sql_friendlist).fetchall()
        friendfood_list = db.session.execute(sql_friendfood).fetchall()
        myfriendlist_l = process_dict(myfriendlist_list, attr_friend)
        friendfood_l = process_dict(friendfood_list, attr_food)
        # print(myfriend_l)

    info_dict = {'name': current_user.name, 'id': current_user.id, 'address': current_user.address, 'phone_number':current_user.phone_number,
        'gender': current_user.gender, 'zipcode': current_user.zipcode, 'image': current_user.image}
        
    return render_template('myfriends.html', myfriends = myfriendlist_l,friendfood = friendfood_l, info = info_dict)    
    
@app.route('/friend/<user_id>',  methods=['POST','GET'])   
def friendProfile(user_id):
    print("current_user:",current_user.id)
    print('user_id',user_id)
    friendlist = []
    sql_friend = db.session.query(User).filter(User.id == user_id).with_entities(User.id,User.name,User.email,User.phone_number,User.address,User.gender,User.birth_year,User.selling_score,User.purchasing_score, User.image).all()
    info = process_dict(sql_friend, attr_friend)
    print(info)
    sql_friendlist = 'SELECT User.id FROM User WHERE User.id IN( SELECT DISTINCT Friend.fuser_id FROM Friend,User WHERE Friend.muser_id = User.id  AND Friend.muser_id = "%s")' % current_user.id
    myfriendlist_list = db.session.execute(sql_friendlist).fetchall()

    for friend in range(len(myfriendlist_list)):
        friendlist.append(str(myfriendlist_list[friend][0]))

    if user_id in friendlist:
        if_friend = True
    else:
        if_friend = False
    
    print(if_friend)
    

    sql_friendfood = db.session.query(Food).filter(Food.maker_id == user_id).with_entities(Food.id ,Food.name, Food.area, Food.price, Food.maker_id, Food.description, Food.available_amount, Food.score, Food.category_id, Food.image).all()
    friendfood_l = process_dict(sql_friendfood, attr_food)
    # print(all_my_food)
    sql_friendprefer = 'SELECT * FROM Category WHERE Category.id IN (SELECT DISTINCT Preference.category_id FROM User LEFT JOIN Preference ON User.id = Preference.user_id WHERE User.id = "%s")' % user_id
    friendprefer_list = db.session.execute(sql_friendprefer).fetchall()
    friendprefer_l = process_dict(friendprefer_list,attr_friendprefer)
    # print(all_my_food)
    # print(friendfood_l)
    # print(friendprefer_l[0])
    
    if request.method == 'POST' and if_friend == False:
        new_friend = Friend(muser_id = current_user.id, fuser_id = user_id)
        db.session.add(new_friend)
        db.session.commit()
        return redirect(url_for("friendProfile", user_id = user_id))
        
    if request.method == 'POST' and if_friend == True:
        # new_friend = db.session.query(Friend).filter(Friend.muser_id == current_user.id).filter(Friend.fuser_id == user_id).with_entities(Friend.muser_id,Friend.fuser_id).all()
        new_friend = 'DELETE FROM Friend WHERE Friend.muser_id = %d and Friend.fuser_id = "%s"'%(current_user.id,user_id)
        print(new_friend)
        db.engine.execute(new_friend) 

        return redirect(url_for("friendProfile",user_id = user_id))
    
    
    # if request.method == 'POST':
    #     if if_friend == False:
    #         new_friend = Friend(muser_id = current_user.id, fuser_id = user_id)
    #         db.session.add(new_friend)
    #         db.session.commit()
    #     elif if_friend == True:
    #         del_friend = 'DELETE FROM Friend WHERE Friend.muser_id = %d and Friend.fuser_id = "%s"'%(current_user.id,user_id)
    #         print(del_friend)
    #         db.engine.execute(del_friend) 
    #     return redirect(url_for(friendProfile,user_id = user_id))
    
    
    return render_template('friend_profile.html',info=info[0],foods = friendfood_l,friendprefer = friendprefer_l, friend_id = user_id,is_friend = if_friend)
    
@app.route('/food/<food_id>',  methods=['POST','GET'])   
def foodProfile(food_id):
    # food
    print(food_id)
    attr_food   = ('id','name', 'area', 'price', 'maker_id', 'description', 'available_amount', 'score', 'category_id', 'image', 'maker_name', 'selling_score')
    info = db.session.query(Food).filter(Food.id == food_id).filter(Food.maker_id==User.id).with_entities(Food.id ,Food.name, Food.area, Food.price, Food.maker_id, Food.description, Food.available_amount, Food.score, Food.category_id, Food.image, User.name, User.selling_score).all()
    food = process_dict(info, attr_food)
    food[0]['score'] = float(food[0]['score'])
    print(food[0])
    
    # orders
    attr_order = ('buyer_id', 'buyer_name', 'buyer_phone','order_id', 'order_time', 'food_id', 'food_amount', 'price', 'note', 'buyer_score')
    user_id = current_user.id
    previous_order = db.session.query(Orders).filter(Orders.food_id == food_id).filter(Orders.buyer_id==User.id).with_entities(User.id, User.name, User.phone_number, Orders.id, Orders.time, Orders.food_id, Orders.food_amount, Orders.total_price, Orders.note, Orders.buyer_score).all()
    order_list = process_dict(previous_order, attr_order)
    print(order_list)
    
    if request.method == 'POST':
        order_amount = int(request.form['amount'])
        
        if order_amount > food[0]['available_amount']:
            return 'error!'
            
        note = 'The maker hasn\'t left any notes yet...'
        food_price = float(food[0]['price'])
        food_score = float(food[0]['score'])
        seller_score = float(food[0]['selling_score'])
        buyer_score = current_user.purchasing_score
        seller_id = food[0]['maker_id']
        
        new_oder = Orders(buyer_id = user_id, seller_id = seller_id, food_id = food_id, food_score = food_score, food_amount = order_amount, note = note, seller_score = seller_score, buyer_score = buyer_score, total_price = food_price * order_amount)
        
        db.session.add(new_oder)
        db.session.commit()
        # update availible amount
        new_food = db.session.query(Food).get(int(food_id))
        new_food.available_amount = new_food.available_amount - order_amount
        db.session.commit()
        
        return redirect(url_for("profile"))
        
    
    return render_template('food_profile.html',food=food[0], orders=order_list, current_user=user_id)
    
    
@app.route('/myfood', methods=['POST','GET'])
def myfood():
    user_id = current_user.id
    attr_food   = ('id','name', 'area', 'price', 'maker_id', 'description', 'available_amount', 'score', 'category_id', 'image')
    all_my_food = db.session.query(Food).filter(Food.maker_id == user_id).with_entities(Food.id ,Food.name, Food.area, Food.price, Food.maker_id, Food.description, Food.available_amount, Food.score, Food.category_id, Food.image).all()
    # print(all_my_food)
    myfood = process_dict(all_my_food, attr_food)
    
   
    # return "hi food"
    return render_template('myfood.html',myfood=myfood)
    
@app.route('/order', methods=['POST','GET'])
def order():
    user_id = current_user.id
    if request.method == 'POST':
        # add order
        return "add order"
    else:
        return "add order page"
    
    
    
   
    # return "hi food"
    return render_template('myfood.html',myfood=myfood)



if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True) # Debug true for development purpose.
