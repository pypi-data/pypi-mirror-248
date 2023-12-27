from crlfi.utils import helper
from crlfi.includes import filereader
from crlfi.utils import configure
from crlfi.includes import crlfi
import click


def display_help(ctx, param, value):
    if value:
        helper.display_help()
        ctx.exit()
   

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-u', '--url', type=str, help='URL to scan')
@click.option('-i', '--input', type=str, help='list of input txt file')
@click.option('-o', '--output', type=str, help='output in txt file')
@click.option('-c', '--chatid', type=str, help='Creating Telegram Notification')
@click.option('--help', '-h', 'display_help', is_flag=True, expose_value=False, is_eager=True, callback=display_help, help='Show custom help message')

def main(url, input, output,chatid, **kwargs):
    if url:
        helper.banner()
        crlfi.scan(url, output)
    if input:
        helper.banner()
        filereader.reader(input,output)
    if chatid:
        helper.banner()
        configure.new_chatid(chatid)

if __name__ == "__main__":
    main()
