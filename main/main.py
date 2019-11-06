from simulators.persistent_simulator import PersistentSimulator
from simulators.non_persistent_simulator import NonPersistentSimulator
from argparse import ArgumentParser
import csv

def main(question_num):
    if question_num == 0:
        __run_question_0()
    elif question_num == 1:
        __run_question_1()
    elif question_num == 2:
        __run_question_2()

# Verify if initial simulation results are correct
def __run_question_0():
    results = []
    for i in [20, 40, 60, 80, 100]:
        metrics = PersistentSimulator(num_nodes=i, arrival_rate=5, persistent_flag=True).run_single_iteration()
        results.append([i, metrics[0], metrics[1]])
        __write_to_csv(['num_nodes', 'efficiency', 'throughput'], results)

# Simulate persistent CSMA/CD protocol
def __run_question_1():
    results = []
    for arrival_rate in [7, 10, 20]:
        for num_nodes in [20, 40, 60, 80, 100]:
            metrics = PersistentSimulator(num_nodes=num_nodes, arrival_rate=arrival_rate, persistent_flag=True).run_single_iteration()
            results.append([arrival_rate, num_nodes, metrics[0], metrics[1]])
            __write_to_csv(['arrival_rate', 'num_nodes', 'efficiency', 'throughput'], results)
    

# Simulate non-persistent CSMA/CD protocol
def __run_question_2():
    results = []
    for arrival_rate in [7, 10, 20]:
        for num_nodes in [20, 40, 60, 80, 100]:
            metrics = PersistentSimulator(num_nodes=num_nodes, arrival_rate=arrival_rate, persistent_flag=False).run_single_iteration()
            results.append([arrival_rate, num_nodes, metrics[0], metrics[1]])
            __write_to_csv(['arrival_rate', 'num_nodes', 'efficiency', 'throughput'], results)
 
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
                        choices=[0,1,2],
                        help="question number to run", 
                        type=int)
    args = parser.parse_args()
    main(args.question_num)