import streamlit as st
import random
import json

def load_questions_from_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: File '{filepath}' not found.")
        return []
    except json.JSONDecodeError:
        st.error(f"Error: Invalid JSON format in '{filepath}'.")
        return []

def run_quiz():
    # Apply custom CSS for centering and styling
    st.markdown(
        """
        <style>
            .question-container {
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
            }
            .progress-container {
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .incorrect-answer {
                color: red;
                font-weight: bold;
            }
            .correct-answer {
                color: green;
                font-weight: bold;
            }
            .stButton > button {
                width: 100%;
                font-size: 18px;
                padding: 10px;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.title("📈 Stock Market Fundamentals Quiz")

    difficulty = st.sidebar.selectbox("Select Difficulty", ["Beginner", "Intermediate", "Advanced"])
    num_questions = st.sidebar.slider("Select Number of Questions", 5, 50, 5, step=5)

    tab1, tab2 = st.tabs(["Welcome", "Quiz"])

    with tab1:
        st.markdown(
            "<h3 style='text-align: center;'>Welcome to the Stock Market Fundamentals Quiz! 🏆</h3>", 
            unsafe_allow_html=True
        )
        st.write("Test your knowledge and improve your understanding of stock market concepts!")

    with tab2:
        question_files = {
            "Beginner": "beginner_questions.json",
            "Intermediate": "intermediate_questions.json",
            "Advanced": "advanced_questions.json",
        }

        if "selected_questions" not in st.session_state or st.session_state.difficulty != difficulty or st.session_state.num_questions != num_questions:
            questions = load_questions_from_json(question_files[difficulty])
            if not questions:
                st.write("⚠️ No questions available for the selected difficulty.")
                return
            random.shuffle(questions)
            st.session_state.selected_questions = questions[:num_questions]
            st.session_state.difficulty = difficulty
            st.session_state.num_questions = num_questions
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.answers = []

        selected_questions = st.session_state.selected_questions

        if st.session_state.question_index < len(selected_questions):
            question_data = selected_questions[st.session_state.question_index]

            st.markdown(
                f"<div class='progress-container'>Question {st.session_state.question_index + 1} of {num_questions}</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='question-container'>Question {st.session_state.question_index + 1}: {question_data['question']}</div>",
                unsafe_allow_html=True
            )

            options = question_data["options"]
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            def process_answer(selected_answer):
                st.session_state.answers.append({
                    "question": question_data["question"],
                    "selected": selected_answer,
                    "correct": question_data["correct_answer"]
                })
                if selected_answer == question_data["correct_answer"]:
                    st.session_state.score += 1
                st.session_state.question_index += 1
                st.rerun()

            with col1:
                if st.button(options[0], key=f"option_0"):
                    process_answer(options[0])

            with col2:
                if st.button(options[1], key=f"option_1"):
                    process_answer(options[1])

            with col3:
                if st.button(options[2], key=f"option_2"):
                    process_answer(options[2])

            with col4:
                if len(options) > 3 and st.button(options[3], key=f"option_3"):
                    process_answer(options[3])

        else:
            st.markdown(
                f"<h2 style='text-align: center;'>🎯 You scored {st.session_state.score} out of {num_questions}!</h2>",
                unsafe_allow_html=True
            )

            if num_questions > 0:
                percentage = (st.session_state.score / num_questions) * 100
                st.markdown(
                    f"<h3 style='text-align: center;'>That's {percentage:.2f}%!</h3>", 
                    unsafe_allow_html=True
                )
            else:
                st.write("No questions were available.")

            st.markdown("<br><h3>Mistakes & Correct Answers:</h3>", unsafe_allow_html=True)

            for answer in st.session_state.answers:
                if answer["selected"] != answer["correct"]:
                    st.markdown(
                        f"❌ <span class='incorrect-answer'>{answer['question']}</span><br>"
                        f"➡ Your answer: <span class='incorrect-answer'>{answer['selected']}</span><br>"
                        f"✅ Correct answer: <span class='correct-answer'>{answer['correct']}</span><br><br>",
                        unsafe_allow_html=True
                    )

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 2, 2])

            with col2:
                if st.button("🔄 Restart Quiz"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

if __name__ == "__main__":
    run_quiz()
