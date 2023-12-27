'''
Wrapper for argparse and argcomplete.

Features the following:
 - Arg, a command line argument.
 - App, a command line application or sub-command.
 - Bundle, parsed Args and an actual list of called Apps.
 - Main, a root App with verbose and detailed flags.
'''

import re
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Any, Iterable, Iterator, overload

from .log import logc, loge

try:
    from argcomplete import autocomplete
    from argcomplete.completers import ChoicesCompleter
except:
    def autocomplete(**kwargs) -> 'None':
        return

    class ChoicesCompleter:
        def __init__(self, choices) -> 'None':
            return


__all__ = [
    'Arg',
    'App',
    'Bundle',
    'Main',
]


def _check_type(o, v, t) -> 'None':
    c = type(o).__name__
    if type(t) != tuple:
        t = (t,)
    _v = getattr(o, v)
    if not isinstance(_v, t):
        _t = type(_v).__name__
        ts = ', '.join(x.__name__ for x in t)
        raise TypeError(f'{c}.{v} must be {ts}. Actual type: {_t}.')


class Arg:
    '''
    Class that represents a command line argument, optional or positional.

    All the fields are read-only, some of them depend on the others. They can
    only be set during the object construction, and are thoroughly validated.
    '''

    @property
    def name(self) -> 'str':
        '''
        The value name: "URI" in "--uri URI, -u URI".
        Can be lowercase.

        Restrictions:
         * Type is str.
         * len(self.name) > 0.
         * Can contain: 'a-z', 'A-Z', '0-9', '-', '_'.
         * Must start with: 'a-z', 'A-Z', '0-9'.

        Deduction:
         * self.lopt.upper().
         * self.sopt.upper().
         * 'ARGS' if self.is_multi.
         * 'ARG'.
        '''
        return self.__name

    @property
    def sopt(self) -> 'str':
        '''
        The short option name: "-u" in "--uri URI, -u URI".

        Restrictions:
         * Type is str.
         * len(self.sopt) == 1.
         * Can be 'a-z', 'A-Z', '0-9'.

        Deduction:
         * None.
        '''
        return self.__sopt

    @property
    def lopt(self) -> 'str':
        '''
        The long option name: "--uri" in "--uri URI, -u URI".

        Restrictions:
         * Type is str.
         * len(self.lopt) > 0.
         * Can contain: 'a-z', 'A-Z', '0-9', '-', '_'.
         * Must start with: 'a-z', 'A-Z', '0-9'.

        Deduction:
         * None.
        '''
        return self.__lopt

    @property
    def help(self) -> 'str':
        '''
        Help message text.

        If self.choices is not None, the following will be appended:
        Possible values:
         * value1 - help1
         * value2 - help2
         * (...)

        value1 and value2 are always defined.
        help1 and help2 are available if self.choices is dict.

        If self.default is not None, the following will be appended:
        Defaults to: value1, value2, (...).
        Multiple values will be printed only if self.is_multi.

        Restrictions:
         * Type is str.

        Deduction:
         * str().
        '''
        return self.__help

    @property
    def count(self) -> 'int | str':
        '''
        Number of values consumed by this argument from the command line:

        Restrictions:
         * Type is int or str.
         * Can be any positive int.
         * Can be 0, if self.is_optional.
         * Can be '?' (0 or 1), '*' (0 and more), '+' (1 and more).

        Deduction:
         * '*' if self.default is non-str Iterable.
         * 1.
        '''
        return self.__count

    @property
    def type(self) -> 'type':
        '''
        Type of individual values.

        Restrictions:
         * Type is type.
         * Can be str, int, float, bool.
         * Must be bool or None, if self.is_flag.

        Deduction:
         * bool, if self.is_flag.
         * type(self.choices[0]).
         * type(self.default[0]), if self.is_multi.
         * type(self.default), if self.is_single.
         * str.
        '''
        return self.__type

    @property
    def choices(self) -> 'list':
        '''
        List of allowed argument values.
        Can be dict, in this case:
         * dict.keys are allowed argument values.
         * dict.values are converted to str and treated as a help text.

        Restrictions:
         * Must be None, if self.is_flag.
         * Type is Iterable (not str).
         * Type of each item is self.type.
         * Each item must be unique.

        Deduction:
         * None.
        '''
        return self.__choices

    @property
    def default(self) -> 'Any':
        '''
        Default value, if not specified.

        Restrictions:
         * Must be None, if self.is_flag.
         * Type is self.type, if self.is_single.

        Restrictions (self.is_multi):
         * Type is non-str Iterable.
         * Type of each item is self.type.
         * Each item is in self.choices.
         * len(self.default) == self.count, if self.count is int.
         * len(self.default) > 0, if self.count == '+'.

        Deduction:
         * None.
        '''
        return self.__default

    @property
    def is_optional(self) -> 'bool':
        '''
        True if self.sopt or self.lopt is not None.
        Mutually exclusive with Arg.is_positional.
        '''
        return self.sopt or self.lopt

    @property
    def is_positional(self) -> 'bool':
        '''
        True if self.sopt and self.lopt are None.
        Mutually exclusive with self.is_optional.
        '''
        return not self.is_optional

    @property
    def is_flag(self) -> 'bool':
        '''
        True if self.count is 0.
        Mutually exclusive with self.is_single and self.is_multi.
        '''
        return self.count == 0

    @property
    def is_single(self) -> 'bool':
        '''
        True if self.count is 1 or '?'.
        Mutually exclusive with self.is_flag and self.is_multi.
        '''
        return self.count == 1 or self.count == '?'

    @property
    def is_multi(self) -> 'bool':
        '''
        True if self.count is greater than 1, '*' or '+'.
        Mutually exclusive with self.is_flag and self.is_single.
        '''
        return not (self.is_flag or self.is_single)

    def __init__(
        self,
        name: 'str' = None,
        sopt: 'str' = None,
        lopt: 'str' = None,
        help: 'str' = None,
        type: 'type' = None,
        count: 'int | str' = None,
        choices: 'Iterable' = None,
        default: 'Any' = None,
    ) -> 'None':
        '''
        Constructs Arg with the given fields.
        Refer to the corresponding fields for restrictions and deductions.
        '''
        # Set immediately, so there is no need to pass the parameters.
        self.__name = name
        self.__sopt = sopt
        self.__lopt = lopt
        self.__help = help
        self.__type = type
        self.__count = count
        self.__choices = choices
        self.__default = default
        # The order matters, many fields depend on the others.
        self.__init_sopt()
        self.__init_lopt()
        self.__init_count()
        self.__init_type()
        self.__init_choices()
        self.__init_default()
        self.__init_name()
        self.__init_help()

    def __call__(
        self,
        v: 'bool | list[str] | None',
    ) -> 'str | int | float | bool | list | None':
        '''
        Parse command line values into an actual value. This method is
        supposed to be called in two cases:
         * By this module, to obtain the actual values.
           The values will be associated with the Arg object in the Bundle.
         * By a sub-class of Arg, in the overridden method.
           This way basic types in the command line can be parse into more
           complex objects.

        Parameters:
         * v - value from the command line, depends on self.count.
           If self.is_flag, it is True (present) or False (absent).
           Otherwise, it is list[str] (present) or None (absent).
           This parameter is guaranteed to be valid: compatible with self.type,
           be present in choices, correct number of values, and so on.

        Raises:
         * ValueError if v is not in self.choices.

        Returns:
         * v, if self.is_flag.
         * [], if self.is_multi and self.is_positional and bool(v) is False.
         * self.default, if v was None.
         * A list of values converted to self.type, if self.is_multi.
         * self.type(v).
        '''
        if self.is_flag:
            return v
        if self.is_multi and self.is_positional and not v:
            return self.default or []
        if v == None:
            return self.default
        v = [self.type(x) for x in v]
        if self.choices:
            for x in v:
                if x not in self.choices:
                    choices = '\n * '.join(str(x) for x in self.choices)
                    raise ValueError(
                        f'Invalid value for argument {self.name}: {x}. '
                        f'The value must be in choices:\n * {choices}')
        return v if self.is_multi else v[0]

    def __init_sopt(self) -> 'None':
        if self.sopt == None:
            return
        _check_type(self, 'sopt', str)
        if self.sopt == str():
            raise ValueError('Arg.sopt must not be empty.')
        if len(self.sopt) != 1:
            raise ValueError(
                f'Arg.sopt must be a single character. '
                f'Actual length: {len(self.sopt)}.')
        if not re.match(r'^[a-zA-Z0-9]$', self.sopt):
            raise ValueError(
                f'Arg.sopt must be one of: a-z, A-Z, 0-9. '
                f'Actual value: {self.sopt}.')

    def __init_lopt(self) -> 'None':
        if self.lopt == None:
            return
        _check_type(self, 'lopt', str)
        if self.lopt == str():
            raise ValueError('Arg.lopt must not be empty.')
        if not re.match(r'^[a-zA-Z0-9]$', self.lopt[0]):
            raise ValueError(
                f'Arg.lopt must start with a-z, A-Z, 0-9. '
                f'Found an invalid character: {self.lopt[0]}.')
        chars = re.findall(r'[^a-zA-Z0-9_-]', self.lopt)
        if chars:
            raise ValueError(
                f'Arg.lopt must contain only a-z, A-Z, 0-9, _, -. '
                f'Found an invalid character: {chars[0]}.')

    def __init_count(self) -> 'None':
        if self.count == None:
            self.__count = '*' if Arg.__is_container(self.default) else 1
            return
        _check_type(self, 'count', (int, str))
        if isinstance(self.count, int) and self.count > 0:
            return
        if self.count in ['?', '+', '*']:
            return
        if self.count == 0:
            if self.is_optional:
                return
            raise ValueError(
                'Arg.count must not be 0 if Arg.is_positional.')
        raise ValueError(
            f'Arg.count must be non-negative int, "?", "*", "+". '
            f'Actual value: {self.count}.')

    def __init_name(self) -> 'None':
        if self.name == None:
            if self.lopt != None:
                self.__name = self.lopt.upper()
            elif self.sopt != None:
                self.__name = self.sopt.upper()
            elif self.is_multi:
                self.__name = 'ARGS'
            else:
                self.__name = 'ARG'
            return
        _check_type(self, 'name', str)
        if self.name == str():
            raise ValueError('Arg.name must not be empty.')
        if not re.match(r'^[a-zA-Z0-9]$', self.name[0]):
            raise ValueError(
                f'Arg.name must start with a-z, A-Z, 0-9. '
                f'Found an invalid character: {self.name[0]}.')
        chars = re.findall(r'[^a-zA-Z0-9_-]', self.name)
        if chars:
            raise ValueError(
                f'Arg.name must contain only a-z, A-Z, 0-9, _, -. '
                f'Found an invalid character: {chars[0]}.')

    def __init_help(self) -> 'None':
        if self.help == None:
            self.__help = str()
        _check_type(self, 'help', str)
        if self.choices:
            self.__help += '\nPossible values:'
            if not isinstance(self.choices, dict):
                self.__help += '\n * '
                self.__help += '\n * '.join(str(x) for x in self.choices)
            else:
                w = max(len(str(x)) for x in self.choices)
                for x in self.choices:
                    self.__help += f'\n * {str(x):{w}} - {self.choices[x]}'
        if self.default:
            self.__help += '\nDefaults to: '
            if self.is_single:
                self.__help += str(self.default)
            else:
                self.__help += ' '.join(str(x) for x in self.default)

    def __init_type(self) -> 'None':
        if self.type == None:
            if self.is_flag:
                self.__type = bool
            elif self.choices and isinstance(self.choices, Iterable):
                self.__type = type(next(iter(self.choices)))
            elif self.default:
                if isinstance(self.default, Iterable):
                    self.__type = type(next(iter(self.default)))
                else:
                    self.__type = type(self.default)
            else:
                self.__type = str
        _check_type(self, 'type', type)
        if not issubclass(self.type, (str, int, float, bool)):
            raise ValueError(
                f'Arg.type value must be str, int, float or bool. '
                f'Actual value: {self.type.__name__}.')
        if self.is_flag and not issubclass(self.type, bool):
            raise ValueError(
                f'Arg.type must be bool or None if Arg.is_flag. '
                f'Actual value: {self.type.__name__}.')

    def __init_choices(self) -> 'None':
        if self.choices == None:
            return
        t = type(self.choices).__name__
        if self.is_flag:
            raise ValueError(
                f'Arg.choices must be None if Arg.is_flag. '
                f'Actual type: {t}.')
        if not Arg.__is_container(self.choices):
            raise TypeError(
                f'Arg.choices must be Iterable (not str). '
                f'Actual type: {t}.')
        if not self.choices:
            raise ValueError('Arg.choices must not be empty.')
        seen = set()
        for x in self.choices:
            if not isinstance(x, self.type):
                raise ValueError(
                    f'Arg.choices values must be {self.type.__name__}. '
                    f'Found {type(x).__name__}: {x}.')
            if x in seen:
                raise ValueError(
                    f'Arg.choices must not have duplicates. '
                    f'Duplicate value: {x}.')
            seen.add(x)

    def __init_default(self) -> 'None':
        if self.default == None:
            return
        t = type(self.default).__name__
        if self.is_flag:
            raise ValueError(
                f'Arg.default must be None if Arg.is_flag. '
                f'Actual type: {t}.')
        elif self.is_single:
            _check_type(self, 'default', self.type)
            if self.choices:
                if self.default not in self.choices:
                    raise ValueError(
                        f'Arg.default must be in Arg.choices. '
                        f'Actual value: {self.default}.')
        else:
            if not Arg.__is_container(self.default):
                raise TypeError(
                    f'Arg.default must be Iterable (not str). '
                    f'Actual type: {t}.')
            if self.count == '+' and len(self.default) == 0:
                raise ValueError(
                    'Arg.default must not be empty if Arg.count is "+".')
            if isinstance(self.count, int) and len(self.default) != self.count:
                raise ValueError(
                    f'Arg.default must have {self.count} values. '
                    f'Actual number of values: {len(self.default)}.')
            if self.choices:
                for x in self.default:
                    if x not in self.choices:
                        raise ValueError(
                            f'Arg.default values must be in Arg.choices. '
                            f'Found unknown value: {x}.')
            else:
                for x in self.default:
                    if not isinstance(x, self.type):
                        raise TypeError(
                            f'Arg.default values must be {self.type.__name__}. '
                            f'Found {type(x).__name__}: {x}.')

    @staticmethod
    def __is_container(o) -> 'bool':
        return isinstance(o, Iterable) and not isinstance(o, str)


class App:
    '''
    Class that represents a command line application.
    App is a also a container for:
     * App.args - App's command line arguments.
     * App.apps - App's sub-commands.

    All the fields are read-only. They can only be set during the object
    construction, and are thoroughly validated. App.args and App.apps can
    be altered via the corresponding methods.
    '''

    @property
    def name(self) -> 'str':
        '''
        The app name.

        Restrictions:
         * Must be set.
         * Type is str.
         * len(self.name) > 0.
         * Can contain: 'a-z', 'A-Z', '0-9', '-', '_'.
         * Must start with: 'a-z', 'A-Z', '0-9'.
        '''
        return self.__name

    @property
    def help(self) -> 'str':
        '''
        A short help for sub-command.

        Restrictions:
         * Type is str.

        Deduction:
         * None.
        '''
        return self.__help

    @property
    def prolog(self) -> 'str':
        '''
        A detailed help before the option list.

        Restrictions:
         * Type is str.

        Deduction:
         * self.help.
        '''
        return self.__prolog

    @property
    def epilog(self) -> 'str':
        '''
        A detailed help after the option list.

        Restrictions:
         * Type is str.

        Deduction:
         * None.
        '''
        return self.__epilog

    @property
    def args(self) -> 'Iterable[Arg]':
        '''
        An Iterable over this App's Args.
        Can be modified via the dedicated methods:
         * self.add(Arg)
         * self.pop(Arg)
        '''
        return self.__args

    @property
    def apps(self) -> 'Iterable[App]':
        '''
        An Iterable over this App's sub-commands (also Apps).
        Can be modified via the dedicated methods:
         * self.add(App)
         * self.pop(App)
        '''
        return self.__apps

    @property
    def parent(self) -> 'App | None':
        '''
        A parent App.
        None if self.is_root.
        '''
        return self.__parent

    @property
    def root(self) -> 'App':
        '''
        The root App.
        '''
        o = self
        while o.parent:
            o = o.parent
        return o

    @property
    def is_root(self) -> 'bool':
        '''
        True if the App is a root App (not a sub-command).
        '''
        return not self.__parent

    @overload
    def add(self, o: 'Arg') -> 'None':
        '''
        Adds Arg to self.args.

        Parameters:
         * o - Arg to add.

        Raises:
         * TypeError, if o is not Arg.
         * ValueError, if Arg with the same sopt or lopt is already added.

        Returns:
         * None.
        '''

    @overload
    def add(self, o: 'App') -> 'None':
        '''
        Adds App to self.apps, making it a sub-command.

        Parameters:
         * o - App to add.

        Raises:
         * TypeError, if o is not App.
         * ValueError, if o.parent is not None (already a sub-command).
         * ValueError, if App with the same name is already added.

        Returns:
         * None.
        '''

    def add(self, o: 'Arg | App') -> 'None':
        if not isinstance(o, (Arg, App)):
            raise TypeError(
                f'App.add(): Cannot add object of type {type(o).__name__}.')
        if isinstance(o, Arg):
            for x in self.args:
                if x.sopt == o.sopt and x.sopt:
                    raise ValueError(
                        f'App.add(): Cannot add Arg. '
                        f'Another Arg already has the same sopt: {x.sopt}.')
                if x.lopt == o.lopt and x.lopt:
                    raise ValueError(
                        f'App.add(): Cannot add Arg. '
                        f'Another Arg already has the same lopt: {x.lopt}.')
            self.__args.append(o)
        else:
            if o.parent:
                raise ValueError(
                    f'App.add(): Cannot add App: {o.name}. '
                    f'Already has a parent: {o.parent.name}.')
            for x in self.apps:
                if x.name == o.name:
                    raise ValueError(
                        f'App.add(): Cannot add App: {o.name}. '
                        f'Another App already has the same name.')
            self.__apps.append(o)
            o.__parent = self

    @overload
    def pop(self, o: 'Arg') -> 'None':
        '''
        Removes Arg from self.args.

        Parameters:
         * o - Arg to remove.

        Raises:
         * TypeError, if o is not Arg.
         * ValueError, if o is not in self.args.
         * ValueError, if self.args is empty.

        Returns:
         * None.
        '''

    @overload
    def pop(self, o: 'App') -> 'None':
        '''
        Removes App from self.apps.

        Parameters:
         * o - App to remove.

        Raises:
         * TypeError, if o is not App.
         * ValueError, if o is not in self.apps.
         * ValueError, if self.apps is empty.

        Returns:
         * None.
        '''

    def pop(self, o: 'Arg | App') -> 'None':
        if o != None and not isinstance(o, (Arg, App)):
            raise TypeError(
                f'App.pop(): Cannot pop object of type {type(o).__name__}.')
        if isinstance(o, Arg):
            _list = self.__args
            _type = 'Arg'
            _name = o.lopt or o.sopt or o.name
        else:
            _list = self.__apps
            _type = 'App'
            _name = o.name
        if not _list:
            raise ValueError(
                f'App.pop(): Cannot pop {_type}. '
                f'App.{_type.lower()}s is empty.')
        if o not in _list:
            raise ValueError(
                f'App.pop(): Cannot pop {_type}. '
                f'{_type} is not in App.{_type.lower()}s: {_name}.')
        _list.remove(o)

    def __init__(
        self,
        name: 'str',
        help: 'str' = None,
        prolog: 'str' = None,
        epilog: 'str' = None,
    ) -> 'None':
        '''
        Constructs App with the given fields.
        Refer to the corresponding fields for restrictions and deductions.
        '''
        # Set immediately, so there is no need to pass the parameters.
        self.__name = name
        self.__help = help
        self.__prolog = prolog
        self.__epilog = epilog
        self.__args: 'list[Arg]' = []
        self.__apps: 'list[App]' = []
        self.__parent: 'App' = None
        # The order matters, some fields may depend on the others.
        self.__init_name()
        self.__init_help()
        self.__init_prolog()
        self.__init_epilog()

    def __call__(self, bundle: 'Bundle') -> 'None':
        '''
        This method is called in Main.__call__() on the Main itself and all its
        sub-commands that are mentioned in the command line. App sub-classes
        are expected to override this method and perform some actions based
        on the arguments stored in the Bundle. All the arguments from the
        command line are available, not just the ones from the current App.
        In case of errors, an Exception should be raised, it will be handled
        by Main.__call__().

        Parameters:
         * bundle - a valid Bundle object.

        Returns:
         * None.
        '''

    def __init_name(self) -> 'None':
        _check_type(self, 'name', str)
        if self.name == str():
            raise ValueError('App.name must not be empty.')
        if not re.match(r'^[a-zA-Z0-9]$', self.name[0]):
            raise ValueError(
                f'App.name must start with a-z, A-Z, 0-9. '
                f'Found an invalid character: {self.name[0]}.')
        chars = re.findall(r'[^a-zA-Z0-9_-]', self.name)
        if chars:
            raise ValueError(
                f'App.name must contain only a-z, A-Z, 0-9, _, -. '
                f'Found an invalid character: {chars[0]}.')

    def __init_help(self) -> 'None':
        if self.help == None:
            return
        _check_type(self, 'help', str)

    def __init_prolog(self) -> 'None':
        if self.prolog == None:
            self.__prolog = self.help
            return
        _check_type(self, 'prolog', str)

    def __init_epilog(self) -> 'None':
        if self.epilog == None:
            return
        _check_type(self, 'epilog', str)


class Bundle:
    '''
    A parsed command line, offers access to:
     * Args and their values, via dict-like interface.
     * Apps that are called, via list-like interface.
    '''

    def __init__(
        self,
        args: 'dict[Arg, Any]',
        apps: 'list[App]',
    ) -> 'None':
        self.__args = args
        self.__apps = apps

    @overload
    def __getitem__(self, key: 'Arg') -> 'Any':
        '''
        Get the command line value of the specific Arg.

        Parameters:
         * key - Arg that serves as a key.

        Raises:
         * TypeError if key is not Arg.

        Return:
         * None, if Arg is not present.
         * Value that was parsed from the command line.
        '''

    @overload
    def __getitem__(self, key: 'int') -> 'App':
        '''
        Get an application from the call stack.

        Parameters:
         * key - index of the App in the call stack. The root App is 0.

        Raises:
         * TypeError if key is not int.
         * ValueError if key is out of bounds.

        Return:
         * App at the specified index.
        '''

    def __getitem__(self, key: 'Arg') -> 'Any':
        if not isinstance(key, (Arg, int)):
            raise TypeError(
                f'Bundle[]: key must be Arg or int. '
                f'Actual type: {type(key).__name__}.')
        if isinstance(key, int):
            l = len(self)
            if key not in range(-l, l):
                raise ValueError(
                    f'Bundle[]: int key must be from {-l} to {l - 1}. '
                    f'Actual value: {key}.')
            return self.__apps[key]
        else:
            return self.__args.get(key, None)

    def __len__(self) -> 'int':
        '''
        Number of Apps in the call stack.
        '''
        return len(self.__apps)

    def __iter__(self) -> 'Iterator[App]':
        '''
        Iterator over Apps in the call stack.
        '''
        return iter(self.__apps)

    def keys(self) -> 'Iterable[Arg]':
        '''
        Iterable of all Args in the command line.
        '''
        return self.__args.keys()

    def values(self) -> 'Iterable[Any]':
        '''
        Iterable of all Arg values in the command line.
        '''
        return self.__args.values()

    def items(self) -> 'Iterable[tuple[Arg, Any]]':
        '''
        Iterable of all Arg-value pairs in the command line.
        '''
        return self.__args.items()


class Formatter(RawTextHelpFormatter):
    '''
    ArgumentParser formatter that preserves the text layout.
    '''

    def __init__(self, *args, **kwds) -> 'None':
        # This is an undocumented option, might stop working.
        kwds['max_help_position'] = 255
        super().__init__(*args, **kwds)


class Parser:
    '''
    A collection of static functions, actually encapsulates argparse
    and argcomplete. This class is not exposed to the user.
    '''

    @staticmethod
    def construct(
        app: 'App',
        parser: 'ArgumentParser' = None,
    ) -> 'ArgumentParser':
        # This is only for the root App.
        parser = parser or ArgumentParser(add_help=False)
        # Set fields of the ArgumentParser.
        kwargs = Parser.app(app)
        for k, v in kwargs.items():
            setattr(parser, k, v)
        # Add arguments to the ArgumentParser.
        parser.add_argument(
            '-h', '--help',
            action='help',
            help=f'Show this help message and exit.')
        for arg in app.args:
            kwargs = Parser.arg(arg)
            args = kwargs.pop('args')
            completer = kwargs.pop('completer')
            o = parser.add_argument(*args, **kwargs)
            setattr(o, 'completer', completer)
        # Recursively construct the sub-commands.
        if app.apps:
            sub = parser.add_subparsers(**Parser.sub(app))
            for x in app.apps:
                Parser.construct(x, sub.add_parser(x.name, add_help=False))
        return parser

    @staticmethod
    def complete(parser: 'ArgumentParser') -> 'None':
        autocomplete(
            argument_parser=parser,
            always_complete_options=False,
        )

    @staticmethod
    def parse(
        parser: 'ArgumentParser',
        app: 'App',
        argv: 'list[str]',
    ) -> 'Bundle':
        parsed = parser.parse_args(argv)
        apps: 'list[App]' = []
        args: 'dict[Arg, Any]' = {}
        while True:
            apps.append(app)
            # Parse arguments.
            for x in app.args:
                values = getattr(parsed, Parser.uid(x), None)
                if x.is_flag:
                    values = bool(values)
                if x.count == '?' and values != None:
                    values = [values]
                args[x] = x(values)
            # Continue with a sub-command.
            name = getattr(parsed, Parser.uid(app), None)
            if name == None:
                break
            for x in app.apps:
                if name == x.name:
                    app = x
                    break
        return Bundle(args, apps)

    @staticmethod
    def arg(o: 'Arg') -> 'dict[str, Any]':
        '''
        Translate Arg to args and kwargs for ArgumentParser.add_argument().
        Note that the result contains two keys that must be used separately:
         * args      - must be used as positional args. Always present.
         * completer - must be set after the argument construction, because
                       argparse does not support custom fields.
        '''
        args = []
        kwargs = {
            'args': args,
            'dest': Parser.uid(o),
            'metavar': o.name,
            'nargs': o.count,
            'help': o.help,
            'completer': None,
        }
        if o.choices:
            kwargs['completer'] = ChoicesCompleter([*o.choices])
        if o.is_optional:
            if o.sopt:
                args.append(f'-{o.sopt}')
            if o.lopt:
                args.append(f'--{o.lopt}')
            if o.is_flag:
                kwargs.pop('metavar')
                kwargs.pop('nargs')
                kwargs['action'] = 'store_true'
        return kwargs

    @staticmethod
    def app(o: 'App') -> 'dict[str, Any]':
        '''
        Translate App to kwargs for ArgumentParser.
        '''
        return {
            'prog': o.name,
            'description': o.prolog,
            'epilog': o.epilog,
            'formatter_class': Formatter,
        }

    @staticmethod
    def sub(o: 'App') -> 'dict[str, Any]':
        '''
        Translate App to kwargs for ArgumentParser.add_subparsers().
        Supposed to be used only for Apps with sub-commands.
        '''
        # Generate help.
        width = max([len(x.name) for x in o.apps])
        nline = '\n' + ' ' * (width + 6)  # Padded newline for the items.
        help = 'Sub-command:'
        for x in o.apps:
            if x.help:
                brief = x.help.replace('\n', nline)
                help += f'\n * {x.name:{width}} - {brief}'
            else:
                help += f'\n * {x.name}'
        # Return kwargs.
        kwargs = {
            'dest': Parser.uid(o),
            'help': help,
            'metavar': 'APP',
        }
        if sys.version_info.minor >= 7:
            kwargs['required'] = True
        return kwargs

    @staticmethod
    def uid(o: 'Arg | App') -> 'str':
        '''
        Get a unique id for the object.
        '''
        return str(id(o))


class Main(App):
    '''
    A sub-class of App that represent the root App.
    Its __call__() method is overloaded to accept Bundle (as App does) and
    list[str] - a list of command line arguments.
    In the first case it behaves like a normal App.
    In the second case it parses and executes the provided command line.

    Main also provides flags that control pykit.log verbosity:
     * arg_verbose  - configures logc(verbose), -v, --verbose.
     * arg_detailed - configures logc(detailed), -d, --detailed.
    '''

    def __init__(
        self,
        name: 'str',
        help: 'str' = None,
        prolog: 'str' = None,
        epilog: 'str' = None,
    ) -> 'None':
        super().__init__(name, help, prolog, epilog)
        self.arg_verbose = Arg(
            sopt='v',
            lopt='verbose',
            help='Print debug and trace logs.',
            count=0,
        )
        self.add(self.arg_verbose)
        self.arg_detailed = Arg(
            sopt='d',
            lopt='detailed',
            help='Print timestamp, process, thread, level, path.',
            count=0,
        )
        self.add(self.arg_detailed)

    @overload
    def __call__(self, bundle: 'Bundle') -> 'None':
        pass

    @overload
    def __call__(self, args: 'Iterable' = sys.argv) -> 'None':
        '''
        Overload specific to class Main. Parses the command line and executes
        it accodingly. Note that it always calls sys.exit() with 0 if there
        was no issues, and 1 if there is an Exception. All exceptions raised
        after the command line parsing are catched and printed via pykit.log.

        Parameters:
         * argv - a list of individual command line tokens. The first item is
                  assumed to be the name of the executable, and is ignored.

        Raises:
         * TypeError, if argv is not Iterable.

        Returns:
         * None.
        '''

    def __call__(
        self,
        argv: 'Bundle | Iterable' = sys.argv,
    ) -> 'None':
        if isinstance(argv, Bundle):
            return
        if not isinstance(argv, Iterable):
            raise TypeError(
                f'Main.__call__(): argv must be Iterable. '
                f'Actual type: {type(argv).__name__}.')
        argv = [str(x) for x in argv][1:]
        parser = Parser.construct(self)
        Parser.complete(parser)
        bundle = Parser.parse(parser, self, argv)
        logc(
            verbose=bundle[self.arg_verbose],
            detailed=bundle[self.arg_detailed],
        )
        try:
            for i in range(len(bundle)):
                bundle[i](bundle)
        except Exception as e:
            loge(e)
            sys.exit(1)
        sys.exit(0)
