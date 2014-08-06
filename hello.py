from flask import Flask, jsonify, request
import os, time

app = Flask(__name__)

# GET interface
@app.route('/', methods=['GET'])
def index():
  return '<script src="/script"></script>'


# GET script file
@app.route('/script', methods=['GET'])
def script():
  file = open('script.js', 'r')
  scriptFile = file.read()
  file.close()
  return scriptFile

# GET File or Folder
@app.route('/rest', methods=['GET'])
def rest():
  try:
    reqpath = request.args['path']
  except:
    reqpath = './'
  try:
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(reqpath)
  except OSError:
    return jsonify({'error':'Improper path'})
  res = {
    "name": reqpath,
    "created": ctime,
    "modified": mtime,
    "size": size
  }
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