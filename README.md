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
| [a_write_back_of_what_the_slot_already_holds_is_not_written](a_write_back_of_what_the_slot_already_holds_is_not_written/) | 38 744 | 5 031 | 537 | 1 950 628 | 72.15 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_walked_crash_lines_read_is_the_rows_read](a_walked_crash_lines_read_is_the_rows_read/) | 306 961 | 17 738 | 4 569 | 5 979 401 | 67.18 | 0.05 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_list_of_lists_filled_again_keeps_each_lists_room](a_list_of_lists_filled_again_keeps_each_lists_room/) | 321 294 | 296 325 | 6 481 | 1 159 793 | 49.57 | 0.28 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [objects_of_one_class_sit_together](objects_of_one_class_sit_together/) | 96 891 | 21 662 | 2 358 | 525 533 | 41.09 | 0.18 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [an_argument_its_caller_holds_is_passed_without_counting](an_argument_its_caller_holds_is_passed_without_counting/) | 26 445 | 34 219 | 675 | 1 400 050 | 39.18 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [report_over_records](report_over_records/) | 847 638 | 579 832 | 22 371 | 6 183 288 | 37.89 | 0.14 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one](a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one/) | 37 024 | 73 730 | 1 015 | 352 293 | 36.48 | 0.11 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [singletons_a_parallel_reaches_take_a_lock](singletons_a_parallel_reaches_take_a_lock/) | 17 671 | 19 477 | 502 | 252 979 | 35.20 | 0.07 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [defaults_the_constructor_replaces_are_never_made](defaults_the_constructor_replaces_are_never_made/) | 11 167 | 41 459 | 334 | 305 878 | 33.43 | 0.04 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_local_list_of_known_size_lives_in_the_frame](a_local_list_of_known_size_lives_in_the_frame/) | 694 654 | 23 408 | 22 887 | 3 767 340 | 30.35 | 0.18 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [reading_an_address_is_one_machine_operation](reading_an_address_is_one_machine_operation/) | 115 565 | 5 683 | 3 999 | 2 437 298 | 28.90 | 0.05 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [an_item_written_back_to_its_own_slot_is_not_written](an_item_written_back_to_its_own_slot_is_not_written/) | 101 148 | 43 180 | 3 505 | 2 261 173 | 28.86 | 0.04 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_lists_templates_read_its_elements_without_counting_them](a_lists_templates_read_its_elements_without_counting_them/) | 60 608 | 29 292 | 2 133 | 1 539 020 | 28.41 | 0.04 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_singletons_reading_functions_do_not_exclude_each_other](a_singletons_reading_functions_do_not_exclude_each_other/) | 125 401 | 88 897 | 4 678 | 589 535 | 26.81 | 0.21 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [maths_on_constants_is_worked_out_while_compiling](maths_on_constants_is_worked_out_while_compiling/) | 65 077 | 13 573 | 2 819 | 26 343 051 | 23.09 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [text_building](text_building/) | 217 441 | 83 878 | 9 580 | 592 978 | 22.70 | 0.37 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_word_inflected_while_compiling](a_word_inflected_while_compiling/) | 72 825 | 268 394 | 3 320 | 881 979 | 21.94 | 0.08 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame](a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame/) | 83 472 | 3 860 | 3 929 | 425 045 | 21.25 | 0.20 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_row_of_borrowed_items_lives_in_the_frame](a_row_of_borrowed_items_lives_in_the_frame/) | 56 706 | 6 684 | 2 838 | 4 933 505 | 19.98 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [template_chains_run_as_one_loop](template_chains_run_as_one_loop/) | 30 270 | 80 924 | 1 551 | 1 633 653 | 19.52 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked](a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked/) | 309 155 | 143 423 | 16 034 | 13 698 872 | 19.28 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [an_allocator_set_after_construction_is_where_the_object_is_made](an_allocator_set_after_construction_is_where_the_object_is_made/) | 37 501 | 75 317 | 2 014 | 459 794 | 18.62 | 0.08 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [records_sorted_by_one_field](records_sorted_by_one_field/) | 1 528 388 | 642 087 | 88 003 | 4 633 597 | 17.37 | 0.33 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [an_items_storage_is_chosen_while_compiling](an_items_storage_is_chosen_while_compiling/) | 34 725 | 29 760 | 2 085 | 1 609 147 | 16.65 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_function_value_describes_its_arguments_when_asked](a_function_value_describes_its_arguments_when_asked/) | 20 116 | 1 233 | 1 217 | 828 493 | 16.53 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_decimal_literal_beside_a_float_is_a_float](a_decimal_literal_beside_a_float_is_a_float/) | 257 979 | 515 300 | 16 106 | 47 413 130 | 16.02 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [while_no_task_runs_a_singletons_lock_is_skipped](while_no_task_runs_a_singletons_lock_is_skipped/) | 34 976 | 50 816 | 2 266 | 2 145 097 | 15.44 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_singletons_attribute_that_never_changes_is_read_in_place](a_singletons_attribute_that_never_changes_is_read_in_place/) | 47 989 | 141 432 | 3 148 | 1 943 221 | 15.24 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [particles](particles/) | 141 774 | 28 186 | 9 935 | 25 296 757 | 14.27 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_numbers_bits_are_read_in_place](a_numbers_bits_are_read_in_place/) | 316 398 | 87 749 | 22 793 | 28 263 394 | 13.88 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [arithmetic_is_checked_in_every_build](arithmetic_is_checked_in_every_build/) | 35 238 | 2 970 | 2 595 | 1 668 529 | 13.58 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [the_compiler_places_memory](the_compiler_places_memory/) | 113 418 | 32 696 | 8 618 | 2 292 126 | 13.16 | 0.05 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [removing_many_at_once](removing_many_at_once/) | 270 224 | 24 074 | 20 884 | 5 449 486 | 12.94 | 0.05 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [game_maths](game_maths/) | 21 452 | 2 186 | 1 699 | 6 783 769 | 12.63 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted](an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted/) | 26 908 | 15 948 | 2 134 | 2 158 666 | 12.61 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [text_joined_in_one_piece](text_joined_in_one_piece/) | 41 589 | 94 097 | 3 361 | 134 040 | 12.37 | 0.31 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [reading_through_a_type_without_counting](reading_through_a_type_without_counting/) | 67 800 | 9 548 | 5 516 | 5 207 925 | 12.29 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [atomic_reference_counts_only_with_threads](atomic_reference_counts_only_with_threads/) | 25 848 | 18 331 | 2 134 | 266 571 | 12.11 | 0.10 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [sorting](sorting/) | 237 081 | 121 089 | 19 745 | 1 081 366 | 12.01 | 0.22 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_list_held_only_by_another_list_lives_in_its_slot](a_list_held_only_by_another_list_lives_in_its_slot/) | 424 884 | 237 948 | 35 471 | 6 445 513 | 11.98 | 0.07 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [smaller_ones](smaller_ones/) | 106 867 | 10 247 | 8 977 | 3 130 579 | 11.90 | 0.03 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [image_filter_over_planes](image_filter_over_planes/) | 247 402 | 235 283 | 21 596 | 7 506 924 | 11.46 | 0.03 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [an_item_a_name_holds_from_its_list_is_not_counted](an_item_a_name_holds_from_its_list_is_not_counted/) | 18 783 | 14 890 | 1 763 | 1 299 726 | 10.65 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [thread_safety_for_singletons_the_rest_of_the_plan](thread_safety_for_singletons_the_rest_of_the_plan/) | 18 312 | 19 206 | 1 894 | 252 038 | 9.67 | 0.07 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [reflection_on_constants_folds_and_unrolls](reflection_on_constants_folds_and_unrolls/) | 23 526 | 12 248 | 2 450 | 7 923 285 | 9.60 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [spreadsheet_recalculation](spreadsheet_recalculation/) | 987 302 | 614 947 | 104 572 | 11 146 690 | 9.44 | 0.09 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_proven_read_tests_only_its_bounds](a_proven_read_tests_only_its_bounds/) | 58 900 | 6 578 | 6 487 | 7 201 769 | 9.08 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot](storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot/) | 38 163 | 6 514 | 4 341 | 1 204 113 | 8.79 | 0.03 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_number_read_from_bytes_is_one_load](a_number_read_from_bytes_is_one_load/) | 273 902 | 52 460 | 31 225 | 26 434 454 | 8.77 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_binary_schema_is_a_constant](a_binary_schema_is_a_constant/) | 4 650 | 350 629 | 566 | 10 184 790 | 8.22 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_function_taking_a_type_is_compiled_per_class](a_function_taking_a_type_is_compiled_per_class/) | 410 890 | 51 824 | 51 824 | 13 578 756 | 7.93 | 0.03 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [concurrency_machinery_only_where_it_is_used](concurrency_machinery_only_where_it_is_used/) | 10 776 | 10 452 | 1 503 | 13 021 | 7.17 | 0.83 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_singleton_no_other_thread_reaches_takes_no_lock](a_singleton_no_other_thread_reaches_takes_no_lock/) | 21 971 | 4 796 | 3 081 | 1 387 459 | 7.13 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [allocation_is_the_c_librarys_counted_only_where_read](allocation_is_the_c_librarys_counted_only_where_read/) | 17 745 | 59 323 | 2 800 | 375 597 | 6.34 | 0.05 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_number_joined_into_text_is_written_in_place](a_number_joined_into_text_is_written_in_place/) | 98 222 | 313 433 | 15 629 | 400 956 | 6.28 | 0.24 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once](a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once/) | 18 152 | 307 710 | 2 974 | 4 598 218 | 6.10 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [objects_that_never_leave_their_function_live_in_the_frame](objects_that_never_leave_their_function_live_in_the_frame/) | 85 528 | 1 007 196 | 14 366 | 43 266 523 | 5.95 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_table_filled_once_is_read_as_constants](a_table_filled_once_is_read_as_constants/) | 112 368 | 20 660 | 19 576 | 3 370 382 | 5.74 | 0.03 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [boxing_only_where_a_value_travels_as_a_shape](boxing_only_where_a_value_travels_as_a_shape/) | 66 635 | 83 630 | 11 758 | 156 648 | 5.67 | 0.43 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [number_dictionary](number_dictionary/) | 64 966 | 18 715 | 11 542 | 351 776 | 5.63 | 0.18 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [short_text_lives_inside_the_string](short_text_lives_inside_the_string/) | 95 506 | 246 537 | 17 025 | 524 514 | 5.61 | 0.18 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_test_against_a_value_a_list_never_holds_is_decided_while_compiling](a_test_against_a_value_a_list_never_holds_is_decided_while_compiling/) | 107 250 | 38 739 | 19 829 | 3 376 092 | 5.41 | 0.03 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [appending_to_text_in_place](appending_to_text_in_place/) | 1 030 | 60 311 | 193 | 5 635 | 5.34 | 0.18 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_dictionary_written_out_and_only_read_by_literal_keys_is_folded](a_dictionary_written_out_and_only_read_by_literal_keys_is_folded/) | 28 725 | 355 156 | 5 661 | 1 371 877 | 5.07 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts](counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts/) | 26 764 | 10 706 | 5 304 | 480 807 | 5.05 | 0.06 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_list_item_read_only_to_test_it_is_not_counted](a_list_item_read_only_to_test_it_is_not_counted/) | 56 208 | 63 261 | 11 365 | 2 653 851 | 4.95 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [thread_safety_for_singletons_the_cheapest_safe_form](thread_safety_for_singletons_the_cheapest_safe_form/) | 1 838 | 156 846 | 423 | 1 381 367 | 4.35 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [an_attribute_a_call_cannot_assign_is_passed_without_counting](an_attribute_a_call_cannot_assign_is_passed_without_counting/) | 10 839 | 4 305 | 2 597 | 1 462 246 | 4.17 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [plain_reference_counts_where_no_thread_reaches_a_class](plain_reference_counts_where_no_thread_reaches_a_class/) | 42 993 | 26 329 | 10 728 | 1 007 804 | 4.01 | 0.04 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_dictionary_hashes_a_key_once_cheaply](a_dictionary_hashes_a_key_once_cheaply/) | 92 593 | 82 894 | 25 258 | 241 255 | 3.67 | 0.38 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_loop_over_a_list_of_different_classes_runs_them_at_once](a_loop_over_a_list_of_different_classes_runs_them_at_once/) | 324 314 | 268 912 | 92 867 | 7 667 283 | 3.49 | 0.04 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [copies_that_cost_nothing](copies_that_cost_nothing/) | 52 906 | 22 388 | 16 233 | 5 989 436 | 3.26 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [calls_in_a_row_run_at_once](calls_in_a_row_run_at_once/) | 74 806 | 42 526 | 23 281 | 4 250 964 | 3.21 | 0.02 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_dictionary_keyed_by_numbers_hashes_the_numbers](a_dictionary_keyed_by_numbers_hashes_the_numbers/) | 40 405 | 15 834 | 13 189 | 474 155 | 3.06 | 0.09 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [objects_made_for_their_owner_are_told_apart](objects_made_for_their_owner_are_told_apart/) | 177 892 | 115 374 | 58 803 | 5 413 227 | 3.03 | 0.03 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_crashs_report_is_kept_out_of_the_way](a_crashs_report_is_kept_out_of_the_way/) | 26 689 | 13 299 | 9 829 | 2 545 821 | 2.72 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [vector_maths](vector_maths/) | 122 878 | 61 695 | 47 757 | 28 187 925 | 2.57 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [tokens_as_columns](tokens_as_columns/) | 180 573 | 130 580 | 73 392 | 2 437 097 | 2.46 | 0.07 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_proven_divisor_is_not_checked](a_proven_divisor_is_not_checked/) | 56 908 | 29 011 | 26 076 | 1 139 739 | 2.18 | 0.05 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [singletons_made_on_first_use_never_counted](singletons_made_on_first_use_never_counted/) | 11 539 | 212 660 | 5 614 | 6 827 632 | 2.06 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [deciding_conditions_at_compile_time](deciding_conditions_at_compile_time/) | 12 265 | 8 616 | 7 495 | 2 729 748 | 1.64 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [reads_in_a_row_overlap](reads_in_a_row_overlap/) | 6 785 | 6 298 | 4 838 | 7 831 | 1.40 | 0.87 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [the_thread_pool_only_where_a_parallel_is_made](the_thread_pool_only_where_a_parallel_is_made/) | 8 934 | 7 367 | 7 199 | 709 731 | 1.24 | 0.01 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_loop_whose_passes_write_only_their_own_item_runs_in_bands](a_loop_whose_passes_write_only_their_own_item_runs_in_bands/) | 34 079 | 769 792 | 31 971 | 252 139 263 | 1.07 | 0.00 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |
| [a_wait_in_a_frame_does_not_hold_the_frame](a_wait_in_a_frame_does_not_hold_the_frame/) | 88 990 | 1 176 799 | 924 587 | 315 887 | 0.10 | 0.28 | timed with D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe |

Last measured 2026-10-23: best of 5 interleaved runs (a form stops repeating once its runs pass 30 s), on AMD Ryzen 9 5950X 16-Core Processor, 32 logical processors; C with clang version 19.1.5 -O2, Python 3.12.10, Spite with `D:\Projects\worktrees\validate\SpiteCompiler\.spite\spite.exe`.
<!-- /results -->
