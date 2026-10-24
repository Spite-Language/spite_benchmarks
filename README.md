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
| [a_write_back_of_what_the_slot_already_holds_is_not_written](a_write_back_of_what_the_slot_already_holds_is_not_written/) | 35 498 | 4 945 | 534 | 1 912 617 | 66.48 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_walked_crash_lines_read_is_the_rows_read](a_walked_crash_lines_read_is_the_rows_read/) | 143 303 | 17 593 | 4 499 | 5 833 554 | 31.85 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_list_of_lists_filled_again_keeps_each_lists_room](a_list_of_lists_filled_again_keeps_each_lists_room/) | 179 935 | 282 941 | 6 360 | 1 065 372 | 28.29 | 0.17 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [text_building](text_building/) | 213 372 | 81 891 | 9 479 | 587 119 | 22.51 | 0.36 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_word_inflected_while_compiling](a_word_inflected_while_compiling/) | 64 999 | 266 363 | 3 223 | 877 769 | 20.17 | 0.07 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [defaults_the_constructor_replaces_are_never_made](defaults_the_constructor_replaces_are_never_made/) | 6 469 | 40 401 | 322 | 296 462 | 20.09 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [report_over_records](report_over_records/) | 377 132 | 561 080 | 22 029 | 6 050 473 | 17.12 | 0.06 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [an_items_storage_is_chosen_while_compiling](an_items_storage_is_chosen_while_compiling/) | 32 904 | 29 351 | 2 071 | 1 549 888 | 15.89 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_row_of_borrowed_items_lives_in_the_frame](a_row_of_borrowed_items_lives_in_the_frame/) | 45 727 | 6 707 | 2 958 | 4 843 574 | 15.46 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one](a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one/) | 15 312 | 72 328 | 993 | 344 697 | 15.42 | 0.04 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_singletons_attribute_that_never_changes_is_read_in_place](a_singletons_attribute_that_never_changes_is_read_in_place/) | 44 631 | 116 115 | 3 029 | 1 877 708 | 14.73 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [objects_of_one_class_sit_together](objects_of_one_class_sit_together/) | 33 941 | 21 920 | 2 377 | 525 019 | 14.28 | 0.06 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [arithmetic_is_checked_in_every_build](arithmetic_is_checked_in_every_build/) | 34 348 | 2 958 | 2 553 | 1 678 944 | 13.45 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_numbers_bits_are_read_in_place](a_numbers_bits_are_read_in_place/) | 297 791 | 86 762 | 22 557 | 27 387 130 | 13.20 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [the_compiler_places_memory](the_compiler_places_memory/) | 111 491 | 32 157 | 8 474 | 2 285 037 | 13.16 | 0.05 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_function_value_describes_its_arguments_when_asked](a_function_value_describes_its_arguments_when_asked/) | 15 539 | 1 211 | 1 202 | 809 459 | 12.93 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [sorting](sorting/) | 222 985 | 118 103 | 17 436 | 1 024 033 | 12.79 | 0.22 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [game_maths](game_maths/) | 21 161 | 2 160 | 1 669 | 6 669 852 | 12.68 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_lists_templates_read_its_elements_without_counting_them](a_lists_templates_read_its_elements_without_counting_them/) | 25 652 | 28 442 | 2 034 | 1 523 646 | 12.61 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [while_no_task_runs_a_singletons_lock_is_skipped](while_no_task_runs_a_singletons_lock_is_skipped/) | 28 139 | 50 067 | 2 241 | 2 070 191 | 12.56 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [text_joined_in_one_piece](text_joined_in_one_piece/) | 41 881 | 93 109 | 3 386 | 131 826 | 12.37 | 0.32 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [template_chains_run_as_one_loop](template_chains_run_as_one_loop/) | 17 592 | 78 267 | 1 440 | 1 597 124 | 12.22 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted](an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted/) | 25 518 | 15 790 | 2 109 | 2 116 133 | 12.10 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [particles](particles/) | 118 664 | 27 858 | 9 825 | 24 705 797 | 12.08 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [an_argument_its_caller_holds_is_passed_without_counting](an_argument_its_caller_holds_is_passed_without_counting/) | 7 820 | 33 711 | 652 | 1 371 187 | 11.99 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [records_sorted_by_one_field](records_sorted_by_one_field/) | 976 653 | 610 700 | 84 502 | 4 495 834 | 11.56 | 0.22 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [reading_through_a_type_without_counting](reading_through_a_type_without_counting/) | 56 458 | 9 408 | 5 389 | 5 223 725 | 10.48 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_proven_read_tests_only_its_bounds](a_proven_read_tests_only_its_bounds/) | 64 621 | 6 519 | 6 379 | 6 998 019 | 10.13 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [singletons_a_parallel_reaches_take_a_lock](singletons_a_parallel_reaches_take_a_lock/) | 4 758 | 18 903 | 471 | 250 925 | 10.10 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [atomic_reference_counts_only_with_threads](atomic_reference_counts_only_with_threads/) | 21 166 | 17 704 | 2 101 | 259 061 | 10.07 | 0.08 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [image_filter_over_planes](image_filter_over_planes/) | 216 552 | 231 680 | 21 771 | 7 316 668 | 9.95 | 0.03 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [reading_an_address_is_one_machine_operation](reading_an_address_is_one_machine_operation/) | 38 220 | 5 477 | 3 937 | 2 341 259 | 9.71 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_list_held_only_by_another_list_lives_in_its_slot](a_list_held_only_by_another_list_lives_in_its_slot/) | 334 579 | 224 991 | 34 784 | 5 322 372 | 9.62 | 0.06 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [an_item_a_name_holds_from_its_list_is_not_counted](an_item_a_name_holds_from_its_list_is_not_counted/) | 15 304 | 14 568 | 1 604 | 1 273 546 | 9.54 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame](a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame/) | 36 661 | 3 824 | 3 916 | 423 294 | 9.36 | 0.09 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot](storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot/) | 37 649 | 6 405 | 4 251 | 1 157 191 | 8.86 | 0.03 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once](a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once/) | 26 120 | 298 546 | 3 055 | 4 556 831 | 8.55 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [spreadsheet_recalculation](spreadsheet_recalculation/) | 802 355 | 612 329 | 101 440 | 10 448 516 | 7.91 | 0.08 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [removing_many_at_once](removing_many_at_once/) | 156 243 | 24 140 | 20 357 | 5 346 476 | 7.68 | 0.03 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [an_item_written_back_to_its_own_slot_is_not_written](an_item_written_back_to_its_own_slot_is_not_written/) | 27 460 | 42 804 | 3 599 | 2 110 481 | 7.63 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [concurrency_machinery_only_where_it_is_used](concurrency_machinery_only_where_it_is_used/) | 10 655 | 10 440 | 1 439 | 13 477 | 7.40 | 0.79 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [maths_on_constants_is_worked_out_while_compiling](maths_on_constants_is_worked_out_while_compiling/) | 19 799 | 13 007 | 2 748 | 26 246 713 | 7.20 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [reflection_on_constants_folds_and_unrolls](reflection_on_constants_folds_and_unrolls/) | 17 735 | 11 516 | 2 477 | 7 796 569 | 7.16 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_singleton_no_other_thread_reaches_takes_no_lock](a_singleton_no_other_thread_reaches_takes_no_lock/) | 20 758 | 4 654 | 3 099 | 1 385 091 | 6.70 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_number_joined_into_text_is_written_in_place](a_number_joined_into_text_is_written_in_place/) | 93 016 | 305 417 | 15 239 | 385 450 | 6.10 | 0.24 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_number_read_from_bytes_is_one_load](a_number_read_from_bytes_is_one_load/) | 176 246 | 51 905 | 30 999 | 25 673 804 | 5.69 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [short_text_lives_inside_the_string](short_text_lives_inside_the_string/) | 94 942 | 235 015 | 16 896 | 505 803 | 5.62 | 0.19 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [objects_that_never_leave_their_function_live_in_the_frame](objects_that_never_leave_their_function_live_in_the_frame/) | 78 340 | 980 947 | 14 160 | 42 784 863 | 5.53 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_function_taking_a_type_is_compiled_per_class](a_function_taking_a_type_is_compiled_per_class/) | 277 128 | 50 784 | 50 720 | 13 386 403 | 5.46 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [appending_to_text_in_place](appending_to_text_in_place/) | 925 | 57 812 | 178 | 5 519 | 5.20 | 0.17 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [allocation_is_the_c_librarys_counted_only_where_read](allocation_is_the_c_librarys_counted_only_where_read/) | 14 116 | 59 074 | 2 736 | 365 697 | 5.16 | 0.04 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [smaller_ones](smaller_ones/) | 43 664 | 9 795 | 9 080 | 3 076 502 | 4.81 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_list_item_read_only_to_test_it_is_not_counted](a_list_item_read_only_to_test_it_is_not_counted/) | 53 094 | 62 410 | 11 212 | 2 525 701 | 4.74 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [boxing_only_where_a_value_travels_as_a_shape](boxing_only_where_a_value_travels_as_a_shape/) | 54 636 | 81 503 | 11 694 | 154 705 | 4.67 | 0.35 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts](counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts/) | 23 708 | 10 585 | 5 163 | 474 812 | 4.59 | 0.05 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [thread_safety_for_singletons_the_cheapest_safe_form](thread_safety_for_singletons_the_cheapest_safe_form/) | 1 822 | 157 937 | 423 | 1 358 200 | 4.31 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [an_attribute_a_call_cannot_assign_is_passed_without_counting](an_attribute_a_call_cannot_assign_is_passed_without_counting/) | 10 607 | 4 294 | 2 539 | 1 417 252 | 4.18 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_dictionary_written_out_and_only_read_by_literal_keys_is_folded](a_dictionary_written_out_and_only_read_by_literal_keys_is_folded/) | 21 866 | 333 424 | 5 604 | 1 320 555 | 3.90 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_loop_over_a_list_of_different_classes_runs_them_at_once](a_loop_over_a_list_of_different_classes_runs_them_at_once/) | 324 492 | 264 393 | 91 290 | 7 331 282 | 3.55 | 0.04 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [plain_reference_counts_where_no_thread_reaches_a_class](plain_reference_counts_where_no_thread_reaches_a_class/) | 36 987 | 24 855 | 10 522 | 975 202 | 3.52 | 0.04 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_binary_schema_is_a_constant](a_binary_schema_is_a_constant/) | 1 919 | 344 560 | 556 | 9 875 480 | 3.45 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [objects_made_for_their_owner_are_told_apart](objects_made_for_their_owner_are_told_apart/) | 198 815 | 113 171 | 57 671 | 5 338 522 | 3.45 | 0.04 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [number_dictionary](number_dictionary/) | 37 218 | 17 488 | 11 262 | 322 234 | 3.30 | 0.12 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [calls_in_a_row_run_at_once](calls_in_a_row_run_at_once/) | 76 224 | 41 751 | 23 142 | 4 046 670 | 3.29 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [copies_that_cost_nothing](copies_that_cost_nothing/) | 50 953 | 22 104 | 15 953 | 5 935 210 | 3.19 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_local_list_of_known_size_lives_in_the_frame](a_local_list_of_known_size_lives_in_the_frame/) | 68 584 | 23 026 | 22 408 | 3 714 138 | 3.06 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_dictionary_hashes_a_key_once_cheaply](a_dictionary_hashes_a_key_once_cheaply/) | 75 462 | 80 497 | 25 422 | 243 111 | 2.97 | 0.31 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_crashs_report_is_kept_out_of_the_way](a_crashs_report_is_kept_out_of_the_way/) | 26 303 | 13 070 | 9 747 | 2 525 662 | 2.70 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_dictionary_keyed_by_numbers_hashes_the_numbers](a_dictionary_keyed_by_numbers_hashes_the_numbers/) | 33 733 | 14 803 | 12 750 | 458 302 | 2.65 | 0.07 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [thread_safety_for_singletons_the_rest_of_the_plan](thread_safety_for_singletons_the_rest_of_the_plan/) | 4 522 | 18 820 | 1 901 | 245 809 | 2.38 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [an_allocator_set_after_construction_is_where_the_object_is_made](an_allocator_set_after_construction_is_where_the_object_is_made/) | 4 652 | 73 157 | 1 990 | 447 861 | 2.34 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_proven_divisor_is_not_checked](a_proven_divisor_is_not_checked/) | 53 665 | 28 852 | 25 747 | 1 138 131 | 2.08 | 0.05 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [vector_maths](vector_maths/) | 96 643 | 60 546 | 46 578 | 26 634 373 | 2.07 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [singletons_made_on_first_use_never_counted](singletons_made_on_first_use_never_counted/) | 11 499 | 206 153 | 5 628 | 6 744 732 | 2.04 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [tokens_as_columns](tokens_as_columns/) | 131 791 | 125 745 | 71 947 | 2 362 470 | 1.83 | 0.06 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [deciding_conditions_at_compile_time](deciding_conditions_at_compile_time/) | 12 635 | 8 389 | 7 372 | 2 670 189 | 1.71 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [the_thread_pool_only_where_a_parallel_is_made](the_thread_pool_only_where_a_parallel_is_made/) | 10 828 | 7 111 | 7 199 | 681 986 | 1.50 | 0.02 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_test_against_a_value_a_list_never_holds_is_decided_while_compiling](a_test_against_a_value_a_list_never_holds_is_decided_while_compiling/) | 26 770 | 37 915 | 19 408 | 3 263 526 | 1.38 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_table_filled_once_is_read_as_constants](a_table_filled_once_is_read_as_constants/) | 26 572 | 20 447 | 19 453 | 3 230 623 | 1.37 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [reads_in_a_row_overlap](reads_in_a_row_overlap/) | 6 280 | 6 213 | 4 854 | 7 688 | 1.29 | 0.82 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked](a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked/) | 19 944 | 140 797 | 15 820 | 13 149 709 | 1.26 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_singletons_reading_functions_do_not_exclude_each_other](a_singletons_reading_functions_do_not_exclude_each_other/) | 5 593 | 86 271 | 4 626 | 575 242 | 1.21 | 0.01 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_loop_whose_passes_write_only_their_own_item_runs_in_bands](a_loop_whose_passes_write_only_their_own_item_runs_in_bands/) | 33 124 | 756 423 | 31 070 | 247 495 528 | 1.07 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_decimal_literal_beside_a_float_is_a_float](a_decimal_literal_beside_a_float_is_a_float/) | 16 109 | 502 045 | 15 887 | 44 567 415 | 1.01 | 0.00 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |
| [a_wait_in_a_frame_does_not_hold_the_frame](a_wait_in_a_frame_does_not_hold_the_frame/) | 91 145 | 1 178 105 | 926 060 | 312 769 | 0.10 | 0.29 | timed with D:\Projects\SpiteCompiler\.spite\spite_all2.exe |

Last measured 2026-10-24: best of 5 interleaved runs (a form stops repeating once its runs pass 30 s), on AMD Ryzen 9 5950X 16-Core Processor, 32 logical processors; C with clang version 19.1.5 -O2, Python 3.12.10, Spite with `D:\Projects\SpiteCompiler\.spite\spite_all2.exe`.
<!-- /results -->
