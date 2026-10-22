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
| [sorting](sorting/) | 1 333 080 | 126 852 | 23 216 | 1 171 435 | 57.42 | 1.14 |  |
| [reads_in_a_row_overlap](reads_in_a_row_overlap/) | 266 181 | 13 315 | 7 617 | 11 404 | 34.95 | 23.34 |  |
| [concurrency_machinery_only_where_it_is_used](concurrency_machinery_only_where_it_is_used/) | 13 570 | 13 538 | 1 603 | 18 679 | 8.47 | 0.73 |  |
| [a_wait_in_a_frame_does_not_hold_the_frame](a_wait_in_a_frame_does_not_hold_the_frame/) | 939 834 | 1 188 658 | 922 146 | 321 033 | 1.02 | 2.93 |  |
| [allocation_is_the_c_librarys_counted_only_where_read](allocation_is_the_c_librarys_counted_only_where_read/) |  |  |  |  |  |  | build: does not compile: allocation_is_the_c_librarys_counted_only_where_read/allocation_is_the_c_librarys_counted_only_where_read.spite:46: error: this value may be null (it is a Node?), so 'value' cannot be read from it yet... |
| [particles](particles/) | 1 296 179 | 54 347 | 33 058 | 17 434 586 | 39.21 | 0.07 | spite: answers height 1065398 spread 7549745 where naive.c answers height 1065390 spread 7549745 |
| [vector_maths](vector_maths/) | 3 186 179 | 68 246 | 51 203 | 29 972 514 | 62.23 | 0.11 | spite: answers checksum 2389814272 ended at 2218210 where naive.c answers checksum 2414989568 ended at 2302946 |

Last measured 2026-10-22: best of 1 interleaved runs (a form stops repeating once its runs pass 60 s), on AMD Ryzen 9 5950X 16-Core Processor, 32 logical processors; C with clang version 19.1.5 -O2, Python 3.12.10, Spite with `D:\Projects\SpiteCompiler\.spite\spite.exe`.
<!-- /results -->
