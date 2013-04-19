import os
import sys
from mercurial import hg, ui
from filters import after_date, is_tdded, on_default
from parse_arguments import parse_arguments

def len_generator(generator):
    return sum(1 for _ in generator)

def repository_exists(directory):
    try:
        hg.repository(ui.ui(), directory)
        return True
    except:
        return False

def get_changesets(repo):
    return (repo[revNum] for revNum in range(0, len(repo)))

def filter_changesets(changesets, filters):
    if len(filters) == 0:
        return changesets
    return filter_changesets(filter(filters[0], changesets), filters[1:])

def get_commit_percent(repo, numerator_filters, denominator_filters):
    numerator_count = len_generator(filter_changesets(get_changesets(repo), numerator_filters))
    denominator_count = max(1, len_generator(filter_changesets(get_changesets(repo), denominator_filters)))

    return float(numerator_count) / denominator_count * 100

def print_metrics(repo):
    if len(repo) == 0:
        print('The repository is empty')
        return

    additional_filters = parse_arguments(sys.argv)

    numerator_filters = additional_filters + [on_default, is_tdded]
    denominator_filters = additional_filters + [on_default]

    if len_generator(filter_changesets(get_changesets(repo), denominator_filters)) == 0:
        print('There are no changesets meeting the criteria')
        return
        
    percentage = get_commit_percent(repo, numerator_filters, denominator_filters)

    print('%d percent of commits have tests' % percentage)

def generate_and_display_metrics():
    if not repository_exists(os.getcwd()):
        print('There is no repository at %s' % os.getcwd())
        return
    repo = hg.repository(ui.ui(), os.getcwd())
    
    print_metrics(repo)
    
if __name__ == '__main__':
    generate_and_display_metrics() 