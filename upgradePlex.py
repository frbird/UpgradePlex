import requests
import os

url = 'https://plex.tv/api/downloads/5.json?channel=plexpass'
token = '*********'

def main():
    d = get_latest_version()
    current_version = os.popen("dpkg-query -W -f='${Version}' plexmediaserver").read()

    # Check to be sure the currently installed version is not the latest.
    if current_version == d['version']:
        print('Currently install version is the latest.')

    # Check to be sure file hasn't already been downloaded.
    elif current_version != d['version'] and os.path.exists(d['filename']):
        print('Latest version is already downloaded. ')
        install_plex(d['filename'], d['version'])

    # Download latest version and install.
    else:
        download_plex(d['download_url'], d['filename'], d['version'])
        install = install_plex(d['filename'], d['version'])
        if install == 0:
            print('Plex has successfully been updated to version %s. ' % d['version'])
            print('Removing installation file.  %s' % d['filename'])
            if os.remove(d['filename']) == 0:
                print('Success! ')
            else:
                print('Removing %s failed.  Please cleanup manually. ' % d['filename'])
        else:
            print('Upgrade failed for some reason. ')

#Get information about the latest version of PMS
def get_latest_version():
    try:
        r = requests.get(url, headers={'X-Plex-Token': token}).json()
        latest_version = r['computer']['Linux']['version']
        download_url = r['computer']['Linux']['releases'][1]['url']

        filename = str(download_url.split('/')[-1])

        data = {
            'download_url': download_url,
            'filename': filename,
            'version': latest_version
            }

        return data
    except:
        print('Could not get latest PMS info for some reason')

#Download PMS
def download_plex(url, filename, version):
    try:
        download = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(download.content)
            print('Downloading Plex version: %s' % str(version))
    except:
        print('Could not download PMS for some reason')

#Install PMS
def install_plex(filename, version):
    print('Upgrading Plex to version: %s' % version)
    result = os.system('sudo dpkg --install ' + filename)
    return result

if __name__ == '__main__':
    main()