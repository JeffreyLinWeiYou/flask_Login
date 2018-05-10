# https://hackmd.io/c/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2Fryvr_ly8f
from flask import Flask, url_for, request, redirect
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask(__name__)
#  會使用到session，故為必設。
app.secret_key = 'Your Key'
login_manager = LoginManager(app)
users = {'foo@bar.tld': {'password': 'secret'}}


class User(UserMixin):
    """
 繼承UserMixin
 UserMixin幫我們記錄了四個用戶狀態：

is_authenticated
    登入成功時return True(這時候才能過的了login_required)
is_active
    帳號啟用並且登入成功的時候return True
is_anonymous
    匿名用戶return True(登入用戶會return False)
get_id()
    取得當前用戶id
 """

    pass


@login_manager.user_loader
def user_loader(email):
    """
  This sets the callback for reloading a user from the session. The
function you set should take a user ID (a ``unicode``) and return a
user object, or ``None`` if the user does not exist.
 :param email:此例將email當id使用，賦值給予user.id
 """
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return '''
     <form action='login' method='POST'>
     <input type='text' name='email' id='email' placeholder='email'/>
     <input type='password' name='password' id='password' placeholder='password'/>
     <input type='submit' name='submit'/>
     </form>
                  '''

    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        #  實作User類別
        user = User()
        #  設置id就是email
        user.id = email
        #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。
        login_user(user)
        #  登入成功，轉址
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@login_required
def protected():
    """
 在login_user(user)之後，我們就可以透過current_user.id來取得用戶的相關資訊了
 """
    #  current_user確實的取得了登錄狀態
    if current_user.is_active:
        return 'Logged in as: ' + current_user.id + 'Login is_active:True'


@app.route('/logout')
def logout():
    """
 logout\_user會將所有的相關session資訊給pop掉
 """
    logout_user()
    return 'Logged out'


if __name__ == '__main__':
    app.debug = True
    app.run(port=5020)