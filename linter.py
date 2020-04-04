#
# linter.py
# Linter for SublimeLinter4, a code checking framework for Sublime Text 3
#
# Written by Joshua Hagins, Al Vaccaro
# Copyright (c) 2015 Joshua Hagins
#
# License: MIT
#

"""This module exports the Scalastyle plugin class."""

from SublimeLinter.lint import Linter
from os import listdir, path


class Scalastyle(Linter):
    """Provides an interface to scalastyle."""

    cmd = None
    regex = (
        r'^(?:(?P<error>error)|(?P<warning>warning))'
        r'(?: file=(?P<file>.+?))'
        r'(?: message=(?P<message>.+?))'
        r'(?: line=(?P<line>\d+))?'
        r'(?: column=(?P<col>\d+))?$'
    )
    multiline = False
    defaults = {
        'selector': 'source.scala'
    }
    line_col_base = (1, 0)
    word_re = r'^(\w+|([\'"]).+?\2)'

    def cmd(self):
        """Return the command to execute."""

        return [
            'java',
            '-jar',
            self.settings['jar_file'],
            '${file}',
            '--config',
            self._get_config()
        ]

    def split_match(self, match):
        """
        Return the components of the match.

        We override this method so that errors with no line number can be displayed.
        """

        match, line, col, error, warning, message, near = super().split_match(match)

        if line is None and message:
            line = 0

        return match, line, col, error, warning, message, near

    def _get_config(self):
        # Return the scalastyle-config.xml config path

        return self.settings['config'] if self.settings.has('config') else self._find_config()

    def _find_config(self):
        # Look for scalastyle-config.xml in file's directory and parent directories

        file_name = 'scalastyle-config.xml'
        file_path = self.settings.context['file_path']
        while file_path != "/" and file_name not in listdir(file_path):
            file_path = path.abspath(file_path + "/../")

        if path.isfile(path.join(file_path, file_name)):
            return path.join(file_path, file_name)
        else:
            raise FileNotFoundError("Couldn't locate {} in {} or parent directories".format(file_name, file))
