from flask import Flask, render_template, request
import math

app = Flask(__name__)

# =====================================================================
# CAREER KNOWLEDGE BASE
# Each career has weighted required skills and metadata.
# =====================================================================
CAREER_PROFILES = [
    {
        "title": "Software Engineer",
        "icon": "💻",
        "description": "Design, develop, and maintain software applications and systems. High demand, strong salary growth, and creative problem-solving at scale.",
        "skills": ["Python", "Algorithms", "System Design", "Problem Solving"],
        "next_steps": [
            "Learn Python or JavaScript",
            "Build 2–3 personal projects on GitHub",
            "Practice on LeetCode / HackerRank",
            "Apply for internships"
        ],
        "weights": {
            "coding": 10,
            "analytical": 8,
            "problem_solving": 9,
            "research": 4,
            "creativity": 3,
            "communication": 3
        },
        "subject_bonus": {"computers": 15, "mathematics": 8},
        "hobby_bonus": {"building_apps": 15, "analyzing_data": 5},
        "env_bonus": {"office": 5, "remote": 8},
        "motivation_bonus": {"high_salary": 8, "innovation": 10},
        "videos": [
            {"title": "What is Software Engineering?", "id": "bZaqbMBRXgA", "channel": "CS Dojo"},
            {"title": "Software Engineer Day in the Life", "id": "rqX8PFcOpxA", "channel": "Mayuko"},
            {"title": "How to become a Software Engineer", "id": "ysEN5RaKOlA", "channel": "Traversy Media"}
        ]
    },
    {
        "title": "Data Scientist",
        "icon": "📊",
        "description": "Extract insights from large datasets using statistics, machine learning, and visualisation to drive business decisions.",
        "skills": ["Statistics", "Machine Learning", "Python/R", "SQL"],
        "next_steps": [
            "Learn Python & pandas",
            "Study statistics and probability",
            "Complete a Kaggle competition",
            "Build a data portfolio"
        ],
        "weights": {
            "analytical": 10,
            "coding": 8,
            "problem_solving": 8,
            "research": 7,
            "creativity": 3,
            "communication": 4
        },
        "subject_bonus": {"mathematics": 12, "computers": 8, "economics": 5},
        "hobby_bonus": {"analyzing_data": 15, "experimenting": 6},
        "env_bonus": {"office": 5, "remote": 8, "lab": 6},
        "motivation_bonus": {"innovation": 10, "high_salary": 8},
        "videos": [
            {"title": "Data Science Full Course for Beginners", "id": "ua-CiDNNj30", "channel": "freeCodeCamp"},
            {"title": "Day in the Life of a Data Scientist", "id": "ft3SkKNIo_g", "channel": "Ken Jee"},
            {"title": "Data Science Roadmap 2024", "id": "8d2wkl0l1I", "channel": "Tech With Tim"}
        ]
    },
    {
        "title": "Doctor / Physician",
        "icon": "🏥",
        "description": "Diagnose and treat illnesses, perform medical procedures, and improve patient health outcomes. Highly respected and socially impactful profession.",
        "skills": ["Biology", "Clinical Skills", "Empathy", "Decision Making"],
        "next_steps": [
            "Focus on Biology and Chemistry",
            "Prepare for medical entrance exams (NEET/MCAT)",
            "Volunteer at local clinics",
            "Pursue MBBS/MD degree"
        ],
        "weights": {
            "analytical": 8,
            "research": 7,
            "problem_solving": 7,
            "communication": 8,
            "creativity": 2,
            "coding": 1
        },
        "subject_bonus": {"biology": 18, "science": 10},
        "hobby_bonus": {"helping_people": 15, "experimenting": 5},
        "env_bonus": {"hospital": 15, "lab": 5},
        "motivation_bonus": {"social_impact": 15, "recognition": 5},
        "videos": [
            {"title": "A Day in the Life of a Doctor", "id": "bWR5M2g4diQ", "channel": "Dr. Jubbal"},
            {"title": "How to Become a Doctor - Full Guide", "id": "RqvVf3IVxHk", "channel": "Med School Insiders"},
            {"title": "Medical School: What to Expect", "id": "QWYv0u9LKDM", "channel": "Doctor Mike"}
        ]
    },
    {
        "title": "Lawyer / Advocate",
        "icon": "⚖️",
        "description": "Represent clients in legal matters, draft legal documents, and argue cases in court. Requires sharp analytical thinking and persuasive communication.",
        "skills": ["Legal Research", "Argumentation", "Writing", "Critical Thinking"],
        "next_steps": [
            "Study Political Science / Law",
            "Develop strong reading & writing habits",
            "Participate in moot court competitions",
            "Pursue LLB degree"
        ],
        "weights": {
            "communication": 10,
            "analytical": 9,
            "problem_solving": 7,
            "research": 8,
            "creativity": 4,
            "coding": 0
        },
        "subject_bonus": {"social_science": 12, "literature": 10, "arts": 5},
        "hobby_bonus": {"debating": 18, "writing": 8},
        "env_bonus": {"office": 8},
        "motivation_bonus": {"social_impact": 10, "recognition": 8, "high_salary": 5},
        "videos": [
            {"title": "What Does a Lawyer Actually Do?", "id": "RjijJBUGbXk", "channel": "LegalEagle"},
            {"title": "How to Become a Lawyer", "id": "rO2sL2Gln5o", "channel": "Law School Toolbox"},
            {"title": "A Day in the Life of a Lawyer", "id": "FmIib46BXHY", "channel": "Legal Eagle"}
        ]
    },
    {
        "title": "UI/UX Designer",
        "icon": "🎨",
        "description": "Create intuitive, beautiful user interfaces for apps and websites. Combines artistic creativity with user psychology and technology.",
        "skills": ["Figma", "User Research", "Prototyping", "Visual Design"],
        "next_steps": [
            "Learn Figma or Adobe XD",
            "Study design principles (typography, color)",
            "Build a design portfolio on Behance",
            "Take UI/UX courses on Coursera"
        ],
        "weights": {
            "creativity": 10,
            "coding": 4,
            "communication": 6,
            "problem_solving": 6,
            "analytical": 4,
            "research": 5
        },
        "subject_bonus": {"arts": 15, "computers": 7},
        "hobby_bonus": {"designing": 18, "building_apps": 6},
        "env_bonus": {"creative_studio": 12, "remote": 8},
        "motivation_bonus": {"creativity": 15, "recognition": 6},
        "videos": [
            {"title": "UI/UX Design Full Course", "id": "c9Wg6Cb_YlU", "channel": "DesignCourse"},
            {"title": "Day in the Life of a UI/UX Designer", "id": "pGYAg7TMmp0", "channel": "CharliMarieTV"},
            {"title": "How to Become a UX Designer in 2024", "id": "rImnGEcFH0g", "channel": "AJ&Smart"}
        ]
    },
    {
        "title": "Business Analyst",
        "icon": "📈",
        "description": "Bridge the gap between business needs and technical solutions by analyzing data, processes, and strategies to improve organizational performance.",
        "skills": ["Excel", "SQL", "Communication", "Process Mapping"],
        "next_steps": [
            "Learn Excel and SQL",
            "Study business management principles",
            "Pursue MBA or BBA degree",
            "Get certified in CBAP or PMP"
        ],
        "weights": {
            "analytical": 9,
            "communication": 9,
            "problem_solving": 7,
            "coding": 3,
            "creativity": 4,
            "research": 6
        },
        "subject_bonus": {"economics": 15, "mathematics": 8, "social_science": 6},
        "hobby_bonus": {"analyzing_data": 10, "managing": 15},
        "env_bonus": {"office": 10},
        "motivation_bonus": {"high_salary": 10, "stability": 8},
        "videos": [
            {"title": "What is a Business Analyst?", "id": "FVtGXXqGFqI", "channel": "BA Careers"},
            {"title": "Business Analyst Career Path Explained", "id": "JT3lhFBpxXk", "channel": "CareerFoundry"},
            {"title": "Day in the Life of a Business Analyst", "id": "6Hk3oAHnlBs", "channel": "Career Insights"}
        ]
    },
    {
        "title": "Mechanical Engineer",
        "icon": "⚙️",
        "description": "Design, analyze, and manufacture mechanical systems — from engines to robotics. Combines physics, math, and creative engineering.",
        "skills": ["CAD", "Thermodynamics", "Material Science", "Physics"],
        "next_steps": [
            "Strong foundation in Physics & Maths",
            "Learn AutoCAD or SolidWorks",
            "Build projects (robotics, 3D printing)",
            "Pursue B.Tech/B.E. in Mechanical"
        ],
        "weights": {
            "analytical": 9,
            "problem_solving": 9,
            "research": 6,
            "creativity": 5,
            "coding": 3,
            "communication": 3
        },
        "subject_bonus": {"science": 15, "mathematics": 12},
        "hobby_bonus": {"experimenting": 15, "building_apps": 3},
        "env_bonus": {"lab": 10, "outdoor": 5},
        "motivation_bonus": {"innovation": 12, "stability": 6},
        "videos": [
            {"title": "What is Mechanical Engineering?", "id": "LtBEP2v7HtM", "channel": "Zach Star"},
            {"title": "Mechanical Engineer Day in the Life", "id": "YVHa9AqcGKE", "channel": "Afrotechmods"},
            {"title": "Mechanical Engineering Degree Guide", "id": "oRBMrfbp1W4", "channel": "Real Engineering"}
        ]
    },
    {
        "title": "Cybersecurity Analyst",
        "icon": "🌐",
        "description": "Protect computer systems and networks from cyber threats, unauthorized access, and data breaches. High growth field with strong demand.",
        "skills": ["Networking", "Ethical Hacking", "Python", "Risk Assessment"],
        "next_steps": [
            "Learn networking fundamentals",
            "Get CompTIA Security+ certified",
            "Practice on TryHackMe / HackTheBox",
            "Study for CEH certification"
        ],
        "weights": {
            "coding": 8,
            "analytical": 9,
            "problem_solving": 9,
            "research": 7,
            "creativity": 3,
            "communication": 4
        },
        "subject_bonus": {"computers": 15, "mathematics": 7},
        "hobby_bonus": {"building_apps": 10, "experimenting": 8},
        "env_bonus": {"remote": 8, "office": 6},
        "motivation_bonus": {"innovation": 10, "high_salary": 8, "stability": 5},
        "videos": [
            {"title": "Cybersecurity Full Course for Beginners", "id": "U_P23SqJaDc", "channel": "freeCodeCamp"},
            {"title": "How to Get into Cybersecurity", "id": "7WMmkl9lv0k", "channel": "NetworkChuck"},
            {"title": "Day in the Life of a Cybersecurity Analyst", "id": "8aKnBOlOa9s", "channel": "John Hammond"}
        ]
    },
    {
        "title": "Content Writer / Journalist",
        "icon": "✍️",
        "description": "Craft compelling written content for blogs, news, marketing, books, or digital media. Ideal for strong communicators with creative expression.",
        "skills": ["Writing", "Research", "SEO", "Storytelling"],
        "next_steps": [
            "Start a personal blog",
            "Practice writing every day",
            "Study Journalism or Mass Communication",
            "Build a portfolio of published articles"
        ],
        "weights": {
            "communication": 10,
            "creativity": 9,
            "research": 7,
            "analytical": 4,
            "coding": 1,
            "problem_solving": 3
        },
        "subject_bonus": {"literature": 18, "social_science": 8, "arts": 6},
        "hobby_bonus": {"writing": 18, "teaching": 5},
        "env_bonus": {"remote": 10, "creative_studio": 8},
        "motivation_bonus": {"creativity": 12, "recognition": 8},
        "videos": [
            {"title": "How to Become a Content Writer", "id": "XFJx3jDlF6o", "channel": "Neil Patel"},
            {"title": "Freelance Writing for Beginners", "id": "szpHSdFE8bA", "channel": "Elna Cain"},
            {"title": "Content Writing vs Copywriting", "id": "sPYGJXFgCNk", "channel": "Alex Cattoni"}
        ]
    },
    {
        "title": "Teacher / Educator",
        "icon": "📚",
        "description": "Inspire and educate the next generation. Teachers shape society and make a lasting impact across every field of knowledge.",
        "skills": ["Communication", "Patience", "Subject Mastery", "Curriculum Design"],
        "next_steps": [
            "Pursue B.Ed or subject-specific degree",
            "Develop subject expertise",
            "Practice public speaking",
            "Explore EdTech platforms (BYJU's, Coursera)"
        ],
        "weights": {
            "communication": 10,
            "creativity": 6,
            "research": 6,
            "analytical": 5,
            "problem_solving": 5,
            "coding": 1
        },
        "subject_bonus": {"literature": 8, "social_science": 8, "science": 7, "mathematics": 7},
        "hobby_bonus": {"teaching": 18, "writing": 5},
        "env_bonus": {"office": 6},
        "motivation_bonus": {"social_impact": 15, "stability": 10},
        "videos": [
            {"title": "How to Become a Teacher", "id": "mNy6R0f4-p4", "channel": "Teaching Channel"},
            {"title": "Day in the Life of a Teacher", "id": "OWEcJGwVFk8", "channel": "Simply Kinder"},
            {"title": "Future of Education & EdTech", "id": "wX78iKhInsc", "channel": "TED-Ed"}
        ]
    },
    {
        "title": "Civil Engineer",
        "icon": "🏗️",
        "description": "Plan, design, and oversee construction of infrastructure — roads, bridges, buildings, dams. A career that literally builds the world.",
        "skills": ["Structural Analysis", "AutoCAD", "Project Management", "Mathematics"],
        "next_steps": [
            "Study Physics and Maths deeply",
            "Pursue B.Tech in Civil Engineering",
            "Learn AutoCAD and STAAD Pro",
            "Do site internships"
        ],
        "weights": {
            "analytical": 8,
            "problem_solving": 8,
            "research": 5,
            "creativity": 5,
            "coding": 2,
            "communication": 5
        },
        "subject_bonus": {"mathematics": 12, "science": 12},
        "hobby_bonus": {"experimenting": 8, "managing": 7},
        "env_bonus": {"outdoor": 15, "lab": 5},
        "motivation_bonus": {"stability": 10, "social_impact": 8},
        "videos": [
            {"title": "What is Civil Engineering?", "id": "n_0underWGQ", "channel": "Zach Star"},
            {"title": "Civil Engineer Day in the Life", "id": "TsZUVYQnFjM", "channel": "Engineering Mindset"},
            {"title": "Civil Engineering Projects That Changed the World", "id": "X9oF-W4oGKA", "channel": "Practical Engineering"}
        ]
    },
    {
        "title": "Research Scientist",
        "icon": "🧪",
        "description": "Conduct experiments and investigations to expand scientific knowledge. Work in academia, pharma, biotech, or government research labs.",
        "skills": ["Research Methodology", "Statistics", "Lab Techniques", "Scientific Writing"],
        "next_steps": [
            "Excel in science subjects",
            "Pursue a Master's / PhD",
            "Publish papers and join research groups",
            "Apply for research fellowships"
        ],
        "weights": {
            "research": 10,
            "analytical": 9,
            "problem_solving": 8,
            "coding": 5,
            "creativity": 4,
            "communication": 5
        },
        "subject_bonus": {"science": 15, "biology": 12, "mathematics": 8},
        "hobby_bonus": {"experimenting": 18, "analyzing_data": 8},
        "env_bonus": {"lab": 15},
        "motivation_bonus": {"innovation": 12, "social_impact": 8},
        "videos": [
            {"title": "What Does a Research Scientist Do?", "id": "IJCYaXJoUOY", "channel": "Science Careers"},
            {"title": "How to Become a Research Scientist", "id": "JTAfbVs49VE", "channel": "ACS Careers"},
            {"title": "A Day in the Life of a Scientist", "id": "6dJv0mDPUuk", "channel": "PhD & Beyond"}
        ]
    }
]


# =====================================================================
# SALARY & MARKET DATA
# =====================================================================
SALARY_DATA = {
    "Software Engineer":      {"avg_salary": "₹8–30 LPA", "global": "$80K–$160K", "growth": "25%", "demand": "Very High", "demand_clr": "#22c55e", "openings": "4M+ jobs"},
    "Data Scientist":         {"avg_salary": "₹6–25 LPA", "global": "$90K–$150K", "growth": "36%", "demand": "Very High", "demand_clr": "#22c55e", "openings": "2M+ jobs"},
    "Doctor / Physician":     {"avg_salary": "₹8–50 LPA", "global": "$150K–$300K", "growth": "13%", "demand": "High",      "demand_clr": "#0ea5e9", "openings": "800K+ jobs"},
    "Lawyer / Advocate":      {"avg_salary": "₹5–20 LPA", "global": "$70K–$180K", "growth": "10%", "demand": "Moderate",  "demand_clr": "#f97316", "openings": "600K+ jobs"},
    "UI/UX Designer":         {"avg_salary": "₹4–18 LPA", "global": "$60K–$120K", "growth": "23%", "demand": "High",      "demand_clr": "#0ea5e9", "openings": "1M+ jobs"},
    "Business Analyst":       {"avg_salary": "₹5–20 LPA", "global": "$65K–$120K", "growth": "14%", "demand": "High",      "demand_clr": "#0ea5e9", "openings": "1.5M+ jobs"},
    "Mechanical Engineer":    {"avg_salary": "₹4–15 LPA", "global": "$60K–$110K", "growth": "11%", "demand": "Moderate",  "demand_clr": "#f97316", "openings": "700K+ jobs"},
    "Cybersecurity Analyst":  {"avg_salary": "₹6–22 LPA", "global": "$85K–$140K", "growth": "32%", "demand": "Very High", "demand_clr": "#22c55e", "openings": "3M+ jobs"},
    "Content Writer / Journalist": {"avg_salary": "₹2–10 LPA", "global": "$40K–$80K",  "growth": "6%",  "demand": "Moderate",  "demand_clr": "#f97316", "openings": "400K+ jobs"},
    "Teacher / Educator":     {"avg_salary": "₹2–10 LPA", "global": "$40K–$80K",  "growth": "8%",  "demand": "Stable",    "demand_clr": "#64748b", "openings": "2M+ jobs"},
    "Civil Engineer":         {"avg_salary": "₹4–15 LPA", "global": "$60K–$110K", "growth": "11%", "demand": "Moderate",  "demand_clr": "#f97316", "openings": "900K+ jobs"},
    "Research Scientist":     {"avg_salary": "₹5–20 LPA", "global": "$70K–$130K", "growth": "17%", "demand": "High",      "demand_clr": "#0ea5e9", "openings": "500K+ jobs"},
}

# =====================================================================
# TOP COURSES & CERTIFICATIONS
# =====================================================================
COURSES_DATA = {
    "Software Engineer": [
        {"name": "The Complete Web Developer", "platform": "Udemy",    "icon": "🎓", "url": "https://www.udemy.com", "level": "Beginner"},
        {"name": "CS50: Intro to Computer Science", "platform": "edX", "icon": "🏫", "url": "https://cs50.harvard.edu", "level": "Beginner"},
        {"name": "Data Structures & Algorithms", "platform": "Coursera", "icon": "📐", "url": "https://www.coursera.org", "level": "Intermediate"},
        {"name": "AWS Certified Developer",      "platform": "AWS",     "icon": "☁️", "url": "https://aws.amazon.com/certification", "level": "Advanced"},
    ],
    "Data Scientist": [
        {"name": "Python for Data Science",     "platform": "Coursera", "icon": "🐍", "url": "https://www.coursera.org", "level": "Beginner"},
        {"name": "Machine Learning by Stanford","platform": "Coursera", "icon": "🤖", "url": "https://www.coursera.org/learn/machine-learning", "level": "Intermediate"},
        {"name": "Deep Learning Specialization","platform": "Coursera", "icon": "🧠", "url": "https://www.coursera.org", "level": "Advanced"},
        {"name": "Google Data Analytics Certificate","platform": "Google","icon": "📊", "url": "https://grow.google/certificates/data-analytics/", "level": "Beginner"},
    ],
    "Doctor / Physician": [
        {"name": "NEET Preparation Course",     "platform": "Unacademy","icon": "🏥", "url": "https://unacademy.com", "level": "Beginner"},
        {"name": "Human Anatomy & Physiology",  "platform": "Coursera", "icon": "🫀", "url": "https://www.coursera.org", "level": "Intermediate"},
        {"name": "Clinical Skills Masterclass",  "platform": "Osmosis",  "icon": "🩺", "url": "https://www.osmosis.org", "level": "Advanced"},
        {"name": "Medical Ethics & Law",         "platform": "edX",      "icon": "⚖️", "url": "https://www.edx.org", "level": "Intermediate"},
    ],
    "Lawyer / Advocate": [
        {"name": "Introduction to Law",          "platform": "Coursera", "icon": "📜", "url": "https://www.coursera.org", "level": "Beginner"},
        {"name": "Constitutional Law",           "platform": "Yale Law", "icon": "🏛️", "url": "https://law.yale.edu", "level": "Intermediate"},
        {"name": "Contract Law Fundamentals",    "platform": "edX",      "icon": "📋", "url": "https://www.edx.org", "level": "Intermediate"},
        {"name": "CLAT Exam Preparation",        "platform": "Unacademy","icon": "🎓", "url": "https://unacademy.com", "level": "Beginner"},
    ],
    "UI/UX Designer": [
        {"name": "Google UX Design Certificate","platform": "Google",   "icon": "🎨", "url": "https://grow.google/certificates/ux-design/", "level": "Beginner"},
        {"name": "UI Design Bootcamp",           "platform": "Udemy",    "icon": "🖌️", "url": "https://www.udemy.com", "level": "Beginner"},
        {"name": "Interaction Design Foundation","platform": "IDF",      "icon": "🔲", "url": "https://www.interaction-design.org", "level": "Intermediate"},
        {"name": "Advanced Figma Mastery",       "platform": "Skillshare","icon": "✏️", "url": "https://www.skillshare.com", "level": "Advanced"},
    ],
    "Business Analyst": [
        {"name": "Business Analysis Fundamentals","platform": "Udemy",   "icon": "📈", "url": "https://www.udemy.com", "level": "Beginner"},
        {"name": "CBAP Certification Prep",       "platform": "IIBA",    "icon": "🏆", "url": "https://www.iiba.org", "level": "Advanced"},
        {"name": "Excel for Business Analysis",   "platform": "Coursera","icon": "📊", "url": "https://www.coursera.org", "level": "Beginner"},
        {"name": "SQL for Data Analysis",         "platform": "Udacity", "icon": "🗄️", "url": "https://www.udacity.com", "level": "Intermediate"},
    ],
    "Mechanical Engineer": [
        {"name": "AutoCAD 2025 Complete Course", "platform": "Udemy",    "icon": "📐", "url": "https://www.udemy.com", "level": "Beginner"},
        {"name": "Finite Element Analysis",       "platform": "Coursera","icon": "⚙️", "url": "https://www.coursera.org", "level": "Advanced"},
        {"name": "Thermodynamics Masterclass",    "platform": "edX",     "icon": "🔥", "url": "https://www.edx.org", "level": "Intermediate"},
        {"name": "GATE ME Preparation",           "platform": "Unacademy","icon": "🎓", "url": "https://unacademy.com", "level": "Advanced"},
    ],
    "Cybersecurity Analyst": [
        {"name": "CompTIA Security+ Prep",       "platform": "CompTIA",  "icon": "🛡️", "url": "https://www.comptia.org", "level": "Intermediate"},
        {"name": "Ethical Hacking Bootcamp",     "platform": "Udemy",    "icon": "🔓", "url": "https://www.udemy.com", "level": "Intermediate"},
        {"name": "CEH Certification",            "platform": "EC-Council","icon": "🎯", "url": "https://www.eccouncil.org", "level": "Advanced"},
        {"name": "Cybersecurity Fundamentals",   "platform": "IBM",      "icon": "💻", "url": "https://www.ibm.com/training", "level": "Beginner"},
    ],
    "Content Writer / Journalist": [
        {"name": "Content Marketing Certification","platform": "HubSpot","icon": "✍️", "url": "https://academy.hubspot.com", "level": "Beginner"},
        {"name": "SEO Writing Mastery",           "platform": "Udemy",   "icon": "🔍", "url": "https://www.udemy.com", "level": "Intermediate"},
        {"name": "Creative Writing Specialization","platform": "Coursera","icon": "📝", "url": "https://www.coursera.org", "level": "Beginner"},
        {"name": "Journalism Fundamentals",        "platform": "edX",    "icon": "📰", "url": "https://www.edx.org", "level": "Beginner"},
    ],
    "Teacher / Educator": [
        {"name": "Learning How to Learn",         "platform": "Coursera","icon": "🧠", "url": "https://www.coursera.org", "level": "Beginner"},
        {"name": "Teaching with Technology",      "platform": "edX",     "icon": "💡", "url": "https://www.edx.org", "level": "Intermediate"},
        {"name": "Curriculum Design Masterclass", "platform": "Udemy",   "icon": "📚", "url": "https://www.udemy.com", "level": "Intermediate"},
        {"name": "B.Ed Entrance Preparation",     "platform": "Unacademy","icon": "🎓","url": "https://unacademy.com", "level": "Beginner"},
    ],
    "Civil Engineer": [
        {"name": "AutoCAD Civil 3D",              "platform": "Autodesk","icon": "🏗️", "url": "https://www.autodesk.com/education", "level": "Intermediate"},
        {"name": "Structural Analysis Basics",    "platform": "Coursera","icon": "🧱", "url": "https://www.coursera.org", "level": "Beginner"},
        {"name": "Project Management Professional","platform": "PMI",    "icon": "📋", "url": "https://www.pmi.org", "level": "Advanced"},
        {"name": "GATE CE Preparation",           "platform": "Unacademy","icon": "🎓","url": "https://unacademy.com", "level": "Advanced"},
    ],
    "Research Scientist": [
        {"name": "Research Methods & Statistics", "platform": "Coursera","icon": "📊", "url": "https://www.coursera.org", "level": "Intermediate"},
        {"name": "Scientific Writing",            "platform": "edX",     "icon": "📝", "url": "https://www.edx.org", "level": "Beginner"},
        {"name": "Data Analysis with Python",     "platform": "IBM",     "icon": "🐍", "url": "https://www.ibm.com/training", "level": "Intermediate"},
        {"name": "Lab Techniques Masterclass",    "platform": "Udemy",   "icon": "🧪", "url": "https://www.udemy.com", "level": "Intermediate"},
    ],
}

# =====================================================================
# CAREER ROADMAP (top match only)
# =====================================================================
ROADMAP_DATA = {
    "Software Engineer": [
        {"phase": "Foundation",    "icon": "📚", "duration": "0–6 months",   "tasks": ["Learn Python / JavaScript basics", "Study DSA fundamentals", "Build your first website"]},
        {"phase": "Skill Building","icon": "🛠️", "duration": "6–12 months",  "tasks": ["Master one framework (React/Django)", "Contribute to open source", "Build 3 projects on GitHub"]},
        {"phase": "Job Ready",     "icon": "💼", "duration": "12–18 months", "tasks": ["Practice 100+ LeetCode problems", "Apply for internships", "Crack technical interviews"]},
        {"phase": "Professional",  "icon": "🚀", "duration": "18–36 months", "tasks": ["Get first full-time role", "Learn system design", "Pursue cloud certification"]},
    ],
    "Data Scientist": [
        {"phase": "Foundation",    "icon": "📚", "duration": "0–4 months",   "tasks": ["Learn Python & pandas", "Statistics & probability basics", "Explore Kaggle datasets"]},
        {"phase": "Skill Building","icon": "🛠️", "duration": "4–10 months",  "tasks": ["Machine learning with scikit-learn", "Deep learning intro (TensorFlow)", "Complete 2 Kaggle competitions"]},
        {"phase": "Job Ready",     "icon": "💼", "duration": "10–16 months", "tasks": ["Build a data portfolio", "Learn SQL & Tableau", "Apply for data analyst roles first"]},
        {"phase": "Professional",  "icon": "🚀", "duration": "16–30 months", "tasks": ["Specialize (NLP/CV/MLOps)", "Publish a research paper", "Target senior DS roles"]},
    ],
    "Doctor / Physician": [
        {"phase": "Foundation",    "icon": "📚", "duration": "Class 11–12",   "tasks": ["Focus on Biology, Chemistry, Physics", "Prepare for NEET entrance exam", "Join coaching or self-study"]},
        {"phase": "MBBS Degree",   "icon": "🏥", "duration": "5.5 years",    "tasks": ["Complete MBBS from medical college", "Clinical rotations in all departments", "Intern at government hospital"]},
        {"phase": "PG / Specialization","icon": "🩺","duration": "3 years",  "tasks": ["Crack NEET-PG exam", "Choose specialization (Surgery/Cardio etc.)", "Complete MD/MS degree"]},
        {"phase": "Practising",    "icon": "🚀", "duration": "Ongoing",      "tasks": ["Register with Medical Council", "Start practice or join hospital", "Keep updating with CME courses"]},
    ],
    "Lawyer / Advocate": [
        {"phase": "Foundation",    "icon": "📚", "duration": "0–1 year",     "tasks": ["Study CLAT or law entrance exams", "Read newspapers & current affairs daily", "Improve writing & debate skills"]},
        {"phase": "LLB Degree",    "icon": "⚖️", "duration": "3–5 years",    "tasks": ["Complete LLB degree (3yr or 5yr)", "Participate in moot courts", "Intern at law firms"]},
        {"phase": "Enrollment",    "icon": "💼", "duration": "After degree",  "tasks": ["Enroll with Bar Council", "Practice under senior advocate", "Build expertise in one area of law"]},
        {"phase": "Established",   "icon": "🚀", "duration": "5+ years",     "tasks": ["Handle independent cases", "Build a client network", "Consider LLM or specialization"]},
    ],
    "UI/UX Designer": [
        {"phase": "Foundation",    "icon": "📚", "duration": "0–3 months",   "tasks": ["Learn design principles & color theory", "Start with Figma (free)", "Study popular app UX patterns"]},
        {"phase": "Skill Building","icon": "🛠️", "duration": "3–8 months",   "tasks": ["Complete Google UX Certificate", "Design 5 case studies", "Learn user research methods"]},
        {"phase": "Portfolio",     "icon": "💼", "duration": "8–12 months",  "tasks": ["Publish portfolio on Behance/Dribbble", "Do freelance projects", "Apply for junior UX roles"]},
        {"phase": "Professional",  "icon": "🚀", "duration": "12–24 months", "tasks": ["Work at a product company", "Learn motion design (After Effects)", "Mentor junior designers"]},
    ],
    "Business Analyst": [
        {"phase": "Foundation",    "icon": "📚", "duration": "0–4 months",   "tasks": ["Learn Excel, SQL basics", "Study business process fundamentals", "Take BA certification course"]},
        {"phase": "Skill Building","icon": "🛠️", "duration": "4–10 months",  "tasks": ["Master requirements gathering", "Learn Agile & Scrum methodologies", "Work on case studies"]},
        {"phase": "Job Ready",     "icon": "💼", "duration": "10–15 months", "tasks": ["Get CBAP or PMI-PBA certified", "Apply for junior BA positions", "Build stakeholder management skills"]},
        {"phase": "Professional",  "icon": "🚀", "duration": "15–30 months", "tasks": ["Lead business analysis projects", "Learn data visualization tools", "Move toward product management"]},
    ],
    "Mechanical Engineer": [
        {"phase": "Foundation",    "icon": "📚", "duration": "Class 11–12",  "tasks": ["Master Physics & Maths", "Learn basic AutoCAD", "Understand engineering basics"]},
        {"phase": "B.Tech / B.E.", "icon": "⚙️", "duration": "4 years",     "tasks": ["Complete Mechanical Engineering degree", "Do internships at manufacturing firms", "Work on robotics/3D printing projects"]},
        {"phase": "Job Ready",     "icon": "💼", "duration": "After degree", "tasks": ["Crack GATE for PSU jobs", "Learn SolidWorks / ANSYS", "Apply for core engineering roles"]},
        {"phase": "Professional",  "icon": "🚀", "duration": "2–5 years",   "tasks": ["Specialize in robotics/automotive/aerospace", "Pursue M.Tech or MBA", "Lead R&D projects"]},
    ],
    "Cybersecurity Analyst": [
        {"phase": "Foundation",    "icon": "📚", "duration": "0–4 months",   "tasks": ["Learn networking (CCNA basics)", "Study Linux fundamentals", "Set up a home lab"]},
        {"phase": "Certification", "icon": "🛡️", "duration": "4–10 months",  "tasks": ["CompTIA Security+ certification", "Practice on TryHackMe/HackTheBox", "Learn Python for scripting"]},
        {"phase": "Specialization","icon": "💼", "duration": "10–18 months", "tasks": ["Choose path (Pentesting/SOC/Cloud)", "Get CEH or OSCP certification", "Apply for security analyst roles"]},
        {"phase": "Professional",  "icon": "🚀", "duration": "18–36 months", "tasks": ["Work in SOC or Red Team", "Contribute to bug bounty programs", "Pursue CISM or CISSP"]},
    ],
    "Content Writer / Journalist": [
        {"phase": "Foundation",    "icon": "📚", "duration": "0–3 months",   "tasks": ["Read extensively every day", "Start a personal blog", "Study grammar & writing style"]},
        {"phase": "Skill Building","icon": "✍️", "duration": "3–8 months",   "tasks": ["Learn SEO writing basics", "Submit articles to online publications", "Build a writing portfolio"]},
        {"phase": "Job Ready",     "icon": "💼", "duration": "8–12 months",  "tasks": ["Get HubSpot Content Marketing certified", "Apply for content writer / journalist roles", "Build LinkedIn presence"]},
        {"phase": "Professional",  "icon": "🚀", "duration": "12–24 months", "tasks": ["Specialize in a niche (tech/health/finance)", "Earn through freelancing", "Write for top publications"]},
    ],
    "Teacher / Educator": [
        {"phase": "Foundation",    "icon": "📚", "duration": "0–4 years",   "tasks": ["Complete graduation in chosen subject", "Develop subject mastery", "Practice public speaking"]},
        {"phase": "B.Ed Degree",   "icon": "🎓", "duration": "2 years",     "tasks": ["Complete B.Ed (Bachelor of Education)", "Do teaching practice at schools", "Learn modern pedagogy methods"]},
        {"phase": "First Job",     "icon": "💼", "duration": "After degree", "tasks": ["Clear TET / CTET exam", "Apply for government or private school", "Join EdTech platforms"]},
        {"phase": "Growth",        "icon": "🚀", "duration": "2–5 years",   "tasks": ["Pursue M.Ed or subject PG", "Create online courses", "Build school/college career"]},
    ],
    "Civil Engineer": [
        {"phase": "Foundation",    "icon": "📚", "duration": "Class 11–12",  "tasks": ["Focus on Physics & Maths", "Study engineering drawings basics", "Learn about construction materials"]},
        {"phase": "B.Tech / B.E.", "icon": "🏗️", "duration": "4 years",     "tasks": ["Complete Civil Engineering degree", "Do site internships", "Learn AutoCAD Civil 3D & STAAD Pro"]},
        {"phase": "Job Ready",     "icon": "💼", "duration": "After degree", "tasks": ["Crack GATE for PSU/M.Tech", "Apply for site engineer roles", "Get project management exposure"]},
        {"phase": "Professional",  "icon": "🚀", "duration": "3–8 years",   "tasks": ["Become a licensed engineer", "Lead large infrastructure projects", "Pursue PMP certification"]},
    ],
    "Research Scientist": [
        {"phase": "Foundation",    "icon": "📚", "duration": "0–4 years",   "tasks": ["Excel in science subjects (PCB/PCM)", "Develop lab skills", "Read research papers regularly"]},
        {"phase": "Graduation",    "icon": "🔬", "duration": "3–4 years",   "tasks": ["Complete B.Sc in relevant field", "Participate in research projects", "Get lab internships"]},
        {"phase": "Postgraduate",  "icon": "💼", "duration": "2–5 years",   "tasks": ["Complete M.Sc / PhD", "Publish 2–3 research papers", "Apply for research fellowships (CSIR/DBT)"]},
        {"phase": "Scientist",     "icon": "🚀", "duration": "5+ years",    "tasks": ["Join research institute or university", "Lead independent research", "Apply for international collaborations"]},
    ],
}

# =====================================================================
# MOTIVATIONAL QUOTES
# =====================================================================
QUOTES_DATA = {
    "Software Engineer":      {"quote": "Any sufficiently advanced technology is indistinguishable from magic.", "author": "Arthur C. Clarke"},
    "Data Scientist":         {"quote": "In God we trust. All others must bring data.", "author": "W. Edwards Deming"},
    "Doctor / Physician":     {"quote": "Wherever the art of medicine is loved, there is also a love of humanity.", "author": "Hippocrates"},
    "Lawyer / Advocate":      {"quote": "Injustice anywhere is a threat to justice everywhere.", "author": "Martin Luther King Jr."},
    "UI/UX Designer":         {"quote": "Design is not just what it looks like. Design is how it works.", "author": "Steve Jobs"},
    "Business Analyst":       {"quote": "Without data, you're just another person with an opinion.", "author": "W. Edwards Deming"},
    "Mechanical Engineer":    {"quote": "Engineering is the art of directing the great sources of power in nature for the use and convenience of man.", "author": "Thomas Tredgold"},
    "Cybersecurity Analyst":  {"quote": "The only truly secure system is one that is powered off, cast in a block of concrete.", "author": "Gene Spafford"},
    "Content Writer / Journalist": {"quote": "If you don't have time to read, you don't have the time to write.", "author": "Stephen King"},
    "Teacher / Educator":     {"quote": "Education is the most powerful weapon which you can use to change the world.", "author": "Nelson Mandela"},
    "Civil Engineer":         {"quote": "Engineers like to solve problems. If there are no problems handily available, they will create their own problems.", "author": "Scott Adams"},
    "Research Scientist":     {"quote": "The important thing is to not stop questioning. Curiosity has its own reason for existing.", "author": "Albert Einstein"},
}

# =====================================================================
# AI RECOMMENDATION ENGINE
# =====================================================================
def calculate_match_score(career, data):
    """
    Compute a weighted match score (0–100) for a career based on
    the student's assessment data.
    """
    total_weight = 0
    earned_score = 0

    # Skill scores
    for skill, weight in career["weights"].items():
        student_val = float(data.get(skill, 5))
        earned_score += (student_val / 10) * weight
        total_weight += weight

    # Normalize base score to 0–60
    base_score = (earned_score / total_weight) * 60

    # Bonuses (out of 40)
    bonus = 0
    top_subject = data.get("top_subject", "")
    if top_subject in career.get("subject_bonus", {}):
        bonus += career["subject_bonus"][top_subject]

    hobby = data.get("hobby", "")
    if hobby in career.get("hobby_bonus", {}):
        bonus += career["hobby_bonus"][hobby]

    work_env = data.get("work_env", "")
    if work_env in career.get("env_bonus", {}):
        bonus += career["env_bonus"][work_env]

    motivation = data.get("motivation", "")
    if motivation in career.get("motivation_bonus", {}):
        bonus += career["motivation_bonus"][motivation]

    # GPA adjustment: slight boost for high GPA
    gpa = float(data.get("gpa", 5))
    gpa_boost = ((gpa - 5) / 5) * 3  # -3 to +3

    total = base_score + min(bonus, 40) + gpa_boost
    return max(0, min(100, round(total)))


def get_recommendations(form_data):
    """Score all careers and return top 5 sorted by score."""
    scored = []
    for career in CAREER_PROFILES:
        score = calculate_match_score(career, form_data)
        scored.append({**career, "match": score})

    scored.sort(key=lambda x: x["match"], reverse=True)
    return scored[:5]


# =====================================================================
# ROUTES
# =====================================================================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.form.to_dict()

    recommendations = get_recommendations(data)
    top_career = recommendations[0]["title"] if recommendations else "Software Engineer"

    scores = {
        "analytical":     int(data.get("analytical", 5)),
        "coding":         int(data.get("coding", 5)),
        "communication":  int(data.get("communication", 5)),
        "creativity":     int(data.get("creativity", 5)),
        "research":       int(data.get("research", 5)),
    }

    # Attach salary & courses to each recommendation
    for rec in recommendations:
        rec["salary"]  = SALARY_DATA.get(rec["title"], {})
        rec["courses"] = COURSES_DATA.get(rec["title"], [])

    # Roadmap & quote for top career only
    roadmap = ROADMAP_DATA.get(top_career, [])
    quote   = QUOTES_DATA.get(top_career, {"quote": "Believe in yourself.", "author": "Unknown"})

    return render_template(
        "results.html",
        student_name=data.get("student_name", "Student"),
        recommendations=recommendations,
        scores=scores,
        top_career=top_career,
        roadmap=roadmap,
        quote=quote,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
