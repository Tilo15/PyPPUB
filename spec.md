# PPUB - Portable PUBlication

## Magic Number

A PPUB file must start with the magic number `"ppub\n"`

## Asset Index

The asset index must follow the magic number. The first line of the asset index is the length in bytes (excluding the first line) of the asset index.

Entries in the index are separated by newline `'\n'` characters.

Each asset has a filename which may contain any character except newline and colon (`:`). Filenames are delemited by a colon and space `": "` character sequence.

Each value following the `: ` sequence is terminated either by a space or the end of the entry (`'\n'`). The first values are:

1. The mimetype of the asset
2. The start of the asset's data (bytes relative to the end of the asset index)
3. The end of the asset's data (bytes relative to the end of the asset index)

Optional flags may be added after the 3rd value, such as `"gzip"` to indicate that the asset has been compressed with GZip.

Entries containing optional flags not understood by the application should be ignored.

Non-official application specific flags should be prefixed with `"x-"`.

The officially supported flags are:

* `gzip` specifies that the asset is compressed with GZip.
* `licence` specifies that the asset is the licence that the publication is under.

The first entry in the asset index **must** be the metadata object. The second entry in the asset index **must** be the initial markdown file to show (i.e. the "cover" of the publication).

An example of an asset index could look like this:

```
121
metadata: application/x-ppub-metadata 0 64
PPUB Specification: text/markdown 64 548 gzip
ppub-logo.png: image/png 548 720
```

## Metadata

An asset named `"metadata"` **must** exist as the fist asset in a PPUB file with the mimetype `"application/x-ppub-metadata"`.

The metadata object is a collection of field-values. The field name is delimited by a space character, and the field value is delimited by a newline character.

Non-official metadata fields should be prefixed with `"x-"`. However it is encouraged to add application specific metadata by adding assets with application specific flags instead.

All metadata fields are optional.

The official metadata fields are:

* `title` publication title, string.
* `author` publication author, string with optional email address enclosed in angle brackets (e.g. `"John Doe <john@doe.com>"`)
* `date` publication date, ISO 8601 format.
* `description` a text blurb of the publication, string.
* `tags` comma separated tags for the publication used for indexing, string.
* `copyright` copyright information, string.