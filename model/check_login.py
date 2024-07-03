from templates.config import conn
cur = conn.cursor()
def is_null(username,password):
	if(username==''or password==''):
		return True
	else:
		return False


def is_existed(username,password):
	sql="SELECT * FROM all_user WHERE user_name ='%s' and user_password ='%s'" %(username,password)
	conn.ping(reconnect=True)
	cur.execute(sql)
	conn.commit()
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def exist_user(username):
	sql = "SELECT * FROM all_user WHERE user_name ='%s'" % (username)
	conn.ping(reconnect=True)
	cur.execute(sql)
	conn.commit()
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True
