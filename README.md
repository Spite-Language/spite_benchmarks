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
| [maths_on_constants_is_worked_out_while_compiling](maths_on_constants_is_worked_out_while_compiling/) | 240 858 891 | 13 714 | 2 907 | 30 598 627 | 82854.80 | 7.87 |  |
| [a_word_inflected_while_compiling](a_word_inflected_while_compiling/) | 37 624 659 | 273 046 | 3 428 | 905 997 | 10975.69 | 41.53 |  |
| [a_row_of_borrowed_items_lives_in_the_frame](a_row_of_borrowed_items_lives_in_the_frame/) | 1 747 729 | 6 799 | 2 947 | 5 079 905 | 593.05 | 0.34 |  |
| [reading_through_a_type_without_counting](reading_through_a_type_without_counting/) | 1 785 912 | 10 144 | 5 638 | 6 275 857 | 316.76 | 0.28 |  |
| [a_numbers_bits_are_read_in_place](a_numbers_bits_are_read_in_place/) | 7 109 298 | 88 275 | 23 005 | 29 148 695 | 309.03 | 0.24 |  |
| [thread_safety_for_singletons_the_cheapest_safe_form](thread_safety_for_singletons_the_cheapest_safe_form/) | 156 633 | 270 747 | 555 | 1 480 211 | 282.22 | 0.11 |  |
| [text_building](text_building/) | 2 666 869 | 91 936 | 10 142 | 642 211 | 262.95 | 4.15 |  |
| [template_chains_run_as_one_loop](template_chains_run_as_one_loop/) | 461 331 | 82 910 | 1 776 | 1 807 257 | 259.76 | 0.26 |  |
| [a_walked_crash_lines_read_is_the_rows_read](a_walked_crash_lines_read_is_the_rows_read/) | 1 189 336 | 18 386 | 4 726 | 7 112 353 | 251.66 | 0.17 |  |
| [defaults_the_constructor_replaces_are_never_made](defaults_the_constructor_replaces_are_never_made/) | 82 160 | 41 931 | 329 | 306 671 | 249.73 | 0.27 |  |
| [a_write_back_of_what_the_slot_already_holds_is_not_written](a_write_back_of_what_the_slot_already_holds_is_not_written/) | 147 561 | 5 256 | 592 | 1 974 265 | 249.26 | 0.07 |  |
| [objects_that_never_leave_their_function_live_in_the_frame](objects_that_never_leave_their_function_live_in_the_frame/) | 3 515 692 | 1 040 903 | 15 185 | 56 403 158 | 231.52 | 0.06 |  |
| [a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one](a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one/) | 228 205 | 73 940 | 1 004 | 351 974 | 227.30 | 0.65 |  |
| [copies_that_cost_nothing](copies_that_cost_nothing/) | 3 673 627 | 22 872 | 16 366 | 6 993 259 | 224.47 | 0.53 |  |
| [image_filter_over_planes](image_filter_over_planes/) | 3 969 457 | 263 032 | 23 038 | 8 680 827 | 172.30 | 0.46 |  |
| [text_joined_in_one_piece](text_joined_in_one_piece/) | 553 256 | 101 144 | 3 526 | 142 866 | 156.91 | 3.87 |  |
| [a_local_list_of_known_size_lives_in_the_frame](a_local_list_of_known_size_lives_in_the_frame/) | 3 582 623 | 23 072 | 22 987 | 3 762 282 | 155.85 | 0.95 |  |
| [a_list_of_lists_filled_again_keeps_each_lists_room](a_list_of_lists_filled_again_keeps_each_lists_room/) | 900 770 | 307 063 | 6 374 | 1 153 499 | 141.32 | 0.78 |  |
| [singletons_made_on_first_use_never_counted](singletons_made_on_first_use_never_counted/) | 786 966 | 246 559 | 5 833 | 7 683 165 | 134.92 | 0.10 |  |
| [report_over_records](report_over_records/) | 2 618 608 | 689 491 | 24 319 | 6 963 324 | 107.68 | 0.38 |  |
| [objects_of_one_class_sit_together](objects_of_one_class_sit_together/) | 233 050 | 22 913 | 2 426 | 562 436 | 96.06 | 0.41 |  |
| [game_maths](game_maths/) | 152 959 | 2 190 | 1 696 | 8 123 771 | 90.19 | 0.02 |  |
| [a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once](a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once/) | 275 881 | 307 364 | 3 117 | 4 956 888 | 88.51 | 0.06 |  |
| [a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame](a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame/) | 350 012 | 3 867 | 3 996 | 426 362 | 87.59 | 0.82 |  |
| [a_function_taking_a_type_is_compiled_per_class](a_function_taking_a_type_is_compiled_per_class/) | 4 463 501 | 51 742 | 51 866 | 14 236 991 | 86.06 | 0.31 |  |
| [a_function_value_describes_its_arguments_when_asked](a_function_value_describes_its_arguments_when_asked/) | 95 511 | 1 231 | 1 223 | 821 858 | 78.10 | 0.12 |  |
| [removing_many_at_once](removing_many_at_once/) | 1 648 414 | 26 001 | 22 046 | 6 300 819 | 74.77 | 0.26 |  |
| [an_allocator_set_after_construction_is_where_the_object_is_made](an_allocator_set_after_construction_is_where_the_object_is_made/) | 154 987 | 79 200 | 2 074 | 472 350 | 74.73 | 0.33 |  |
| [an_argument_its_caller_holds_is_passed_without_counting](an_argument_its_caller_holds_is_passed_without_counting/) | 49 173 | 35 480 | 716 | 1 437 400 | 68.68 | 0.03 |  |
| [a_loop_whose_passes_write_only_their_own_item_runs_in_bands](a_loop_whose_passes_write_only_their_own_item_runs_in_bands/) | 2 413 715 | 765 270 | 37 932 | 259 287 384 | 63.63 | 0.01 |  |
| [the_compiler_places_memory](the_compiler_places_memory/) | 518 744 | 33 893 | 9 121 | 2 507 540 | 56.87 | 0.21 |  |
| [a_singletons_attribute_that_never_changes_is_read_in_place](a_singletons_attribute_that_never_changes_is_read_in_place/) | 172 651 | 157 976 | 3 097 | 1 929 138 | 55.75 | 0.09 |  |
| [an_items_storage_is_chosen_while_compiling](an_items_storage_is_chosen_while_compiling/) | 119 638 | 31 674 | 2 189 | 1 680 120 | 54.65 | 0.07 |  |
| [an_item_written_back_to_its_own_slot_is_not_written](an_item_written_back_to_its_own_slot_is_not_written/) | 198 227 | 43 549 | 3 675 | 2 149 258 | 53.94 | 0.09 |  |
| [an_item_a_name_holds_from_its_list_is_not_counted](an_item_a_name_holds_from_its_list_is_not_counted/) | 91 984 | 15 324 | 1 726 | 1 328 288 | 53.29 | 0.07 |  |
| [a_decimal_literal_beside_a_float_is_a_float](a_decimal_literal_beside_a_float_is_a_float/) | 856 493 | 512 731 | 16 139 | 59 470 652 | 53.07 | 0.01 |  |
| [a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked](a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked/) | 826 085 | 144 204 | 16 006 | 14 496 789 | 51.61 | 0.06 |  |
| [singletons_a_parallel_reaches_take_a_lock](singletons_a_parallel_reaches_take_a_lock/) | 23 694 | 23 693 | 548 | 268 057 | 43.24 | 0.09 |  |
| [reading_an_address_is_one_machine_operation](reading_an_address_is_one_machine_operation/) | 180 058 | 5 879 | 4 222 | 2 675 973 | 42.65 | 0.07 |  |
| [boxing_only_where_a_value_travels_as_a_shape](boxing_only_where_a_value_travels_as_a_shape/) | 494 933 | 85 178 | 12 416 | 158 819 | 39.86 | 3.12 |  |
| [a_lists_templates_read_its_elements_without_counting_them](a_lists_templates_read_its_elements_without_counting_them/) | 85 542 | 29 835 | 2 191 | 1 563 087 | 39.04 | 0.05 |  |
| [short_text_lives_inside_the_string](short_text_lives_inside_the_string/) | 692 304 | 268 514 | 18 276 | 554 210 | 37.88 | 1.25 |  |
| [reflection_on_constants_folds_and_unrolls](reflection_on_constants_folds_and_unrolls/) | 88 052 | 12 724 | 2 811 | 9 498 923 | 31.32 | 0.01 |  |
| [a_number_joined_into_text_is_written_in_place](a_number_joined_into_text_is_written_in_place/) | 435 522 | 309 402 | 15 372 | 391 175 | 28.33 | 1.11 |  |
| [a_list_held_only_by_another_list_lives_in_its_slot](a_list_held_only_by_another_list_lives_in_its_slot/) | 966 309 | 243 968 | 35 508 | 4 877 154 | 27.21 | 0.20 |  |
| [an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted](an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted/) | 57 813 | 16 060 | 2 131 | 2 135 375 | 27.13 | 0.03 |  |
| [records_sorted_by_one_field](records_sorted_by_one_field/) | 2 464 307 | 764 760 | 96 333 | 5 410 000 | 25.58 | 0.46 |  |
| [spreadsheet_recalculation](spreadsheet_recalculation/) | 2 932 817 | 712 667 | 115 212 | 13 388 336 | 25.46 | 0.22 |  |
| [atomic_reference_counts_only_with_threads](atomic_reference_counts_only_with_threads/) | 53 739 | 18 974 | 2 151 | 264 373 | 24.98 | 0.20 |  |
| [a_singletons_reading_functions_do_not_exclude_each_other](a_singletons_reading_functions_do_not_exclude_each_other/) | 124 374 | 88 675 | 6 097 | 577 145 | 20.40 | 0.22 |  |
| [while_no_task_runs_a_singletons_lock_is_skipped](while_no_task_runs_a_singletons_lock_is_skipped/) | 44 245 | 53 976 | 2 419 | 2 298 594 | 18.29 | 0.02 |  |
| [an_attribute_a_call_cannot_assign_is_passed_without_counting](an_attribute_a_call_cannot_assign_is_passed_without_counting/) | 42 511 | 4 475 | 2 681 | 1 487 602 | 15.86 | 0.03 |  |
| [smaller_ones](smaller_ones/) | 158 401 | 10 847 | 10 050 | 3 511 723 | 15.76 | 0.05 |  |
| [arithmetic_is_checked_in_every_build](arithmetic_is_checked_in_every_build/) | 40 128 | 3 024 | 2 599 | 1 701 391 | 15.44 | 0.02 |  |
| [storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot](storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot/) | 68 772 | 6 861 | 4 558 | 1 291 407 | 15.09 | 0.05 |  |
| [appending_to_text_in_place](appending_to_text_in_place/) | 2 850 | 61 972 | 194 | 5 643 | 14.69 | 0.51 |  |
| [a_proven_read_tests_only_its_bounds](a_proven_read_tests_only_its_bounds/) | 91 048 | 6 668 | 6 498 | 7 404 074 | 14.01 | 0.01 |  |
| [sorting](sorting/) | 280 236 | 130 609 | 21 869 | 1 219 384 | 12.81 | 0.23 |  |
| [a_number_read_from_bytes_is_one_load](a_number_read_from_bytes_is_one_load/) | 392 016 | 52 313 | 31 443 | 27 457 010 | 12.47 | 0.01 |  |
| [reads_in_a_row_overlap](reads_in_a_row_overlap/) | 72 020 | 6 886 | 5 855 | 8 926 | 12.30 | 8.07 |  |
| [a_binary_schema_is_a_constant](a_binary_schema_is_a_constant/) | 5 898 | 358 420 | 591 | 14 101 674 | 9.98 | 0.00 |  |
| [a_dictionary_written_out_and_only_read_by_literal_keys_is_folded](a_dictionary_written_out_and_only_read_by_literal_keys_is_folded/) | 56 496 | 353 126 | 5 760 | 1 363 057 | 9.81 | 0.04 |  |
| [tokens_as_columns](tokens_as_columns/) | 752 263 | 144 832 | 79 384 | 2 702 512 | 9.48 | 0.28 |  |
| [a_list_item_read_only_to_test_it_is_not_counted](a_list_item_read_only_to_test_it_is_not_counted/) | 106 953 | 63 234 | 11 435 | 2 650 251 | 9.35 | 0.04 |  |
| [thread_safety_for_singletons_the_rest_of_the_plan](thread_safety_for_singletons_the_rest_of_the_plan/) | 22 904 | 34 240 | 2 538 | 266 684 | 9.02 | 0.09 |  |
| [counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts](counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts/) | 49 638 | 11 304 | 5 552 | 496 000 | 8.94 | 0.10 |  |
| [a_table_filled_once_is_read_as_constants](a_table_filled_once_is_read_as_constants/) | 152 768 | 21 450 | 19 719 | 3 333 566 | 7.75 | 0.05 |  |
| [a_singleton_no_other_thread_reaches_takes_no_lock](a_singleton_no_other_thread_reaches_takes_no_lock/) | 24 149 | 4 776 | 3 154 | 1 410 631 | 7.66 | 0.02 |  |
| [a_test_against_a_value_a_list_never_holds_is_decided_while_compiling](a_test_against_a_value_a_list_never_holds_is_decided_while_compiling/) | 153 995 | 38 991 | 20 121 | 3 452 587 | 7.65 | 0.04 |  |
| [concurrency_machinery_only_where_it_is_used](concurrency_machinery_only_where_it_is_used/) | 11 370 | 10 926 | 1 544 | 13 336 | 7.36 | 0.85 |  |
| [number_dictionary](number_dictionary/) | 79 336 | 21 928 | 12 675 | 399 422 | 6.26 | 0.20 |  |
| [a_crashs_report_is_kept_out_of_the_way](a_crashs_report_is_kept_out_of_the_way/) | 61 549 | 13 668 | 10 124 | 2 573 702 | 6.08 | 0.02 |  |
| [a_dictionary_hashes_a_key_once_cheaply](a_dictionary_hashes_a_key_once_cheaply/) | 142 954 | 82 073 | 25 843 | 239 468 | 5.53 | 0.60 |  |
| [plain_reference_counts_where_no_thread_reaches_a_class](plain_reference_counts_where_no_thread_reaches_a_class/) | 60 165 | 28 003 | 11 428 | 1 082 950 | 5.26 | 0.06 |  |
| [calls_in_a_row_run_at_once](calls_in_a_row_run_at_once/) | 99 750 | 42 417 | 23 118 | 4 113 211 | 4.31 | 0.02 |  |
| [a_loop_over_a_list_of_different_classes_runs_them_at_once](a_loop_over_a_list_of_different_classes_runs_them_at_once/) | 384 938 | 268 435 | 92 251 | 7 850 687 | 4.17 | 0.05 |  |
| [deciding_conditions_at_compile_time](deciding_conditions_at_compile_time/) | 28 282 | 8 698 | 7 604 | 2 734 435 | 3.72 | 0.01 |  |
| [objects_made_for_their_owner_are_told_apart](objects_made_for_their_owner_are_told_apart/) | 183 191 | 119 473 | 60 701 | 5 819 009 | 3.02 | 0.03 |  |
| [a_dictionary_keyed_by_numbers_hashes_the_numbers](a_dictionary_keyed_by_numbers_hashes_the_numbers/) | 39 667 | 15 160 | 13 173 | 461 973 | 3.01 | 0.09 |  |
| [a_proven_divisor_is_not_checked](a_proven_divisor_is_not_checked/) | 66 995 | 29 247 | 26 162 | 1 123 896 | 2.56 | 0.06 |  |
| [the_thread_pool_only_where_a_parallel_is_made](the_thread_pool_only_where_a_parallel_is_made/) | 11 358 | 7 554 | 7 629 | 772 919 | 1.49 | 0.01 |  |
| [a_wait_in_a_frame_does_not_hold_the_frame](a_wait_in_a_frame_does_not_hold_the_frame/) | 945 331 | 1 186 542 | 923 666 | 315 367 | 1.02 | 3.00 |  |
| [allocation_is_the_c_librarys_counted_only_where_read](allocation_is_the_c_librarys_counted_only_where_read/) |  |  |  |  |  |  | build: does not compile: allocation_is_the_c_librarys_counted_only_where_read/allocation_is_the_c_librarys_counted_only_where_read.spite:45: error: this value may be null (it is a Node?), so 'value' cannot be read from it yet... |
| [particles](particles/) | 222 304 | 56 852 | 33 592 | 17 793 435 | 6.62 | 0.01 | spite: answers height 1065398 spread 7549745 where naive.c answers height 1065390 spread 7549745 |
| [vector_maths](vector_maths/) | 1 627 581 | 69 541 | 50 540 | 37 646 499 | 32.20 | 0.04 | spite: answers checksum 2389814272 ended at 2218210 where naive.c answers checksum 2414989568 ended at 2302946 |

Last measured 2026-10-22: best of 5 interleaved runs (a form stops repeating once its runs pass 30 s), on AMD Ryzen 9 5950X 16-Core Processor, 32 logical processors; C with clang version 19.1.5 -O2, Python 3.12.10, Spite with `D:\Projects\SpiteCompiler\.spite\spite.exe`.
<!-- /results -->
