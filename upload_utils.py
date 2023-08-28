import nextcloud_client
import requests


def upload_dir(base_url, remote_directory, username, passw, localdir_path):
    nc = nextcloud_client.Client(f"{base_url}")
    nc.login(username, passw)
    try:
        nc.mkdir(remote_directory)
    except Exception as e:
        print(e)
        pass
    nc.put_directory(remote_directory, localdir_path)

    print("Done")


def upload_file_from_url(url, base_url, directory, username, passw):
    nc = nextcloud_client.Client(f"http://{base_url}")
    nc.login(username, passw)
    try:
        nc.mkdir(directory)
    except:
        pass
    # Get file size and create upload session
    file_to_go = requests.get(url)
    name = url.split("/")[-1]
    nc.put_file_contents(f"{directory}/{name}", file_to_go.content)
    link_info = nc.share_file_with_link(f"{directory}/{name}")
    return link_info.get_link()


def upload_file(local_file, base_url, directory, username, passw):
    nc = nextcloud_client.Client(f"http://{base_url}")
    nc.login(username, passw)
    try:
        nc.mkdir(directory)
    except:
        pass
    # Get file size and create upload session

    name = local_file.split("/")[-1]
    nc.put_file(f"{directory}/{name}", local_file)

    return True


# EXAMPLE USAGE
# upload_dir(
#     base_url="{place you want to upload}",
#     remote_directory="testdir",
#     localdir_path="test/",
#     username="user",
#     passw="pass",
# )

# upload_file(
#     local_file="test/1.jpg",
#     base_url="{place you want to upload}",
#     directory="testdir",
#     username="user",
#     passw="pass",
# )

# upload_file_from_url(
#     url="place you want to get file from",
#     base_url="{place you want to upload}",
#     directory="testdir",
#     username="user",
#     passw="pass",
# )

# via curl loop
# count=1
# for file in somefile*; do
#   curl -u USER:PASSWORD -T "$file" "{base_url}/remote.php/dav/files/{USER}/{PATH_TO_FILE}/$file"
#   let count=count+1
# done

# via curl
# curl -u USER:PASSWORD -T somefile "{base_url}/remote.php/dav/files/{USER}/{PATH_TO_FILE}/file"
