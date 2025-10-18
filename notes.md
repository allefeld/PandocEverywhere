# TODO

-   tidy HTML
-   does difference between Pandoc'ed (html+raw_html) and raw HTML make sense?
    maybe just Markdown vs tidied HTML → tidying becomes conversion.

-   delete / backup previous files
    function to restore previous version

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

-   implement in python
    ```js
    const html = editor.innerHTML
      .replace(/\s+data-mce-[^\s=]+="[^"]*"/g, "")
      .replace(/<!-- start raw html -->/g, "<script>")
      .replace(/<!-- stop raw html -->/g, "</script>");
    ```


# Info

Pandoc Server: <https://pandoc.org/pandoc-server.html>

In Brave, filtering of localhost needs to be explicitly disabled:
```
@@||localhost^
@@||127.0.0.1^
```



# Test

With Outlook: <https://outlook.office.com/mail/drafts>

With Moodle: <https://moodle4.city.ac.uk/blocks/quickmail/compose.php?courseid=15270>

With TinyMCE Demo: <https://www.tiny.cloud/docs/tinymce/latest/full-featured-premium-demo/>

With curl:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text": "Hi", "format": "markdown", "url": "nowhere"}' -D - http://localhost:5000/
```


# HTML Content

https://www.reddit.com/answers/196c9712-4e85-4fac-bc2d-b583143cb644/
https://premailer.dialect.ca/

Start from h3
