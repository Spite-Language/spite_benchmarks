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
`clock.elapsed()`, a `Duration`, whose difference they print with `total('microseconds')`.

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
default `../spite_compiler/.spite/spite.exe`, the compiler `bash scripts/bootstrap.sh --install` leaves in the
repository beside this one) and both C programs with clang `-O2` (from `CC`, the `PATH`,
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
| [a_list_of_lists_filled_again_keeps_each_lists_room](a_list_of_lists_filled_again_keeps_each_lists_room/) | 290 956 | 333 376 | 6 465 | 1 312 615 | 45.00 | 0.22 |  |
| [text_building](text_building/) | 222 739 | 87 008 | 9 761 | 618 027 | 22.82 | 0.36 |  |
| [a_walked_crash_lines_read_is_the_rows_read](a_walked_crash_lines_read_is_the_rows_read/) | 91 587 | 18 505 | 4 746 | 6 324 502 | 19.30 | 0.01 |  |
| [a_word_inflected_while_compiling](a_word_inflected_while_compiling/) | 63 854 | 270 382 | 3 374 | 903 936 | 18.93 | 0.07 |  |
| [report_over_records](report_over_records/) | 436 299 | 675 926 | 23 082 | 6 531 015 | 18.90 | 0.07 |  |
| [a_list_held_only_by_another_list_lives_in_its_slot](a_list_held_only_by_another_list_lives_in_its_slot/) | 640 044 | 274 768 | 36 964 | 9 020 416 | 17.32 | 0.07 |  |
| [a_write_back_of_what_the_slot_already_holds_is_not_written](a_write_back_of_what_the_slot_already_holds_is_not_written/) | 9 613 | 5 180 | 578 | 1 995 507 | 16.63 | 0.00 |  |
| [an_items_storage_is_chosen_while_compiling](an_items_storage_is_chosen_while_compiling/) | 37 010 | 31 964 | 2 435 | 1 743 417 | 15.20 | 0.02 |  |
| [objects_of_one_class_sit_together](objects_of_one_class_sit_together/) | 36 580 | 25 916 | 2 509 | 635 257 | 14.58 | 0.06 |  |
| [a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one](a_deep_copy_is_written_per_class_with_a_table_only_where_a_graph_needs_one/) | 15 008 | 79 850 | 1 055 | 391 110 | 14.23 | 0.04 |  |
| [arithmetic_is_checked_in_every_build](arithmetic_is_checked_in_every_build/) | 38 334 | 3 081 | 2 697 | 1 731 491 | 14.21 | 0.02 |  |
| [a_singletons_attribute_that_never_changes_is_read_in_place](a_singletons_attribute_that_never_changes_is_read_in_place/) | 48 402 | 175 716 | 3 505 | 2 094 748 | 13.81 | 0.02 |  |
| [a_row_of_borrowed_items_lives_in_the_frame](a_row_of_borrowed_items_lives_in_the_frame/) | 40 909 | 7 041 | 3 051 | 5 177 879 | 13.41 | 0.01 |  |
| [text_joined_in_one_piece](text_joined_in_one_piece/) | 43 956 | 97 110 | 3 426 | 137 435 | 12.83 | 0.32 |  |
| [defaults_the_constructor_replaces_are_never_made](defaults_the_constructor_replaces_are_never_made/) | 4 470 | 45 229 | 351 | 330 101 | 12.74 | 0.01 |  |
| [template_chains_run_as_one_loop](template_chains_run_as_one_loop/) | 18 714 | 83 742 | 1 549 | 1 962 516 | 12.08 | 0.01 |  |
| [an_argument_its_caller_holds_is_passed_without_counting](an_argument_its_caller_holds_is_passed_without_counting/) | 8 141 | 34 885 | 674 | 1 427 255 | 12.08 | 0.01 |  |
| [the_compiler_places_memory](the_compiler_places_memory/) | 106 538 | 33 185 | 8 833 | 2 333 230 | 12.06 | 0.05 |  |
| [a_lists_templates_read_its_elements_without_counting_them](a_lists_templates_read_its_elements_without_counting_them/) | 26 040 | 30 437 | 2 172 | 1 599 078 | 11.99 | 0.02 |  |
| [records_sorted_by_one_field](records_sorted_by_one_field/) | 1 147 969 | 696 770 | 97 602 | 5 163 201 | 11.76 | 0.22 |  |
| [an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted](an_item_passed_to_a_call_that_cannot_change_its_list_is_not_counted/) | 24 773 | 16 404 | 2 175 | 2 190 974 | 11.39 | 0.01 |  |
| [image_filter_over_planes](image_filter_over_planes/) | 239 775 | 263 308 | 22 799 | 7 973 798 | 10.52 | 0.03 |  |
| [sorting](sorting/) | 200 056 | 124 570 | 19 026 | 1 143 056 | 10.51 | 0.18 |  |
| [a_numbers_bits_are_read_in_place](a_numbers_bits_are_read_in_place/) | 245 022 | 90 769 | 23 664 | 29 033 358 | 10.35 | 0.01 |  |
| [reading_an_address_is_one_machine_operation](reading_an_address_is_one_machine_operation/) | 42 198 | 5 670 | 4 076 | 2 491 579 | 10.35 | 0.02 |  |
| [atomic_reference_counts_only_with_threads](atomic_reference_counts_only_with_threads/) | 22 958 | 23 895 | 2 298 | 287 401 | 9.99 | 0.08 |  |
| [a_proven_read_tests_only_its_bounds](a_proven_read_tests_only_its_bounds/) | 66 944 | 6 828 | 6 723 | 7 527 644 | 9.96 | 0.01 |  |
| [a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame](a_variadic_list_the_callee_only_reads_lives_in_the_callers_frame/) | 37 164 | 4 030 | 4 102 | 436 412 | 9.06 | 0.09 |  |
| [a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once](a_counted_loop_of_calls_to_one_singleton_takes_its_lock_once/) | 26 466 | 311 837 | 2 978 | 4 993 561 | 8.89 | 0.01 |  |
| [an_item_a_name_holds_from_its_list_is_not_counted](an_item_a_name_holds_from_its_list_is_not_counted/) | 15 856 | 15 245 | 1 907 | 1 338 633 | 8.31 | 0.01 |  |
| [while_no_task_runs_a_singletons_lock_is_skipped](while_no_task_runs_a_singletons_lock_is_skipped/) | 42 445 | 111 974 | 5 301 | 4 445 006 | 8.01 | 0.01 |  |
| [reflection_on_constants_folds_and_unrolls](reflection_on_constants_folds_and_unrolls/) | 20 616 | 12 920 | 2 612 | 8 315 463 | 7.89 | 0.00 |  |
| [reading_through_a_type_without_counting](reading_through_a_type_without_counting/) | 43 395 | 9 935 | 5 521 | 5 522 007 | 7.86 | 0.01 |  |
| [concurrency_machinery_only_where_it_is_used](concurrency_machinery_only_where_it_is_used/) | 12 181 | 11 638 | 1 573 | 14 666 | 7.74 | 0.83 |  |
| [an_item_written_back_to_its_own_slot_is_not_written](an_item_written_back_to_its_own_slot_is_not_written/) | 28 631 | 44 571 | 3 788 | 2 234 239 | 7.56 | 0.01 |  |
| [particles](particles/) | 77 046 | 29 104 | 10 515 | 26 977 926 | 7.33 | 0.00 |  |
| [maths_on_constants_is_worked_out_while_compiling](maths_on_constants_is_worked_out_while_compiling/) | 21 022 | 13 506 | 2 880 | 27 332 773 | 7.30 | 0.00 |  |
| [singletons_a_parallel_reaches_take_a_lock](singletons_a_parallel_reaches_take_a_lock/) | 4 533 | 27 732 | 628 | 261 294 | 7.22 | 0.02 |  |
| [removing_many_at_once](removing_many_at_once/) | 145 274 | 24 858 | 21 399 | 5 980 191 | 6.79 | 0.02 |  |
| [a_singleton_no_other_thread_reaches_takes_no_lock](a_singleton_no_other_thread_reaches_takes_no_lock/) | 21 424 | 4 920 | 3 293 | 1 460 049 | 6.51 | 0.01 |  |
| [spreadsheet_recalculation](spreadsheet_recalculation/) | 682 957 | 697 516 | 109 341 | 12 692 061 | 6.25 | 0.05 |  |
| [short_text_lives_inside_the_string](short_text_lives_inside_the_string/) | 107 595 | 259 783 | 17 507 | 538 837 | 6.15 | 0.20 |  |
| [a_number_joined_into_text_is_written_in_place](a_number_joined_into_text_is_written_in_place/) | 97 589 | 324 508 | 15 881 | 411 722 | 6.15 | 0.24 |  |
| [game_maths](game_maths/) | 9 485 | 2 259 | 1 752 | 6 988 735 | 5.41 | 0.00 |  |
| [an_allocator_set_after_construction_is_where_the_object_is_made](an_allocator_set_after_construction_is_where_the_object_is_made/) | 10 684 | 79 035 | 2 044 | 465 687 | 5.23 | 0.02 |  |
| [storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot](storing_an_object_into_a_list_counts_it_only_when_it_changes_the_slot/) | 23 407 | 6 710 | 4 487 | 1 260 062 | 5.22 | 0.02 |  |
| [allocation_is_the_c_librarys_counted_only_where_read](allocation_is_the_c_librarys_counted_only_where_read/) | 14 535 | 60 820 | 2 905 | 383 342 | 5.00 | 0.04 |  |
| [an_attribute_a_call_cannot_assign_is_passed_without_counting](an_attribute_a_call_cannot_assign_is_passed_without_counting/) | 13 233 | 4 405 | 2 647 | 1 486 726 | 5.00 | 0.01 |  |
| [smaller_ones](smaller_ones/) | 44 728 | 10 443 | 9 188 | 3 243 763 | 4.87 | 0.01 |  |
| [a_list_item_read_only_to_test_it_is_not_counted](a_list_item_read_only_to_test_it_is_not_counted/) | 53 578 | 64 513 | 11 673 | 3 034 981 | 4.59 | 0.02 |  |
| [boxing_only_where_a_value_travels_as_a_shape](boxing_only_where_a_value_travels_as_a_shape/) | 53 369 | 99 937 | 12 560 | 164 340 | 4.25 | 0.32 |  |
| [thread_safety_for_singletons_the_cheapest_safe_form](thread_safety_for_singletons_the_cheapest_safe_form/) | 1 889 | 219 417 | 449 | 1 427 111 | 4.21 | 0.00 |  |
| [number_dictionary](number_dictionary/) | 52 333 | 27 859 | 12 884 | 423 133 | 4.06 | 0.12 |  |
| [a_loop_over_a_list_of_different_classes_runs_them_at_once](a_loop_over_a_list_of_different_classes_runs_them_at_once/) | 338 991 | 275 710 | 93 619 | 7 775 268 | 3.62 | 0.04 |  |
| [counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts](counts_stay_plain_for_what_one_of_the_calls_run_at_once_counts/) | 19 263 | 10 623 | 5 416 | 493 942 | 3.56 | 0.04 |  |
| [objects_made_for_their_owner_are_told_apart](objects_made_for_their_owner_are_told_apart/) | 207 942 | 119 505 | 60 440 | 5 592 187 | 3.44 | 0.04 |  |
| [appending_to_text_in_place](appending_to_text_in_place/) | 728 | 93 980 | 215 | 5 780 | 3.39 | 0.13 |  |
| [calls_in_a_row_run_at_once](calls_in_a_row_run_at_once/) | 79 875 | 43 839 | 23 630 | 4 242 186 | 3.38 | 0.02 |  |
| [a_number_read_from_bytes_is_one_load](a_number_read_from_bytes_is_one_load/) | 100 778 | 53 929 | 32 241 | 26 614 134 | 3.13 | 0.00 |  |
| [a_dictionary_written_out_and_only_read_by_literal_keys_is_folded](a_dictionary_written_out_and_only_read_by_literal_keys_is_folded/) | 17 101 | 384 367 | 5 705 | 1 386 968 | 3.00 | 0.01 |  |
| [a_binary_schema_is_a_constant](a_binary_schema_is_a_constant/) | 1 792 | 351 997 | 599 | 10 268 363 | 2.99 | 0.00 |  |
| [copies_that_cost_nothing](copies_that_cost_nothing/) | 48 916 | 23 095 | 16 636 | 6 156 622 | 2.94 | 0.01 |  |
| [a_local_list_of_known_size_lives_in_the_frame](a_local_list_of_known_size_lives_in_the_frame/) | 64 671 | 23 777 | 23 286 | 3 998 632 | 2.78 | 0.02 |  |
| [a_dictionary_hashes_a_key_once_cheaply](a_dictionary_hashes_a_key_once_cheaply/) | 73 761 | 85 655 | 26 690 | 248 340 | 2.76 | 0.30 |  |
| [a_crashs_report_is_kept_out_of_the_way](a_crashs_report_is_kept_out_of_the_way/) | 27 481 | 13 498 | 10 034 | 2 632 904 | 2.74 | 0.01 |  |
| [thread_safety_for_singletons_the_rest_of_the_plan](thread_safety_for_singletons_the_rest_of_the_plan/) | 5 107 | 26 281 | 1 879 | 254 141 | 2.72 | 0.02 |  |
| [a_dictionary_keyed_by_numbers_hashes_the_numbers](a_dictionary_keyed_by_numbers_hashes_the_numbers/) | 30 428 | 15 683 | 13 083 | 478 857 | 2.33 | 0.06 |  |
| [a_proven_divisor_is_not_checked](a_proven_divisor_is_not_checked/) | 56 938 | 29 892 | 26 767 | 1 164 400 | 2.13 | 0.05 |  |
| [singletons_made_on_first_use_never_counted](singletons_made_on_first_use_never_counted/) | 11 226 | 220 332 | 5 746 | 7 125 345 | 1.95 | 0.00 |  |
| [plain_reference_counts_where_no_thread_reaches_a_class](plain_reference_counts_where_no_thread_reaches_a_class/) | 20 869 | 27 542 | 11 109 | 1 045 098 | 1.88 | 0.02 |  |
| [a_function_value_describes_its_arguments_when_asked](a_function_value_describes_its_arguments_when_asked/) | 2 200 | 1 251 | 1 239 | 822 492 | 1.78 | 0.00 |  |
| [tokens_as_columns](tokens_as_columns/) | 135 784 | 134 463 | 76 565 | 2 549 438 | 1.77 | 0.05 |  |
| [deciding_conditions_at_compile_time](deciding_conditions_at_compile_time/) | 12 714 | 8 799 | 7 745 | 2 771 341 | 1.64 | 0.00 |  |
| [a_function_taking_a_type_is_compiled_per_class](a_function_taking_a_type_is_compiled_per_class/) | 74 809 | 52 433 | 52 295 | 15 767 051 | 1.43 | 0.00 |  |
| [a_table_filled_once_is_read_as_constants](a_table_filled_once_is_read_as_constants/) | 28 863 | 21 489 | 20 574 | 3 453 019 | 1.40 | 0.01 |  |
| [a_test_against_a_value_a_list_never_holds_is_decided_while_compiling](a_test_against_a_value_a_list_never_holds_is_decided_while_compiling/) | 28 497 | 39 822 | 20 444 | 3 476 405 | 1.39 | 0.01 |  |
| [reads_in_a_row_overlap](reads_in_a_row_overlap/) | 7 178 | 7 284 | 5 710 | 8 945 | 1.26 | 0.80 |  |
| [a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked](a_loop_over_plain_values_reads_its_count_once_and_its_items_unchecked/) | 20 098 | 147 217 | 16 354 | 13 839 666 | 1.23 | 0.00 |  |
| [vector_maths](vector_maths/) | 59 749 | 63 864 | 49 365 | 28 089 717 | 1.21 | 0.00 |  |
| [the_thread_pool_only_where_a_parallel_is_made](the_thread_pool_only_where_a_parallel_is_made/) | 9 001 | 7 395 | 7 438 | 715 612 | 1.21 | 0.01 |  |
| [objects_that_never_leave_their_function_live_in_the_frame](objects_that_never_leave_their_function_live_in_the_frame/) | 17 216 | 1 023 689 | 14 793 | 44 316 628 | 1.16 | 0.00 |  |
| [a_singletons_reading_functions_do_not_exclude_each_other](a_singletons_reading_functions_do_not_exclude_each_other/) | 6 838 | 118 750 | 6 151 | 595 265 | 1.11 | 0.01 |  |
| [a_loop_whose_passes_write_only_their_own_item_runs_in_bands](a_loop_whose_passes_write_only_their_own_item_runs_in_bands/) | 57 820 | 788 392 | 54 676 | 257 928 036 | 1.06 | 0.00 |  |
| [a_decimal_literal_beside_a_float_is_a_float](a_decimal_literal_beside_a_float_is_a_float/) | 16 456 | 522 910 | 16 557 | 55 334 741 | 0.99 | 0.00 |  |
| [a_wait_in_a_frame_does_not_hold_the_frame](a_wait_in_a_frame_does_not_hold_the_frame/) | 87 358 | 1 168 666 | 930 663 | 320 556 | 0.09 | 0.27 |  |

Last measured 2026-10-26: best of 7 interleaved runs (a form stops repeating once its runs pass 30 s), on AMD Ryzen 9 5950X 16-Core Processor, 32 logical processors; C with clang version 19.1.5 -O2, Python 3.12.10, Spite with `D:\Projects\SpiteOrganization\work\regression\spite_compiler\.spite\spite.exe`.
<!-- /results -->
