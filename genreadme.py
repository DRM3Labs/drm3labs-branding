#  @license
#  Copyright 2023 DRM3 Labs Corp
#  SPDX-License-Identifier: Apache-2.0

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

def buildimagehtml(source, width, padding):
  html = '  <img src="{source}" width="{width}" style="padding: {padding}" style="margin: {padding}"/>'
  
  html = html.replace('{source}', source)
  html = html.replace('{width}', width)
  html = html.replace('{padding}', padding)

  return html

def buildassetsmd(assets):
    clear = '<div style="clear: both"></div>' + '\n\n'
    md = ''
    for key in sorted(assets.keys()):
      md += clear
      md += '\n## ' + key + '\n'
      
      if len (assets[key]['jpg']) > 0:
        md += '### jpg\n<div style="float: left">\n'
        for asset in assets[key]['jpg']:
          
          md += buildimagehtml(asset, '140px', '2em') + '\n'
        md += '</div>\n' + clear

      if len (assets[key]['png']) > 0:
        md += '### png\n<div style="float: left">\n'
     
        for asset in assets[key]['png']:
          md += buildimagehtml(asset, '140px', '2em') + '\n'
        md += '</div>\n' + clear

    return md

def buildcolormd(color):
  html = "\n  <div style='float: left; margin: 1.75em; background-color: {color}; width: 6em; height: 6em; padding: 10px;'>{color}</div>"
  return html.replace('{color}', color)

def buildcolorsmd():
  html = "# colors\n"
  html += "<div style='color: black;'>{colorshtml}\n</div>\n"
  colorshtml = buildcolormd('#FDC003')
  colorshtml += buildcolormd('#05A154')
  colorshtml += buildcolormd('#2F9CFB')
  colorshtml += buildcolormd('#FB3D8E')
  colorshtml += buildcolormd('#D3D3D3')
  colorshtml += buildcolormd('#FFFFFF')
  html = html.replace('{colorshtml}', colorshtml)
  return html

def buildwarningmd():
  return "\n\n<!---WARNING:  This file is autogenerated by genreadme.md--->\n\n"

def buildheadermd():
  md  = '<a href="{license}">&copy; Copyright 2023 drm3labs.io</a>\n\n'
  md = md.replace('{license}', './LICENSE.txt')
  md += '<p style="font-style: italic;">This file is auto-generated.</p>'
  return md

assets = buildresourcemap('/brand')
print(json.dumps(assets, indent=4)) 

md = buildwarningmd() + buildheadermd() + buildassetsmd(assets)
print(md)

with open("README.md", "w") as textfile:
    textfile.write(md)