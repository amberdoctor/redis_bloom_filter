from flask import Flask
from flasker.redis_bloom_filter import (
    add_to_bloom_filter_format_result,
    is_unique_bloom_filter,
)
from flasker.redis_set import (
    add_to_set_format_result,
    is_unique_set
)
from flasker.check_passwords import (
    check_passwords,
    check_passwords_fixed,
    check_passwords_fixed_error_rate_fixed,
)
from flasker.reset_app import reset_app


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        """Just a Hi so that the base url isn't blank."""
        return "Hello Bloom Filter Talk Participants!"

    @app.route("/add_password_bloom_filter/<bf>/<pw>")
    def add_password_bloom_filter(bf, pw):
        """
        Keyword arguments:
        bf -- the bloom filter
        pw -- the password to add

        Return:
        boolean indicating success

        Throws:
        AssertionError on None value args
        """
        return str(add_to_bloom_filter_format_result(bf, pw))

    @app.route("/check_unique_bloom_filter/<bf>/<pw>")
    def check_password_unique_bloom_filter(bf, pw):
        """
        Keyword arguments:
        bf -- the bloom filter
        pw -- the password to check

        Return:
        str(bool) indicating if item is unique (aka not found).
        String formatting chosen for route display.
        """
        return str(is_unique_bloom_filter(bf, pw))

    @app.route("/add_password_set/<set_name>/<pw>")
    def add_password_set(set_name, pw):
        """
        Keyword arguments:
        set_name -- the set name
        pw -- the password to add

        Return:
        str(bool) indicating item was added.
        False may indicate that item had previously been added.
        """
        return str(add_to_set_format_result(set_name, pw))

    @app.route("/check_unique_set/<set_name>/<pw>")
    def check_password_unique_set(set_name, pw):
        """
        Keyword arguments:
        set_name -- the set name
        pw -- the password to check

        Return:
        str(bool) indicating if item is unique (aka not found).
        String formatting chosen for route display.
        """
        return str(is_unique_set(set_name, pw))

    @app.route("/check_grandmas_passwords")
    def check_grandmas_passwords():
        """Check grandma's original password list."""
        return check_passwords()

    @app.route("/check_grandmas_passwords_fixed")
    def check_grandmas_passwords_fixed():
        """Check grandma's improved password list with 20% error rate."""
        return check_passwords_fixed()

    @app.route("/check_grandmas_passwords_fixed_error_rate_adjusted")
    def check_grandmas_passwords_fixed_error_rate_adjusted():
        """Check grandma's improved password list with .1% error rate."""
        return check_passwords_fixed_error_rate_fixed()

    @app.route("/reset")
    def reset():
        """ Quick and dirty way to reset Redis for the demo. """
        return str(reset_app())

    return app
