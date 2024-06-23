from flask import Flask, render_template, request
import requests
from datetime import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)

def check_profile(profile_url):
    try:
        response = requests.get(profile_url)
        response.raise_for_status()
        return response.status_code
    except requests.RequestException:
        return None

def check_badges(profile_url, badge_list):
    response = requests.get(profile_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="jump-content")
    profile_badges = results.find_all("div", class_="profile-badges")

    results = []
    arcade_badges_earned = 0
    course_badges_earned = 0
    skill_badges_earned = 0
    total_points = 0

    for badge_type, badge_label, badge_name, badge_url in badge_list:
        arcade_points = 1
        courses_points = 0
        skill_badge_points = 0.5
        found = False

        for profile_badge in profile_badges:
            spawn_profile_badge = profile_badge.find_all("span", class_="ql-title-medium")
            for profile_badge in spawn_profile_badge:
                badge_title = profile_badge.text.strip()
                if badge_title == badge_name:
                    found = True
                    break

        points = arcade_points if badge_type == "Arcade Game" else skill_badge_points if badge_type == "Skill Badges" else courses_points if badge_type == "Course" else 0
        if found:
            total_points += points
            if badge_type == "Arcade Game":
                arcade_badges_earned += 1
            if badge_type == "Course":
                course_badges_earned += 1
            if badge_type == "Skill Badges":
                skill_badges_earned += 1
        results.append((badge_type, badge_label, badge_name, badge_url, points, '✅' if found else '❌'))

    return results, arcade_badges_earned, skill_badges_earned, course_badges_earned, total_points, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        profile_url = request.form['profileUrl']
        status_code = check_profile(profile_url)
        tier_results = []
        errors = []
        cloud_bonus_points = 0.0
        ai_bonus_points = 0.0
        track_bonus_points = 0.0

        if status_code == 200:
            cloud_badges = [
                ("Arcade Game", "Level 1 (May): Security and Compliance (1q-secure-0545)", "Level 1: Security and Compliance", "https://www.cloudskillsboost.google/games/5058"),
                ("Arcade Game", "Level 2 (May): Data with BigQuery (1q-bigquery-0544)", "Level 2: Data with BigQuery", "https://www.cloudskillsboost.google/games/5057"),
                ("Arcade Game", "Level 1 (June): Cloud Networking (1q-networking-0631)", "Level 1: Cloud Networking", "https://www.cloudskillsboost.google/games/5156"),
                ("Arcade Game", "Level 2 (June): Develop and Deploy (1q-deploy-0632)", "Level 2: Develop and Deploy", "https://www.cloudskillsboost.google/games/5155"),
                ("Arcade Game", "Level 1 (July): Arcade Games - Coming Soon", "Level 1: Arcade Juli - Coming Soon", "https://www.cloudskillsboost.google/games/"),
                ("Arcade Game", "Level 2 (July): Arcade Games - Coming Soon", "Level 2: Arcade Juli - Coming Soon", "https://www.cloudskillsboost.google/games/"),
                ("Course", "Google Cloud Computing Foundations: Cloud Computing Fundamentals", "Google Cloud Computing Foundations: Cloud Computing Fundamentals", "https://www.cloudskillsboost.google/course_templates/153"),
                ("Course", "Google Cloud Computing Foundations: Infrastructure in Google Cloud", "Google Cloud Computing Foundations: Infrastructure in Google Cloud", "https://www.cloudskillsboost.google/course_templates/154"),
                ("Course", "Google Cloud Computing Foundations: Networking & Security in Google Cloud", "Google Cloud Computing Foundations: Networking & Security in Google Cloud", "https://www.cloudskillsboost.google/course_templates/155"),
                ("Course", "Google Cloud Computing Foundations: Data, ML, and AI in Google Cloud", "Google Cloud Computing Foundations: Data, ML, and AI in Google Cloud", "https://www.cloudskillsboost.google/course_templates/156"),
                ("Skill Badges", "Implement Load Balancing on Compute Engine", "Implement Load Balancing on Compute Engine", "https://www.cloudskillsboost.google/course_templates/648"),
                ("Skill Badges", "Set Up an App Dev Environment on Google Cloud", "Set Up an App Dev Environment on Google Cloud", "https://www.cloudskillsboost.google/course_templates/637"),
                ("Skill Badges", "Build a Secure Google Cloud Network", "Build a Secure Google Cloud Network", "https://www.cloudskillsboost.google/course_templates/654"),
                ("Skill Badges", "Prepare Data for ML APIs on Google Cloud", "Prepare Data for ML APIs on Google Cloud", "https://www.cloudskillsboost.google/course_templates/631"),
                ("Skill Badges", "Set Up a Google Cloud Network", "Set Up a Google Cloud Network", "https://www.cloudskillsboost.google/course_templates/641"),
                ("Skill Badges", "Implement Cloud Security Fundamentals on Google Cloud", "Implement Cloud Security Fundamentals on Google Cloud", "https://www.cloudskillsboost.google/course_templates/645"),
                ("Skill Badges", "Get Started with Cloud Storage", "Get Started with Cloud Storage", "https://www.cloudskillsboost.google/course_templates/725"),
                ("Skill Badges", "The Basics of Google Cloud Compute", "The Basics of Google Cloud Compute", "https://www.cloudskillsboost.google/course_templates/754")
            ]

            ai_badges = [
                ("Arcade Game", "Level 3 (May): GenAIus Registries (1q-deploy-0632)", "Level 3: GenAIus Registries", "https://www.cloudskillsboost.google/games/5060"),
                ("Arcade Game", "Level 3 (June): GenAIus Travels (1q-genai-0631)", "Level 3: GenAIus Travels", "https://www.cloudskillsboost.google/games/5154"),
                ("Arcade Game", "Level 3 (July): Coming Soon", "Level 3: Coming Soon", "https://www.cloudskillsboost.google/games/"),
                ("Course", "Introduction to Generative AI", "Introduction to Generative AI", "https://www.cloudskillsboost.google/course_templates/536"),
                ("Course", "Introduction to Large Language Models", "Introduction to Large Language Models", "https://www.cloudskillsboost.google/course_templates/539"),
                ("Course", "Introduction to Responsible AI", "Introduction to Responsible AI", "https://www.cloudskillsboost.google/course_templates/554"),
                ("Course", "Responsible AI: Applying AI Principles with Google Cloud", "Responsible AI: Applying AI Principles with Google Cloud", "https://www.cloudskillsboost.google/course_templates/388"),
                ("Skill Badges", "Prompt Design in Vertex AI", "Prompt Design in Vertex AI", "https://www.cloudskillsboost.google/course_templates/976"),
                ("Skill Badges", "Get Started with TensorFlow on Google Cloud", "Classify Images with TensorFlow on Google Cloud", "https://www.cloudskillsboost.google/course_templates/646"),
                ("Skill Badges", "Build and Deploy Machine Learning Solutions on Vertex AI", "Build and Deploy Machine Learning Solutions on Vertex AI", "https://www.cloudskillsboost.google/course_templates/684"),
                ("Skill Badges", "Analyze Speech and Language with Google APIs", "Analyze Speech and Language with Google APIs", "https://www.cloudskillsboost.google/course_templates/634"),
                ("Skill Badges", "Create ML Models with BigQuery ML", "Create ML Models with BigQuery ML", "https://www.cloudskillsboost.google/course_templates/626"),
                ("Skill Badges", "Derive Insights from BigQuery Data", "Derive Insights from BigQuery Data", "https://www.cloudskillsboost.google/course_templates/623"),
                ("Skill Badges", "Detect Manufacturing Defects using Visual Inspection AI", "Detect Manufacturing Defects using Visual Inspection AI", "https://www.cloudskillsboost.google/course_templates/644"),
                ("Skill Badges", "Analyze Sentiment with Natural Language API", "Analyze Sentiment with Natural Language API", "https://www.cloudskillsboost.google/course_templates/667")
            ]

            cloud_results, cloud_arcade_badges, cloud_skill_badges, cloud_course_badges, cloud_points, cloud_error = check_badges(profile_url, cloud_badges)
            ai_results, ai_arcade_badges, ai_skill_badges, ai_course_badges, ai_points, ai_error = check_badges(profile_url, ai_badges)

            cloud_arcade_valid = cloud_arcade_badges >= 4
            ai_arcade_valid = ai_arcade_badges >= 2
            cloud_skill_valid = cloud_skill_badges >= 8
            ai_skill_valid = ai_skill_badges >= 8
            cloud_course_valid = cloud_course_badges >= 4
            ai_course_valid = ai_course_badges == 4

            cloud_valid = cloud_arcade_valid and cloud_skill_valid and cloud_course_valid
            ai_valid = ai_arcade_valid and ai_skill_valid and ai_course_valid

            if cloud_valid and ai_valid:
                tier_result = "Tier Advance (Milestone #2) 🎉🥳"
                tier_color = "success"
                ai_bonus_points = 4.0
                cloud_bonus_points = 2.0
                track_bonus_points = 5.0
            elif cloud_valid:
                tier_result = "Tier Standard (Milestone #1) 🥳, work harder to achieve the Milestone #2, keep it up bro 🔥"
                tier_color = "info"
                ai_bonus_points = ai_bonus_points
                cloud_bonus_points = 2.0
                track_bonus_points = track_bonus_points
            elif ai_valid:
                tier_result = "Tier Standard 🥳, work harder to achieve the Milestone #2, keep it up bro 🔥"
                tier_color = "info"
                cloud_bonus_points = cloud_bonus_points
                ai_bonus_points = 4.0
                track_bonus_points = track_bonus_points
            else:
                tier_result = "No Tier. Keep it up bro 🔥"
                tier_color = "danger"

            tier_results.append((tier_result, tier_color))
            return render_template('index.html', cloud_results=cloud_results, ai_results=ai_results, tier_results=tier_results, ai_points=ai_points, cloud_points=cloud_points, ai_bonus_points=ai_bonus_points, cloud_bonus_points=cloud_bonus_points, track_bonus_points=track_bonus_points, profile_url=profile_url)
        elif status_code == None:
            error_message="An error occurred while checking url. Please make sure the profile URL is correct."
            error_color= "danger"
            errors.append((error_message, error_color))
        return render_template('index.html', profile_url=profile_url, errors=errors)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
