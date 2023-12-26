#
# This file is part of PLCreX (https://github.com/marwern/PLCreX).
#
# Copyright (c) 2022-2023 Marcel C. Werner.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import colorama
from typing import Optional
from plcrex.tools.st2ia import _st2ia
from plcrex.tools.fbd2st import _fbd2st
from plcrex.tools.ds2ts import _ds2ts
from plcrex.tools.st2ast import _st2ast
from plcrex.tools.st2x import _st2x
from plcrex.tools.xmlval import _xml_val
from plcrex.tools.iecchecker import _iec_checker
from plcrex.add import *
from pathlib import Path
from plcrex import __app_name__, __version__
from rich.console import Console

console = Console()
app = typer.Typer(context_settings={"help_option_names": ["--help"]}, add_completion=True, rich_markup_mode="rich")
colorama.init()


@app.command("iec-checker")
def iec_checker(
        source: Path = typer.Argument(help="source path"),
        exe: Path = typer.Argument(help="iec_checker_Windows_x86_64_v0.4.exe path"),
        export: Path = typer.Argument(help="export path"),
        filename: str = typer.Argument(help="filename without file extension"),
        verbose: bool = typer.Option(False, help="print full log"),
        help_: bool = typer.Option(False, "--help_iec_checker", help="call iec-checker help")
):
    """IEC-Checker\t\t*.st → iecchecker → *.log"""
    _iec_checker.cli(source, exe, verbose, export, filename, help_)
    typer.echo("\n" + typer.style("Success!", fg=typer.colors.GREEN, bold=True))
    raise typer.Exit()


@app.command("test-case-gen")  # epilog=fr"[yellow]PLCreX-{__version__}, plcrex.info@gmail.com[/yellow]"
def ds2ts(formula: str = typer.Argument(help="condition \"(,),&,|,^,~,<=>\""),
          sc: bool = typer.Option(False, help="print statement coverage test case"),
          dc: bool = typer.Option(False, help="print decision coverage test cases"),
          mcdc: bool = typer.Option(False, help="print modified condition/decision coverage test cases"),
          mcc: bool = typer.Option(False, help="print multiple condition coverage test cases")
          ):
    """Test-Case-Generator\tFORMULA:str → ds2ts → stdout"""
    _ds2ts.cli(formula, sc, dc, mcdc, mcc)
    typer.echo("\n" + typer.style("Success!", fg=typer.colors.GREEN, bold=True))
    raise typer.Exit()


@app.command("fbd-to-st")
def fbd2st(
        source: Path = typer.Argument(help="source path"),
        export: Path = typer.Argument(help="export path"),
        filename: str = typer.Argument(help="filename without file extension"),
        bwd: bool = typer.Option(False, help="use backward translation"),
        formal: bool = typer.Option(False, help="formal parameter list")
        ):
    """FBD-to-ST Compiler\t*.xml → fbd2st → *.st"""
    _fbd2st.cli(source, export, filename, bwd, formal)
    typer.echo("\n" + typer.style("Success!", fg=typer.colors.GREEN, bold=True))
    raise typer.Exit()


@app.command("impact-analysis")
def impact_anal(
        source: Path = typer.Argument(help="source path"),
        export: Path = typer.Argument(help="export path"),
        filename: str = typer.Argument(help="filename without file extension")
        ):
    """I/O-Impact Analysis\t*.xml → fbd2st → *.st → st2ia → *.dot"""
    _st2ia.cli(source, export, filename)
    typer.echo("\n" + typer.style("Success!", fg=typer.colors.GREEN, bold=True))
    raise typer.Exit()


@app.command("st-parser")
def st2ast(
        source: Path = typer.Argument(help="source path"),
        export: Path = typer.Argument(help="export path"),
        filename: str = typer.Argument(help="filename without file extension"),
        txt: bool = typer.Option(True, help="tree export as *.txt"),
        dot: bool = typer.Option(True, help="tree export as *.dot"),
        beckhoff: bool = typer.Option(False, help="use Beckhoff TwinCAT ST grammar")
        ):
    """ST-Parser\t\t*.st → st2ast → *.dot/*.txt"""
    _st2ast.cli(source, export, filename, txt, dot, beckhoff)
    typer.echo("\n" + typer.style("Success!", fg=typer.colors.GREEN, bold=True))
    raise typer.Exit()


@app.command("fbd-optimizer")
def fbd_opt(
        source: Path = typer.Argument(help="source path"),
        exe: Path = typer.Argument(help="NuSMV.exe path"),
        export: Path = typer.Argument(help="export path"),
        filename: str = typer.Argument(help="filename without file extension"),
        edge_opt: bool = typer.Option(False, help="optimize edges"),
        var_opt: bool = typer.Option(False, help="optimize variables"),
        op_opt: bool = typer.Option(False, help="optimize operators")
        ):
    """FBD-Optimizer\t\t*.xml → fbd2st → *.st → st2x → *.st/*.sctx"""
    _st2x.cli(source, export, filename, exe, edge_opt, var_opt, op_opt)
    typer.echo("\n" + typer.style("Success!", fg=typer.colors.GREEN, bold=True))
    raise typer.Exit()


@app.command("xml-validator")
def xml_val(
        source: Path = typer.Argument(help="source path"),
        v201: bool = typer.Option(False, help="use tc6_xml_v201.xsd")
        ):
    """XML-Validator\t\t*.xml → xmlval → stdout"""
    _xml_val.cli(source, v201)
    typer.echo("\n" + typer.style("Success!", fg=typer.colors.GREEN, bold=True))
    raise typer.Exit()


def version_callback(value: bool):
    # print_plcrex_header()
    if value:
        typer.echo(fr"""
PLCreX-{__version__}, plcrex.info@gmail.com

Copyright (c) 2022-2023 Marcel C. Werner.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
        """)
        raise typer.Exit()


@app.callback()  # epilog=fr"[yellow]PLCreX-{__version__}, plcrex.info@gmail.com[/yellow]"
def main(
        version: Optional[bool] = typer.Option(None, "--version", callback=version_callback, is_eager=True)
    ):
    return
