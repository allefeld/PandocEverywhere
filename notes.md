# TODO

-   fix convert to work with de-newlined HTML
    info: pandoc does not touch anything within `<script>` at all

-   remove data-mce-* attributes

-   styling via inlining?
    configure style per host?
    see https://premailer.io/, https://github.com/Automattic/juice
    remove (redundant) styles upon conversion. or all, just keep classes
    ```python
    from lxml import html
    tree = html.fromstring(html_content)
    for el in tree.iter():
    if 'style' in el.attrib:
        del el.attrib['style']
    ```
    also useful for following


# Info

In Brave, filtering of localhost needs to be explicitly disabled:
```
@@||localhost^
@@||127.0.0.1^
```

In VS Code, trust the containing folder once.


# Test

With Outlook: <https://outlook.office.com/mail/drafts>

With Moodle: <https://moodle4.city.ac.uk/blocks/quickmail/compose.php?courseid=15270>

With TinyMCE Demo: <https://www.tiny.cloud/docs/tinymce/latest/full-featured-premium-demo/>


# Recommended HTML Content

https://www.reddit.com/answers/196c9712-4e85-4fac-bc2d-b583143cb644/
https://premailer.dialect.ca/

Start from h3
