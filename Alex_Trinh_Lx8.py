'''
Alex Trinh
SYST 230
Lab 8
'''

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)

from expressions import Generator


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.generator = Generator(max_num=10)
        self.questions = []
        self.answers = []
        self.current_question = -1
        self.setup_ui()
        self.generate_quiz()

    def setup_ui(self):
        self.setWindowTitle('Quiz Generator')

        self.resize(400, 400)

        # Main layout
        self.layout = QVBoxLayout()

        # Question label
        self.question_label = QLabel("Question will be here")
        self.layout.addWidget(self.question_label)

        # Answer input
        self.answer_input = QLineEdit()
        self.layout.addWidget(self.answer_input)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()

        # Previous button
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_question)
        self.buttons_layout.addWidget(self.prev_button)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_answer)
        self.buttons_layout.addWidget(self.submit_button, 1)  # The 1 here will center the button

        # Next button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_question)
        self.buttons_layout.addWidget(self.next_button)

        # Add the buttons layout to the main layout
        self.layout.addLayout(self.buttons_layout)

        # Set the main layout
        self.setLayout(self.layout)

    def generate_quiz(self):
        self.questions.clear()
        self.answers.clear()

        # This will generate 5 questions
        for i in range(5):
            q, a = self.generator.generate(level=1)
            self.questions.append(q)
            self.answers.append(a)
        self.current_question = 0
        self.display_question()

    def next_question(self):
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.display_question()

    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.display_question()

    def submit_answer(self):
        # Submit will be later for lab 9, so we will pass this function for now
        pass

    def display_question(self):
        self.question_label.setText(self.questions[self.current_question])
        self.answer_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    quiz_app.show()
    sys.exit(app.exec())
