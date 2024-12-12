from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from transformers import pipeline
import bcrypt
import os
import logging
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_cors import CORS

# Initialize Flask app
app = Flask(_name_)
app.secret_key = os.urandom(24)  # Generate a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profiles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
limiter = Limiter(app, key_func=lambda: session.get('username'))
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Define the UserProfile model
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    preferences = db.Column(db.String(500))  # Store user preferences
    marketing_goals = db.Column(db.String(500))  # Store marketing goals

# Define the AffiliateProgram model
class AffiliateProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    commission_rate = db.Column(db.Float, nullable=False)
    reputation = db.Column(db.Float, nullable=False)
    ease_of_use = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Initialize the language model
try:
    llm = pipeline('text-classification', model='your_model_name')  # Replace with your model
except Exception as e:
    logging.error(f"Error initializing the model: {str(e)}")
    llm = None  # Set to None if model initialization fails

# Content Generator Class
class ContentGenerator:
    @staticmethod
    def generate_content(prompt, model=llm):
        if model is None:
            return {"message": "Language model is not initialized."}, 500

        try:
            content = model(prompt)
            return {"content": content}, 200
        except Exception as e:
            logging.error(f"Error generating content: {str(e)}")
            return jsonify({"message": "An error occurred during content generation."}), 500

@app.route('/affiliate_programs', methods=['GET', 'POST'])
def manage_affiliate_programs():
    if request.method == 'POST':
        data = request.json
        new_program = AffiliateProgram(
            name=data['name'],
            description=data['description'],
            commission_rate=data['commission_rate'],
            reputation=data['reputation'],
            ease_of_use=data['ease_of_use'],
            user_id=session['user_id']  # Assuming user_id is stored in session
        )
        db.session.add(new_program)
        db.session.commit()
        return jsonify({"message": "Affiliate program added successfully!"}), 201

    # GET request to retrieve all affiliate programs
    programs = AffiliateProgram.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        "name": program.name,
        "description": program.description,
        "commission_rate": program.commission_rate,
        "reputation": program.reputation,
        "ease_of_use": program.ease_of_use
    } for program in programs]), 200

@app.route('/generate_content', methods=['POST'])
def generate_content():
    prompt = request.json.get('prompt')
    return ContentGenerator.generate_content(prompt)

@app.route('/profile', methods=['GET', 'POST'])
def manage_profile():
    if 'username' not in session:
        return jsonify({"message": "Unauthorized!"}), 401

    if request.method == 'POST':
        preferences = request.json.get('preferences')
        marketing_goals = request.json.get('marketing_goals')
        
        user = User.query.filter_by(username=session['username']).first()
        user_profile = UserProfile.query.filter_by(user_id=user.id).first()
        
        if user_profile:
            user_profile.preferences = preferences
            user_profile.marketing_goals = marketing_goals
        else:
            user_profile = UserProfile(user_id=user.id, preferences=preferences, marketing_goals=marketing_goals)
            db.session.add(user_profile)
        
        db.session.commit()
        return jsonify({"message": "Profile updated successfully!"}), 200

    user = User.query.filter_by(username=session['username']).first()
    user_profile = UserProfile.query.filter_by(user_id=user.id).first()
    return jsonify({"preferences": user_profile.preferences, "marketing_goals": user_profile.marketing_goals}), 200

if _name_ == '_main_':
    db.create_all()  # Create database tables
    app.run(debug=True)