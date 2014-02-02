# coding=utf-8
import dropbox
import _config as conf
from wordpressAPI import Wordpy

# load list of images current on blog
def load_img_list():
    ret = []

    with open(conf.IMG_DIR + '/list.txt', 'rb') as f:
        for line in f:
            ret.append(line.rstrip())

    return ret

# get images currently on dropbox
def load_dp_img_list():
    ret = []

    try:
        client = dropbox.client.DropboxClient(conf.DP_TOKEN)
        folder_metadata = client.metadata(conf.DP_IMG_DIR)

        # go through content
        for item in folder_metadata['contents']:
            if 'image' in item['mime_type']:
                # append only the imagew with FH 'tag'
                if 'FH' in item['path']:
                    ret.append(item['path'].split('/')[-1])


    except dropbox.rest.ErrorResponse as e:
        print e.traceback()
        print 'load_dp_img_list() faield..'
        print 'Token may have expired..'

    return ret


# download from dropbox
def download_images(to_download):
    client = dropbox.client.DropboxClient(conf.DP_TOKEN)
    for img in to_download:
        print 'downloading ' + img + '...'
        # get from dropbox
        img_f = client.get_file(conf.DP_IMG_DIR + '/' + img)

        print 'saving ' + img + '...'
        # save to local img drive
        with open(conf.IMG_DIR + '/' + img, 'wb') as out:
            out.write(img_f.read())

    return True
 
# upload to folsomhasook.wordpress.com
def upload_images(to_upload):
    # intialize wp wrapper
    wpy = Wordpy(conf.WP_FOLSOM_TOKEN)

    for img in to_upload:
        print 'Uploading ' + img + '...'

        img_datetime = parse_datetime(img)

        # form  title
        title = img_datetime['pretty_date'] + u' ' + img_datetime['pretty_time']

        # create post
        wpy.create_post(title=title, categories='식사', img=conf.IMG_DIR + '/' + img)

        print 'Uploading ' + img + ' done!'

# pare date and time based on image name
# useful for my android phone
# format: IMG_<YYYYMMDD>_<HHMMSS>
def parse_datetime(filename):
    ret = dict()

    split_f = filename.split('_')

    ret['date'] = split_f[1]
    ret['time'] = split_f[2]

    # prettify date and time
    ret['pretty_date'] = split_f[1][4:6] + u'월 ' + split_f[1][6:] + u'일'

    if int(split_f[2][0:2]) < 12:
        ret['pretty_time'] = u'아침'
    elif int(split_f[2][0:2]) < 17:
        ret['pretty_time'] = u'점심'
    else:
        ret['pretty_time'] = u'저녁'

    return ret

# compare two lists,
# downloads missing images
# upload to blog
# updates local list
def run():
    local = load_img_list()
    repo = load_dp_img_list()

    print 'locally available images: '
    print local

    print 'images on dropbox:'
    print repo
    print ''

    # compare and get list of images to download
    to_download = [img for img in repo if img not in local]
    print 'images to upadate:'
    print to_download
    print

    # download missing images
    print 'downloading images...'
    download_images(to_download)

    print 'IMG DOWNLOAD DONE!'
    print 

    # upload to wordpress
    print 'uploading to wordpress...'
    upload_images(to_download)

    print 'IMG UPLOAD DONE!'
    print 

    # update local list
    print('updating local list...')
    with open(conf.IMG_DIR + '/list.txt', 'wb') as local_f:
        print '\n'.join(repo)
        local_f.write( '\n'.join(repo) )
    print 'UPDATING LOCAL LIST DONE!'
    print 

    print 'SEE YOU LATER!'


    return True

if __name__ == '__main__':
    #print update_blog()
    #print parse_datetime(u'IMG_20140201_182313')['pretty_time']
    #print parse_datetime(u'IMG_20140201_182313')['pretty_date']
    run()
