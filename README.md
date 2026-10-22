# Spite benchmarks

Every case here is one small program written four ways, so you can see what the Spite compiler makes of a plain
program against what a person gets from C and from Python for the same work:

| file | what it is |
|---|---|
| `<case>.spite` | the plain Spite program, written the obvious way; its other classes are beside it |
| `naive.c` | the same program in C the way a person writes it without tuning: the same loops, the same objects allocated the same way |
| `expert.c` | the same computation tuned by hand by someone who knows the machine: any layout, any loop, as long as it does all the work and prints the same answer |
| `naive.py` | the same program in plain idiomatic Python 3, the way a Python programmer writes it, standard library only |

Every form prints the same answer on its standard output and times its own work, printing `microseconds <n>` on its
error output, so starting a process (and the Python interpreter) is not counted. The C programs read the clock
through [clock.h](clock.h), the Python ones through `time.perf_counter_ns()`, the Spite ones through
`clock.elapsed_nanoseconds()`.

**Only the result counts.** Any form is fair as long as it prints the same answer: if `expert.c` folds work away
or computes the answer another way, that is the target, and the compiler must learn to reach it from the unchanged
Spite program.

## Running

```
python run.py                                  every case, with the master compiler
python run.py --compiler=path/to/spite.exe a_case another_case
python run.py --runs=7 --budget=30             the defaults
```

For every case named (all of them when none is), `run.py` builds the Spite program with the compiler given (by
default `D:/Projects/SpiteCompiler/.spite/spite.exe`) and both C programs with clang `-O2` (from `CC`, the `PATH`,
Visual Studio's LLVM, or `zig cc`), runs the four forms interleaved in the case's folder, keeps the best of seven
runs of each, checks that every form prints exactly what `naive.c` prints, and rewrites the rows of the cases it
timed in the table below (the others are kept, from `results.json`). A form whose runs pass `--budget` seconds in
all stops repeating, so a slow form (most often the Python one) is timed fewer than seven times. A row timed with
another compiler than master says so in its last column, so an optimisation can be timed on its own cases first.

The ratios are Spite's time divided by the other form's: below 1.00 Spite is faster, above it slower. The table is
ordered by Spite's time over expert C's, worst first; the cases that do not build or answer differently come last,
with the reason.

## Where the cases come from

The cases are the benchmarks the language repository kept beside its C backend, with the Spite rewritten for the
current compiler, which writes machine code: each program loads the library itself, its entry function is named
after its folder, and it reads the clock around its work. Two use what the language now leaves to the compiler:
`an_allocator_set_after_construction_is_where_the_object_is_made` no longer sets an arena (a program cannot name
one), and `the_compiler_places_memory` fills a `List<Long>` where it allocated memory by hand. The C programs are
unchanged, and so is what every case computes.

Cases that measured the C backend, or measured no time at all, were left behind: the build flags and translation
units of the C (`a_release_build_is_o3_with_link_time_optimisation`, `a_release_is_inlined_in_every_unit`,
`the_c_is_compiled_in_parallel_units_and_cached`, `tree_shaking_the_generated_c`), what an executable carries
(`crash_text_out_of_the_binary`, `the_fault_handler_is_in_every_program`, `short_symbols_are_inline_text`,
`singletons_that_hold_nothing_are_static_objects`, `identical_functions_are_folded_into_one`,
`a_foreign_name_is_never_copied`, `reflection_symbols_and_registries_only_where_read`, `proofs_that_survive_a_call`,
`hidden_async_await_as_compile_time_state_machines`, `other_optimisations`), and the development builds
(`a_reload_compiles_only_the_classes_that_changed`, `repl_live_reload_and_debug_machinery_only_in_those_builds`,
`what_a_hot_reload_build_carries_so_its_objects_can_move`).

## Every case

<!-- results -->
| case | Spite µs | naive C µs | expert C µs | Python µs | Spite / expert C | Spite / Python | problem |
|---|---|---|---|---|---|---|---|
| [maths_on_constants_is_worked_out_while_compiling](maths_on_constants_is_worked_out_while_compiling/) | 229 467 641 | 13 332 | 2 809 | 29 437 453 | 81690.15 | 7.80 |  |
| [a_word_inflected_while_compiling](a_word_inflected_while_compiling/) | 33 177 871 | 273 516 | 3 350 | 912 808 | 9903.84 | 36.35 |  |
| [a_dictionary_written_out_and_only_read_by_literal_keys_is_folded](a_dictionary_written_out_and_only_read_by_literal_keys_is_folded/) | 14 683 052 | 368 092 | 5 983 | 1 473 242 | 2454.13 | 9.97 |  |
| [a_row_of_borrowed_items_lives_in_the_frame](a_row_of_borrowed_items_lives_in_the_frame/) | 1 839 683 | 7 241 | 3 108 | 5 370 045 | 591.92 | 0.34 |  |
| [a_number_read_from_bytes_is_one_load](a_number_read_from_bytes_is_one_load/) | 15 965 741 | 54 173 | 33 246 | 39 513 506 | 480.23 | 0.40 |  |
| [thread_safety_for_singletons_the_cheapest_safe_form](thread_safety_for_singletons_the_cheapest_safe_form/) | 142 585 | 162 280 | 375 | 1 399 161 | 380.23 | 0.10 |  |
| [a_numbers_bits_are_read_in_place](a_numbers_bits_are_read_in_place/) | 8 479 953 | 92 814 | 23 752 | 40 720 763 | 357.02 | 0.21 |  |
| [reading_through_a_type_without_counting](reading_through_a_type_without_counting/) | 1 820 177 | 9 613 | 5 448 | 5 536 438 | 334.10 | 0.33 |  |
| [template_chains_run_as_one_loop](template_chains_run_as_one_loop/) | 449 701 | 81 852 | 1 627 | 1 763 694 | 276.40 | 0.25 |  |
| [a_local_list_of_known_size_lives_in_the_frame](a_local_list_of_known_size_lives_in_the_frame/) | 6 520 508 | 24 291 | 23 692 | 4 082 545 | 275.22 | 1.60 |  |
| [a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked](a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked/) | 4 478 468 | 153 341 | 16 774 | 14 642 089 | 266.99 | 0.31 |  |
| [a_write_back_of_what_the_slot_already_holds_is_not_written](a_write_back_of_what_the_slot_already_holds_is_not_written/) | 147 851 | 5 261 | 567 | 2 025 285 | 260.76 | 0.07 |  |
| [a_walked_crash_lines_read_is_the_rows_read](a_walked_crash_lines_read_is_the_rows_read/) | 1 236 650 | 18 321 | 4 767 | 6 609 820 | 259.42 | 0.19 |  |
| [text_building](text_building/) | 2 542 909 | 85 975 | 9 870 | 592 367 | 257.64 | 4.29 |  |
| [a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one](a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one/) | 249 619 | 78 565 | 1 018 | 378 201 | 245.21 | 0.66 |  |
| [defaults_the_constructor_replaces_are_never_made](defaults_the_constructor_replaces_are_never_made/) | 85 053 | 42 680 | 347 | 313 247 | 245.11 | 0.27 |  |
| [copies_that_cost_nothing](copies_that_cost_nothing/) | 4 009 936 | 22 840 | 16 536 | 6 768 985 | 242.50 | 0.59 |  |
| [objects_that_never_leave_their_function_live_in_the_frame](objects_that_never_leave_their_function_live_in_the_frame/) | 3 450 321 | 1 022 853 | 14 721 | 56 472 044 | 234.38 | 0.06 |  |
| [image_filter_over_planes](image_filter_over_planes/) | 3 739 188 | 265 978 | 22 589 | 8 030 628 | 165.53 | 0.47 |  |
| [text_joined_in_one_piece](text_joined_in_one_piece/) | 517 950 | 97 293 | 3 439 | 136 080 | 150.61 | 3.81 |  |
| [a_list_of_lists_filled_again_keeps_each_lists_room](a_list_of_lists_filled_again_keeps_each_lists_room/) | 906 696 | 307 716 | 6 645 | 1 167 971 | 136.45 | 0.78 |  |
| [singletons_made_on_first_use_never_counted](singletons_made_on_first_use_never_counted/) | 699 819 | 216 216 | 5 842 | 7 406 893 | 119.79 | 0.09 |  |
| [report_over_records](report_over_records/) | 2 124 541 | 594 987 | 22 864 | 7 261 544 | 92.92 | 0.29 |  |
| [a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once](a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once/) | 280 977 | 305 675 | 3 074 | 4 781 909 | 91.40 | 0.06 |  |
| [a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame](a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame/) | 369 259 | 4 024 | 4 059 | 447 461 | 90.97 | 0.83 |  |
| [game_maths](game_maths/) | 155 599 | 2 279 | 1 762 | 8 352 160 | 88.31 | 0.02 |  |
| [a_function_taking_a_type_is_compiled_per_class](a_function_taking_a_type_is_compiled_per_class/) | 4 539 694 | 52 900 | 53 124 | 14 958 061 | 85.45 | 0.30 |  |
| [objects_of_one_class_sit_together](objects_of_one_class_sit_together/) | 204 043 | 22 539 | 2 442 | 550 610 | 83.56 | 0.37 |  |
| [a_function_value_describes_its_arguments_when_asked](a_function_value_describes_its_arguments_when_asked/) | 94 843 | 1 241 | 1 241 | 832 185 | 76.42 | 0.11 |  |
| [an_allocator_set_after_construction_is_where_the_object_is_made](an_allocator_set_after_construction_is_where_the_object_is_made/) | 155 696 | 78 999 | 2 046 | 479 293 | 76.10 | 0.32 |  |
| [an_argument_its_caller_holds_is_passed_without_counting](an_argument_its_caller_holds_is_passed_without_counting/) | 47 668 | 35 311 | 702 | 1 425 011 | 67.90 | 0.03 |  |
| [removing_many_at_once](removing_many_at_once/) | 1 390 083 | 24 827 | 21 352 | 6 236 188 | 65.10 | 0.22 |  |
| [an_item_written_back_to_its_own_slot_is_not_written](an_item_written_back_to_its_own_slot_is_not_written/) | 211 824 | 43 931 | 3 586 | 2 247 506 | 59.07 | 0.09 |  |
| [a_singletons_attribute_that_never_changes_is_read_in_place](a_singletons_attribute_that_never_changes_is_read_in_place/) | 184 775 | 184 701 | 3 269 | 2 039 770 | 56.52 | 0.09 |  |
| [the_compiler_places_memory](the_compiler_places_memory/) | 469 801 | 32 337 | 8 619 | 2 299 279 | 54.51 | 0.20 |  |
| [a_decimal_literal_beside_a_float_is_a_float](a_decimal_literal_beside_a_float_is_a_float/) | 873 160 | 524 834 | 16 528 | 49 697 773 | 52.83 | 0.02 |  |
| [an_items_storage_is_chosen_while_compiling](an_items_storage_is_chosen_while_compiling/) | 113 092 | 30 034 | 2 313 | 1 688 116 | 48.89 | 0.07 |  |
| [an_item_a_name_holds_from_its_list_is_not_counted](an_item_a_name_holds_from_its_list_is_not_counted/) | 88 931 | 15 185 | 1 822 | 1 359 744 | 48.81 | 0.07 |  |
| [reading_an_address_is_one_machine_operation](reading_an_address_is_one_machine_operation/) | 172 001 | 5 553 | 4 009 | 2 501 066 | 42.90 | 0.07 |  |
| [boxing_only_where_a_value_travels_as_a_shape](boxing_only_where_a_value_travels_as_a_shape/) | 518 268 | 104 469 | 12 418 | 163 880 | 41.74 | 3.16 |  |
| [singletons_a_parallel_reaches_take_a_lock](singletons_a_parallel_reaches_take_a_lock/) | 21 480 | 19 563 | 527 | 257 770 | 40.76 | 0.08 |  |
| [a_lists_templates_read_its_elements_without_counting_them](a_lists_templates_read_its_elements_without_counting_them/) | 88 518 | 29 744 | 2 180 | 1 588 676 | 40.60 | 0.06 |  |
| [short_text_lives_inside_the_string](short_text_lives_inside_the_string/) | 622 840 | 246 372 | 17 134 | 517 877 | 36.35 | 1.20 |  |
| [reflection_on_constants_folds_and_unrolls](reflection_on_constants_folds_and_unrolls/) | 86 342 | 11 786 | 2 581 | 8 214 409 | 33.45 | 0.01 |  |
| [a_list_held_only_by_another_list_lives_in_its_slot](a_list_held_only_by_another_list_lives_in_its_slot/) | 1 129 715 | 262 756 | 36 840 | 5 269 878 | 30.67 | 0.21 |  |
| [a_singletons_reading_functions_do_not_exclude_each_other](a_singletons_reading_functions_do_not_exclude_each_other/) | 144 010 | 114 404 | 4 968 | 612 518 | 28.99 | 0.24 |  |
| [a_number_joined_into_text_is_written_in_place](a_number_joined_into_text_is_written_in_place/) | 473 429 | 338 602 | 16 386 | 432 851 | 28.89 | 1.09 |  |
| [an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted](an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted/) | 58 827 | 16 421 | 2 200 | 2 263 370 | 26.74 | 0.03 |  |
| [atomic_reference_counts_only_with_threads](atomic_reference_counts_only_with_threads/) | 59 663 | 19 771 | 2 249 | 279 572 | 26.53 | 0.21 |  |
| [spreadsheet_recalculation](spreadsheet_recalculation/) | 2 695 262 | 661 137 | 104 117 | 10 713 677 | 25.89 | 0.25 |  |
| [records_sorted_by_one_field](records_sorted_by_one_field/) | 2 354 797 | 691 913 | 92 561 | 4 927 879 | 25.44 | 0.48 |  |
| [while_no_task_runs_a_singletons_lock_is_skipped](while_no_task_runs_a_singletons_lock_is_skipped/) | 41 699 | 51 164 | 2 275 | 2 165 763 | 18.33 | 0.02 |  |
| [smaller_ones](smaller_ones/) | 157 733 | 10 172 | 9 029 | 3 209 656 | 17.47 | 0.05 |  |
| [an_attribute_a_call_cannot_assign_is_passed_without_counting](an_attribute_a_call_cannot_assign_is_passed_without_counting/) | 43 030 | 4 443 | 2 633 | 1 506 438 | 16.34 | 0.03 |  |
| [storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot](storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot/) | 68 982 | 6 741 | 4 347 | 1 228 756 | 15.87 | 0.06 |  |
| [arithmetic_is_checked_in_every_build](arithmetic_is_checked_in_every_build/) | 40 878 | 3 104 | 2 660 | 1 743 189 | 15.37 | 0.02 |  |
| [a_proven_read_tests_only_its_bounds](a_proven_read_tests_only_its_bounds/) | 97 036 | 6 886 | 6 788 | 7 693 254 | 14.30 | 0.01 |  |
| [appending_to_text_in_place](appending_to_text_in_place/) | 2 776 | 62 843 | 196 | 5 806 | 14.16 | 0.48 |  |
| [sorting](sorting/) | 262 839 | 121 619 | 18 969 | 1 076 510 | 13.86 | 0.24 |  |
| [reads_in_a_row_overlap](reads_in_a_row_overlap/) | 70 543 | 6 900 | 5 528 | 8 296 | 12.76 | 8.50 |  |
| [thread_safety_for_singletons_the_rest_of_the_plan](thread_safety_for_singletons_the_rest_of_the_plan/) | 21 368 | 19 951 | 1 988 | 253 123 | 10.75 | 0.08 |  |
| [a_binary_schema_is_a_constant](a_binary_schema_is_a_constant/) | 5 908 | 359 126 | 574 | 11 765 073 | 10.29 | 0.00 |  |
| [tokens_as_columns](tokens_as_columns/) | 712 329 | 136 472 | 74 701 | 2 512 269 | 9.54 | 0.28 |  |
| [a_list_item_read_only_to_test_it_is_not_counted](a_list_item_read_only_to_test_it_is_not_counted/) | 107 547 | 64 487 | 11 593 | 2 728 771 | 9.28 | 0.04 |  |
| [counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts](counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts/) | 49 291 | 10 905 | 5 356 | 496 608 | 9.20 | 0.10 |  |
| [a_test_against_a_value_a_list_never_holds_is_decided_while_compiling](a_test_against_a_value_a_list_never_holds_is_decided_while_compiling/) | 162 251 | 40 058 | 20 654 | 3 561 377 | 7.86 | 0.05 |  |
| [a_table_filled_once_is_read_as_constants](a_table_filled_once_is_read_as_constants/) | 159 116 | 21 710 | 20 349 | 3 531 610 | 7.82 | 0.05 |  |
| [concurrency_machinery_only_where_it_is_used](concurrency_machinery_only_where_it_is_used/) | 11 873 | 11 953 | 1 528 | 14 622 | 7.77 | 0.81 |  |
| [a_singleton_no_other_thread_reaches_takes_no_lock](a_singleton_no_other_thread_reaches_takes_no_lock/) | 25 839 | 5 259 | 3 384 | 1 562 708 | 7.64 | 0.02 |  |
| [a_crashs_report_is_kept_out_of_the_way](a_crashs_report_is_kept_out_of_the_way/) | 59 994 | 13 326 | 9 852 | 2 520 451 | 6.09 | 0.02 |  |
| [a_loop_over_a_list_of_different_classes_runs_them_at_once](a_loop_over_a_list_of_different_classes_runs_them_at_once/) | 553 949 | 282 579 | 96 107 | 7 913 166 | 5.76 | 0.07 |  |
| [plain_reference_counts_where_no_thread_reaches_a_class](plain_reference_counts_where_no_thread_reaches_a_class/) | 62 534 | 28 123 | 10 936 | 1 041 757 | 5.72 | 0.06 |  |
| [calls_in_a_row_run_at_once](calls_in_a_row_run_at_once/) | 102 141 | 43 225 | 23 815 | 4 295 716 | 4.29 | 0.02 |  |
| [deciding_conditions_at_compile_time](deciding_conditions_at_compile_time/) | 30 056 | 8 769 | 7 743 | 2 805 298 | 3.88 | 0.01 |  |
| [objects_made_for_their_owner_are_told_apart](objects_made_for_their_owner_are_told_apart/) | 185 489 | 118 854 | 60 246 | 5 600 591 | 3.08 | 0.03 |  |
| [a_proven_divisor_is_not_checked](a_proven_divisor_is_not_checked/) | 69 013 | 30 243 | 27 213 | 1 210 411 | 2.54 | 0.06 |  |
| [the_thread_pool_only_where_a_parallel_is_made](the_thread_pool_only_where_a_parallel_is_made/) | 11 157 | 7 257 | 7 244 | 697 286 | 1.54 | 0.02 |  |
| [a_wait_in_a_frame_does_not_hold_the_frame](a_wait_in_a_frame_does_not_hold_the_frame/) | 927 798 | 1 174 123 | 918 021 | 314 621 | 1.01 | 2.95 |  |
| [a_dictionary_hashes_a_key_once_cheaply](a_dictionary_hashes_a_key_once_cheaply/) |  | 88 165 | 27 609 | 246 789 |  |  | spite: ran longer than 300 s |
| [a_dictionary_keyed_by_numbers_hashes_the_numbers](a_dictionary_keyed_by_numbers_hashes_the_numbers/) |  | 17 472 | 16 062 | 515 606 |  |  | spite: ran longer than 300 s |
| [a_loop_whose_passes_write_only_their_own_item_runs_in_bands](a_loop_whose_passes_write_only_their_own_item_runs_in_bands/) | 4 630 800 | 823 234 | 55 981 |  | 82.72 |  | python: ran longer than 300 s |
| [allocation_is_the_c_librarys_counted_only_where_read](allocation_is_the_c_librarys_counted_only_where_read/) |  |  |  |  |  |  | build: does not compile: allocation_is_the_c_librarys_counted_only_where_read/allocation_is_the_c_librarys_counted_only_where_read.spite:46: error: this value may be null (it is a Node?), so 'value' cannot be read from it yet... |
| [number_dictionary](number_dictionary/) |  | 19 136 | 11 864 | 366 908 |  |  | spite: ran longer than 300 s |
| [particles](particles/) | 207 338 | 53 849 | 32 717 | 17 575 256 | 6.34 | 0.01 | spite: answers height 1065398 spread 7549745 where naive.c answers height 1065390 spread 7549745 |
| [vector_maths](vector_maths/) | 1 538 102 | 65 329 | 48 266 | 38 949 997 | 31.87 | 0.04 | spite: answers checksum 2389814272 ended at 2218210 where naive.c answers checksum 2414989568 ended at 2302946 |

Last measured 2026-10-22: best of 7 interleaved runs (a form stops repeating once its runs pass 30 s), on AMD Ryzen 9 5950X 16-Core Processor, 32 logical processors; C with clang version 19.1.5 -O2, Python 3.12.10, Spite with `D:\Projects\SpiteCompiler\.spite\spite.exe`.
<!-- /results -->
