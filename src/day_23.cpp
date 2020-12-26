#include <cstdio>
#include <vector>
#include <algorithm>
#include <chrono>
#include <iostream>

typedef int seq_t;

inline seq_t modulo(seq_t i, seq_t div) {
    seq_t v = i%div;
    if (v < 0) {
        v += div;
    }
    return v;
}

seq_t get_max_element(seq_t* array, size_t len) {
    seq_t max_element = array[0];
    for(size_t i = 0; i < 9; ++i) {
        if (array[i] > max_element) {
            max_element = array[i];
        }
    }
	return max_element;
}

inline seq_t decrement(seq_t i, seq_t div) {
    return modulo(i-2,div)+1;
}

void print_array(seq_t* array, size_t len) {
    size_t i = 0;
    for(size_t i = 0; i < len; ++i) {
        printf("%i,", array[i]);
    }
    printf("\n");
}

void advance_sequence(seq_t* array, seq_t max_element, size_t len) {
    // temporarily save set of three
    seq_t temp[3];
    size_t i = 0;
    while(i < 3) {
        temp[i] = array[i+1];
        i += 1;
    }
    // Locate destination
    seq_t destination = decrement(array[0], max_element);
    while (true) {
        // Search the saved values
        bool found = false;
        for (i = 0; i < 3; ++i) {
            if (temp[i] == destination) {
                found = true;
                break;
            }
        }
        if (found) {
            destination = decrement(destination, max_element);
        } else {
            break;
        }
    }
    // Find idx of destination
    size_t destination_idx = 0;
    for (size_t i = 0; i < len; ++i) {
        if (array[i] == destination) {
            destination_idx = i;
            break;
        }
    }
    // Save first value
    seq_t ini = array[0];
    // Set initial value
    array[0] = array[4];
    // Entries before the insertion
    i = 1;
    while(i < destination_idx-3) {
        array[i] = array[i+4];
        i += 1;
    }
    // Copy in the held out values
    size_t j = 0;
    while(j < 3) {
        array[i+j] = temp[j];
        j += 1;
    }
    i += 3;
    // Copy other values
    while(i < len-1) {
        array[i] = array[i+1];
        i += 1;
    }
    // Copy final value.
    array[len-1] = ini;
}

/*
void advance_sequence(seq_t* array, size_t* current_idx_ptr, seq_t max_element, size_t len) {
    size_t current_idx = *current_idx_ptr;
    // temporarily save set of three
    seq_t temp[3];
    size_t i = 0;
    if (current_idx-(len-1-3)>0) {
        while (i < (current_idx-(len-1-3))) {
            temp[i] = array[i];
            i += 1;
        }
    }
    if (i < 3) {
        while ((i < current_idx) && (i < 3)) {
            temp[i] = array[i];
            i += 1;
        }
    }
    // Locate destination
    seq_t destination = decrement(array[current_idx], max_element);
    while (true) {
        // Search the saved values
        bool found = false;
        for (size_t i = 0; i < 3; ++i) {
            if (temp[i] == destination) {
                found = true;
                break;
            }
        }
        if (found) {
            destination = decrement(destination, max_element);
        } else {
            break;
        }
    }
    // Find idx of destination
    size_t destination_idx = 0;
    for (size_t i = 0; i < len; ++i) {
        if (array[i] == destination) {
            destination_idx = i;
            break;
        }
    }
    // Shift array.
    if (current_idx-(len-1-3)>0) {
        
        while (i < (current_idx-(len-1-3))) {
            temp[i] = array[i];
            i += 1;
        }
    }
    
    bool found = false;
    while (!found) {
        size_t i = 0;
        // current_idx = len-1 => 3 to skip at beginning
        // current_idx = len-1-3 => 0 to skip at beginning
        // current_idx = len-1-2 => 1 to skip at beginning
        // current_idx - len-1-3
        if (i <= (current_idx-len-1-3)) {
            // Skip spillover from end of array.
            i += 1;
        }
        if ((i >= current_idx) || (i <= current_idx+3)) {
            // Skip buffered items
            i += 1;
        }
        // Search other items
        if (array[i] == destination) {
            found = true;
            break;
        }
    }
}
*/

size_t hash_array(seq_t* array, size_t len) {
    // https://stackoverflow.com/questions/42701688/using-an-unordered-map-with-arrays-as-keys/42701876
    std::size_t h = 0;
    for (size_t i = 0; i < len; ++i) {
        h ^= ((size_t)array[i]) + 0x9e3779b9 + (h << 6) + (h >> 2);
    }   
    return h;
}

std::vector<size_t> get_history(seq_t* array, size_t len) {
    size_t initial_hash = hash_array(array, len);
    std::vector<size_t> history;
    history.push_back(initial_hash);

    size_t max_number = get_max_element(array, len);
    bool periodic = false;
    while (!periodic) {
        //print_array(array, len);
        advance_sequence(array, max_number, len);
        size_t number_hash = hash_array(array, len);
        if (std::find(history.begin(), history.end(), number_hash) != history.end()) {
            // Now periodic!
            periodic = true;
        }
        history.push_back(number_hash);
    }
    return history;
}

void get_history_timing(seq_t* array, size_t len, size_t num_steps) {
    size_t initial_hash = hash_array(array, len);
    std::vector<size_t> history;
    history.push_back(initial_hash);

    size_t max_number = get_max_element(array, len);
    bool periodic = false;
	size_t step_i = 0;
    auto start = std::chrono::high_resolution_clock::now();
    while ((!periodic) && (step_i < num_steps)) {
        //print_array(array, len);
        advance_sequence(array, max_number, len);
        size_t number_hash = hash_array(array, len);
        if (std::find(history.begin(), history.end(), number_hash) != history.end()) {
            // Now periodic!
            periodic = true;
        }
        history.push_back(number_hash);
        step_i += 1;
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end-start);
    std::cout << num_steps << " steps in " << ((float)duration.count())/(1000.) << " milliseconds." << std::endl;
}

void get_value_in_sequence(seq_t* array, size_t len, std::vector<size_t> history, size_t I) {
    size_t last_hash = history[history.size()-1];
    auto first_hash_it = std::find(history.begin(), history.end(), last_hash);
    auto last_hash_it = history.end()-1;
    size_t period = std::distance(last_hash_it,first_hash_it);
    size_t first_hash_idx = std::distance(history.begin(), first_hash_it);
    size_t runup = first_hash_idx;
    size_t target_hash;
    if (I < runup) {
        target_hash = history[I];
    } else {
        size_t i = I-runup;
        i = modulo(i,period);
        target_hash = history[runup+i];
    }

    seq_t max_number = get_max_element(array, len);
    while (hash_array(array, len) != target_hash) {
        advance_sequence(array, max_number, len);
        //print_array(array, len);
    }
}

int main(int argc, char** argv) {
    char* filepath = argv[1];

    FILE* handle = fopen(filepath, "r");

    char* line_ptr = NULL;
    size_t len;
    ssize_t ret;
    ret = getline(&line_ptr, &len, handle);

    seq_t initial_array[9];

    for(size_t i = 0; i < 9; ++i) {
        initial_array[i] = line_ptr[i]-48;
    }

    delete line_ptr;

    seq_t array[9];
    for(size_t i = 0; i < 9; ++i) {
        array[i] = initial_array[i];
    }

	auto history = get_history(array, 9);

    array[9];
    for(size_t i = 0; i < 9; ++i) {
        array[i] = initial_array[i];
    }

    get_value_in_sequence(array, 9, history, 100);

    size_t idx_1 = 0;
    while (idx_1 < 9) {
        if (array[idx_1] == 1) {
            break;
        }
    }

    printf("Day 23 task 1: ");

    size_t i = idx_1+1;
    while (i < 9) {
        printf("%i", array[i]);
        i += 1;
    }
    i = 0;
    while (i < idx_1) {
        printf("%i", array[i]);
        i += 1;
    }
    printf("\n");

    seq_t array2[1000000];
    for(size_t i = 0; i < 9; ++i) {
        array2[i] = initial_array[i];
    }
    for(size_t i = 10; i < 1000000; ++i) {
        array2[i] = i;
    }

    printf("Gettting long history\n");
    get_history_timing(array2, 1000000, 1000);
	//auto history_2 = get_history(array2, 1000000);
    printf("End history\n");


    return 0;
}
