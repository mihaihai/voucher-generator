#Generating a voucher

import numpy as np

class voucher():

    def __init__(self, type):
        self.value = 0.0
        self.type = type
        self.percentage = 0.0
        self.max_order_value = 0.0
        self.with_money = False
        if self.type == 'value' or self.type == 'percentage':
            self.with_money = True

    def add_value(self, value):
        self.value = value

    def add_percentage(self, percentage):
        self.percentage = percentage

    def add_max_order_value(self, max_order_value):
        self.max_order_value = max_order_value

    def print(self):
        print('Type: '+self.type + ' Percent: '+str(self.percentage) + ' Value: '+str(self.value) + ' Max order: ' + str(self.max_order_value))



def predicted_no_of_issues(mean_no_of_issues, stddev_no_of_issues):
    no_of_issues = int(round(np.random.normal(mean_no_of_issues, stddev_no_of_issues)))
    return no_of_issues

def randomizer_generator(expected_no_of_issues, types_of_vouchers, budget, min_voucher_value):

    vector_of_types = np.random.randint(len(types_of_vouchers), size = expected_no_of_issues)

    expected_no_of_issues_solved_with_money = int(round(expected_no_of_issues / 2))
    expected_mean_voucher_value = budget / expected_no_of_issues_solved_with_money
    exponential_distribution_coef =  expected_mean_voucher_value - min_voucher_value

    if exponential_distribution_coef <= 0:
        print('Budget is too small!')

    vector_of_values = np.random.exponential(exponential_distribution_coef, size = expected_no_of_issues)

    vector_of_percentages = 0.05 * np.random.randint(1, 11, size = expected_no_of_issues)

    return (vector_of_types, vector_of_values, vector_of_percentages)


def generate_vouchers(budget, expected_no_of_issues, types_of_vouchers, min_voucher_value, max_voucher_value):

    (vector_of_types, vector_of_values, vector_of_percentages) = randomizer_generator(expected_no_of_issues, types_of_vouchers, budget, min_voucher_value)

    voucher_list = []

    for issue_index in range(expected_no_of_issues):

        voucher_instance = voucher(types_of_vouchers[vector_of_types[issue_index]])

        if voucher_instance.type == 'percentage':
            voucher_value = round(min(vector_of_values[issue_index] + min_voucher_value, max_voucher_value), 2)
            voucher_percentage = vector_of_percentages[issue_index]
            max_order_value = round(voucher_value / voucher_percentage , 2)

            voucher_instance.add_value(voucher_value)
            voucher_instance.add_percentage(voucher_percentage)
            voucher_instance.add_max_order_value(max_order_value)

        elif voucher_instance.type == 'value':

            voucher_value = round(min(vector_of_values[issue_index] + min_voucher_value, max_voucher_value), 2)
            voucher_instance.add_value(voucher_value)
            voucher_instance.add_max_order_value(voucher_value)

        voucher_list.append(voucher_instance)

    for issue_index in range(expected_no_of_issues):
        voucher_instance = voucher_list[issue_index]
        voucher_instance.print()

    return voucher_list

def test():
    mean_no_of_issues = 200
    stddev_no_of_issues = 20
    types_of_vouchers = ['value', 'percentage', 'apology', 'free delivery']
    min_voucher_value = 5.0
    max_voucher_value = 20.0
    budget = 2000.0
    achieved_budget = 0.0

    expected_no_of_issues = predicted_no_of_issues(mean_no_of_issues, stddev_no_of_issues)
    voucher_list = generate_vouchers(budget, expected_no_of_issues, types_of_vouchers, min_voucher_value, max_voucher_value)

    for issue_index in range(expected_no_of_issues):
        voucher_instance = voucher_list[issue_index]
        voucher_instance.print()
        achieved_budget += voucher_instance.value

    print('Number of issues: ' + str(expected_no_of_issues) +' Achieved budget:' + str(achieved_budget))

    return 1

test()
