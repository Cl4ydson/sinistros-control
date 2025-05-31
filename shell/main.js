const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let backend;
function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
    },
  });
  win.loadFile(path.join(__dirname, "../frontend/dist/index.html"));
}

app.whenReady().then(() => {
  // inicia backend.exe (porta 8000)
  const exePath = path.join(__dirname, "..", "backend", "dist", "backend.exe");
  backend = spawn(exePath);
  backend.stdout.on("data", (d) => console.log(`[BACKEND] ${d}`));
  backend.stderr.on("data", (d) => console.error(`[BACKEND] ${d}`));

  createWindow();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
  backend && backend.kill();
});
