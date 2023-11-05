@echo off
call expensetracker\Scripts\activate
set FLASK_APP=index.py
flask run