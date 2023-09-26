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
    nc = nextcloud_client.Client(f"{base_url}")
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
    nc = nextcloud_client.Client(f"{base_url}")
    nc.login(username, passw)
    try:
        nc.mkdir(directory)
    except:
        pass
    # Get file size and create upload session

    name = local_file.split("/")[-1]
    nc.put_file(f"{directory}/{name}", local_file)

    return True


def zipandupload_directories(
    localdir_path, base_url, remote_directory, username, passw
):
    import shutil
    import os

    # list folders in local directory path

    folders = [
        f
        for f in os.listdir(localdir_path)
        if os.path.isdir(os.path.join(localdir_path, f))
    ]
    zipped = []
    uploaded = []
    if os.path.exists("zipped.txt"):
        zipped = open("zipped.txt", "r").readlines()[0].split(",")

    if os.path.exists("uploaded.txt"):
        uploaded = open("uploaded.txt", "r").readlines()[0].split(",")

    for folder in folders:
        dir_name = os.path.join(localdir_path, folder)
        output_filename = os.path.join(localdir_path, folder)
        print(f"Zipping {folder}")
        if folder not in zipped:
            shutil.make_archive(output_filename, "zip", dir_name)
            zipped.append(folder)
            with open("zipped.txt", "w") as f:
                f.write(",".join(zipped))
        print(f"Uploading {folder}")
        if folder not in uploaded:
            upload_file(
                local_file=f"{output_filename}.zip",
                base_url=base_url,
                directory=remote_directory,
                username=username,
                passw=passw,
            )
            uploaded.append(folder)
            with open("uploaded.txt", "w") as f:
                f.write(",".join(uploaded))

    print("Done")


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

zipandupload(
    localdir_path="test",
    base_url="https://nx36834.your-storageshare.de/",
    remote_directory="test",
    username="",
    passw="",
)

# via curl loop
# count=1
# for file in somefile*; do
#   curl -u USER:PASSWORD -T "$file" "{base_url}/remote.php/dav/files/{USER}/{PATH_TO_FILE}/$file"
#   let count=count+1
# done

# via curl
# curl -u USER:PASSWORD -T somefile "{base_url}/remote.php/dav/files/{USER}/{PATH_TO_FILE}/file"
