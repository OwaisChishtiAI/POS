const electronInstaller = require('electron-winstaller');
const path = require('path');

const rootPath = path.join('./');

resultPromise = electronInstaller.createWindowsInstaller({
    appDirectory: './Store-POS-release-builds-POS-win32-x64-win32-x64',
    outputDirectory: './exes',
    authors: 'Hosting Domain',
    noMsi: true,
    exe: 'Store-POS-release-builds-POS-win32-x64.exe',
    setupExe: 'POSInstaller.exe',
    setupIcon: path.join(rootPath, 'assets', 'images', 'logo.ico')
  });

resultPromise.then(() => console.log("It worked!"), (e) => console.log(`No dice: ${e.message}`));