
```markdown
# File Upload Script

This script allows uploading files and directories to a remote server via PHP.

## Usage

### Upload a directory

```python
upload_dir(
    base_url="https://example.com", 
    remote_directory="testdir",
    localdir_path="test/",
    username="user",
    password="pass"
)
```

### Upload a single file

```python  
upload_file(
    local_file="test/1.jpg",
    base_url="https://example.com",
    directory="testdir", 
    username="user",
    password="pass"
)
```

### Upload a file from a URL

```python
upload_file_from_url(
    url="https://example.com/file.jpg",
    base_url="https://example.com",
    directory="testdir",
    username="user",
    password="pass"  
)
```

### Upload via curl

Loop through files:

```bash
count=1
for file in somefile*; do
  curl -u USER:PASSWORD -T "$file" "https://example.com/remote.php/dav/files/USER/PATH/TO/FILE/$file"
  let count=count+1 
done
```

Single file:

```bash
curl -u USER:PASSWORD -T somefile "https://example.com/remote.php/dav/files/USER/PATH/TO/FILE/file"
```

Replace `USER`, `PASSWORD`, `PATH/TO/FILE` with your credentials and target directory.
```