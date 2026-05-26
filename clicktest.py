import sys
import shlex
import click


@click.command()
@click.option('--category', '-c', required=True, help='Category name')
@click.option('--num-symbols', '-n', type=int, required=True, help='Number of stock symbols')
@click.option('--num-days', '-d', type=int, required=True, help='Number of days')
@click.option('--symbol', '-s', multiple=True, required=True, help='Stock symbol (use multiple times)')
def compare(category, num_symbols, num_days, symbol):
    if len(symbol) != num_symbols:
        raise click.BadParameter(f'Expected {num_symbols} stock symbols, got {len(symbol)}.')
    click.echo(f'Category: {category}')
    click.echo(f'Number of symbols: {num_symbols}')
    click.echo(f'Number of days: {num_days}')
    click.echo(f'Stock symbols: {" ".join(symbol)}')


if __name__ == '__main__':
    # If no CLI args provided, prompt the user to enter them as a single line
    if len(sys.argv) <= 1:
        try:
            line = input('Enter arguments: ')
        except EOFError:
            sys.exit(0)
        tokens = shlex.split(line)
        if len(tokens) >= 4 and not tokens[0].startswith('-'):
            args = [
                '--category', tokens[0],
                '--num-symbols', tokens[1],
                '--num-days', tokens[2],
            ]
            for symbol in tokens[3:]:
                args.extend(['--symbol', symbol])
        else:
            args = tokens
        compare.main(args=args)
    else:
        compare()