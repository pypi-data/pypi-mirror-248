import os
from pathlib import Path
import yaml

from cloudmesh.catalog.converter import Converter
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import banner
from cloudmesh.common.util import readfile
from cloudmesh.common.util import writefile
from cloudmesh.common.console import Console

class Convert:
    """Implementation in support for

    catalog export bibtex [--name=NAME] [--source=SOURCE] [--destination=DESTINATION]
    catalog export md [--name=NAME]  [--source=SOURCE] [--destination=DESTINATION]
    catalog export [hugo] md [--name=NAME]  [--source=SOURCE] [--destination=DESTINATION]

    Convert Class

    This class provides support for exporting catalog entries in different formats.

    Methods:
        - convert(source=None, conversion=None, template=None): Convert catalog entries from YAML to other formats.
        - template(sources=None, template=None): Apply a template to catalog entries.
        - bibtex(sources=None): Export catalog entries to BibTeX format.
        - markdown(sources=None): Export catalog entries to Markdown format.
        - hugo_markdown(sources=None): Export catalog entries to Hugo Markdown format.
        - yaml_check(source=".", relative=True): Check YAML files for formatting and content issues.

    Usage:
        convert_instance = Convert()
        convert_instance.convert(source='path/to/catalog.yaml', conversion=convert_instance._markdown)
        convert_instance.bibtex(sources=['entry1.yaml', 'entry2.yaml'])
        convert_instance.hugo_markdown(sources=['entry3.yaml'])
        convert_instance.yaml_check(source='catalog_dir', relative=True)
    """

    def __init__(self):
        """
        Initialize the Convert class.

        Args:
            None

        Returns:
            None
        """
        pass

    def _find_sources_from_dir(self, source=None):
        """
        Find YAML sources in a directory.

        Args:
            source (str): Directory path.

        Returns:
            generator: Generator containing YAML sources.
        """
        source = Path(source).resolve()
        result = Path(source).rglob('*.yaml')
        return result

    def convert(self, source=None, conversion=None, template=None):
        """
        Convert catalog entries from YAML to other formats.

        Args:
            source (str or list): Source file(s) or directory path.
            conversion (callable): Conversion function.
            template (str): Template name.

        Returns:
            None
        """
        if type(source) is str and os.path.isdir(source):
            sources = self._find_sources_from_dir(source=source)
        elif type(source) is str:
            sources = [source]
        else:
            sources = source
        for source in sources:
            print(f"Convert {source} to {conversion.__name__[1:]}")
            if template is None:
                conversion(source)
            else:
                conversion(source, template)

    def _bibtex(self, source):
        """
        Convert YAML to BibTeX format.

        Args:
            source (str): Source YAML file.

        Returns:
            None
        """
        destination = str(source).replace(".yaml", ".bib")
        converter = Converter(filename=source)
        entry = converter.bibtex()
        writefile(destination, entry)

    def _markdown(self, source):
        """
        Convert YAML to Markdown format.

        Args:
            source (str): Source YAML file.

        Returns:
            None
        """
        destination = str(source).replace(".yaml", ".md")
        converter = Converter(filename=source)
        entry = converter.markdown()
        writefile(destination, entry)

    def _hugo_markdown(self, source):
        """
        Convert YAML to Hugo Markdown format.

        Args:
            source (str): Source YAML file.

        Returns:
            None
        """
        destination = str(source).replace(".yaml", "-h.md")
        converter = Converter(filename=source)
        entry = converter.hugo_markdown()
        writefile(destination, entry)

    def _template(self, source, template):
        """
        Apply a template to YAML.

        Args:
            source (str): Source YAML file.
            template (str): Template name.

        Returns:
            None
        """
        raise NotImplementedError
        ending = str(source).rsplit(".")[1]
        destination = str(source).replace(".yaml", ending)
        converter = Converter(filename=source)
        entry = converter.template(template)
        writefile(destination, entry)

    def template(self, sources=None, template=None):
        """
        Apply a template to catalog entries.

        Args:
            sources (str or list): Source file(s) or directory path.
            template (str): Template name.

        Returns:
            None
        """
        self.convert(sources, self._template, template=template)

    def bibtex(self, sources=None):
        """
         Export catalog entries to BibTeX format.

         Args:
             sources (str or list): Source file(s) or directory path.

         Returns:
             None
         """
        self.convert(sources, self._bibtex)

    def markdown(self, sources=None):
        """
        Export catalog entries to Markdown format.

        Args:
            sources (str or list): Source file(s) or directory path.

        Returns:
            None
        """
        self.convert(sources, self._markdown)

    def hugo_markdown(self, sources=None):
        """
         Export catalog entries to Hugo Markdown format.

         Args:
             sources (str or list): Source file(s) or directory path.

         Returns:
             None
         """
        self.convert(sources, self._hugo_markdown)

    def _shorten_path(self, source):
        """
        Shorten the file path.

        Args:
            source (str): File path.

        Returns:
            str: Shortened file path.
        """
        return str(source).replace(os.getcwd(), ".")

    def yaml_check(self, source=".", relative=True):
        """
         Check YAML files for formatting and content issues.

         Args:
             source (str): Source file or directory path.
             relative (bool): If True, display the relative file path.

         Returns:
             None
         """
        source = Path(source).resolve()
        banner(f"check {source}")
        for filename in Path(source).rglob('*.yaml'):
            content = readfile(filename).splitlines()
            report = Shell.run(f"yamllint {filename}").strip().splitlines()[1:]
            for entry in report:
                entry = self._shorten_path(entry)
                entry = entry.replace("\t", " ").strip()
                # line, column\
                parts = entry.split()
                line, column = parts[0].split(":")
                line = int(line)
                try:
                    if "line too long" in entry and not "http" in entry:
                        pass
                    else:
                        print(
                            filename, "\n",
                            content[line - 1], "\n",
                            entry,
                        )
                        print()
                except:
                    pass

            content = readfile(filename)
            entry = yaml.safe_load(content)

            _filename = filename
            if relative:
                _filename = self._shorten_path(filename)

            value = entry["id"]
            if value.lower() in ["missing", "unkown"]:
                Console.error(f"id is not specified {_filename} id={value} wrong")
            try:
                for _date in ["modified", "created"]:
                    value = str(entry[_date])
                    try:
                        year, month, day = value.strip().split("-")
                        year = int(year)
                        month = int(month)
                        day = int(day)
                        if not (1900 <= year <= 2100):
                            Console.error(f"year format in {_filename} at {_date} wrong: it should be YYYY-MM-DD found '{value}'")
                        if not (1 <= month <= 12):
                            Console.error(f"month format in {_filename} at {_date} wrong: it should be YYYY-MM-DD found '{value}'")
                        if not (1 <= day <= 31):
                            Console.error(f"day format in {_filename} at {_date} wrong: it should be YYYY-MM-DD found '{value}'")
                    except Exception as e:
                        Console.error(f"time format in {_filename} at {_date} wrong: it should be YYYY-MM-DD found '{value}'")

                        print (e)
            except Exception as e:
                print(e)
