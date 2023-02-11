import os, json

def buildresourcemap(base):
  assets={}
  rootdir = os.getcwd() + os.sep
  for subdir, dirs, files in os.walk(rootdir + base):
      for file in files:
          category = (subdir.rsplit(os.sep, 1))[1]
          resourcepath = subdir + os.sep + file
          resourcetype = file[-3:]
          if resourcepath.endswith(('jpg', 'png')):
              relpath = resourcepath.rsplit(rootdir, 1)[1]       
              if not (assets.get(category, None)):
                  assets[category] = category
                  assets[category] = {'jpg': [], 'png': []}
              assets[category][resourcetype].append('.' + relpath)
  return assets

def buildimagehtml(floatval, source, alt, width, padding):
  html = ' <div style="float:{float}"><img src="{source}" alt="{alt}" width="{width}" style="padding: {padding}"/></div>'
  
  html = html.replace('{float}', floatval)
  html = html.replace('{source}', source)
  html = html.replace('{alt}', alt)
  html = html.replace('{width}', width)
  html = html.replace('{padding}', padding)

  return html

def buildmd(assets):
    clear = '<div style="clear: both"></div>' + '\n\n'
    md = ''
    for key in sorted(assets.keys()):
      md += clear
      md += '\n# ' + key + '\n'
      
      if len (assets[key]['jpg']) > 0:
        md += '## jpg\n<div style="float: left">\n'
        for asset in assets[key]['jpg']:
          md += buildimagehtml('left', asset, key, '100px', '0.5em') + '\n'
        md += '</div>\n' + clear

      if len (assets[key]['png']) > 0:
        md += '## png\n<div style="float: left">\n'
        for asset in assets[key]['png']:
          md += buildimagehtml('left', asset, key, '200px', '0.5em') + '\n'
        md += '</div>\n' + clear

    return md

assets = buildresourcemap('/brand')
print(json.dumps(assets, indent=4)) 
md = buildmd(assets)
print(md)

with open("README.md", "w") as textfile:
    textfile.write(md)