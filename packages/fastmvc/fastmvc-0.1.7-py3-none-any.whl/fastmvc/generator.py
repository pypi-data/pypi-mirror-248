from dataclasses import dataclass
from pathlib import Path
from os import walk, makedirs
from secrets import token_urlsafe
from fastmvc.utilities import (
    config, Platform, get_project_platform, get_smtp_defaults, get_default_service_account_file)
from jinja2 import Environment


"""
HELPERS
"""


def __builder(
    project_path: str,
    generator_path:str,
    format_attrs: dict,
    scaffold_obj_name='',
    ignore_list: list or None = None
) -> None:
    """Build a project scaffold from a generator template.

    Args:
        project_path (str): The path to the directory where the project scaffold should be created.
        generator_path (str): The path to the directory containing the generator template files.
        format_attrs (dict): A dictionary of attributes to be used in formatting the generator template files.
        scaffold_obj_name (str, optional): The name of the object being scaffolded. Defaults to an empty string.
    """
    project_path = Path(project_path)
    generator_path = Path(__file__).parent.resolve() / generator_path
    for (dirpath, _, filenames) in walk(generator_path):
        np = (Path(scaffold_obj_name) / project_path
              if scaffold_obj_name else project_path)
        new_path = dirpath.replace(str(generator_path), str(np))
        if '__pycache__' in str(dirpath):
            continue
        makedirs(new_path, exist_ok=True)
        for filename in filenames:
            if any([filename in igf for igf in ignore_list or list()]):
                continue
            full_path = Path(dirpath) / filename
            print(f">> {Path(new_path) / filename}")
            with open(full_path, 'r', encoding='utf-8') as c:
                content = c.read()

            with open(Path(new_path) / filename, 'w+', encoding='utf-8') as o:
                o.write(__format(content, format_attrs))


def __format(doc: str, attr_dict: dict) -> str:
    """Format a document with the specified attribute dictionary.

    Args:
        doc (str): The document to be formatted.
        attr_dict (dict): A dictionary of attributes to be used in the formatting.

    Returns:
        str: The formatted string.
    """
    env = Environment(
        variable_start_string='^{',
        variable_end_string='}^',
        block_start_string='^%',
        block_end_string='%^',
        trim_blocks=True,
        lstrip_blocks=True)
    template = env.from_string(doc)
    return template.render(**attr_dict)


def __get_object_attrs(attributes: list) -> dict:
    """Get a dictionary of object attributes from a list of attribute strings.

    Args:
        attributes (list): A list of strings representing object attributes in the form "name:type".

    Returns:
        dict: A dictionary of object attributes,
            where the keys are the attribute names and the values are the attribute types.
    """
    obj_attrs = dict()
    for a in attributes:
        if not a:
            continue
        s = a.split(':')
        obj_attrs[s[0]] = 'str' if len(s) == 1 else s[1].lower()
    return obj_attrs


def __prepare_model_attrs(obj_attrs: dict) -> str:
    """Provides attributes for the Model

    Args:
        obj_attrs (dict): attributes dictionary

    Returns:
        str: prepared attributes as string
    """
    model_attrs = [
        f"{k}{'_id' if v == 'references' else ''}: {'str' if v in ('text', 'wysiwyg', 'references') else v}"
        for k, v in obj_attrs.items()]
    return '\n    '.join(model_attrs)


def __create_form_attrs(attributes: dict, helpers_path: str) -> str:
    """Create form field HTML for the specified attributes.

    Args:
        attributes (dict): A dictionary of form field attributes,
            where the keys are the field names and the values are the field types.
        helpers_path (str): The path to the directory containing form field helper templates.

    Returns:
        str: The HTML for the form fields.
    """
    helpers_path = Path(__file__).parent.resolve() / helpers_path
    form_fields = list()
    for f, t in attributes.items():
        field_helper = helpers_path / f'{t}.html'
        if not field_helper.exists():
            field_helper = helpers_path / 'str.html'
        with open(field_helper, 'r') as o:
            content = o.read()
        format_attrs = {
            'f': f"{f}{'_id' if t == 'references' else ''}",
            'F': f.title()}
        form_fields.append(__format(content, format_attrs))
    return '\n'.join(form_fields)


def __add_wysiwyg_meta(take_action: bool):
    if take_action:
        with open(Path(__file__).parent.resolve()
                  / 'templates/scaffold_helpers/trix_meta_content.html',
                  'r') as o:
            return o.read()


def __get_import_placement(main_py: list) -> int:
    """Get the index at which to insert an import statement in the main Python script.

    Args:
        main_py (list): A list of lines in the main Python script.

    Returns:
        int: The index at which to insert an import statement.
    """
    imp_placement = 0
    for i, line in enumerate(main_py):
        if '_router' in line and 'import' in line:
            imp_placement = i + 1
    return imp_placement


"""
GENERATORS
"""


def build_base(p: str, project_name: str, platform: Platform) -> None:
    """Builds a base for the new project.

    Currently supports two platforms: Google App Engine and Deta.
    See templates/core/ or templates/mkdocs_core/ to see the files
    which will be generated through the `__builder` method

    Args:
        p (str): the current working directory
        project_name (str): name of the new project
        platform (Platform): platform to build for.
    """
    makedirs(p)
    content_attrs = {
        'Obj': project_name.title(),
        'project_key': config('project_key') or '',
        'platform': platform.name,
        'service_account': get_default_service_account_file() or None }

    ignore_list = list()
    if platform != Platform.GOOGLE_APP_ENGINE:
        ignore_list.append('app.yaml')
        ignore_list.append('service-account-file.json')

    __builder(
        project_path=p,
        generator_path=f'templates/core',
        format_attrs=content_attrs,
        ignore_list=ignore_list)


def __build_platform_specific_info():
    platform = dict()
    plat = get_project_platform()
    if plat == Platform.DETA:
        platform = {
            'data_model_import': 'deta import DetaBase',
            'data_model': 'DetaBase'
        }
    elif plat == Platform.GOOGLE_APP_ENGINE:
        platform = {
            'data_model_import': 'firestore import Firestore',
            'data_model': 'Firestore'
        }
    return platform



def gen_scaffold(p: str, obj: str, attributes: list, options: dict) -> None:
    """Generates Model, View, and Controller for a new Object.

    Args:
        p (str): the current working directory
        obj (str): the name of the new object to be created
        attributes (list): the attributes of the new object
        options (dict): dictionary of any additional options.
    """
    obj_attrs = __get_object_attrs(attributes)
    format_attrs = {
        'proj': Path.cwd().name,
        'obj': obj,
        'Obj': obj.title(),
        'model_attrs': __prepare_model_attrs(obj_attrs),
        'form_attrs': __create_form_attrs(
            attributes=obj_attrs,
            helpers_path='templates/scaffold_helpers'),
        'wysiwyg': __add_wysiwyg_meta('wysiwyg' in obj_attrs.values()),
        'platform': __build_platform_specific_info(),
        'options': options}

    __builder(
        project_path=p,
        generator_path='templates/scaffold',
        format_attrs=format_attrs,
        scaffold_obj_name=obj)
    update(add_to_main(p, obj))

    with open(Path(__file__).parent.resolve()
              / 'templates/scaffold_helpers/scaffold_navlink.html',
              'r') as o:
        scaffold_link = __format(o.read(), format_attrs)

    update(add_to_navlinks(
        p,
        content=scaffold_link))

    for a, v in obj_attrs.items():
        if v == 'references':
            with open(Path(__file__).parent.resolve()
                    / 'templates/scaffold_helpers/reference_model_list.py',
                        'r') as o:
                reference_list = __format(o.read(), {'obj': obj, 'Obj': obj.title(), 'ref': a})
            update(add_obj_list_to_reference(
                p,
                a,
                content=reference_list,
                import_statement=f"from {obj}.model import {obj.title()}\n"))


def gen_authlib(p: str) -> None:
    """Generates a minimal authorization framework.

    Based on AuthLib library, the generate authorization framework
    allows users to login with Google. See AuthLib library for
    other potential Open ID providers.

    Args:
        p (str): the current working directory
    """
    obj = 'user'
    format_attrs = {
        'proj': Path.cwd().name,
        'obj': obj,
        'Obj': obj.title(),
        'platform': __build_platform_specific_info() }

    __builder(
        project_path=p,
        generator_path='templates/users',
        format_attrs=format_attrs,
        scaffold_obj_name=obj)
    update(add_to_main(
        p,
        obj,
        extra_imports=[
            'from starlette.middleware.sessions import SessionMiddleware\n',
            'from os import environ\n'],
        extra_includes=[
            '\napp.add_middleware(SessionMiddleware, secret_key=environ.get("APP_SECRET"))']))
    update(add_to_requirements(
        p,
        reqs=['itsdangerous', 'httpx', 'Authlib', 'pyjwt', 'passlib[bcrypt]']))
    update(add_to_env(
        p,
        APP_SECRET=format_attrs['proj'][0] + token_urlsafe(16),
        GOOGLE_CLIENT_ID="",
        GOOGLE_CLIENT_SECRET=""))

    with open(Path(__file__).parent.resolve() / 'templates/scaffold_helpers/user_login.html', 'r') as o:
        user_links = o.read()

    update(add_to_navlinks(
        p,
        content=user_links))


def gen_simple_auth(p: str) -> None:
    """Generates a minimal authorization framework.

    Creates a simple email-based authorization framework with Users model.
    Sign-in flow is similar to substack.com where there is no password,
    instead using email confirmation and callback.

    Args:
        p (str): the current working directory
    """
    obj = 'user'
    format_attrs = {
        'proj': Path.cwd().name,
        'obj': obj,
        'Obj': obj.title(),
        'platform': __build_platform_specific_info() }

    __builder(
        project_path=p,
        generator_path='templates/simple_auth',
        format_attrs=format_attrs,
        scaffold_obj_name=obj)
    update(add_to_main(
        p,
        obj,
        extra_imports=[
            'from starlette.middleware.sessions import SessionMiddleware\n',
            'from os import environ\n'],
        extra_includes=[
            '\napp.add_middleware(SessionMiddleware, secret_key=environ.get("APP_SECRET"))']))
    update(add_to_requirements(
        p,
        reqs=['itsdangerous', 'httpx', 'pyjwt', 'passlib[bcrypt]']))

    conf = get_smtp_defaults()
    update(add_to_env(
        p,
        APP_SECRET=format_attrs['proj'][0] + token_urlsafe(16),
        SMTP_PORT=int(conf.get('SMTP_PORT', 587)),
        SMTP_SERVER=conf.get('SMTP_SERVER', "smtp.server.com"),
        SMTP_LOGIN=conf.get('SMTP_LOGIN', "mail_server_account"),
        SMTP_PASSWORD=conf.get('SMTP_PASSWORD', "mail_server_password"),
        SMTP_SENDER_NAME=format_attrs['proj'].title(),
        SMTP_SENDER_EMAIL=f"no-reply@{format_attrs['proj']}.com"))

    with open(Path(__file__).parent.resolve() / 'templates/scaffold_helpers/user_login.html', 'r') as o:
        user_links = o.read()

    update(add_to_navlinks(
        p,
        content=user_links))


"""
UPDATERS
"""
@dataclass
class File:
    filepath: str
    content: str
    mode: str = 'w'


def update(file: File):
    if file:
        with open(file.filepath, file.mode) as m:
            m.write(file.content)


def add_to_main(
    p: str,
    name: str,
    extra_imports: list or None = None,
    extra_includes: list or None = None
) -> File:
    """Adds provided data to the main router with the scaffold router imports.

    When a new scaffolded MVC is added to the project, the router for
    it should be added to main.py. This method will import the router
    and include the router in the main `app`, along with the appropriate
    prefix. Extra imports and app additions may be appended as well.

    Args:
        p (str): The path to the directory containing the main file.
        name (str): name of the router to include.
        extra_imports (listorNone, optional): additional imports to include. Defaults to None.
        extra_includes (listorNone, optional): additional lines of code to include. Defaults to None.

    Return:
        File: the updated file and metadata
    """
    main_file = Path(p) / 'main.py'
    with open(main_file, 'r') as m:
        main = m.readlines()
    imprt = [f'from {name}.router import {name}_router\n']
    incld = [f'\napp.include_router({name}_router, tags=["{name}"], prefix="/{name}")']
    imprt += extra_imports or list()
    incld += extra_includes or list()
    main.insert(
        __get_import_placement(main),
        ''.join(imprt))
    main.append(''.join(incld))
    return File(
        filepath=main_file,
        content=''.join(main),
        mode='w')


def add_to_requirements(p: str, reqs: list) -> File:
    """Adds provided data to the requirements file at the specified path with the provided requirements.

    Args:
        p (str): The path to the directory containing the requirements file.
        reqs (list): A list of requirements to be added to the requirements

    Return:
        File: the updated file and metadata
    """
    req_file = Path(p) / 'requirements.txt'
    with open(req_file, 'r') as m:
        file_reqs = m.readlines()

    file_reqs.insert(0, '\n'.join(reqs) + '\n')
    return File(
        filepath=req_file,
        content=''.join(file_reqs),
        mode='w')


def add_to_env(p: str, **kwargs) -> File:
    """Adds provided data to the env file at the specified path with the provided variables.

    Args:
        p (str): The path to the directory containing the env file.
        kwargs: key and value for each entry

    Return:
        File: the updated file and metadata
    """
    env_file = Path(p) / '.env'
    with open(env_file, 'r') as e:
        file_env = e.readlines()
    file_env += [
        f"""{k}="{v.replace('"', '') if isinstance(v, str) else v}" """
        for k, v in kwargs.items()]
    return File(
        filepath=env_file,
        content='\n'.join(file_env) + '\n',
        mode='w')


def add_to_navlinks(p: str, content: str):
    navlink_file = Path(p) / 'static_pages' / 'templates' / '_navlinks.html'
    if Path.exists(navlink_file):
        with open(navlink_file, 'r') as e:
            file_navlink = e.read()
        return File(
            filepath=navlink_file,
            content=file_navlink + '\n\n' + content,
            mode='w')

def add_obj_list_to_reference(p: str, ref: str, content: str, import_statement: str):
    referencing_model = Path(p) / ref / 'model.py'
    if Path.exists(referencing_model):
        with open(referencing_model, 'r') as e:
            file_model = e.readlines()
        file_model.insert(1, import_statement)
        updated_file = ''.join(file_model) + '\n\n' + content
        return File(
            filepath=referencing_model,
            content=updated_file,
            mode='w'
        )
