from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit

app  = QApplication([])
window = QWidget()

main_layout = QVBoxLayout()

top_button = QPushButton('ปุ่มด้านบน')
main_layout.addWidget(top_button)

bottom_layout = QHBoxLayout()

input1 = QLineEdit('ช่องที่1')
input2 = QLineEdit('ช่องที่2')
bottom_layout.addWidget(input1)
bottom_layout.addWidget(input2)

main_layout.addLayout(bottom_layout)

window.setLayout(main_layout)


window.setLayout(main_layout)
window.show()
app.exec()






