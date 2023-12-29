# -*- coding: UTF-8 -*-

'''
Module
    read_template.py
Copyright
    Copyright (C) 2021 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    gen_dbus is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    gen_dbus is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class ReadTemplate with attribute(s) and method(s).
    Creates an API for reading a template files.
'''

import sys
from typing import Any, List, Dict, Tuple
from os.path import dirname, realpath

try:
    from ats_utilities.config_io.file_check import FileCheck
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/gen_dbus'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/gen_dbus/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReadTemplate(FileCheck):
    '''
        Defines class ReadTemplate with attribute(s) and method(s).
        Creates an API for reading a template files.

        It defines:

            :attributes:
                | _GEN_VERBOSE - Console text indicator for process-phase.
                | _TEMPLATE_DIR - Template dir path.
            :methods:
                | __init__ - Initials ReadTemplate constructor.
                | read - Reads a templates.
    '''

    _GEN_VERBOSE: str = 'GEN_DBUS::PRO::READ_TEMPLATE'
    _TEMPLATE_DIR: str = '/../conf/template/'

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials ReadTemplate constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        super().__init__(verbose)
        verbose_message(verbose, [f'{self._GEN_VERBOSE} init reader'])

    def read(
        self,
        pro_setup: Dict[Any, Any],
        pro_type: str | None,
        verbose: bool = False
    ) -> List[Tuple[Dict[str, str], Dict[str, str]]]:
        '''
            Reads a templates.

            :param pro_setup: Project templates
            :type pro_setup: <Dict[Any, Any]>
            :param pro_type: Project type | None
            :type pro_type: <str> | <NoneType>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: Template files for project setup
            :rtype: <dict>
            :exceptions: ATSTypeError | ATSBadCallError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        error_msg, error_id = self.check_params([
            ('dict:pro_setup', pro_setup), ('str:pro_type', pro_type)
        ])
        if error_id == self.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pro_setup):
            raise ATSValueError('missing templates')
        if not bool(pro_type):
            raise ATSValueError('missing project type')
        pro_content: List[Tuple[Dict[str, str], Dict[str, str]]] = []
        pro_index: int | None = None
        if pro_type in pro_setup['templates'][0].keys():
            pro_index = 0
        elif pro_type in pro_setup['templates'][1].keys():
            pro_index = 1
        elif pro_type in pro_setup['templates'][2].keys():
            pro_index = 2
        else:
            return pro_content
        type_templates: List[str] = pro_setup['templates'][pro_index][pro_type]
        type_modules: List[str] = pro_setup['modules'][pro_index][pro_type]
        client_templates: List[str] = type_templates[0]['dbus_client']
        server_templates: List[str] = type_templates[1]['dbus_server']
        client_modules: List[str] = type_modules[0]['dbus_client']
        server_modules: List[str] = type_modules[1]['dbus_server']
        for key_cl_module, cl_module, key_sr_module, sr_module in zip(
            client_modules, client_templates, server_modules, server_templates
        ):
            module_content: str | None = None
            template_content: str | None = None
            current_dir: str = dirname(realpath(__file__))
            template_dir: str = f'{current_dir}{self._TEMPLATE_DIR}'
            cl_module = f'{template_dir}{pro_type}/dbus_client/{cl_module}'
            self.check_path(cl_module, verbose)
            self.check_mode('r', verbose)
            self.check_format(cl_module, 'template', verbose)
            if self.is_file_ok():
                with open(cl_module, 'r', encoding='utf-8') as setup_client:
                    module_content = setup_client.read()
            sr_module = f'{template_dir}{pro_type}/dbus_server/{sr_module}'
            self.check_path(sr_module, verbose)
            self.check_mode('r', verbose)
            self.check_format(sr_module, 'template', verbose)
            if self.is_file_ok():
                with open(sr_module, 'r', encoding='utf-8') as setup_server:
                    template_content = setup_server.read()
            pro_content.append((
                {key_cl_module: module_content},
                {key_sr_module: template_content}
            ))
        return pro_content
