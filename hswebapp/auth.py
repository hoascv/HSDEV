from flask import Blueprint,render_template,flash, redirect, url_for, request, Response, jsonify
from jinja2 import TemplateNotFound
from hswebapp import app,db
from importlib import import_module
import os
from flask_login import login_required,login_user,logout_user, current_user
from datetime import datetime
from time import sleep
from hswebapp.forms.hswforms import LoginForm,RegisterForm,EditUserForm
from hswebapp.models.system_models import User,Logs,AccessGroup
import copy
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from hswebapp.models.hsutil import Hsutil

webapp_auth = Blueprint('webapp_auth', __name__,template_folder='templates/auth/pages')
@webapp_auth.route('/register', methods=['GET','POST'])

def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
                
        try:
            new_user = User(username=form.username.data,email=form.email.data,lastlogin=datetime.now())
            new_user.set_password(new_password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            
        except IntegrityError as e:
            db.session.rollback()
            flash('The user: {} or the email {} already exists \n Thank you'.format(form.username.data,form.email.data))
            app.logger.error('Sign up error: {}'.format(e))
            return render_template("hsw_signup.html",form = form)
        
        except Exception as e:
            app.logger.error('Sign up error: {}'.format(e))
            db.session.rollback()
            flash('Error! Sorry for the inconvinience The issue has been logged and it will be solved asap')
            return render_template("hsw_signup.html",form = form)
        
        finally:
            db.session.close()
    
                         
        flash('The user: {} has been created'.format(form.username.data))                
        return redirect(url_for('webapp_auth.login'))
        
    return render_template("hsw_signup.html",form = form)

@webapp_auth.route('/login', methods=['GET','POST'] )
def login():
    form = LoginForm()
    if form.validate_on_submit():
    
        try:    
            user = User.query.filter_by(username=form.username.data).first()
        
        
            if (user):
                if  user.check_password(check_password=form.password.data):
                    user.lastlogin = datetime.now()
                    db.session.commit()
                
                    login_user(user,remember=form.rememberme.data)
                    log = Logs(user_id= user.id,operation='login')
                    db.session.add(log)
                    db.session.commit()
                    
                    #TODO IMPLEMENT REDIRECT GET THE NEXT
                    #next = request.args.get('next')
                    #if not is_safe_url(nextform):
                    #    return flask.abort(400)
                    #http://flask.pocoo.org/snippets/62/
                    #return redirect(url_for(next))
                    next_page = request.args.get('next')
                    #flash(next_page) none 
                    if not next_page or not next_page.startswith('/'):
                        next_page=url_for('views.home')
                    return redirect(next_page)
                    
                    
                    #return redirect(url_for('views.home'))
                            
                flash('Invalid password')
                return render_template("hsw_login.html",form = form)
            flash('User does not exist')
            return render_template("hsw_login.html",form = form)
    
        except:
            flash("InvalidRequestError: {} ".format(sys.exc_info()[0]))
        
            raise
            db.session.rollback()
            return redirect(url_for('home'))
        
        finally:
            db.session.close()
    
    return render_template("hsw_login.html",form = form)

@webapp_auth.route('/logout')
@login_required
def logout():
    ## fix the null problem log out
    #shallow copy copy.copy(current_user.id)
    user= copy.copy(current_user)
    logout_user()
    flash("See ya: {}".format(user.username))
    log = Logs(user_id= user.id,operation='logout')
    db.session.add(log)
    db.session.commit() 
    return redirect(url_for('views.home'))

@webapp_auth.route('/logs')
@login_required
def user_logs():
    
    try:
        users= User.query.all()
    except:
        raise
        db.session.rollback()
    
    #finally:  does not show the logs detail
    #    db.session.close()
    
    return render_template("logs_stats.html", users=users)
    

@webapp_auth.route('/users', methods=['GET'])
def show_users():
# http://flask-sqlalchemy.pocoo.org/2.3/api/   check flask_sqlalchemy.Pagination 
    page_num = request.args.get('page_num',1,type=int)
    
    users = User.query.paginate(per_page=3, page=page_num, error_out=True)

    return render_template('system_users.html', users=users)    

@webapp_auth.route('/edit_user', methods=['GET','POST'] )
@login_required
def edit_user():
    
    form = EditUserForm(obj=current_user)
    form.acess_group.choices = [(g.id, g.description) for g in AccessGroup.query.order_by('id')]
        
        
    if (request.method == 'POST' and form.validate_on_submit()==True):
        
        form.populate_obj(current_user) 
        db.session.commit()
        
        flash('Your change(s) has(have) been saved ')
        return redirect(url_for('webapp_auth.edit_user'))
    db.session.close()  ## close the session on update page problems  
    return render_template('edit_user.html', form=form,hsutil=Hsutil)
        
  
@webapp_auth.route('/delete_user', methods=['GET','POST'] )
@login_required
def delete_user():
    
    user_id=request.form['user_id']
    
#    user_id = request.args.get('user_id',0,type=int)
    user = User.query.get(user_id)
    if not user :  
        return jsonify({'result' : 'error','message':'User not provided'})
    
    
    if (user.logs.count() == 0):
        db.session.delete(user) # todo check for constraint 
        db.session.commit()
    else :
        
        user.deleted_on=datetime.utcnow()
        #db.session.add(user)
        db.session.commit()
        
    return jsonify({'result' : 'success', 'message' :'user deleted' })
        
@webapp_auth.route('/update_user', methods=['POST'])
@login_required
def update_user():
    app.logger.info('updating user')
    updated=datetime.now()
    try:
        user = User.query.filter_by(id=request.form['id']).first()
        user.username = request.form['username']
        user.email = request.form['email']
        user.updatedAt = updated
        
        db.session.commit()
        
    
    except Exception as e:
        app.logger.error('Update error: {}'.format(e))
        db.session.rollback()
        flash('Error! Sorry for the inconvinience The issue has been logged and it will be solved asap') 
        return jsonify({'result' : 'error'})
    
    finally:
        db.session.close()
        
    return jsonify({'result' : 'success', 'updated' :updated })

    