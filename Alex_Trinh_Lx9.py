'''
Alex Trinh
SYST 230
Lab Lx9
'''
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)

# Ensure the Generator class from expressions module is implemented to generate questions and answers.
from expressions import Generator

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize the question generator with a maximum number of 10
        self.generator = Generator(max_num=10)
        self.questions = []
        self.answers = []
        self.user_answers = []
        self.current_question = -1
        self.score = 0
        self.setup_ui()
        self.generate_quiz()

    def setup_ui(self):
        #Setup the user interface elements and layouts
        self.setWindowTitle('Quiz Generator')
        self.resize(400, 400)

        # Main vertical layout
        self.layout = QVBoxLayout()

        # Display area for the quiz question
        self.question_label = QLabel("Question will be here")
        self.layout.addWidget(self.question_label)

        # Input field for user answers
        self.answer_input = QLineEdit()
        self.layout.addWidget(self.answer_input)

        # Horizontal layout for navigation and action buttons
        self.buttons_layout = QHBoxLayout()

        # Button to navigate to the previous question
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_question)
        self.buttons_layout.addWidget(self.prev_button)

        # Button to submit the answer
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_answer)
        self.buttons_layout.addWidget(self.submit_button)

        # Button to navigate to the next question
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_question)
        self.buttons_layout.addWidget(self.next_button)

        # Reset quiz button
        self.reset_button = QPushButton("Reset Quiz")
        self.reset_button.clicked.connect(self.reset_quiz)
        self.layout.addWidget(self.reset_button)

        # Generate new quiz button
        self.new_quiz_button = QPushButton("New Quiz")
        self.new_quiz_button.clicked.connect(self.generate_quiz)
        self.layout.addWidget(self.new_quiz_button)

        # Integrating all layouts into the main window
        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

    def generate_quiz(self):
        #Generates a new set of questions and answers
        self.questions.clear()
        self.answers.clear()
        self.user_answers = [None] * 5
        self.score = 0

        # Generate 5 questions and answers
        for i in range(5):
            q, a = self.generator.generate(level=1)
            self.questions.append(q)
            self.answers.append(a)
        self.current_question = 0
        self.display_question()

    def next_question(self):
        #Go to the next question, saving the current answer
        self.save_current_answer()
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.display_question()

    def prev_question(self):
        #Go back to the previous question, saving the current answer
        self.save_current_answer()
        if self.current_question > 0:
            self.current_question -= 1
            self.display_question()

    def submit_answer(self):
        #Submit all answers, calculate score, and show corrections if needed
        self.save_current_answer()
        self.calculate_score()
        if self.score == len(self.questions):
            QMessageBox.information(self, "Quiz Completed", "Perfect score! You got all answers right.")
        else:
            correction_text = self.generate_correction_text()
            QMessageBox.information(self, "Quiz Completed", f"Your score is {self.score}/{len(self.questions)}.\n\n{correction_text}")

    def generate_correction_text(self):
        #Generate a detailed text showing which answers were incorrect along with the correct answers
        correction_text = ""
        for i in range(len(self.questions)):
            if str(self.answers[i]) != self.user_answers[i]:
                correction_text += f"Question {i+1}: Your answer was '{self.user_answers[i]}' (Incorrect). Correct answer: '{self.answers[i]}'\n"
        return correction_text

    def save_current_answer(self):
        #Save the answer provided by the user for the current question
        self.user_answers[self.current_question] = self.answer_input.text()

    def calculate_score(self):
        #Calculate the user's score based on correct answers
        self.score = sum(1 for i in range(len(self.answers)) if str(self.answers[i]) == self.user_answers[i])

    def reset_quiz(self):
        #Reset all answers and start the quiz over from the first question
        self.user_answers = [None] * len(self.questions)
        self.current_question = 0
        self.display_question()

    def display_question(self):
        #Display the current question and any existing user answer
        self.question_label.setText(self.questions[self.current_question])
        answer = self.user_answers[self.current_question]
        if answer is not None:
            self.answer_input.setText(answer)
        else:
            self.answer_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    quiz_app.show()
    sys.exit(app.exec())
