from flask import Flask, Blueprint, render_template, redirect, request
import sqlite3


bp_login = Blueprint('login', __name__)

@bp_login.route('/')
def validar_login():
    return render_template('pasta_login/pasta_acesso_login/tela_logica_login.html')