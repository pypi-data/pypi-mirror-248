## Usage

Once installed usage is straight forward, to search for files with the defaults, looking in the current directory for
`jpg` files and outputting to `YYYY/mm/dd` directory structure in the current directory just invoke `mvdate`. the
`ctime` (creation time) of a file, which is immutable, is extracted and used as a basis for creating directories.

Thus, given a directory with the following files...

```bash
❱ l
drwxrwx--- user1 users 4.0 KB Sun Jan 29 07:04:17 2023  .
drwxrwxrwx user1 users 4.0 KB Mon Sep  4 21:38:15 2023  ..
.rw-rw---- user1 users 2.5 MB Fri Oct 23 08:57:20 2020  IMG_20201023_085720.jpg
.rw-rw---- user1 users 2.5 MB Fri Oct 23 08:57:24 2020  IMG_20201023_085725.jpg
.rw-rw---- user1 users 2.4 MB Fri May 20 07:51:04 2022  IMG_20210115_091528.jpg
.rw-rw---- user1 users 2.4 MB Fri May 20 07:51:04 2022  IMG_20210115_091530.jpg
.rw-rw---- user1 users 2.6 MB Fri Apr  1 10:35:44 2022  IMG_20220401_093544.jpg
.rw-rw---- user1 users 2.6 MB Fri Apr  1 10:35:46 2022  IMG_20220401_093546.jpg
.rw-rw---- user1 users 2.5 MB Sun Jan 29 05:21:28 2023  IMG_20220729_085918.jpg
.rw-rw---- user1 users 2.4 MB Sun Jan 29 05:21:28 2023  IMG_20220729_085951.jpg
.rw-rw---- user1 users 2.7 MB Sun Jan 29 05:24:40 2023  IMG_20221021_085226.jpg
.rw-rw---- user1 users 2.5 MB Sun Jan 29 05:24:40 2023  IMG_20221021_085231.jpg
```

To move them to `YYYY-mm-dd` directory just invoke `mvdate` as the default file extensions is `jpg` and the method used
is `exif` which extracts the `Created date` from the Exif data.

```bash
❱ mvdate
                       __      __
   ____ ___ _   ______/ /___ _/ /____
  / __ `__ \ | / / __  / __ `/ __/ _ \
 / / / / / / |/ / /_/ / /_/ / /_/  __/
/_/ /_/ /_/|___/\__,_/\__,_/\__/\___/


2023-12-27 10:12:18.553 | INFO     | Search directory                           : ./
2023-12-27 10:12:18.554 | INFO     | Searching for files with extension         : jpg
2023-12-27 10:12:18.554 | INFO     | Files found                                : 10
2023-12-27 10:12:18.554 | INFO     | Destination directory                      : ./
2023-11-04 09:12:12.887 | INFO     | Created target directory : 2020/10/23
2023-11-04 09:12:12.888 | INFO     | Created target directory : 2022/04/01
2023-11-04 09:12:12.888 | INFO     | Created target directory : 2022/05/20
2023-11-04 09:12:12.889 | INFO     | Created target directory : 2023/01/29
Moving 10 files.: 0it [00:00, ?it/s]
2023-11-04 09:12:12.911 | INFO     | Moved : IMG_20201023_085720.jpg -> ./2020/10/23/IMG_20201023_085720.jpg
2023-11-04 09:12:12.911 | INFO     | Moved : IMG_20201023_085725.jpg -> ./2020/10/23/IMG_20201023_085725.jpg
2023-11-04 09:12:12.912 | INFO     | Moved : IMG_20210115_091528.jpg -> ./2021/01/15/IMG_20210115_091528.jpg
2023-11-04 09:12:12.912 | INFO     | Moved : IMG_20210115_091530.jpg -> ./2021/01/15/IMG_20210115_091530.jpg
2023-11-04 09:12:12.913 | INFO     | Moved : IMG_20220401_093544.jpg -> ./2022/04/01/IMG_20220401_093544.jpg
2023-11-04 09:12:12.913 | INFO     | Moved : IMG_20220401_093546.jpg -> ./2022/04/01/IMG_20220401_093546.jpg
2023-11-04 09:12:12.913 | INFO     | Moved : IMG_20220729_085918.jpg -> ./2022/07/29/IMG_20220729_085918.jpg
2023-11-04 09:12:12.914 | INFO     | Moved : IMG_20220729_085951.jpg -> ./2022/07/29/IMG_20220729_085951.jpg
2023-11-04 09:12:12.914 | INFO     | Moved : IMG_20221021_085226.jpg -> ./2022/10/21/IMG_20221021_085226.jpg
2023-11-04 09:12:12.914 | INFO     | Moved : IMG_20221021_085231.jpg -> ./2022/10/21/IMG_20221021_085231.jpg
Moving 10 files.: 10it [00:00, 4648.94it/s]
```

If you wanted to search for files in one directory and output to the desired structure in a different directory you can
use the `-b`/`--base` option to specify the base directory to search and the `-d` / `--destination` option to specify
the destination directory.

``` bash
❱ mvdate -e jpg -b ~/pics/clearing -d ~/pics -m exif
                       __      __
   ____ ___ _   ______/ /___ _/ /____
  / __ `__ \ | / / __  / __ `/ __/ _ \
 / / / / / / |/ / /_/ / /_/ / /_/  __/
/_/ /_/ /_/|___/\__,_/\__,_/\__/\___/


2023-12-27 10:12:18.553 | INFO     | Search directory                           : ~/pics/clearing
2023-12-27 10:12:18.554 | INFO     | Searching for files with extension         : jpg
2023-12-27 10:12:18.554 | INFO     | Files found                                : 4
2023-12-27 10:12:18.554 | INFO     | Destination directory                      : ~/pics/
2023-12-27 10:12:18.562 | INFO     | Created target directory : ~/pics/2021/02/03
2023-12-27 10:12:18.562 | INFO     | Created target directory : ~/pics/2020/08/28
2023-12-27 10:12:18.563 | INFO     | Created target directory : ~/pics/2020/12/09
Moving 4 files.: 0it [00:00, ?it/s]
2023-12-27 10:12:18.564 | INFO     | Moved : selfie.jpg -> ~/pics/2021/02/03/selfie.jpg
2023-12-27 10:12:18.565 | INFO     | Moved : another.jpg -> ~/pics/2021/02/03/another.jpg
2023-12-27 10:12:18.565 | INFO     | Moved : IMG_20200828_100935.jpg -> ~/pics/2020/08/28/IMG_20200828_100935.jpg
2023-12-27 10:12:18.565 | INFO     | Moved : IMG_20201209_163230.jpg -> ~/pics/2020/12/09/IMG_20201209_163230.jpg
Moving 4 files.: 4it [00:00, 4735.76it/s]

```

You can disable all output by passing the `-q`/`--quiet` option.

**NB** If an image file has no Exif data for `Created date` then the `ctime` will be used.

## Options

The table below lists all command line options.

| Option (Short) | Option (Long) | Description                                                                                                                                                                                                                       |
|----------------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-v`           | `--version`   | Print out the version and exit.                                                                                                                                                                                                   |
| `-b`           | `--base`      | The base directory under which files are searched for.                                                                                                                                                                            |
| `-l`           | `--log_file`  | File to save log output to.                                                                                                                                                                                                       |
| `-m`           | `--method`    | Method used to extract date/time of file. Currently three options `exif` (default) which uses the `Created Date` field of Exif data of image files. For non-image files use either `ctime` or `mtime` for created/modified times. **NB** If an image is missing the `Created Date` field we default to `ctime`. |
| `-n`           | `--nesting`   | Level of nesting to move files to, should be a single letter, 'Y'ear, 'm'onth, 'd'ay (default), 'H'our, 'M'inutes.                                                                                                                |
| `-q`           | `--quiet`     | Execute quietly and suppress all output.                                                                                                                                                                                          |
| `-s`           | `--single`    | Whether to have a single directory of the form `YYYY-mm[-dd[-HH[-MM]]]` rather than a nested structure.                                                                                                                           |
