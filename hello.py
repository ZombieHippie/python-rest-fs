from flask import Flask, jsonify, request
import os, time

app = Flask(__name__)

# GET File or Folder
@app.route('/', methods=['GET'])
def index():
  try:
    reqpath = request.args['path']
  except AttributeError:
    reqpath = 'friends and date of birth.csv'
  try:
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(reqpath)
  except OSError:
    return jsonify({'error':'Improper path'})
  reqargsdict = request.args
  infodict = {
    "name": reqpath,
    "created": ctime,
    "modified": mtime,
    "size": size
  }
  res = dict(list(reqargsdict.items()) + list(infodict.items()))
  # Was having problems running stats on open file, so we separate the two
  # win mode or linux mode
  if mode == 16895 or mode == 16877:
    res["type"] = "directory"
    res["content"] = os.listdir(reqpath)
  elif mode == 33206 or mode == 33188:
    res["type"] = "file"
    file = open(reqpath, 'r')
    res["content"] = file.read()
    file.close()
  return jsonify(res)

if __name__ == '__main__':
  app.run(debug=True)