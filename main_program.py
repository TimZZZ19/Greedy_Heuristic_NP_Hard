import random as rd


def find_largest_sets(sets):
    max_count = -1
    largest_sets = []

    for sets_idx in range(0, len(sets)):
        if len(sets[sets_idx]) > max_count:
            max_count = len(sets[sets_idx])  # First, find the largest count;

    for sets_j in range(0, len(sets)):
        if len(sets[sets_j][0]) != 0 and len(sets[sets_j]) == max_count:
            largest_sets.append(sets_j)  # Then, find the set whose pair count matches max_count and append its index;

    return largest_sets


def update_sets(input_all_pairs, input_sets, input_pick, input_picked_set):
    for set_idx in range(0, len(input_picked_set)):
        input_all_pairs.remove(input_picked_set[set_idx])

    for set_idx in range(0, len(input_picked_set)):
        for sets_idx in range(0, len(input_sets)):
            if sets_idx == input_pick:
                continue
            if input_picked_set[set_idx] in input_sets[sets_idx]:
                if len(input_sets[sets_idx]) == 1:
                    input_sets[sets_idx] = [[]]
                else:
                    input_sets[sets_idx].remove(input_picked_set[set_idx])

    input_sets[input_pick] = [[]]


def form_sets(all_lines, all_pairs, all_pairs_in_y):
    sets = []
    for lines_idx in range(0, len(all_lines)):
        single_set = []
        for pairs_idx in range(0, len(all_pairs)):
            if all_lines[lines_idx][0] == 'v':
                if all_pairs[pairs_idx][0] < all_lines[lines_idx][1] < all_pairs[pairs_idx][1]:
                    single_set.append(all_pairs[pairs_idx])
            if all_lines[lines_idx][0] == 'h':
                if min(all_pairs_in_y[pairs_idx][0], all_pairs_in_y[pairs_idx][1]) \
                        < all_lines[lines_idx][1] \
                        < max(all_pairs_in_y[pairs_idx][0], all_pairs_in_y[pairs_idx][1]):
                    single_set.append(all_pairs[pairs_idx])
        sets.append(single_set)
    return sets


def get_ans(input_y, input_n):
    # Find all the horizontal pairs;
    all_pairs = []

    for i in range(1, input_n + 1):
        for j in range(i + 1, input_n + 1):
            all_pairs.append([i, j])

    # Name each point after y;
    points_by_y = input_y

    # Find all the vertical pairs based on points_by_y;
    all_pairs_in_y = []
    for i in range(0, input_n):
        for j in range(i + 1, input_n):
            all_pairs_in_y.append([points_by_y[i], points_by_y[j]])

    # Generate all the lines;
    all_lines = []

    for i in range(1, input_n):
        all_lines.append(['v', i + 0.5])

    for j in range(1, input_n):
        all_lines.append(['h', j + 0.5])

    # Form sets using lines and pairs;
    sets = form_sets(all_lines, all_pairs, all_pairs_in_y)

    # Following is the greedy procedure;
    ans = []
    while len(all_pairs) > 0:
        largest_sets = find_largest_sets(sets)
        pick = rd.sample(largest_sets, 1)[0]
        picked_set = sets[pick]
        picked_line = all_lines[pick]
        ans.append(picked_line)
        update_sets(all_pairs, sets, pick, picked_set)

    return ans


def get_filename_sequence(input_filename, input_n):
    seq = []
    for postfix in range(1, input_n + 1):
        if 0 < postfix < 10:
            filename = input_filename + "0" + str(postfix) + ".txt"
        else:
            filename = input_filename + str(postfix) + ".txt"
        seq.append(filename)
    return seq


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print("\n" + "\t" + '''This program reads input data in a sequence of "instance01.txt, instance02.txt, ... ..., instancen.txt"; 
    so in your space where you put this program you should have all the n files using this naming sequence. 
    The output will be a sequence of "solution01.txt, solution02.txt, ... ..., solutionn.txt" stored in 
    the same folder with the input files and this program. ''')

    n = int(input('\n' + '\t' + 'Specify your n, where n is the number of files in your folder:' + '\n' + '\t'))

    print('\n' + '\t' + 'Programming running ...' + '\n' + '\t')

    # Come up with all the input filenames;
    inputs = get_filename_sequence("instance", n)

    # Come up with all the output filenames;
    outputs = get_filename_sequence("solution", n)

    for idx in range(0, n):
        curr_input_filename = inputs[idx]
        curr_output_filename = outputs[idx]

        # Read the file;
        with open(curr_input_filename) as file:
            lines = []
            for line in file:
                lines.append(line)

        for line_idx in range(0, len(lines)):
            lines[line_idx] = lines[line_idx].strip("\n")

        # Get n, y;
        n = int(lines[0])
        y = []  # n and y are used for calculating the final answer;
        for index in range(1, len(lines)):
            y.append(int(lines[index].split(' ')[1]))

        # This is where all the calculation is, the meat of the program;
        result = get_ans(y, n)

        # Saving the result into txt;
        f = open(curr_output_filename, "w+")
        f.write(str(len(result)) + '\n')
        for index in range(0, len(result)):
            f.write(str(result[index][0]) + ' ' + str(result[index][1]) + '\n')
        f.close()
