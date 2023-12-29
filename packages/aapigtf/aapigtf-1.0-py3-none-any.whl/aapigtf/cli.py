import os
import click
from pathlib import Path
from apixunit.fgen import *

mypath = Path.cwd()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project', metavar='<project>')
@click.argument('apl', type=click.Choice(['api', 'apix']), metavar='<apl>')
def main(project, apl):
    """
    CLI.
    """
    print(project, apl)
    if project:
        ppath = mypath / project
        create_scaffold(project_name=ppath, apl_name=apl)
        return 0


def create_scaffold(project_name, apl_name):
    """
    create scaffold with specified project name.
    """

    def create_folder(path):
        os.makedirs(path, exist_ok=True)
        msg = "created folder: {}".format(path)
        # log.info(msg)

    def create_file(path, file_content=""):
        if not os.path.exists(path):
            if file_content is not None:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                msg = "created file: {}".format(path)
                rtx = 'Y'
            else:
                msg = "create excel file: {}".format(path)
                rtx = 'YY'
        else:
            msg = "File already exists. Not creating a new one."
            rtx = 'N'
        # print(msg)
        return rtx
        # log.info(msg)

    create_folder(project_name)
    create_folder(os.path.join(project_name, "utils"))
    create_folder(os.path.join(project_name, "test_dir"))
    create_folder(os.path.join(project_name, "reports"))
    create_folder(os.path.join(project_name, "test_data"))
    create_folder(os.path.join(project_name, "test_data", "json_data"))
    create_folder(os.path.join(project_name, "test_data", "json_data", "mixdata"))
    create_folder(os.path.join(project_name, "test_data", "json_data", "reqdata"))
    create_folder(os.path.join(project_name, "test_data", "json_data", "resdata"))
    file_path_test = mypath / project_name / "test_data" / "api_test_case_and_data.xlsx"
    getf = create_file(file_path_test, None)
    if getf == 'YY':
        create_excel_sheet_for_testcase(file_path_test)
    create_file(os.path.join(project_name, "requirement.txt"), test_requires)
    create_file(os.path.join(project_name, "requirement.txt"), test_requires)
    create_file(os.path.join(project_name, "README.md"), readme_requires)
    create_file(os.path.join(project_name, "config.ini"), conf_requires)
    create_file(os.path.join(project_name, "utils", "endpointapi.ini"), apiconf_requires)
    create_file(os.path.join(project_name, "test_dir", "test_api1.py"), samp_test)
    create_file(os.path.join(project_name, "run.py"), run_test)


if __name__ == '__main__':
    cli()