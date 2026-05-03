import streamlit as st
import pandas as pd
import json
import os
import random
import time
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Quiz App",
    page_icon="🎯",
    layout="wide"
)

# Questions database
QUESTIONS = {
    "Data Science": [
        {
            "q": "Which algorithm is used for classification"
                 " and regression?",
            "options": ["Random Forest", "K-Means",
                        "PCA", "DBSCAN"],
            "answer": "Random Forest",
            "explanation": "Random Forest works for both "
                           "classification and regression tasks."
        },
        {
            "q": "What does TF-IDF stand for?",
            "options": [
                "Term Frequency-Inverse Document Frequency",
                "Total Features In Data Format",
                "Text Format Identification",
                "Training Features Index Data"
            ],
            "answer": "Term Frequency-Inverse Document Frequency",
            "explanation": "TF-IDF measures word importance "
                           "in a document relative to a corpus."
        },
        {
            "q": "Which metric is used for regression models?",
            "options": ["Accuracy", "F1 Score",
                        "Mean Squared Error", "AUC-ROC"],
            "answer": "Mean Squared Error",
            "explanation": "MSE measures average squared "
                           "difference between predicted "
                           "and actual values."
        },
        {
            "q": "What is overfitting?",
            "options": [
                "Model performs well on training, "
                "poorly on test",
                "Model performs poorly on both",
                "Model performs well on test only",
                "Model has too few parameters"
            ],
            "answer": "Model performs well on training, "
                      "poorly on test",
            "explanation": "Overfitting means the model "
                           "memorized training data but "
                           "cannot generalize."
        },
        {
            "q": "Which library is used for deep learning "
                 "in Python?",
            "options": ["Pandas", "Matplotlib",
                        "TensorFlow", "Seaborn"],
            "answer": "TensorFlow",
            "explanation": "TensorFlow is Google's deep "
                           "learning framework."
        },
        {
            "q": "What does PCA stand for?",
            "options": [
                "Principal Component Analysis",
                "Primary Calculation Algorithm",
                "Predictive Classification Approach",
                "Partial Correlation Analysis"
            ],
            "answer": "Principal Component Analysis",
            "explanation": "PCA reduces dimensionality while "
                           "preserving variance."
        },
        {
            "q": "Which of these is a clustering algorithm?",
            "options": ["Linear Regression",
                        "K-Means", "Logistic Regression",
                        "Decision Tree"],
            "answer": "K-Means",
            "explanation": "K-Means groups data into K "
                           "clusters based on similarity."
        },
        {
            "q": "What is a confusion matrix used for?",
            "options": [
                "Visualizing regression results",
                "Evaluating classification models",
                "Reducing dimensions",
                "Clustering data"
            ],
            "answer": "Evaluating classification models",
            "explanation": "Confusion matrix shows TP, TN, "
                           "FP, FN for classification."
        }
    ],
    "Python": [
        {
            "q": "What is the output of len([1,2,3,4,5])?",
            "options": ["4", "5", "6", "Error"],
            "answer": "5",
            "explanation": "len() returns number of elements. "
                           "List has 5 elements."
        },
        {
            "q": "Which keyword is used to define "
                 "a function in Python?",
            "options": ["func", "define", "def", "function"],
            "answer": "def",
            "explanation": "def is the keyword to define "
                           "functions in Python."
        },
        {
            "q": "What does enumerate() do?",
            "options": [
                "Sorts a list",
                "Returns index and value pairs",
                "Removes duplicates",
                "Reverses a list"
            ],
            "answer": "Returns index and value pairs",
            "explanation": "enumerate() returns (index, value) "
                           "tuples while iterating."
        },
        {
            "q": "Which data structure uses key-value pairs?",
            "options": ["List", "Tuple",
                        "Dictionary", "Set"],
            "answer": "Dictionary",
            "explanation": "Dictionaries store data as "
                           "key:value pairs."
        },
        {
            "q": "What is a lambda function?",
            "options": [
                "A named function",
                "An anonymous one-line function",
                "A recursive function",
                "A class method"
            ],
            "answer": "An anonymous one-line function",
            "explanation": "Lambda creates small anonymous "
                           "functions in one line."
        },
        {
            "q": "What does pip stand for?",
            "options": [
                "Python Installation Package",
                "Pip Installs Packages",
                "Python Index Protocol",
                "Package Integration Program"
            ],
            "answer": "Pip Installs Packages",
            "explanation": "pip is Python's package manager — "
                           "Pip Installs Packages."
        },
        {
            "q": "Which of these is immutable in Python?",
            "options": ["List", "Dictionary",
                        "Set", "Tuple"],
            "answer": "Tuple",
            "explanation": "Tuples cannot be modified "
                           "after creation — they are immutable."
        },
        {
            "q": "What does the 'pass' keyword do?",
            "options": [
                "Exits a loop",
                "Skips current iteration",
                "Does nothing — placeholder",
                "Returns None"
            ],
            "answer": "Does nothing — placeholder",
            "explanation": "pass is a null statement used "
                           "as a placeholder in empty blocks."
        }
    ],
    "Machine Learning": [
        {
            "q": "What is the bias-variance tradeoff?",
            "options": [
                "Balance between model complexity "
                "and generalization",
                "Tradeoff between speed and accuracy",
                "Balance between training and test size",
                "Tradeoff between features and samples"
            ],
            "answer": "Balance between model complexity "
                      "and generalization",
            "explanation": "High bias = underfitting, "
                           "high variance = overfitting."
        },
        {
            "q": "Which activation function outputs "
                 "values between 0 and 1?",
            "options": ["ReLU", "Tanh",
                        "Sigmoid", "Leaky ReLU"],
            "answer": "Sigmoid",
            "explanation": "Sigmoid maps any value to "
                           "(0,1) — used in binary classification."
        },
        {
            "q": "What is gradient descent?",
            "options": [
                "A feature selection method",
                "An optimization algorithm to "
                "minimize loss",
                "A data preprocessing step",
                "A clustering technique"
            ],
            "answer": "An optimization algorithm to "
                      "minimize loss",
            "explanation": "Gradient descent iteratively "
                           "updates parameters to minimize loss."
        },
        {
            "q": "What does dropout do in neural networks?",
            "options": [
                "Removes neurons permanently",
                "Randomly deactivates neurons "
                "during training",
                "Speeds up training",
                "Increases model complexity"
            ],
            "answer": "Randomly deactivates neurons "
                      "during training",
            "explanation": "Dropout prevents overfitting by "
                           "randomly disabling neurons."
        },
        {
            "q": "What is cross-validation used for?",
            "options": [
                "Data cleaning",
                "Feature engineering",
                "Evaluating model performance "
                "reliably",
                "Hyperparameter tuning only"
            ],
            "answer": "Evaluating model performance reliably",
            "explanation": "Cross-validation gives more "
                           "reliable performance estimates "
                           "than a single split."
        },
        {
            "q": "Which ensemble method builds trees "
                 "sequentially?",
            "options": ["Random Forest", "Bagging",
                        "Gradient Boosting", "Voting"],
            "answer": "Gradient Boosting",
            "explanation": "Gradient Boosting builds trees "
                           "sequentially, each correcting "
                           "previous errors."
        },
        {
            "q": "What is the vanishing gradient problem?",
            "options": [
                "Gradients become too large",
                "Gradients become very small "
                "in deep networks",
                "Loss function diverges",
                "Weights become negative"
            ],
            "answer": "Gradients become very small "
                      "in deep networks",
            "explanation": "Vanishing gradients make early "
                           "layers learn very slowly in "
                           "deep networks."
        },
        {
            "q": "What does LSTM stand for?",
            "options": [
                "Long Short-Term Memory",
                "Large Scale Training Model",
                "Linear Sequence Training Method",
                "Layered Sequential Transfer Model"
            ],
            "answer": "Long Short-Term Memory",
            "explanation": "LSTM is a type of RNN designed "
                           "to learn long-term dependencies."
        }
    ],
    "General CS": [
        {
            "q": "What is the time complexity of "
                 "binary search?",
            "options": ["O(n)", "O(n²)",
                        "O(log n)", "O(1)"],
            "answer": "O(log n)",
            "explanation": "Binary search halves the search "
                           "space each step — O(log n)."
        },
        {
            "q": "What does API stand for?",
            "options": [
                "Application Programming Interface",
                "Automated Program Integration",
                "Advanced Python Interface",
                "Application Process Index"
            ],
            "answer": "Application Programming Interface",
            "explanation": "API defines how software "
                           "components communicate."
        },
        {
            "q": "Which data structure is LIFO?",
            "options": ["Queue", "Stack",
                        "Linked List", "Tree"],
            "answer": "Stack",
            "explanation": "Stack is Last In First Out — "
                           "like a stack of plates."
        },
        {
            "q": "What is Git used for?",
            "options": [
                "Database management",
                "Version control",
                "Web hosting",
                "Code compilation"
            ],
            "answer": "Version control",
            "explanation": "Git tracks changes in code "
                           "and enables collaboration."
        },
        {
            "q": "What does SQL stand for?",
            "options": [
                "Structured Query Language",
                "Simple Question Language",
                "Sequential Query Logic",
                "Standard Query List"
            ],
            "answer": "Structured Query Language",
            "explanation": "SQL is used to manage and query "
                           "relational databases."
        },
        {
            "q": "What is recursion?",
            "options": [
                "A loop that runs forever",
                "A function that calls itself",
                "A sorting algorithm",
                "A type of variable"
            ],
            "answer": "A function that calls itself",
            "explanation": "Recursion is when a function "
                           "calls itself with a smaller input."
        },
        {
            "q": "Which HTTP method is used to "
                 "retrieve data?",
            "options": ["POST", "PUT",
                        "DELETE", "GET"],
            "answer": "GET",
            "explanation": "GET retrieves data from a server "
                           "without modifying it."
        },
        {
            "q": "What is a primary key in a database?",
            "options": [
                "The first column always",
                "A unique identifier for each row",
                "An encrypted password",
                "The most important data field"
            ],
            "answer": "A unique identifier for each row",
            "explanation": "Primary key uniquely identifies "
                           "each record in a table."
        }
    ]
}

# Leaderboard persistence
LB_FILE = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(LB_FILE):
        with open(LB_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leaderboard(lb):
    with open(LB_FILE, 'w') as f:
        json.dump(lb, f, indent=2)

# Session state init
if 'quiz_started'   not in st.session_state:
    st.session_state.quiz_started   = False
if 'current_q'      not in st.session_state:
    st.session_state.current_q      = 0
if 'score'          not in st.session_state:
    st.session_state.score          = 0
if 'answers'        not in st.session_state:
    st.session_state.answers        = []
if 'questions'      not in st.session_state:
    st.session_state.questions      = []
if 'quiz_complete'  not in st.session_state:
    st.session_state.quiz_complete  = False
if 'player_name'    not in st.session_state:
    st.session_state.player_name    = ""
if 'category'       not in st.session_state:
    st.session_state.category       = ""
if 'start_time'     not in st.session_state:
    st.session_state.start_time     = None

# Tabs
tab1, tab2, tab3 = st.tabs([
    "🎯 Play Quiz",
    "🏆 Leaderboard",
    "📊 Stats"
])

# Tab 1 — Quiz
with tab1:
    if not st.session_state.quiz_started \
       and not st.session_state.quiz_complete:
        st.markdown("### 👋 Welcome to the Quiz!")
        st.markdown("Test your knowledge in Data Science, "
                    "Python, ML and CS fundamentals.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            player_name = st.text_input(
                "Your name:",
                placeholder="Enter your name"
            )
            category = st.selectbox(
                "Choose category:",
                list(QUESTIONS.keys()) + ["🎲 Random Mix"]
            )
            num_q = st.slider(
                "Number of questions:",
                5, 8, 8
            )

        with col2:
            st.markdown("### 📋 Rules")
            st.info("""
            - Read each question carefully
            - Select your answer
            - Get instant feedback
            - Your score goes on the leaderboard
            - All the best! 🚀
            """)

        if st.button("🚀 Start Quiz", type="primary"):
            if not player_name.strip():
                st.warning("Please enter your name!")
            else:
                if category == "🎲 Random Mix":
                    all_q = []
                    for qs in QUESTIONS.values():
                        all_q.extend(qs)
                    selected = random.sample(
                        all_q,
                        min(num_q, len(all_q))
                    )
                else:
                    selected = random.sample(
                        QUESTIONS[category],
                        min(num_q,
                            len(QUESTIONS[category]))
                    )

                st.session_state.quiz_started  = True
                st.session_state.questions     = selected
                st.session_state.current_q     = 0
                st.session_state.score         = 0
                st.session_state.answers       = []
                st.session_state.player_name   = \
                    player_name
                st.session_state.category      = category
                st.session_state.quiz_complete = False
                st.session_state.start_time    = \
                    time.time()
                st.rerun()

    elif st.session_state.quiz_started \
         and not st.session_state.quiz_complete:
        questions = st.session_state.questions
        current   = st.session_state.current_q
        total     = len(questions)

        if current < total:
            # Progress
            progress = current / total
            st.progress(progress)
            st.markdown(
                f"**Question {current+1} of {total}** "
                f"| Score: {st.session_state.score}"
                f"/{current} "
                f"| Player: "
                f"{st.session_state.player_name}"
            )
            st.markdown("---")

            q    = questions[current]
            opts = q['options'].copy()
            random.shuffle(opts)

            st.markdown(f"### {current+1}. {q['q']}")
            choice = st.radio(
                "Select your answer:",
                opts,
                key=f"q_{current}"
            )

            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("Submit Answer",
                             type="primary"):
                    correct = choice == q['answer']
                    if correct:
                        st.session_state.score += 1
                        st.success(
                            "✅ Correct! "
                            + q['explanation'])
                    else:
                        st.error(
                            f"❌ Wrong! "
                            f"Correct: **{q['answer']}**"
                            f"\n\n{q['explanation']}"
                        )

                    st.session_state.answers.append({
                        'question': q['q'],
                        'your_answer': choice,
                        'correct_answer': q['answer'],
                        'correct': correct
                    })
                    st.session_state.current_q += 1

                    if st.session_state.current_q \
                            >= total:
                        st.session_state.quiz_complete \
                            = True
                        st.session_state.quiz_started \
                            = False

                        # Save to leaderboard
                        elapsed = time.time() - \
                            st.session_state.start_time
                        lb = load_leaderboard()
                        lb.append({
                            'name':     st.session_state
                                        .player_name,
                            'score':    st.session_state
                                        .score,
                            'total':    total,
                            'percent':  round(
                                st.session_state.score
                                / total * 100, 1),
                            'category': st.session_state
                                        .category,
                            'time':     round(elapsed),
                            'date':     datetime.now()
                                        .strftime(
                                '%Y-%m-%d %H:%M')
                        })
                        lb.sort(
                            key=lambda x: (
                                -x['percent'],
                                x['time']
                            )
                        )
                        save_leaderboard(lb[:50])
                    st.rerun()

    elif st.session_state.quiz_complete:
        score   = st.session_state.score
        total   = len(st.session_state.questions)
        percent = score / total * 100

        if percent >= 80:
            st.balloons()
            grade = "🏆 Excellent!"
            color = "#2ecc71"
        elif percent >= 60:
            grade = "👍 Good Job!"
            color = "#f39c12"
        else:
            grade = "📚 Keep Practicing!"
            color = "#e74c3c"

        st.markdown(
            f"<h2 style='text-align:center; "
            f"color:{color}'>{grade}</h2>",
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Score",    f"{score}/{total}")
        col2.metric("Percent",  f"{percent:.0f}%")
        col3.metric("Category",
                    st.session_state.category[:15])
        col4.metric("Player",
                    st.session_state.player_name[:10])

        # Answer review
        st.markdown("### 📋 Answer Review")
        for i, ans in enumerate(
            st.session_state.answers, 1
        ):
            icon = "✅" if ans['correct'] else "❌"
            with st.expander(
                f"{icon} Q{i}: {ans['question'][:50]}"
            ):
                st.write(
                    f"**Your answer:** "
                    f"{ans['your_answer']}"
                )
                st.write(
                    f"**Correct answer:** "
                    f"{ans['correct_answer']}"
                )

        if st.button("🔄 Play Again", type="primary"):
            st.session_state.quiz_started  = False
            st.session_state.quiz_complete = False
            st.session_state.current_q     = 0
            st.session_state.score         = 0
            st.session_state.answers       = []
            st.rerun()

# Tab 2 — Leaderboard
with tab2:
    st.markdown("### 🏆 Leaderboard")
    lb = load_leaderboard()

    if not lb:
        st.info("No scores yet. Play a quiz first!")
    else:
        df_lb = pd.DataFrame(lb)

        # Top 3 podium
        top3 = df_lb.head(3)
        cols = st.columns(3)
        medals = ["🥇", "🥈", "🥉"]
        for i, (_, row) in enumerate(top3.iterrows()):
            cols[i].metric(
                f"{medals[i]} {row['name']}",
                f"{row['percent']}%",
                f"{row['score']}/{row['total']}"
            )

        st.markdown("---")
        st.markdown("### Full Rankings")
        display = df_lb[
            ['name', 'score', 'total',
             'percent', 'category',
             'time', 'date']
        ].copy()
        display.index = range(1, len(display) + 1)
        display.columns = [
            'Name', 'Score', 'Total',
            'Percent %', 'Category',
            'Time (s)', 'Date'
        ]
        st.dataframe(display,
                     use_container_width=True)

# Tab 3 — Stats
with tab3:
    st.markdown("### 📊 Quiz Statistics")
    lb = load_leaderboard()

    if len(lb) < 2:
        st.info("Play more quizzes to see stats!")
    else:
        df_s = pd.DataFrame(lb)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Score Distribution")
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_s['percent'], bins=10,
                    color='#3498db',
                    edgecolor='black',
                    alpha=0.8)
            ax.axvline(df_s['percent'].mean(),
                       color='#e74c3c',
                       linewidth=2,
                       label=f"Avg: "
                             f"{df_s['percent'].mean():.1f}%")
            ax.set_title('Score Distribution',
                         fontsize=12)
            ax.set_xlabel('Score (%)')
            ax.set_ylabel('Count')
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.markdown("#### Scores by Category")
            cat_avg = df_s.groupby(
                'category')['percent'].mean()
            fig2, ax2 = plt.subplots(figsize=(7, 4))
            colors = plt.cm.RdYlGn(
                cat_avg.values / 100)
            ax2.bar(cat_avg.index, cat_avg.values,
                    color=colors, edgecolor='black')
            ax2.set_title('Avg Score by Category',
                          fontsize=12)
            ax2.set_ylabel('Average Score (%)')
            ax2.set_ylim(0, 100)
            plt.xticks(rotation=30, ha='right')
            plt.tight_layout()
            st.pyplot(fig2)

        st.markdown("#### Overall Stats")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Total Games",
                  len(df_s))
        s2.metric("Average Score",
                  f"{df_s['percent'].mean():.1f}%")
        s3.metric("Highest Score",
                  f"{df_s['percent'].max():.1f}%")
        s4.metric("Top Player",
                  df_s.loc[
                      df_s['percent'].idxmax(),
                      'name'
                  ])

st.markdown("---")
st.markdown(
    "Built by **Jyotiraditya** | "
    "Quiz App with Live Leaderboard"
)