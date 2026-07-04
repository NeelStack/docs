---
document_id: NES-410
title: Mobile Performance
subtitle: Enterprise Mobile Performance, Hermes, Rendering & Profiling Standard
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

> **"Unresponsive mobile interfaces lead to uninstalled applications. We target constant 60/120 FPS rendering, rapid boot times, and low memory utilization."**

---

# Executive Summary

Mobile applications run on varied hardware profiles, from high-end flagship phones to low-cost budget devices.

Poor performance shows up as stuttering scroll feeds, lagging animations, long app startup screens, and device overheating.

This standard outlines the configurations, coding rules, component layouts, and diagnostic profiling tools to optimize performance across both iOS and Android.

---

# Purpose

This standard defines:

- JavaScript Engine Standard (Hermes)
- Image Caching and Rendering (Expo Image)
- List Rendering Optimization (FlatList / FlashList)
- Layout Computation and Rendering Optimizations
- Performance Profiling and Monitoring Tools

---

# JavaScript Engine (Hermes)

All NeelStack mobile applications must compile and run on the **Hermes JavaScript Engine**.

- **Hermes Advantages**: Pre-compiles JS code into bytecode during the build process, reducing application startup time, lowering memory footprint, and improving CPU utilization.
- **Rule**: Enable Hermes inside `app.json` config settings:

```json
{
  "expo": {
    "jsEngine": "hermes"
  }
}
```

---

# Image Optimization (Expo Image)

Images are the most common source of memory bloat in mobile applications.

- **Standard**: Do not use the standard React Native `Image` component. Use **`expo-image`** (powered by SDWebImage on iOS and Glide on Android).
- **Benefits**: Cross-platform disk caching, progressive image loading, vector graphics support, and automatic performance tuning.

```typescript
import { Image } from 'expo-image';

export function Avatar({ url }: { url: string }) {
  return (
    <Image
      source={url}
      placeholder="blur-hash-placeholder-string"
      contentFit="cover"
      transition={200} // Smooth crossfade animation
      style={{ width: 50, height: 50, borderRadius: 25 }}
    />
  );
}
```

---

# List Rendering (FlashList)

For rendering large feeds of data (e.g. hundreds of documents, logs, or feed updates), avoid standard `ScrollView` and `FlatList`.

- **Standard**: Use **`@shopify/flash-list`**.
- **Performance**: FlashList recycles cell views instead of constantly creating and destroying them, preventing frame drops during quick scrolling.

### Implementation Checklist:

1. Specify `estimatedItemSize`: FlashList requires this property to optimize scroll physics.
2. Avoid complex view structures inside render items. Keep children structures flat.

```typescript
import { FlashList } from '@shopify/flash-list';

export function DocumentList({ items }: { items: Document[] }) {
  return (
    <FlashList
      data={items}
      renderItem={({ item }) => <DocumentRow item={item} />}
      estimatedItemSize={80} // Average height of rows in pixels
    />
  );
}
```

---

# Component Render Optimization

Prevent unnecessary re-renders that throttle the JavaScript thread:

- **Memoization**: Wrap static UI layouts or complex rows in `React.memo` to prevent re-rendering when parent states shift.
- **Reference Hooks**: Use `useCallback` for event handlers passed to children and `useMemo` for heavy data mapping operations.
- **Batching state**: Utilize React 18 automatic batching to group multiple state transitions.

```typescript
// Memoized row component
export const DocumentRow = React.memo(({ item }: { item: Document }) => {
  return (
    <View className="p-4 border-b border-slate-200">
      <Text>{item.title}</Text>
    </View>
  );
});
```

---

# Profiling and Diagnostics

Developers must profile their applications before committing major features.

- **Tools**:
  - **React DevTools Profiler**: Measure component render durations and identify unnecessary updates.
  - **Flipper / Hermes Debugger**: Track memory allocations, identify memory leaks, and profile CPU execution patterns.
  - **Xcode Instruments (iOS)** / **Android Studio Profiler**: Trace native CPU usage, memory leaks, and GPU render paths.

---

# Anti-Patterns

❌ **Anonymous Arrow Functions in JSX**: Declaring functions inline like `<Button onPress={() => doStuff()} />` inside list rendering loops. This creates new function instances on every render.

❌ **Raw Unoptimized Images**: Loading massive high-res photos (e.g. 5MB raw uploads) straight into layout cards without scaling or compression.

❌ **Nested ScrollViews**: Nesting scroll containers in the same direction, which breaks virtual scrolling calculations and drops frame rates.

---

# Production Checklist

- [ ] Hermes engine is verified as active in production build configurations.
- [ ] Image assets pass through optimized image cache handlers.
- [ ] All FlashList components have an accurate `estimatedItemSize` set.
- [ ] Profiler runs confirm zero continuous re-renders.
- [ ] Flipper check verifies no memory leaks exist on view transitions.

---

# Success Criteria

The Performance standards are successful when:
- App launch to interactive (TTI) completes in less than 2.0 seconds on mid-range devices.
- Thread frames remain at 60 FPS (or matching refresh rate) during rapid list scrolling.
- Memory usage profile remains stable under continuous usage (no memory leaks on navigation loop).

---

# Document Status

**Document:** NES-410 — Mobile Performance
**Version:** 1.0.0
**Status:** Ready for Review
**Next Document:** **NES-411 — Testing**
