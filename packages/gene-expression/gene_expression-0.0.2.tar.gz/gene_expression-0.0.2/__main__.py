import sys

if __package__:
    from .gene_expression import main
else:
    from gene_expression import main


main(sys.argv[1:])
