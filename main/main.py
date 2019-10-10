from simulators.persistent_simulator import PersistentSimulator
from simulators.non_persistent_simulator import NonPersistentSimulator
from argparse import ArgumentParser
import csv

def main(question_num):
    if question_num == 1:
        __run_question_1()
    elif question_num == 2:
        __run_question_2()

# Simulate persistent CSMA/CD protocol
def __run_question_1():
    PersistentSimulator().run_single_iteration()

# Simulate non-persistent CSMA/CD protocol
def __run_question_2():
    pass

# Output results to a csv file
def __write_to_csv(headers, results):
    with open('output.csv', mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(headers)
        for result in results:
            output_writer.writerow(result)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("question_num", 
                        action="store", 
                        choices=[1,2],
                        help="question number to run", 
                        type=int)
    args = parser.parse_args()
    main(args.question_num)