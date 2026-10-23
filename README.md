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
| [a_word_inflected_while_compiling](a_word_inflected_while_compiling/) | 5 096 692 | 277 539 | 3 416 | 917 200 | 1492.01 | 5.56 |  |
| [template_chains_run_as_one_loop](template_chains_run_as_one_loop/) | 451 278 | 92 920 | 1 882 | 2 003 781 | 239.79 | 0.23 |  |
| [a_row_of_borrowed_items_lives_in_the_frame](a_row_of_borrowed_items_lives_in_the_frame/) | 657 039 | 7 349 | 3 285 | 6 633 088 | 200.01 | 0.10 |  |
| [thread_safety_for_singletons_the_cheapest_safe_form](thread_safety_for_singletons_the_cheapest_safe_form/) | 77 398 | 462 522 | 495 | 1 544 275 | 156.36 | 0.05 |  |
| [a_write_back_of_what_the_slot_already_holds_is_not_written](a_write_back_of_what_the_slot_already_holds_is_not_written/) | 82 573 | 5 370 | 602 | 2 011 343 | 137.16 | 0.04 |  |
| [a_walked_crash_lines_read_is_the_rows_read](a_walked_crash_lines_read_is_the_rows_read/) | 526 034 | 18 349 | 4 709 | 8 318 833 | 111.71 | 0.06 |  |
| [reading_through_a_type_without_counting](reading_through_a_type_without_counting/) | 551 854 | 9 764 | 5 344 | 5 565 374 | 103.27 | 0.10 |  |
| [a_list_of_lists_filled_again_keeps_each_lists_room](a_list_of_lists_filled_again_keeps_each_lists_room/) | 617 983 | 355 465 | 6 462 | 1 465 493 | 95.63 | 0.42 |  |
| [singletons_made_on_first_use_never_counted](singletons_made_on_first_use_never_counted/) | 543 250 | 218 443 | 5 694 | 7 060 024 | 95.41 | 0.08 |  |
| [an_argument_its_caller_holds_is_passed_without_counting](an_argument_its_caller_holds_is_passed_without_counting/) | 58 463 | 35 082 | 693 | 1 452 985 | 84.36 | 0.04 |  |
| [a_loop_whose_passes_write_only_their_own_item_runs_in_bands](a_loop_whose_passes_write_only_their_own_item_runs_in_bands/) | 2 469 039 | 793 610 | 41 576 | 273 098 390 | 59.39 | 0.01 |  |
| [defaults_the_constructor_replaces_are_never_made](defaults_the_constructor_replaces_are_never_made/) | 18 924 | 44 101 | 341 | 323 036 | 55.50 | 0.06 |  |
| [a_local_list_of_known_size_lives_in_the_frame](a_local_list_of_known_size_lives_in_the_frame/) | 1 247 281 | 23 768 | 23 011 | 3 864 133 | 54.20 | 0.32 |  |
| [objects_of_one_class_sit_together](objects_of_one_class_sit_together/) | 129 852 | 24 154 | 2 421 | 560 385 | 53.64 | 0.23 |  |
| [a_decimal_literal_beside_a_float_is_a_float](a_decimal_literal_beside_a_float_is_a_float/) | 878 222 | 526 267 | 16 484 | 49 841 481 | 53.28 | 0.02 |  |
| [a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked](a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked/) | 844 811 | 148 299 | 16 275 | 13 699 686 | 51.91 | 0.06 |  |
| [reading_an_address_is_one_machine_operation](reading_an_address_is_one_machine_operation/) | 206 769 | 5 605 | 4 065 | 2 468 143 | 50.87 | 0.08 |  |
| [an_item_written_back_to_its_own_slot_is_not_written](an_item_written_back_to_its_own_slot_is_not_written/) | 188 919 | 46 238 | 3 971 | 2 369 588 | 47.57 | 0.08 |  |
| [a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one](a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one/) | 48 118 | 82 228 | 1 051 | 399 543 | 45.78 | 0.12 |  |
| [report_over_records](report_over_records/) | 1 027 415 | 651 527 | 23 063 | 6 505 349 | 44.55 | 0.16 |  |
| [singletons_a_parallel_reaches_take_a_lock](singletons_a_parallel_reaches_take_a_lock/) | 22 245 | 20 020 | 518 | 252 020 | 42.94 | 0.09 |  |
| [an_items_storage_is_chosen_while_compiling](an_items_storage_is_chosen_while_compiling/) | 99 600 | 32 070 | 2 332 | 1 733 465 | 42.71 | 0.06 |  |
| [an_item_a_name_holds_from_its_list_is_not_counted](an_item_a_name_holds_from_its_list_is_not_counted/) | 68 881 | 15 566 | 1 961 | 1 359 617 | 35.13 | 0.05 |  |
| [a_lists_templates_read_its_elements_without_counting_them](a_lists_templates_read_its_elements_without_counting_them/) | 80 543 | 30 462 | 2 352 | 1 629 947 | 34.24 | 0.05 |  |
| [maths_on_constants_is_worked_out_while_compiling](maths_on_constants_is_worked_out_while_compiling/) | 91 190 | 13 221 | 2 891 | 27 922 943 | 31.54 | 0.00 |  |
| [a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame](a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame/) | 129 587 | 4 181 | 4 200 | 447 308 | 30.85 | 0.29 |  |
| [reflection_on_constants_folds_and_unrolls](reflection_on_constants_folds_and_unrolls/) | 72 305 | 12 916 | 2 617 | 8 437 728 | 27.63 | 0.01 |  |
| [an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted](an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted/) | 57 491 | 16 660 | 2 203 | 2 242 327 | 26.10 | 0.03 |  |
| [text_building](text_building/) | 258 495 | 91 669 | 10 153 | 653 353 | 25.46 | 0.40 |  |
| [a_list_held_only_by_another_list_lives_in_its_slot](a_list_held_only_by_another_list_lives_in_its_slot/) | 844 443 | 328 130 | 37 689 | 9 608 239 | 22.41 | 0.09 |  |
| [a_singletons_attribute_that_never_changes_is_read_in_place](a_singletons_attribute_that_never_changes_is_read_in_place/) | 71 801 | 183 594 | 3 354 | 2 107 292 | 21.41 | 0.03 |  |
| [objects_that_never_leave_their_function_live_in_the_frame](objects_that_never_leave_their_function_live_in_the_frame/) | 301 731 | 1 021 568 | 14 623 | 45 860 880 | 20.63 | 0.01 |  |
| [a_singletons_reading_functions_do_not_exclude_each_other](a_singletons_reading_functions_do_not_exclude_each_other/) | 107 806 | 117 751 | 5 289 | 608 013 | 20.38 | 0.18 |  |
| [records_sorted_by_one_field](records_sorted_by_one_field/) | 1 924 198 | 721 097 | 95 151 | 5 064 617 | 20.22 | 0.38 |  |
| [the_compiler_places_memory](the_compiler_places_memory/) | 185 289 | 34 741 | 9 331 | 2 542 750 | 19.86 | 0.07 |  |
| [a_function_taking_a_type_is_compiled_per_class](a_function_taking_a_type_is_compiled_per_class/) | 1 043 744 | 52 727 | 52 772 | 14 314 030 | 19.78 | 0.07 |  |
| [an_allocator_set_after_construction_is_where_the_object_is_made](an_allocator_set_after_construction_is_where_the_object_is_made/) | 40 159 | 77 464 | 2 059 | 476 698 | 19.50 | 0.08 |  |
| [game_maths](game_maths/) | 31 410 | 2 234 | 1 733 | 7 047 091 | 18.12 | 0.00 |  |
| [a_function_value_describes_its_arguments_when_asked](a_function_value_describes_its_arguments_when_asked/) | 21 664 | 1 238 | 1 246 | 861 162 | 17.39 | 0.03 |  |
| [atomic_reference_counts_only_with_threads](atomic_reference_counts_only_with_threads/) | 37 419 | 19 957 | 2 219 | 275 202 | 16.86 | 0.14 |  |
| [spreadsheet_recalculation](spreadsheet_recalculation/) | 1 916 696 | 732 194 | 116 660 | 14 223 400 | 16.43 | 0.13 |  |
| [a_numbers_bits_are_read_in_place](a_numbers_bits_are_read_in_place/) | 397 878 | 93 291 | 24 393 | 40 692 880 | 16.31 | 0.01 |  |
| [particles](particles/) | 168 816 | 28 652 | 10 525 | 26 631 544 | 16.04 | 0.01 |  |
| [image_filter_over_planes](image_filter_over_planes/) | 343 059 | 251 465 | 22 691 | 9 364 459 | 15.12 | 0.04 |  |
| [while_no_task_runs_a_singletons_lock_is_skipped](while_no_task_runs_a_singletons_lock_is_skipped/) | 34 654 | 53 137 | 2 373 | 2 232 710 | 14.60 | 0.02 |  |
| [removing_many_at_once](removing_many_at_once/) | 309 961 | 24 894 | 21 277 | 5 872 768 | 14.57 | 0.05 |  |
| [a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once](a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once/) | 43 789 | 401 319 | 3 057 | 4 889 187 | 14.32 | 0.01 |  |
| [a_proven_read_tests_only_its_bounds](a_proven_read_tests_only_its_bounds/) | 99 379 | 7 263 | 7 018 | 9 628 598 | 14.16 | 0.01 |  |
| [arithmetic_is_checked_in_every_build](arithmetic_is_checked_in_every_build/) | 36 745 | 3 026 | 2 664 | 1 758 313 | 13.79 | 0.02 |  |
| [storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot](storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot/) | 63 676 | 7 111 | 4 747 | 1 310 600 | 13.41 | 0.05 |  |
| [text_joined_in_one_piece](text_joined_in_one_piece/) | 47 455 | 102 920 | 3 576 | 147 638 | 13.27 | 0.32 |  |
| [sorting](sorting/) | 251 480 | 123 977 | 20 772 | 1 148 388 | 12.11 | 0.22 |  |
| [smaller_ones](smaller_ones/) | 108 470 | 10 235 | 9 082 | 3 421 632 | 11.94 | 0.03 |  |
| [an_attribute_a_call_cannot_assign_is_passed_without_counting](an_attribute_a_call_cannot_assign_is_passed_without_counting/) | 31 613 | 4 418 | 2 647 | 1 517 508 | 11.94 | 0.02 |  |
| [a_number_read_from_bytes_is_one_load](a_number_read_from_bytes_is_one_load/) | 384 439 | 53 830 | 33 225 | 28 817 853 | 11.57 | 0.01 |  |
| [thread_safety_for_singletons_the_rest_of_the_plan](thread_safety_for_singletons_the_rest_of_the_plan/) | 24 354 | 34 315 | 2 283 | 274 130 | 10.67 | 0.09 |  |
| [number_dictionary](number_dictionary/) | 121 494 | 22 213 | 11 946 | 418 174 | 10.17 | 0.29 |  |
| [a_test_against_a_value_a_list_never_holds_is_decided_while_compiling](a_test_against_a_value_a_list_never_holds_is_decided_while_compiling/) | 178 019 | 39 583 | 20 535 | 3 850 344 | 8.67 | 0.05 |  |
| [a_table_filled_once_is_read_as_constants](a_table_filled_once_is_read_as_constants/) | 177 211 | 21 374 | 20 600 | 3 861 402 | 8.60 | 0.05 |  |
| [a_list_item_read_only_to_test_it_is_not_counted](a_list_item_read_only_to_test_it_is_not_counted/) | 92 475 | 64 416 | 11 561 | 3 151 371 | 8.00 | 0.03 |  |
| [concurrency_machinery_only_where_it_is_used](concurrency_machinery_only_where_it_is_used/) | 11 872 | 11 903 | 1 504 | 15 018 | 7.89 | 0.79 |  |
| [a_singleton_no_other_thread_reaches_takes_no_lock](a_singleton_no_other_thread_reaches_takes_no_lock/) | 25 456 | 5 176 | 3 301 | 1 517 121 | 7.71 | 0.02 |  |
| [counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts](counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts/) | 40 053 | 10 987 | 5 370 | 499 001 | 7.46 | 0.08 |  |
| [short_text_lives_inside_the_string](short_text_lives_inside_the_string/) | 129 600 | 267 808 | 17 489 | 540 951 | 7.41 | 0.24 |  |
| [a_dictionary_written_out_and_only_read_by_literal_keys_is_folded](a_dictionary_written_out_and_only_read_by_literal_keys_is_folded/) | 40 260 | 404 116 | 5 842 | 1 434 668 | 6.89 | 0.03 |  |
| [a_binary_schema_is_a_constant](a_binary_schema_is_a_constant/) | 5 320 | 372 775 | 842 | 11 063 599 | 6.32 | 0.00 |  |
| [a_crashs_report_is_kept_out_of_the_way](a_crashs_report_is_kept_out_of_the_way/) | 62 955 | 13 689 | 10 253 | 2 722 551 | 6.14 | 0.02 |  |
| [boxing_only_where_a_value_travels_as_a_shape](boxing_only_where_a_value_travels_as_a_shape/) | 71 299 | 96 039 | 12 157 | 164 235 | 5.86 | 0.43 |  |
| [vector_maths](vector_maths/) | 285 001 | 63 634 | 48 999 | 45 727 764 | 5.82 | 0.01 |  |
| [a_number_joined_into_text_is_written_in_place](a_number_joined_into_text_is_written_in_place/) | 89 822 | 329 356 | 15 966 | 415 005 | 5.63 | 0.22 |  |
| [deciding_conditions_at_compile_time](deciding_conditions_at_compile_time/) | 42 887 | 8 849 | 7 637 | 2 769 607 | 5.62 | 0.02 |  |
| [appending_to_text_in_place](appending_to_text_in_place/) | 1 022 | 63 078 | 195 | 5 824 | 5.24 | 0.18 |  |
| [calls_in_a_row_run_at_once](calls_in_a_row_run_at_once/) | 101 644 | 43 410 | 23 460 | 4 272 706 | 4.33 | 0.02 |  |
| [copies_that_cost_nothing](copies_that_cost_nothing/) | 71 278 | 22 863 | 16 617 | 6 318 051 | 4.29 | 0.01 |  |
| [a_loop_over_a_list_of_different_classes_runs_them_at_once](a_loop_over_a_list_of_different_classes_runs_them_at_once/) | 396 459 | 273 305 | 93 733 | 7 734 116 | 4.23 | 0.05 |  |
| [plain_reference_counts_where_no_thread_reaches_a_class](plain_reference_counts_where_no_thread_reaches_a_class/) | 41 637 | 28 150 | 10 993 | 1 038 683 | 3.79 | 0.04 |  |
| [a_dictionary_hashes_a_key_once_cheaply](a_dictionary_hashes_a_key_once_cheaply/) | 97 088 | 87 143 | 26 485 | 249 112 | 3.67 | 0.39 |  |
| [tokens_as_columns](tokens_as_columns/) | 232 415 | 136 569 | 75 660 | 2 579 567 | 3.07 | 0.09 |  |
| [objects_made_for_their_owner_are_told_apart](objects_made_for_their_owner_are_told_apart/) | 180 234 | 118 222 | 59 932 | 5 609 719 | 3.01 | 0.03 |  |
| [a_dictionary_keyed_by_numbers_hashes_the_numbers](a_dictionary_keyed_by_numbers_hashes_the_numbers/) | 41 312 | 15 822 | 14 060 | 488 714 | 2.94 | 0.08 |  |
| [a_proven_divisor_is_not_checked](a_proven_divisor_is_not_checked/) | 61 966 | 31 294 | 28 182 | 1 225 370 | 2.20 | 0.05 |  |
| [the_thread_pool_only_where_a_parallel_is_made](the_thread_pool_only_where_a_parallel_is_made/) | 10 349 | 7 618 | 7 620 | 784 437 | 1.36 | 0.01 |  |
| [reads_in_a_row_overlap](reads_in_a_row_overlap/) | 6 993 | 6 661 | 5 508 | 8 318 | 1.27 | 0.84 |  |
| [a_wait_in_a_frame_does_not_hold_the_frame](a_wait_in_a_frame_does_not_hold_the_frame/) | 86 416 | 1 176 714 | 924 643 | 316 595 | 0.09 | 0.27 |  |
| [allocation_is_the_c_librarys_counted_only_where_read](allocation_is_the_c_librarys_counted_only_where_read/) |  |  |  |  |  |  | build: does not compile: allocation_is_the_c_librarys_counted_only_where_read/allocation_is_the_c_librarys_counted_only_where_read.spite:45: error: this value may be null (it is a Node?), so 'value' cannot be read from it yet... |

Last measured 2026-10-22: best of 5 interleaved runs (a form stops repeating once its runs pass 30 s), on AMD Ryzen 9 5950X 16-Core Processor, 32 logical processors; C with clang version 19.1.5 -O2, Python 3.12.10, Spite with `D:\Projects\SpiteCompiler\.spite\spite.exe`.
<!-- /results -->
