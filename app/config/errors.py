# coding: utf-8

from flask import render_template
from app.main import main

__author__ = 'Jux.Liu'




def configure_errorhandlers(app):
    """Configures the error handlers."""

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("error/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("error/404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("error/500.html"), 500