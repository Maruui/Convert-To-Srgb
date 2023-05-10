import io
import os
import os.path #trim last oath
from PIL import Image
from PIL import ImageCms
import shutil
from tkinter import Tk 
from tkinter import messagebox    # from tkinter import Tk for Python 3.x
# from tkinter.filedialog import askopenfilename
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
from tkinter.filedialog import askdirectory

try:
    Tk().withdraw()
    path = askdirectory()
    dir_list = os.listdir(path)
    # function 
    def convert_to_srgb(img):
        '''Convert PIL image to sRGB color space (if possible)'''
        icc = img.info.get('icc_profile', '')
        if icc:
            io_handle = io.BytesIO(icc)     # virtual file
            src_profile = ImageCms.ImageCmsProfile(io_handle)
            dst_profile = ImageCms.createProfile('sRGB')
            img = ImageCms.profileToProfile(img, src_profile, dst_profile)
        return img

    makepath = '{}/upload_snap'.format(os.path.dirname(path))
    try:
        os.mkdir(makepath)
    except FileExistsError:
        messagebox.showinfo("Alert", "Folder alery create")
    x=0
    # loop Convert to sRGB
    for i in dir_list:
        img = Image.open('{}/{}'.format(path,i))
        img_conv = convert_to_srgb(img)   
        if img.info.get('icc_profile', '') != img_conv.info.get('icc_profile', ''):
            
            # copy detail of image and push to new image
            exif = img.info['exif']
            # ICC profile was changed -> save converted file
            img_conv.save('{}/upload_snap/{}'.format(os.path.dirname(path),i),
                format = 'JPEG',
                quality = 100,
                exif=exif,
                icc_profile = img_conv.info.get('icc_profile',''))
        else:
            # if is sRBG just move to upload_snap
            shutil.copy('{}/{}'.format(path,i), '{}/upload_snap/{}'.format(os.path.dirname(path),i))
        # Check finish
        x+=1


    if(x==len(dir_list)):
        messagebox.showinfo("Notification", "Convert Success")

except:
    messagebox.showinfo("Alert", "Close programe")

