import streamlit as st
import time
import mysql.connector
import pandas as pd




def add_review(mydb):

    sql=""
    form = st.form("review form")
    email=form.text_input("enter email")
    match=form.text_input("enter match number")
    rank = form.slider("rank the match" ,0,10,5)
    review=form.text_input("enter match review")
    if form.form_submit_button("Submit"):
        sql= """
        INSERT INTO reviewings VALUES (\""""+email+"""\", """+match+ """, """+str(rank)+""",\""""+review+"""\" );
        """
        mycursor = mydb.cursor()
        mycursor.execute(sql)


    return 

def add_user(mydb):

    sql=""
    form = st.form("user form")
    username=form.text_input("enter username")
    email=form.text_input("enter email")

    gender=form.selectbox('gender', (   'm', 'f'))
    team=form.text_input("enter favorite team")
    age = form.slider("enter age" ,0,99,20)
    if form.form_submit_button("Submit"):
        sql= """
        INSERT INTO fan VALUES (\""""+email+"""\", \""""+username+ """\", \'"""+gender+"""\',"""+str(age)+""",\""""+team+"""\" );
        """
        mycursor = mydb.cursor()
        mycursor.execute(sql)


    return 

def query_clubs(mydb):

    sql=""

    navigator=st.selectbox('Search by', (   'club name',
                                            #'city', 
                                            'home stadium', 
                                            'top 10 matches won',# neads to change db format
                                            'top 10 home matches won',# neads to change db format
                                            'top 10 # of yellow cards', 
                                            'top 10 # of red cards',
                                            'top 10 # of shots',
                                            'top 10 # of goals',
                                            ))



    if (navigator== 'club name'):
        input_club=st.text_input("enter name")
        sql = """
        Select Distinct * 
        FROM clubs 
        where name Like \"%"""+input_club+"""%\"
        """ 

    if (navigator== 'home stadium'):
        input_club=st.text_input("enter stadium")
        sql = """
        Select Distinct * 
        FROM clubs 
        where home_stadium_name Like \"%"""+input_club+"""%\"
        """ 

    elif (navigator== 'top 10 # of yellow cards'):
        sql = """
        Select name, SUM(
        CASE 
        WHEN c.name=a.home_club_name THEN a.home_yellow_cards
        WHEN c.name=a.away_club_name THEN a.away_yellow_cards
        ELSE 0 END
        ) FROM clubs c INNER JOIN attend a
        ON (c.name = a.home_club_name OR c.name = a.away_club_name)
        GROUP BY name
        ORDER BY 2 DESC 
        LIMIT 10;   
        """ 

    elif (navigator== 'top 10 # of red cards'):
        sql = """
        Select name, SUM(
        CASE 
        WHEN c.name=a.home_club_name THEN a.home_red_cards
        WHEN c.name=a.away_club_name THEN a.away_red_cards
        ELSE 0 END
        ) FROM clubs c INNER JOIN attend a
        ON (c.name = a.home_club_name OR c.name = a.away_club_name)
        GROUP BY name
        ORDER BY 2 DESC 
        LIMIT 10;   
        """ 

    elif (navigator== 'top 10 # of shots'):
        sql = """
        Select name, SUM(
        CASE 
        WHEN c.name=a.home_club_name THEN a.home_no_of_shots
        WHEN c.name=a.away_club_name THEN a.away_no_of_shots
        ELSE 0 END
        ) FROM clubs c INNER JOIN attend a
        ON (c.name = a.home_club_name OR c.name = a.away_club_name)
        GROUP BY name
        ORDER BY 2 DESC 
        LIMIT 10;   
        """ 
    elif (navigator== 'top 10 # of goals'):
        sql = """
        Select name, SUM(
        CASE 
        WHEN c.name=a.home_club_name THEN a.home_no_of_goals
        WHEN c.name=a.away_club_name THEN a.away_no_of_goals
        ELSE 0 END
        ) FROM clubs c INNER JOIN attend a
        ON (c.name = a.home_club_name OR c.name = a.away_club_name)
        GROUP BY name
        ORDER BY 2 DESC 
        LIMIT 10; 
        """ 

    elif (navigator== 'top 10 matches won'):
        sql = """
        SELECT name, SUM(
        CASE WHEN( (c.name=a.home_club_name AND a.home_no_of_goals > a.away_no_of_goals) 
        OR         (c.name=a.away_club_name AND a.home_no_of_goals < a.away_no_of_goals)) THEN 1 ELSE 0 END) 
        FROM clubs c
        INNER JOIN attend a ON (c.name=a.home_club_name 
                            OR  c.name=a.away_club_name)
        GROUP BY name
        ORDER BY 2 DESC 
        LIMIT 10;
        """ 


           

    elif (navigator== 'top 10 home matches won'):
        sql = """
        SELECT name, SUM(
        CASE WHEN( (c.name=a.home_club_name AND a.home_no_of_goals > a.away_no_of_goals)
        ) THEN 1 ELSE 0 END) 
        FROM clubs c
        INNER JOIN attend a ON (c.name=a.home_club_name 
                            OR  c.name=a.away_club_name)
        GROUP BY name
        ORDER BY 2 DESC 
        LIMIT 10;
        """ 
    return sql


def query_players(mydb):

    sql=""

    navigator=st.selectbox('Search by', ("name", 'team', 'position', 'nationality', 'height', 'birthdate'))

    if (navigator== 'name'):
        name=st.text_input("enter name")
        sql = """
        Select Distinct * 
        FROM players 
        where name Like \"%"""+name+"""%\"
        """ 
    elif (navigator== 'height'):
        height=st.text_input("enter height")
        sql = """
        Select Distinct * 
        FROM players 
        where height Like \""""+height+"""%\"
        """ 

    elif (navigator== 'birthdate'):
        birthdate=st.text_input("enter date")
        sql = """
        Select Distinct * 
        FROM players 
        where birthdate Like \""""+birthdate+"""%\"
        """ 
    elif (navigator== 'team'):
        name=st.text_input("enter team")
        sql = """
        Select Distinct name, nationality, birthdate, height , p.position, pf.season 
        FROM playedfor pf INNER JOIN players p 
        ON pf.players_name = p.name 
        where club_name Like \"%"""+name+"""%\"
        """ 

    elif (navigator== 'position'):
        input_position=st.selectbox('Search by', (  'defender',
                                                    'midfielder', 
                                                    'goalkeeper',
                                                    'forward',  ))
        sql = """
        Select Distinct * 
        FROM players
        where position = \""""+input_position+"""\"
        """ 

    elif (navigator== 'nationality'):
        input_natio=st.text_input("enter position")
        sql = """
        Select Distinct * 
        FROM players
        where nationality = \""""+input_natio+"""\"
        """ 

    return sql



def query_reviews(mydb):
    sql = """
        Select * 
        FROM reviewings
        where matchesn = 0;
        """ 
    form = st.form("review form")
    match="0"
    match=form.text_input("enter match id")
    if form.form_submit_button("search"):
        sql = """
        Select * 
        FROM reviewings
        where matchesn = """+match+""";
        """ 
    return sql

def search(mydb):


    st.sidebar.header("Search")
    navigator=st.sidebar.selectbox('Search for', ('clubs', 'players', 'reviews'), index=1)
    sql=""
    if (navigator== 'clubs'):
        sql = query_clubs(mydb)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = pd.DataFrame(mycursor.fetchall())
        st.subheader('The  search result is:')
        st.subheader(' table length:'+str(len(result)))
        st.write(result)
    elif (navigator== 'reviews'):
        sql = query_reviews(mydb)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = pd.DataFrame(mycursor.fetchall())
        st.subheader('The  search result is:')
        st.subheader(' table length:'+str(len(result)))
        st.write(result)
    elif (navigator== 'players'):
        sql = query_players(mydb)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = pd.DataFrame(mycursor.fetchall())
        st.subheader('The  search result is:')
        st.subheader(' table length:'+str(len(result)))
        st.write(result)



    return 


@st.experimental_singleton
def connect_db():
    #st.write("Connecting to Database...")
    mydb = mysql.connector.connect(
        host="mysql-78110-0.cloudclusters.net",
        user="admin",
        password="AY9PfdMV",
        database="league",
        port ="17369"
    )
    #st.write("Connected.")
    return mydb


mydb= connect_db()
st.write ('''

# Welcome to The Premier League Database

''')

st.sidebar.header("what do you want to do?")
nav=st.sidebar.selectbox('do',  ('Add review', 'Add User', 'search'), index=1)
if nav =='Add review':
    add_review(mydb)
elif nav =='Add User':
    add_user(mydb)
elif nav =='search':
    search(mydb)






