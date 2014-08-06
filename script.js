var _el = document.createElement.bind(document)
var _l = console.log.bind(console)
function _li (name, restpath) {
  anchor = _el('a')
  anchor.setAttribute('href', restpath)
  anchor.text = name
  anchor.addEventListener('click', function (event) {
    event.preventDefault()
    changePath(this.href)
    return false
  })
  item = _el('li')
  item.appendChild
  item.appendChild(anchor)
  return item
}
function _getpath (restpath, done) {
  var get = new XMLHttpRequest()
  get.onload = function () { done(JSON.parse(get.response)) }
  get.open('get', restpath, true)
  get.send()
}
// restpath: already encoded
function joinEncodePath (restpath, path) {
  path = restpath + encodeURIComponent('/' + path)
  return path.replace(/%2f%2f|%2f%2f%2f/ig, "%2f")
}
function changePath (path) {
  var restpath = path
  _getpath(path, function (data) {
    console.log(data)
    document.body.innerHTML = ""

    restPaths = restpath.split(/%2f/gi).slice(0,-1)
    document.body.appendChild( _li('../', restPaths.join('%2f') + (restPaths.length === 1?'%2f':'') ) )
    if(data.type === "file") {
      pre = _el('pre')
      pre.innerText = data.content
      document.body.appendChild(pre)
    } else {
      var path, i, len = data.content.length
      for(i = 0; i < len; i++) {
        path = data.content[i]
        document.body.appendChild( _li(path, joinEncodePath(restpath, path)) )
      }
    }
  })
}

changePath('/rest?path=%2F')
