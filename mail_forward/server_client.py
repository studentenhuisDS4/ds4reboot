import json

import requests
import os
import pickle


class ServerClient(object):
    """
        Class to manage data from mijndomein webmail server concerning authentication and email filters (forwards).
    """

    SERVER_API_BASE = 'https://webmail.mijndomein.nl/appsuite/api/'

    # requires: &name=mail%40ds4.nl and password in url_encoded
    SERVER_LOGIN = SERVER_API_BASE + 'login?action=login'

    SERVER_MAILFILTER_LIST = SERVER_API_BASE + \
                             'mailfilter/v2?action=list'  # requires: &session=
    SERVER_MAILFILTER_PUT_UPDATE = SERVER_API_BASE + \
                                   'mailfilter/v2?action=update'  # requires: &session=
    SERVER_MAILFILTER_PUT_NEW = SERVER_API_BASE + \
                                'mailfilter/v2?action=new'  # requires: &session=
    SERVER_MAILFILTER_PUT_DELETE = SERVER_API_BASE + \
                                   'mailfilter/v2?action=delete'  # requires: &session=
    LOGIN_PICKLEFILE = "./data/mijndomein_token.pickle"
    LOGIN_SESSIONPICKLE = "./data/mijndomein_session.pickle"
    TOKEN_KEY = "session"
    LOGIN = None

    def __init__(self):
        self.login_token = None
        self.logged_in = None
        self.fetched_filters = []
        self.session = None

    def authenticate(self, username, password, session: requests.Session):
        # Always do authenticate, if the asker requests it.
        self.LOGIN = {
            'name': username,
            'password': password
        }

        result = None
        if session:
            self.session = session
            result = session.post(self.SERVER_LOGIN, data=self.LOGIN)
        else:
            result = requests.post(self.SERVER_LOGIN, data=self.LOGIN)

        try:
            json_result = result.json()
            if self.TOKEN_KEY in json_result.keys():
                self.login_token = result.json()[self.TOKEN_KEY]
            else:
                print("WARNING: token not found in server response.")

            if result.status_code == 200:
                if self.session:
                    self.dump_session_pickle(self.session)
                if self.dump_token_pickle(session=self.login_token) is None:
                    print(
                        "ERROR: authentication could not save token as pickle. Another error must have occurred.")
                else:
                    self.logged_in = True
                    print("INFO: Authentication saved for next start.")
            elif result.status_code == 401:
                print(
                    "ERROR: authentication failed, wrong credentials. Deleting token, if any.")
                self.clean_signin()
            elif result.status_code == 500:
                print("ERROR: authentication failed, internal server error.")
            else:
                print(
                    "ERROR: authentication failed, possibly a connection failure.")

            return result.status_code == 200
        except Exception as e:
            raise e

    def action_list(self):
        # Load mijndomein filtersfrom the server API
        try:
            if self.logged_in:
                # Add authentication
                session_url = '&session=' + self.login_token
                response = None
                if self.session:
                    response = self.session.put(
                        self.SERVER_MAILFILTER_LIST + session_url)
                else:
                    raise Exception("Need session to update mijndomein API.")

                self.process_errors(response)
                if response.status_code == 200:
                    self.fetched_filters = response.json()
                    return self.fetched_filters
            else:
                print("WARN: can't retrieve mail filters without successful login.")
        except Exception as e:
            print("Exception " + str(e))

    def new_filter(self, data):
        self.put_action(self.SERVER_MAILFILTER_PUT_NEW, data)

    def update_filter(self, data):
        self.put_action(self.SERVER_MAILFILTER_PUT_UPDATE, data)

    def put_action(self, url, data):
        # Update mijndomein filtersfrom the server API
        if self.logged_in:
            # Add authentication
            session_url = '&session=' + self.login_token
            if self.session:
                response = self.session.put(
                    url + session_url, json=data)

                self.process_errors(response)
                return response
            else:
                raise Exception("Need session to update mijndomein API.")
        else:
            print("WARN: can't get successful login.")

    def process_errors(self, response):
        if response.status_code == 200:
            if "error" in response.json().keys():
                if "error_desc" in response.json().keys():
                    if "Please start a new browser session." in response.json()["error_desc"]:
                        # self.clean_signin()
                        raise Exception(
                            "You need to login again. Cleared login token:", response.json()["error_desc"])
                    raise Exception(
                        "Unsolvable error received with description:", response.json()["error_desc"])
                raise Exception("Received error:",
                                response.json()["error"])
        elif response.status_code == 401:
            raise Exception(
                "ERROR: server did not accept the login token provided (401 NOT_AUTH code)")
        else:
            raise Exception(
                "WARN: request was responded with unhandled response code for highscores, status-code: {} ("
                "response: {}) "
                    .format(response.status_code, response))

    def signin_token(self):
        # Avoids sign-in with credentials, just by token from a file.
        return self.load_token_pickle()

    def dump_session_pickle(self, session):
        # Should dump a token to file.
        try:
            self.ensure_folder_exists(self.LOGIN_SESSIONPICKLE)
            sessionfile = open(self.LOGIN_PICKLEFILE, 'ab')
            pickle.dump(session, sessionfile)
            sessionfile.close()
            return True
        except Exception as e:
            print("ERROR: exception while storing login token as pickle file.")
            return None

    def dump_token_pickle(self, session):
        # Should dump a token to file.
        try:
            self.ensure_folder_exists(self.LOGIN_PICKLEFILE)
            sessionfile = open(self.LOGIN_PICKLEFILE, 'ab')
            pickle.dump(session, sessionfile)
            sessionfile.close()
            return True
        except Exception as e:
            print("ERROR: exception while storing login token as pickle file.")
            return None

    def load_token_pickle(self):
        # Should load token or return None if not found (read with binary mode rb).
        try:
            self.logged_in = None
            if os.path.isfile(self.LOGIN_PICKLEFILE) and os.path.getsize(self.LOGIN_PICKLEFILE) == 0:
                print("WARN: removed empty pickle file.")
                os.remove(self.LOGIN_PICKLEFILE)

            if os.path.isfile(self.LOGIN_SESSIONPICKLE):
                sessionfile = open(self.LOGIN_SESSIONPICKLE, 'rb')
                self.session = pickle.load(sessionfile)
                sessionfile.close()

            if os.path.isfile(self.LOGIN_PICKLEFILE):
                tokenfile = open(self.LOGIN_PICKLEFILE, 'rb')
                pickle_result = pickle.load(tokenfile)
                tokenfile.close()

                if pickle_result is not None:
                    self.login_token = pickle_result
                    self.logged_in = True
                else:
                    # Unexpected scenario
                    print(
                        "WARN: pickle loading result was None, which poses a problem in retrieving a token.")
                    self.logged_in = False
            return self.logged_in
        except Exception as e:
            print("ERROR: exception swallowed on LOGIN PICKLE loading: {}".format(e))

        return -1

    def clean_signin(self):
        if os.path.isfile(self.LOGIN_PICKLEFILE):
            os.remove(self.LOGIN_PICKLEFILE)
        self.logged_in = None
        self.login_token = None

    def get_token_header(self, provided_token):
        return {'Authorization': 'Bearer ' + provided_token}

    def ensure_folder_exists(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
