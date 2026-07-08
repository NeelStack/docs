---
document_id: NES-401
title: Capacitor Architecture
subtitle: Enterprise Capacitor Config, Development Workflows & Native Sync Standards
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Team
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-400 Capacitor Mobile Standards
next_document: NES-402 Navigation
---

# NES-401 — Capacitor Architecture

> **"Capacitor bridges the gap between web platforms and native wrappers. We treat the web build as the source of truth, compiling and syncing web assets directly into native iOS and Android containers."**

---

# Executive Summary

Capacitor wraps a standard modern web application inside a secure, high-performance native WebView container, exposing native APIs (biometrics, push notifications, storage, network access) via an asynchronous JavaScript-to-Native bridge.

This standard establishes the configuration layouts (`capacitor.config.ts` and `vite.config.ts`), native synchronization procedures, and build processes required for all NeelStack Capacitor-based mobile applications.

---

# Purpose

This standard defines:

- Capacitor Configuration (`capacitor.config.ts`)
- Vite Configuration (`vite.config.ts`) for mobile builds
- Directory Structure & Platform Folder Policies
- The Sync Lifecycle (`npx cap sync`)
- Development running and debugging using Live Reload
- Custom Native Plugins integration

---

# Configuration Standards

We use standard TypeScript for the Capacitor and Vite configurations to enable type safety and dynamically inject environment flags.

### 1. Capacitor Configuration (`capacitor.config.ts`)

```typescript
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.neelstack.portal',
  appName: 'NeelStack Portal',
  webDir: 'dist',
  bundledWebRuntime: false,
  server: {
    androidScheme: 'https',
    iosScheme: 'https'
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: '#6366F1',
      androidSplashResourceName: 'splash',
      iosSplashResourceName: 'Default'
    }
  }
};

export default config;
```

### 2. Vite Configuration (`vite.config.ts` for Mobile)

Ensure the build output directory matches `webDir` in the Capacitor config (default `dist`):

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom', 'zustand'],
        },
      },
    },
  },
});
```

---

# Directory Structure & Platform Folder Policies

Unlike temporary build folders in React Native/Expo Managed configurations, the `/ios` and `/android` directories in Capacitor represent the native wrappers and **must be committed to git**.

- **Web Source of Truth**: All components, routing, layouts, and styles are maintained in `src/`. No editing of native code in Xcode/Android Studio is allowed unless writing custom native plugins.
- **Native Project Settings**: Re-sign parameters, package bundles, and entitlements are configured once inside Xcode (`App.xcodeproj`) and Android Studio (`build.gradle`) and committed.

---

# Sync Lifecycle

Capacitor functions by building the web assets first and then copying them to native platform projects.

```text
  Web Build: npm run build (writes to /dist)
                      │
                      ▼
   Capacitor Copy: npx cap copy (copies /dist to platforms)
                      │
                      ▼
  Plugin Update: npx cap update (syncs native plugins / npm packages)
                      │
                      ▼
  Unified Standard: npx cap sync (runs both copy and update)
```

### Standard Developer Routine:
```bash
# 1. Build the web app
npm run build

# 2. Sync code and plugins to native folders
npx cap sync

# 3. Compile and open in device/emulator
npx cap run ios
npx cap run android
```

---

# Live Reload & Debugging

During active development, building the web assets on every change is slow. We enforce the use of **Live Reload** to connect native emulators directly to the Vite dev server.

- **Vite Server**: Ensure Vite is bound to local interface: `npm run dev -- --host`
- **Capacitor Configuration override (Temporary only; never commit this to production)**:
```typescript
server: {
  url: 'http://192.168.1.50:5173', // Developer local IP
  cleartext: true
}
```

---

# Anti-Patterns

❌ **Committing Live Reload Server URL**: Leaving the dev server IP address inside the production `capacitor.config.ts` configuration, causing production builds to fail to load.

❌ **Direct Native File Editing**: Modifying the native storyboard layout or Java helper files directly in native directories instead of writing clean Web-based UI features.

❌ **Running Sync Without Build**: Invoking `npx cap sync` before compilation, copying stale web artifacts to mobile wrappers.

---

# Production Checklist

- [ ] `dist` folder matches the compiled production web package.
- [ ] iOS bundle ID (`com.neelstack.portal`) and Android package names are aligned.
- [ ] Splash screens and launcher icons are generated and placed in native directories.
- [ ] Cleartext configurations are removed from the production server configs.
- [ ] `npx cap sync` completes successfully without dependency mismatch errors.

---

# Success Criteria

The Capacitor configuration is successful when:
- Running `npm run build && npx cap sync` compiles the web bundle and populates platform projects correctly.
- Emulators launch the compiled bundle successfully in local developer sandboxes.
- Web assets load dynamically under local live-reload debugging.

---

# Document Status

**Document:** NES-401 — Capacitor Architecture
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-402 — Navigation**
