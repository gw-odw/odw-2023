# Solutions

This directory contains encrypted versions of the solution files (stored as
`.ipynb.gpg`). We keep these encrypted before the ODW to encourage users to
have a go themselves. If you have access the to key, you can unencrypt these
files by running

```
$ gpg -o <FILENAME.ipynb> -c <FILENAME.ipynb.gpg>
```
and replacing `FILENAME` with the tutorial you wish to decrypt.
