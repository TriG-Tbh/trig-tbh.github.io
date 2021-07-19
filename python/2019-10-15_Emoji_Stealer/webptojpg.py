def convert(mypath):

    import glob, os
    from PIL import Image
    os.chdir(mypath)

    for my_file in glob.glob("*"): 
        if not my_file.endswith('.webp') and not my_file.endswith(".gif"):
            base = os.path.splitext(my_file)[0]
            os.rename(my_file, base + '.webp')
        
    for my_file in glob.glob("*"):
        if not my_file.endswith(".jpg") and not my_file.endswith(".gif"):
            im = Image.open(my_file).convert("RGBA")
            #my_file = my_file.replace(".webp", '')
            file, _ = my_file.split('.')
            im.save(file + ".png","png")

    for my_file in glob.glob("*"):
        if my_file.endswith('.webp') and ('.jpg' not in my_file):
            os.remove(my_file)

    for my_file in glob.glob("*"):
        if my_file.endswith(".gif"):
            im = Image.open(my_file).convert("RGB")
            im.save(file + ".gif")
        