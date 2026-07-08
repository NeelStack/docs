---
document_id: NES-410
title: Mobile Performance
subtitle: Enterprise WebView Performance, Bundle Sizing & Virtualization Standard
version: 1.0.0
status: Draft
classification: Internal
owner: Mobile Architecture Board
review_cycle: Every 6 Months
document_type: Engineering Standard
parent_document: NES-409 Storage
next_document: NES-411 Testing
---

# NES-410 — Mobile Performance

> **"Unresponsive mobile interfaces lead to uninstalled applications. We target constant 60/120 FPS rendering inside WebViews, rapid TTI (Time to Interactive), and low memory footprint."**

---

# Executive Summary

Because Capacitor applications execute within WebView containers (System WebViews on Android, WebKit/WKWebView on iOS), performance is defined by DOM depth, asset size, JavaScript bundle optimization, and rendering efficiency.

Unoptimized layouts manifest as slow scroll response, thermal throttling, and high memory alerts.

This standard outlines rules for asset management, layout virtualizations, bundle optimizations, and diagnostic web profiling.

---

# Purpose

This standard defines:

- JavaScript engine runtime profiles (V8 vs. JavaScriptCore)
- Web bundle optimizations (Code splitting, Vite configurations)
- Image rendering optimizations in WebViews
- List Virtualization standards
- Web Inspector profiling and CPU tracing

---

# Runtime Engine & Bundle Optimizations

We rely on native web browser engines inside the container WebView:
- **Android**: Chromium-based V8 engine.
- **iOS**: Apple WebKit WKWebView.

To optimize load times, we must minimize bundle sizes and speed up JS parsing:
- **Code Splitting**: Wrap route configurations in React lazy loading (`React.lazy`) to prevent loading all views on boot.
- **Tree Shaking**: Configure Vite to eliminate unused exports.
- **Asset Minification**: Utilize ESBuild (enabled by default in Vite) to compress files.

---

# Image Optimization in WebViews

WebViews have less memory headroom than native apps. Loading multiple high-resolution images will trigger memory terminations.

1. **Format Standards**: Serve image resources in modern WebP or AVIF formats.
2. **Lazy Loading**: Apply the standard HTML attribute `loading="lazy"` on offscreen images.
3. **Dimensions Constraint**: Ensure image assets serve matching display dimensions (e.g. do not render a 5MB photo in a 40px avatar container).

```tsx
export function UserProfile({ avatarUrl }: { avatarUrl: string }) {
  return (
    <img
      src={avatarUrl}
      loading="lazy"
      alt="User Profile"
      className="w-10 h-10 rounded-full object-cover"
    />
  );
}
```

---

# List Virtualization

Standard list scrolls (`map` or simple lists) generate DOM elements for every array index, quickly slowing down rendering speed.

- **Standard**: For lists exceeding 100 entries, use virtualized list libraries such as **`@tanstack/react-virtual`** or **`react-window`**.
- **Virtualization Benefits**: Renders only the items visible in the viewport, maintaining a constant DOM depth regardless of array size.

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

export function VirtualList({ items }: { items: any[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const rowVirtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 60, // Fixed or estimated height in pixels
  });

  return (
    <div ref={parentRef} className="h-[400px] overflow-auto border border-slate-200 rounded">
      <div
        className="w-full relative"
        style={{ height: `${rowVirtualizer.getTotalSize()}px` }}
      >
        {rowVirtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            className="absolute top-0 left-0 w-full p-4 border-b border-slate-100"
            style={{
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            {items[virtualItem.index].title}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

# Profiling and Diagnostics

Mobile developers must profile applications using web inspectors connected to mobile emulators/devices.

- **Chrome DevTools (Android)**: Run `chrome://inspect` inside Google Chrome to inspect the Android WebView console, view rendering paint flashes, and trace JS execution paths.
- **Safari Web Inspector (iOS)**: Activate Safari Develop menu to connect to iOS Simulators, analyzing memory timelines and CSS animations.

---

# Anti-Patterns

❌ **Nesting Heavy Loops**: Writing nested loops inside component render blocks, which blocks WebView rendering frames (aim to execute logic within 16ms).

❌ **Using Scroll Listeners without Passive Flag**: Attaching scroll trackers to DOM elements without the `passive: true` listener configuration, which delays touch response.

---

# Production Checklist

- [ ] Route components are lazy loaded via code-splitting.
- [ ] Large list elements use `@tanstack/react-virtual` containers.
- [ ] Static images are scaled and served in WebP format.
- [ ] CSS transitions use `transform` and `opacity` to invoke GPU acceleration.

---

# Success Criteria

The Performance standards are successful when:
- App launch to interactive (TTI) is under 1.5 seconds on mid-range devices.
- Scroll paths maintain a steady 60 FPS (or 120 FPS on matching hardware displays).
- WebView memory timelines remain stable without continuous growth.

---

# Document Status

**Document:** NES-410 — Mobile Performance
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-411 — Testing**
