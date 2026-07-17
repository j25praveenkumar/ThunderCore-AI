/**
 * Thunder AI — Electron Preload Script
 * Exposes safe APIs to the renderer process.
 */
const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('thunderAPI', {
  platform: process.platform,
  version:  process.env.npm_package_version || '1.0.0',
});
