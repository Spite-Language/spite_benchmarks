"""Builds and times every benchmark case (or the ones named) in its four forms, and writes the table in README.md.

    python run.py [--compiler=path] [--runs=7] [--budget=30] [case ...]

Each case is a folder holding `<case>.spite` (with any other classes beside it), `naive.c`, `expert.c` and
`naive.py`. The Spite program is built with the compiler given (by default the master compiler,
../spite_compiler/.spite/spite.exe beside this repository), both C programs with clang -O2, and the four forms are run interleaved,
each in its case's folder, best of `--runs` runs. A form whose runs have taken more than `--budget` seconds in all
stops after the run that crossed it, so a slow form is timed fewer times instead of for an hour. Every program times
its own work and prints "microseconds <n>" on its error output; its standard output is its answer, and every form
must print exactly what naive.c prints. The rows of the cases timed are written into the table of README.md, the
other rows are kept, and the table is ordered by Spite's time over expert C's, worst first.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date

here = os.path.dirname(os.path.abspath(__file__))
readme = os.path.join(here, 'README.md')
results_file = os.path.join(here, 'results.json')
run_timeout = 300
master_compiler = os.path.normpath(os.path.join(here, '..', 'spite_compiler', '.spite', 'spite.exe'))


def find_c_compiler():
    """clang from $CC, the PATH, Visual Studio's LLVM, or zig's (`zig cc`), as a command list"""
    if os.environ.get('CC'):
        return os.environ['CC'].split()
    found = shutil.which('clang')
    if found:
        return [found]
    for candidate in glob.glob('C:/Program Files/Microsoft Visual Studio/*/*/VC/Tools/Llvm/x64/bin/clang.exe'):
        return [candidate]
    found = shutil.which('zig')
    if found:
        return [found, 'cc']
    sys.exit('error: no C compiler found: set CC, or install clang or zig')


def answer_of(text):
    return text.replace('\r', '')


def microseconds_in(text):
    found = re.search(r'^microseconds (\d+)\s*$', text.replace('\r', ''), re.M)
    if not found:
        return None
    return int(found.group(1))


def one_line(text, limit=200):
    text = ' '.join(text.replace('\r', '').split())
    return text if len(text) <= limit else text[:limit] + '...'


def build(case, compiler, c_compiler):
    """the four forms' command lines, or the reason one could not be built"""
    folder = os.path.join(here, case)
    build_folder = os.path.join(folder, '.spite', 'build')
    spite_executable = os.path.join(build_folder, case + '.exe')
    if os.path.exists(spite_executable):
        os.remove(spite_executable)
    built = subprocess.run([compiler, case], cwd=here, capture_output=True, text=True, errors='replace')
    if built.returncode != 0 or not os.path.exists(spite_executable):
        return None, 'does not compile: ' + one_line(built.stdout + built.stderr)
    forms = {'spite': [spite_executable]}
    for name in ('naive', 'expert'):
        executable = os.path.join(build_folder, name + '_c.exe')
        made = subprocess.run(c_compiler + ['-O2', '-w', name + '.c', '-o', executable], cwd=folder,
                              capture_output=True, text=True, errors='replace')
        if made.returncode != 0:
            return None, f'{name}.c does not build: ' + one_line(made.stderr)
        forms[name] = [executable]
    forms['python'] = [sys.executable, 'naive.py']
    return forms, None


def run_once(command, folder):
    try:
        ran = subprocess.run(command, cwd=folder, capture_output=True, text=True, errors='replace',
                             timeout=run_timeout)
    except subprocess.TimeoutExpired:
        return None, None, f'ran longer than {run_timeout} s'
    if ran.returncode != 0:
        return None, None, f'exit code {ran.returncode}: ' + one_line(ran.stdout + ran.stderr)
    took = microseconds_in(ran.stderr)
    if took is None:
        return None, None, 'printed no "microseconds <n>" line'
    return answer_of(ran.stdout), took, None


def time_case(case, forms, runs, budget):
    folder = os.path.join(here, case)
    os.makedirs(os.path.join(folder, '.spite'), exist_ok=True)   # where the file cases write
    best = {}
    spent = {name: 0 for name in forms}
    answers = {}
    problems = {}
    for attempt in range(runs):
        for name, command in forms.items():
            if name in problems or spent[name] > budget * 1000000:
                continue
            answer, took, problem = run_once(command, folder)
            if problem:
                problems[name] = problem
                continue
            answers.setdefault(name, answer)
            if answers[name] != answer:
                problems[name] = 'answers differently from one run to the next'
                continue
            spent[name] += took
            best[name] = min(best.get(name, took), took)
    reference = answers.get('naive')
    for name in forms:
        if name not in problems and name != 'naive' and reference is not None and answers.get(name) != reference:
            problems[name] = ('answers ' + one_line(answers.get(name) or '', 120) + ' where naive.c answers ' +
                              one_line(reference, 120))
    return best, problems


def spaced(number):
    return f'{number:,}'.replace(',', ' ')


def ratio(top, bottom):
    if top is None or bottom is None:
        return None
    return top / max(bottom, 1)


def row_of(case, result):
    best = result.get('best', {})
    cells = []
    for name in ('spite', 'naive', 'expert', 'python'):
        cells.append(spaced(best[name]) if name in best else '')
    expert_ratio = ratio(best.get('spite'), best.get('expert'))
    python_ratio = ratio(best.get('spite'), best.get('python'))
    cells.append(f'{expert_ratio:.2f}' if expert_ratio is not None else '')
    cells.append(f'{python_ratio:.2f}' if python_ratio is not None else '')
    notes = '; '.join(f'{name}: {problem}' for name, problem in result.get('problems', {}).items())
    if result.get('compiler') and result['compiler'] != master_compiler:
        notes = (notes + '; ' if notes else '') + f'timed with {result["compiler"]}'
    notes = notes.replace('|', '/')
    return f'| [{case}]({case}/) | ' + ' | '.join(cells) + f' | {notes} |'


def sort_key(item):
    case, result = item
    best = result.get('best', {})
    expert_ratio = ratio(best.get('spite'), best.get('expert'))
    if expert_ratio is None or result.get('problems'):
        return (1, case)
    return (0, -expert_ratio)


def write_table(results, note):
    lines = ['| case | Spite µs | naive C µs | expert C µs | Python µs | Spite / expert C | Spite / Python | problem |',
             '|---|---|---|---|---|---|---|---|']
    for case, result in sorted(results.items(), key=sort_key):
        lines.append(row_of(case, result))
    lines.append('')
    lines.append(note)
    text = open(readme, encoding='utf-8').read()
    start = text.index('<!-- results -->\n') + len('<!-- results -->\n')
    finish = text.index('<!-- /results -->')
    text = text[:start] + '\n'.join(lines) + '\n' + text[finish:]
    open(readme, 'w', encoding='utf-8', newline='\n').write(text)


def machine_note(c_compiler, compiler, runs, budget):
    processor = os.environ.get('PROCESSOR_IDENTIFIER', 'unknown processor')
    try:
        named = subprocess.run(['powershell', '-NoProfile', '-Command',
                                '(Get-CimInstance Win32_Processor).Name'], capture_output=True, text=True)
        if named.returncode == 0 and named.stdout.strip():
            processor = named.stdout.strip()
    except OSError:
        pass
    version = subprocess.run(c_compiler + ['--version'], capture_output=True, text=True).stdout.splitlines()
    c_name = re.sub(r' \(.*', '', version[0]) if version else 'unknown C compiler'
    python_name = 'Python ' + sys.version.split()[0]
    return (f'Last measured {date.today()}: best of {runs} interleaved runs (a form stops repeating once its runs '
            f'pass {budget} s), on {processor}, {os.cpu_count()} logical processors; C with {c_name} -O2, '
            f'{python_name}, Spite with `{compiler}`.')


def main():
    compiler = master_compiler
    runs = 7
    budget = 30
    cases = []
    for argument in sys.argv[1:]:
        if argument.startswith('--compiler='):
            compiler = argument.split('=', 1)[1]
        elif argument.startswith('--runs='):
            runs = int(argument.split('=', 1)[1])
        elif argument.startswith('--budget='):
            budget = int(argument.split('=', 1)[1])
        elif argument.startswith('--'):
            sys.exit(f'error: unknown flag {argument}')
        else:
            cases.append(os.path.basename(argument.rstrip('/\\')))
    every_case = sorted(name for name in os.listdir(here) if os.path.isfile(os.path.join(here, name, name + '.spite')))
    for case in cases:
        if case not in every_case:
            sys.exit(f'error: there is no case named {case}')
    if not cases:
        cases = every_case
    compiler = os.path.abspath(compiler)
    c_compiler = find_c_compiler()
    results = json.load(open(results_file, encoding='utf-8')) if os.path.exists(results_file) else {}
    results = {case: result for case, result in results.items() if case in every_case}
    for case in cases:
        forms, problem = build(case, compiler, c_compiler)
        if problem:
            results[case] = {'best': {}, 'problems': {'build': problem}}
        else:
            best, problems = time_case(case, forms, runs, budget)
            results[case] = {'best': best, 'problems': problems}
        results[case]['compiler'] = compiler
        print(row_of(case, results[case]), flush=True)
        json.dump(results, open(results_file, 'w', encoding='utf-8'), indent=1, sort_keys=True)
    write_table(results, machine_note(c_compiler, compiler, runs, budget))


if __name__ == '__main__':
    main()
