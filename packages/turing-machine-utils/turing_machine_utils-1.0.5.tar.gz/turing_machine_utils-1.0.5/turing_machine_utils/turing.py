def create_turing_machine(tape, states, transition_rules):
    # Initialize the tape head position
    head_position = 0

    # Run the Turing machine
    current_state = states[0]  # Start from the initial state

    while current_state not in ['accept', 'discard']:
        current_symbol = tape[head_position]

        if (current_state, current_symbol) in transition_rules:
            new_state, new_symbol, move_direction = transition_rules[(current_state, current_symbol)]

            # Update tape
            tape[head_position] = new_symbol

            # Move tape head
            if move_direction == 'R':
                head_position += 1
            elif move_direction == 'L':
                head_position -= 1

            # Update current state
            current_state = new_state
        else:
            print("Undefined transition for state: {}, symbol: {}".format(current_state, current_symbol))
            return 0, tape  # Return 0 for an undefined transition

    if current_state == 'accept':
        print("Turing machine accepted the tape.")
        return 1, tape
    elif current_state == 'discard':
        print("Turing machine discarded the tape.")
        return -1, tape
