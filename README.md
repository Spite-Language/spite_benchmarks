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
| [thread_safety_for_singletons_the_cheapest_safe_form](thread_safety_for_singletons_the_cheapest_safe_form/) | 143 992 | 158 977 | 383 | 1 380 503 | 375.96 | 0.10 |  |
| [a_walked_crash_lines_read_is_the_rows_read](a_walked_crash_lines_read_is_the_rows_read/) | 404 693 | 17 666 | 4 526 | 5 948 053 | 89.42 | 0.07 |  |
| [a_loop_whose_passes_write_only_their_own_item_runs_in_bands](a_loop_whose_passes_write_only_their_own_item_runs_in_bands/) | 2 383 387 | 762 617 | 30 338 | 251 366 972 | 78.56 | 0.01 |  |
| [a_write_back_of_what_the_slot_already_holds_is_not_written](a_write_back_of_what_the_slot_already_holds_is_not_written/) | 40 422 | 4 951 | 531 | 1 940 213 | 76.12 | 0.02 |  |
| [an_argument_its_caller_holds_is_passed_without_counting](an_argument_its_caller_holds_is_passed_without_counting/) | 41 039 | 34 666 | 654 | 1 399 180 | 62.75 | 0.03 |  |
| [a_decimal_literal_beside_a_float_is_a_float](a_decimal_literal_beside_a_float_is_a_float/) | 846 866 | 507 122 | 15 934 | 47 084 404 | 53.15 | 0.02 |  |
| [a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked](a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked/) | 819 187 | 142 875 | 15 873 | 13 311 136 | 51.61 | 0.06 |  |
| [reading_an_address_is_one_machine_operation](reading_an_address_is_one_machine_operation/) | 195 692 | 5 475 | 3 951 | 2 431 852 | 49.53 | 0.08 |  |
| [a_list_of_lists_filled_again_keeps_each_lists_room](a_list_of_lists_filled_again_keeps_each_lists_room/) | 296 478 | 294 512 | 6 339 | 1 133 396 | 46.77 | 0.26 |  |
| [reflection_on_constants_folds_and_unrolls](reflection_on_constants_folds_and_unrolls/) | 110 658 | 11 937 | 2 432 | 7 990 451 | 45.50 | 0.01 |  |
| [a_local_list_of_known_size_lives_in_the_frame](a_local_list_of_known_size_lives_in_the_frame/) | 978 362 | 23 097 | 22 389 | 3 795 090 | 43.70 | 0.26 |  |
| [singletons_a_parallel_reaches_take_a_lock](singletons_a_parallel_reaches_take_a_lock/) | 20 152 | 19 132 | 502 | 253 119 | 40.14 | 0.08 |  |
| [a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one](a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one/) | 39 170 | 72 352 | 996 | 358 367 | 39.33 | 0.11 |  |
| [defaults_the_constructor_replaces_are_never_made](defaults_the_constructor_replaces_are_never_made/) | 12 562 | 41 024 | 328 | 305 433 | 38.30 | 0.04 |  |
| [report_over_records](report_over_records/) | 841 494 | 567 829 | 22 289 | 6 125 845 | 37.75 | 0.14 |  |
| [objects_of_one_class_sit_together](objects_of_one_class_sit_together/) | 87 716 | 22 051 | 2 325 | 530 663 | 37.73 | 0.17 |  |
| [an_items_storage_is_chosen_while_compiling](an_items_storage_is_chosen_while_compiling/) | 74 285 | 29 347 | 1 995 | 1 564 127 | 37.24 | 0.05 |  |
| [maths_on_constants_is_worked_out_while_compiling](maths_on_constants_is_worked_out_while_compiling/) | 93 212 | 13 031 | 2 676 | 26 478 326 | 34.83 | 0.00 |  |
| [a_lists_templates_read_its_elements_without_counting_them](a_lists_templates_read_its_elements_without_counting_them/) | 69 371 | 28 890 | 2 096 | 1 521 409 | 33.10 | 0.05 |  |
| [a_row_of_borrowed_items_lives_in_the_frame](a_row_of_borrowed_items_lives_in_the_frame/) | 90 654 | 6 678 | 2 758 | 4 962 617 | 32.87 | 0.02 |  |
| [an_item_written_back_to_its_own_slot_is_not_written](an_item_written_back_to_its_own_slot_is_not_written/) | 104 409 | 43 351 | 3 573 | 2 149 359 | 29.22 | 0.05 |  |
| [a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame](a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame/) | 99 053 | 3 921 | 3 907 | 431 469 | 25.35 | 0.23 |  |
| [text_building](text_building/) | 232 211 | 82 824 | 9 477 | 592 832 | 24.50 | 0.39 |  |
| [an_item_a_name_holds_from_its_list_is_not_counted](an_item_a_name_holds_from_its_list_is_not_counted/) | 37 626 | 14 825 | 1 636 | 1 298 790 | 23.00 | 0.03 |  |
| [a_singletons_reading_functions_do_not_exclude_each_other](a_singletons_reading_functions_do_not_exclude_each_other/) | 101 605 | 87 925 | 4 426 | 578 245 | 22.96 | 0.18 |  |
| [a_word_inflected_while_compiling](a_word_inflected_while_compiling/) | 73 032 | 265 834 | 3 245 | 881 199 | 22.51 | 0.08 |  |
| [template_chains_run_as_one_loop](template_chains_run_as_one_loop/) | 36 341 | 78 563 | 1 630 | 1 632 850 | 22.30 | 0.02 |  |
| [an_allocator_set_after_construction_is_where_the_object_is_made](an_allocator_set_after_construction_is_where_the_object_is_made/) | 43 274 | 74 806 | 1 980 | 458 419 | 21.86 | 0.09 |  |
| [objects_that_never_leave_their_function_live_in_the_frame](objects_that_never_leave_their_function_live_in_the_frame/) | 293 409 | 1 004 904 | 14 158 | 43 225 809 | 20.72 | 0.01 |  |
| [reading_through_a_type_without_counting](reading_through_a_type_without_counting/) | 103 538 | 9 482 | 5 213 | 5 257 571 | 19.86 | 0.02 |  |
| [a_function_taking_a_type_is_compiled_per_class](a_function_taking_a_type_is_compiled_per_class/) | 1 003 801 | 50 884 | 51 006 | 13 638 219 | 19.68 | 0.07 |  |
| [records_sorted_by_one_field](records_sorted_by_one_field/) | 1 641 944 | 633 474 | 85 165 | 4 584 667 | 19.28 | 0.36 |  |
| [the_compiler_places_memory](the_compiler_places_memory/) | 162 613 | 32 726 | 8 532 | 2 338 023 | 19.06 | 0.07 |  |
| [a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once](a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once/) | 56 524 | 300 360 | 2 984 | 4 627 269 | 18.94 | 0.01 |  |
| [game_maths](game_maths/) | 30 262 | 2 180 | 1 673 | 6 767 272 | 18.09 | 0.00 |  |
| [a_numbers_bits_are_read_in_place](a_numbers_bits_are_read_in_place/) | 383 415 | 87 665 | 22 611 | 27 824 863 | 16.96 | 0.01 |  |
| [a_function_value_describes_its_arguments_when_asked](a_function_value_describes_its_arguments_when_asked/) | 19 849 | 1 213 | 1 202 | 821 986 | 16.51 | 0.02 |  |
| [a_singletons_attribute_that_never_changes_is_read_in_place](a_singletons_attribute_that_never_changes_is_read_in_place/) | 51 096 | 124 755 | 3 181 | 1 923 221 | 16.06 | 0.03 |  |
| [particles](particles/) | 160 089 | 27 833 | 10 397 | 25 220 258 | 15.40 | 0.01 |  |
| [while_no_task_runs_a_singletons_lock_is_skipped](while_no_task_runs_a_singletons_lock_is_skipped/) | 32 933 | 50 501 | 2 239 | 2 128 893 | 14.71 | 0.02 |  |
| [a_proven_read_tests_only_its_bounds](a_proven_read_tests_only_its_bounds/) | 92 522 | 6 617 | 6 456 | 7 243 121 | 14.33 | 0.01 |  |
| [arithmetic_is_checked_in_every_build](arithmetic_is_checked_in_every_build/) | 36 219 | 2 946 | 2 595 | 1 691 962 | 13.96 | 0.02 |  |
| [removing_many_at_once](removing_many_at_once/) | 280 513 | 23 812 | 20 410 | 5 407 463 | 13.74 | 0.05 |  |
| [a_list_held_only_by_another_list_lives_in_its_slot](a_list_held_only_by_another_list_lives_in_its_slot/) | 479 358 | 230 876 | 34 960 | 6 149 966 | 13.71 | 0.08 |  |
| [sorting](sorting/) | 240 532 | 118 764 | 17 789 | 1 053 477 | 13.52 | 0.23 |  |
| [an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted](an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted/) | 28 542 | 15 599 | 2 118 | 2 151 185 | 13.48 | 0.01 |  |
| [atomic_reference_counts_only_with_threads](atomic_reference_counts_only_with_threads/) | 28 189 | 18 083 | 2 139 | 261 486 | 13.18 | 0.11 |  |
| [image_filter_over_planes](image_filter_over_planes/) | 283 440 | 234 055 | 21 791 | 7 459 920 | 13.01 | 0.04 |  |
| [text_joined_in_one_piece](text_joined_in_one_piece/) | 42 687 | 94 245 | 3 307 | 134 646 | 12.91 | 0.32 |  |
| [smaller_ones](smaller_ones/) | 104 986 | 9 861 | 8 635 | 3 129 900 | 12.16 | 0.03 |  |
| [thread_safety_for_singletons_the_rest_of_the_plan](thread_safety_for_singletons_the_rest_of_the_plan/) | 19 690 | 19 042 | 1 853 | 248 378 | 10.63 | 0.08 |  |
| [a_number_read_from_bytes_is_one_load](a_number_read_from_bytes_is_one_load/) | 329 195 | 52 055 | 31 160 | 25 951 305 | 10.56 | 0.01 |  |
| [a_singleton_no_other_thread_reaches_takes_no_lock](a_singleton_no_other_thread_reaches_takes_no_lock/) | 32 698 | 4 736 | 3 143 | 1 402 726 | 10.40 | 0.02 |  |
| [a_binary_schema_is_a_constant](a_binary_schema_is_a_constant/) | 5 981 | 346 793 | 588 | 10 207 178 | 10.17 | 0.00 |  |
| [spreadsheet_recalculation](spreadsheet_recalculation/) | 987 038 | 600 869 | 102 243 | 11 158 798 | 9.65 | 0.09 |  |
| [storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot](storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot/) | 39 981 | 6 457 | 4 286 | 1 197 088 | 9.33 | 0.03 |  |
| [an_attribute_a_call_cannot_assign_is_passed_without_counting](an_attribute_a_call_cannot_assign_is_passed_without_counting/) | 21 103 | 4 257 | 2 544 | 1 448 090 | 8.30 | 0.01 |  |
| [a_table_filled_once_is_read_as_constants](a_table_filled_once_is_read_as_constants/) | 149 334 | 20 427 | 19 677 | 3 363 029 | 7.59 | 0.04 |  |
| [a_test_against_a_value_a_list_never_holds_is_decided_while_compiling](a_test_against_a_value_a_list_never_holds_is_decided_while_compiling/) | 147 929 | 38 028 | 19 545 | 3 368 167 | 7.57 | 0.04 |  |
| [concurrency_machinery_only_where_it_is_used](concurrency_machinery_only_where_it_is_used/) | 10 783 | 10 711 | 1 462 | 13 040 | 7.38 | 0.83 |  |
| [number_dictionary](number_dictionary/) | 80 946 | 17 888 | 11 246 | 340 869 | 7.20 | 0.24 |  |
| [allocation_is_the_c_librarys_counted_only_where_read](allocation_is_the_c_librarys_counted_only_where_read/) | 19 102 | 59 690 | 2 748 | 377 749 | 6.95 | 0.05 |  |
| [deciding_conditions_at_compile_time](deciding_conditions_at_compile_time/) | 46 020 | 8 422 | 7 493 | 2 721 746 | 6.14 | 0.02 |  |
| [boxing_only_where_a_value_travels_as_a_shape](boxing_only_where_a_value_travels_as_a_shape/) | 71 791 | 83 020 | 12 162 | 157 265 | 5.90 | 0.46 |  |
| [counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts](counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts/) | 30 594 | 10 666 | 5 209 | 479 770 | 5.87 | 0.06 |  |
| [vector_maths](vector_maths/) | 275 986 | 60 948 | 46 991 | 27 605 985 | 5.87 | 0.01 |  |
| [short_text_lives_inside_the_string](short_text_lives_inside_the_string/) | 97 211 | 246 092 | 16 850 | 511 747 | 5.77 | 0.19 |  |
| [a_number_joined_into_text_is_written_in_place](a_number_joined_into_text_is_written_in_place/) | 85 610 | 319 207 | 15 207 | 396 299 | 5.63 | 0.22 |  |
| [a_dictionary_written_out_and_only_read_by_literal_keys_is_folded](a_dictionary_written_out_and_only_read_by_literal_keys_is_folded/) | 29 459 | 345 335 | 5 606 | 1 362 028 | 5.25 | 0.02 |  |
| [a_list_item_read_only_to_test_it_is_not_counted](a_list_item_read_only_to_test_it_is_not_counted/) | 57 376 | 62 177 | 11 229 | 2 661 220 | 5.11 | 0.02 |  |
| [appending_to_text_in_place](appending_to_text_in_place/) | 922 | 59 636 | 184 | 5 578 | 5.01 | 0.17 |  |
| [calls_in_a_row_run_at_once](calls_in_a_row_run_at_once/) | 97 317 | 41 889 | 22 770 | 4 234 866 | 4.27 | 0.02 |  |
| [a_loop_over_a_list_of_different_classes_runs_them_at_once](a_loop_over_a_list_of_different_classes_runs_them_at_once/) | 387 324 | 266 957 | 91 912 | 7 576 505 | 4.21 | 0.05 |  |
| [a_crashs_report_is_kept_out_of_the_way](a_crashs_report_is_kept_out_of_the_way/) | 40 445 | 13 107 | 9 789 | 2 522 471 | 4.13 | 0.02 |  |
| [copies_that_cost_nothing](copies_that_cost_nothing/) | 64 934 | 22 263 | 16 033 | 6 022 464 | 4.05 | 0.01 |  |
| [plain_reference_counts_where_no_thread_reaches_a_class](plain_reference_counts_where_no_thread_reaches_a_class/) | 42 276 | 25 065 | 10 779 | 998 484 | 3.92 | 0.04 |  |
| [a_dictionary_hashes_a_key_once_cheaply](a_dictionary_hashes_a_key_once_cheaply/) | 84 625 | 82 121 | 25 375 | 243 828 | 3.33 | 0.35 |  |
| [a_dictionary_keyed_by_numbers_hashes_the_numbers](a_dictionary_keyed_by_numbers_hashes_the_numbers/) | 39 404 | 14 728 | 12 636 | 473 024 | 3.12 | 0.08 |  |
| [objects_made_for_their_owner_are_told_apart](objects_made_for_their_owner_are_told_apart/) | 177 421 | 113 985 | 57 828 | 5 388 051 | 3.07 | 0.03 |  |
| [tokens_as_columns](tokens_as_columns/) | 216 942 | 128 538 | 72 084 | 2 417 733 | 3.01 | 0.09 |  |
| [singletons_made_on_first_use_never_counted](singletons_made_on_first_use_never_counted/) | 15 518 | 210 042 | 5 577 | 6 816 545 | 2.78 | 0.00 |  |
| [a_proven_divisor_is_not_checked](a_proven_divisor_is_not_checked/) | 56 613 | 28 848 | 26 022 | 1 135 574 | 2.18 | 0.05 |  |
| [reads_in_a_row_overlap](reads_in_a_row_overlap/) | 6 551 | 6 207 | 4 826 | 7 699 | 1.36 | 0.85 |  |
| [the_thread_pool_only_where_a_parallel_is_made](the_thread_pool_only_where_a_parallel_is_made/) | 8 627 | 7 215 | 7 174 | 689 111 | 1.20 | 0.01 |  |
| [a_wait_in_a_frame_does_not_hold_the_frame](a_wait_in_a_frame_does_not_hold_the_frame/) | 89 781 | 1 185 394 | 922 617 | 316 128 | 0.10 | 0.28 |  |

Last measured 2026-10-23: best of 5 interleaved runs (a form stops repeating once its runs pass 30 s), on AMD Ryzen 9 5950X 16-Core Processor, 32 logical processors; C with clang version 19.1.5 -O2, Python 3.12.10, Spite with `D:\Projects\SpiteCompiler\.spite\spite.exe`.
<!-- /results -->
