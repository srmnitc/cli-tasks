from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import json

questions = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': 'What\'s your first name',
    },
    
    {
        'type': 'input',
        'name': 'surname',
        'message': 'What\'s your surname',
    }
]

answers = prompt(questions)
print answers['first_name']
#ltes try to append a field to json

with open("test.json", "w") as write_file:
    json.dump(answers, write_file)
#print_json(answers)  # use the answers as input for your app