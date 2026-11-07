#===========================================================
# NZART Voting System
# By Connor Brennan
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from string import ascii_letters, digits
from secrets import choice
from time import sleep
from threading import Thread

# SMTP functionality
from smtplib            import SMTP
from dotenv import load_dotenv
from os import getenv
from email.utils import formataddr
from email.message import EmailMessage



# Create the app
app = Flask(__name__)

#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Home page - Dynamic Per login and vote state
# Gross
#-----------------------------------------------------------
@app.get("/")
def show_home():
    if (session.get("logged_in")):
        # Determine whether user has voted
        with connect_db() as db:
            sql = """
                SELECT votes_cast 
                FROM users
                WHERE user_id=?
            """
            params = (session["user"]["user_id"],)
            voted = db.execute(sql, params).fetchone()["votes_cast"]
            if(voted): 
                return render_template("pages/voting_success.jinja")

        return render_template("pages/voting_home.jinja")
    else:
        return render_template("pages/noauth_overview.jinja")


#=====================================================================
# Login & Auth Functions
#=====================================================================

#-----------------------------------------------------------
# Form login Handler - User submitted id and pw
#-----------------------------------------------------------
@app.post("/login")
def login_post():
    user_id = request.form.get("member_id")
    pw = request.form.get("password")

    sleep(1)
    with connect_db() as db:
        sql = """
            SELECT user_id, name, callsign, email, pw_hash, role, votes_cast
            FROM users
            WHERE user_id=?
        """
        params = (user_id,)
        user = db.execute(sql, params).fetchone()

        if not user:
            flash(f"Unknown user", "error")
            return redirect("/login")

        if not check_password_hash(user["pw_hash"], pw):
            flash(f"Incorrect password", "error")
            return redirect("/login")

    login_user(user)

    return redirect("/")

#-----------------------------------------------------------
# Login Page - Show or find auth token
#-----------------------------------------------------------
@app.get("/login")
def login_get():

    login_token = request.args.get('token')
    

    if not login_token:
        return render_template("pages/login.jinja")

    # Log badtoken attempts?
    try:
        data = serializer.loads(login_token)
    except Exception as e:
        return redirect("/")
        print(f"Invalid token: {e}")
        # return errors?

    #Fetch remainder of user info
    with connect_db() as db:
        sql = """
            SELECT user_id, name, callsign, email, role
            FROM users
            WHERE user_id=?
        """
        params = (data["user_id"],)
        user = db.execute(sql, params).fetchone()

        if not user:
            flash(f"Unknown user", "error")
            return redirect("/login")
   
 
    # Log the user with the correct info in
    login_user(user)
    return redirect("/")

#-----------------------------------------------------------
# Add validated user object to session
#-----------------------------------------------------------
def login_user(user):
    session["logged_in"] = True
    session["user"] = {
        "user_id":       user["user_id"],
        "name":          user["name"],
        "callsign":      user["callsign"],
        "email":         user["email"],
        "role":          user["role"]
        # votes and pw_hash should be backend only
    }

    flash("Login successful", "success")
    return redirect("/")

#-----------------------------------------------------------
# Cleanly logout the user
#-----------------------------------------------------------
@app.get("/logout")
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect("/")



#=====================================================================
# Admin Pages
#=====================================================================
@admin_required
@app.get("/admin/users")
def show_admin_home():
    with connect_db() as db:
        sql = """SELECT 
            user_id, name, callsign, email, role, votes_cast
            FROM users
            """
        params = ()
        users = db.execute(sql, params).fetchall()
    
    return render_template("pages/admin_users.jinja", users=users)

@admin_required
@app.post("/admin/users/update/")
def update_resend_user():
    id = request.args.get("id").strip().lower()
    new_email = request.form.get("email").strip().lower()

    with connect_db() as db:
        sql = """UPDATE users
            SET email=?
            WHERE user_id=?
        """
        params = (new_email, id,)
        db.execute(sql, params)
        
    return redirect("/admin/users")


@admin_required
@app.get("/admin/users/delete/")
def delete_user():
    id = request.args.get("id").strip().lower()

    with connect_db() as db:
        sql = """
            DELETE FROM users
            WHERE user_id=?
        """
        params = (id,)
        db.execute(sql, params)
    
    flash("User Deleted", "message")
        

    return redirect("/admin/users")



    return redirect("/admin/users")

@admin_required
@app.post("/admin/users/search")
def return_searched_users():
    search_name = request.form.get("search").strip().lower()
    with connect_db() as db:
        sql = """SELECT 
            user_id, name, callsign, email, role, votes_cast, email_status
            FROM users
            WHERE name LIKE ?
            """
        params = (f"%{search_name}%",)
        users = db.execute(sql, params).fetchall()
    
    return render_template("partials/user_list.jinja", users=users)





#=====================================================================
# Election Officer Pages
#=====================================================================
@officer_required
@app.get("/officer/election")
def show_election_page():
    with connect_db() as db:
        sql = """ 
            SELECT * FROM elections
        """
        elections = db.execute(sql).fetchall()

        sql = """
            SELECT user_id FROM candidate_info
        """
        candidates = db.execute(sql).fetchall()

        return render_template("pages/election.jinja", elections=elections, candidates=candidates)


@officer_required
@app.get("/officer/election/create")
def show_new_election_page():
    return render_template("pages/new_election.jinja")

@officer_required
@app.post("/officer/election/create")
def submit_new_election():
    name = request.form.get("name")
    open_dt = request.form.get("open_dt")
    close_dt = request.form.get("close_dt")

    with connect_db() as db:
        sql = """
            INSERT INTO elections
            (name, open_dt, close_dt)
            VALUES (?,?,?)
        """
        params = (name, open_dt, close_dt)
        db.execute(sql, params)

    return redirect("/officer/election")



@officer_required
@app.post("/officer/election/<int:id>")
def update_election_info(id):
    open_dt = request.form.get("open_dt")
    closed_dt = request.form.get("close_dt")

    with connect_db() as db:
        sql = """
            UPDATE elections
            SET open_dt=?, close_dt=?, sealed_dt=CURRENT_TIMESTAMP
            WHERE id=?
        """
        params = (open_dt, closed_dt, id)
        db.execute(sql, params)
        
        flash("Election details updated", "info")

        return redirect("/officer/election")



@officer_required
@app.get("/officer/candidates")
def show_election_candidates():
    with connect_db() as db:
        sql = """SELECT *
            FROM candidate_info
            INNER JOIN users 
            USING (user_id)
        """
        params = ()
        candidates = db.execute(sql, params).fetchall()

    return render_template("pages/candidates.jinja", candidates=candidates)


@officer_required
@app.post("/officer/candidates/new")
def add_new_candidate():
    description = request.form.get("description")
    photo_path = request.form.get("photo_path")
    island = request.form.get("island")
    for_council = request.form.get("for_council")
    for_president = request.form.get("for_president")
    user_id = request.form.get("user_id")


    with connect_db() as db:
        sql = """
            INSERT INTO candidate_info
            (description, photo_path, island, for_council, for_president, user_id) 
            VALUES (?,?,?,?,?,?,)
        """
        params = (description, photo_path, island, for_council, for_president, user_id,)
        result = db.execute(sql, params)

    flash("New Candidate Added", "info")

    return redirect("/officer/candidates")


@officer_required
@app.post("/officer/candidates/update")
def edit_candidate_info():
    description = request.form.get("description")
    photo_path = request.form.get("photo_path")
    island = request.form.get("island")
    for_council = request.form.get("for_council")
    for_president = request.form.get("for_president")
    user_id = request.form.get("user_id")


    with connect_db() as db:
        sql = """ UPDATE candidate_info
            SET description=?, photo_path=?, island=?, for_council=?, for_president=?
            WHERE user_id=?
        """
        params = (description, photo_path, island, for_council, for_president, user_id,)
        result = db.execute(sql, params)

    flash("Candidate details updated", "info")
    return redirect("/officer/candidates")


@officer_required
@app.get("/officer/results")
def show_results_page():
    with connect_db() as db:
        sql = """ SELECT for_type, candidate_id, approx_timestamp
          FROM votes
        """
        params = ()
        votes = db.execute(sql, params).fetchall()

    return render_template("pages/results.jinja", votes=votes)



#=====================================================================
# Ballot submission 
#=====================================================================
# @login_required
# @app.get("/voting")
# def show_voting_home():
    # return render_template("pages/voting_home.jinja")

@login_required
@app.get("/voting/select")
def show_candidate_selection():
    island = request.args.get("island")

    with connect_db() as db:
        if island=="north":
            sql = """
                SELECT * 
                FROM candidate_info
                INNER JOIN users ON candidate_info.user_id=users.user_id 
                WHERE island='north'
            """
        elif island=="south":
            sql = """
                SELECT * 
                FROM candidate_info
                INNER JOIN users ON candidate_info.user_id=users.user_id 
                WHERE island='south'
            """
        else:
            sql = """
                SELECT * 
                FROM candidate_info
                INNER JOIN users ON candidate_info.user_id=users.user_id 
            """
        params = ()
        candidates = db.execute(sql, params).fetchall()

    return render_template("pages/voting_select.jinja", candidates=candidates)

@login_required
@app.post("/voting/submit")
def submit_ballot():
    # Get their council and candidate votes
    council_ballot = request.form.get("council")
    presidential_ballot = request.form.get("presidential")

    # Check if the user has voted before
    with connect_db() as db:
        sql = """
            SELECT votes_cast 
            FROM users
            WHERE user_id=?
        """
        params = (session["user"]["user_id"],)
        user_vote = db.execute(sql, params).fetchone()

    if user_vote["votes_cast"]!=0:
        flash("Vote has already been submitted", "error")
        return redirect("/")
    
    # Validate 2 votes received to be applicable candidates
    with connect_db() as db:
        sql = """
            SELECT user_id, for_council, for_president
            FROM candidate_info
            WHERE (user_id=? AND for_council=1)
            OR (user_id=? AND for_president=1)
        """
        params = (council_ballot, presidential_ballot,)
        candidates = db.execute(sql, params).fetchall()
    
    if len(candidates)!=2:
        flash("Invalid Ballot", "error")
        return redirect("/")
    
    # Mark the user as voted
    with connect_db() as db:
        sql = """
            UPDATE users
            SET votes_cast=1
            WHERE user_id=?
        """
        params = (session["user"]["user_id"],)
        result = db.execute(sql, params)

    # Log any errors in this step
    #if result!=success:

    # Add each vote entry to the votes table with timestamps 
    with connect_db() as db:
        sql = """
            INSERT INTO votes (for_type, candidate_id)
            VALUES
                ("council", ?),
                ("presidential", ?)
        """
        params = (council_ballot, presidential_ballot,)
        result = db.execute(sql, params)

    # if result=yay

    flash("You have successfully voted!", "info")
    return redirect("/")




#=====================================================================
# User Adding
#=====================================================================

@app.get("/addusertest")
def add_user_test():
    provision_account(88888888, "Firsty Last", "ZL3FL", "reddogrun.cb@gmail.com", "user")
    return redirect("/")



@app.post("/admin/users/adduser")
def add_standard_user():
    member_id = request.form.get("member_id")
    name = request.form.get("name")
    callsign = request.form.get("callsign")
    email = request.form.get("email")

    provision_account(member_id, name, callsign, email, "user")

    ## Get a user readable error message returned eg user already exists

    flash(f"User Added", "info")
    return redirect("/admin/users")

def provision_account(user_id, name, callsign, email, role):

    plain_pw = "".join(choice(ascii_letters + digits + "!@#$%^&*()") for _ in range(16))

    hashed_pw = generate_password_hash(plain_pw)

    login_token = serializer.dumps({"user_id": user_id})

    body=f"""Dear {name} {callsign},
    Your login for NZART council and president is now ready.

    Please use the link or membership id and password below to sign in and vote.

    http://localhost:5000/login?token={login_token}

    Membership ID: {user_id}
    Voting Password: {plain_pw}

    73,
    <ELECTION OFFICER, NZART>
    """

    html_template = """
    <!DOCTYPE html>
    <html>
        <head>
        <meta charset="utf-8">
        <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .credentials-box {{ background-color: #f4f6f9; border-left: 4px solid #0056b3;
            padding: 15px; margin: 20px 0; font-family: monospace; font-size: 14px; }}
        .btn {{ display: inline-block; background-color: #0056b3; color: #ffffff !important;
            padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; margin: 15px 0; }}
        .footer {{ margin-top: 30px; border-top: 1px solid #e0e0e0; padding-top: 15px;
            font-size: 12px; color: #777777; }}
        </style>
        </head>
        <body>
            <div class="container">
            <p>Dear {name} {callsign},</p>
            <p>Your login for the NZART council and president election is now ready.</p>
            <p>Please use the link below to sign in and vote directly, or manually enter the credentials provided below on the login page on PROD_URL</p>
            <p><a href="{login_url}" class="btn">Sign In and Vote</a></p>
            <div class="credentials-box">
            <strong>Membership ID:</strong> {user_id}<br>
            <strong>Voting Password:</strong> {plain_pw}
            </div>
            <div class="footer">
            <p>73,<br><strong>&lt;ELECTION OFFICER, NZART&gt;</strong></p>
            </div>
            </div>
        </body>
    </html>
    """

    login_url = f"http://localhost:5000/login?token={login_token}"
    html_body = html_template.format(
        name=name, callsign=callsign, user_id=user_id,
        plain_pw=plain_pw, login_url=login_url,
    )
    
    print(f"sending onboarding to {email}")
    print(f"TEMPORARY PW------------------------------------------------- {plain_pw}")

    thread = Thread(target=send_provision_email_async, args=(body, html_body, email, user_id))
    thread.start()

    with connect_db() as db:
        sql = "INSERT INTO users (user_id, name, callsign, email, pw_hash, role) VALUES (?,?,?,?,?,?)"
        params = [user_id, name, callsign, email, hashed_pw, role]
        db.execute(sql,params)

    print("added new user")



def send_provision_email_async(body, html, recipient_email, user_id):
    #Need to add a success/failure information returned try except 
    with connect_db() as db:
        sql = """UPDATE users
            SET email_status=?
            WHERE user_id=?
        """
        params = ("sending", user_id,)
        db.execute(sql, params)
    
    try:
        with SMTP(getenv("SMTP_SERVER"), getenv("SMTP_PORT")) as server:
            msg = EmailMessage() 

            msg["From"] = formataddr((getenv("SMTP_NAME"), getenv("SMTP_EMAIL")))
            msg["To"] = recipient
            msg["Subject"] = "NZART Elections Open 2027"
            msg.set_content(body)
            msg.add_alternative(html, subtype="html")

            server.starttls()
            server.login(getenv("SMTP_EMAIL"), getenv("SMTP_KEY"))
            result = server.send_message(msg)

            if result:
                with connect_db() as db:
                    sql = """UPDATE users
                        SET email_status=?
                        WHERE user_id=?
                    """
                    params = ("sent", user_id,)
                    db.execute(sql, params)
                # Add email pending to user
            else:
                # Add error and log
                with connect_db() as db:
                    sql = """UPDATE users
                        SET email_status=?
                        WHERE user_id=?
                    """
                    params = ("error", user_id,)
                    db.execute(sql, params)

    except Exception as e:
        print(f"SMTP ERROR SENDING EMAIL TO {recipient}: {e}")
        # Log e into the log db 
        with connect_db() as db:
            sql = """UPDATE users
                SET email_status=?
                WHERE user_id=?
            """
            params = ("error", user_id,)
            db.execute(sql, params)


        

#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)
serializer = URLSafeTimedSerializer(getenv("FLASK_SECRET_KEY"), getenv("FLASK_SALT"))

