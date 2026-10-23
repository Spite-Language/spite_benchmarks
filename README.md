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
| [a_write_back_of_what_the_slot_already_holds_is_not_written](a_write_back_of_what_the_slot_already_holds_is_not_written/) | 35 763 | 5 072 | 576 | 1 991 959 | 62.09 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_list_of_lists_filled_again_keeps_each_lists_room](a_list_of_lists_filled_again_keeps_each_lists_room/) | 241 551 | 321 867 | 6 453 | 1 277 007 | 37.43 | 0.19 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [an_argument_its_caller_holds_is_passed_without_counting](an_argument_its_caller_holds_is_passed_without_counting/) | 26 366 | 34 516 | 705 | 1 441 816 | 37.40 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_walked_crash_lines_read_is_the_rows_read](a_walked_crash_lines_read_is_the_rows_read/) | 162 110 | 17 924 | 4 549 | 6 463 001 | 35.64 | 0.03 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [defaults_the_constructor_replaces_are_never_made](defaults_the_constructor_replaces_are_never_made/) | 10 114 | 44 792 | 337 | 309 734 | 30.01 | 0.03 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [an_item_written_back_to_its_own_slot_is_not_written](an_item_written_back_to_its_own_slot_is_not_written/) | 101 977 | 43 886 | 3 604 | 2 278 712 | 28.30 | 0.04 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [text_building](text_building/) | 229 100 | 83 969 | 9 667 | 616 016 | 23.70 | 0.37 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [maths_on_constants_is_worked_out_while_compiling](maths_on_constants_is_worked_out_while_compiling/) | 60 822 | 13 316 | 2 783 | 28 538 599 | 21.85 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_word_inflected_while_compiling](a_word_inflected_while_compiling/) | 67 970 | 275 585 | 3 363 | 910 544 | 20.21 | 0.07 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked](a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked/) | 311 954 | 146 760 | 16 271 | 14 208 348 | 19.17 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [report_over_records](report_over_records/) | 417 816 | 626 851 | 22 807 | 6 559 636 | 18.32 | 0.06 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_row_of_borrowed_items_lives_in_the_frame](a_row_of_borrowed_items_lives_in_the_frame/) | 54 735 | 7 393 | 3 096 | 5 216 080 | 17.68 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_decimal_literal_beside_a_float_is_a_float](a_decimal_literal_beside_a_float_is_a_float/) | 262 462 | 521 932 | 16 333 | 50 302 153 | 16.07 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one](a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one/) | 16 011 | 74 780 | 1 023 | 372 496 | 15.65 | 0.04 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [template_chains_run_as_one_loop](template_chains_run_as_one_loop/) | 22 139 | 84 836 | 1 485 | 1 809 593 | 14.91 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [an_items_storage_is_chosen_while_compiling](an_items_storage_is_chosen_while_compiling/) | 33 398 | 30 360 | 2 241 | 1 644 766 | 14.90 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [arithmetic_is_checked_in_every_build](arithmetic_is_checked_in_every_build/) | 39 307 | 3 008 | 2 659 | 1 742 323 | 14.78 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_function_value_describes_its_arguments_when_asked](a_function_value_describes_its_arguments_when_asked/) | 18 082 | 1 240 | 1 229 | 844 992 | 14.71 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [objects_of_one_class_sit_together](objects_of_one_class_sit_together/) | 35 536 | 24 549 | 2 546 | 563 532 | 13.96 | 0.06 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_singletons_attribute_that_never_changes_is_read_in_place](a_singletons_attribute_that_never_changes_is_read_in_place/) | 49 309 | 142 183 | 3 617 | 2 001 653 | 13.63 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [smaller_ones](smaller_ones/) | 130 433 | 10 871 | 9 626 | 3 222 921 | 13.55 | 0.04 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_list_held_only_by_another_list_lives_in_its_slot](a_list_held_only_by_another_list_lives_in_its_slot/) | 479 209 | 282 875 | 36 278 | 5 416 782 | 13.21 | 0.09 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [the_compiler_places_memory](the_compiler_places_memory/) | 114 532 | 32 913 | 8 761 | 2 417 200 | 13.07 | 0.05 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_numbers_bits_are_read_in_place](a_numbers_bits_are_read_in_place/) | 302 327 | 89 467 | 23 285 | 30 219 113 | 12.98 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [text_joined_in_one_piece](text_joined_in_one_piece/) | 43 384 | 96 006 | 3 413 | 140 479 | 12.71 | 0.31 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [while_no_task_runs_a_singletons_lock_is_skipped](while_no_task_runs_a_singletons_lock_is_skipped/) | 28 736 | 51 805 | 2 296 | 2 188 513 | 12.52 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [game_maths](game_maths/) | 21 617 | 2 215 | 1 741 | 7 151 617 | 12.42 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [records_sorted_by_one_field](records_sorted_by_one_field/) | 1 119 117 | 687 560 | 91 791 | 4 903 540 | 12.19 | 0.23 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted](an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted/) | 26 301 | 16 067 | 2 163 | 2 202 888 | 12.16 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_lists_templates_read_its_elements_without_counting_them](a_lists_templates_read_its_elements_without_counting_them/) | 28 219 | 30 375 | 2 393 | 1 606 782 | 11.79 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [sorting](sorting/) | 233 453 | 122 406 | 20 763 | 1 163 832 | 11.24 | 0.20 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [particles](particles/) | 117 691 | 28 564 | 10 492 | 27 018 487 | 11.22 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [image_filter_over_planes](image_filter_over_planes/) | 249 629 | 249 070 | 22 396 | 8 038 059 | 11.15 | 0.03 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [reading_through_a_type_without_counting](reading_through_a_type_without_counting/) | 59 722 | 9 501 | 5 376 | 5 607 329 | 11.11 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [atomic_reference_counts_only_with_threads](atomic_reference_counts_only_with_threads/) | 23 894 | 19 746 | 2 192 | 276 576 | 10.90 | 0.09 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_proven_read_tests_only_its_bounds](a_proven_read_tests_only_its_bounds/) | 66 446 | 6 750 | 6 634 | 7 655 491 | 10.02 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [an_item_a_name_holds_from_its_list_is_not_counted](an_item_a_name_holds_from_its_list_is_not_counted/) | 16 842 | 15 004 | 1 705 | 1 346 494 | 9.88 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [spreadsheet_recalculation](spreadsheet_recalculation/) | 1 068 916 | 698 403 | 110 209 | 11 397 638 | 9.70 | 0.09 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [reading_an_address_is_one_machine_operation](reading_an_address_is_one_machine_operation/) | 38 995 | 5 572 | 4 044 | 2 497 654 | 9.64 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame](a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame/) | 38 143 | 3 985 | 3 993 | 435 520 | 9.55 | 0.09 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once](a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once/) | 28 983 | 312 814 | 3 103 | 4 826 240 | 9.34 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_binary_schema_is_a_constant](a_binary_schema_is_a_constant/) | 5 370 | 352 950 | 581 | 11 027 599 | 9.24 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot](storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot/) | 40 435 | 6 585 | 4 380 | 1 233 291 | 9.23 | 0.03 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [singletons_a_parallel_reaches_take_a_lock](singletons_a_parallel_reaches_take_a_lock/) | 4 769 | 19 964 | 543 | 258 395 | 8.78 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [removing_many_at_once](removing_many_at_once/) | 182 262 | 24 749 | 21 022 | 5 752 384 | 8.67 | 0.03 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [reflection_on_constants_folds_and_unrolls](reflection_on_constants_folds_and_unrolls/) | 21 016 | 12 226 | 2 648 | 8 562 284 | 7.94 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [concurrency_machinery_only_where_it_is_used](concurrency_machinery_only_where_it_is_used/) | 10 668 | 10 897 | 1 498 | 14 211 | 7.12 | 0.75 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_singleton_no_other_thread_reaches_takes_no_lock](a_singleton_no_other_thread_reaches_takes_no_lock/) | 21 227 | 4 879 | 3 189 | 1 443 280 | 6.66 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [short_text_lives_inside_the_string](short_text_lives_inside_the_string/) | 109 814 | 256 339 | 17 319 | 524 807 | 6.34 | 0.21 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [number_dictionary](number_dictionary/) | 81 138 | 43 082 | 13 168 | 407 743 | 6.16 | 0.20 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_number_joined_into_text_is_written_in_place](a_number_joined_into_text_is_written_in_place/) | 95 540 | 318 914 | 15 536 | 397 684 | 6.15 | 0.24 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [allocation_is_the_c_librarys_counted_only_where_read](allocation_is_the_c_librarys_counted_only_where_read/) | 17 066 | 60 241 | 2 832 | 390 519 | 6.03 | 0.04 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_number_read_from_bytes_is_one_load](a_number_read_from_bytes_is_one_load/) | 180 675 | 52 936 | 31 968 | 30 589 244 | 5.65 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [objects_that_never_leave_their_function_live_in_the_frame](objects_that_never_leave_their_function_live_in_the_frame/) | 80 824 | 1 035 422 | 14 645 | 46 247 601 | 5.52 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [appending_to_text_in_place](appending_to_text_in_place/) | 1 021 | 60 795 | 186 | 5 690 | 5.49 | 0.18 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_function_taking_a_type_is_compiled_per_class](a_function_taking_a_type_is_compiled_per_class/) | 286 257 | 52 348 | 52 261 | 14 626 240 | 5.48 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [boxing_only_where_a_value_travels_as_a_shape](boxing_only_where_a_value_travels_as_a_shape/) | 57 342 | 93 833 | 12 080 | 164 552 | 4.75 | 0.35 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts](counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts/) | 24 776 | 10 828 | 5 335 | 483 905 | 4.64 | 0.05 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [thread_safety_for_singletons_the_cheapest_safe_form](thread_safety_for_singletons_the_cheapest_safe_form/) | 1 899 | 165 337 | 416 | 1 417 535 | 4.56 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_list_item_read_only_to_test_it_is_not_counted](a_list_item_read_only_to_test_it_is_not_counted/) | 53 256 | 64 250 | 11 693 | 2 901 289 | 4.55 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_test_against_a_value_a_list_never_holds_is_decided_while_compiling](a_test_against_a_value_a_list_never_holds_is_decided_while_compiling/) | 89 686 | 39 397 | 20 044 | 3 445 948 | 4.47 | 0.03 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_table_filled_once_is_read_as_constants](a_table_filled_once_is_read_as_constants/) | 90 378 | 21 167 | 20 300 | 3 469 414 | 4.45 | 0.03 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [an_attribute_a_call_cannot_assign_is_passed_without_counting](an_attribute_a_call_cannot_assign_is_passed_without_counting/) | 10 893 | 4 415 | 2 628 | 1 511 757 | 4.14 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_dictionary_written_out_and_only_read_by_literal_keys_is_folded](a_dictionary_written_out_and_only_read_by_literal_keys_is_folded/) | 22 975 | 378 909 | 5 677 | 1 403 137 | 4.05 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_local_list_of_known_size_lives_in_the_frame](a_local_list_of_known_size_lives_in_the_frame/) | 93 626 | 23 711 | 23 305 | 3 934 282 | 4.02 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [an_allocator_set_after_construction_is_where_the_object_is_made](an_allocator_set_after_construction_is_where_the_object_is_made/) | 7 333 | 76 973 | 2 042 | 463 243 | 3.59 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_loop_over_a_list_of_different_classes_runs_them_at_once](a_loop_over_a_list_of_different_classes_runs_them_at_once/) | 334 311 | 274 965 | 93 406 | 8 235 204 | 3.58 | 0.04 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [objects_made_for_their_owner_are_told_apart](objects_made_for_their_owner_are_told_apart/) | 207 777 | 116 958 | 59 697 | 5 680 385 | 3.48 | 0.04 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [plain_reference_counts_where_no_thread_reaches_a_class](plain_reference_counts_where_no_thread_reaches_a_class/) | 37 390 | 27 081 | 10 906 | 1 025 098 | 3.43 | 0.04 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [calls_in_a_row_run_at_once](calls_in_a_row_run_at_once/) | 78 884 | 44 415 | 23 733 | 4 458 378 | 3.32 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_dictionary_hashes_a_key_once_cheaply](a_dictionary_hashes_a_key_once_cheaply/) | 77 300 | 88 386 | 25 655 | 252 852 | 3.01 | 0.31 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [copies_that_cost_nothing](copies_that_cost_nothing/) | 48 189 | 22 730 | 16 778 | 6 375 844 | 2.87 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_dictionary_keyed_by_numbers_hashes_the_numbers](a_dictionary_keyed_by_numbers_hashes_the_numbers/) | 34 566 | 15 424 | 13 158 | 489 811 | 2.63 | 0.07 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_crashs_report_is_kept_out_of_the_way](a_crashs_report_is_kept_out_of_the_way/) | 23 555 | 13 375 | 9 883 | 2 641 983 | 2.38 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [thread_safety_for_singletons_the_rest_of_the_plan](thread_safety_for_singletons_the_rest_of_the_plan/) | 4 650 | 20 154 | 2 116 | 256 198 | 2.20 | 0.02 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_proven_divisor_is_not_checked](a_proven_divisor_is_not_checked/) | 56 010 | 29 663 | 26 607 | 1 168 315 | 2.11 | 0.05 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [vector_maths](vector_maths/) | 100 949 | 63 199 | 48 356 | 29 515 093 | 2.09 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [singletons_made_on_first_use_never_counted](singletons_made_on_first_use_never_counted/) | 11 830 | 214 569 | 5 814 | 7 211 329 | 2.03 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [tokens_as_columns](tokens_as_columns/) | 140 471 | 134 475 | 75 266 | 2 531 390 | 1.87 | 0.06 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [deciding_conditions_at_compile_time](deciding_conditions_at_compile_time/) | 13 344 | 8 766 | 8 037 | 2 800 634 | 1.66 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [the_thread_pool_only_where_a_parallel_is_made](the_thread_pool_only_where_a_parallel_is_made/) | 9 260 | 7 288 | 7 279 | 727 108 | 1.27 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_singletons_reading_functions_do_not_exclude_each_other](a_singletons_reading_functions_do_not_exclude_each_other/) | 7 301 | 97 370 | 6 118 | 611 120 | 1.19 | 0.01 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [reads_in_a_row_overlap](reads_in_a_row_overlap/) | 6 682 | 6 765 | 5 947 | 8 487 | 1.12 | 0.79 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_loop_whose_passes_write_only_their_own_item_runs_in_bands](a_loop_whose_passes_write_only_their_own_item_runs_in_bands/) | 46 935 | 784 022 | 44 565 | 274 129 124 | 1.05 | 0.00 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |
| [a_wait_in_a_frame_does_not_hold_the_frame](a_wait_in_a_frame_does_not_hold_the_frame/) | 87 812 | 1 174 022 | 921 486 | 315 348 | 0.10 | 0.28 | timed with D:\Projects\worktrees\compiler_ranges\.spite\s2.exe |

Last measured 2026-10-23: best of 5 interleaved runs (a form stops repeating once its runs pass 30 s), on AMD Ryzen 9 5950X 16-Core Processor, 32 logical processors; C with clang version 19.1.5 -O2, Python 3.12.10, Spite with `D:\Projects\worktrees\compiler_ranges\.spite\s2.exe`.
<!-- /results -->
