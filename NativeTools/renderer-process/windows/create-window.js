const BrowserWindow = require('electron').remote.BrowserWindow
const path = require('path')

const ipc = require('electron').ipcRenderer

const selectDirBtn = document.getElementById('new-window')

selectDirBtn.addEventListener('click', function (event) {
  ipc.send('open-file-dialog')
})

ipc.on('selected-directory', function (event, path) {
  var fileHandle=path;
  //document.getElementById('selected-file').innerHTML = `You selected: ${path}`
})





