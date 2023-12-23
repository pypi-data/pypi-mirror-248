import os
import textwrap

import yaml

from cloudmesh.common.util import readfile


class Converter:
    """
    Converter Class

    This class provides methods for converting catalog entries to various formats, including BibTeX, Hugo Markdown,
    and regular Markdown.

    Methods:
        - __init__(filename=None, template=None): Initializes the Converter instance.
        - dedent(text): Dedents the specified text.
        - template(): Generates a template based on the Converter data.
        - bibtex(): Generates a BibTeX entry based on the Converter data.
        - hugo_markdown(): Generates a Hugo Markdown entry based on the Converter data.
        - markdown(): Generates a regular Markdown entry based on the Converter data.

    Attributes:
        - content: The content of the catalog entry file.
        - template_form: The template form for formatting the output.
        - data: Parsed data from the catalog entry file.

    Usage:
        converter = Converter(filename='path/to/catalog.yaml', template='path/to/template.txt')
        template_result = converter.template()
        bibtex_result = converter.bibtex()
        hugo_markdown_result = converter.hugo_markdown()
        markdown_result = converter.markdown()
    """

    def __init__(self, filename=None, template=None):
        """
        Initializes the Converter instance.

        Args:
            filename (str): The path to the catalog entry file.
            template (str): The path to the template file.

        Raises:
            ValueError: If the specified file cannot be found.

        Returns:
            None
        """
        # data/catalog/azure/bot_services.yaml"
        if not os.path.exists(filename):
            raise ValueError("file can not be found")
        self.content = readfile(filename)
        self.template_form = None
        if template is not None:
            self.template_form = readfile(template)
        self.data = yaml.safe_load(self.content)
        self.data["edit_url"] = "https://github.com/laszewsk/nist/blob/main/catalog/" + \
                                str(filename).split("catalog/")[1]
        day, month, year = str(self.data["modified"]).split("-")
        import calendar

        self.data["label"] = "wrong"
        self.data["title"] = self.data["name"]
        self.data["year"] = year
        self.data["month"] = calendar.month_abbr[int(month)].lower()

        self.data["url"] = self.data["documentation"]
        if "http" not in self.data["url"]:
            raise ValueError("url not found")

    def dedent(self, text):
        """
        Dedents the specified text.

        Args:
            text (str): The text to be dedented.

        Returns:
            str: The dedented text.
        """
        return textwrap.dedent(text).strip() + "\n"

    def template(self):
        """
        Generates a template based on the Converter data.

        Returns:
            str: The generated template.
        """
        return self.dedent(self.template_form.format(**self.data))

    def bibtex(self):
        """
        Generates a BibTeX entry based on the Converter data.

        Returns:
            str: The generated BibTeX entry.
        """
        bibtex_entry = """
        @misc{{{id},
          title={{{title}}},
          name={{{name}}},
          author={{{author}}},
          howpubllished={{Web Page}},
          month = {month},
          year = {{{year}}},
          url = {{{url}}}
        }}
        """
        return self.dedent(bibtex_entry.format(**self.data))

    def hugo_markdown(self):
        """
        Generates a Hugo Markdown entry based on the Converter data.

        Returns:
            str: The generated Hugo Markdown entry.
        """
        for entry in ["tags", "categories"]:
            self.data[entry] = "\n".join(["- " + value for value in self.data[entry]])

        # description: {description}
        # author: {author}

        markdown_entry = textwrap.dedent("""
        ---
        date: {modified}
        title: {title}
        tags: 
        {tags}
        categories: 
        {categories}
        linkTitle: MISSING
        draft: False         
        github_url: {edit_url}
        ---
                
        {{{{% pageinfo %}}}}
        {description}
        {{{{% /pageinfo %}}}}
        
        ## Description
        
        {description}

        ## Version
        
        {version}

        ## Documentation
        
        {documentation}
        
        ## SLA
        
        {sla}
        
        ## Data
        
        {data}
        """)
        return self.dedent(markdown_entry.format(**self.data))

    def markdown(self):
        """
         Generates a regular Markdown entry based on the Converter data.

         Returns:
             str: The generated regular Markdown entry.
         """
        self.d
        self.data["tags"] = ", ".join(self.data["tags"])
        self.data["categories"] = ", ".join(self.data["categories"])
        markdown_entry = """
        # {title}
        
        * Author: {author}
        * Version: {version}
        * Modified: {modified}
        * Created: {created}
        * <{documentation}>
        * Tags: {tags}
        * Categories: {categories}
        
        ## Description

        {description}
        
        ## SLA
        
        {sla}
        
        ## Data
        
        {data}
        """
        return self.dedent(markdown_entry.format(**self.data))
