from collections import OrderedDict as odict
from inspect import _empty as NoTypeInfo
from inspect import _ParameterKind as ParameterKind
from inspect import signature
from string import Template
from typing import Callable
from typing import Optional
from typing import TypeVar


T = TypeVar('T')

class CheckSignature:

    def __init__(self, func: Optional[Callable[..., T]] = None):
        self.func = func

    def evaluate(self, *args, **kwargs):
        if not self.func:
            return None

        given_params = args
        given_kw_params = tuple(odict(kwargs).values())
        parameters = signature(self.func).parameters
        parameters_names = tuple(parameters.keys())

        if not len(parameters_names):
            return None

        i = 0
        while i < len(parameters_names):
            parameter_name = parameters_names[i]
            expected_type = parameters[parameter_name].annotation

            try:
                if parameters[parameter_name].kind == ParameterKind.VAR_POSITIONAL:
                    for j in range(len(given_params)):
                        given_param = given_params[i + j]
                        check_type(given_param, parameter_name, expected_type)
                if parameters[parameter_name].kind == ParameterKind.VAR_KEYWORD:
                    for k, _ in enumerate(given_kw_params):
                        given_kw_param = given_kw_params[k]
                        check_type(given_kw_param, parameter_name, expected_type)
                    break

                given_param = given_params[i]
                check_type(given_param, parameter_name, expected_type)
            except IndexError:
                pass
            
            i += 1

    def __call__(self, *args, **kwargs):
        if self.func:
            self.evaluate(*args, **kwargs)
            return self.func(*args, **kwargs)

    def __repr__(self):
        if self.func:
            return f'<CheckSignature({self.func.__name__})>'
        else:
            return f'<CheckSignature()>'

    def __str__(self):
        if self.func:
            return self.func.__name__
        else:
            return ''


def check_type(param_value, param_name, expected_type):
    given_param_type = type(param_value)

    def raise_TypeError(expected_type_name: str):
        issue = Template(
            'Expected parameter "$param" with value "$value" to be of type, "$expected_type". '
        )
        actuality = Template(
            'Received "$given_type" instead.'
        )
        raise TypeError(
            issue.substitute(
                param=param_name,
                value=param_value,
                expected_type=expected_type_name
            ) + actuality.substitute(
                given_type=type(param_value).__name__
            )
        )

    if expected_type != NoTypeInfo:
        if str(expected_type).startswith('typing.Union'):
            if given_param_type not in expected_type.__args__:
                raise_TypeError(f'{[et.__name__ for et in expected_type.__args__]}')
        else:
            if given_param_type != expected_type:
                raise_TypeError(expected_type.__name__)


def checksignature(function: Callable = None):
    return CheckSignature(function)


