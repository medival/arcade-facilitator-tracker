from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

forwarded_allow_ips = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }

app = Flask(__name__)

def check_badges(profile_url, badge_list):
    # Set up the WebDriver (Make sure you have the ChromeDriver installed and set in your PATH)
    chrome_driver_path = '/usr/local/bin/chromedriver'
    service = Service(chrome_driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode if you don't need a browser UI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the Qwiklabs public profile
    driver.get(profile_url)

    results = []
    arcade_badges_earned = 0
    course_badges_earned = 0
    skill_badges_earned = 0
    total_points = 0
    for badge_type, badge_name, badge_url in badge_list:
        try:
            badge_elements = driver.find_elements(By.CSS_SELECTOR, "span.ql-title-medium.l-mts")
            arcade_points = 1
            courses_points = 0
            skill_badge_points = 0.5
            found = False
            for element in badge_elements:
                if element.text == badge_name:
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
            results.append(( badge_type, badge_name, badge_url, points, '✅' if found else '❌'))
        except Exception as e:
            results.append((badge_type, badge_name, 0, '❌'))
    # Close the WebDriver
    driver.quit()
    return results, arcade_badges_earned, skill_badges_earned, course_badges_earned, total_points

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
      profile_url = request.form['profileUrl']
      tier_results = []
      cloud_results = []
      ai_results = []
      total_points = 0
      
      cloud_badges = [
          ("Arcade Game", "Level 1: Security and Compliance", "https://example.com/level1"),
          ("Arcade Game", "Level 2: Data with BigQuery", "https://example.com/level2"),
          ("Arcade Game", "Level 1: Cloud Networking", "https://example.com/level1_networking"),
          ("Arcade Game", "Level 2: Develop and Deploy", "https://example.com/level2_deploy"),
          ("Arcade Game", "Level 1: Arcade Juli - Coming Soon", "https://example.com/level2_deploy"),
          ("Arcade Game", "Level 2: Arcade Juli - Coming Soon", "https://example.com/level2_deploy"),
          ("Course", "Google Cloud Computing Foundations: Cloud Computing Fundamentals", "https://example.com/foundations1"),
          ("Course", "Google Cloud Computing Foundations: Infrastructure in Google Cloud", "https://example.com/foundations2"),
          ("Course", "Google Cloud Computing Foundations: Networking & Security in Google Cloud", "https://example.com/foundations3"),
          ("Course", "Google Cloud Computing Foundations: Data, ML, and AI in Google Cloud", "https://example.com/foundations4"),
          ("Skill Badges", "Implement Load Balancing on Compute Engine", "https://example.com/load_balancing"),
          ("Skill Badges", "Set Up an App Dev Environment on Google Cloud", "https://example.com/app_dev"),
          ("Skill Badges", "Build a Secure Google Cloud Network", "https://example.com/secure_network"),
          ("Skill Badges", "Prepare Data for ML APIs on Google Cloud", "https://example.com/ml_apis"),
          ("Skill Badges", "Set Up a Google Cloud Network", "https://example.com/cloud_network"),
          ("Skill Badges", "Implement Cloud Security Fundamentals on Google Cloud", "https://example.com/security_fundamentals"),
          ("Skill Badges", "Get Started with Cloud Storage", "https://example.com/cloud_storage"),
          ("Skill Badges", "The Basics of Google Cloud Compute", "https://example.com/cloud_compute")
      ]

      ai_badges = [
          ("Arcade Game", "Level 3: GenAIus Registries", "https://example.com/genaius_registries"),
          ("Arcade Game", "Level 3: GenAIus Travels", "https://example.com/genaius_travels"),
          ("Arcade Game", "Level 3: Coming Soon", "https://example.com/genaius_travels"),
          ("Course", "Introduction to Generative AI", "https://example.com/generative_ai"),
          ("Course", "Introduction to Large Language Models", "https://example.com/large_language_models"),
          ("Course", "Introduction to Responsible AI", "https://example.com/responsible_ai"),
          ("Course", "Responsible AI: Applying AI Principles with Google Cloud", "https://example.com/applying_ai_principles"),
          ("Skill Badges", "Prompt Design in Vertex AI", "https://example.com/prompt_design"),
          ("Skill Badges", "Classify Images with TensorFlow on Google Cloud", "https://example.com/classify_images"),
          ("Skill Badges", "Build and Deploy Machine Learning Solutions on Vertex AI", "https://example.com/ml_solutions"),
          ("Skill Badges", "Analyze Speech and Language with Google APIs", "https://example.com/speech_language"),
          ("Skill Badges", "Create ML Models with BigQuery ML", "https://example.com/bigquery_ml"),
          ("Skill Badges", "Derive Insights from BigQuery Data", "https://example.com/insights_bigquery"),
          ("Skill Badges", "Detect Manufacturing Defects using Visual Inspection AI", "https://example.com/visual_inspection"),
          ("Skill Badges", "Analyze Sentiment with Natural Language API", "https://example.com/sentiment_analysis")
      ]

      cloud_results, cloud_arcade_badges, skill_badges, course_badges, cloud_points = check_badges(profile_url, cloud_badges)
      ai_results, ai_arcade_badges, skill_badges, course_badges, ai_points = check_badges(profile_url, ai_badges)

      total_points = ai_points + cloud_points
      
      # minimum badges
      cloud_arcade_valid = cloud_arcade_badges >= 4
      ai_arcade_valid = ai_arcade_badges >= 2
      skill_valid = skill_badges == 8
      course_valid = course_badges == 4

      # Check if all badges are valid
      cloud_valid = cloud_arcade_valid and skill_valid and course_valid
      ai_valid = ai_arcade_valid and skill_valid and course_valid

      if cloud_valid and ai_valid:
          tier_result = "you got Tier Advance 🎉🥳"
          tier_color = "success"
      elif cloud_valid or ai_valid:
          tier_result = "You got tier Standard 🥳, work harder to get next milestone, keep it up bro 🔥"
          tier_color = "info"
      else:
          tier_result = "You got no Tier rn, keep it up bro 💔"
          tier_color = "danger"
      
      tier_results.append(( tier_result, tier_color ))
      return render_template('index.html', cloud_results=cloud_results, ai_results=ai_results, tier_results=tier_results, ai_points=ai_points, cloud_points=cloud_points, total_points=total_points, profile_url=profile_url)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)