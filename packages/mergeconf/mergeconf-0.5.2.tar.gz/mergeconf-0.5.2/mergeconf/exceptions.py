# vi: set softtabstop=2 ts=2 sw=2 expandtab:
# pylint: disable=redefined-builtin
# TODO: at some point rename `type` parameter and remove exception for
#       redefined-builtin
"""
Exceptions raised by MergeConf package.
"""

class MissingConfiguration(Exception):
  """
  Raised if mandatory configuration items are missing.

  Attributes:
    missing: string list of missing items in section-dot-key notation,
      separated by commas.
  """

  def __init__(self, missing):
    self._missing = missing

    description = f"Undefined mandatory variables: {missing}"
    super().__init__(description)

  @property
  def missing(self):
    """ Return the string list of missing items """
    return self._missing

class MissingConfigurationFile(Exception):
  """
  Raised if the specified configuration file is missing or otherwise
  unreadable.

  Attributes:
    file: the missing file
  """

  def __init__(self, file):
    self._file = file
    description = f"Configuration file missing or unreadable: {file}"
    super().__init__(description)

  @property
  def file(self):
    """ Return the missing or unreadable file """
    return self._file

class UnsupportedType(Exception):
  """
  Raised if a configuration item is added with an unsupported type.

  Attributes:
    type: the unsupported type
  """

  def __init__(self, type):
    self._type = type.__name__
    description = f"Unsupported type: {self._type}"
    super().__init__(description)

  @property
  def type(self):
    """ Return the unsupported type """
    return self._type

class UndefinedSection(Exception):
  """
  Raised if a section is found that was not defined for the parser.

  Attributes:
    section: the section name
  """
  def __init__(self, section):
    self._section = section
    description = f"Unexpected section found: '{section}'"
    super().__init__(description)

  @property
  def section(self):
    """ Return the undefined section """
    return self._section

class UndefinedConfiguration(Exception):
  """
  Raised if a configuration item is found that was not defined for the parser.

  Attributes:
    section: the section name
    item: the item name
  """
  def __init__(self, section, item):
    self._section = section
    self._item = item
    description = f"Unexpected configuration item found: '{item}' in section '{section}'"
    super().__init__(description)

  @property
  def section(self):
    """ Return the section where the item was found """
    return self._section

  @property
  def item(self):
    """ Return the undefined item """
    return self._item

#class Deprecated(Exception):
#  """
#  Raised for hard deprecations where functionality has been removed and the
#  API is not available at all.
#
#  Attributes:
#    version: the last version in which this functionality is available.
#    message: further information to assist the user.
#  """
#  def __init__(self, version, message=None):
#    self._version = version
#    self._message = message
#    self._function = inspect.stack()[1].function
#    etc = f": {message}" if message else '.'
#    description = f"Deprecated API `{self._function}` last available in version {version}{etc}"
#    super().__init__(description)
#
#  @property
#  def function(self):
#    return self._function
#
#  @property
#  def version(self):
#    return self._version
