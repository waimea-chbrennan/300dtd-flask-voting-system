#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class Users:

    NAME = "users"

    SCHEMA = """
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            name    TEXT NOT NULL,
            callsign    TEXT NOT NULL,
            email TEXT NOT NULL,
            pw_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            votes_cast INTEGER NOT NULL DEFAULT 0,
            email_status TEXT
        )
    """

    SEED_DATA = """
        INSERT INTO users (user_id, name, callsign, email, pw_hash, role, email_status)
        VALUES
            (46223819, "Abby Accent", "ZL1AA", "zl1aa@gmail.coml", "scrypt:32768:8:1$smLV0QV6ZVl1wY1Q$e52937bd37fe18f3dc74fc9ecfb97aa4d8368653df296fe634c12590cd67384d5d300a1dcc12c91f34ea17ea6d4e4c042d1e01ac6a0303a90761b517f989c291", "user", "sending"),
            (87137785, "Barry Blizzard", "ZL1BB", "zl3bb@gmail.coml", "scrypt:32768:8:1$smLV0QV6ZVl1wY1Q$e52937bd37fe18f3dc74fc9ecfb97aa4d8368653df296fe634c12590cd67384d5d300a1dcc12c91f34ea17ea6d4e4c042d1e01ac6a0303a90761b517f989c291", "user", "sending"),
            (10924844, "Charlie Cookie", "ZL1CC", "zl3cc@gmail.coml", "scrypt:32768:8:1$smLV0QV6ZVl1wY1Q$e52937bd37fe18f3dc74fc9ecfb97aa4d8368653df296fe634c12590cd67384d5d300a1dcc12c91f34ea17ea6d4e4c042d1e01ac6a0303a90761b517f989c291", "user", "error"),
            (00001234, "Debby Morgan", "ZL2DL", "zl2dl@icloud.coml", "scrypt:32768:8:1$XA3IJfTCzhWHWcaY$9f2d57127a7d47dd34ac45de858df65692f19e8117c9d2b4f0d08c6f1061ba2da32ccc57140c85563d7e790bb4bcd0b64e389837c25c9f870e121e19bdccc4da", "admin", "sent"),
            (00004321, "Mr. Election Officer", "ZL6EO", "zl6eo@nzart.org.nzl", "scrypt:32768:8:1$XA3IJfTCzhWHWcaY$9f2d57127a7d47dd34ac45de858df65692f19e8117c9d2b4f0d08c6f1061ba2da32ccc57140c85563d7e790bb4bcd0b64e389837c25c9f870e121e19bdccc4da", "officer", "sent")
    """


class StaffCreds:
    NAME = "staff_creds"

    SCHEMA = """
        CREATE TABLE staff_creds (
            user_id INTEGER PRIMARY KEY REFERENCES users(user_id),
            pw_hash TEXT NOT NULL,
            totp_secret TEXT NOT NULL,
            last_login TEXT
        )
    """

    SEED_DATA = ""


class CandidateInfo:
    NAME = "candidate_info"

    SCHEMA = """ 
        CREATE TABLE candidate_info (
            user_id INTEGER PRIMARY KEY REFERENCES users(user_id),
            description TEXT NOT NULL,
            photo_path TEXT NOT NULL,
            island TEXT NOT NULL,
            nominated_by INTEGER NOT NULL,
            for_council INTEGER NOT NULL,
            for_president INTEGER NOT NULL
        )
    """

    SEED_DATA = """
        INSERT INTO candidate_info (user_id, description, photo_path, island, nominated_by, for_council, for_president)
        VALUES
            (46223819, "A wonderful candidate, several years of service already.", "/photos/abby", "north", 00000000, 1, 1),
            (87137785, "Really really wants to be president of the world since in the year 1994 where they baked a storage container backward in a 7/11 in string handcuffs.", "/photos/barry", "south", 00000020, 0, 1),
            (10924844, "An ambitious member of all of the branches at the same time, even contributing to the committee on 44% of them and helping pull 10 out of recess in the last 36 hours.", "/photos/barry", "south", 00000013, 1, 0)
    """

class Votes:
    NAME = "votes"

    SCHEMA = """
        CREATE TABLE votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            for_type TEXT NOT NULL,
            candidate_id TEXT NOT NULL,
            approx_timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:00:00', 'now'))
        )
    """

    SEED_DATA = ""



class StaffLogs:
    NAME = "staff_logs"

    SCHEMA = """
        CREATE TABLE staff_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(user_id),
            action TEXT NOT NULL,
            detail TEXT NOT NULL,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    
    """

    SEED_DATA = ""

class AuthLogs:
    NAME = "auth_logs"

    SCHEMA = """ 
        CREATE TABLE auth_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            event INTEGER NOT NULL
        )
    """

    SEED_DATA = ""

class Elections:
    NAME = "elections"

    SCHEMA = """
        CREATE TABLE elections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            open_dt TEXT NOT NULL,
            close_dt TEXT NOT NULL,
            sealed_dt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """

    SEED_DATA = """
    """


#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1Name,
#     Table2Name,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
# foreign keys *after* the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    Users,
    StaffCreds,
    CandidateInfo,
    Votes,
    StaffLogs,
    AuthLogs,
    Elections,
]

