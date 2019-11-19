from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, ReviewForm, RegistrationForm
from app import db, log
from app.models import User, Trial, Review, ReviewerReviews, ReviewerInformation, Book
from werkzeug.urls import url_parse
from datetime import datetime, date

reviewID = Trial.query.filter_by(reviewID=form.reviewID.data).first()
print(reviewID)
